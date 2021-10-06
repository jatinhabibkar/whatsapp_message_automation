# from modules.messageModule import DriveAuth
from oauth2client.service_account import ServiceAccountCredentials
from modules.messageModule import *
import os,time,csv,clipboard,sys,inquirer,gspread,pyperclip

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# variable and sheet names
SHEET_NAME_DOB_DATE="SHEET_NAME"
SHORT_MESSAGE="SHEET_NAME"
DEFAULT_MESSAGE='textmessage.txt'
WD_PATH="DRIVER_PATH"
# variable and sheet names


# test users
# users=[{
#     'NAME': 'Niap Pei Swan',
#     'DOB': '',
#     '26/04/2021': 1,
#     '27/04/2021': 2,
#     '28/04/2021': 3,
#     '29/04/2021': 4
# }, {
#     'NAME': 'Adrian Watuna',
#     'DOB': '',
#     '26/04/2021': 2,
#     '27/04/2021': 3,
#     '28/04/2021': 4,
#     '29/04/2021': 5
# }]
# for usr in users:
#     data={
#         'usr':usr['NAME'],
#         'dob':usr['DOB'],
#         'number':usr[dr.todaystr] #get number from todays date and find in the user dict
#     }
#     finalmsg =dr.format_data(data)
#     print(finalmsg)



try:
    dr = DriveAuth() 
except Exception as e:
    print(e,"something happend in auth")

# real uers
users=dr.getData_sheet(SHEET_NAME_DOB_DATE)


print(users)



def getready():
    try:
        global driver
        driver =webdriver.Chrome(WD_PATH)

        driver.get('https://web.whatsapp.com/')
        # wait till we get the access to search bar
        print("waiting for u to scan QR code ")
        while(dr.check_xp(driver,'//*[@id="side"]/div[1]/div/label/div/div[2]')):
            time.sleep(3)
        print("-"*20,"important log","-"*20)
    except Exception as e:

        print("update drivers https://chromedriver.chromium.org/downloads")
        print("plz update your drivers")
        input()
        sys.exit()

getready()
for usr in users[:]: #send to only  top 2 users 

    data={
        'usr':usr['NAME'],
        'dob':usr['DOB'],
        'number':usr[dr.todaystr] #get number from todays date and find in the user dict
    }
    finalmsg =dr.format_data(data)


    # select search bar                 
    search=driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
    search.click()
    # select search bar 
    search.send_keys(usr['NAME']+" ( MC )")
    search.send_keys(Keys.ENTER)

    try:
        # get the name of that user page
        titlename=driver.find_element_by_xpath('//*[@id="main"]/header/div[2]/div/div/span').text.lower()

        # check if we are in that user page
        if titlename == usr['NAME'].lower()+" ( mc )":
            msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')

            # clipboard.copy(finalmsg)
            pyperclip.copy(finalmsg)
            time.sleep(0.1)

            msg_box.send_keys(Keys.CONTROL, 'v')
            msg_box.send_keys(Keys.ENTER)
            print(f"Successfully sended message to {usr['NAME']}")
        else:
            print(f"{usr['NAME']} can't find on whatsapp")
    except Exception as e:
        print(f"{usr['NAME']} can't find on whatsapperror",e)
    
    # first clear search bar for every user
    for i in range(60):
        search.send_keys(Keys.BACKSPACE)
    # first clear search bar for every user

print("-"*20,"hey my work is done master","-"*20)
input()

