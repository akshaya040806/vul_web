from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    rendered = ""

    if request.method == "POST":
        user_input = request.form.get("input", "")
        rendered = render_template_string(user_input)

    return render_template_string(f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SSTI Lab</title>
        </head>
        <body>
            <h2>Enter any text</h2>
            <form method="POST">
                <input type="text" name="input" style="width:400px">
                <button type="submit">Submit</button>
            </form>
            <hr>
            <div>{rendered}</div>
        </body>
        </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

