from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from pydantic import BaseModel
import connection as connection
from sqlalchemy.orm import sessionmaker
import jwt
import datetime
from requests_cache import CachedSession
import cv2
import mediapipe as mp
import io
import numpy as np
from fastapi.responses import FileResponse

app = FastAPI()
# creating a seesion
cs = CachedSession(cache_name="caches", expire_after=300)

# JWT Secret key
SECRET_KEY = "signature"


# to generate tokens using jwt
def generateToken(data):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {"data": data, "exp": expiration}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# to decode jwt tokenized string
def decodeToken(str):
    try:
        payload = jwt.decode(str, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


class User(BaseModel):
    name: str


def get_session():
    sess = connection.Session()
    try:
        yield sess
    finally:
        sess.close()


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, sess: sessionmaker = Depends(get_session)):
    user_data = connection.User(**user.dict())
    user_data.name = generateToken(user_data.name)
    sess.add(user_data)
    sess.commit()


@app.get("/users/{id}", status_code=status.HTTP_200_OK)
async def get_user(id: int, sess: sessionmaker = Depends(get_session)):

    user = sess.query(connection.User).filter_by(id=id).one_or_none()
    if user:
        user.name= decodeToken(user.name)
        print(user.name)
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User with that id={id} not found")


@app.get("/users_search/", status_code=status.HTTP_200_OK)
async def get_user(st: str, sess: sessionmaker = Depends(get_session)):
    # st=generateToken(st).split('.')[1]
    users = sess.query(connection.User).filter(connection.User.name.like(f"%{st}%"))
    user_list={}
    if users:
        for user in users:
            # user.name=decodeToken(user.name)
            user_list[user.id]=user.name
        return user_list
    else:
        raise HTTPException(
            status_code=404, detail=f"User with that string={st} not found"
        )


@app.delete("/users/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id: int, sess: sessionmaker = Depends(get_session)):

    user = sess.query(connection.User).filter_by(id=id).one_or_none()
    if user:
        sess.delete(user)
        sess.commit()
    else:
        raise HTTPException(status_code=404, detail=f"User with that id={id} not found")


@app.put("/users/{id}", status_code=status.HTTP_200_OK)
async def update_user(id: int, userUp: User, sess: sessionmaker = Depends(get_session)):
    user = sess.query(connection.User).filter_by(id=id).one_or_none()
    if user:
        userUp.name = generateToken(userUp.name)
        user.name = userUp.name
        sess.commit() 
    else:
        raise HTTPException(status_code=404, detail=f"User with that id={id} not found")


# machine learning task
@app.post("/detect_face/", status_code=status.HTTP_201_CREATED)
async def create_user(image: UploadFile = File(...)):
    image_stream = io.BytesIO(await image.read())
    image_stream.seek(0)
    image_array = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    img = cv2.resize(img, (600, 600), interpolation=cv2.INTER_NEAREST)

    face = mp.solutions.face_detection
    draw = mp.solutions.drawing_utils
    with face.FaceDetection(
        model_selection=1, min_detection_confidence=0.6
    ) as face_detection:

        res = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        box = res.detections[0].location_data.relative_bounding_box
        x_min, y_min = int(box.xmin * img.shape[1]), int(box.ymin * img.shape[0])
        x_max, y_max = int((box.xmin + box.width) * img.shape[1]), int(
            (box.ymin + box.height) * img.shape[0]
        )

        draw.draw_detection(img, res.detections[0])
        cropped_image = img[y_min:y_max, x_min:x_max]

        cv2.imwrite(
            r"C:\Users\pc\Desktop\test\api_project\cropped_image.jpg", cropped_image
        )
        return FileResponse(r"C:\Users\pc\Desktop\test\api_project\cropped_image.jpg")
