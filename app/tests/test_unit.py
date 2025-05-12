import unittest
from app import application
from app.models import User

class BasicUnitTests(unittest.TestCase):

    def setUp(self):
        application.config['WTF_CSRF_ENABLED'] = False
        self.app = application.test_client()
        self.app.testing = True

    def test_user_model_fields(self):
        """Test if User model fields can be assigned and password is set properly"""
        user = User(username="citsgroup3", email="citsgroup3@uwa.com")
        user.set_password("Citsgroup3")
        self.assertEqual(user.username, "citsgroup3")
        self.assertTrue(user.check_password("Citsgroup3"))

    def test_invalid_login(self):
        """Test that login with empty username and password fails"""
        response = self.app.post('/login', data={'username': '', 'password': ''})
        self.assertIn(b'Invalid', response.data)

    def test_register_returns_page(self):
        """Test if the register page loads successfully"""
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_set_and_check_password(self):
        """Test password setting and verification logic"""
        user = User(username="citsgroup3")
        user.set_password("citsGroup3")
        self.assertTrue(user.check_password("citsGroup3"))
        self.assertFalse(user.check_password("CITSGroup3"))

    def test_upload_requires_login_redirect(self):
        """Test that unauthenticated users are redirected from upload page"""
        response = self.app.get('/upload', follow_redirects=True)
        self.assertIn(b'id="loginForm"', response.data)

if __name__ == '__main__':
    unittest.main()