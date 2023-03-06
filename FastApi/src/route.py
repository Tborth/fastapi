from fastapi import FastAPI, Request,File,UploadFile,Depends
from fastapi.templating import Jinja2Templates
import sqlalchemy as db
from sqlalchemy import update 
from schema import BaseUlds,BaseAircraft,BaseAirline,BaseAirlineAircraftMapping,BaseAirlineAircraftUldMapping,Connection
from flask import render_template, request, redirect
from fastapi import APIRouter,Form, Depends
from main import *
routes = APIRouter()

templates = Jinja2Templates(directory="templates")
connected={}
select_airline={}
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

@routes.get("/")
def get_index_data():
    query="select * from ulds "
    test={}
    entries=[]
    
    return templates.TemplateResponse("content.html", { "request": {}})


@routes.post("/connect",response_model=Connection)
def post_connect_data(ipaddress: str = Form(...), port: int = Form(1),username:str = Form(2),password:str = Form(3),database:str = Form(4)):
    global connected
    connected={"ipaddress":ipaddress,"port":port,"database":database,"password":password,"username":username}
    
    test_connection=update_connection(ipaddress,port,password,database,username)
    if test_connection:
         return templates.TemplateResponse("connection_success.html", { "request": {},"connected": connected,"airlines":get_airline()})
    else:
        return templates.TemplateResponse("connection_failed.html", { "request": {}})
   
@routes.post("/addairline")
async def add_airline_data(airlinecode: str = Form(...), airlinename: str = Form(1),):
    # baseAirline=BaseAirline( airlinecode,airlinename)
    baseAirline={"airlinecode":airlinecode,"airlinename":airlinename}
    airline_post_query(baseAirline)
    global connected
    return templates.TemplateResponse("connection_success.html", 
                    { "request": {},"connected": connected,"airlines":get_airline()})
    return {
        "status"      : "SUCCESS",
        "airlinecode" :  airline_post_query(baseAirline)
    }

@routes.get("/updateAirline/{item_id}")
def update_airline_data(item_id: str):

    return templates.TemplateResponse("airlineUpdate.html", { "request": {},"airlinedata": get_airline_by_code(item_id)[0]})
    # if not id or id != 0:
    #     entry = Entry.query.get(id)
    #     f entry:


@routes.post("/updateAirline/{item_id}")
def update_airline_data(item_id: str,airlinecode: str = Form(...), airlinename: str = Form(1)):
    baseAirline=dict(airlinename=airlinename, 
                                             airlinecode=airlinecode)
    airline_put_query(item_id,baseAirline)
    # print(result)
    return templates.TemplateResponse("connection_success.html", { "request": {},"connected": connected,"airlines":get_airline()})

 
    # if not id or id != 0:
    #     entry = Entry.query.get(id)
    #     f entry:

@routes.get("/airlineDelete/{code}")
def airline_delete(code: str):
    airline_delete_query(code)
    return templates.TemplateResponse("connection_success.html", { "request": {},"connected": connected,"airlines":get_airline()})



@routes.get("/airlineaircraft/{code}")
def airline_aircraft_data(code: str):
    airline_aircraft_join(code)
    # return get_aircraft()
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]
    
    return templates.TemplateResponse("aircraft.html", { "request": {},"connected": connected,
                                                "airlines":get_airline(),
                                        "aircraft": airline_aircraft_join(code),"airlinedict":airline_dict,
                                        "activecode":code})



@routes.post("/addaircraft")
async def add_airline_data(aircraftname: str = Form(...), aircraftmodel: str = Form(1),aircraftairlines: str = Form(2)):
    aircraft_data={"manufacturername":aircraftname,"modelnumber":aircraftmodel}
    mapping_data={"airlinecode":aircraftairlines,"aircraftid":aircraft_post_query(aircraft_data)[0]}
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]

    return templates.TemplateResponse("aircraft.html", { "request": {},"connected": connected,
                                            "airlines":get_airline(),
                                        "aircraft": airline_aircraft_join(aircraftairlines),
                                        "airlinedict":airline_dict,"activecode":aircraftairlines})

    # baseAirline=BaseAirline( airlinecode,airlinename)
    # baseAirline={"airlinecode":airlinecode,"airlinename":airlinename}
    # airline_post_query(baseAirline)
    # global connected
    # return templates.TemplateResponse("connection_success.html", 
                    # { "request": {},"connected": connected,"airlines":get_airline()})

