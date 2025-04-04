import dht
import time
from i2c_lcd import lcd
import machine
print("we in the building")

#sets sensor input pin
sensorpin = 3

#sets motor output pin
motorpin = 17

#ideal humidity in %
hum_thres = 30

#lcd setup
i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0), freq=400000)
lcd = lcd(i2c, 0x27)
#sensor setup
sensor = dht.DHT11(machine.Pin(sensorpin))

#motor setup
motor = machine.Pin(motorpin, machine.Pin.OUT)

#function to get humidity value from sensor
def read_sensor():
    sensor.measure()
    return sensor.humidity()

#function to spin fan motor
def spin_motor():
    motor.value(1)
    print("we almost spinnin")
    while read_sensor() < hum_thres: #checks humidity and sleeps while below threshold
        print("we spinnin")
        lcd.lcd_clear()
        lcd.lcd_display_string(str(f"Humidity: {read_sensor()}%"), 1)
        lcd.lcd_display_string("Humidifying", 2)
        time.sleep(5)
    motor.value(0)

print("we on the floor")   
#main function for reading sensor and turning on the motor as necessary
def main():
    print("in main function")
    motor.value(0) #initial state is off
    while True:
        print("in read sensor loop")
        hum = read_sensor()
        print(f"Humidity = {hum}%")
        lcd.lcd_clear()
        lcd.lcd_display_string(str(f"Humidity: {hum}%"), 1)
        lcd.lcd_display_string("Humidity ideal", 2)
        if(read_sensor() < hum_thres):
            spin_motor()
        time.sleep(1)
main() 