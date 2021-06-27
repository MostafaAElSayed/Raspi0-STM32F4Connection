#################################################################################
#							Raspberry Pi Example with F429						#
#################################################################################

#################################################################################
# 									Includes Required 							#
#################################################################################
import RPi.GPIO as GPIO
import os
import pyrebase
import serial
from time import sleep

#################################################################################
#				Variables definitions instead of #defines and enums in c		#
#################################################################################

# Variables used as FSM Identification (Intstead of Enum in C code)
PI_IDLE_STATE = 0
PI_DOWNLOAD_FILE_STATE = 1
PI_SEND_UPDATE_REQUEST_STATE = 2
PI_WAIT_STM_RESPONSE_STATE = 3
PI_SEND_UPDATE_INFO_STATE = 4
PI_SEND_FILE_SIZE = 5
PI_SEND_PACKET_STATE = 6
PI_RETRANSMIT_PACKET_STATE = 7
PI_END_STATE = 8


# Defienes used as ACKs
PI_READY = 0x21  # ASCII of '!'
PI_NEW_UPDATE_AVAILABLE = 0x2F  # ASCII of '/'

# Bootloader Command Codes
BOOTLOADER_UPDATE_INFO_CODE = 0x41  # ASCII of A
BOOTLOADER_SEND_PACKET_CODE = 0x42  # ASCII of B
BOOTLOADER_SEND_SUBPACKET_CODE = 0x43  # ASCII of C

# Bootloader Command Sizes
BOOTLOADER_UPDATE_INFO_SIZE = 5
BOOTLOADER_SEND_PACKET_SIZE = 1

# Macros for STM to PI ACks
STM_FINISHED_INITIATION = 0x30  # ASCII of 0 */
STM_READY_TO_GET_INFO = 0x31  # ASCII of 1 */
STM_READY_TO_RECEIVE_UPDATE_PACEKTS = 0x32  # ASCII of 2 */
STM_READY_TO_RECEIVE_PACKET = 0x33  # ASCII of 3 */
STM_READY_TO_RECEIVE_SUBPACEKT = 0x34  # ASCII of 4 */
STM_END_STATUS = 0x35  # ASCII of 5 */

# Received messages IDs
DISCARD_UPDATE = 0x01
READY_FOR_UPDATE = 0x02
READY_TO_RECEIVE_NEXT_PACKET = 0x03
RETRANSMIT_LAST_PACKET = 0x04

# Devices IDs
STM32F429_ID = 0x50
STM32F407_ID = 0x60

# Packet size in bytes
PACKET_SIZE = 1024
FIRST_PACKET_SIZE = 4

#################################################################################
#					  Variables definitions used inside the code				#
#################################################################################

# Variable to check if there is a new update found
NewUpdate = "False"

###########################
#  Variable to get Kit ID #
#  0x50 -> F429			  #
#  0x60 -> F407			  #
###########################
UpdateId = ""

# Variable to hold Firmware name from FireBase
# (Instead of FirmwareURL Variable in C code)
FirmwareName = "";

# Variable to save website Fingerprint
# FingerPrint = "";


# List to save File size
AppSizeArr = []

# Variable used as a counter
counter = 0;

# Variable to read ACKs */
Rec_Msg = 0;

# Variable to count Packets */
PacketNum = 0;

# Used to save Extra_Bytes(SubPackets */
Extra_Bytes = 0
# Variable to receive the code byte by byte */
ByteBuffer = 0

# Variabel to count file size on it */
FileSize = 0

# Variable to know how many packets of the code will be sent */
NumOfPackets = 0

# Variables to calculate file size */
led = 2
thousands = 0
hundreds = 0
tens = 0
c = 0
# Indicator of first pacekt */
FirstPacket = 1

ReadOnce = 0
# Variable used in FSM of Switch case */
PI_State = PI_IDLE_STATE;
#################################################################################
    # ****************************************************************************/
    # *    Function Name           : Download_Firmware                           */
    # *    Function Description    : Download firmware and store it into flash   */
    # *    Parameter in            : none                                        */
    # *    Parameter inout         : none                                        */
    # *    Parameter out           : none                                        */
    # *    Return value            : none                                        */
    # ****************************************************************************/


