# Simple LIDAR Visualizer

A minimalist Python script for visualizing LIDAR sensor data in real-time.

## Features

- Real-time visualization of LIDAR point cloud data
- Fixed 3-meter radius display
- Reference circles at 1m and 2m distances
- Automatic serial port detection
- Displays current RPM in title
- Minimal and clean visualization

## Requirements

- Python 3.x
- matplotlib
- numpy
- pyserial

## Usage

Run the script with:

```bash
python simple_lidar.py
```

The script will automatically detect connected LIDAR devices and visualize the data in a fixed 3-meter radius circle.

## Sensor Data Format

The script expects serial data in the following format:

- RPM data: `R:<value>` (e.g., `R:20.5`)
- Distance data: `D:<value>` (e.g., `D:150`)

Press Ctrl+C to exit the visualization.
