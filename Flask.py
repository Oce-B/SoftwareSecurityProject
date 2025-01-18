from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/attack', methods=['GET', 'POST'])
def attack():
    if request.method == 'GET':
        # Command Injection
        cmd = request.args.get('cmd')
        if not cmd:
            return "No command provided!", 400
        # Execute the command (vulnerable to command injection)
        result = os.popen(cmd).read()
        return f"<pre>{result}</pre>", 200

    elif request.method == 'POST':
        # HTTP Parameter Pollution
        account = request.form.get('account')
        amounts = request.form.getlist('amount')  # Get all 'amount' values
        total_amount = sum(map(int, amounts))  # Sum all amounts
        return f"Transfer to account {account} with total amount {total_amount} initiated!", 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
