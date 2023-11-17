import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
CREDENTIALS = 'secrets/client_secret_1071226092782-svh8jcqb6kpti3a7depp496jducuvfo8.apps.googleusercontent.com.json'

creds = None
sheet = None
sheet_id = None

def google_auth(i_sheet_id):
    global creds, sheet, sheet_id
    sheet_id = i_sheet_id
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
    with open("secrets/token.json", "w") as token:
        token.write(creds.to_json())
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

def get_examples():
    try:
        # Call the Sheets API
        range_name = 'Examples!B6:H33'    
        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
            return []
    except HttpError as err:
        print(err)
    return values

def get_abstracts():
    try:
        # Call the Sheets API
        range_name = 'Examples!B5:H33'   
        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
            return []
    except HttpError as err:
        print(err)
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

def get_prompts():
    try:
        # Call the Sheets API
        range_name = 'Prompts!B2:B5'    
        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print("No data found.")
            return []
    except HttpError as err:
        print(err)
    return values

def update_scores(records):
    print('updating scores...')
    range_name = 'Examples!E6:H33'
    value_input_option = 'USER_ENTERED'
    update_values = [rec[3:7] for rec in records]
    update_body = {'values': update_values}    
    result = sheet.values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption=value_input_option, body=update_body).execute()
    print('result:', result)
