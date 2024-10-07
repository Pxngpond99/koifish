from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from fastapi.responses import StreamingResponse
import requests
import mongoengine as me
import logging
import cv2
import redis
import time
import pandas
import json, numpy, base64
from PIL import Image
from io import BytesIO
from requests.auth import HTTPDigestAuth
from koifish.api.core import deps
from .schemas import StartRedis, DataRedis
from ..accounts.models import User
from koifish.api.redis_rq import redis_queue
from koifish.api.utils import video_utils
from koifish.api.core.app import get_app_settings

router = APIRouter(tags=["koifish"], prefix="/koifish")


# @router.get(
#     "/image/{step}",
#     responses={
#         200: {
#             "content": {
#                 "application/octet-stream": {
#                     "schema": {"type": "string", "format": "binary"}
#                 }
#             }
#         }
#     },
#     response_class=StreamingResponse,
# )
# def get_image(step: int):
#     url = "http://172.30.9.139/ISAPI/Streaming/channels/101/picture"
#     username = "coe"
#     password = "zxcASDqwe"

#     # Attempt using Digest Authentication
#     response = requests.get(url, auth=HTTPDigestAuth(username, password))

#     # Check if the request was successful
#     if response.status_code == 200:
#         # Convert response content (binary) to a BytesIO stream
#         image_stream = BytesIO(response.content)

#         # Return the image as a streaming response
#         return StreamingResponse(image_stream, media_type="image/jpeg")
#     else:
#         return {
#             "error": f"Failed to retrieve image. Status code: {response.status_code}"
#         }


@router.get(
    "/{step}/image",
    responses={
        200: {
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        }
    },
    response_class=FileResponse,
)
def get_koi_image(
    step: int,
    # current_user: User = Depends(deps.get_current_user),
):
    r = redis.Redis(host="localhost", port=6379, db=0)
    key = "koifish"

    # Retrieve and decode the dictionary from Redis
    dict_str = r.get(key)
    my_all_dict = json.loads(dict_str)

    # Extract the base64-encoded image for the given step
    encoded_image = my_all_dict["step_all"][-1]["image"]
    img_data = base64.b64decode(encoded_image)

    # Convert the image data to a NumPy array and decode it as an image
    nparr = numpy.frombuffer(img_data, numpy.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Encode the image back to JPEG (or any format) to send as a response
    ret, img_encoded = cv2.imencode(".jpg", frame)  # Encoding the image in JPEG format

    if not ret:
        return Response(status_code=500, content="Error encoding image")

    # Send the encoded image as a binary response
    return Response(content=img_encoded.tobytes(), media_type="image/jpeg")


@router.get(
    "/{step}/image_scatter",
    responses={
        200: {
            "content": {
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        }
    },
    response_class=FileResponse,
)
def get_koi_image_scatter(
    step: int,
    # current_user: User = Depends(deps.get_current_user),
):
    r = redis.Redis(host="localhost", port=6379, db=0)
    key = "koifish"

    # Retrieve and decode the dictionary from Redis
    dict_str = r.get(key)
    my_all_dict = json.loads(dict_str)

    # Extract the base64-encoded image for the given step
    encoded_image = my_all_dict["step_all"][-1]["scatter_image"]
    img_data = base64.b64decode(encoded_image)

    # Convert the image data to a NumPy array and decode it as an image
    nparr = numpy.frombuffer(img_data, numpy.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Encode the image back to JPEG (or any format) to send as a response
    ret, img_encoded = cv2.imencode(".jpg", frame)  # Encoding the image in JPEG format

    if not ret:
        return Response(status_code=500, content="Error encoding image")

    # Send the encoded image as a binary response
    return Response(content=img_encoded.tobytes(), media_type="image/jpeg")


@router.get(
    "/get_lastest_data",
    response_model_by_alias=False,
    response_model=DataRedis,
)
def get_lastest_data(
    request: Request,
):

    r = redis.Redis(host="localhost", port=6379, db=0)
    key = "koifish"
    dict_str = r.get(key)
    my_all_dict = json.loads(dict_str)

    data_redis = DataRedis()
    averaged_A = []
    averaged_B = []
    averaged_C = []

    averaged_X = []
    averaged_Y = []

    all_x = []
    all_y = []
    for i in my_all_dict["step_all"]:
        averaged_A.append(sum(i["area_A"]))
        averaged_B.append(sum(i["area_B"]))
        averaged_C.append(sum(i["area_C"]))
        all_x = all_x + i["x"]
        all_y = all_y + i["y"]

    averaged_X = i["x"]
    averaged_Y = i["y"]
    fish_name = i["fish_name"]

    heatmap_data, xedges, yedges = numpy.histogram2d(
        all_x, all_y, bins=(1280 // 20, 960 // 20)
    )

    data_redis.averaged_A = averaged_A
    data_redis.averaged_B = averaged_B
    data_redis.averaged_C = averaged_C

    data_redis.averaged_X = []
    data_redis.averaged_Y = []
    data_redis.fish_name = fish_name
    
    heatmap_data = numpy.fliplr(heatmap_data)
    data_redis.heatmap_data = heatmap_data.T.tolist()
    data_redis.xedges = xedges.tolist()
    data_redis.yedges = yedges.tolist()

    data_redis.image = str(
        request.url_for("get_koi_image", step=my_all_dict["step_all"][-1]["step"])
    )
    data_redis.image_scatter = str(
        request.url_for("get_koi_image_scatter", step=my_all_dict["step_all"][-1]["step"])
    )
    return data_redis


@router.get(
    "/start_redis",
    response_model_by_alias=False,
    response_model=StartRedis,
)
def get_start():
    job = redis_queue.queue.enqueue(
        video_utils.calculate_video,
        job_id=f"calculate_video",
        args=("start", "end"),
        timeout=600,
        job_timeout=600,
    )
    start_redis = StartRedis()
    start_redis.name = f"start {job.id}"

    return start_redis
