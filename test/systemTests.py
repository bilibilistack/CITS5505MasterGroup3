import unittest
import multiprocessing
import time
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import db, create_app
from app.config import TestingConfig

BASE_URL = "http://127.0.0.1:5000"

def run_server():
    app = create_app(config=TestingConfig)
    with app.app_context():
        db.create_all()
    app.run(use_reloader=False)

class SystemTests(unittest.TestCase):
    def setUp(self):
        self.app_context = create_app(config=TestingConfig).app_context()
        self.app_context.push()
        db.create_all()

        # Start Flask server in a separate process using a top-level function
        self.server_process = multiprocessing.Process(target=run_server)
        self.server_process.start()
        time.sleep(1)  # Give server time to start

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.server_process.terminate()
        self.driver.quit()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_with_invalid_credentials(self):
        driver = self.driver
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.ID, "username").send_keys("wronguser")
        driver.find_element(By.ID, "password").send_keys("wrongpassword")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginForm")))
        self.assertIn("login", driver.current_url.lower())

    def test_register_page_loads_properly(self):
        driver = self.driver
        driver.get(f"{BASE_URL}/register")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "registerForm")))
        self.assertIn("register", driver.current_url.lower())
        self.assertIn("registerForm", driver.page_source)

    def test_login_and_redirect_to_home(self):
        driver = self.driver
        username, password = self.perform_registration(driver)
        self.perform_login(driver, username, password)
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))
        self.assertNotIn("login", driver.current_url.lower())

    def test_access_upload_page_after_login(self):
        driver = self.driver
        username, password = self.perform_registration(driver)
        self.perform_login(driver, username, password)

        driver.get(f"{BASE_URL}/upload")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "file-input")))
        self.assertIn("upload", driver.current_url.lower())
        self.assertTrue(driver.find_element(By.ID, "file-input"))

    def test_access_share_page_after_login(self):
        driver = self.driver
        username, password = self.perform_registration(driver)
        self.perform_login(driver, username, password)

        driver.get(f"{BASE_URL}/share")
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "share-btn")))
        self.assertIn("share", driver.current_url.lower())
        self.assertTrue(driver.find_element(By.ID, "share-btn"))

    def perform_registration(self, driver, username=None, password="123123", email=None):
        if username is None:
            username = f"testuser_{uuid.uuid4().hex[:8]}"
        if email is None:
            email = f"{username}@example.com"
        driver.get(f"{BASE_URL}/register")
        driver.find_element(By.ID, "newUsername").send_keys(username)
        driver.find_element(By.ID, "email").send_keys(email)
        driver.find_element(By.ID, "newPassword").send_keys(password)
        driver.find_element(By.ID, "confirmPassword").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except Exception:
            pass
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginForm")))
        return username, password

    def perform_login(self, driver, username, password):
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        WebDriverWait(driver, 5).until(EC.url_changes(driver.current_url))

if __name__ == "__main__":
    unittest.main()