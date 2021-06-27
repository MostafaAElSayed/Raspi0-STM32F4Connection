import index
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

##################################################################
##################################################################

Encrypted_Firmware_Name = index.FirmwareName

i = 0
# File calculations
FileSize = os.path.getsize(Encrypted_Firmware_Name)
print("File size is :", FileSize, "Bytes")
Counter = FileSize/256
print("Counter = ",Counter)


with open(Encrypted_Firmware_Name,"rb") as f:
        encrypted = f.read()
        
with open("Firmware Before Decryption.bin","wb") as file:
        file.write(encrypted)
        
with open("Firmware Before Decryption.bin","rb") as f:
    while(Counter >= 1):
        print("Seek = ",f.tell())
        encrypted = f.read(256)
            
            
        with open("private_key_PI.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        original_message = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        if(i == 0):
            with open(Encrypted_Firmware_Name,"wb") as file:
                file.write(original_message)
        
        else:
            with open(Encrypted_Firmware_Name,"ab") as file:
                file.write(original_message)
        
        Counter = Counter-1
        i = i + 1    
