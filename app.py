from flask import Flask, render_template, request, jsonify
import os
import stripe

app = Flask(__name__)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

@app.route("/")
def index():
    return render_template(
        "index.html",
        publishable_key=os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
    )

@app.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    data = request.get_json()
    amount = float(data.get("amount", 0))

    if amount < 10:
        return jsonify({"error": "El monto mínimo es $10 MXN"}), 400

    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency="mxn",
        automatic_payment_methods={"enabled": True}
    )

    return jsonify({"clientSecret": intent.client_secret})

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/failed")
def failed():
    msg = request.args.get("msg", "Pago rechazado")
    return render_template("failed.html", msg=msg)

@app.route("/webhook", methods=["POST"])
def webhook():
    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
