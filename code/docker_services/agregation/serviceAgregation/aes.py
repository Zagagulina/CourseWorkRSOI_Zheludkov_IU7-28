import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher:
    def __init__( self, key ):
        self.BS = 32
        self.key = key

    def _pad(self, s):
        return s + (self.BS - len(s) % self.BS) * chr(self.BS - len(s) % self.BS)

    def encrypt( self, raw ):
        raw = self._pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return self._unpad(cipher.decrypt( enc[16:] ))

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]