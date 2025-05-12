# DIY LiDAR System

A graduation project for creating a low-cost, DIY Light Detection and Ranging (LiDAR) system using Arduino and Python.

## Project Overview

This project implements a homemade LiDAR system that uses a TF-Luna distance sensor mounted on a rotating platform to create a 2D point cloud visualization of surroundings. The system captures distance data at various angles as the sensor rotates, enabling mapping of the environment within a 3-meter radius.

## Repository Structure

- **Arduino/** - Contains the firmware for the microcontroller
  - **Read_Send/Read_Send.ino** - Arduino code that controls the motor and reads/transmits sensor data
  
- **Python/** - Contains visualization software
  - **simple_lidar.py** - Minimalist Python script for visualizing LiDAR data in real-time
  - **py_serial.py** - (Empty in current version, but backup contains a more complex GUI version)
  
- **3D_models/** - Contains 3D printable models for physical components
  - **Body.3mf** - Main housing for the LiDAR system
  - **MotorGear.3mf** - Gear for the motor
  - **Spinning_Head.3mf** - Rotating head that holds the sensor
  
- **Documents/** - Project documentation
  - **ENG402-Graduation_Project_Report_Yigit_Salih_Emecen.pdf** - Detailed project report

## Hardware Requirements

- Arduino board (e.g., Arduino Uno/Nano)
- TF-Luna I2C LiDAR sensor
- Hall effect sensor
- DC motor
- Motor driver
- 3D printed components (files provided in 3D_models folder)
- Appropriate power supply

## Software Requirements

- Arduino IDE
- Python 3.x with the following libraries:
  - matplotlib
  - numpy
  - pyserial

## Setup Instructions

1. **3D Print the Components**:
   - Print all files in the `3D_models` folder using appropriate materials

2. **Assemble the Hardware**:
   - Mount the TF-Luna sensor on the spinning head
   - Attach the motor gear to the DC motor
   - Install the Hall effect sensor at the reference position
   - Connect all components according to the pin configuration in the Arduino code

3. **Upload Arduino Code**:
   - Open `Arduino/Read_Send/Read_Send.ino` in the Arduino IDE
   - Connect your Arduino board
   - Upload the code to the board

4. **Run the Visualization Software**:
   - Install required Python libraries: `pip install matplotlib numpy pyserial`
   - Run `python Python/simple_lidar.py`
   - The software will automatically detect the connected LiDAR device and display the visualization

## Usage

Once everything is set up, the system will start collecting distance data and visualizing it in real-time. The visualization shows:

- Points detected by the LiDAR sensor within a 3-meter radius
- Current rotation speed (RPM) in the window title
- Reference circles at 1m and 2m distances

To exit the visualization, press Ctrl+C in the terminal.

## Data Format

The Arduino code sends data serially in the following format:
- RPM data: `R:<value>` (e.g., `R:20.5`)
- Distance data: `D:<value>` (e.g., `D:150`)

## Troubleshooting

- If the serial port cannot be detected automatically, check the available ports and modify the port name in the Python script
- Ensure the Arduino is properly connected and the code has been successfully uploaded
- Check all hardware connections if no data is being received

## License

This project is open-source and available for educational and personal use.

## Author

Yigit Salih Emecen
