#defines

Firmware_Name = "BlinkGreenLed.bin"
Output_Name = 'Encrypted_Firmware.bin'
Public_Key_Name = "public_key_PI.pem"      #DON'T change it

#################################################################
#################################################################

import os
import sys
import shutil
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

#################################################################
#################################################################

if not os.path.exists("Encrypted File"):
    os.mkdir("Encrypted File")
    print("Directory " , "Encrypted File" ,  " Created ")
else:    
    print("Directory " , "Encrypted File" ,  " already exists")
    shutil.rmtree("Encrypted File")
    os.mkdir("Encrypted File")
    
# File calculations
FileSize = os.path.getsize(Firmware_Name)
print("File size is :", FileSize, "Bytes")
Counter = FileSize/128
print("Counter = ",Counter)

with open(Firmware_Name,"rb") as source_coed:
 while(Counter >= 0):
    if(Counter < 1):
        message = source_coed.read()
    else:
        message = source_coed.read(128)
        
    print("size of packet = ",sys.getsizeof(message))
    with open(Public_Key_Name, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    pos = "Encrypted File/%s" %(Output_Name)
    
    with open(pos,"ab") as f:
        f.write(encrypted)
        
    print(os.path.getsize(pos))
    print(Counter)
    Counter = Counter-1
    
