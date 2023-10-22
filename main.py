from ultralytics import YOLO
import cv2
import math
import serial, time
import requests


# Start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Load YOLOv5s model
model = YOLO('./model_weights/best.pt')

# Object classes
classNames = ["Class A Fire", "Class B Fire", "Class C Fire", "Class D Fire", "Class K Fire"]

# Serial port
ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

# get ip address of the device
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

# get location of the device
def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "region": response.get("region"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
    }
    return location_data

location_info = get_location()
city = location_info.get("city")
latitude = location_info.get("latitude")
longitude = location_info.get("longitude")

# write to serial port
def write_read(x):
    ser.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = ser.readline()
    return data


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # send data to arduino
            if confidence >= 0.5:
                if cls == 0:
                    write_read('Class A Fire detected at {} latitude {} longitude {}'.format(city, latitude, longitude))
                elif cls == 1:
                    write_read('Class B Fire detected at {} latitude {} longitude {}'.format(city, latitude, longitude))
                elif cls == 2:
                    write_read('Class C Fire detected at {} latitude {} longitude {}'.format(city, latitude, longitude))
                elif cls == 3:
                    write_read('Class D Fire detected at {} latitude {} longitude {}'.format(city, latitude, longitude))
                elif cls == 4:
                    write_read('Class K Fire detected at {} latitude {} longitude {}'.format(city, latitude, longitude))
            else:
                write_read('No Fire detected')

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()