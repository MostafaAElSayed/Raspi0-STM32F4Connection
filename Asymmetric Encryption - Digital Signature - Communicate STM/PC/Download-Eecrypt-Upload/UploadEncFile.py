import pyrebase


config = {
  "apiKey": "AIzaSyCgIC9fUEy4pB0OM58kJ0xIAITMBVwCG3Y",
  "authDomain": "fota-pizero.firebaseapp.com",
  "databaseURL": "https://fota-pizero-default-rtdb.firebaseio.com/",
  "storageBucket": "fota-pizero.appspot.com"
}
# Connect to firebase
firebase = pyrebase.initialize_app(config)
print("Firebase Connected")

# Connect to data base of firebase (Where the firmware is saved)
storage = firebase.storage()

storage.child("Encrypted_Firmware.bin").put("Encrypted File/Encrypted_Firmware.bin")
print("Encrypted Firmware Uploaded")

storage.child("Signed_Firmware.bin").put("Signed File/Signed_Firmware.bin")
print("Signed Firmware Uploaded")