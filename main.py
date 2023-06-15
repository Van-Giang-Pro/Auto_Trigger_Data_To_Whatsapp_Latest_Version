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
import json


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
        elif socket.gethostname() == "FS-35828":
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
        with open('C:\\Users\\Admin\\Desktop\\Personal Documents\\Python '
                  'Project\\Auto_Trigger_Data_To_Whatsapp_Latest_Version\\user_data.json') as json_file:
            self.data = json.load(json_file)
        print("Raw Data Read From Trigger File Information")
        print(self.data)
        # Create folder for each user to make a buffer memory for storing the image
        # Scan and check file in foler is empty or not. Request to add files if it is empty
        current_folder_path = os.getcwd()
        image_folder = os.path.join(current_folder_path, 'Image')
        script_folder = os.path.join(current_folder_path, 'Script')
        sql_folder = os.path.join(current_folder_path, 'SQL')
        os.chdir(current_folder_path)
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
            os.getcwd()
        os.chdir(image_folder)
        for user_data in self.data.keys():
            if not os.path.exists(os.path.join(image_folder,
                                               (self.data[user_data]['User'] + '_' + \
                                                self.data[user_data]['Data Description']))):
                os.makedirs(os.path.join(image_folder,
                                               (self.data[user_data]['User'] + '_' + \
                                                self.data[user_data]['Data Description'])))
        os.chdir(current_folder_path)
        if not os.path.exists(script_folder):
            os.makedirs(script_folder)
            os.getcwd()
        os.chdir(script_folder)
        for user_data in self.data.keys():
            if not os.path.exists(os.path.join(script_folder,
                                               (self.data[user_data]['User'] + '_' +
                                                self.data[user_data]['Data Description']))):
                os.makedirs(os.path.join(script_folder,
                                               (self.data[user_data]['User'] + '_' +
                                                self.data[user_data]['Data Description'])))
        os.chdir(current_folder_path)
        if not os.path.exists(sql_folder):
            os.makedirs(sql_folder)
            os.getcwd()
        os.chdir(sql_folder)
        for user_data in self.data.keys():
            if not os.path.exists(os.path.join(sql_folder,
                                               (self.data[user_data]['User'] + '_' +
                                                self.data[user_data]['Data Description']))):
                os.makedirs(os.path.join(sql_folder,
                                                (self.data[user_data]['User'] + '_' +
                                                 self.data[user_data]['Data Description'])))
        popup = input("Please Add All Files To SQL Folder And Script Then Typing Yes To Continue: ")
        if popup.lower() == 'no':
            print("Please Add All Files To SQL Folder And Script")
            self.chrome_driver.quit()
            sys.exit()
        elif popup.lower() == 'yes':
            for user_data in self.data.keys():
                script_folder_path = os.path.join(current_folder_path, 'Script')
                sql_folder_path = os.path.join(current_folder_path, 'SQL')
                for file in os.listdir(script_folder_path):
                    if not os.listdir(os.path.join(script_folder_path, file)):
                        print(f"Please Add All Files To Script Folder for {file}")
                        self.chrome_driver.quit()
                        sys.exit()
                    else:
                        print(f"Script File For Folder {file} Is Ready")
                for file in os.listdir(sql_folder_path):
                    if not os.listdir(os.path.join(sql_folder_path, file)):
                        print(f"Please Add All Files To SQL Folder {file}")
                        self.chrome_driver.quit()
                        sys.exit()
                    else:
                        print(f"SQL Folder For {file} Is Ready")
        else:
            print("Please Type Yes Or No And Run The Program Again")
            self.chrome_driver.quit()
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
        # Send message and image to each user
        for user_data in self.data.keys():
            self.search_box.clear()
            self.search_box.click()
            self.search_box.send_keys(self.data[user_data]['User'])
            self.search_box.send_keys(Keys.ENTER)
            print("Start Sending Message To {0}".format(self.data[user_data]['User']))
            message_box = self.wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.message_box_xpath)))
            message_box.clear()
            message_box.click()
            message_box.send_keys(self.data[user_data]['Text'] + '\n' +
                                  self.data[user_data]['Data Description'] + '\n' + "Time Period" + " " +
                              str(self.data[user_data]['Period']))
            time.sleep(1) # Wait for the message to be sent
            message_box.send_keys(Keys.ENTER)
            time.sleep(3)
            print("Start Sending Image To {0}".format(self.data[user_data]['User']))
            if os.listdir(os.path.join(image_path_folder, (self.data[user_data]['User'] + "_" +
                                                           self.data[user_data]['Data Description']))):
                for image in os.listdir(os.path.join(image_path_folder,
                                                     (self.data[user_data]['User'] + "_" +
                                                      self.data[user_data]['Data Description']))):
                    image_path = os.path.join(image_path_folder,
                                              os.path.join((
                                                      self.data[user_data]['User'] + "_" +
                                                      self.data[user_data]['Data Description']), image))
                    attachment_icon = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                      self.attachment_icon_xpath)))
                    attachment_icon.click()
                    image_attachment = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                       self.image_attachment_xpath)))
                    image_attachment.send_keys(image_path)
                    time.sleep(1)  # Wait for the image to be uploaded
                    send_image_button = self.wait.until(EC.presence_of_element_located((By.XPATH,
                                        self.send_button_xpath)))
                    send_image_button.click()
                    time.sleep(3)
            else:
                print(f"No Image In Folder "
                      f"{self.data[user_data]['User'] + '_' + self.data[user_data]['Data Description']}")
                self.search_box.clear()
                self.search_box.click()
                message_box = self.wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.message_box_xpath)))
                message_box.clear()
                message_box.click()
                message_box.send_keys("Data Is Empty")
                time.sleep(1)  # Wait for the message to be sent
                message_box.send_keys(Keys.ENTER)
                time.sleep(3)

    def delete_image_folder_buffer(self, image_path_folder):
    # Delete all image in image buffer folder
    # Prepare for next run with new image in image buffer folder
        for i in range(len(os.listdir(image_path_folder))):
            image_folder_path = os.path.join(image_path_folder, os.listdir(image_path_folder)[i])
            if os.listdir(image_folder_path):
                for image in os.listdir(image_folder_path):
                    os.remove(os.path.join(image_folder_path, image))


if __name__ == '__main__':
    trigger_path = os.getcwd() + "\Trigger_Information\data_trigger.csv"
    image_path_folder = os.getcwd() + "\Image"
    url = "https://web.whatsapp.com/"
    whatsapp = Whatsapp(url, trigger_path)
    whatsapp.send_message_and_image(image_path_folder=image_path_folder)
    whatsapp.delete_image_folder_buffer(image_path_folder=image_path_folder)
    # Bypass quiting chrome driver for testing
    # whatsapp.chrome_driver.quit()






