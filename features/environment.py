from selenium import webdriver


def before_all(context):

    context.driver = webdriver.Chrome()
    context.driver.maximize_window()

    context.base_url = "https://opensource-demo.orangehrmlive.com"


def after_all(context):

    context.driver.quit()