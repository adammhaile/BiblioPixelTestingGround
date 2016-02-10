from PIL import ImageGrab
import numpy as np
import cv2

while True:
    img = ImageGrab.grab((0,0,640,480))
    img_np = np.array(img)
    print img_np.shape
    # frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("test", frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
