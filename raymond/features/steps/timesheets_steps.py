import time
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta


@given("je suis connecté en tant qu'admin")
def step_login_as_admin(context):
    driver = context.driver
    wait = WebDriverWait(driver, 40)

    driver.get(f"{context.base_url}/web/index.php/auth/login")
    wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

    wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys(context.admin_username)
    wait.until(EC.visibility_of_element_located((By.NAME, "password"))).send_keys(context.admin_password)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    wait.until(EC.url_contains("dashboard"))


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
    time.sleep(0.5)
    employee_input.send_keys("John")
    time.sleep(3)  # ← augmenté à 3s pour laisser le dropdown charger

    first_option = wait.until(
        EC.element_to_be_clickable(                          # ← clickable au lieu de visible
            (By.XPATH, "//div[@role='listbox']//div[@role='option']")
        )
    )
    context.selected_employee = first_option.text.strip()
    first_option.click()
    time.sleep(1)  # ← attendre que la sélection soit validée

    # Vérifier qu'il n'y a pas de message "Invalid"
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Invalid" not in page_text, \
        f"La sélection de l'employé a échoué — champ marqué Invalid."

    print(f"\n👤 Employé sélectionné : {context.selected_employee}")


@when("je sélectionne la période de la semaine courante")
def step_select_current_week(context):
    driver = context.driver
    wait = WebDriverWait(driver, 20)

    # Cliquer sur View pour charger la feuille de temps
    wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='View']"))
    ).click()
    time.sleep(3)  # ← augmenté à 3s

    # Vérifier qu'on est bien sur la page de timesheet
    wait.until(EC.url_contains("viewTimesheet"))

@then("la feuille de temps de l'employé doit être affichée")
def step_verify_timesheet_displayed(context):
    driver = context.driver
    wait = WebDriverWait(driver, 15)

    # 1. Vérifier que l'URL contient viewTimesheet
    assert "viewTimesheet" in driver.current_url, \
        f"Mauvaise URL : {driver.current_url}"

    # 2. Vérifier que le nom de l'employé est dans la page
    page_content = driver.find_element(By.TAG_NAME, "body").text
    assert context.selected_employee in page_content, \
        f"Employé '{context.selected_employee}' absent de la page."

    # 3. Vérifier "Timesheet Period" visible dans le texte de la page
    assert "Timesheet Period" in page_content, \
        "Bloc 'Timesheet Period' non trouvé dans la page."

    print(f"\n✅ Feuille de temps affichée pour : {context.selected_employee}")
    print(f"   URL : {driver.current_url}")