@routes.get("/updateAircraft/{item_id}/{code}")
def update_aircraft_data(item_id: str,code: str):

    get_aircraft_by_id(item_id)

    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]
    return templates.TemplateResponse("aircraftUpdate.html", { "request": {},"connected": connected,"activecode":code,
                                                "aircraftdata":  get_aircraft_by_id(item_id)[0],
                                                "airlinedict":airline_dict
                                                })

@routes.post("/updateAircraft/{item_id}/{code}")
def update_aircraft_data(item_id: str,code:str,aircraftname: str = Form(...),  aircraftmodel: str = Form(1)):
    get_aircraft_by_id(item_id)
    aircraft_data={"manufacturername":aircraftname, 
                         "modelnumber": aircraftmodel}
    aircraft_put_query(item_id, aircraft_data)                        
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]

    mapping_id=update_aircraft_airline_mapping(code,item_id)
    baseAirlineAircraftMapping={"airlinecode":aircraftmodel, "aircraftid":item_id}
    update_airlineaircraftmapping_query(mapping_id[0],baseAirlineAircraftMapping)

    return templates.TemplateResponse("aircraft.html", { "request": {},"connected": connected,"activecode":code,
                                                  "airlines":get_airline(),
                                                "aircraft":  airline_aircraft_join(code),
                                                "airlinedict":airline_dict
                                                })

@routes.get("/aircraftDelete/{item_id}/{code}")
def airline_delete(item_id: str,code: str):

    aircraft_delete_query(item_id)    
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]
    return templates.TemplateResponse("aircraft.html", { "request": {},"connected": connected,"activecode":code,
                                                  "airlines":get_airline(),
                                                "aircraft":  airline_aircraft_join(code),
                                                "airlinedict":airline_dict
                                                })


@routes.get("/aircraftulds/{item_id}/{code}")
def aircraft_ulds_data(item_id: str,code: str):
    airline_aircraft_join(code)
    airline_dict={}

    for al in get_airline():
        airline_dict[al[0]]=al[1]
    aircraft_dict={}
    for ac in airline_aircraft_join(code):
        keys=str(ac[1])+" "+str(ac[2])
        aircraft_dict[keys]=keys
    mapping_id=get_airline_aircraft_mappingid(code,item_id)[0]
    return templates.TemplateResponse("ulds.html", { "request": {},"connected": connected,
                                                "airlines":get_airline(),
                                        "aircraft": airline_aircraft_join(code),"airlinedict":airline_dict,
                                        "aircraftdict":aircraft_dict,
                                        "activecode":code,"ulds":get_ulds_ids_query(mapping_id),"activeaircraft":int(item_id)})

