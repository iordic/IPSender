import os


class Obfuscator:
    def __init__(self, password, key=None):
        self.password = bytearray(password)
        if key is None:
            keysize = len(self.password)
            self.key = self.generate_key(keysize)
        else:
            self.key = bytearray(key)
        # Obtain ciphered password
        self.cpassword = self.mix_keys(self.password, self.key)

    def generate_key(self, size):
        """ Generate key using random bytes with specified size. """
        key = bytearray()
        for i in range(0,size):
            random_byte = ord(os.urandom(1))
            key.append(random_byte)
        return key

    def mix_keys(self, password, key):
        """ 'Encrypt' the password with the key. Reverse key bytes and
            XOR with password bytes. Very low security but a bit obfuscated. """
        rev_key = list(reversed(key))   # Reverse bytes
        result = bytearray()
        for i in range(0, len(password)):
            xored = password[i] ^ rev_key[i]    # Mix each byte
            result.append(xored)
        return result
