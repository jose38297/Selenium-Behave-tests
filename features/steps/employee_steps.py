from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import datetime
import random

BASE_URL = "https://opensource-demo.orangehrmlive.com"


def vue_set_value(driver, element, value):
    """Set value on a Vue.js input and trigger all necessary events."""
    driver.execute_script("""
        var el = arguments[0];
        var value = arguments[1];
        var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, value);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    """, element, value)


def wait_for_loader(driver, timeout=10):
    """Wait until the oxd-form-loader spinner disappears."""
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "oxd-form-loader"))
        )
    except Exception:
        pass  # If loader never appeared, that's fine


def click_submit(driver):
    """Wait for loader to disappear, then click submit via JS to bypass interception."""
    wait_for_loader(driver)
    submit_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
    )
    driver.execute_script("arguments[0].click();", submit_btn)


def find_employee_name_input(driver):
    """
    Trouve le champ 'Employee Name' avec plusieurs sélecteurs en fallback.
    Affiche les inputs disponibles en mode debug si tous les sélecteurs échouent.
    """
    selectors = [
        (By.XPATH,        "//label[text()='Employee Name']/following::input[1]"),
        (By.XPATH,        "//label[normalize-space()='Employee Name']/following::input[1]"),
        (By.XPATH,        "//input[@placeholder='Type for hints...']"),
        (By.CSS_SELECTOR, ".oxd-autocomplete-text-input input"),
        (By.XPATH,        "(//div[contains(@class,'oxd-input-group')]//input[@placeholder])[1]"),
    ]

    for by, selector in selectors:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((by, selector))
            )
            print(f"✅ Champ 'Employee Name' trouvé avec: {selector}")
            return element
        except Exception:
            print(f"⚠️ Sélecteur échoué: {selector}")
            continue

    # Mode debug — afficher tous les inputs visibles pour diagnostic
    print("🔎 DEBUG — inputs visibles sur la page:")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for i, inp in enumerate(inputs):
        print(
            f"  input[{i}] "
            f"placeholder='{inp.get_attribute('placeholder')}' "
            f"class='{inp.get_attribute('class')}' "
            f"name='{inp.get_attribute('name')}'"
        )

    raise AssertionError("❌ Champ 'Employee Name' introuvable avec tous les sélecteurs")


def search_employee(driver, wait, fullname):
    """
    Navigue vers la liste des employés et recherche par nom complet.
    Utilise find_employee_name_input() avec fallback multi-sélecteurs.
    """
    driver.get(BASE_URL + "/web/index.php/pim/viewEmployeeList")
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "oxd-table")))
    wait_for_loader(driver)
    time.sleep(4)  # laisser Vue finir le rendu complet

    name_input = find_employee_name_input(driver)

    # Utiliser vue_set_value pour déclencher la réactivité Vue.js
    vue_set_value(driver, name_input, fullname)
    time.sleep(2)

    suggestions = driver.find_elements(By.XPATH, "//div[@role='option']")
    if suggestions:
        suggestions[0].click()
        time.sleep(1)
    else:
        print("⚠️ Pas d'autocomplete, recherche directe")

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)


def set_employee_id(driver, wait):
    """Try to set a unique Employee ID, retrying with a new random ID if already taken."""
    max_attempts = 10
    for attempt in range(max_attempts):
        new_id = str(random.randint(1000, 9999))

        wait_for_loader(driver)

        emp_id_field = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
            )
        )
        vue_set_value(driver, emp_id_field, new_id)
        time.sleep(0.5)

        print(f"🔍 Tentative {attempt + 1} — Employee ID: {new_id}")

        click_submit(driver)
        time.sleep(3)

        # Vérifier erreur sur l'ID
        id_errors = driver.find_elements(
            By.XPATH,
            "//label[text()='Employee Id']/following::span[contains(@class,'oxd-input-field-error-message')][1]"
        )
        id_error_texts = [e.text for e in id_errors if e.text.strip()]

        if id_error_texts:
            print(f"⚠️ ID {new_id} rejeté: {id_error_texts} — nouvel essai...")
            continue

        # Succès : l'URL a changé
        if "addEmployee" not in driver.current_url:
            print(f"✅ Employee ID {new_id} accepté")
            return True

        # Toujours sur la page — autres erreurs ?
        other_errors = driver.find_elements(
            By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]"
        )
        other_texts = [e.text for e in other_errors if e.text.strip()]
        if other_texts:
            print(f"❌ Autres erreurs (non liées à l'ID): {other_texts}")
            return False

        print(f"⚠️ Toujours sur addEmployee sans erreur visible — nouvel essai ID...")

    raise AssertionError(f"❌ Impossible de trouver un Employee ID unique après {max_attempts} tentatives")


# ---------------------------------------------------------------------------
# STEPS
# ---------------------------------------------------------------------------