@routes.post("/addulds/{aircraftid}/{code}/")
async def add_airline_data(aircraftid:int,code: str,uldcode: str = Form(...),\
     uldtype: str = Form(1),ulddesc: str = Form(2),uldlength: str = Form(3),uldwidth: str = Form(4),\
     uldheight: str = Form(5),uldtarewgt:str=Form(6),segments:str=Form(7),aircraftairlines:str=Form(8)):
 
    ulds_data={"uldcode":uldcode, 
                                  "uldtype": uldtype ,
                                  "ulddesc":ulddesc,
                                  "uldlength":uldlength,
                                  "uldwidth":uldwidth,
                                  "uldheight":uldheight,
                                #   uldvolume=baseUlds.get("uldvolume"),
                                  "uldtarewgt": uldtarewgt,
                                  "uldmasgrosswgt":uldtarewgt,
                                #   "uldmaxload":baseUlds.get("uldmaxload"),
                                #   "uldpos"    = baseUlds.get("uldpos"),
                                #     # uldimage = baseUlds.uldimage,
                                #   "reducedlength": baseUlds.get("reducedlength"),
                                #   "reducedwidth" : baseUlds.get("reducedwidth"),
                                #   "reducedheight":  baseUlds.get("reducedheight"),
                                  "isactive":"Y"}
  

    aircraft_name=aircraftairlines.split(" ")
    # aircraftid=get_aircraft_id(aircraft_name[0],aircraft_name[1])
    uld_id=post_ulds_query(ulds_data)
  
    #add mapping ulds
    mapping_id=update_aircraft_airline_mapping(code,aircraftid )
    baseAirlineAircraftUldMapping=dict(mappingid=  mapping_id[0], uldid=uld_id[0])
    map_id=post_airlineaircraftuldmapping_query(baseAirlineAircraftUldMapping)
    #get airlline and aircraft data
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]
    aircraft_dict={}
    for ac in airline_aircraft_join(code):
        keys=str(ac[1])+" "+str(ac[2])
        aircraft_dict[keys]=keys

    return templates.TemplateResponse("ulds.html", { "request": {},"connected": connected,
                                                "airlines":get_airline(),
                                        "aircraft": airline_aircraft_join(code),"airlinedict":airline_dict,
                                         "activeaircraft":aircraftid,
                                        "aircraftdict":aircraft_dict,
                                        "activecode":code,"ulds":get_ulds_ids_query(mapping_id[0])})


@routes.get("/updateUlds/{item_id}/{aircraftid}/{code}")
def update_ulds_data(item_id: str,aircraftid:int,code: str):
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]
 
    aircraft_dict={}
    select_aircraft=[]
    for ac in airline_aircraft_join(code):
        keys=str(ac[1])+" "+str(ac[2])
        aircraft_dict[keys]=keys
        if ac[0] == aircraftid:
            select_aircraft.append(keys)

    return templates.TemplateResponse("uldsUpdate.html", { "request": {},"connected": connected,"activecode":code,
                                                "uldsdata":  get_ulds_by_id(item_id),
                                                "activeaircraft":aircraftid,
                                                "selectedaircraft":select_aircraft[0],
                                                "aircraftdict": aircraft_dict,
                                                "airlinedict":airline_dict
                                                })

@routes.post("/updateUlds/{item_id}/{aircraftid}/{code}")
def update_aircraft_data(item_id: str,aircraftid:int,code: str, uldcode: str = Form(...), uldtype: str = Form(1),ulddesc: str = Form(2),uldlength: str = Form(3),uldwidth: str = Form(4),uldheight: str = Form(5),uldtarewgt:str=Form(6),segments:str=Form(7),aircraftairlines:str=Form(8)):
    
    ulds_data={"uldcode":uldcode, 
                "uldtype": uldtype ,
                "ulddesc":ulddesc,
                "uldlength":uldlength,
                "uldwidth":uldwidth,
                "uldheight":uldheight,
            #   uldvolume=baseUlds.get("uldvolume"),
                "uldtarewgt": uldtarewgt,
                "uldmasgrosswgt":uldtarewgt,
            #   "uldmaxload":baseUlds.get("uldmaxload"),
            #   "uldpos"    = baseUlds.get("uldpos"),
            #     # uldimage = baseUlds.uldimage,
            #   "reducedlength": baseUlds.get("reducedlength"),
            #   "reducedwidth" : baseUlds.get("reducedwidth"),
            #   "reducedheight":  baseUlds.get("reducedheight"),
                "isactive":"Y"}
    update_ulds_query(item_id,ulds_data)
    
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]

    mapping_id=update_aircraft_airline_mapping(code,aircraftid)[0]
    
    aircraft_name=aircraftairlines.split(" ")
    updatedaircraftid=get_aircraft_id(aircraft_name[0],aircraft_name[1])
    new_mapping_id=update_aircraft_airline_mapping(code,updatedaircraftid[0])

    #get id of mapping aircrafanduld
    id=get_aircraft_uldsmapping_id(mapping_id,item_id)[0]
    #update mapping
    baseAirlineAircraftUldMapping={"mappingid":new_mapping_id[0],"uldid":item_id}
    update_airlineaircraftuldmapping_query(id,baseAirlineAircraftUldMapping)
    
    aircraft_dict={}
    for ac in airline_aircraft_join(code):
        keys=str(ac[1])+" "+str(ac[2])
        aircraft_dict[keys]=keys
    
    return templates.TemplateResponse("ulds.html", { "request": {},"connected": connected,
                                "airlines":get_airline(),
                                "aircraft": airline_aircraft_join(code),"airlinedict":airline_dict,
                                "aircraftdict":aircraft_dict,
                                "activecode":code,"ulds":get_ulds_ids_query(aircraftid),"activeaircraft":aircraftid})


