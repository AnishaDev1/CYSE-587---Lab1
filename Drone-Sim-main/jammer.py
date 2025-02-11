import random
import time
import numpy as np

class Jammer:
    """
    This class simulates jamming by introducing errors, increasing delay, or blocking messages.
    """
    def __init__(self, jamming_probability=0.3, noise_intensity=0.7, jamming_power_dbm=-70):
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity  # Higher value increases interference
        self.jamming_power_dbm = jamming_power_dbm  # Default jamming signal power in dBm

    def jam_signal(self, message):
        """Introduce signal degradation or block messages entirely."""
        if random.random() < self.jamming_probability:
            print("[Jammer] Jamming message:", message)
            if random.random() < self.noise_intensity:
                print("[Jammer] Message completely lost!")
                return None, True  # Message is lost
            else:
                message['latitude'] += random.uniform(-0.1, 0.1)
                message['longitude'] += random.uniform(-0.1, 0.1)
                message['altitude'] += random.uniform(-100, 100)
                return message, True
        return message, False

    def jamming_signal_power(self):
        """Returns the power of the jamming signal in dBm."""
        return self.jamming_power_dbm

#class PulsedNoiseJammer:
    #def __init__(self, pulse_duration=0.5, pulse_interval=2.0, noise_level=1.0):
        #self.pulse_duration = pulse_duration
        #self.pulse_interval = pulse_interval
        #self.noise_level = noise_level
        #self.jamming_active = False

   # def generate_noise(self, signal_length):
        #return np.random.normal(0, self.noise_level, signal_length)

   # def jam_signal(self, signal):
        #jammed_signal = np.copy(signal)
        #current_time = 0
        
        #while current_time < len(signal):
            #if random.random() > 0.5:  # Random chance to activate jamming
                #noise_burst = self.generate_noise(min(int(self.pulse_duration * len(signal)), len(signal) - current_time))
                #jammed_signal[current_time:current_time+len(noise_burst)] += noise_burst
            #current_time += int(self.pulse_interval * len(signal))

        #return jammed_signal

   # def start_jamming(self):
        #while True:
            #print("Jamming activated")
            #self.jamming_active = True
            #time.sleep(self.pulse_duration)
            #print("Jamming deactivated")
            #self.jamming_active = False
            #time.sleep(self.pulse_interval)
