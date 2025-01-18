import matplotlib.pyplot as plt

lengths = [1, 2, 3, 4, 5, 6, 7, 8, 9]
brut_force_times = [0.01, 0.01, 0.05, 0.50,
                    10.5, 254.4, 5000, 125000, 3000000, 75000000]
dictionary_times = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]

plt.plot(lengths, brut_force_times, label="Brut Force", marker='o')
plt.plot(lengths, dictionary_times, label="Dictionnaire", marker='o')
plt.title("Comparaison des temps d'exécution")
plt.xlabel("Longueur du mot de passe")
plt.ylabel("Temps (secondes)")
plt.legend()
plt.grid()
plt.show()
