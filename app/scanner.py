import json
import re
import spacy
# ✅ 1. Matcher ki jagah PhraseMatcher import karo
from spacy.matcher import PhraseMatcher 

# Load the spaCy model once
nlp = spacy.load("en_core_web_sm")

def load_rules(filepath="rules/policy_rules.json"):
    with open(filepath, 'r') as f:
        return json.load(f)

def scan_text(text, rules_data):
    flagged_sentences = []
    
    doc = nlp(text)

    for rule in rules_data["rules"]:
        # Regex-based rules (yeh pehle se theek hai)
        if "pattern_regex" in rule:
            for match in re.finditer(rule["pattern_regex"], doc.text):
                for sent in doc.sents:
                    if match.start() >= sent.start_char and match.end() <= sent.end_char:
                        flagged_sentences.append({
                            "sentence": sent.text,
                            "rule_id": rule["id"],
                            "rule_name": rule["name"]
                        })
                        break
        
        # Keyword-based rules
        if "patterns" in rule:
            # ✅ 2. Matcher ki jagah PhraseMatcher use karo
            matcher = PhraseMatcher(nlp.vocab) 
            patterns_to_add = [nlp.make_doc(p["pattern"]) for p in rule["patterns"]]
            matcher.add(rule["id"], patterns_to_add)
            
            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                flagged_sentences.append({
                    "sentence": span.sent.text,
                    "rule_id": nlp.vocab.strings[match_id],
                    "rule_name": rule["name"]
                })

    return flagged_sentences