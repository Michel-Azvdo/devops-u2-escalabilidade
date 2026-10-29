from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import socket

app = Flask(__name__)
REQUESTS = Counter("app_requests_total", "Total de requisições", ["endpoint"])

@app.route("/")
def home():
    REQUESTS.labels("/").inc()
    return jsonify(msg="Olá!", pod=socket.gethostname())

@app.route("/health")
def health():
    return "ok", 200

@app.route("/cpu")
def cpu():
    REQUESTS.labels("/cpu").inc()
    x = 0
    for i in range(3_000_000):
        x += i * i
    return jsonify(done=True, pod=socket.gethostname())

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
