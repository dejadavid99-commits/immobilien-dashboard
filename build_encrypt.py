import json
import os
import base64

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITERATIONS = 250000

password = os.environ["APP_PASSWORD"].encode("utf-8")

with open("data.source.json", "r", encoding="utf-8") as f:
    plaintext = f.read().encode("utf-8")

salt = os.urandom(16)
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITERATIONS)
key = kdf.derive(password)

aesgcm = AESGCM(key)
iv = os.urandom(12)
ciphertext = aesgcm.encrypt(iv, plaintext, None)

bundle = {
    "salt": base64.b64encode(salt).decode("ascii"),
    "iv": base64.b64encode(iv).decode("ascii"),
    "ciphertext": base64.b64encode(ciphertext).decode("ascii"),
    "iterations": ITERATIONS,
}

with open("encrypted_data.json", "w", encoding="utf-8") as f:
    json.dump(bundle, f)

print("encrypted_data.json geschrieben.")
