# =============================================================================
# PAGE OBJECT : LoginPage
# =============================================================================
# Gere toutes les interactions avec la page de connexion OrangeHRM
# URL : https://opensource-demo.orangehrmlive.com/web/index.php/auth/login
#
# HTML confirme :
#   Username : <input name="username">
#   Password : <input name="password">
#   Bouton   : <button type="submit">
#   Erreur   : <div class="oxd-alert-content"> ou <p class="oxd-text--p">
# =============================================================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

BASE_URL = "https://opensource-demo.orangehrmlive.com"
LOGIN_URL = BASE_URL + "/web/index.php/auth/login"
DASHBOARD_URL = "/dashboard"


class LoginPage:

    # -----------------------------------------------------------------------
    # LOCATORS
    # -----------------------------------------------------------------------

    # Champ Username - HTML : <input name="username">
    USERNAME_INPUT = (By.NAME, "username")

    # Champ Password - HTML : <input name="password">
    PASSWORD_INPUT = (By.NAME, "password")

    # Bouton Login - HTML : <button type="submit">
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Message d erreur connexion invalide
    # HTML : <div class="oxd-alert-content-text">
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    # Messages de validation champs obligatoires
    # HTML : <span class="oxd-text oxd-input-field-error-message">
    VALIDATION_MESSAGES = (By.CSS_SELECTOR, ".oxd-input-field-error-message")

    # Menu utilisateur (avatar en haut a droite)
    # HTML : <span class="oxd-userdropdown-tab">
    USER_DROPDOWN = (By.CSS_SELECTOR, ".oxd-userdropdown-tab")

    # Lien Logout dans le menu
    LOGOUT_LINK = (By.XPATH, "//a[normalize-space(text())='Logout']")

    # Element confirme qu on est sur le Dashboard
    # HTML : <h6 class="oxd-text oxd-text--h6">Dashboard</h6>
    DASHBOARD_TITLE = (By.XPATH,
        "//h6[contains(@class,'oxd-text--h6') and text()='Dashboard']")

    # Menu de navigation lateral
    NAV_MENU = (By.CSS_SELECTOR, ".oxd-sidepanel-body")


    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)


    # -----------------------------------------------------------------------
    # ACTIONS
    # -----------------------------------------------------------------------

    def open(self):
        """Navigue vers la page de connexion et attend qu elle soit chargee."""
        self.driver.get(LOGIN_URL)
        self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )

    def saisir_username(self, username):
        """Saisit le nom d utilisateur."""
        field = self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        field.clear()
        field.send_keys(username)

    def saisir_password(self, password):
        """Saisit le mot de passe."""
        field = self.driver.find_element(*self.PASSWORD_INPUT)
        field.clear()
        field.send_keys(password)

    def cliquer_login(self):
        """Clique sur le bouton de connexion."""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
        time.sleep(2)

    def login(self, username, password):
        """
        Connexion complete : ouvre la page, saisit les identifiants, valide.
        Utilise dans le Background des autres features.
        """
        self.open()
        self.saisir_username(username)
        self.saisir_password(password)
        self.cliquer_login()
        # Attend la redirection vers le dashboard
        self.wait.until(EC.url_contains("dashboard"))

    def cliquer_menu_utilisateur(self):
        """Clique sur l avatar utilisateur pour ouvrir le menu."""
        menu = self.wait.until(
            EC.element_to_be_clickable(self.USER_DROPDOWN)
        )
        menu.click()
        time.sleep(0.5)

    def cliquer_logout(self):
        """Clique sur Logout dans le menu utilisateur."""
        logout = self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        )
        logout.click()
        time.sleep(2)


    # -----------------------------------------------------------------------
    # VERIFICATIONS
    # -----------------------------------------------------------------------

    def est_sur_dashboard(self):
        """True si l URL contient dashboard."""
        return "dashboard" in self.driver.current_url

    def est_sur_page_connexion(self):
        """True si l URL contient auth/login."""
        return "auth/login" in self.driver.current_url

    def get_message_erreur(self):
        """Retourne le texte du message d erreur de connexion."""
        try:
            msg = self.wait.until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return msg.text.strip()
        except TimeoutException:
            return ""

    def get_messages_validation(self):
        """Retourne la liste des messages de validation (champs obligatoires)."""
        try:
            msgs = self.wait.until(
                EC.presence_of_all_elements_located(self.VALIDATION_MESSAGES)
            )
            return [m.text.strip() for m in msgs if m.text.strip()]
        except TimeoutException:
            return []

    def est_menu_navigation_visible(self):
        """True si le menu lateral est visible (= utilisateur connecte)."""
        try:
            menu = self.driver.find_element(*self.NAV_MENU)
            return menu.is_displayed()
        except Exception:
            return False