@routes.get("/uldsDelete/{item_id}/{aircraftid}/{code}")
def ulds_delete(item_id: str,aircraftid:int,code: str):
    delete_ulds_query(item_id)
    
    airline_dict={}
    for al in get_airline():
        airline_dict[al[0]]=al[1]
    
    aircraft_dict={}
    for ac in airline_aircraft_join(code):
        keys=str(ac[1])+" "+str(ac[2])
        aircraft_dict[keys]=keys
    return templates.TemplateResponse("ulds.html", { "request": {},"connected": connected,
                                "airlines":get_airline(),
                                "aircraft": airline_aircraft_join(code),"airlinedict":airline_dict,
                                "aircraftdict":aircraft_dict,
                                "activecode":code,"ulds":get_ulds_ids_query(aircraftid),
                                "activeaircraft":aircraftid})



#AirCraft API's
@routes.get("/aircraft",tags=['Aircraft'])
def get_aircraft_data():
    return get_aircraft()

@routes.post("/aircraft",tags=['Aircraft'])
async def post_aircraft_data(baseAircraft:BaseAircraft):
    baseAircraft=dict(manufacturername=baseAircraft.manufacturername, 
                                            modelnumber=baseAircraft.modelnumber)
    return {
        "status" : "SUCCESS",
        "id" :  aircraft_post_query(baseAircraft)
    }

@routes.put("/aircraft",tags=['Aircraft'])
async def update_aircraft_data(id,baseAircraft:BaseAircraft):
    baseAircraft=dict(manufacturername= baseAircraft.manufacturername, 
                         modelnumber=baseAircraft.modelnumber)
    aircraft_put_query(baseAircraft)
    return aircraft_delete_query(id)


#aircraftFile
@routes.post("/aircraftfile/",tags=["Aircraft"])
async def aircraft_upload_files(upload_file:UploadFile= File(...)):
    return {
        "status" : "SUCCESS",
        "id"     :  aircraft_upload_query(upload_file)
    }



# API's airline
@routes.get("/airline",tags=['Airline'])
def get_airline_data():
    return get_airline()

@routes.post("/airline",tags=['Airline'])
async def post_airline_data(baseAirline:BaseAirline):
    baseAirline=dict(airlinename=baseAirline.airlinename, 
                                             airlinecode=baseAirline.airlinecode)
    return {
        "status"      : "SUCCESS",
        "airlinecode" :  airline_post_query(baseAirline)
    }

@routes.put("/airline",tags=['Airline'])
async def update_airlines_data(id,baseAirline:BaseAirline):
    baseAirline=dict(airlinename=baseAirline.airlinename, 
                                             airlinecode=baseAirline.airlinecode)
    # print(result)

    return airline_put_query(id,baseAirline)

@routes.delete("/airline",tags=['Airline'])
async def delete_airline_data(airlinecode):
    airline_delete_query(airlinecode)
    return str(airlinecode)+ " record is delete"

