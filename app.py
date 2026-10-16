from flask import Flask

app = Flask(__name__)

@app.route("/")
def accueil():
    return "<h1>Mini-GMAO</h1><p>L'application fonctionne.</p>"

if __name__ == "__main__":
    app.run(debug=True)