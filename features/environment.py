"""
# features/environment.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_binary  # installe le driver automatiquement

def before_all(context):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    context.driver = webdriver.Chrome(options=chrome_options)

def after_all(context):
    if hasattr(context, "driver"):
        context.driver.quit()




"""
from selenium import webdriver


def before_all(context):

    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

    context.base_url = "https://opensource-demo.orangehrmlive.com"


def after_all(context):

    context.driver.quit()
    
