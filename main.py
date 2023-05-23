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
        # Set Up For Personal Laptop
        driver_path = r"C:\Users\Admin\Desktop\Personal Documents" \
                      r"\Python Project\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
                      r"\Chrome_Driver\chromedriver.exe"
        # Set Up For Company Laptop
        # driver_path = r"C:\Users\fs120806\PycharmProjects" \
        #               r"Auto_Trigger_Data_To_Whatsapp_Latest_Version\Chrome_Driver" \
        #               r"\chromedriver.exe"
        # Set Up For Home PC
        # driver_path = r"C:\Users\admin\PycharmProjects" \
        #               r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
        #               r"\Chrome_Driver\chromedriver.exe"
        # Set Up For Personal Laptop
        chrome_directory = r"user-data-dir=C:\Users\Admin\AppData" \
                           r"\Local\Google\Chrome\User_Data_For_Auto_Trigger_System"
        # Set Up For Company Laptop
        # chrome_directory = r"user-data-dir=C:\Users\fs120806\AppData\Local\Google\Chrome" \
        #                    r"\User_Data_For_Auto_Trigger_System"
        # Set Up For Home PC
        # chrome_directory = r"user-data-dir=C:\Users\admin\AppData\Local\Google" \
        #                    r"\Chrome\User_Data_For_Auto_Trigger_System"
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
            print(self.user_dict_list)

    def send_message_and_image(self, image_path_folder):
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
	        for i in range(len(self.user_dict_list)):
		        script_folder_path = self.user_dict_list[i]['Script Folder']
		        if (os.listdir(script_folder_path) == []):
			        print(f"Please Add All Files To Script Folder for {self.user_dict_list[i]['User'] + ' ' + self.user_dict_list[i]['Data Description']}")
		        else:
			        print(f"Script Folder For {self.user_dict_list[i]['User'] + ' ' + self.user_dict_list[i]['Data Description']} Is Ready")
	        for i in range(len(self.user_dict_list)):
		        sql_folder_path = self.user_dict_list[i]['SQL Folder']
		        if (os.listdir(sql_folder_path) == []):
			        print(f"Please Add All Files To SQL Folder {self.user_dict_list[i]['User'] + ' ' + self.user_dict_list[i]['Data Description']}")
		        else:
			        print(f"SQL Folder For {self.user_dict_list[i]['User'] + ' ' + self.user_dict_list[i]['Data Description']} Is Ready")
        else:
	        print("Please Type Yes Or No")

        # for i in range(len(image_folder_list)):
        #     image_folder_path_area.append(os.path.join(image_path_folder, image_folder_list[i]))
        # for i in range(len(image_folder_path_area)): # Count number of folder in image folder
        #     for j in range(len(os.listdir(image_folder_path_area[i]))): # Count number of image in each folder
        #         image_path.append(os.path.join(image_folder_path_area[i], (os.listdir(image_folder_path_area[i])[j])))
        # print(image_folder_path_area)
        # print(image_path)
        # # Send message and image to each user
        # for user in self.user_dict_list:
        #     self.search_box.clear()
        #     self.search_box.click()
        #     self.search_box.send_keys(user['User'])
        #     self.search_box.send_keys(Keys.ENTER)
        #     print("Start Sending Message To {0}".format(user['User']))
        #     message_box = self.wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.message_box_xpath)))
        #     message_box.clear()
        #     message_box.click()
        #     message_box.send_keys(user['Text'] + '\n' + user['Data Description'])
        #     time.sleep(1) # Wait for the message to be sent
        #     message_box.send_keys(Keys.ENTER)
        #     time.sleep(3)
        #     print("Start Sending Image To {0}".format(user['User']))
        #     for i in range(len(image_path)):
        #         image_path = os.path.join(image_path_folder, image_path[i])  # Get the image path
        #         attachment_icon = self.wait.until(EC.presence_of_element_located((By.XPATH, self.attachment_icon_xpath)))
        #         attachment_icon.click()
        #         image_attachment = self.wait.until(EC.presence_of_element_located((By.XPATH, self.image_attachment_xpath)))
        #         image_attachment.send_keys(image_path[i])
        #         time.sleep(1)  # Wait for the image to be uploaded
        #         send_image_button = self.wait.until(EC.presence_of_element_located((By.XPATH, self.send_button_xpath)))
        #         send_image_button.click()
        #         time.sleep(3)


# class CreateImage:
# 	def __inti__(self, script_folder_path):
# 		self.script_folder_path = script_folder_path


if __name__ == '__main__':
	# Set Up For Personal Laptop
	trigger_path = r"C:\Users\Admin\Desktop\Personal Documents\Python Project" \
	               r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
	               r"\Trigger_Information\data_trigger.csv"
	# Set Up For Company Laptop
	# trigger_path = (r"C:\Users\fs120806\PycharmProjects" \
	#                 r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
	#                 r"\Trigger_Information\data_trigger.csv")
	# Set Up For Home PC
	# trigger_path = r"C:\Users\admin\PycharmProjects" \
	#                r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
	#                r"\Trigger_Information\data_trigger.csv"
	# Set Up For Personal Laptop
	image_path_folder = r"C:\Users\Admin\Desktop\Personal Documents\Python Project" \
						  r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version"
	# Set Up For Company Laptop
	# image_path_folder = r"C:\Users\fs120806\PycharmProjects" \
	#                     r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version\Image"
	# Set Up For Home PC
	# image_path_folder = r"C:\Users\fs120806\PycharmProjects" \
	#                     r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version\Image"
	url = "https://web.whatsapp.com/"
	whatsapp = Whatsapp(url, trigger_path)
	whatsapp.send_message_and_image(image_path_folder=image_path_folder)






