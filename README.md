# PolicyPulse – Internal Policy Compliance Checker

PolicyPulse is a web-based service that scans documents or emails to flag potential policy violations based on a defined set of rules. It provides a simple dashboard to view the flagged content.

## Features
- **Rule-Based Scanning**: Scans text for forbidden keywords and PII patterns using custom rules defined in a JSON file.
- **API-Driven**: Includes a Flask-based REST API to handle scan requests and reports.
- **Web UI**: A simple browser-based dashboard to paste text, scan inboxes, and view highlighted violations.
- **Mock Email Integration**: Simulates scanning email inboxes by fetching data from a mock JSON file.

## Technology Stack
- **Backend**: Python, Flask, Gunicorn
- **NLP**: spaCy (for Phrase Matching and Entity Recognition)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Deployment**: Docker, Render

## Project Setup and Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/policypulse.git](https://github.com/your-username/policypulse.git)
    cd policypulse
    ```
2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```
3.  **Run the application:**
    ```bash
    flask --app app.api run
    ```
4.  Open your browser and navigate to `http://127.0.0.1:5000`.

## API Endpoints
- **`POST /scan`**: Accepts a JSON body with either a `text` key or an `inbox` key to start a scan. Returns a `scanId`.
- **`GET /reports/{scanId}`**: Returns the detailed report for a given scan ID.
- **`GET /emails/{inbox_name}`**: Returns mock email data for a specified inbox (`inbox_hr` or `inbox_finance`).