def Download_Firmware():
    global FileSize
    global NumOfPackets
    global Extra_Bytes
    
    print("Download File")
    # Downlaod Firmware Binary File Command
    storage.child(FirmwareName).download(FirmwareName)
     
    #Downlaod Public_Key_PC
    storage.child("Public_Key_PC/public_key_PC.pem").download("public_key_PC.pem")

    #Downlaod Signed_Firmware
    storage.child("Signed_Firmware.bin").download("Signed_Firmware.bin")
    
    #Verify The File
    exec(open("./Verify_File.py").read())
    
    #Decrypt The File
    exec(open("./DecryptFile.py").read())
    

    # File calculations
    FileSize = os.path.getsize(FirmwareName)
    print("File size is :", FileSize, "Bytes")
    
    # Calculate Number of Pacekts */
    NumOfPackets = int(FileSize / PACKET_SIZE)
    print("NumOfPackets = ", NumOfPackets)

    # Calculate Number of SubPackets */
    Extra_Bytes = FileSize % PACKET_SIZE
    print("Extra_Bytes = ", Extra_Bytes)

    # ****************************************************************************/

    # ****************************************************************************/
    # *    Function Name           : Send_First_Packet                           */
    # *    Function Description    : sends first packet into serial pin TX (pin1)*/
    # *              First Pacekt Contain HW ID (F429 or F407 )                  */
    # *              and App Size                                                */
    # *    Parameter in            : none                                        */
    # *    Parameter inout         : none                                        */
    # *    Parameter out           : none                                        */
    # *    Return value            : none                                        */
    # ****************************************************************************/
def Send_First_Packet():
    global FileSize

    sleep(1)
    # File calculations
    FileSize = os.path.getsize(FirmwareName)
    if(UpdateId == "F429"):		
        # F429 ID
#        AppSizeArr.append(0x50)
        byteInfo = 0x50
        ser.write(bytes([byteInfo]))
    else:
        byteInfo = 0x60
        ser.write(bytes([byteInfo]))
        # F407 ID
#        AppSizeArr.append(0x60)
        
    # Write Application Size 
    # First byte is the thousands value 
    # Second Byte is the Hundrades value
    # Third byte is the tens value
    # So for example if file size = 42876 Byte
    # First byte Sent(Thousands)  = 42
    # Second Byte sent(Hundrades) = 8
    # Third Byte sent (Tens)    = 76
    byteInfo = int(FileSize/1000)
    print(byteInfo)
    ser.write(bytes([byteInfo]))
    byteInfo = int((FileSize%1000)/100)
    print(byteInfo)
    ser.write(bytes([byteInfo]))
    byteInfo = int((FileSize%1000)%100)
    print(byteInfo)
    ser.write(bytes([byteInfo]))
#    AppSizeArr.append(FileSize/1000)
#    AppSizeArr.append( (FileSize % 1000) / 100)
#    AppSizeArr.append( (FileSize % 1000) % 100)		
        
#    for AppSizeArrElement in AppSizeArr:
#        print(AppSizeArrElement)
#        ser.write(AppSizeArrElement)
    # ****************************************************************************/

    # ****************************************************************************/
    # *    Function Name           : Send_Packet                                 */
    # *    Function Description    : sends 1024 byte into serial pin TX (pin1)   */
    # *    Parameter in            : none                                        */
    # *    Parameter inout         : none                                        */
    # *    Parameter out           : none                                        */
    # *    Return value            : none                                        */
    # ****************************************************************************/
