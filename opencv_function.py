import cv2
import numpy as np

class Opencv_Function():
    
    def videoCapture(self):
        cap = cv2.VideoCapture(1)
        cap.set(3, 640)
        cap.set(4, 480)

        return cap


    def find_Chess(self, img, contourimg): 
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Blue Red Yellow
        colorHSV = [[108, 0, 17, 115, 255, 156],
                    [0, 151, 128, 16, 255, 255],
                    [22, 145, 70, 29, 255, 241]]

        # Yellow
        y_lower = np.array(colorHSV[2][:3])
        y_upper = np.array(colorHSV[2][3:6])
        y_mask = cv2.inRange(hsv, y_lower, y_upper)


        # x座標的中心點
        y_point_center = self.find_Contour(y_mask, contourimg)



        # 用X座標判斷是在哪個位子    
        if y_point_center < 169 and y_point_center > 159:
            pos = 0
        elif y_point_center < 223 and y_point_center > 213:
            pos = 1
        elif y_point_center < 278 and y_point_center > 268:
            pos = 2
        elif y_point_center < 332 and y_point_center > 322:
            pos = 3
        elif y_point_center < 385 and y_point_center > 375:
            pos = 4
        elif y_point_center < 439 and y_point_center > 429:
            pos = 5
        elif y_point_center < 493 and y_point_center > 483:
            pos = 6
        else:
            pos = -2

        return pos

    def find_Contour(self, img, contourimg):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        x, y, w, h = -1, -1, -1, -1
        point_center = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # 讓棋子在適當距離才會被偵測
            if area < 1500:
                cv2.drawContours(contourimg, cnt, -1, (255, 0, 0), 4)
                peri = cv2.arcLength(cnt, True)
                vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)
                x, y, w, h = cv2.boundingRect(vertices)
                contour_point = [x, y, w, h]

                point_center = self.find_Contour_center(contourimg, peri, contour_point)

        return point_center


    def find_Contour_center(self, contourimg, peri, contour_point):
        radius = int((peri / 2) / np.pi)
        point_center = contour_point[0] + radius
        cv2.circle(contourimg, (contour_point[0] + radius, contour_point[1] + radius), 1, (255, 0, 0), cv2.FILLED)
        
        return point_center

    def prepare(self):
        key_bottom = 0
        while key_bottom == 0:
            p_bottom = int(input("開始遊戲請按1，結束按2: "))
            if p_bottom == 1:
                print("開始遊戲")
                cap = self.videoCapture()
                key_bottom = 1
                return p_bottom, cap
                
            elif p_bottom == 2:
                print("結束遊戲")
                break
            else:
                print("請輸入整數!")
                continue