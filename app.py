@app.route("/api/save-location", methods=["POST"])
def save_location():

    data = request.get_json()

    # Read previous data from file
    locations = []
    with open("locations.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            locations.append({"latitude": float(row[0]), "longitude": float(row[1])})

    locations.append(data)
    with open("locations.csv", "a") as f:
        f.write(f"{data['latitude']},{data['longitude']}\n")
    with open("locations.csv", "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['latitude'], data['longitude']])
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)