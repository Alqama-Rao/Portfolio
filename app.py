import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from flask import Flask, request, jsonify, redirect

# Client ID, client secret, and redirect URL from Google Cloud Console
CLIENT_ID = "303785721663-i1i1sglg1niqesp4m1lkaa1aq48ipaoc.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://myportfolio1.herokuapp.com/oauth_callback"

# Define the scopes that the application needs to authorize
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    creds = None
    if os.path.exists('Credentials.json'):
        creds = Credentials.from_authorized_user_file('Credentials.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                'client_secret.json', SCOPES, redirect_uri=REDIRECT_URI)
            auth_url, _ = flow.authorization_url(prompt='consent')
            return redirect(auth_url)

        # Save the credentials for the next run
        with open('Credentials.json', 'w') as token:
            token.write(creds.to_json())

    return creds

creds = get_credentials()

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

@app.route("/")
def index():
    return "Hello, World!"

@app.route("/oauth_callback")
def oauth_callback():
    flow = Flow.from_client_secrets_file(
        'client_secret.json', SCOPES, redirect_uri=REDIRECT_URI)
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    with open('Credentials.json', 'w') as token:
        token.write(creds.to_json())
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
