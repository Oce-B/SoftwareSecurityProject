from flask import Flask, render_template, request, redirect, url_for
from attacks import run_xss_test, run_csrf_test

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        attack_type = request.form.get("attack_type")
        target_url = request.form.get("target_url")

        if not target_url:
            return render_template("index.html", error="Please provide a target URL.")

        return redirect(url_for("results", attack_type=attack_type, target_url=target_url))

    return render_template("index.html")

@app.route("/results")
def results():
    attack_type = request.args.get("attack_type")
    target_url = request.args.get("target_url")

    if not attack_type or not target_url:
        # No valid attack selected or target provided, go back to main
        return redirect(url_for("index"))

    if attack_type == "xss":
        outcome = run_xss_test(target_url)
    elif attack_type == "csrf":
        outcome = run_csrf_test(target_url)
    else:
        outcome = [{"error": f"Unknown attack type: {attack_type}"}]

    return render_template("results.html", attack_type=attack_type, target_url=target_url, outcome=outcome)

if __name__ == "__main__":
    app.run(debug=True)
