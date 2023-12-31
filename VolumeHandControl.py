import math
import keyboard
import cv2
import time
import numpy as np
import HandTrackingModule as htm

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
###################################
wCam, hCam = 980, 720
###################################

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=400
volPer=0
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2) // 2

        cv2.circle(img, (x1,y1), 15, (155,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (155,0,255), cv2.FILLED)

        cv2.line(img, (x1,y1), (x2,y2), (255,9,255), 3)
        cv2.circle(img, (cx, cy), 15, (155,0,255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)

        # hand range 35,220
        # volume range -24 -12

        vol = np.interp(length, [35,220], [minVol, maxVol])
        volBar = np.interp(length, [35,220], [400, 150])
        volPer = np.interp(length, [35,220], [0, 100])
        print(length, vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0,255,0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85,400), (0,255,0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85,400), (0,255,0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40,450), cv2.FONT_HERSHEY_TRIPLEX, 1, (0,250,0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)
    if keyboard.is_pressed('space'):
        break





