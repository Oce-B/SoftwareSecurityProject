import time


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
                    print(f"Progression : {
                          attempt_count} mots de passe testés...")

                # Comparer avec le mot de passe cible
                if attempt_password == target_password:
                    end_time = time.time()
                    print(f"\nMot de passe trouvé : {attempt_password}")
                    print(f"Nombre total d'essais : {attempt_count}")
                    print(f"Temps écoulé : {
                          end_time - start_time:.2f} secondes.")
                    return

        # Si on atteint la fin du fichier sans trouver le mot de passe
        print("Mot de passe introuvable dans le dictionnaire.")
    except FileNotFoundError:
        print(f"Erreur : Le fichier {dictionary_file} est introuvable.")


# Exemple d'utilisation
target = input("Entrez le mot de passe cible : ")
dictionary_file = "rockyou.txt"  # Chemin vers le fichier rockyou.txt
dictionary_attack(target, dictionary_file)
