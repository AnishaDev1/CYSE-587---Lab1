import random
import numpy as np
import time
#some positioning libraries that may be helpful. 
#import geopy 
#from geographiclib import geodesic #can calculate distances between coordinates with this??
from gcs import GCS
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#import pygnssutils
#import gnssanalysis #this one took a few min for an install

class Spoofer:
    """
    This class simulates ADS-B spoofing by modifying legitimate drone messages
    or injecting entirely fake drones into the system.
    """
    def __init__(self, spoof_probability=0.5, fake_drone_id="FAKE123"):
        self.spoof_probability = spoof_probability
        self.fake_drone_id = fake_drone_id 
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.position = (self.lat,self.lon,self.alt)
        self.drone_position = {}

    def spoof_message(self, message):
        """Modify a real drone message or inject a fake drone."""
        if random.random() < self.spoof_probability:
            #for i in random.randrange(0, 200): # for loop to spoof messages a random number of times (between 0 and 200)
                print("[Spoofer] Spoofing message:", message)
                spoofed_message = message.copy()
                spoofed_message['latitude'] += self.lat + random.uniform(0, 0.5)  # changed ranges - only positive values so position only shifts in one direction
                spoofed_message['longitude'] += self.lon + random.uniform(0, 0.5) # changed ranges 
                spoofed_message['altitude'] += self.alt + random.uniform(-60, 60) #changed ranges
                spoofed_message['timestamp'] += time.time() + random.uniform(0.8, 1.2) # modified range to reflect ADS-B broadcast at random time, roughly 0.8 - 1.2 seconds, to report wrong time
                spoofed_message['drone_id'] = self.fake_drone_id if random.random() < 0.5 else message['drone_id']
                #GCS.receive_update( spoofed_message['drone_id'],(spoofed_message['latitude'], spoofed_message['longitude'], spoofed_message['altitude']))
                #for positioning maybe we use recieve update in GCS from the real drone and like add a few meters to it?
                return spoofed_message, True
        return message, False