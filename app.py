from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Webhook activo"

@app.route("/webhook", methods=["POST"])
def webhook():
    print(request.json)
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
