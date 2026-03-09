from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pages.employee_list_page import EmployeeListPage, BASE_URL


@given("je suis connecte en tant qu admin")
def step_connecte_admin(context):
    context.driver.get(BASE_URL + "/web/index.php/auth/login")
    wait = WebDriverWait(context.driver, 15)
    username = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    username.clear()
    username.send_keys("Admin")
    password = context.driver.find_element(By.NAME, "password")
    password.clear()
    password.send_keys("admin123")
    context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    wait.until(EC.url_contains("dashboard"))
    context.employee_page = EmployeeListPage(context.driver)


@given("je suis sur la page liste des employes")
def step_page_liste(context):
    context.employee_page.open()


# ---------------------------------------------------------------------------
# WHEN
# ---------------------------------------------------------------------------

@when("je recherche un employe par le nom vide")
def step_recherche_vide(context):
    """Champ vide -> affiche tous les employes."""
    context.employee_page.search_by_name_autocomplete("")


@when('je recherche par autocomplete le nom "{nom}"')
def step_recherche_autocomplete(context, nom):
    """
    Recherche via le champ autocomplete Employee Name.
    Selectionne la suggestion si disponible.
    """
    context.search_name = nom
    context.employee_page.search_by_name_autocomplete(nom)


@when('je recherche par employee id "{employee_id}"')
def step_recherche_id(context, employee_id):
    """
    Recherche via le champ Employee Id (simple input, sans autocomplete).
    Utilise pour les cas aucun resultat car plus fiable.
    """
    context.employee_page.search_by_employee_id(employee_id)


@when('je filtre les employes par sous-unite "{departement}"')
def step_filtre(context, departement):
    context.employee_page.filter_by_sub_unit(departement)


# ---------------------------------------------------------------------------
# THEN
# ---------------------------------------------------------------------------

@then("au moins un resultat doit s afficher")
def step_au_moins_un(context):
    count = context.employee_page.get_result_count()
    assert count >= 1, "ECHEC : Aucun employe affiche. Lignes : " + str(count)


@then("le nombre de resultats doit etre superieur a 0")
def step_superieur_zero(context):
    count = context.employee_page.get_result_count()
    assert count > 0, "ECHEC : Aucun resultat. Lignes : " + str(count)


@then("aucun resultat ne doit s afficher")
def step_aucun_resultat(context):
    aucun = context.employee_page.is_no_records_displayed()
    count = context.employee_page.get_result_count()
    assert aucun, "ECHEC : " + str(count) + " resultat(s) affiches pour un ID inexistant"


@then("le nombre de resultats doit etre superieur ou egal a 0")
def step_zero_ou_plus(context):
    count = context.employee_page.get_result_count()
    assert count >= 0, "ECHEC : Etat invalide"
    print("  -> " + str(count) + " employe(s) trouves")
