import datetime


import io
import base64
import copy

import PIL

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, PackageLoader, select_autoescape, Template

import mongoengine as me
import logging
import cv2
import redis
import time
import pandas
import json


def calculate_video(start, end):
    print("START")

    # เชื่อม redis และสร้าง key
    r = redis.Redis(host="localhost", port=6379, db=0)
    key = "koifish"
    if not r.exists(key):
        initial_dict = {
            "step_all": [
                # {
                #     "step": 0,
                #     "x": [],
                #     "y": [],
                #     "radius": [],
                #     "area_A": [],
                #     "area_B": [],
                #     "area_C": [],
                #     "image": [],
                # }
            ],
        }
        r.set(key, json.dumps(initial_dict))

    # อ่านไฟล์
    df = pandas.read_csv(
        "koifish/modules/dashboard/data/20241002_modify.csv",
    )

    # อ่านวิดีโอ
    cap = cv2.VideoCapture("koifish/web/static/images/output_20241002.mp4")

    step = 0

    while cap.isOpened():
        ret, frame = cap.read()
        img = frame.copy()

        if not ret:
            print("video closed")
            break

        df_step = df[df["step"] == step]

        dict_str = r.get(key)
        my_all_dict = json.loads(dict_str)

        ret, buffer = cv2.imencode(".jpg", frame)

        encoded_image = base64.b64encode(buffer).decode("utf-8")

        try:
            my_all_dict["step_all"][-1]["image"] = ""
            my_all_dict["step_all"][-1]["scatter_image"] = ""
        except:
            pass

        my_dict = dict(
            step=0,
            x=[],
            y=[],
            radius=[],
            area_A=[],
            area_B=[],
            area_C=[],
            image="",
            fish_name=[],
            scatter_image=""
        )
        my_dict["step"] = step

        # save image ของ background ขณะนั้น ถ้าจะ ทำเป็น pyplot ต้องทำแล้ว encode ไว้แล้ว savem ลง redis คล้ายๆ แบบนี้
        my_dict["image"] = encoded_image


        for idx, row in df_step.iterrows():
            my_dict["x"].append(int(row["x"]))
            my_dict["y"].append(int(row["y"]))
            my_dict["radius"].append(int(row["radius"]))
            my_dict["area_A"].append(1 if str(row["Area"]) == "A" else 0)
            my_dict["area_B"].append(1 if str(row["Area"]) == "B" else 0)
            my_dict["area_C"].append(1 if str(row["Area"]) == "C" else 0)
            my_dict["fish_name"].append("Unknow" if int(row["fish_name"]) == -1  else ("No. " + str(row["fish_name"] + 1)))


            if row['Area'] == "A":
                color = (0, 0, 255)
            elif row['Area'] == "B":
                color = (0, 255, 255)
            else:
                color = (255, 0, 0)
            img = cv2.circle(img, (int(row["x"]), int(row["y"])), int(row['radius']) // 2, color, 3)

        img = cv2.line(img, (640, 0), (640, 960), (255, 0, 0), 5)

        img = cv2.line(img, (640, 480), (1280, 480), (0, 255, 0), 5)


        img = cv2.putText(img, f"A", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), cv2.LINE_AA)
        img = cv2.putText(img, f"B", (660, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), cv2.LINE_AA)
        img = cv2.putText(img, f"C", (660, 560), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), cv2.LINE_AA)

        ret2, buffer2 = cv2.imencode(".jpg", img)

        encoded_image2 = base64.b64encode(buffer2).decode("utf-8")

        my_dict['scatter_image'] = encoded_image2
        
        my_all_dict["step_all"].append(my_dict)
        r.set(key, json.dumps(my_all_dict))

        # cv2.imshow("test", frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
        print(f"STEP {step}")
        step += 1
        time.sleep(0.5)
