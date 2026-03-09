# test_simple.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 40)

print("Ouverture du site...")
driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

print(f"URL actuelle : {driver.current_url}")
print(f"Titre de la page : {driver.title}")

try:
    field = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    print("✅ Champ username trouvé !")
    field.send_keys("Admin")
    
    driver.find_element(By.NAME, "password").send_keys("admin123")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    
    wait.until(EC.url_contains("dashboard"))
    print("✅ Connecté ! URL dashboard :", driver.current_url)

except Exception as e:
    print(f"❌ Erreur : {e}")
    print(f"URL au moment de l'erreur : {driver.current_url}")
    driver.save_screenshot("debug_login.png")
    print("Screenshot sauvegardé : debug_login.png")

input("Appuyez sur Entrée pour fermer le navigateur...")
driver.quit()