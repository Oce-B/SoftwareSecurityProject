from flask import Flask, request
import time

app = Flask(__name__)

# Route principale
@app.route("/")
def home():
    return "Welcome to the Flask Server!"

# Route lourde simulant une tâche complexe
@app.route("/heavy-task")
def heavy_task():
    time.sleep(5)  # Simule un traitement long (5 secondes)
    return "Task completed!"

# Démarrage du serveur Flask
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
