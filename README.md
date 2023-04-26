# Raspi0-STM32F4Connection
Author      :   Mostafa Ahmed El-Sayed  
=========================================

The project is divided to 3 main stages, first stage is the encryption, signing and
sending the firmware to the firebase database. Second stage is download and verifying
the firmware, Finally the third stage is deploying the new firmware.
- In our security model we used:
    • Asymmetric Encryption(RSA Algorithm).
    • Authentication Digital Signature(Public-key encryption).
=========================================================


==Stage 1: Encryption, signing and sending the firmware==
=========================================================

This stage includes encrypting operations that occur to the file, after the file is en-
crypted it will be signed then it will be uploaded to the firebase.

  ![image](https://user-images.githubusercontent.com/40046072/234724598-2621103b-d5cd-4085-bca4-263c8df8332f.png)

    1-Generating Public & Private Keys
      First: " PI and PC " each one of those will Generate Public & private key
      Then upload their public keys on firebase storage.
      
    2-Encrypt Firmware using PI public key.
      This step occurs in the OEM PC using public key of raspberry pi. The in-
      put of encryption operation is the firmware(binary file) and the output will be
      encrypted firmware file.
      
      
    3-Signing the Encrypted file using PC private key
        1. Calculate HASH (SHA265 algorithm) to the encrypted firmware.
        2. Encrypt the output HASH using PC private key:
        After the hash file is generated. The PC will encrypt the HASH file using
        his private key. the output will be encrypted HASH.
        
    4-Sending the firmware:
      finally... Uploading the Encrypted firmware"Encrypted Firmware.bin" & Digi-
      tal signature Encrypted HASH "Signed Firmware.bin" to the firebase storage.
      
      
      

==Stage 2: Download and verify==
================================

    After uploading the encrypted firmware and the encrypted hash (digest) from the
    firebase, the raspberry pi will calculate the hash of the encrypted firmware (HASH1)
    and it will decrypt the encrypted hash using developer PC public key. After that,
    raspberry pi will compare 2 HASHes, if both are the same then this firmware is trusted
    and it will be decrypted using raspberry pi private key.
    
![image](https://user-images.githubusercontent.com/40046072/234725331-9b51fe1f-a1c7-410a-8546-6b17180782ba.png)

    

==Stage 3: Deploy new firmware==
================================

    Finally, after firmware decryption by raspberry pi private key. The firmware will be
    sent to the STM32F429 ECU using UART communication protocol. If the firmware
    update is for it, the STM32F429 will install it using its built-in bootloader which
    designed to receive the firmware update using UART communication protocol.
    However, if the update is for STM32F407 ECU, the firmware update will be transferd
    from STM32F429- without installing it to STM32F407 ECU using CAN communi-
    cation protocol. After that, the STM32F407 will install the new firmware using its
    own bootloader which designed to receieve the update using CAN communication
    protocol.
    
 ![image](https://user-images.githubusercontent.com/40046072/234725351-fee4328e-9147-44f6-af50-3b1f826acffe.png)

    
    
