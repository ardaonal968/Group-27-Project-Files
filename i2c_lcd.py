# original code documents
# Modified Python I2C library for Raspberry Pi
# as found on http://www.recantha.co.uk/blog/?p=4849
# Joined existing 'i2c_lib.py' and 'lcddriver.py' into a single library
# added bits and pieces from various sources
# By DenisFromHR (Denis Pleic)
# 2015-02-10, ver 0.1
# modified by Oskar Castren

from time import sleep
import machine

# LCD Address (adjust as needed)
ADDRESS = 0x27

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00
LCD_4BITMODE = 0x00

En = 0b00000100  # Enable bit
Rs = 0b00000001  # Register select bit

class i2c_device:
    """Class for communicating with I2C devices using MicroPython's I2C."""
    def __init__(self, addr=ADDRESS, i2c=None):
        self.addr = addr
        self.i2c = i2c or machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))  # Default I2C pins
        self.backlight = LCD_BACKLIGHT  # Ensure backlight is ON

    def write_cmd(self, cmd):
        """Write a single command, ensuring backlight remains ON."""
        self.i2c.writeto(self.addr, bytes([cmd | self.backlight]))  # Include backlight
        sleep(0.0001)

class lcd:
    """Class for interfacing with I2C LCD device."""
    def __init__(self, i2c, addr=ADDRESS):
        self.lcd_device = i2c_device(addr)
        self.i2c = i2c
        self.backlight_on()
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self.lcd_write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        sleep(0.2)

    def lcd_strobe(self, data):
        """Clocks enable bit to latch command."""
        self.lcd_device.write_cmd(data | En)
        sleep(0.0005)
        self.lcd_device.write_cmd(data & ~En)
        sleep(0.0001)

    def lcd_write(self, cmd, mode=0):
        """Write a command to lcd."""
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_write_four_bits(self, data):
        """Write four bits of data to lcd."""
        self.lcd_device.write_cmd(data)
        self.lcd_strobe(data)

    def lcd_display_string(self, string, line):
        """Display string on lcd screen."""
        if line == 1:
            self.lcd_write(0x80)
        elif line == 2:
            self.lcd_write(0xC0)
        for char in string:
            self.lcd_write(ord(char), Rs)

    def lcd_clear(self):
        """Clear lcd and set to home."""
        self.lcd_write(LCD_CLEARDISPLAY)
        self.lcd_write(LCD_RETURNHOME)
    def backlight_on(self):
        """Turn the backlight ON."""
        self.lcd_device.backlight = LCD_BACKLIGHT

    def backlight_off(self):
        """Turn the backlight OFF."""
        self.lcd_device.backlight = LCD_NOBACKLIGHT


