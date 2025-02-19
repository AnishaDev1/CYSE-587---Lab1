import random
import time
import numpy as np
import threading

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

class PulsedNoiseJammer:
    """
    Implements Pulsed Noise Jamming (Burst Jamming) where interference occurs in short bursts.
    """
    def __init__(self, pulse_duration=0.5, pulse_interval=2.0, noise_level=1.0):
        self.pulse_duration = pulse_duration  # Duration of jamming bursts (seconds)
        self.pulse_interval = pulse_interval  # Time between bursts (seconds)
        self.noise_level = noise_level  # Intensity of noise
        self.jamming_active = False
        self.jamming_thread = None

    def generate_noise(self, signal_length):
        """ Generate noise burst """
        return np.random.normal(0, self.noise_level, signal_length)

    def jam_signal(self, message):
        """ Introduce pulsed noise into the signal """
        if message is None:
            return None
        
        if random.random() > 0.5:  # Random chance to activate jamming
            print("[PulsedNoiseJammer] Jamming message:", message)
            message['latitude'] += random.uniform(-0.1, 0.1)
            message['longitude'] += random.uniform(-0.1, 0.1)
            message['altitude'] += random.uniform(-50, 50)
        
        return message

    def start_jamming(self):
        """ Start pulsed jamming in a separate thread """
        if not self.jamming_active:
            self.jamming_active = True
            self.jamming_thread = threading.Thread(target=self._run_jamming, daemon=True)
            self.jamming_thread.start()
            print("[PulsedNoiseJammer] Jamming started...")

    def stop_jamming(self):
        """ Stop jamming """
        if self.jamming_active:
            self.jamming_active = False
            if self.jamming_thread is not None:
                self.jamming_thread.join()
            print("[PulsedNoiseJammer] Jamming stopped.")
    
    def jamming_signal_power(self):
        """Returns the power of the jamming signal in dBm."""
        return self.jamming_power_dbm

    def _run_jamming(self):
        """ Internal function to activate jamming bursts """
        while self.jamming_active:
            print("[PulsedNoiseJammer] Jamming activated")
            time.sleep(self.pulse_duration)
            print("[PulsedNoiseJammer] Jamming deactivated")
            time.sleep(self.pulse_interval)

# Example Usage
if __name__ == "__main__":
    jammer = PulsedNoiseJammer(pulse_duration=0.5, pulse_interval=2.0, noise_level=1.0)
    jammer.start_jamming()
    time.sleep(10)  # Simulate system running
    jammer.stop_jamming()



class ContinuousWaveJammer:
    """
    Simulates CW Jamming, continuously interfering with signals by adding constant noise.
    """

    def __init__(self, power_dbm=-60, noise_level=0.5, jamming_interval=1.0):
        self.power_dbm = power_dbm  # Jamming signal power
        self.noise_level = noise_level  # Strength of interference
        self.jamming_interval = jamming_interval  # Time between noise applications
        self.jamming_active = False  # Track if jamming is running
        self.jamming_thread = None  # Thread to handle jamming

    def jam_signal(self, message):
        """
        Adds continuous noise to GPS signal.
        message: Dictionary containing latitude, longitude, and altitude.
        Returns a jammed message.
        """
        if message is None:
            return None

        jammed_message = message.copy()
        jammed_message['latitude'] += np.random.normal(0, self.noise_level)
        jammed_message['longitude'] += np.random.normal(0, self.noise_level)
        jammed_message['altitude'] += np.random.normal(0, self.noise_level * 50)  # Adjusted for altitude variations

        print("[CWJammer] Jamming signal applied:", jammed_message)
        return jammed_message

    def jamming_signal_power(self):
        """Returns the power of the CW jamming signal in dBm."""
        return self.power_dbm

    def start_jamming(self):
        """Starts continuous jamming in a separate thread."""
        if not self.jamming_active:
            self.jamming_active = True
            self.jamming_thread = threading.Thread(target=self._run_jamming, daemon=True)
            self.jamming_thread.start()
            print("[CWJammer] Continuous jamming started...")

    def stop_jamming(self):
        """Stops continuous jamming."""
        if self.jamming_active:
            self.jamming_active = False
            if self.jamming_thread is not None:
                self.jamming_thread.join(timeout=1.0)  # Timeout prevents blocking
            print("[CWJammer] Jamming stopped.")

    def _run_jamming(self):
        """Internal function to simulate continuous noise."""
        while self.jamming_active:
            print(f"[CWJammer] Jamming active... Power: {self.power_dbm} dBm")
            time.sleep(self.jamming_interval)

# Example Usage
if __name__ == "__main__":
    cw_jammer = ContinuousWaveJammer(power_dbm=-55, noise_level=1.0, jamming_interval=1.0)
    cw_jammer.start_jamming()
    time.sleep(5)
    cw_jammer.stop_jamming()
