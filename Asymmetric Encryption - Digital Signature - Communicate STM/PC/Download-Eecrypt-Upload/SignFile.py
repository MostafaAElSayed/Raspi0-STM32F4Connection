#defines
Firmware_Name = "Encrypted File/Encrypted_Firmware.bin"
Output_Name = 'Signed_Firmware.bin'
Private_Key_Name = "private_key_PC.pem"      #DON'T change it

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

if not os.path.exists("Signed File"):
    os.mkdir("Signed File")
    print("Directory " , "Signed File" ,  " Created ")
else:    
    print("Directory " , "Signed File" ,  " already exists")
    shutil.rmtree("Signed File")
    os.mkdir("Signed File")
    
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
    with open("private_key_PC.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
            )

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    pos = "Signed File/%s" %(Output_Name)
    
    with open(pos,"ab") as f:
        f.write(signature)
        
    print(os.path.getsize(pos))
    print(Counter)
    Counter = Counter-1
    
