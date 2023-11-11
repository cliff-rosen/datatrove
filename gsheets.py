import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
CREDENTIALS = 'secrets/client_secret_1071226092782-svh8jcqb6kpti3a7depp496jducuvfo8.apps.googleusercontent.com.json'

creds = None

def google_auth():
    global creds
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("secrets/token.json"):
        creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
        print('found token.json', creds.valid)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print('no valid creds found')
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS, SCOPES
        )
        creds = flow.run_local_server(port=0)
    else:
    # Save the credentials for the next run
        print('valid creds found')
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    with open("token.json", "w") as token:
        token.write(creds.to_json())

def get_sheet(sheet_id):
  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    range_name = 'Questions!B6:B33'    
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=sheet_id, range=range_name)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    print("Name, Major:")
    for row in values:
      print(f"{row[0]}")
  except HttpError as err:
    print(err)
 

def update_sheet():
    service = build("sheets", "v4", credentials=creds)
    range_name = 'Prompts!C3:D3'
    value_input_option = 'USER_ENTERED'
    update_values = [['a', 'b']]
    update_body = {'values': update_values}    
    range_name = 'Questions!B6:B33'    
    sheet = service.spreadsheets()
    result = sheet.values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption=value_input_option, body=update_body).execute()

