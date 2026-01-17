from flask import Flask, request, redirect, render_template, session
import sqlite3

app = Flask(__name__)
app.secret_key = "this-is-unsafe-secret"

# ----------------------------------------------------
# Database Setup
# ----------------------------------------------------
def get_db():
    conn = sqlite3.connect("auth.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
    db.execute("INSERT INTO users(username,password) VALUES('admin','admin123')")
    db.commit()
    db.close()

init_db()

# ----------------------------------------------------
# Login Page (SQLi Vulnerable)
# ----------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")

        # ❌ SQL Injection Vulnerable Query
        query = f"SELECT * FROM users WHERE username = '{uname}' AND password = '{pwd}'"
        db = get_db()
        cur = db.execute(query)
        row = cur.fetchone()

        if row:
            session["user"] = row["username"]
            return redirect("/message")
        else:
            msg = "Login Failed"

    return render_template("login.html", msg=msg)

# ----------------------------------------------------
# Message Page (SSTI Vulnerable)
# ----------------------------------------------------
@app.route("/message", methods=["GET", "POST"])
def message():
    if "user" not in session:
        return redirect("/")

    ssti_input = ""
    if request.method == "POST":
        ssti_input = request.form.get("message")

    # Also support SSTI via query parameter
    ssti_param = request.args.get("message", "")

    final_input = ssti_input or ssti_param

    # ❌ SSTI Vulnerability via render_template_string
    template = f"""
    <html>
    <body>
        <h1>Leave a Message</h1>
        <form method="POST">
            <textarea name="message"></textarea><br><br>
            <button type="submit">Submit</button>
        </form>
        <hr>
        <h2>Your Input:</h2>
        <div>{final_input}</div>
    </body>
    </html>
    """

    return render_template_string(template)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

