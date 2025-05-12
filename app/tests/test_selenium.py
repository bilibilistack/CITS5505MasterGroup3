from app import application
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

# Define the base URL of the Flask app
BASE_URL = "http://127.0.0.1:5000"

class SeleniumTests(unittest.TestCase):

    def setUp(self):
        application.config['WTF_CSRF_ENABLED'] = False
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)

    def tearDown(self):
        self.driver.quit()

    def test_login_with_invalid_credentials(self):
        """Verify that login fails with invalid credentials"""
        driver = self.driver
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "username").send_keys("wronguser")
        driver.find_element(By.ID, "password").send_keys("wrongpassword")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        time.sleep(2)
        self.assertIn("login", driver.current_url.lower())

    def test_register_page_loads_properly(self):
        """Verify that the registration page loads correctly"""
        driver = self.driver
        driver.get(f"{BASE_URL}/register")
        time.sleep(2)
        self.assertIn("register", driver.current_url.lower())
        self.assertIn("registerForm", driver.page_source)

    def test_login_and_redirect_to_home(self):
        """Verify successful login and redirection to home page"""
        driver = self.driver
        driver.get(f"{BASE_URL}/login")

        driver.find_element(By.ID, "username").send_keys("cj1")
        driver.find_element(By.ID, "password").send_keys("123123")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        time.sleep(5)
        self.assertNotIn("login", driver.current_url.lower())

    def test_access_upload_page_after_login(self):
        """Verify that upload page is accessible after login and file input is present"""
        driver = self.driver
        self.perform_login(driver)

        driver.get(f"{BASE_URL}/upload")
        time.sleep(2)
        self.assertIn("upload", driver.current_url.lower())
        self.assertTrue(driver.find_element(By.ID, "file-input"))

    def test_access_share_page_after_login(self):
        """Verify that share page is accessible after login and share button is present"""
        driver = self.driver
        self.perform_login(driver)

        driver.get(f"{BASE_URL}/share")
        time.sleep(2)
        self.assertIn("share", driver.current_url.lower())
        self.assertTrue(driver.find_element(By.ID, "share-btn"))

    def perform_login(self, driver):
        """Reusable login procedure"""
        driver.get(f"{BASE_URL}/login")
        driver.find_element(By.ID, "username").send_keys("cj1")
        driver.find_element(By.ID, "password").send_keys("123123")
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
        time.sleep(5)

if __name__ == "__main__":
    unittest.main()