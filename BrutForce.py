import itertools
import time


def brut_force_attack(target_password, max_length):
    # Jeu de caractères (modifiable)
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?;:/=+()&@#"

    # Début du chronomètre
    start_time = time.time()

    # Initialisation du compteur d'essais
    attempt_count = 0

    print("Démarrage de l'attaque Brut Force...")

    # Tester toutes les combinaisons possibles
    for length in range(1, max_length + 1):
        print(f"Test des combinaisons de longueur {length}...")
        # Générer les combinaisons
        for attempt in itertools.product(characters, repeat=length):
            # Convertir la combinaison en chaîne de caractères
            attempt_password = ''.join(attempt)

            # Incrémenter le compteur d'essais
            attempt_count += 1

            # Comparer avec le mot de passe cible
            if attempt_password == target_password:
                end_time = time.time()
                print(f"\nMot de passe trouvé : {attempt_password}")
                print(f"Nombre total d'essais : {attempt_count}")
                print(f"Temps écoulé : {end_time - start_time:.2f} secondes.")
                return

    print("Mot de passe introuvable dans la limite donnée.")


# Exemple d'utilisation
target = input("Entrez le mot de passe cible : ")
max_length = int(input("Entrez la longueur maximale à tester : "))
brut_force_attack(target, max_length)
