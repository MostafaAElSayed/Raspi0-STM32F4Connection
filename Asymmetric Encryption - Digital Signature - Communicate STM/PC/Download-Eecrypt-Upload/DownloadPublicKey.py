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

# Downlaod Firmware Binary File Command
storage.child("Public_Key_PI/public_key_PI.pem").download("public_key_PI.pem")