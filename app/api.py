from flask import Flask, request, jsonify, render_template
from .scanner import scan_text, load_rules
import uuid
import json

app = Flask(__name__, template_folder='templates')
policy_rules = load_rules()
scan_reports = {}

def load_mock_emails():
    with open('data/emails_mock.json', 'r') as f:
        return json.load(f)

mock_emails = load_mock_emails()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/emails/<inbox_name>", methods=['GET'])
def get_emails(inbox_name):
    """API endpoint to get mock emails from an inbox."""
    inbox = mock_emails.get(inbox_name, [])
    return jsonify(inbox)

@app.route("/scan", methods=['POST'])
def scan_document():
    if not request.json:
        return jsonify({"error": "Invalid request"}), 400

    text_to_scan = ""
    # Check if text is provided directly
    if 'text' in request.json and request.json['text']:
        text_to_scan = request.json['text']
    # If not, check if an inbox name is provided
    elif 'inbox' in request.json:
        inbox_name = request.json['inbox']
        inbox_content = mock_emails.get(inbox_name, [])
        # Combine the body of all emails in the inbox for scanning
        text_to_scan = "\n\n--- Next Email ---\n\n".join([email['body'] for email in inbox_content])
    else:
        return jsonify({"error": "Missing 'text' or 'inbox' in request body"}), 400

    scan_id = str(uuid.uuid4())
    results = scan_text(text_to_scan, policy_rules)
    scan_reports[scan_id] = {"original_text": text_to_scan, "violations": results}
    
    return jsonify({"scanId": scan_id})

@app.route("/reports/<scanId>", methods=['GET'])
def get_report(scanId):
    report = scan_reports.get(scanId)
    if not report:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report)