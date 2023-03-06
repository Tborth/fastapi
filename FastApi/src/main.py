from operator import and_
import sqlalchemy as db
from sqlalchemy import update ,select,text
from sqlalchemy.exc import SQLAlchemyError
from schema import BaseUlds,BaseAircraft,BaseAirline,BaseAirlineAircraftMapping,BaseAirlineAircraftUldMapping
import datetime
from fastapi import APIRouter
import json

routes = APIRouter()
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
PDB_IP = os.environ.get("PLANBOOKING_DB_IP")
#credentials
psw = "post"
database = "planbooking_dev"
PDB_IP="192.168.43.213"
current_time = datetime.datetime.now()

 
# create an engine
pengine=""
try:
    pengine = db.create_engine('postgresql+psycopg2://postgres:' + psw +'@'+PDB_IP+':5437/' + database )
    meta_data = db.MetaData(bind=pengine)
    db.MetaData.reflect(meta_data)

    aircraft= meta_data.tables.get('aircraft')
    airline= meta_data.tables.get('airline')
    airlineaircraftmapping= meta_data.tables.get('airlineaircraftmapping')
    airlineaircraftuldmapping= meta_data.tables.get('airlineaircraftuldmapping')
    ulds= meta_data.tables.get('ulds')
except SQLAlchemyError as e:
    print("Failed to Connect with the PlanbookingDB please check the FastAPI", str(e), flush=True)




def update_connection(ipaddress , port,password,database,username='postgres'):
    test_connection=False
    try:
        global pengine
        pengine = db.create_engine('postgresql+psycopg2://'+str(username)+':' + str(password) +'@'+str(ipaddress)+':'+ str(port)+'/' + str(database) )
        global meta_data
        meta_data = db.MetaData(bind=pengine)
        db.MetaData.reflect(meta_data)
        global airline
        global airlineaircraftmapping
        global aircraft
        global airlineaircraftuldmapping
        global ulds
        aircraft= meta_data.tables.get('aircraft')
        airline= meta_data.tables.get('airline')
        airlineaircraftmapping= meta_data.tables.get('airlineaircraftmapping')
        airlineaircraftuldmapping= meta_data.tables.get('airlineaircraftuldmapping')
        ulds= meta_data.tables.get('ulds')
        test_connection=True
    except SQLAlchemyError as e:
        print(e)
    return test_connection


#Get all the aircraft records
def get_aircraft():
    print("-------->>>>>>>>>>.--",pengine)
    query="select * from aircraft "
    return pengine.execute(query).fetchall()


def aircraft_post_query(baseAircraft):
    query = aircraft.insert().values(manufacturername=baseAircraft.get('manufacturername'), 
                                            modelnumber=baseAircraft.get('modelnumber'))
    pengine.execute(query)
    #getting the id of update
    query="SELECT MAX(aircraftid) from aircraft"
    new_id = pengine.execute(query).first()
    return new_id 

def aircraft_put_query(id,baseAircraft):
    query = update(aircraft)
    query= query.values({"aircraftid":id,"manufacturername": baseAircraft.get('manufacturername'), 
                         "modelnumber":baseAircraft.get('modelnumber')})
    query = query.where(aircraft.c.aircraftid == id)
    pengine.execute(query)


def aircraft_delete_query(id):
    query=aircraft.delete().where(aircraft.c.aircraftid == id)
    query.execute()
    return str(id)+" Aircraft Delete"

def aircraft_upload_query(upload_file):
    json_data =json.load(upload_file.file)
    for aircraft_data in  json_data.get('aircrafts'):
        query = aircraft.insert().values(manufacturername=aircraft_data.get('manufacturername'), 
                                            modelnumber=aircraft_data.get('modelnumber'))
        pengine.execute(query)
    query="SELECT MAX(aircraftid) from  aircraft "
    new_id = pengine.execute(query).first()
    return new_id

def get_airline_aircraft_mappingid(airlinecode,aircraftid):
    query =select(airlineaircraftmapping)
    query=query.where(and_( airlineaircraftmapping.c.airlinecode == airlinecode, airlineaircraftmapping.c.aircraftid == aircraftid))
    return pengine.execute(query).first()

#Get all the aircraft records
def get_airline():
    query="select * from airline "
    return pengine.execute(query).fetchall()

def airline_post_query(baseAirline):
    airline= meta_data.tables.get('airline')
    query = airline.insert().values(airlinename=baseAirline.get('airlinename'), 
                                             airlinecode=baseAirline.get('airlinecode') )
    pengine.execute(query)
  
    return baseAirline.get('airlinecode')

