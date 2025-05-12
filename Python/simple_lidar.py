#!/usr/bin/env python3
"""
Simple LIDAR Visualizer
- Displays LIDAR data in real-time in a 3-meter radius circle
- Minimal functionality, focused on clarity and simplicity
"""
import serial
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import sys

class SimpleLidarVisualizer:
    def __init__(self):
        # LIDAR parameters
        self.SENSOR_HZ = 240      # Readings per second
        self.SENSOR_OFFSET = 3.0  # Sensor offset from center (cm)
        self.MAX_RADIUS = 300     # Plot radius in cm (3 meters)
        self.MAX_POINTS = 500     # Maximum points to display for performance
        
        # Variables for angle and RPM calculation
        self.current_rpm = 0.0
        self.angle = 0.0
        self.angle_step = 0.0
        
        # Storage for points to display
        self.points = deque(maxlen=self.MAX_POINTS) 
        
        # Setup visualization
        self.setup_plot()
        
        # Connect to LIDAR
        self.connect_lidar()
    
    def setup_plot(self):
        """Set up a simple circular plot for LIDAR data"""
        plt.ion()  # Interactive mode for real-time updates
        
        # Create figure and axis
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.canvas.manager.set_window_title('LIDAR Visualization (3m radius)')
        
        # Initialize empty scatter plot
        self.scatter = self.ax.scatter([], [], s=5, c='blue')
        
        # Set up axis and labels
        self.ax.set_xlabel('X (cm)')
        self.ax.set_ylabel('Y (cm)')
        self.ax.set_title('LIDAR Point Cloud')
        
        # Set equal aspect ratio and limits
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-self.MAX_RADIUS, self.MAX_RADIUS)
        self.ax.set_ylim(-self.MAX_RADIUS, self.MAX_RADIUS)
        
        # Add grid and circle to represent 3m boundary
        self.ax.grid(True, linestyle='--', alpha=0.7)
        boundary_circle = plt.Circle((0, 0), self.MAX_RADIUS, fill=False, 
                                     color='red', linestyle='-')
        self.ax.add_artist(boundary_circle)
        
        # Add 1m and 2m reference circles
        for radius in [100, 200]:
            circle = plt.Circle((0, 0), radius, fill=False, color='gray', 
                              linestyle='--', alpha=0.5)
            self.ax.add_artist(circle)
            self.ax.text(0, -radius, f"{radius} cm", ha='center', va='top', 
                       color='gray', fontsize=8)
        
        # Show plot
        plt.tight_layout()
        self.fig.canvas.draw()
    
    def connect_lidar(self):
        """Connect to LIDAR device using serial port"""
        # Find available serial ports
        import glob
        available_ports = glob.glob('/dev/tty.*') + glob.glob('/dev/cu.*')
        
        print("Available serial ports:")
        for i, port in enumerate(available_ports):
            print(f"[{i}] {port}")
        
        # Try to find a likely LIDAR port
        self.port = None
        for port in available_ports:
            if 'usbserial' in port:
                self.port = port
                break
        
        if not self.port and available_ports:
            self.port = available_ports[0]
        
        if not self.port:
            print("No serial ports found. Please connect your LIDAR device.")
            sys.exit(1)
        
        # Connect to the selected port
        try:
            self.ser = serial.Serial(self.port, 250000, timeout=1)
            print(f"Connected to {self.port}")
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {str(e)}")
            sys.exit(1)
    
    def run(self):
        """Main loop - read data and update visualization"""
        print("Reading LIDAR data... Press Ctrl+C to exit.")
        
        buffer = ""
        
        try:
            while True:
                if self.ser.in_waiting:
                    # Read all available data
                    data = self.ser.read(self.ser.in_waiting).decode('utf-8', errors='replace')
                    buffer += data
                    
                    # Process complete lines
                    lines = buffer.split('\n')
                    buffer = lines.pop() if lines else ""
                    
                    for line in lines:
                        line = line.strip()
                        
                        # Process RPM data
                        if line.startswith("R:"):
                            try:
                                rpm = float(line[2:])
                                self.current_rpm = rpm
                                self.angle_step = (rpm * 6) / self.SENSOR_HZ
                                self.angle = 0.0  # Reset angle
                            except ValueError:
                                continue
                        
                        # Process distance data
                        elif line.startswith("D:"):
                            try:
                                distance = int(line[2:])
                                self.process_distance(distance)
                            except ValueError:
                                continue
                
                # Update plot every 100ms for smoother visualization
                # and to prevent excessive CPU usage
                self.update_plot()
                plt.pause(0.1)
                
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            if hasattr(self, 'ser') and self.ser.is_open:
                self.ser.close()
                print("Serial port closed")
    
    def process_distance(self, distance):
        """Process a distance reading at the current angle"""
        # Skip invalid readings
        if distance <= 0 or distance > 800:
            self.angle = (self.angle + self.angle_step) % 360
            return
        
        # Convert polar to cartesian coordinates
        rad = math.radians(self.angle)
        
        # Account for sensor offset
        sensor_x = self.SENSOR_OFFSET * math.cos(rad)
        sensor_y = self.SENSOR_OFFSET * math.sin(rad)
        
        # Calculate point position
        x = sensor_x + distance * math.cos(rad)
        y = sensor_y + distance * math.sin(rad)
        
        # Store point
        self.points.append((x, y))
        
        # Update angle for next reading
        self.angle = (self.angle + self.angle_step) % 360
    
    def update_plot(self):
        """Update the visualization with current points"""
        if not self.points:
            return
        
        # Extract x and y coordinates
        x_values = [p[0] for p in self.points]
        y_values = [p[1] for p in self.points]
        
        # Update the scatter plot with new points
        self.scatter.set_offsets(np.column_stack((x_values, y_values)))
        
        # Update the title with RPM information
        self.ax.set_title(f'LIDAR Point Cloud - {self.current_rpm:.1f} RPM')
        
        # Redraw the plot
        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    visualizer = SimpleLidarVisualizer()
    visualizer.run()
