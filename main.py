from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import subprocess
import sys
import socket



class Whatsapp:
    search_box_xpath = "//div[@title='Tìm kiếm bằng ô nhập văn bản']"
    message_box_xpath = "//div[@title='Nhập tin nhắn']"
    attachment_icon_xpath = "//div[@title='Đính kèm']"
    image_attachment_xpath = "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
    send_button_xpath = "//span[@data-icon='send']"
    def __init__(self, url, trigger_path):
        self.url = url
        self.trigger_path = trigger_path
        self.user_dict_list = []
        driver_path = os.getcwd() + "\Chrome_Driver\chromedriver.exe"
        print(socket.gethostname())
        if socket.gethostname() == "My-Personal-PC":
            print("Running Under My Personal PC")
            chrome_directory = r"user-data-dir=C:\Users\Admin\AppData" \
                               r"\Local\Google\Chrome\User_Data_For_Auto_Trigger_System"
        elif socket.gethostname() == "FS-35826":
            print("Running Under Company Laptop")
            chrome_directory = r"user-data-dir=C:\Users\fs120806\AppData\Local\Google\Chrome" \
                               r"\User_Data_For_Auto_Trigger_System"
        else:
            print("Running Under Home PC")
            chrome_directory = r"user-data-dir=C:\Users\admin\AppData\Local\Google" \
                               r"\Chrome\User_Data_For_Auto_Trigger_System"
        # Access To Whatsapp
        self.chrome_options = Options()
        self.chrome_options.add_argument(chrome_directory)
        self.chrome_options.add_experimental_option("detach", True)
        # Keep the chrome driver open after the program is finished
        self.service = Service(driver_path)
        self.chrome_driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.wait = WebDriverWait(self.chrome_driver, 100)
        self.chrome_driver.get(self.url)
        page_title = self.chrome_driver.title
        # Get the title of the website
        print(f"The Website You Are Accessing Is {page_title}")
        try:
            self.search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.search_box_xpath)))
        except TimeoutException:
            print("The Website Is Not Available Or The Internet Connection Is Not Stable")
            self.chrome_driver.quit()
        with open(self.trigger_path, 'r') as file:
            df = pd.read_csv(file)
            for i in range(len(df.index)):
                user = {'User': (df.iloc[i]).loc['User'],
                        'Text': (df.iloc[i]).loc['Text'],
                        'Image Folder': (df.iloc[i]).loc['Image Folder'],
                        'Script Folder': (df.iloc[i]).loc['Script Folder'],
                        'SQL Folder': (df.iloc[i]).loc['SQL Folder'],
                        'Period': (df.iloc[i]).loc['Period'],
                        'Data Description': (df.iloc[i]).loc['Data Description']}
                self.user_dict_list.append(user)
        print("Raw Data Read From Trigger File Information")
        print(self.user_dict_list)
        # Create folder for each user to make a buffer memory for storing the image
        # Scan and check file in foler is empty or not. Request to add files if it is empty
        current_folder_path = os.getcwd()
        image_folder = os.path.join(current_folder_path, 'Image')
        script_folder = os.path.join(current_folder_path, 'Script')
        sql_folder = os.path.join(current_folder_path, 'SQL')
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
            os.getcwd()
            for i in range(len(self.user_dict_list)):
                os.makedirs(self.user_dict_list[i]['Image Folder'])
        if not os.path.exists(script_folder):
            os.makedirs(script_folder)
            os.getcwd()
            for i in range(len(self.user_dict_list)):
                os.makedirs(self.user_dict_list[i]['Script Folder'])
        if not os.path.exists(sql_folder):
            os.makedirs(sql_folder)
            os.getcwd()
            for i in range(len(self.user_dict_list)):
                os.makedirs(self.user_dict_list[i]['SQL Folder'])
        popup = input("Please Add All Files To SQL Folder And Script Then Typing Yes To Continue: ")
        if popup.lower() == 'no':
            print("Please Add All Files To SQL Folder And Script")
            sys.exit()
        elif popup.lower() == 'yes':
            check_script_id = 0
            check_sql_id = 0
            for i in range(len(self.user_dict_list)):
                script_folder_path = self.user_dict_list[i]['Script Folder']
                sql_folder_path = self.user_dict_list[i]['SQL Folder']
                if not os.listdir(script_folder_path):
                    print(f"Please Add All Files To Script Folder for {self.user_dict_list[i]['User'] + ' '}"
                          f"{self.user_dict_list[i]['Data Description']}")
                    sys.exit()
                else:
                    print(f"Script Folder For {self.user_dict_list[i]['User'] + ' '}"
                          f"{self.user_dict_list[i]['Data Description']} Is Ready")
                if not os.listdir(sql_folder_path):
                    print(f"Please Add All Files To SQL Folder {self.user_dict_list[i]['User'] + ' '}"
                          f"{self.user_dict_list[i]['Data Description']}")
                    sys.exit()
                else:
                    print(f"SQL Folder For {self.user_dict_list[i]['User'] + ' '}"
                          f"{self.user_dict_list[i]['Data Description']} Is Ready")
        else:
            print("Please Type Yes Or No And Run The Program Again")
            sys.exit()
        print("All Files Are Loaded And Ready To Send To User")
        print("Start Program To Send Message And Image To User")
        time.sleep(5)

    def send_message_and_image(self, image_path_folder):
        image_folder_list = os.listdir(image_path_folder)
        image_folder_path_area = []
        for i in range(len(image_folder_list)): # Count number of folder in image folder
            image_folder_path_area.append(os.path.join(image_path_folder, image_folder_list[i]))
            if not os.listdir(image_folder_path_area[i]):
                print(f"No Images Files In Folder {image_folder_path_area[i]}")
        # for j in range(len(image_folder_path_area)): # Count number of image in each folder
        #     for k in range(len(os.listdir(image_folder_path_area[j]))):
        #             image_path.append(os.path.join(image_folder_path_area[j], (os.listdir(image_folder_path_area[j])[k])))
        # user_and_image_path = {}
        # for i in range(len(self.user_dict_list)):
        #     user_and_image_path.setdefault(self.user_dict_list[i]['User'], []).append(self.user_dict_list[i]['Text'] + " " + self.user_dict_list[i]['Data Description'])
        #     for j in range (len(os.listdir(self.user_dict_list[i]['Image Folder']))):
        #         user_and_image_path[self.user_dict_list[i]['User']].append(os.path.join(self.user_dict_list[i]['Image Folder'], (os.listdir(self.user_dict_list[i]['Image Folder'])[j])))
        # print(user_and_image_path)
        # user_and_image_path.[self.user_dict_list[i]['User']].append(os.path.join(self.user_dict_list[i]['Image Folder'], (os.listdir(self.user_dict_list[i]['Image Folder'])[j])))
        # print("List Of Folder In Image Folder")
        # print(image_folder_path_area)
        # print("Path Of All Images In Every Folder Correcponding To User")
        # print(user_and_image_path)
        data = {}
        user = []
        for i in range(len(self.user_dict_list)):
            user.append(self.user_dict_list[i]['User'])
        for j in range(len(self.user_dict_list)):
            data['Text'] = self.user_dict_list[j]['Text']
            data['Data Description'] = self.user_dict_list[j]['Data Description']
            data['Period'] = self.user_dict_list[j]['Period']
            for k in range(len(os.listdir(self.user_dict_list[j]['Image Folder']))):
                data['Image'] = os.path.join(self.user_dict_list[j]['Image Folder'], (os.listdir(self.user_dict_list[j]['Image Folder'])[k]))
        user_data = dict.fromkeys(user, data)
        print(user_data)
        # Send message and image to each user
        for key in user_data:
            self.search_box.clear()
            self.search_box.click()
            self.search_box.send_keys(key)
            self.search_box.send_keys(Keys.ENTER)
            print("Start Sending Message To {0}".format(key))
            message_box = self.wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.message_box_xpath)))
            message_box.clear()
            message_box.click()
            message_box.send_keys(user_data[key]['Text'] + '\n' + user_data[key]['Data Description'] + '\n' + "Time Period" + " " + str(user_data[key]['Period']))
            time.sleep(1) # Wait for the message to be sent
            message_box.send_keys(Keys.ENTER)
            time.sleep(3)
            print("Start Sending Image To {0}".format(key))
            attachment_icon = self.wait.until(EC.presence_of_element_located((By.XPATH, self.attachment_icon_xpath)))
            attachment_icon.click()
            image_attachment = self.wait.until(EC.presence_of_element_located((By.XPATH, self.image_attachment_xpath)))
            image_attachment.send_keys(user_data[key]['Image'])
            time.sleep(1)  # Wait for the image to be uploaded
            send_image_button = self.wait.until(EC.presence_of_element_located((By.XPATH, self.send_button_xpath)))
            send_image_button.click()
            time.sleep(3)


if __name__ == '__main__':
    trigger_path = os.getcwd() + "\Trigger_Information\data_trigger.csv"
    image_path_folder = os.getcwd() + "\Image"
    url = "https://web.whatsapp.com/"
    whatsapp = Whatsapp(url, trigger_path)
    whatsapp.send_message_and_image(image_path_folder=image_path_folder)






