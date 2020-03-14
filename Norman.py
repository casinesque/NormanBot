import telepot  # Importing the telepot library
import datetime
import time
import redis
import Utils
import RPi.GPIO as GPIO
from picamera import PiCamera


GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN) #PIR
camera = PiCamera()
camera.rotation = 180
camera.resolution = (1280, 720)

bot = telepot.Bot(MY_BOT_API_KEY) #add this to another filed called Utils.py
redis_client=redis.StrictRedis(host='localhost',port=6379, db=0) #skitp this if you do not need redis
#print (bot.getMe())
try:
    time.sleep(2) # to stabilize sensor
    while True:
      if GPIO.input(23)==True:
            #time.asleep(0.5) #Buzzer turns on for 0.5 sec
            print("Motion Detected...")
            timestamp = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
            redis_client.set(timestamp,"Motion detection!")
            bot.sendMessage (MY_TELEGRAM_ID_KEY, str("WARNING! INTRUDER ALERT!"))
            #sleep(1)
            camera.start_preview()
            camera.capture('/home/pi/Desktop/image.jpg') #choose your favourite path.
            print("Picture taken!")
            currenttime=datetime.datetime.now()
            print("Timestamp acquired")
            #camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') --> really slow op
            #camera.annotate_text = "%s" % currenttime --> really slow op
            print("Starting send operation...")
            bot.sendPhoto(MY_TELEGRAM_ID_KEY, photo=open('/home/pi/Desktop/image.jpg', 'rb'))
            print("Send operation completed.")
            camera.stop_preview()
            #time.sleep(2) #to avoid multiple detection

      else:
            print("no motion") #optional
            time.sleep(0.3)#loop delay, should be less than detection delay        
except:
    GPIO.cleanup()
