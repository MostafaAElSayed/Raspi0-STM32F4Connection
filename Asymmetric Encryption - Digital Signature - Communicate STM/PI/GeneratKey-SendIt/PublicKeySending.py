import pyrebase

# Dictionary used to connect to firebase
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

###############################################################################


storage.child("Public_Key_PI/public_key_PI.pem").put("public_key_PI.pem")
print("PI's Public Key uploaded successfully")