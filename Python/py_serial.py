import serial
import math
import matplotlib.pyplot as plt
import numpy as np

# === Serial Setup ===
ser = serial.Serial('/dev/tty.usbserial-140', 115200)

# === TF-Luna settings ===
SENSOR_HZ = 240  # Readings per second

# === State ===
current_rpm = 0.0
angle = 0.0
angle_step = 0.0
xs = []
ys = []


# === Plot Setup ===
plt.ion()
fig, ax = plt.subplots()
scatter = ax.scatter([], [], s=4, c='blue')
ax.set_xlim(-50, 50)
ax.set_ylim(-50, 50)

ax.set_aspect('equal')
ax.set_title("LiDAR 2D Plot (Hall-triggered rotation)")

update_counter = 0
UPDATE_EVERY = 5  # Plot update every 5 points

while True:
    try:
        line = ser.readline().decode().strip()

        # === Handle RPM reading (new rotation starts here) ===
        if line.startswith("R:"):
            try:
                current_rpm = float(line[2:])
                angle_step = (current_rpm * 6) / SENSOR_HZ
                angle = 0  # Reset angle — Hall effect = 0 degrees
            except:
                continue

        # === Handle Distance reading ===
        elif line.startswith("D:"):
            try:
                distance = int(line[2:])
            except:
                continue

            # Calculate (x, y)
            rad = math.radians(angle)
            x = distance * math.cos(rad)
            y = distance * math.sin(rad)

            xs.append(x)
            ys.append(y)

            # Increment angle for next sample
            angle = (angle + angle_step) % 360

            # Limit to last 200 points
            if len(xs) > 500:
                xs = xs[-500:]
                ys = ys[-500:]


            # Plot update
            update_counter += 1
            if update_counter >= UPDATE_EVERY:
                scatter.set_offsets(np.c_[xs, ys])
                ax.set_title(f"RPM: {current_rpm:.1f} | Points: {len(xs)}")
                fig.canvas.draw()
                fig.canvas.flush_events()
                update_counter = 0

    except KeyboardInterrupt:
        break
