from selenium.webdriver.common.by import By

class LeavePage:

    def __init__(self, driver):
        self.driver = driver

    leave_menu = (By.XPATH, "//span[text()='Leave']")
    apply_btn = (By.XPATH, "//a[text()='Apply']")
    from_date = (By.XPATH, "//input[@placeholder='yyyy-mm-dd']")
    to_date = (By.XPATH, "(//input[@placeholder='yyyy-mm-dd'])[2]")
    submit_btn = (By.XPATH, "//button[@type='submit']")
    status_text = (By.XPATH, "//div[contains(text(),'Pending')]")

    def open_leave_section(self):
        self.driver.find_element(*self.leave_menu).click()

    def apply_leave(self, start, end):
        self.driver.find_element(*self.apply_btn).click()
        self.driver.find_element(*self.from_date).send_keys(start)
        self.driver.find_element(*self.to_date).send_keys(end)
        self.driver.find_element(*self.submit_btn).click()

    def get_status(self):
        return self.driver.find_element(*self.status_text).text