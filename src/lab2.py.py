import micropython
import time
import pyb


pinPB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
pinPB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)


# adcpin_6 = pyb.ADC(pinPB6)
# adcpin_7 = pyb.ADC(pinPB7)

t_4 = pyb.Timer(4, freq = 1000)

# pyb.Timer.ENC_AB(t_4)  # start the timer from the timer value
# tch1 = t.channel(pyb.Timer.A, pin=pinPB6)  # create the timer channels for each motor pin
# tch2 = t.channel(pyb.Timer.B, pin=pinPB7)
enc_channel_1 = t_4.channel(1, pyb.Timer.ENC_AB, pin = pinPB6)
enc_channel_2 = t_4.channel(2, pyb.Timer.ENC_AB, pin = pinPB7)


while True:
    try:
        value = t_4.counter()
        print(value)
        time.sleep(0.25)
    except KeyboardInterrupt:
        break