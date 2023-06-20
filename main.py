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
import whatsapp


if __name__ == '__main__':
	whatsapp_link = "https://web.whatsapp.com/"
	whatsapp = whatsapp.Whatsapp(whatsapp_link)
	whatsapp.send_message_and_image()
	whatsapp.delete_image_folder_buffer()
	# Bypass quiting chrome driver for testing
	whatsapp.chrome_driver.quit()
	print("Program Is Done, Thank You For Using This Program")
	print("Wrote By: Nguyễn Văn Giang")
	print("Email: vangiang260694@gmail.com")
	print("Phone: 0383069353")
	print("Company: First Solar Vietnam")


