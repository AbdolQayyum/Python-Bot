from concurrent.futures import ThreadPoolExecutor
import os
from modules.google_sheets_module import GoogleSheets
from modules.form_submission import FormSubmission

from dotenv import load_dotenv

load_dotenv()

def main():
    
    #SPREADSHEET_ID=1JYXuzwUbCt9YyyZSEdWmHLGYuCAnAHGXRZ2rP4YJiUs
    #SERVICE_ACCOUNT_FILE=.venv/credentials.json
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID') 
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')  

    # Enter the starting row number
    start_row = int(input("Enter the starting row number: "))
    # Enter the number of threads
    num_threads = int(input("Enter the number of threads: "))

    # Define the range for reading data from Google Sheets
    RANGE_NAME = f'Sheet1!A{start_row}:B' 

    # Initialize Google Sheets API
    sheets = GoogleSheets(SPREADSHEET_ID, SERVICE_ACCOUNT_FILE)
    data = sheets.read_data(RANGE_NAME)

    # Use ThreadPoolExecutor to manage multiple threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        tasks = []  # Make the tasks list so that when form submission is done then append in list.
        
        for i, row in enumerate(data, start=start_row):
            name, email = row[0], row[1]
            form_sub = FormSubmission()
            
            # Submit form asynchronously using threads
            tasks.append(executor.submit(form_sub.submit_form, name, email))

        # Wait for all threads to finish and update Google Sheets for each completed form
        for i, task in enumerate(tasks, start=start_row): 
            task.result()  
            sheets.update_data(i) 

if __name__ == '__main__':
    main()
