from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import io
import sys
import time
import datetime
import gspread
import os
import time
import csv
import clipboard
import sys
import inquirer
import random
from selenium.webdriver.common.by import By

# you can edit

SCOPE = ['https://www.googleapis.com/auth/drive',
         'https://spreadsheets.google.com/feeds']

# files
THE_JSON = "modules/keys.json"
DEFAULT_MESSAGE = 'textmessage.txt'
DIR = ""

# data present on gdrive with this name
COLOR_NUMBER = "SHEET_NAME"
SHEET_NAME_DOB_DATE = "SHEET_NAME"
SHORT_MESSAGE = "SHEET_NAME"
DEFAULT_MESSAGE = "file.txt"
DATE_SHEET = "SHEET_NAME"
sm = {}
# you can edit


class DriveAuth:
    def __init__(self):
        # Authorizing and getting data from gdrive
        print("Authorizing and getting data...")
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            THE_JSON, SCOPE)
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
            sm[i["NUMBER"]] = i["MESSAGE"]

    def get_date(self, sheetName):
        sheet = self.client.open(sheetName).get_worksheet(1).get_all_records()
        return sheet[0]["DATE"]

    # all record

    def get_data_sheet(self, sheetName):
        return self.client.open(sheetName).sheet1.get_all_records()

    # open txt file and return the text
    def get_default_message(self, filename):
        try:
            self.filedata = open(DIR+filename, 'r', encoding='utf-8')
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
            return sm[num]
        except Exception as e:
            print(e, "can't find ", num)

    # check if the xpath is present or not
    def check_xp(self, webdriver, xpath):
        try:
            webdriver.find_element(by=By.XPATH, value=xpath)
        except Exception as e:
            return True
        return False
