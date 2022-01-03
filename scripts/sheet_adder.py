from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import settings


class SheetInterface:
    def __init__(self):
        self.sheet_name = f"{datetime.now().strftime('%B')} {datetime.now().year}"
        self.sheet_id = None
        # Creates the credential using the service account file.
        service_acc_file = './monthly-spending-334222-4c36bd281ec7.json'
        scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
        self.credentials = service_account.Credentials.from_service_account_info(settings.GOOGLE_CLOUD_KEY,
                                                                                 scopes=scopes)
        # Grabs the sheet ID using the Google Drive API
        self.get_sheet_id_from_drive()

    def get_sheet_id_from_drive(self) -> int:
        """
        Connects to the Google Drive API and gets all of the files the Service Account has access to. It then loops
        through them and matches their names with self.sheet_name which has the "Month Year" format.
        :return: It returns 1 if the no file matching the month was found.
        """
        service = build('drive', 'v3', credentials=self.credentials)
        results = service.files().list(fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        # Loops through the files and grabs the ID of the sheet that matches the current month's sheet
        for item in items:
            if item['name'] == self.sheet_name:
                self.sheet_id = item['id']
        # Error returned if sheet is not found.
        if self.sheet_id is None:
            return 1

    @staticmethod
    def create_request_body(expense_text: str, amount: float, expense_type: str) -> dict:
        """
        Takes in the arguments of an entry and creates a request that can be accepted by the Google Sheets API
        :param expense_text: String containing the details about the expense
        :param amount: Float representing the amount.
        :param expense_type: String representing the type of the expense (Food, etc)
        :return: A dictionary formatted in a way accepted by the Google Sheets API
        """
        current_day = datetime.now().day
        current_month = datetime.now().month

        body = dict()
        body['values'] = [[f'{current_day}/{current_month}', amount, expense_text, expense_type]]
        return body

    def add_expense(self, amount: float, expense_text: str, expense_type: str) -> int:
        """
        Connects to the Sheets API and adds the parameters of the function on the sheet at the next location.
        :param amount: Float representing the amount.
        :param expense_text: String containing the details about the expense
        :param expense_type: String representing the type of the expense (Food, etc)
        :return: Returns 0
        """
        if self.sheet_id is None:
            return 1
        service = build('sheets', 'v4', credentials=self.credentials)
        sheet_range = 'Transactions!B5:E223'
        # Builds the body, containing the info which will be sent to the sheets
        request_body = self.create_request_body(expense_text, amount, expense_type)
        # Grabs the sheet and then makes the request
        sheet = service.spreadsheets()
        request = sheet.values().append(spreadsheetId=self.sheet_id, range=sheet_range, valueInputOption="USER_ENTERED",
                                        body=request_body)
        request.execute()
        return 0

    def add_income(self, amount, income_text, income_type):
        """
        Connects to the Sheets API and adds the parameters of the function on the sheet at the next location.
        :param amount: Float representing the amount.
        :param income_text: String containing the details about the expense
        :param income_type: String representing the type of the expense (Food, etc)
        :return: Returns 0
        """
        if self.sheet_id is None:
            return 1
        service = build('sheets', 'v4', credentials=self.credentials)
        sheet_range = 'Transactions!G5:J223'
        # Builds the body, containing the info which will be sent to the sheets
        request_body = self.create_request_body(income_text, amount, income_type)
        # Grabs the sheet and then makes the request
        sheet = service.spreadsheets()
        request = sheet.values().append(spreadsheetId=self.sheet_id, range=sheet_range, valueInputOption="USER_ENTERED",
                                        body=request_body)
        request.execute()
        return 0

    def get_current_month_value(self) -> str:
        """
        Gets the "End Balance" value from the latest sheet.
        :return: Returns the end balance.
        """
        service = build('sheets', 'v4', credentials=self.credentials)
        sheet = service.spreadsheets()
        sheet_cell = 'Summary!E17'
        results = sheet.values().get(spreadsheetId=self.sheet_id, range=sheet_cell).execute()
        return results['values'][0][0]
