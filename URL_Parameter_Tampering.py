import requests
import random
import csv

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

def generate_report(results, output_file):
    """
    Generate a detailed report of the test results in CSV format.
    Args:
        results (list): The results from the URL tests.
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
        fieldnames = ["url", "params", "status_code", "successful", "response_preview", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            # Ensure all fields are present in the result
            result.setdefault("error", None)
            result.setdefault("response_preview", None)
            writer.writerow(result)

    print(f"Report saved to {output_file}")

# Main Execution
if __name__ == "__main__":
    base_url = "http://localhost:3000"

    # Step 1: Generate paths dynamically
    print("\n--- Generating Paths ---")
    paths = generate_paths(base_url, num_paths=1000)
    print(f"Generated {len(paths)} paths for testing.")

    # Step 2: Define parameters to test
    parameters = [
        {"id": "1"}, {"id": "99999"}, {"debug": "true"},
        {"admin": "true"}, {"authToken": "test"}, {"q": "' OR 1=1 --"}
    ]

    # Step 3: Test all URLs (limit total tests to 10,000)
    results = test_urls(paths, parameters, max_tests=10000)

    # Step 4: Generate a report
    generate_report(results, "URL_Parameter_Tampering_results.csv")
