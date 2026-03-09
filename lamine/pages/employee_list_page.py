# =============================================================================
# PAGE OBJECT : EmployeeListPage (version finale corrigee)
# =============================================================================
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time

BASE_URL = "https://opensource-demo.orangehrmlive.com"


class EmployeeListPage:

    # -----------------------------------------------------------------------
    # LOCATORS - confirmes par inspection HTML reelle
    # -----------------------------------------------------------------------

    # Champ autocomplete "Employee Name" - selecteur confirme par HTML reel :
    # Structure : label "Employee Name" -> oxd-autocomplete-wrapper -> input
    # On cible via le label pour eviter de prendre le champ Supervisor Name
    EMPLOYEE_NAME_INPUT = (By.XPATH,
        "//label[normalize-space(text())='Employee Name']"
        "/parent::div/parent::div//input[@placeholder='Type for hints...']")

    # Suggestions autocomplete
    AUTOCOMPLETE_OPTIONS = (By.CSS_SELECTOR,
        ".oxd-autocomplete-dropdown .oxd-autocomplete-option")

    # Champ "Employee Id" - selecteur base sur le HTML reel :
    # Structure : label-wrapper > label "Employee Id"
    #             frere div > input.oxd-input--active
    # XPath : label -> remonte au groupe -> descend vers input
    EMPLOYEE_ID_INPUT = (By.XPATH,
        "//label[normalize-space(text())='Employee Id']"
        "/parent::div/parent::div//input[contains(@class,'oxd-input--active')]")

    # Bouton Search
    SEARCH_BUTTON = (By.CSS_SELECTOR,
        "button[type='submit'].oxd-button--secondary")

    # Bouton Reset
    RESET_BUTTON = (By.CSS_SELECTOR,
        "button[type='reset']")

    # Dropdown Sub Unit (via label HTML confirme)
    SUB_UNIT_SELECT = (By.XPATH,
        "//label[text()='Sub Unit']/ancestor::div[contains(@class,'oxd-input-group')]"
        "//div[contains(@class,'oxd-select-text-input')]")

    # Options dropdown ouvert
    DROPDOWN_OPTIONS = (By.CSS_SELECTOR,
        ".oxd-select-dropdown [role='option'] span")

    # Lignes du tableau
    RESULT_ROWS = (By.CSS_SELECTOR,
        ".oxd-table-body .oxd-table-row")

    # Message No Records Found
    NO_RECORDS_MSG = (By.XPATH,
        "//*[contains(text(),'No Records')]")


    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 20)


    def open(self):
        """Ouvre la page liste des employes et attend qu elle soit prete."""
        self.driver.get(BASE_URL + "/web/index.php/pim/viewEmployeeList")
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        time.sleep(1.5)


    def _reset_form(self):
        """
        Remet le formulaire a zero en cliquant sur Reset.
        Attend que la page soit de nouveau stable apres le reset.
        """
        btns = self.driver.find_elements(*self.RESET_BUTTON)
        if btns:
            btns[0].click()
            # Attend que le bouton Search soit de nouveau cliquable
            # = la page a fini de se reinitialiser
            self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
            time.sleep(1)


    def _click_search(self):
        """Clique sur Search et attend la stabilisation du tableau."""
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON))
        btns = self.driver.find_elements(*self.SEARCH_BUTTON)
        if btns:
            btns[0].click()
        time.sleep(3)


    # -----------------------------------------------------------------------
    # RECHERCHE PAR AUTOCOMPLETE (Employee Name)
    # -----------------------------------------------------------------------
    def search_by_name_autocomplete(self, name):
        """
        Tape un nom dans le champ autocomplete Employee Name.
        Selectionne la premiere suggestion si disponible.
        """
        self._reset_form()

        if not name:
            self._click_search()
            return

        try:
            field = self.wait.until(
                EC.element_to_be_clickable(self.EMPLOYEE_NAME_INPUT)
            )
            field.clear()
            field.send_keys(name)
        except TimeoutException:
            self._click_search()
            return

        # Attend les suggestions (2 secondes)
        time.sleep(2)
        suggestions = self.driver.find_elements(*self.AUTOCOMPLETE_OPTIONS)

        if suggestions:
            suggestions[0].click()
            time.sleep(0.5)

        self._click_search()


    # -----------------------------------------------------------------------
    # RECHERCHE PAR EMPLOYEE ID
    # -----------------------------------------------------------------------
    def search_by_employee_id(self, employee_id):
        """
        Recherche via le champ Employee Id.
        Selecteur confirme : //label[text()=Employee Id]//input
        Champ simple input texte, sans autocomplete -> tres fiable.
        """
        self._reset_form()

        try:
            # Localise le champ via le label Employee Id confirme
            id_field = self.wait.until(
                EC.element_to_be_clickable(self.EMPLOYEE_ID_INPUT)
            )
            id_field.clear()
            id_field.send_keys(employee_id)
            print("  -> ID saisi : [" + employee_id + "]")
        except TimeoutException as e:
            print("  [WARN] Champ Employee ID introuvable : " + str(e))

        self._click_search()


    # -----------------------------------------------------------------------
    # FILTRE PAR SOUS-UNITE
    # -----------------------------------------------------------------------
    def filter_by_sub_unit(self, department):
        """Selectionne un departement dans le dropdown Sub Unit."""
        try:
            select = self.wait.until(
                EC.element_to_be_clickable(self.SUB_UNIT_SELECT)
            )
            select.click()
            time.sleep(0.5)

            options = self.wait.until(
                EC.presence_of_all_elements_located(self.DROPDOWN_OPTIONS)
            )
            for opt in options:
                if department.lower() in opt.text.lower():
                    opt.click()
                    break
        except Exception as e:
            print("  [WARN] Sub Unit : " + str(e))

        self._click_search()


    # -----------------------------------------------------------------------
    # GETTERS
    # -----------------------------------------------------------------------
    def get_result_count(self):
        """Retourne le nombre de lignes dans le tableau."""
        rows = self.driver.find_elements(*self.RESULT_ROWS)
        return len(rows)

    def is_no_records_displayed(self):
        """True si aucun resultat affiche."""
        try:
            msgs = self.driver.find_elements(*self.NO_RECORDS_MSG)
            if any(m.is_displayed() for m in msgs):
                return True
        except Exception:
            pass
        return self.get_result_count() == 0
