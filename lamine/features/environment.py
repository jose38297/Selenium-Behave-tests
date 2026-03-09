# =============================================================================
# ENVIRONMENT.PY - Configuration Behave
# =============================================================================
# Ce fichier est automatiquement lu par Behave.
# Il contient les "hooks" : fonctions appelees avant/apres les tests.
#
# HOOKS disponibles :
#   before_all     -> avant TOUS les tests
#   before_feature -> avant chaque fichier .feature
#   before_scenario-> avant chaque Scenario
#   after_scenario -> apres chaque Scenario
#   after_all      -> apres TOUS les tests
# =============================================================================

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def before_scenario(context, scenario):
    """
    Avant CHAQUE scenario : cree un nouveau navigateur Chrome.

    Pourquoi avant chaque scenario et pas avant tous ?
    -> Chaque test doit partir d un etat propre (pas de cookies, pas de cache)
    -> Les tests sont ainsi independants les uns des autres
    """
    # Configuration Chrome
    options = Options()
    options.add_argument("--headless")           # sans interface graphique
    options.add_argument("--no-sandbox")          # requis sur Linux/CI
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Lance Chrome avec le bon driver (telecharge automatiquement)
    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)

    # Attente implicite : Selenium attend jusqu a 10s avant echec
    context.driver.implicitly_wait(10)


def after_scenario(context, scenario):
    """
    Apres CHAQUE scenario : ferme le navigateur.
    Meme si le test a echoue, le driver est bien ferme (pas de fuites).
    """
    if hasattr(context, "driver"):
        context.driver.quit()
