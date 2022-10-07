import codecs
import csv

from core import get_mongodb
from fastapi import APIRouter, Depends, File, UploadFile

# from fastapi import APIRouter, Body, Depends, File, UploadFile, status
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from models import StudentModel

router = APIRouter(
    prefix="/mgdb",
    tags=["mgdb"],
    dependencies=[Depends(get_mongodb)],
    responses={404: {"description": "API Not found"}},
)


@router.post("/upload")
def upload(file: UploadFile = File(...)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, "utf-8"))
    data = {}
    for rows in csvReader:
        key = rows["Id"]  # Assuming a column named 'Id' to be the primary key
        data[key] = rows

    file.file.close()
    return data


# @router.post("/", response_description="Add new student", response_model=StudentModel)
# async def create_student(student: StudentModel = Body(...)):
#     db = get_mongodb("students")
#     student = jsonable_encoder(student)
#     new_student = await db["students"].insert_one(student)
#     created_student = await db["students"].find_one({"_id": new_student.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)