def Send_Packet():
    # Variabel to count file size on it */
    global FileSize 
    global PacketNum
    global NumOfPackets
    global ByteBuffer
    global PACKET_SIZE
    global Extra_Bytes
    
    counter2 = 0
    # Opening firmware file 
    with open(FirmwareName, "rb") as f:
        print("Sending Send Packet ACK to F429")
        # Sending ACK to F429
        ser.write(bytes([BOOTLOADER_SEND_PACKET_CODE]))
        print("NumOfPackets2 = ", NumOfPackets)
        
        
        # Code will hault here untill all packets sent */
        while(NumOfPackets > 0):
            # Pointing the code to the Packet Number line
            f.seek(PacketNum*1024)
            
            RedyToRecivePacketAck = ser.read(1)
            print("RedyToRecivePacketAck = ",RedyToRecivePacketAck)
            
            # Send Packet Byte by byte
            print("Sending Packet", PacketNum+1)
            while(counter2 < PACKET_SIZE):
                # read byte from file
                ByteBuffer = f.read(1)
                
                # send this byte through UART
                ser.write(ByteBuffer)
                counter2 = counter2 + 1
                
            counter2 = 0
            PacketNum = PacketNum + 1 
            NumOfPackets = NumOfPackets - 1
            FileSize = FileSize - PACKET_SIZE
            
        print("Packets Sent Successfully")
        
        print("Extra_Bytes2 = ", Extra_Bytes)
        # Sending Extra bytes after packets

        if(Extra_Bytes > 0):
            f.seek(PacketNum * PACKET_SIZE)
            print("SEEK = ",PacketNum * PACKET_SIZE)
            print("Mstny El ACK")
            Ack1 = ser.read(1)
            print(Ack1) #43
            
            sleep(1)
            
            # Send an ACK to STM that PI is ready */
            ser.write(bytes([BOOTLOADER_SEND_SUBPACKET_CODE]))
            print(bytes([BOOTLOADER_SEND_SUBPACKET_CODE]))
            print("Sending SubPacket = ", Extra_Bytes, "Bytes")

            Ack3 = ser.read(1)
            print("ACk3 = ",Ack3)
            counter2 = 0
            

            print("counter= ",counter2)
            # Sending SubPacket byte by byte
            while(counter2 < Extra_Bytes): 
                # read byte from file
                ByteBuffer = f.read(1)
                
                ByteBuffer2 = str(ByteBuffer)
                print(ByteBuffer2)
                
                # send this byte through UART
                ser.write(ByteBuffer)
                counter2 = counter2 + 1

            print("counter2= ",counter2)   
            print("SubPacket Sent Successfully")	
            FileSize = FileSize - Extra_Bytes
                
    print("Firmware Sent Successfully")			
    # ****************************************************************************/				
                
                
                

#################################################################################
#				  Code Executed once (Instead of void(setup) at ESP)			#
#################################################################################

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

# Connect to realtime database
db = firebase.database()

# Initiating UART Communication with 115200 BaudRate
ser = serial.Serial("/dev/ttyS0", 115200)


# Sending ACK to F429 That PI is ready
ser.write(bytes([PI_READY]))

#################################################################################
#				  Code Executed forever (Instead of void(loop) at ESP)			#
#################################################################################

while True:
    # ********************************** Idle State ***********************************/
    if(PI_State == PI_IDLE_STATE):
        print("Idle State")
        # Get NewUpdate Address from realtime database
        NewUpdate1 = db.child("NewUpdate").get()
        # Get Newupdate value
        NewUpdate = NewUpdate1.val()
        print("New Update value = ", NewUpdate)

        # Get UpdateId Address from realtime database
        UpdateId1 = db.child("UpdateId").get()
        # Get UpdateId value
        UpdateId = UpdateId1.val()
        print("UpdateId value = ", UpdateId)

        # Check if there's a new update found
        if((NewUpdate == "True") and (ReadOnce == False)):

            print("New Update available")
            FirstPacket = 1
            ReadOnce = 1
            PI_State = PI_DOWNLOAD_FILE_STATE

        else:
            print("No Update available")
            PI_State = PI_IDLE_STATE

    # ********************************************************************************/

    # ********************************* Download File State **************************/
    elif(PI_State == PI_DOWNLOAD_FILE_STATE):
        print("Download FIle State")

        # Firmware Name Address on Realtime Database
        FirmwareNameAddress = db.child("FirmwareName").get()

        # Get Firmware Name Value
        FirmwareName2 = FirmwareNameAddress.val()

        # Type case to the variable to string
        FirmwareName = str(FirmwareName2)
        print(FirmwareName)

        # Download New Firmware
        Download_Firmware()
        
