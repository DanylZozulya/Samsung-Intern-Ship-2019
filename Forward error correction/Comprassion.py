from Channel_Model import channel_model
from Encoder import Encoder
from Decoder import Decoder

def channel_threshold(s,p):
    c=0
    a=s._sour_pack
    b=s._red_pack
    for i in range(b+1):
        c+=(p**(a+i))*((1-p)**(b-i))
    return c