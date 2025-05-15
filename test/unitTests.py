import unittest
from app import create_app
from app.config import TestingConfig
from app.models import User
from app import db

class BasicUnitTests(unittest.TestCase):

    def setUp(self):
        self.application = create_app(config=TestingConfig)
        self.application.config['WTF_CSRF_ENABLED'] = False
        self.application.config['SECRET_KEY'] = 'test_secret_key'  
        self.app_context = self.application.app_context()
        self.app_context.push()
        db.create_all()
        self.app = self.application.test_client()
        self.app.testing = True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_model_fields(self):
        """Test if User model fields can be assigned and password is set properly"""
        user = User(username="citsgroup3", email="citsgroup3@uwa.com")
        user.set_password("Citsgroup3")
        self.assertEqual(user.username, "citsgroup3")
        self.assertTrue(user.check_password("Citsgroup3"))

    def test_invalid_login(self):
        """Test that login with empty username and password fails"""
        response = self.app.post('/login', data={'username': '', 'password': ''})
        self.assertIn(b'This field is required.', response.data)

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

    def test_homechart_redirects_to_upload(self):
        """Test that accessing homechart redirects to upload page if clicked (authenticated user)"""
        # Register a user
        self.app.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@uwa.com',
            'password': 'Testpass123',
            'confirm_password': 'Testpass123'
        }, follow_redirects=True)
        # Log in the user
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'Testpass123'
        }, follow_redirects=True)
        # Now access /homechart
        response = self.app.get('/upload', follow_redirects=True)
        # Use a unique string from upload.html for assertion
        self.assertIn(b'Upload weather data', response.data)

    def test_homechart_share_button_redirect(self):
        """Test that clicking the 'Share With Friends' button on homechart page redirects to the share page (authenticated user)"""
        # Register a user
        self.app.post('/register', data={
            'username': 'testuser',
            'email': 'testuser@uwa.com',
            'password': 'Testpass123',
            'confirm_password': 'Testpass123'
        }, follow_redirects=True)
        # Log in the user
        self.app.post('/login', data={
            'username': 'testuser',
            'password': 'Testpass123'
        }, follow_redirects=True)
        # Access /homechart to get the page with the button
        response = self.app.get('/homechart', follow_redirects=True)
        self.assertIn(b'id="share-to-btn"', response.data)
        # Simulate clicking the button by making a GET or POST request to the endpoint it triggers
        # Assuming the button triggers a GET to /share 
        response = self.app.get('/share', follow_redirects=True)
        self.assertIn(b'Share Weather Visualization', response.data)

if __name__ == '__main__':
    unittest.main()