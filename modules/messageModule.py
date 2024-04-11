import os
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import gspread
import random
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv()

# you can edit

SCOPE = ['https://www.googleapis.com/auth/drive',
         'https://spreadsheets.google.com/feeds']

# files
GCP_KEY=os.getenv('GCP_KEY')
DEFAULT_MESSAGE=os.getenv('DEFAULT_MESSAGE')

# data
COLOR_NUMBER=os.getenv('COLOR_NUMBER')
SHEET_NAME_DOB_DATE=os.getenv('SHEET_NAME_DOB_DATE')
SHORT_MESSAGE=os.getenv('SHORT_MESSAGE')
DATE_SHEET=os.getenv('DATE_SHEET')
gsheet_messages={}
# you can edit 


class DriveAuth:
    def __init__(self):
        # Authorizing and getting data from gdrive
        print("Authorizing and getting data...")
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            GCP_KEY, SCOPE)
        self.client = gspread.authorize(self.creds)

        # greetings
        self.todaystr = self.get_date(DATE_SHEET)
        print("#"*20)
        print("Date is ", self.todaystr)
        print("#"*20)
        # sheet 1
        print("getting default message...")
        self.msg = self.get_default_message(DEFAULT_MESSAGE)

        # sheet 2
        print("getting colors and number...")
        self.colr, self.numr = self.get_color(COLOR_NUMBER)

        # sheet 3
        print("getting short message....")
        self.shortM = self.get_data_sheet(SHORT_MESSAGE)
        for i in self.shortM:
            gsheet_messages[i["NUMBER"]] = i["MESSAGE"]

    def get_date(self, sheetName):
        sheet = self.client.open(sheetName).get_worksheet(1).get_all_records()
        return sheet[0]["DATE"]

    # all record

    def get_data_sheet(self, sheetName):
        return self.client.open(sheetName).sheet1.get_all_records()

    # open txt file and return the text
    def get_default_message(self, filename):
        try:
            self.filedata = open(""+filename, 'r', encoding='utf-8')
            return self.filedata.read()
        except Exception as e:
            print(e, "something went wrong with default msg read")

    def get_color(self, sheetname):
        sheet = self.client.open(sheetname).sheet1
        colr = sheet.get('A:A')
        numr = sheet.get('B:B')
        colr = [x[0] for x in colr[1:]]
        numr = [x[0] for x in numr[1:]]
        return colr, numr

    def format_data(self, data):
        # data should contain usr,dob,msg
        try:
            msg = self.msg
            msg = msg.replace("{usr}", data['usr'])
            msg = msg.replace("{dob}", data['dob'])
            msg = msg.replace("{today}", self.todaystr)
            msg = msg.replace("{msg}", self.get_msg_by_number(data['number']))
            msg = msg.replace("{num}", str(random.choice(self.numr)))
            msg = msg.replace("{col}", random.choice(self.colr))

            return msg
        except Exception as e:
            print(e, "somthing went wrong for", data["usr"])

    def get_msg_by_number(self, num):
        try:
            return gsheet_messages[num]
        except Exception as e:
            print(e, "can't find ", num)

    # check if the xpath is present or not
    def check_xp(self, webdriver, xpath):
        try:
            webdriver.find_element(by=By.XPATH, value=xpath)
        except Exception as e:
            return True
        return False