#airlineFile
@routes.post("/airlinefile/",tags=["Airline"])
async def airline_upload_files(upload_file:UploadFile= File(...)):
  
    return {
        "status" : "SUCCESS",
        "lastAirlineName" : airline_upload_query(upload_file)
    }




# API's airlineaircraftmapping
@routes.get("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
def get_airlineaircraftmapping_data():
    return get_airlineaircraftmapping_query()


@routes.post("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
async def post_airlineaircraftmapping_data(baseAirlineAircraftMapping:BaseAirlineAircraftMapping):
    baseAirlineAircraftMapping=dict(baseAirlineAircraftMapping.airlinecode, 
                                             aircraftid=baseAirlineAircraftMapping.aircraftid)
    return {
        "status" : "SUCCESS",
        "id" : post_airlineaircraftmapping_query(baseAirlineAircraftMapping)
    }

@routes.put("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
async def update_airlineaircraftmapping_data(mappingid,baseAirlineAircraftMapping:BaseAirlineAircraftMapping):
    baseAirlineAircraftMapping=dict(airlinecode=baseAirlineAircraftMapping.airlinecode, 
                                             aircraftid=baseAirlineAircraftMapping.aircraftid)
    return update_airlineaircraftmapping_query(mappingid,baseAirlineAircraftMapping)

@routes.delete("/airlineaircraftmapping",tags=['AirlineAircraftMapping'])
async def delete_airlineaircraftmapping_data(mappingid):
    return delete_airlineaircraftmapping_query(mappingid)




# API's airlineaircraftuldmapping 
@routes.get("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
def get_airlineaircraftuldmapping_data():
    return get_airlineaircraftuldmapping_query()

@routes.post("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
async def post_airlineaircraftuldmapping_data(baseAirlineAircraftUldMapping: BaseAirlineAircraftUldMapping):
    baseAirlineAircraftUldMapping=dict(mappingid=baseAirlineAircraftUldMapping.mappingid, 
                                            uldid=baseAirlineAircraftUldMapping.uldid)
    return {
        "status" : "SUCCESS",
        "id"     : post_airlineaircraftuldmapping_query(baseAirlineAircraftUldMapping)
    }

@routes.put("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
async def update_airlineaircraftuldmapping_data(id,baseAirlineAircraftUldMapping: BaseAirlineAircraftUldMapping):
    baseAirlineAircraftUldMapping={"mappingid":baseAirlineAircraftUldMapping.mappingid, 
                                            "uldid":baseAirlineAircraftUldMapping.uldid }
    return update_airlineaircraftuldmapping_query(id,baseAirlineAircraftUldMapping)


@routes.delete("/airlineaircraftuldmapping",tags=["AirlineAircraftUldMapping"])
async def delete_airlineaircraftuldmapping_data(id):
    return delete_airlineaircraftuldmapping_query(id)




#uld configAPIs
@routes.get("/ulds",tags=["ULDS"])
def get_ulds_data():
    return get_ulds_query()


@routes.post("/ulds",tags=["ULDS"])
async def post_ulds_data( baseUlds:BaseUlds):
    baseUlds=dict(uldcode=baseUlds.uldcode, 
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
    return {
        "status" : "SUCCESS",
        "id"     : post_ulds_query( baseUlds)
    }

@routes.delete("/ulds",tags=["ULDS"])
async def delete_ulds_data(id):
    return delete_ulds_query(id)

@routes.put("/ulds",tags=["ULDS"])
async def update_ulds_data(id,baseUlds:BaseUlds):
    baseUlds={"uldcode": baseUlds.uldcode,
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
                        "isactive":baseUlds.isactive}
    return update_ulds_query(id,baseUlds)

#uldFile
@routes.post("/uldfile/",tags=["ULDS"])
def uld_upload_files(upload_file:UploadFile= File(...)):
    return {
        "status" : "SUCCESS",
        "id"     : uld_upload_query(upload_file)
    }




