## Fire Detection system using YOLOv5, OpenCV, GSM, and Arduino

### Introduction

This project is a fire detection system that uses YOLOv5, OpenCV, GSM, and Arduino. The system is able to detect fire in real-time and send an SMS to the user. The system is also able to detect smoke and send an SMS to the relevant authorities i.e. Firefighting teams. Using an object detection model running on the device our system is able to identify fire and its class i.e. class A, B, C, D, and E and alert firefighting teams so that they are aware of the type of fire they are dealing with.

### Setup and Installation

1. Clone the repository
2. Create a virtual environment using `python -m venv venv`
3. Activate the virtual environment using `venv\Scripts\activate`
4. Install the dependencies using `pip install -r requirements.txt`
5. Change directory to `webhook` using `cd webhook`
6. Create a separate virtual environment for the webhook using `python -m venv venv` on a separate terminal
7. Activate the virtual environment using `venv\Scripts\activate`
8. Install the dependencies using `pip install -r requirements.txt`
9. Start the server by running `flask run`
10. Connect your SIM800L module to your Arduino.
11. Upload the `GSM_Stacuity.ino` file to your Arduino.
12. Change your terminal back to the main directory.
13. Run the `main.py` file using `python main.py`
