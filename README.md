# DIY LiDAR System with ESP8266 Integration

A graduation project that implements a low-cost, DIY Light Detection and Ranging (LiDAR) system using Arduino, ESP8266, and Python. This system provides real-time 2D point cloud visualization of surroundings, making it suitable for robotics, mapping, and educational purposes.

## Project Overview

This project creates a homemade LiDAR system that combines:
- A TF-Luna distance sensor for accurate distance measurements
- A rotating platform driven by a DC motor for 360-degree scanning
- Hall effect sensor for precise rotation tracking
- ESP8266 for wireless data transmission
- Real-time visualization software in Python

The system can map environments within a 3-meter radius and transmits data wirelessly over UDP, making it suitable for mobile robotics applications.

## Repository Structure

```
Grad_Project/
├── 3D_models/               # 3D printable components
│   ├── Belt_Route_for_Head.stl  # Belt routing mechanism
│   ├── Bottom.stl               # Base component
│   ├── Case.stl                # Main enclosure
│   └── Spinning_Head.stl       # Rotating sensor mount
├── Arduino/                 # Microcontroller firmware
│   └── Read_Send/
│       └── Read_Send.ino   # Main Arduino code for sensor control
├── Python/                 # Visualization software
│   ├── esp8266.py         # UDP-based data visualization
│   └── backup/            # Backup of previous versions
└── Documents/             # Project documentation
    └── ENG402-Graduation_Project_Report_Yigit_Salih_Emecen.pdf
```

## Technical Specifications

### Hardware Components
- **Distance Sensor**: TF-Luna I2C LiDAR sensor
  - Range: 0.2m to 8m
  - Update Rate: 240Hz
  - Interface: I2C
- **Motion System**:
  - DC Motor with PWM control
  - Hall effect sensor for rotation tracking
  - Maximum RPM: ~600 (limited by debounce)
- **Communication**:
  - ESP8266 for wireless data transmission
  - UDP protocol for real-time data streaming
- **Physical Build**:
  - 3D printed components for durability
  - Belt-driven rotation system
  - Compact case design

### Software Features
- **Arduino Firmware**:
  - High-speed I2C communication (240Hz)
  - Precise RPM calculation
  - Debounced hall effect sensing
  - Configurable motor speed via PWM
  
- **Python Visualization**:
  - Real-time point cloud display
  - UDP socket communication
  - Dynamic plot updates
  - Configurable display parameters
  - Point history tracking (up to 200 points)

## Setup Instructions

### Hardware Assembly
1. **3D Printing**:
   - Print all STL files from the `3D_models` directory
   - Recommended settings:
     - Layer height: 0.2mm
     - Infill: 20% minimum
     - Support: Required for overhangs

2. **Component Assembly**:
   - Mount the TF-Luna sensor on the `Spinning_Head`
   - Install the hall effect sensor on the `Bottom` component
   - Route the timing belt using the `Belt_Route_for_Head`
   - Enclose electronics in the `Case`

3. **Wiring**:
   ```
   Arduino:
   - Hall Sensor → Pin 2
   - Motor Pin 1 → Pin 9 (PWM)
   - Motor Pin 2 → Pin 10
   - TF-Luna:
     - SDA → Arduino SDA
     - SCL → Arduino SCL
   ```

### Software Setup

1. **Arduino Environment**:
   ```bash
   # Required Libraries
   - Wire (built-in)
   - TFLI2C (TF-Luna I2C Library)
   ```

2. **Python Environment**:
   ```bash
   # Install required packages
   pip install numpy matplotlib socket
   ```

3. **Configuration**:
   - Set UDP_PORT in `esp8266.py` (default: 12345)
   - Adjust MAX_POINTS for visualization (default: 200)
   - Motor speed can be modified in Arduino code (PWM value)

## Usage

1. **Start the System**:
   ```bash
   # Run the visualization software
   python Python/esp8266.py
   ```

2. **Data Format**:
   The system transmits UDP packets containing:
   - Distance data: "D: [value]"
   - Angle data: "A: [value]"
   - Each measurement includes both distance (mm) and angle (degrees)

3. **Visualization**:
   - Blue dots represent detected points
   - Grid shows distance in millimeters
   - Real-time updates at up to 240Hz
   - Points persist based on MAX_POINTS setting

## Performance Optimization

- **Scan Rate**: Adjustable via motor PWM (pin 9)
- **Update Rate**: Configurable TF-Luna frame rate (default 240Hz)
- **Point Density**: Modify MAX_POINTS in Python code
- **Debounce Time**: Adjustable in Arduino code (affects maximum RPM)

## Troubleshooting

1. **No Data Reception**:
   - Check ESP8266 IP address and port configuration
   - Verify UDP_PORT matches in both devices
   - Ensure proper power supply to all components

2. **Irregular Scanning**:
   - Check belt tension
   - Verify hall sensor alignment
   - Adjust motor speed if needed

3. **Poor Point Cloud Quality**:
   - Clean sensor lens
   - Check for mechanical obstructions
   - Verify sensor mounting alignment

## Future Improvements

- 3D scanning capability by adding vertical motion
- Web-based visualization interface
- SLAM integration for mapping
- Point cloud data recording and playback

## Author

Yigit Salih Emecen

## License

This project is open-source and available for educational and personal use. See the project report for detailed technical information and methodology.
