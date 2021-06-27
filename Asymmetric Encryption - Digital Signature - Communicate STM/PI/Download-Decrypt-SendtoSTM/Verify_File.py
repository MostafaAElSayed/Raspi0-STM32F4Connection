import index
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
####################################################################

Encrypted_Firmware_Name = index.FirmwareName

i = 0
# File calculations
FileSize = os.path.getsize("Signed_Firmware.bin")
print("File size is :", FileSize, "Bytes")
Counter = FileSize/256
print("Counter = ",Counter)


with open("Signed_Firmware.bin","rb") as Signed:
    with open(Encrypted_Firmware_Name,"rb") as f:
        while(Counter >= 1):
            print("Seek = ",f.tell())
            messsage = f.read(128)
            sign = Signed.read(256)
                
            with open("public_key_PC.pem", "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

            verify_value = public_key.verify(
                sign,
                messsage,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
                )
                
            print("verify_value(None) = ",verify_value)
            Counter = Counter-1
            i = i + 1
print("Firmware is TRUSTED")            
