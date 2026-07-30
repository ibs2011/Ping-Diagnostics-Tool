                                            -#####-    W A R N I N G    -#####-: Please Read

"Ping Diagnostics v1.exe" may trigger warnings from antivirus software, such as Windows Security. It may be detected as:

Trojan/Wacatac.B!ml

Why do these alerts appear and prevent the download of this software?

This application is newly released and has little to no reputation or download history. It was compiled using PyInstaller, which can sometimes cause antivirus software to flag new executables.

The application:

Uses the Windows command line to retrieve ping data.
Analyses latency, averages, packet loss, and latency spikes.
Executes the built-in ping.exe utility and captures its output.

These detections are believed to be false positives. The complete source code is available in this repository for anyone who wishes to inspect it.

Thank you for your understanding.


----------------------------------------------------------------------------------

                                            -#####-    Ping Diagnostics Tool  -#####-: Please Read

A lightweight Python-based network diagnostics tool that measures and analyses network latency in real time.

Overview

Ping Diagnostics Tool is a command-line application designed to monitor the quality of a network connection by sending ICMP ping requests to a user-specified host. It collects latency data over time and provides useful statistics to help identify unstable connections, high latency, and packet loss.

This project was developed as a personal programming project to explore networking, data analysis, and Python application development.

Features
Test any IPv4 address or hostname (e.g. 1.1.1.1 or google.com)
Real-time latency monitoring
Current, minimum, maximum, and average ping
Packet loss detection
Latency spike detection (>100 ms)
Latency spike coverage analysis
Average latency of detected spikes
Spike interval calculations
Colour-coded terminal output
Standalone Windows executable included
Example Output

The application displays live network statistics including:

Current Ping
Maximum Ping
Minimum Ping
Average Ping
Packet Loss
Number of Latency Spikes
Spike Coverage
Spike Interval Analysis
Requirements
Running from source
Python 3.x
Running the executable

No Python installation is required. Simply download and run the executable included in the release.

How to Use
Launch the application.
Enter the host you wish to test.
The program will begin collecting ping data and updating the statistics in real time.

Example:

Enter host address to test (e.g. 1.1.1.1 or google.com):
Repository Contents
Ping-Diagnostics-Tool/
├── Ping Diagnostics.py
├── Colour.py
├── Ping Diagnostics.spec
├── Ping icon.ico
├── dist/
│   └── Ping Diagnostics.exe
└── README.md
