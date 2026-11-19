
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

PLATFORMS = {
    "reader": {
        "name": "Sparx Reader",
        "url": os.getenv("READER_URL", "https://sparxreader.com")
    },
    "maths": {
        "name": "Sparx Maths",
        "url": os.getenv("MATHS_URL", "https://sparxmaths.com")
    },
    "science": {
        "name": "Sparx Science",
        "url": os.getenv("SCIENCE_URL", "https://sparxscience.com")
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/platforms")
def platforms():
    return jsonify([
        {"id": key, "name": value["name"]}
        for key, value in PLATFORMS.items()
    ])


@app.route("/api/test", methods=["POST"])
def run_test():
    data = request.get_json(silent=True) or {}
    platform = data.get("platform", "").lower()

    if platform not in PLATFORMS:
        return jsonify({
            "success": False,
            "message": "Please select a valid Sparx platform."
        }), 400

    # Credentials are deliberately not stored or logged.
    # This starter version does not log into Sparx.
    return jsonify({
        "success": True,
        "platform": PLATFORMS[platform]["name"],
        "message": (
            "Test request received. "
            "Authenticated testing is not enabled in this version."
        )
    })


@app.route("/health")
def health():
    return jsonify({"status": "online", "app": "CART3R"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000))
    )
