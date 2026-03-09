from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def before_all(context):
    context.base_url = "https://opensource-demo.orangehrmlive.com"
    context.admin_username = "Admin"
    context.admin_password = "admin123"
    context.employee_name = "John"

def before_scenario(context, scenario):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    context.driver = webdriver.Chrome(options=chrome_options)
    context.driver.implicitly_wait(10)
    context.driver.set_page_load_timeout(60)   # ← clé du problème

def after_scenario(context, scenario):
    if scenario.status == "failed":
        screenshot_name = scenario.name.replace(" ", "_") + "_FAILED.png"
        context.driver.save_screenshot(f"reports/{screenshot_name}")
        print(f"\n📸 Screenshot : reports/{screenshot_name}")
    context.driver.quit()

def after_all(context):
    print("\n✅ Suite de tests terminée.")