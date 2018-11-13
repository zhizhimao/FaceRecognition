# -*- coding: utf-8 -*-
"""
创建时间： Sun Nov 11 12:04:00 2018
作者: 星空飘飘
平台：Anaconda 3-5.1.0
语言版本：Python 3.6.4
编辑器：Spyder 3.2.6
分析器：Pandas: 0.22.0
解析器：lxml: 4.1.1
数据库：MongoDB 2.6.12
程序名：facerecognition.py
"""

import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

obama_img = face_recognition.load_image_file("xk.jpg")  # 识别的照片
obama_face_encoding = face_recognition.face_encodings(obama_img)[0]
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
index = 0
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
#    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    if process_this_frame:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)
        face_names = []
        for face_encoding in face_encodings:
            match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
            if match[0]:
                name = "xk"
#                import os
#                os.system('rundll32.exe user32.dll,LockWorkStation')
#                video_capture.release()
#                cv2.destroyAllWindows()
#                break
            else:
                name = "unknown"
                index = index + 1
                cv2.imwrite(f'unknown{index}.jpg', frame)
            face_names.append(name)
    process_this_frame = not process_this_frame
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255),  2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left+12, bottom-12), font, 1.0, (255, 255, 255), 1)
#        cv2.putText(frame, name, (left+6, bottom-6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
