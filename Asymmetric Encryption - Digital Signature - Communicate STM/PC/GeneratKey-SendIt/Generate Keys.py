# Mostafa Ahmed Mohamed
# V1

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
print("private_key =",private_key)


pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open('private_key_PC.pem', 'wb') as f:
    f.write(pem)

with open('../Download-Eecrypt-Upload/private_key_PC.pem','wb') as f:
    f.write(pem)
    
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('public_key_PC.pem', 'wb') as f:
    f.write(pem)
