import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


@given("je suis connecté en tant qu'admin")
def step_login_as_admin(context):
    driver = context.driver
    wait = WebDriverWait(driver, 40)

    driver.get(f"{context.base_url}/web/index.php/auth/login")

    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(context.admin_username)
    wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(context.admin_password)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

    wait.until(EC.url_contains("dashboard"))

    print("[SUCCESS] Login admin réussi")


@given("je navigue vers la page Timesheets")
def step_navigate_to_timesheets(context):
    driver = context.driver
    wait = WebDriverWait(driver, 20)

    driver.get(f"{context.base_url}/web/index.php/time/viewEmployeeTimesheet")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Type for hints...']")
        )
    )

    print("[INFO] Page Timesheets chargée")


@when("je sélectionne un employé dans la liste")
def step_select_employee(context):
    driver = context.driver
    wait = WebDriverWait(driver, 20)

    employee_input = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@placeholder='Type for hints...']")
        )
    )

    employee_input.click()
    employee_input.send_keys(Keys.CONTROL + "a")
    employee_input.send_keys(Keys.DELETE)

    employee_input.send_keys("John")

    dropdown_option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='listbox']//div[@role='option']")
        )
    )

    context.selected_employee = dropdown_option.text.strip()

    dropdown_option.click()

    wait.until(
        lambda d: context.selected_employee in d.find_element(By.TAG_NAME, "body").text
    )

    page_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Invalid" not in page_text, \
        "[ERROR] La sélection de l'employé a échoué (champ Invalid)"

    print(f"[INFO] Employé sélectionné : {context.selected_employee}")


@when("je sélectionne la période de la semaine courante")
def step_select_current_week(context):
    driver = context.driver
    wait = WebDriverWait(driver, 20)

    view_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='View']")
        )
    )

    view_button.click()

    wait.until(EC.url_contains("viewTimesheet"))

    print("[INFO] Timesheet demandée")


@then("la feuille de temps de l'employé doit être affichée")
def step_verify_timesheet_displayed(context):
    driver = context.driver
    wait = WebDriverWait(driver, 20)

    wait.until(EC.url_contains("viewTimesheet"))

    current_url = driver.current_url

    assert "viewTimesheet" in current_url, \
        f"[ERROR] Mauvaise page chargée : {current_url}"

    page_content = driver.find_element(By.TAG_NAME, "body").text

    assert context.selected_employee in page_content, \
        f"[ERROR] Employé '{context.selected_employee}' non trouvé dans la page"

    assert "Timesheet Period" in page_content, \
        "[ERROR] Bloc 'Timesheet Period' absent"

    print(f"[SUCCESS] Feuille de temps affichée pour : {context.selected_employee}")
    print(f"[INFO] URL : {current_url}")