#######################################################################################
        
        
#######################################################################################

        PI_State = PI_SEND_UPDATE_REQUEST_STATE
    # ********************************************************************************/

    # ****************************** Send Update Request State ***********************/
    elif(PI_State == PI_SEND_UPDATE_REQUEST_STATE):
        print("Send Update Request State")

        # Send update request to Gateway node
        ser.write(bytes([PI_NEW_UPDATE_AVAILABLE]))
        PI_State = PI_WAIT_STM_RESPONSE_STATE
    # ********************************************************************************/

    # ******************************* Wait STM Response state ************************/
    elif(PI_State == PI_WAIT_STM_RESPONSE_STATE):
        print("Wait STM Response state")
        Rec_Msg = ser.read(1)

        print(Rec_Msg)

        if(Rec_Msg == bytes([DISCARD_UPDATE])):
            print("Discard Update response from F429")

        elif(Rec_Msg == bytes([STM_READY_TO_GET_INFO])):
            print("STM_READY_TO_GET_INFO")
            # Send an ACK to F429 */
            ser.write(bytes([BOOTLOADER_UPDATE_INFO_CODE]))
            PI_State = PI_SEND_PACKET_STATE

        elif(Rec_Msg == bytes([STM_READY_TO_RECEIVE_UPDATE_PACEKTS])):
            print("STM_READY_TO_RECEIVE_UPDATE_PACEKTS")
            PI_State = PI_SEND_PACKET_STATE 

        elif(Rec_Msg == bytes([RETRANSMIT_LAST_PACKET])):
            print("RETRANSMIT_LAST_PACKET")
            PI_State = PI_RETRANSMIT_PACKET_STATE 

        elif(Rec_Msg == bytes([STM_END_STATUS])):
            print("STM_END_STATUS")
            PI_State = PI_IDLE_STATE 

        else:
            print("Undefined Response")
            PI_State = PI_WAIT_STM_RESPONSE_STATE ;
    # ********************************************************************************/

    # ******************************** PI Send Pacekt State *************************/
    elif(PI_State == PI_SEND_PACKET_STATE):
        print("PI_SEND_PACKET_STATE")
        # Our first Packet is File Size 
        if(FirstPacket == 1):
           print("Sending First Packet")
           Send_First_Packet() 
           FirstPacket = 0 
        else:
          # Sending the Packets of the firmware
          print("Sending the rest of packets")
          Send_Packet()
        
        if(FileSize == 0):
          # All packets sent 
          print("Packets Sent")
          PI_State = PI_END_STATE
          
        PI_State = PI_WAIT_STM_RESPONSE_STATE
    # ********************************************************************************/

    # *************************** Retransmit State (Future Work) *********************/
    elif(PI_State == PI_RETRANSMIT_PACKET_STATE):
        print("PI_SEND_PACKET_STATE")
        PacketNum = PacketNum - 1
        NumOfPackets = NumOfPackets + 1
        if(FileSize == 0 and Extra_Bytes != 0):
            FileSize = FileSize + Extra_Bytes
        else:
            FileSize += PACKET_SIZE 
            PacketNum = PacketNum - 1 
            NumOfPackets = NumOfPackets + 1
        PI_State = PI_SEND_PACKET_STATE ;
    # ********************************************************************************/	

    # *************************** PI_END_STATE (Future Work) *********************/
    elif(PI_State == PI_END_STATE):
        print("End State")
        PI_State = PI_IDLE_STATE 
    # ********************************************************************************/

    else:
        print("Error State in FSM")

