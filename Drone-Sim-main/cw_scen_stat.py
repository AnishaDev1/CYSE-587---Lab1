from jammer import ContinuousWaveJammer
import time
import numpy as np
import matplotlib.pyplot as plt
import os
from drone import Drone
from route import RouteGenerator
from gcs import GCS
from adsbchannel import ADSBChannel
from spoofer import Spoofer
import seaborn as sns

# Define central location (e.g., Washington, D.C.)
center_lat, center_lon = 38.8977, -77.0365  

# Initialize GCS
gcs = GCS(center_lat, center_lon)
gcs_pos = (center_lat, center_lon)

# Create a RouteGenerator instance
route_gen = RouteGenerator(center_lat, center_lon, num_routes=2, waypoints_per_route=5, max_offset=0.02)
routes = route_gen.generate_routes()

# Function to initialize drones
def initialize_drones():
    return [
        Drone(
            id=f"{i+1}",
            drone_type=f"type{i+1}",
            acceleration_rate=2.0,
            climb_rate=3.0,
            speed=10.0 + i*5,
            position_error=2.0,
            altitude_error=1.0,
            battery_consume_rate=0.05,
            battery_capacity=10.0 + i*5,
            route=routes[i]
        )
        for i in range(len(routes))
    ]

# Scenarios using CW Jamming
scenarios = {
    "No Attacks": {"jamming": False, "spoofing": False},
    "Only CW Jamming": {"jamming": True, "spoofing": False},
    "CW Jamming and Spoofing": {"jamming": True, "spoofing": True},
}

def run_simulation(jamming=False, spoofing=False, spoof_probability=0.5): 
    channel = ADSBChannel()
    
    jammer = ContinuousWaveJammer(power_dbm=-55, noise_level=0.1, jamming_interval=1.0) if jamming else None  
   
    spoofer = Spoofer(spoof_probability=spoof_probability, fake_drone_id="FAKE-DRONE") if spoofing else None

    drones = initialize_drones()
    total_messages = 0
    lost_messages = 0
    packet_loss_over_time = []
    snr_values = []
    latency_values = []
    throughput_values = []

    start_time = time.time()

    for drone in drones:
        while True:
            status = drone.calculate_navigation(1)
            if status in [-1, -2, 0]:
                break

            send_time = time.time()
            original_message = {
                'drone_id': drone.id,
                'latitude': drone.current_position[0],
                'longitude': drone.current_position[1],
                'altitude': drone.current_position[2],
                'timestamp': send_time
            }

            received_message, delay_ns, corrupted, snr_db = channel.transmit(
                original_message, gcs_pos, jammer=jammer, spoofer=spoofer
            )

            if jamming and received_message is not None:
                received_message = jammer.jam_signal(received_message)

            receive_time = time.time()
            total_messages += 1

            if jamming and jammer:
                received_message = jammer.jam_signal(received_message)
                jammed = received_message is None
    
                if jammed:
                    lost_messages += 1
                    packet_loss_over_time.append((total_messages, lost_messages / total_messages * 100))
                    continue


            if spoofing and spoofer:
                received_message, spoofed = spoofer.spoof_message(received_message)

            gcs.receive_update(
                received_message['drone_id'],
                (
                    received_message['latitude'],
                    received_message['longitude'],
                    received_message['altitude']
                )
            )

            if corrupted and not (jamming and jammed):
                lost_messages += 1

            packet_loss_over_time.append((total_messages, lost_messages / total_messages * 100))
            snr_values.append((total_messages, snr_db))

            latency = (receive_time - send_time) * 1000
            latency_values.append((total_messages, latency))

            elapsed_time = receive_time - start_time
            throughput = total_messages / elapsed_time
            throughput_values.append((elapsed_time, throughput))

    return packet_loss_over_time, snr_values, latency_values, throughput_values

# Run simulations for CW Jamming scenarios
results = {}
for scenario, params in scenarios.items():
    print(f"Running scenario: {scenario}")
    packet_loss_data, snr_data, latency_data, throughput_data = run_simulation(**params)
    results[scenario] = {
        'packet_loss': packet_loss_data,
        'snr': snr_data,
        'latency': latency_data,
        'throughput': throughput_data
    }

# Save results
if not os.path.exists('results'):
    os.makedirs('results')

# Plot results
def plot_cw_results(results):
    plt.figure(figsize=(12, 6))
    for scenario, data in results.items():
        if 'packet_loss' in data:
            times, packet_loss = zip(*data['packet_loss'])
            plt.plot(times, packet_loss, label=scenario)

    plt.xlabel('Total Messages Sent')
    plt.ylabel('Packet Loss (%)')
    plt.title('Packet Loss Over Time - CW Jamming')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/cw_packet_loss.png')
    plt.show()

plot_cw_results(results)
