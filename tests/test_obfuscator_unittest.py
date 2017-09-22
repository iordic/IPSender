import unittest
from tools.Obfuscator import Obfuscator


class TestObfuscator(unittest.TestCase):

    def setUp(self):
        pass

    def test_mix_keys(self):
        """ Check the password encryption and decryption. """
        # Password encryption
        first = Obfuscator('1234')
        first_key = first.key
        first_cpassword = first.cpassword
        # Password decryption
        second = Obfuscator(first_cpassword, first_key)
        # Decrypted password should be same as first password
        expected = first.password
        actual = second.cpassword
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
