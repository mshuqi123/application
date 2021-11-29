import json
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.number import ceil_div, bytes_to_long, long_to_bytes
import Crypto.Util.number
from Crypto import Random
from Crypto.PublicKey import RSA
from utils import setting
private_path = setting.conf + '/rsa-private.pem'
pubkey_path = setting.conf + '/rsa-public.pem'


class PKCS115Cipher(PKCS1_v1_5.PKCS115_Cipher):

    def decrypt(self, ciphertext="", sentinel=""):
        # See 7.2.1 in RFC3447
        modBits = Crypto.Util.number.size(self._key.n)
        k = ceil_div(modBits, 8)  # Convert from bits to bytes
        # Step 1
        if len(ciphertext) > k:
            raise ValueError("Ciphertext with incorrect length.")
        # Step 2a (O2SIP)
        ct_int = bytes_to_long(ciphertext)
        # Step 2b (RSADP)
        m_int = self._key._decrypt(ct_int)
        # Complete step 2c (I2OSP)
        em = long_to_bytes(m_int, k)
        # Step 3
        sep = em.find(b'\x00', 2)
        if not em.startswith(b'\x00\x02') or sep < 10:
            return sentinel
        # Step 4
        return em[sep + 1:]


def new(key, randfunc=None):
    if randfunc is None:
        randfunc = Random.get_random_bytes
    return PKCS115Cipher(key, randfunc)


class RSATool(object):
    def __init__(self, private, pubkey):
        with open(private) as f:
            self.private_key = f.read()
        with open(pubkey) as f:
            self.pubkey_str = f.read()
        self.rsakey = RSA.importKey(self.private_key)
        self.default_length = 128
        self.cipher = new(self.rsakey)
        self.default_value = b"verify_error"

    def rsa_decrypt(self, data=None):
        """
        解密
        :param data:
        :return:
        """
        decrypt_byte = b""
        if "," in data:
            for i in data.split(","):
                decrypt_byte += self.cipher.decrypt(base64.b64decode(i), self.default_value)
        else:
            decrypt_byte = self.cipher.decrypt(base64.b64decode(data), self.default_value)

        decrypted = decrypt_byte.decode()
        if "verify_error" in decrypted:
            return None
        return json.loads(decrypted)

    def rsa_encrypt(self, data):
        """
        加密
        :param msg:
        :param pubkey:
        :return:
        """
        msg = json.dumps(data).encode(encoding="utf-8")
        length = len(msg)
        default_length = 117
        # 公钥加密
        pubobj = new(RSA.importKey(self.pubkey_str))
        # 长度不用分段
        if length < default_length:
            return base64.b64encode(pubobj.encrypt(msg))
        # 需要分段
        offset, res = 0, []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(base64.b64encode(pubobj.encrypt(msg[offset:offset + default_length])).decode("utf-8"))
            else:
                res.append(base64.b64encode(pubobj.encrypt(msg[offset:])).decode("utf-8"))
            offset += default_length
        return ",".join(res)

    def base64_encrypt(self, data):
        """base64 加密"""
        return base64.b64encode(json.dumps(data).encode("utf-8")).decode("utf-8")

    def base64_decrypt(self, data):
        """base64 解密"""
        return base64.b64decode(data).decode("utf-8")

if __name__ == '__main__':
    a = RSATool(private_path, pubkey_path)
    data = '+ALR6SjWD65mqlCbHzgsy8/a5vvFZc2pnZSbWoCnS7A='
    b = a.rsa_decrypt(data)
    print(b)