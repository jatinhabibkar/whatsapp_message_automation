from modules.messageModule import DriveAuth
from modules.messageModule import *
import time
import sys
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# logs file variables
file = open('logs/failed.txt', 'w', encoding="utf-8")
file.write('FAILED MESSAGES\n')
# logs file variables


# test users
# users=[{
#     'NAME': 'name1',
#     'DOB': '',
#     '26/04/2021': 1,
#     '27/04/2021': 2,
#     '28/04/2021': 3,
#     '29/04/2021': 4
# }, {
#     'NAME': 'name2',
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


dr = DriveAuth()

# real uers
users = dr.get_data_sheet(SHEET_NAME_DOB_DATE)


print('Data is present ' + str(len(users) > 0))


def open_whatsapp_and_authorize():
    try:
        global driver
        
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()))

        driver.get('https://web.whatsapp.com/')
        # wait till we get the access to search bar
        print("waiting for u to scan QR code ")
        while (dr.check_xp(driver, '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p')):
            time.sleep(3)
        print("-"*20, "important log", "-"*20)
    except Exception as e:

        print("update drivers https://chromedriver.chromium.org/downloads")
        print("plz update your drivers "+str(e))
        input()
        sys.exit()


open_whatsapp_and_authorize()
print("sleeping for 20 seconds.....zzzzz")
time.sleep(20)  # sleep for 20 seconds

for usr in users[:]:
    if (usr['NAME'] == ''):
        continue
    data = {
        'usr': usr['NAME'],
        'dob': usr['DOB'],
        # get number from todays date and find in the user dict
        'number': usr[dr.todaystr]
    }
    finalmsg = dr.format_data(data)

    # select search bar
    search = driver.find_element(by=By.XPATH, value='//*[@id="side"]/div[1]/div/div[2]/div/div/div/p')
    search.click()
    # select search bar
    time.sleep(2)
    search.send_keys(str(usr['NAME'])+" ( MC )")
    search.send_keys(Keys.ENTER)
    try:
        # get the name of that user page

        # title_user_name = driver.find_element(
        #     by=By.XPATH, value='//*[@id="main"]/header/div[2]/div/div/div/span').text.lower()  // other system
        title_user_name = driver.find_element(
            by=By.XPATH, value='//*[@id="main"]/header/div[2]/div[1]/div/span').text.lower()

        # check if we are in that user page
        if title_user_name == usr['NAME'].lower()+" ( mc )":
            msg_box = driver.find_element(
                by=By.XPATH, value='//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]')

            # clipboard.copy(finalmsg)
            pyperclip.copy(finalmsg)
            time.sleep(0.1)

            msg_box.send_keys(Keys.CONTROL, 'v')
            msg_box.send_keys(Keys.ENTER)
            print(f"Successfully sended message to {usr['NAME']}")
        else:
            print(f"{usr['NAME']} can't find on whatsapp")
            file.write(str('\n======================= ' + usr['NAME']+' ========================== \n\n'))
            file.write(str(finalmsg))

    except Exception as e:
        print(f"{usr['NAME']} can't find title whatsapperror")
    time.sleep(4)
    search = driver.find_element(by=By.XPATH, value='//*[@id="side"]/div[1]/div/div[2]/div/div/div/p')
    # first clear search bar for every user
    search.send_keys(Keys.CONTROL, 'a')
    search.send_keys(Keys.BACKSPACE)
    # first clear search bar for every user

print("-"*20, "hey my work is done master", "-"*20)
file.close()
input()
