'''!
@file encoder_reader.py 

@author Abe Muldrow
@author Lucas Rambo
@author Peter Tomson
@date February 8th, 2024
'''

import micropython
import time
import pyb
import motor_driver.py
# have to import pyb for it work on the board

class EncoderReader:
    """! 
    
    """
    def __init__ (self, in1pin, in2pin, timer):
        """! 
        Creates a encoder by initializing GPIO
        pins and turning off the motor for safety. 

        @param en_pin This is the value for the CPU pin needed to control the motor. This value is input as a string of the pin name.
                The pin is set to high in the code to enable motor control.
        @param in1pin This is the value for the first pin name needed to control the motor. This value is input as a string of the pin name.
        @param in2pin This is the value for the second pin name needed to control the motor. This value is input as a string of the pin name.
        @param timer This is the value for the timer channel of the motor. Set as a integer. 
        """
        # get the pin values for the pin store
        in1pin = getattr(pyb.Pin.board, in1pin)
        in2pin = getattr(pyb.Pin.board, in2pin)
 
        self.pin1 = pyb.Pin(in1pin, pyb.Pin.IN)
        self.pin2 = pyb.Pin(in2pin, pyb.Pin.IN)
        
        self.enc_timer = pyb.Timer(timer, freq = 1000)
        
        self.enc_channel_1 = self.enc_timer.channel(1, pyb.Timer.ENC_AB, pin = self.pin1)
        self.enc_channel_2 = self.enc_timer.channel(2, pyb.Timer.ENC_AB, pin = self.pin2)
        
        # init the values for read
        self.delta=0
        self.pos=0	# absolute total position
        self.prev_pos=0
#         self.ENx = pyb.Pin (en_pin, pyb.Pin.OUT_PP, value = 0)  # init the CPU pin
#         self.IN1x = pyb.Pin (in1pin, pyb.Pin.OUT_PP, value = 0) # init the first pin
#         self.IN2x = pyb.Pin (in2pin, pyb.Pin.OUT_PP, value = 0) # init the second pin
#         self.t = pyb.Timer(timer, freq=1000)    # start the timer from the timer value
#         self.tch1 = self.t.channel(1,pyb.Timer.PWM, pin=self.IN1x)  # create the timer channels for each motor pin
#         self.tch2 = self.t.channel(2,pyb.Timer.PWM, pin=self.IN2x)
#         self.ENx.high() # set the motor pin to high 
        print ("Creating an encoder!")

    def read (self):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
#         if level >= 0:  # test the sign of motor
#             self.tch1.pulse_width_percent(0)    # if positive turn the motor one direction based on the value of level
#             self.tch2.pulse_width_percent(level)
#         else:
#             self.tch2.pulse_width_percent(0)    # turn the motor the other way if negative
#             self.tch1.pulse_width_percent(-1*level) # set level as an absolute value
#                 
#         print (f"Setting duty cycle to {level}")
        self.value = self.enc_timer.counter()
        self.delta=self.value-self.prev_pos
    
        if self.delta<=-(16000+1)/2:
            self.delta=self.delta+16001
        elif self.delta>=(16000+1)/2:
            self.delta=self.delta-16001
                     
        self.pos=self.pos+self.delta    
        self.prev_pos=self.value
    
    def zero(self):
        self.delta=0
        self.pos=0	# absolute total position
        self.prev_pos=self.value
        


if __name__ == "__main__":  # test code contained below
    encoder1= EncoderReader('PC6','PC7',8)
    motor1 = MotorDriver ('PA10', 'PB4', 'PB5', 3)
    motor1.set_duty_cycle(50) 
    while True:
        try:
            for i in range(100):
                encoder1.read()
                print(encoder1.pos)
                time.sleep(.1)
            encoder1.zero()
        except KeyboardInterrupt:
            break