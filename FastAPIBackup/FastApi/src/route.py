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
from app import app

# app =FastAPI()
#credentials
psw = "postgres"
database = "planbooking_dev"
PDB_IP="192.168.18.32"
current_time = datetime.datetime.now()

 
# create an engine
pengine=""
try:
    pengine = db.create_engine('postgresql+psycopg2://postgres:' + psw +'@'+PDB_IP+':5437/' + database )
except Exception as e:
    print("Failed to Connect with the PlanbookingDB please check the FastAPI", str(e), flush=True)

# engine = db.create_engine("postgresql://postgres:postgres@planbooking-db:5437/planbooking_dev")

meta_data = db.MetaData(bind=pengine)
db.MetaData.reflect(meta_data)

tags_metadata = [
    {
        "name": "ulds",
        "description": "Ulds configurations",
    },
      {
        "name": "Aircraft",
        "description": "Aircraft configurations",
    },
      {
        "name": "Airline",
        "description": "Airline configurations",
    },
     {
        "name": "Airlineaircraftmapping",
        "description": "Airline Aircraft Mapping configurations",
    },
     {
        "name": "ULDS",
        "description": "Ulds configurations",
    },
]

#tables selection

aircraft= meta_data.tables['aircraft']
airline= meta_data.tables['airline']
airlineaircraftmapping= meta_data.tables['airlineaircraftmapping']
airlineaircraftuldmapping= meta_data.tables['airlineaircraftuldmapping']
ulds= meta_data.tables['ulds']



#AirCraft API's
@app.get("/aircraft",tags=['Aircraft'])
def get_aircraft_data():
    query="select * from aircraft "
    result = pengine.execute(query).fetchall()
    return result

@app.post("/aircraft",tags=['Aircraft'])
async def post_aircraft_data(baseAircraft:BaseAircraft):
    query = aircraft.insert().values(manufacturername=baseAircraft.manufacturername, 
                                            modelnumber=baseAircraft.modelnumber )
    pengine.execute(query)
    #getting the id of update
    query="SELECT MAX(aircraftid) from aircraft"
    new_id = pengine.execute(query).first()

    return {
        "status" : "SUCCESS",
        "id" : new_id[0]
    }

@app.put("/aircraft",tags=['Aircraft'])
async def update_aircraft_data(id,baseAircraft:BaseAircraft):
    query = update(aircraft)
    query= query.values({"aircraftid":id,"manufacturername": baseAircraft.manufacturername, 
                         "modelnumber":baseAircraft.modelnumber})
    query = query.where(aircraft.c.aircraftid == id)
    pengine.execute(query)
    # print(result)
    return "update successfully"

@app.delete("/aircraft",tags=['Aircraft'])
async def delete_aircraft_data(id):
    query=aircraft.delete().where(aircraft.c.aircraftid == id)
    query.execute()
    return str(id)+ " record is delete"

#aircraftFile
@app.post("/aircraftfile/",tags=["Aircraft"])
async def aircraft_upload_files(upload_file:UploadFile= File(...)):
    json_data =json.load(upload_file.file)
    for aircraft_data in  json_data.get('aircrafts'):
        query = aircraft.insert().values(manufacturername=aircraft_data.get('manufacturername'), 
                                            modelnumber=aircraft_data.get('modelnumber'))
        pengine.execute(query)
    query="SELECT MAX(aircraftid) from  aircraft "
    new_id = pengine.execute(query).first()
    return {
        "status" : "SUCCESS",
        "id" : new_id[0]
    }

    return {"data_in_file":json_data}


# API's airline
@app.get("/airline",tags=['Airline'])
def get_airline_data():
    query="select * from airline "
    result = pengine.execute(query).fetchall()
    return result

@app.post("/airline",tags=['Airline'])
async def post_airline_data(baseAirline:BaseAirline):
    query = airline.insert().values(airlinename=baseAirline.airlinename, 
                                             airlinecode=baseAirline.airlinecode )
    pengine.execute(query)

    return {
        "status" : "SUCCESS",
        "airlinecode" : baseAirline.airlinecode
    }

@app.put("/airline",tags=['Airline'])
async def update_airlines_data(baseAirline:BaseAirline):
    query = update(airline)
    query= query.values({"aircraftid":id,"airlinename":baseAirline.airlinename, 
                         "airlinecode":baseAirline.airlinecode})
    query = query.where(airline.c.airlinecode == baseAirline.airlinecode)
    pengine.execute(query)
    # print(result)
    return "update successfully"

