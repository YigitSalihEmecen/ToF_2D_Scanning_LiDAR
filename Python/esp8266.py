import socket
import time
import matplotlib.pyplot as plt
import math
import numpy as np
from collections import deque

UDP_PORT = 12345  # remotePort from ESP code
MAX_POINTS = 200  # Maximum number of points to display

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))  # listen on all local IPs

print("Listening for TF-Luna data over UDP...")

# Initialize plot
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-500, 500)
ax.set_ylim(-500, 500)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title('TF-Luna Data Visualization')
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')

# Store points in a deque with maximum length
x_points = deque(maxlen=MAX_POINTS)
y_points = deque(maxlen=MAX_POINTS)
scatter = ax.scatter([], [], c='blue', alpha=0.5)

count = 0
start_time = time.time()

def polar_to_cartesian(distance, angle_deg):
    # Convert angle from degrees to radians
    angle_rad = math.radians(angle_deg)
    # Calculate x and y coordinates
    x = distance * math.cos(angle_rad)
    y = distance * math.sin(angle_rad)
    return x, y

while True:
    data, addr = sock.recvfrom(1024)
    try:
        message = data.decode().strip()
        print(f"Received data: {message}")
        
        # Parse the message
        parts = message.split()
        distance = float(parts[1])  # D: value
        angle = float(parts[5])     # A: value
        
        # Convert to Cartesian coordinates
        x, y = polar_to_cartesian(distance, angle)
        
        # Add points to the deques
        x_points.append(x)
        y_points.append(y)
        
        # Update the plot
        scatter.set_offsets(np.c_[list(x_points), list(y_points)])
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
        
        count += 1
        
        current_time = time.time()
        if current_time - start_time >= 1.0:
            print(f"Received {count} data packets in the last second")
            count = 0
            start_time = current_time
    except Exception as e:
        print(f"Error processing data: {e}")
        continue
