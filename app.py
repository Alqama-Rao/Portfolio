from flask import Flask, request, jsonify
import openpyxl

app = Flask(__name__)


@app.route("/api", methods=["GET"])
def Default():
    return "Hello Deer"


@app.route("/api/save-location", methods=["POST"])
def save_location():

    data = request.get_json()

    # Load previous data from file
    workbook = openpyxl.load_workbook("locations.xlsx")
    worksheet = workbook.active
    locations = []
    for row in worksheet.iter_rows(values_only=True):
        locations.append({"latitude": float(row[0]), "longitude": float(row[1])})

    # Add new data to list
    locations.append(data)

    # Write data to file
    worksheet.append([data["latitude"], data["longitude"]])
    workbook.save("locations.xlsx")
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
