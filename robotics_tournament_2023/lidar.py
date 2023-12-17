from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')
import wiringpi

wiringpi.wiringPiSetup()  
wiringpi.pinMode(0, wiringpi.GPIO.OUTPUT)
wiringpi.digitalWrite(0,1)
info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

# for i, scan in enumerate(lidar.iter_scans()):
#     print('%d: Got %d measurments' % (i, len(scan)))
#     print (scan)
#     if i > 10:
#         break
iter = lidar.iter_scans()

def lidar_update(lidar):
    global iter
    distance = 5000
    for i, scan in enumerate(iter):
        if i > 1 : break
        for pt in scan:
            if pt[1] > 175 and pt[1] < 180:
                distance = pt[2]
                break
    return distance

print(lidar_update(lidar))
print(lidar_update(lidar))
print(lidar_update(lidar))
lidar.stop()
lidar.stop_motor()
lidar.disconnect()