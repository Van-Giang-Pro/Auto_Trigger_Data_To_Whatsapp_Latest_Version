from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


class Whatsapp:
    search_box_xpath = "//div[@title='Tìm kiếm bằng ô nhập văn bản']"
    message_box_xpath = "//div[@title='Nhập tin nhắn']"
    attachment_icon_xpath = ''
    image_attachment_xpath = ''
    send_button_xpath = ''

    def __init__(self, url, trigger_path):
        self.url = url
        self.trigger_path = trigger_path

        # Set Up For Personal Laptop
        # driver_path = r"C:\Users\Admin\Desktop\Personal Documents" \
        #               r"\Python Project\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
        #               r"\Chrome_Driver\chromedriver.exe"

        # Set Up For Company Laptop
        driver_path = r"C:\Users\fs120806\PycharmProjects" \
                      r"Auto_Trigger_Data_To_Whatsapp_Latest_Version\Chrome_Driver" \
                      r"\chromedriver.exe"

        # Set Up For Home PC
        # driver_path = r"C:\Users\admin\PycharmProjects" \
        #               r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
        #               r"\Chrome_Driver\chromedriver.exe"

        # Set Up For Personal Laptop
        # chrome_directory = r"user-data-dir=C:\Users\Admin\AppData" \
        #                    r"\Local\Google\Chrome\User_Data_For_Auto_Trigger_System"

        # Set Up For Company Laptop
        chrome_directory = r"user-data-dir=C:\Users\fs120806\AppData\Local\Google\Chrome" \
                           r"\User_Data_For_Auto_Trigger_System"

        # Set Up For Home PC
        # chrome_directory = r"user-data-dir=C:\Users\admin\AppData\Local\Google" \
        #                    r"\Chrome\User_Data_For_Auto_Trigger_System"
        self.chrome_options = Options()
        self.chrome_options.add_argument(chrome_directory)
        self.chrome_options.add_experimental_option("detach", True)
        # Keep the chrome driver open after the program is finished
        self.service = Service(driver_path)
        self.chrome_driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.chrome_driver.get(self.url)
        page_title = self.chrome_driver.title
        # Get the title of the website
        print(f"The Website You Are Accessing Is {page_title}")

    def read_trigger_information(self):
	    with open(self.trigger_path, 'r') as file:
		    df = pd.read_csv(file)
		    user_dict_list = []
		    for i in range(len(df.index)):
			    user = {'User': (df.iloc[i]).loc['User'],
			            'Text': (df.iloc[i]).loc['Text'],
			            'Content': (df.iloc[i]).loc['Image'],
			            'Period': (df.iloc[i]).loc['Time Period (Minutes)']}
		    user_dict_list.append(user)
	    return user_dict_list

    def run_script_export_image(self):
	    user_dict_list = self.read_trigger_information()
	    for user in user_dict_list:
		    script_link = user['Content']
		    print(script_link)
		    period = user['Period']
		    print(period)

    def send_message(self):
	    wait = WebDriverWait(self.chrome_driver, 40)
	    try:
	        search_box = wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.search_box_xpath)))
	    except TimeoutException:
		    print("The Website Is Not Available Or The Internet Connection Is Not Stable")
		    self.chrome_driver.quit()
		    return None
	    for user in user_dict_list:
		    search_box.clear()
		    search_box.click()
		    search_box.send_keys(user['User'])
		    search_box.send_keys(Keys.ENTER)
		    print("Start Sending Message To {0}".format(user['User']))
		    message_box = wait.until(EC.presence_of_element_located((By.XPATH, Whatsapp.message_box_xpath)))
		    message_box.clear()
		    message_box.click()
		    message_box.send_keys(user['Text'])
		    time.sleep(1) # Wait for the message to be sent
		    message_box.send_keys(Keys.ENTER)


    def send_image(self, image_path_folder):
	    wait = WebDriverWait(self.chrome_driver, 40)
	    search_box_xpath = ''
	    message_box_xpath = ''
	    attachment_icon_xpath = ''
	    image_attachment_xpath = ''
	    send_button_xpath = ''
	    for user in user_dict_list:
		    search_box.clear()
		    search_box.click()
		    search_box.send_keys(user['User'])
		    search_box.send_keys(Keys.ENTER)
		    print("Start Sending Message To {0}".format(user['User']))
		    message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_xpath)))
		    message_box.clear()
		    message_box.click()
		    message_box.send_keys(user['Text'])
		    time.sleep(1)  # Wait for the message to be sent
		    message_box.send_keys(Keys.ENTER)
		    print("Start Sending Image To {0}".format(user['User']))
		    attachment_icon = wait.until(EC.presence_of_element_located((By.XPATH, attachment_icon_xpath)))
		    attachment_icon.click()
		    image_attachment = wait.until(EC.presence_of_element_located((By.XPATH, image_attachment_xpath)))
		    image_attachment.send_keys(image_path_folder)
		    time.sleep(1)  # Wait for the image to be uploaded
		    send_image_button = wait.until(EC.presence_of_element_located((By.XPATH, send_button_xpath)))
		    send_image_button.click()


if __name__ == '__main__':
	# Set Up For Company Laptop
	trigger_path = (r"C:\Users\fs120806\PycharmProjects" \
	                r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
	                r"\Trigger_Information\data_trigger.csv")
	# Set Up For Personal Laptop
	# trigger_path = r"C:\Users\Admin\Desktop\Personal Documents\Python Project" \
	#                 r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
	#                 r"\Trigger_Information\data_trigger.csv"

	# Set Up For Personal Laptop
	# image_path_folder = r"C:\Users\Admin\Desktop\Personal Documents\Python Project" \
	# 					 "\Auto_Trigger_Data_To_Whatsapp_Latest_Version\Image\Giang.png"

	# Set Up For Company Laptop
	image_path_folder = (r"C:\Users\fs120806\PycharmProjects" \
	                    r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version\Image\Giang.png")
	url = "https://web.whatsapp.com/"
	whatsapp = Whatsapp(url, trigger_path)
	user_dict_list = whatsapp.read_trigger_information()
	whatsapp.send_message()
	# whatsapp.send_image(image_path_folder=image_path_folder)
	whatsapp.run_script_export_image()






