import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from flask import Flask, request, jsonify

creds = None
if os.path.exists('credentials.json'):
    creds = Credentials.from_authorized_user_file('credentials.json')

# Define the spreadsheet ID and range to write data to
SPREADSHEET_ID = '1SEw29nHHIlDq149QW78HVtx5rzJCr-FRQn49HzntpOs'
RANGE_NAME = 'Sheet1!A1:B'

def write_to_sheet(values):
    print("Write to sheet")
    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': [values]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', insertDataOption='INSERT_ROWS',
        body=body).execute()
    print('{0} cells appended.'.format(result \
                                       .get('updates') \
                                       .get('updatedCells')))



app = Flask(__name__)


@app.route("/api/save-location", methods=["POST"])
def save_location():
    print("Save location")
    data = request.get_json()
    values = [data['latitude'], data['longitude']]
    write_to_sheet(values)
    return jsonify(success=True)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
