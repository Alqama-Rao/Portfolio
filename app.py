from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def Default():
    return "Hello Deer"


@app.route("/api/save-location", methods=["POST"])
def save_location():
    print("Save location called")
    data = request.get_json()

    print("Reading file data")
    # Load previous data from file
    try:
        with open("locations.txt", "r") as f:
            locations = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        locations = []

    # Add new data to list
    locations.append([data["latitude"], data["longitude"]])

    print("Writing data in file")

    # Write data to file
    with open("locations.txt", "w") as f:
        for loc in locations:
            f.write(f"{loc[0]},{loc[1]}\n")
    import os
    print(os.getcwd())

    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
