import os
import google.auth
from googleapiclient.discovery import build

class GoogleSheets:
    def __init__(self, spreadsheet_id, service_account_file):
        self.spreadsheet_id = spreadsheet_id
        self.service_account_file = service_account_file
        self.service = self.create_service()

    def create_service(self):
        credentials = None
        if os.path.exists(self.service_account_file):
            credentials, project = google.auth.load_credentials_from_file(self.service_account_file)
        return build('sheets', 'v4', credentials=credentials)

    def read_data(self, range_name):
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=range_name
        ).execute()
        return result.get('values', [])

    def update_data(self, row):
        range_name = f'Sheet1!C{row}'  # Update column third column for marking as "Done"
        body = {'values': [['Done']]}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
