from motors import *
from sensors import *

def follower():
    sE, sD = getSensorsValue()
    if(sE == 0 and sD == 0):
        Ahead()
    
