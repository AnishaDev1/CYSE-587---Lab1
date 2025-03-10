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
    def __init__(self, pulse_duration=0.5, pulse_interval=2.0, noise_level=1.0):
        """
        Initialize a pulsed noise jammer.
        :param pulse_duration: Duration of each jamming pulse in seconds.
        :param pulse_interval: Interval between pulses in seconds.
        :param noise_level: Strength of the noise added during jamming.
        """
        self.pulse_duration = pulse_duration
        self.pulse_interval = pulse_interval
        self.noise_level = noise_level
        self.last_pulse_time = time.time()
        self.jamming_active = False

    def update_jamming_state(self):
        """Toggle jamming based on pulse timing."""
        current_time = time.time()
        elapsed_time = current_time - self.last_pulse_time

        if self.jamming_active and elapsed_time >= self.pulse_duration:
            self.jamming_active = False  # End jamming pulse
            self.last_pulse_time = current_time

        elif not self.jamming_active and elapsed_time >= self.pulse_interval:
            self.jamming_active = True  # Start a new jamming pulse
            self.last_pulse_time = current_time

    def jam_signal(self, message):
        """
        Applies pulsed jamming to a given message.
        If the jammer is active, introduce high noise or nullify the message.
        """
        self.update_jamming_state()
        if self.jamming_active:
            # Either completely jam (None) or introduce high noise in coordinates
            if random.random() < 0.5:  # 50% chance to completely jam the message
                return None, True
            else:
                message['latitude'] += random.uniform(-self.noise_level, self.noise_level)
                message['longitude'] += random.uniform(-self.noise_level, self.noise_level)
                message['altitude'] += random.uniform(-10 * self.noise_level, 10 * self.noise_level)
                return message, True
        return message, False  # Message not jammed




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


class SweepingJammer:
   
    def __init__(self, jamming_probability=0.4, noise_intensity=0.8, hop_rate=2, freq_range=(1090, 1100), power_dbm=-60):
        self.jamming_probability = jamming_probability
        self.noise_intensity = noise_intensity
        self.hop_rate = hop_rate  # Time interval (seconds) between frequency hops
        self.freq_range = list(range(freq_range[0], freq_range[1] + 1))  
        self.current_freq = random.choice(self.freq_range)  # Start on a random frequency
        self.power_dbm = power_dbm
        self.jamming_active = False  # Initially inactive
        self.jamming_thread = None  # Thread for frequency hopping

    def start_jamming(self):
    
        if not self.jamming_active:
            self.jamming_active = True
            self.jamming_thread = threading.Thread(target=self._hop_frequency, daemon=True)
            self.jamming_thread.start()
            print("[SweepingJammer] Jamming started...")

    def stop_jamming(self):
        
        if self.jamming_active:
            self.jamming_active = False
            if self.jamming_thread is not None:
                self.jamming_thread.join()
            print("[SweepingJammer] Jamming stopped.")

    def _hop_frequency(self):
       
        while self.jamming_active:
            time.sleep(self.hop_rate)
            self.current_freq = random.choice(self.freq_range)
            print(f"[SweepingJammer] Hopped to frequency {self.current_freq} MHz")

    def jam_signal(self, message, drone_freq):
      
        if self.jamming_active and drone_freq == self.current_freq and random.random() < self.jamming_probability:
            print(f"[SweepingJammer] Jamming message on {self.current_freq} MHz")

            if random.random() < self.noise_intensity:
                print("[SweepingJammer] Message completely lost!")
                return None, True  # Message is lost
            else:
                message['latitude'] += random.uniform(-0.05, 0.05)
                message['longitude'] += random.uniform(-0.05, 0.05)
                message['altitude'] += random.uniform(-50, 50)
                return message, True
        return message, False

    def jamming_signal_power(self):
     
        return self.power_dbm

# Example Drone Class
class Drone:
    """Simulated drone that sends its position over a given frequency."""
    def __init__(self, drone_id, initial_position, frequency):
        self.id = drone_id
        self.position = initial_position
        self.frequency = frequency  
        self.logs = []

    def transmit(self, jammer):
        """Sends a position signal that may be jammed."""
        message = {'latitude': self.position[0], 'longitude': self.position[1], 'altitude': self.position[2]}
        jammed_message, jammed = jammer.jam_signal(message, self.frequency)

        if jammed_message is None:
            print(f"[Drone-{self.id}] Transmission blocked!")
        else:
            print(f"[Drone-{self.id}] Sent position: {jammed_message}")

        self.logs.append(jammed_message)
        return jammed_message

# Initialize drone and jammer
jammer = SweepingJammer(jamming_probability=0.5, noise_intensity=0.8, hop_rate=3, freq_range=(1090, 1095), power_dbm=-55)
#jammer = PulsedNoiseJammer(jamming_probability=0.3, noise_intensity=0.7, jamming_power_dbm=-70)
drone = Drone(drone_id=1, initial_position=(33.6844, 73.0479, 1000), frequency=1092)

# Start jamming before drone transmission
jammer.start_jamming()

# Simulate transmissions
for _ in range(10):
    time.sleep(1)
    drone.transmit(jammer)

# Stop jamming after testing
jammer.stop_jamming()
