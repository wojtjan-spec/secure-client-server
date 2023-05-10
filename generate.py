# Imported from cryptography library
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

KEY_SIZE = 2048
PUBLIC_EXP = 65537

# Create private server key
private_key = rsa.generate_private_key(
    public_exponent=PUBLIC_EXP,
    key_size=KEY_SIZE,
    backend=default_backend()
)

# Save private server key
with open("private.txt", "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# Create public client key
public_key = private_key.public_key()

# Save public client key
with open("public.txt", "wb") as f:
    f.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )