try:
    from pirc522.rfid import RFID
    from pirc522.util import RFIDUtil
except RuntimeError:
    print("Must be used on Raspberry Pi or Beaglebone")
