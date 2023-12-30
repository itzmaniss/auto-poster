from flask import *
import meta as m

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return redirect(m.login())

@app.route("/success")
def success():
    fragment = request.args.get("access_token")
    print(fragment)
    return render_template("success.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, ssl_context="adhoc", debug=True)
