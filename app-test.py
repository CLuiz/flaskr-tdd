import unittest
import os
import tempfile
import app


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """Initial test. Ensure flask was correctly set up."""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        """Initial test. Ensure database exists."""
        tester = os.path.exists('flaskr.db')
        self.assertTrue(tester)


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        """Set up blank temp db before each test."""
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        """Destroy blank temp database after each test"""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        """Login helper function"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        """Logout helper function"""
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        """Ensure databaase is blank"""
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data

    def test_login(self):
        """Test login and logout using helper functions"""
        rv = self.login(
            app.app.config['USERNAME'],
            app.app.config['PASSWORD']
        )
        assert b'You were logged in' in rv.data
        rv = self.logout()
        
    def
if __name__ == '__main__':
    unittest.main()