def airline_put_query(id,baseAirline):
    query = update(airline)
    query= query.values({"airlinename":baseAirline.get('airlinename'), 
                         "airlinecode":baseAirline.get('airlinecode')})
    query = query.where(airline.c.airlinecode == baseAirline.get('airlinecode'))
    pengine.execute(query)
    return str(id)+"Update successfully"

def get_airline_by_code(code):
    query =select(airline)
    q=query.where(airline.c.airlinecode == code)
    print(q)
    return pengine.execute(q).fetchall()

def get_aircraft_by_id(id):
    query =select(aircraft)
    q=query.where(aircraft.c.aircraftid == id)
    print(q)
    return pengine.execute(q).fetchall()

def get_aircraft_id(manufacturername,modelnumber):
    query =select(aircraft)
    query=query.where(and_(aircraft.c.manufacturername == manufacturername,aircraft.c.modelnumber == modelnumber))
    return pengine.execute(query).first()

def airline_delete_query(airlinecode):
    query=airline.delete().where(airline.c.airlinecode == airlinecode)
    query.execute()
    return  str(airlinecode)+ " record is delete"

def airline_aircraft_join(code):
    query =select(airlineaircraftmapping)
    query.join(airlineaircraftmapping,airline.c.airlinecode== airlineaircraftmapping.c.airlinecode)
    q=query.filter(airlineaircraftmapping.c.airlinecode == code)
    l_list=[]

    acs=pengine.execute(q).fetchall()
    for ac in acs:
        l_list.append(ac[2])

    query =select(aircraft)
    s = text('SELECT * FROM aircraft WHERE aircraftid IN :id_list')
    if len(l_list) >0:
        rs=pengine.execute(s, id_list=tuple(l_list)).fetchall()
        return rs
    else:
        return []
    

def airline_upload_query(upload_file):
    json_data =json.load(upload_file.file)
    airline_name=[]
    for airlines in  json_data.get('airlines'):
        query = airline.insert().values(airlinename=airlines.get("airlinename"), 
                                             airlinecode=airlines.get("airlinecode"))
        pengine.execute(query)
        airline_name.append(airlines.get("airlinename"))
    return airline_name
    
#Get the mapping of airlineaircraftmapping
def get_airlineaircraftmapping_query():
    query="select * from airlineaircraftmapping "
    return pengine.execute(query).fetchall()

def post_airlineaircraftmapping_query(baseAirlineAircraftMapping):
    query = airlineaircraftmapping.insert().values( airlinecode=baseAirlineAircraftMapping.get('airlinecode'), 
                                             aircraftid=baseAirlineAircraftMapping.get('aircraftid') )
    pengine.execute(query)
    #getting the id of update
    query="SELECT MAX(mappingid) from airlineaircraftmapping"
    new_id = pengine.execute(query).first()
    return new_id

def update_aircraft_airline_mapping(airlinecode,aircraftid ):
    query = select(airlineaircraftmapping)
    q=query.where(and_(airlineaircraftmapping.c.airlinecode == airlinecode , airlineaircraftmapping.c.aircraftid == aircraftid))
    return pengine.execute(q).first()

def update_airlineaircraftmapping_query(mappingid,baseAirlineAircraftMapping):
    query = update(airlineaircraftmapping)
    query= query.values({"mappingid":mappingid,"airlinecode":baseAirlineAircraftMapping.get('airlinecode'), 
                                             "aircraftid":baseAirlineAircraftMapping.get('aircraftid') })
    query = query.where(airlineaircraftmapping.c.mappingid == mappingid)
    pengine.execute(query)
    return str(mappingid)+" update successfully"

def delete_airlineaircraftmapping_query(mappingid):
    query=airlineaircraftmapping.delete().where(airlineaircraftmapping.c.mappingid == mappingid)
    query.execute()
    return str(mappingid) + " record is delete"


#Get the airlineAircraftUldMapping
def get_airlineaircraftuldmapping_query():
    query="select * from airlineaircraftuldmapping "
    return pengine.execute(query).fetchall()

# def get_airlinecode_by_aircraftid(id):

def post_airlineaircraftuldmapping_query(baseAirlineAircraftUldMapping):
    query = airlineaircraftuldmapping.insert().values(mappingid=baseAirlineAircraftUldMapping.get('mappingid'), 
                                            uldid=baseAirlineAircraftUldMapping.get('uldid') )
    pengine.execute(query)
    #getting the id of update
    query="SELECT MAX(id) from airlineaircraftuldmapping"
    new_id = pengine.execute(query).first()
    return new_id

