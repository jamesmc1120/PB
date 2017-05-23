#!/user/bin/python
import RPi.GPIO as GPIO
import time
import screen
import numpad
import switch
import led
start = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# sets GPIO for push buttons
right_button = 15
left_button = 14
menu_button = 22


GPIO.setup(right_button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(right_button, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(left_button, GPIO.IN, GPIO.PUD_UP)

# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

GPIO.setup(LCD_E, GPIO.OUT)  # E
GPIO.setup(LCD_RS, GPIO.OUT) # RS
GPIO.setup(LCD_D4, GPIO.OUT) # DB4
GPIO.setup(LCD_D5, GPIO.OUT) # DB5
GPIO.setup(LCD_D6, GPIO.OUT) # DB6
GPIO.setup(LCD_D7, GPIO.OUT) # DB7





n1 = 5
n2 = 6
n3 = 13
n4 = 19
n5 = 26
n6 = 12
n7 = 16
n8 = 20
n9 = 12
n0 = 4
star = 17
pound = 27

global win
global acodeloop
acodeloop = True
display = []
keys = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n0,star,pound]
numbers = [1,2,3,4,5,6,7,8,9,0,"*","#"]
shows = dict(zip(keys,numbers))  # this lines points one string at the other
acode = []
aacode = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(n1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n3, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n4, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n5, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n6, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n7, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n8, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n9, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(n0, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(star, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(pound, GPIO.IN, GPIO.PUD_UP)



def setup():
# Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7

  # Initialise display
  lcd_init()

  
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
  
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  lcd_toggle_enable()

def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display

  message = message.ljust(LCD_WIDTH," ")

  lcd_byte(line, LCD_CMD)

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def choose(): #not used
    global aacode
    screen.lcd_string("Choose Game", LCD_LINE_1)
    screen.lcd_string("1:Timer  2:Bomb", LCD_LINE_2)
    for key in keys:
        if GPIO.input(key) == False:
            acode.append(shows[key])  # adds new input to the array
            aacode = "".join(str(elm) for elm in acode)  #takes the array , converts each element to a string and then removes the commas and brackets.
            print aacode
            if aacode == 1:
                print "timer"
                numpad.numpad1()
            if aacode == 2:
                print "bomb"
                switch.switch1()

def choose2():    
    screen.lcd_string("Choose Game", LCD_LINE_1)
    screen.lcd_string("1:Bomb  2:Timer", LCD_LINE_2)    
    for key in keys:
        if GPIO.input(key) == False:
            print key
            if key == 5:
                print "numpad"
                numpad.numpad2()
            if key == 6:
                print "switch"
                switch.switch1()

        
def run():                
    led.updateHue(0, 0,255)
    while acodeloop == True:
        choose2()
def reset():
    lcd_init()
    screen.lcd_string("Choose Game", LCD_LINE_1)
    screen.lcd_string("1:Timer  2:Bomb", LCD_LINE_2)
    #time.sleep(1)
    while True:
        run()
        

        
        
if __name__ == '__main__':

  try:
    lcd_init()               
    while True:                
        run()
  except KeyboardInterrupt:
    screen.lcd_string("Fuckin Reapers",LCD_LINE_1)
    screen.lcd_string("",LCD_LINE_2)
    pass
  finally:
    screen.lcd_byte(0x01, LCD_CMD)
    screen.lcd_string("Fuckin Reapers",LCD_LINE_1)
    screen.lcd_string("",LCD_LINE_2)
    GPIO.cleanup()       
        
#if __name__== 'starttest':

  
  
    #lcd_byte(0x01, LCD_CMD)
    #lcd_string("starttest import",LCD_LINE_1)        

    
