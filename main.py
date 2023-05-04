from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd


class TriggerInformation:
    def __init__(self, trigger_information_path):
        self.trigger_information_path = trigger_information_path
    def read_trigger_information(self):
        with open(self.trigger_information_path, 'r') as file:
            df = pd.read_csv(file)
            user_dict_list = []
            for i in range(len(df.index)):
                user = {'User': (df.iloc[i]).loc['User'],
                           'Type': (df.iloc[i]).loc['Text'],
                           'Content': (df.iloc[i]).loc['Image'],
                           'Period': (df.iloc[i]).loc['Time Period (Minutes)']}
                user_dict_list.append(user)
            print(user_dict_list)
            print(type(user_dict_list))
        return user_dict_list


class Whatsapp:
    @staticmethod
    def access_whatsapp():
        # Set Up For Personal Laptop
        driver_path = r"C:\Users\Admin\Desktop\Personal Documents" \
                      r"\Python Project\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
                      r"\Chrome_Driver\chromedriver.exe"

        # Set Up For Company PC
        # driver_path = r"C:\Users\fs120806\PycharmProjects" \
        #               r"Auto_Trigger_Data_To_Whatsapp_Latest_Version\Chrome_Driver" \
        #               r"\chromedriver.exe"

        # # Set Up For Home PC
        # driver_path = r"C:\Users\admin\PycharmProjects" \
        #               r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
        #               r"\Chrome_Driver\chromedriver.exe"

        # Set Up For Personal Laptop
        chrome_directory = r"user-data-dir=C:\Users\Admin\AppData" \
                           r"\Local\Google\Chrome\User_Data_For_Auto_Trigger_System"

        # Set Up For Company PC
        # chrome_directory = r"user-data-dir=C:\Users\fs120806\AppData\Local\Google\Chrome" \
        #                    r"\User_Data_For_Auto_Trigger_System"

        # Set Up For Home PC
        # chrome_directory = r"user-data-dir=C:\Users\admin\AppData\Local\Google" \
        #                    r"\Chrome\User_Data_For_Auto_Trigger_System"
        chrome_options = Options()
        chrome_options.add_argument(chrome_directory)
        chrome_options.add_experimental_option("detach", True)
        service = Service(driver_path)
        chrome_driver = webdriver.Chrome(service=service, options=chrome_options)
        chrome_driver.set_page_load_timeout(3)
        chrome_driver.get("https://web.whatsapp.com/")


class AccessWebsiteConfig:
    def __init__(self, url, web_page_timeout):
        self.url = url
        self.web_page_timeout = web_page_timeout
        # Set Up For Personal Laptop
        driver_path = r"C:\Users\Admin\Desktop\Personal Documents" \
                      r"\Python Project\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
                      r"\Chrome_Driver\chromedriver.exe"

        # Set Up For Company PC
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

        # Set Up For Company PC
        # chrome_directory = r"user-data-dir=C:\Users\fs120806\AppData\Local\Google\Chrome" \
        #                    r"\User_Data_For_Auto_Trigger_System"

        # Set Up For Home PC
        # chrome_directory = r"user-data-dir=C:\Users\admin\AppData\Local\Google" \
        #                    r"\Chrome\User_Data_For_Auto_Trigger_System"
        self.chrome_options = Options()
        self.chrome_options.add_argument(chrome_directory)
        self.chrome_options.add_experimental_option("detach", True)
        # Keep the chrome driver open after the program is finished
        self.service = Service(driver_path)
        self.chrome_driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.chrome_driver.set_page_load_timeout(self.web_page_timeout)
        try:
            self.chrome_driver.get(self.url)
        except:
            print("The website Is Not Available Or The Internet Connection Is Not Stable")
        page_title = self.chrome_driver.title
        # Get the title of the website
        print(f"The Website You Are Accessing Is {page_title}")


class SendInformation(TriggerInformation, AccessWebsiteConfig):
    @staticmethod
    def send_information():
        pass


if __name__ == '__main__':
    access_website = AccessWebsiteConfig("https://web.whatsapp.com/", 10)
    triggerinformation= TriggerInformation(r"C:\Users\Admin\Desktop\Personal Documents\Python Project" \
                                           r"\Auto_Trigger_Data_To_Whatsapp_Latest_Version" \
                                           r"\Trigger_Information\data_trigger.csv")
    user_dict_list = triggerinformation.read_trigger_information()
    print(user_dict_list[1])







