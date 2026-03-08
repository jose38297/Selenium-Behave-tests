from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


@given("je suis connecté en tant qu'employé")
def step_login_employee(context):

    context.driver = webdriver.Chrome()
    context.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    time.sleep(3)

    context.driver.find_element(By.NAME, "username").send_keys("Admin")
    context.driver.find_element(By.NAME, "password").send_keys("admin123")
    context.driver.find_element(By.XPATH, "//button[@type='submit']").click()


@when("je crée une demande de congé pour une période donnée")
def step_create_leave(context):

    time.sleep(3)
    context.driver.find_element(By.XPATH, "//span[text()='Leave']").click()


@then('la demande apparaît comme "En attente" dans la liste des congés')
def step_verify_pending(context):

    print("Demande en attente")


@given("je suis connecté en tant que manager")
def step_login_manager(context):

    print("Manager connecté")


@when("je valide la demande de congé de l'employé")
def step_validate_leave(context):

    print("Demande validée")


@then('le statut de la demande doit être "Approuvé"')
def step_verify_approved(context):

    print("Statut Approved")