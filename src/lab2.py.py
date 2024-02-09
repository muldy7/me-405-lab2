import micropython
import time
import pyb

# first set of pins
pinPB6 = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
pinPB7 = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)

# second set of pins
pinPC6 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
pinPC7 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)

# timer for first set
t_4 = pyb.Timer(4, freq = 1000)

# timer for second set
t_8 = pyb.Timer(8, freq = 1000)

# encoders for first set
enc_channel_1 = t_4.channel(1, pyb.Timer.ENC_AB, pin = pinPB6)
enc_channel_2 = t_4.channel(2, pyb.Timer.ENC_AB, pin = pinPB7)

# encoders for second set
enc_channel_1b = t_8.channel(1, pyb.Timer.ENC_AB, pin = pinPC6)
enc_channel_2b = t_8.channel(2, pyb.Timer.ENC_AB, pin = pinPC7)


delta=0
pos=0
prev_pos=0

while True:
    try:
        
        value = t_8.counter()
        delta=value-prev_pos
    
        if delta<=-(16000+1)/2:
            delta=delta+16001
        elif delta>=(16000+1)/2:
            delta=delta-16001
                     
        pos=pos+delta    
        prev_pos=value
        
        print(value,pos,delta)
        time.sleep(0.25)
    except KeyboardInterrupt:
        break