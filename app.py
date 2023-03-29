import logging
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.DEBUG)

@app.route("/api", methods=["GET"])
def Default():
    return "Hello Deer"

@app.route("/api/save-location", methods=["POST"])
def save_location():
    app_logger.info("Received request to save location")
    longitude = request.args.get("longitude")
    latitude = request.args.get("latitude")

    # Load previous data from file
    try:
        with open("/app/locations.txt", "r") as f:
            locations = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        locations = []

    # Add new data to list
    locations.append([latitude, longitude])

    # Write data to file
    with open("/app/locations.txt", "w") as f:
        for loc in locations:
            f.write(f"{loc[0]},{loc[1]}\n")

    app_logger.debug(f"Current working directory: {os.getcwd()}")
    app_logger.info("Successfully saved location")
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
