from flask import Flask, render_template, make_response, request

app = Flask(__name__)

@app.route('/victim')
def victim():
    """Simulate a victim page with vulnerable cookies"""
    response = make_response(render_template('victim.html'))
    response.set_cookie('test_cookie', 'cookie_value')  # Simulate a cookie
    return response


@app.route('/test')
def test():
    """Simulate a vulnerable endpoint for SQL Injection testing"""
    user_input = request.args.get('input', '')
    if "'" in user_input or "OR" in user_input:
        return "SQL Error detected!", 500
    return "Input is safe."

if __name__ == '__main__':
    app.run(port=5001, debug=True)