@given("je suis connecté en tant qu'admin")
def step_login(context):
    driver = context.driver
    driver.get(BASE_URL + "/web/index.php/auth/login")

    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.NAME, "username")))

    driver.find_element(By.NAME, "username").send_keys("Admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait.until(EC.url_contains("/dashboard"))
    print("✅ Connecté avec succès")


@when("je crée un nouvel employé")
def step_add_employee(context):
    driver = context.driver
    wait = WebDriverWait(driver, 30)

    suffix = datetime.datetime.now().strftime("%H%M%S")
    context.emp_firstname = "QA"
    context.emp_lastname  = f"Tester{suffix}"
    context.emp_fullname  = f"{context.emp_firstname} {context.emp_lastname}"

    driver.get(BASE_URL + "/web/index.php/pim/addEmployee")
    wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
    time.sleep(2)

    fn = driver.find_element(By.NAME, "firstName")
    ln = driver.find_element(By.NAME, "lastName")

    vue_set_value(driver, fn, context.emp_firstname)
    time.sleep(0.5)
    vue_set_value(driver, ln, context.emp_lastname)
    time.sleep(0.5)

    print(f"🔍 firstName: {fn.get_attribute('value')}")
    print(f"🔍 lastName:  {ln.get_attribute('value')}")

    set_employee_id(driver, wait)

    if "addEmployee" in driver.current_url:
        errors = driver.find_elements(
            By.XPATH, "//span[contains(@class,'oxd-input-field-error-message')]"
        )
        error_texts = [e.text for e in errors if e.text.strip()]
        raise AssertionError(f"❌ Toujours sur addEmployee. Erreurs: {error_texts}")

    print(f"✅ Employé {context.emp_fullname} créé — URL: {driver.current_url}")


@then("l'employé doit apparaître dans la liste des employés")
def step_verify_employee(context):
    driver = context.driver
    wait = WebDriverWait(driver, 30)

    search_employee(driver, wait, context.emp_fullname)

    rows = driver.find_elements(
        By.XPATH, "//div[@class='oxd-table-body']//div[@role='row']"
    )
    assert len(rows) > 0, f"❌ Employé '{context.emp_fullname}' non trouvé dans la liste"
    print(f"✅ Employé {context.emp_fullname} trouvé dans la liste")


@when("je modifie les informations de l'employé")
def step_edit_employee(context):
    driver = context.driver
    wait = WebDriverWait(driver, 30)

    search_employee(driver, wait, context.emp_fullname)

    edit_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//div[@class='oxd-table-body']//div[@role='row'])[1]//button[1]")
        )
    )
    edit_btn.click()

    wait.until(EC.url_contains("/pim/viewPersonalDetails"))
    time.sleep(2)

    firstname = wait.until(EC.element_to_be_clickable((By.NAME, "firstName")))
    vue_set_value(driver, firstname, "Automation")
    time.sleep(0.5)

    print(f"🔍 firstName après édition: {firstname.get_attribute('value')}")

    context.emp_firstname = "Automation"
    context.emp_fullname  = f"Automation {context.emp_lastname}"

    wait_for_loader(driver)
    click_submit(driver)

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")
        )
    )
    print("✅ Employé modifié avec succès")


@then("les informations mises à jour doivent être visibles")
def step_verify_update(context):
    driver = context.driver
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
    name = driver.find_element(By.NAME, "firstName").get_attribute("value")
    print(f"🔍 firstName lu: '{name}'")
    assert name == "Automation", f"❌ Attendu 'Automation', obtenu '{name}'"
    print("✅ Mise à jour vérifiée")


@when("je supprime l'employé")
def step_delete_employee(context):
    driver = context.driver
    wait = WebDriverWait(driver, 30)

    search_employee(driver, wait, context.emp_fullname)

    delete_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "(//div[@class='oxd-table-body']//div[@role='row'])[1]//button[2]")
        )
    )
    delete_btn.click()

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Yes, Delete']")
        )
    ).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'oxd-toast--success')]")
        )
    )
    print("✅ Employé supprimé avec succès")


@then("l'employé ne doit plus apparaître dans la liste")
def step_verify_delete(context):
    driver = context.driver
    wait = WebDriverWait(driver, 20)

    wait_for_loader(driver)
    time.sleep(2)

    name_input = find_employee_name_input(driver)
    name_input.clear()
    vue_set_value(driver, name_input, context.emp_fullname)
    time.sleep(2)

    suggestions = driver.find_elements(By.XPATH, "//div[@role='option']")
    if not suggestions:
        print("✅ Aucune suggestion → employé bien supprimé")
        return

    suggestions[0].click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

    rows = driver.find_elements(
        By.XPATH, "//div[@class='oxd-table-body']//div[@role='row']"
    )
    assert len(rows) == 0, "❌ L'employé apparaît encore après suppression"
    print("✅ Suppression confirmée")