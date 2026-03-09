# =============================================================================
# STEP DEFINITIONS : Authentification
# =============================================================================
# Traduit chaque ligne Gherkin en action Python/Selenium
#
# Structure :
#   @given  -> etat initial (contexte de depart)
#   @when   -> action effectuee par l utilisateur
#   @then   -> verification du resultat attendu
# =============================================================================

from behave import given, when, then

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pages.login_page import LoginPage


# ---------------------------------------------------------------------------
# GIVEN - Etat initial
# ---------------------------------------------------------------------------

@given("je suis sur la page de connexion")
def step_page_connexion(context):
    """
    Ouvre le navigateur sur la page de connexion OrangeHRM.
    Le navigateur est deja lance par environment.py (before_scenario).
    """
    context.login_page = LoginPage(context.driver)
    context.login_page.open()


@given("je suis connecte en tant qu Admin")
def step_connecte_admin(context):
    """
    Effectue une connexion complete avant le test.
    Utilise par le scenario de deconnexion.
    """
    context.login_page = LoginPage(context.driver)
    context.login_page.login("Admin", "admin123")


# ---------------------------------------------------------------------------
# WHEN - Actions utilisateur
# ---------------------------------------------------------------------------

@when('je saisis le nom d utilisateur "{username}"')
def step_saisir_username(context, username):
    """Saisit le nom d utilisateur dans le champ correspondant."""
    context.login_page.saisir_username(username)


@when('je saisis le mot de passe "{password}"')
def step_saisir_password(context, password):
    """Saisit le mot de passe dans le champ correspondant."""
    context.login_page.saisir_password(password)


@when("je clique sur le bouton de connexion")
def step_cliquer_login(context):
    """Clique sur le bouton Login pour soumettre le formulaire."""
    context.login_page.cliquer_login()


@when("je clique sur le menu utilisateur")
def step_menu_utilisateur(context):
    """Clique sur l avatar/nom utilisateur en haut a droite."""
    context.login_page.cliquer_menu_utilisateur()


@when("je clique sur Logout")
def step_logout(context):
    """Clique sur le lien Logout dans le menu deroulant."""
    context.login_page.cliquer_logout()


# ---------------------------------------------------------------------------
# THEN - Verifications
# ---------------------------------------------------------------------------

@then("je dois etre redirige vers le tableau de bord")
def step_verif_dashboard(context):
    """
    Verifie que l URL contient 'dashboard'.
    = Connexion reussie et redirection effectuee.
    """
    est_dashboard = context.login_page.est_sur_dashboard()
    url_actuelle = context.driver.current_url
    assert est_dashboard, (
        "ECHEC : Pas sur le dashboard apres connexion. "
        "URL actuelle : " + url_actuelle
    )


@then("je dois voir le menu de navigation")
def step_verif_menu(context):
    """
    Verifie que le menu lateral est visible.
    = L utilisateur est bien connecte et a acces a l application.
    """
    menu_visible = context.login_page.est_menu_navigation_visible()
    assert menu_visible, "ECHEC : Menu de navigation non visible apres connexion"


@then("je dois voir un message d erreur de connexion")
def step_verif_erreur(context):
    """
    Verifie qu un message d erreur est affiche.
    OrangeHRM affiche 'Invalid credentials' pour un mauvais mot de passe.
    """
    message = context.login_page.get_message_erreur()
    assert message != "", (
        "ECHEC : Aucun message d erreur affiche pour des identifiants incorrects"
    )
    print("  -> Message d erreur affiche : [" + message + "]")


@then("je dois rester sur la page de connexion")
def step_verif_reste_connexion(context):
    """
    Verifie que l utilisateur n a pas ete redirige apres echec de connexion.
    """
    est_login = context.login_page.est_sur_page_connexion()
    url_actuelle = context.driver.current_url
    assert est_login, (
        "ECHEC : L utilisateur a ete redirige malgre des identifiants incorrects. "
        "URL : " + url_actuelle
    )


@then("je dois voir des messages de validation obligatoires")
def step_verif_validation(context):
    """
    Verifie que des messages 'Required' apparaissent quand les champs sont vides.
    OrangeHRM affiche 'Required' sous chaque champ obligatoire non rempli.
    """
    messages = context.login_page.get_messages_validation()
    assert len(messages) > 0, (
        "ECHEC : Aucun message de validation affiche pour des champs vides"
    )
    print("  -> Messages de validation : " + str(messages))


@then("je dois etre redirige vers la page de connexion")
def step_verif_retour_login(context):
    """
    Verifie que la deconnexion redirige bien vers la page de connexion.
    """
    est_login = context.login_page.est_sur_page_connexion()
    url_actuelle = context.driver.current_url
    assert est_login, (
        "ECHEC : Apres deconnexion, redirection incorrecte. "
        "URL : " + url_actuelle
    )
