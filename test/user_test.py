import unittest

from app.models import User

class UserTest(unittest.TestCase):
    """
    Test class to test the user
    """
    def setUp(self):
        self.new_user = User(username='peter',password='peter1010')

    def test_password_setter(self):
        self.assertTrue(self.new_user.password is not None)

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.check_password('peter1010'))


if __name__ == '__main__':
    unittest.main()
