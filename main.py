from fastapi import FastAPI, Request

app = FastAPI()

locations = []

@app.post("/api/save-location")
async def save_location(request: Request):
    data = await request.json()
    locations.append(data)
    with open("locations.txt", "a") as f:
        f.write(f"{data['latitude']},{data['longitude']}\n")
    return {"success": True}


if __name__ == "__main__":
    app.run(debug=True)