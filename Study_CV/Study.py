
import numpy
import cv2


cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    # Включаем первую камеру


    # "Прогреваем" камеру, чтобы снимок не был тёмным
    '''
    for i in range(30):
        cap.read()
    '''
    while True:
        # Делаем снимок
        flag, img = cap.read()

    # Записываем в файл
    #cv2.imwrite('cam.png', frame)

        low_blue = numpy.array((16,60,60), numpy.uint8)
        high_blue = numpy.array((34,255,255), numpy.uint8)
        try:
            #создание маски
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask_blue = cv2.inRange(img_hsv, low_blue, high_blue)
            #накладываем на изображение
            result = cv2.bitwise_and(img_hsv,img_hsv,mask=mask_blue)
            result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

            moments = cv2.moments(mask_blue,1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']
            if dArea > 150:
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                #-1 в конце закрашенный кружок
                cv2.circle(img, (x,y), 10, (0,250,0), -1)

            cv2.imshow('Camera',  img)
            cv2.imshow('Mask',  result)
        except:
            cap.release()
            raise
        ch = cv2.waitKey(30)

        if ch == 27:
            break

# Отключаем камеру
cap.release()
cv2.destroyAllWindows()





