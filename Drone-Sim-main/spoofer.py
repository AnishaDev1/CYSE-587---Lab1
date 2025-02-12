import random
import numpy as np
import time

class Spoofer:
    """
    This class simulates ADS-B spoofing by modifying legitimate drone messages
    or injecting entirely fake drones into the system.
    """
    def __init__(self, spoof_probability=0.5, fake_drone_id="FAKE123"):
        self.spoof_probability = spoof_probability
        self.fake_drone_id = fake_drone_id 

    def spoof_message(self, message):
        """Modify a real drone message or inject a fake drone."""
        if random.random() < self.spoof_probability:
            for i in random.uniform(0, 200): # for loop to spoof messages a random number of times (between 0 and 200)
                print("[Spoofer] Spoofing message:", message)
                spoofed_message = message.copy()
                spoofed_message['latitude'] += random.uniform(-0.5, 0.5) #changed ranges 
                spoofed_message['longitude'] += random.uniform(-0.5, 0.5) #changed ranges 
                spoofed_message['altitude'] += random.uniform(-60, 60) #changed ranges
                spoofed_message['timestamp'] += time.time() + random.uniform(0.8, 1.2) # modified range to reflect ADS-B broadcast at random time, roughly 0.8 - 1.2 seconds, to report wrong time
                spoofed_message['drone_id'] = self.fake_drone_id if random.random() < 0.5 else message['drone_id']
                return spoofed_message, True
        return message, False