def get_aircraft_uldsmapping_id(mapping_id,uld_id):
    query =select(airlineaircraftuldmapping)
    query=query.where(and_(airlineaircraftuldmapping.c.mappingid == mapping_id,airlineaircraftuldmapping.c.uldid == uld_id))
    return pengine.execute(query).first()

def update_airlineaircraftuldmapping_query(id,baseAirlineAircraftUldMapping):
    query = update(airlineaircraftuldmapping)
    query= query.values({"id":id,"mappingid":baseAirlineAircraftUldMapping.get('mappingid'), 
                                            "uldid":baseAirlineAircraftUldMapping.get('uldid') })
    query = query.where(airlineaircraftuldmapping.c.id == id)
    pengine.execute(query)
    return str(id) + " update successfully" 

def delete_airlineaircraftuldmapping_query(id):
    query=airlineaircraftuldmapping.delete().where(airlineaircraftuldmapping.c.id == id)
    query.execute()
    return str(id) +" record deleted"


def get_ulds_ids_query(id):
    query =select(airlineaircraftuldmapping)
    q=query.where(airlineaircraftuldmapping.c.mappingid == id)
    print(q)
    mapping_ids=pengine.execute(q).fetchall()
    ids_list=[]
    for mapping_id in mapping_ids:
        ids_list.append(mapping_id[2])
    s = text('SELECT * FROM ulds WHERE uldid IN :id_list')
    if len(ids_list) >0:
        ulds_data=pengine.execute(s, id_list=tuple(ids_list)).fetchall()
        return ulds_data
    else:
        return []


#GET ULDs data
def get_ulds_query():
    query="select * from ulds "
    return pengine.execute(query).fetchall()

def get_ulds_by_id(id):
    query =select(ulds)
    q=query.where(ulds.c.uldid == id)
    return pengine.execute(q).first()

def post_ulds_query( baseUlds):
    query = ulds.insert().values( uldcode=baseUlds.get("uldcode"), 
                                  uldtype=baseUlds.get("uldtype") ,
                                  ulddesc=baseUlds.get("ulddesc"),
                                  uldlength= baseUlds.get("uldlength"),
                                  uldwidth= baseUlds.get("uldwidth"),
                                  uldheight=baseUlds.get("uldheight"),
                                #   uldvolume=baseUlds.get("uldvolume"),
                                  uldtarewgt= baseUlds.get("uldtarewgt"),
                                  uldmasgrosswgt=baseUlds.get("uldmasgrosswgt"),
                                  uldmaxload=baseUlds.get("uldmaxload"),
                                  uldpos    = baseUlds.get("uldpos"),
                                    # uldimage = baseUlds.uldimage,
                                #   reducedlength =  baseUlds.get("reducedlength"),
                                #   reducedwidth =  baseUlds.get("reducedwidth"),
                                #   reducedheight =  baseUlds.get("reducedheight"),
                                  isactive=baseUlds.get("isactive"),
                                  createdt=current_time,
                                  lastupdatedt=current_time)
    
    pengine.execute(query)
    query="SELECT MAX(uldid) from ulds "
    new_id = pengine.execute(query).first()
    return new_id


def delete_ulds_query(id):
    query=ulds.delete().where(ulds.c.uldid == id)
    query.execute()
    return str(id) +" record deleted"

def update_ulds_query(id,baseUlds):
    query = update(ulds)
    query= query.values({"uldid":id,
                        "uldcode": baseUlds.get('uldcode'),
                        "uldtype":baseUlds.get('uldtype') , 
                        "ulddesc":baseUlds.get('ulddesc'),
                        "uldlength": baseUlds.get('uldlength'),
                        "uldwidth": baseUlds.get('uldwidth'),
                        "uldheight":baseUlds.get('uldheight'),
                        "uldvolume":baseUlds.get('uldvolume'),
                        # "uldtarewgt": baseUlds.get('uldtarewgt'),
                        # "uldmasgrosswgt":baseUlds.get('uldmasgrosswgt'),
                        # "uldmaxload":baseUlds.get('uldmaxload'),
                        # "uldpos": baseUlds.get('uldpos'),
                        # # uldimage = baseUlds.uldimage,
                        # "reducedlength":baseUlds.get('reducedlength'),
                        # "reducedwidth":baseUlds.get('reducedwidth'),
                        # "reducedheight":baseUlds.get('reducedheight'),
                        "isactive":baseUlds.get('isactive'),
                        "createdt":current_time,
                        "lastupdatedt":current_time})

    query = query.where(ulds.c.uldid == id)
    pengine.execute(query)
    return str(id) + " update successfully"

def uld_upload_query(upload_file):
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
    return new_id