@app.delete("/airline",tags=['Airline'])
async def delete_airline_data(airlinecode):
    query=airline.delete().where(airline.c.airlinecode == airlinecode)
    query.execute()
    return str(airlinecode)+ " record is delete"

#airlineFile
@app.post("/airlinefile/",tags=["Airline"])
async def airline_upload_files(upload_file:UploadFile= File(...)):
    json_data =json.load(upload_file.file)
    for airlines in  json_data.get('airlines'):
        query = airline.insert().values(airlinename=airlines.get("airlinename"), 
                                             airlinecode=airlines.get("airlinecode"))
        pengine.execute(query)
    query="SELECT MAX(uldid) from ulds "
    new_id = pengine.execute(query).first()
    return {
        "status" : "SUCCESS",
        "AirlineName" : airlines.get("airlinename")
    }



# API's airlineaircraftmapping
@app.get("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
def get_airlineaircraftmapping_data():
    query="select * from airlineaircraftmapping "
    result = pengine.execute(query).fetchall()
    return result


@app.post("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
async def post_aircraft_data(baseAirlineAircraftMapping:BaseAirlineAircraftMapping):
    query = airlineaircraftmapping.insert().values( airlinecode=baseAirlineAircraftMapping.airlinecode, 
                                             aircraftid=baseAirlineAircraftMapping.aircraftid )
    pengine.execute(query)
    #getting the id of update
    query="SELECT MAX(mappingid) from airlineaircraftmapping"
    new_id = pengine.execute(query).first()

    return {
        "status" : "SUCCESS",
        "id" : new_id[0]
    }

@app.put("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
async def update_airlines_data(mappingid,baseAirlineAircraftMapping:BaseAirlineAircraftMapping):
    query = update(airlineaircraftmapping)
    query= query.values({"mappingid":mappingid,"airlinecode":baseAirlineAircraftMapping.airlinecode, 
                                             "aircraftid":baseAirlineAircraftMapping.aircraftid })
    query = query.where(airlineaircraftmapping.c.mappingid == mappingid)
    pengine.execute(query)
    # print(result)
    return "update successfully"

@app.delete("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
async def delete_airline_data(mappingid):
    query=airlineaircraftmapping.delete().where(airlineaircraftmapping.c.mappingid == mappingid)
    query.execute()
    return str(mappingid)+ " record is delete"



# API's airlineaircraftuldmapping 
@app.get("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
def get_airlineaircraftuldmapping_data():
    query="select * from airlineaircraftuldmapping "
    result = pengine.execute(query).fetchall()
    return result

@app.post("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
async def post_airlineaircraftuldmapping_data(baseAirlineAircraftUldMapping: BaseAirlineAircraftUldMapping):
    query = airlineaircraftuldmapping.insert().values(mappingid=baseAirlineAircraftUldMapping.mappingid, 
                                            uldid=baseAirlineAircraftUldMapping.uldid )
    pengine.execute(query)

    #getting the id of update
    query="SELECT MAX(id) from airlineaircraftuldmapping"
    new_id = pengine.execute(query).first()

    return {
        "status" : "SUCCESS",
        "id" : new_id[0]
    }

@app.put("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
async def update_airlineaircraftuldmapping_data(id,baseAirlineAircraftUldMapping: BaseAirlineAircraftUldMapping):
    query = update(airlineaircraftuldmapping)
    query= query.values({"id":id,"mappingid":baseAirlineAircraftUldMapping.mappingid, 
                                            "uldid":baseAirlineAircraftUldMapping.uldid })
    query = query.where(airlineaircraftuldmapping.c.id == id)
    pengine.execute(query)
    # print(result)
    return "update successfully"


@app.delete("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
async def delete_airlineaircraftuldmapping_data(id):
    query=airlineaircraftuldmapping.delete().where(airlineaircraftuldmapping.c.id == id)
    query.execute()
    return str(id)+ " record is delete"



#uld configAPIs

@app.get("/ulds",tags=["ULDS"])
def get_ulds_data():
    query="select * from ulds "
    result = pengine.execute(query).fetchall()
    return result


@app.post("/ulds",tags=["ULDS"])
async def post_ulds_data( baseUlds:BaseUlds):
    query = ulds.insert().values( uldcode=baseUlds.uldcode, 
                                  uldtype=baseUlds.uldtype ,
                                  ulddesc=baseUlds.ulddesc,
                                  uldlength= baseUlds.uldlength,
                                  uldwidth= baseUlds.uldwidth,
                                  uldheight=baseUlds.uldheight,
                                  uldvolume=baseUlds.uldvolume,
                                  uldtarewgt= baseUlds.uldtarewgt,
                                  uldmasgrosswgt=baseUlds.uldmasgrosswgt,
                                  uldmaxload=baseUlds.uldmaxload,
                                  uldpos    = baseUlds.uldpos,
                                    # uldimage = baseUlds.uldimage,
                                  reducedlength =  baseUlds.reducedlength,
                                  reducedwidth =  baseUlds.reducedwidth,
                                  reducedheight =  baseUlds.reducedheight,
                                  isactive=baseUlds.isactive,
                                  createdt=current_time,
                                  lastupdatedt=current_time)
   
    result=pengine.execute(query)
    query="SELECT MAX(uldid) from ulds "
    new_id = pengine.execute(query).first()
    return {
        "status" : "SUCCESS",
        "id" : new_id[0]
    }

@app.delete("/ulds",tags=["ULDS"])
async def delete_ulds_data(id):
    query=ulds.delete().where(ulds.c.uldid == id)
    record=query.execute()
    return str(id)+ "record is delete"

@app.put("/ulds",tags=["ULDS"])
async def update_ulds_data(id,baseUlds:BaseUlds):
    print(id)
    print(type(baseUlds))
    print(baseUlds)
    query = update(ulds)
    query= query.values({"uldid":id,
                        "uldcode": baseUlds.uldcode,
                        "uldtype":baseUlds.uldtype , 
                        "ulddesc":baseUlds.ulddesc,
                        "uldlength": baseUlds.uldlength,
                        "uldwidth": baseUlds.uldwidth,
                        "uldheight":baseUlds.uldheight,
                        "uldvolume":baseUlds.uldvolume,
                        "uldtarewgt": baseUlds.uldtarewgt,
                        "uldmasgrosswgt":baseUlds.uldmasgrosswgt,
                        "uldmaxload":baseUlds.uldmaxload,
                        "uldpos": baseUlds.uldpos,
                        # uldimage = baseUlds.uldimage,
                        "reducedlength":baseUlds.reducedlength,
                        "reducedwidth":baseUlds.reducedwidth,
                        "reducedheight":baseUlds.reducedheight,
                        "isactive":baseUlds.isactive,
                        "createdt":current_time,
                        "lastupdatedt":current_time})

    query = query.where(ulds.c.uldid == id)
    pengine.execute(query)
    # print(result)
    return "update successfully"

#uldFile
@app.post("/uldfile/",tags=["ULDS"])
def uld_upload_files(upload_file:UploadFile= File(...)):
    json_data =json.load(upload_file.file)
    for uld in  json_data.get('bins'):
        query = ulds.insert().values({
                        "uldcode":   uld.get('uldCode'),
                        "uldtype":   uld.get('uldType') , 
                        "ulddesc":   uld.get('uldType'),
                        "uldlength": uld.get('length'),
                        "uldwidth":  uld.get('width'),
                        "uldheight": uld.get('height'),
                        "uldvolume": uld.get('volume'),
                        # "uldtarewgt": baseUlds.uldtarewgt,
                        # "uldmasgrosswgt":baseUlds.uldmasgrosswgt,
                        # "uldmaxload":baseUlds.uldmaxload,
                        # "uldpos": baseUlds.uldpos,
                        # # uldimage = baseUlds.uldimage,
                        # "reducedlength":baseUlds.reducedlength,
                        # "reducedwidth":baseUlds.reducedwidth,
                        # "reducedheight":baseUlds.reducedheight,
                        "isactive":"True",
                        "createdt":current_time,
                        "lastupdatedt":current_time})
        pengine.execute(query)
    query="SELECT MAX(uldid) from ulds "
    new_id = pengine.execute(query).first()
    return {
        "status" : "SUCCESS",
        "id" : new_id[0]
    }





if __name__ == "__main__":
    uvicorn.run(app,host='0.0.0.0',port=8000)