from selenium.webdriver.common.by import By

class LoginPage:

    def __init__(self, driver):
        self.driver = driver
        self.url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

    username = (By.NAME, "username")
    password = (By.NAME, "password")
    login_btn = (By.XPATH, "//button[@type='submit']")

    def open(self):
        self.driver.get(self.url)

    def login(self, user, pwd):
        self.driver.find_element(*self.username).send_keys(user)
        self.driver.find_element(*self.password).send_keys(pwd)
        self.driver.find_element(*self.login_btn).click()