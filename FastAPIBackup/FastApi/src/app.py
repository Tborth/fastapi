
import uvicorn
# from flask_sqlalchemy import SQLAlchemy
from fastapi import FastAPI, Request,File,UploadFile
# import requests
# import psycopg2
import sqlalchemy as db
from sqlalchemy import update 
from schema import BaseUlds,BaseAircraft,BaseAirline,BaseAirlineAircraftMapping,BaseAirlineAircraftUldMapping
import datetime
import json
from mainlogic import *

app =FastAPI()
#credentials
psw = "postgres"
database = "planbooking_dev"
PDB_IP="192.168.18.32"
current_time = datetime.datetime.now()


if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)