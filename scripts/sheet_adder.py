from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import service_account_path


def form_body(expense, amount, exp_type):
    current_day = datetime.now().day
    current_month = datetime.now().month

    body = dict()
    body['values'] = [[f'{current_day}/{current_month}', amount, expense, exp_type]]
    return body


def add_to_sheet(expense_text, amount, exp_type, income):
    # Generates the sheet name based on the current month and year
    sheet_name = f"{datetime.now().strftime('%B')} {datetime.now().year}"
    sheet_id = None
    # Range on the sheet where it will be inputted
    if not income:
        sheet_range = 'Transactions!B5:E223'
    else:
        sheet_range = 'Transactions!G5:J223'

    # Absolute path to the service account file
    service_account_file = '../monthly-spending-334222-4c36bd281ec7.json'

    # Which APIs are we using
    scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

    # Creates the credentials
    credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)

    # Builds the google drive API
    service = build('drive', 'v3', credentials=credentials)

    # Grabs all of the files from the Expense Sheets folder
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    # Loops through the files and grabs the ID of the sheet that matches the current month's sheet
    for item in items:
        if item['name'] == sheet_name:
            sheet_id = item['id']
    # Error returned if sheet is not found.
    if sheet_id is None:
        return 1
    # Replaces the drive service with the sheets service
    service = build('sheets', 'v4', credentials=credentials)
    # Builds the body, containing the info which will be sent to the sheets
    request_body = form_body(expense_text, amount, exp_type)
    # Grabs the sheet and then makes the request
    sheet = service.spreadsheets()
    request = sheet.values().append(spreadsheetId=sheet_id, range=sheet_range, valueInputOption="USER_ENTERED",
                                    body=request_body)
    request.execute()
    return 0


if __name__ == '__main__':
    add_to_sheet('Test', 50, 'Food', False)
