from datetime import date
from email.mime import image
from pydantic import BaseModel
from typing import Union
from fastapi import Form, Depends

class Connection(BaseModel):
    # uldid: int
    ipaddress:str= ""
    port:str = ""
    password:str = ""
    database:str = ""
    # def __init__(self, ipaddress: str = Form(...), port: int = Form(1),password:str = Form(2),database:str = Form(3)):
    #         # id = uuid4()
    #         super().__init__( ipaddress, port,password,database)

class BaseUlds(BaseModel):
    # uldid: int
    uldcode:str
    uldtype:str
    ulddesc:str
    uldlength:float
    uldwidth:float
    uldheight:float
    uldvolume:float
    uldtarewgt:float
    uldmasgrosswgt:float
    uldmaxload:float
    uldpos:str
    uldimage:str
    reducedlength:float
    reducedwidth:float
    reducedheight:float
    contouraxis:str
    segments:str
    isactive:str 

class BaseAircraft(BaseModel):
    # aircraftid : int
    manufacturername:str
    modelnumber:str

class BaseAirline(BaseModel):
    # uldid: int
    airlinecode :str
    airlinename:str

class BaseAirlineAircraftMapping(BaseModel):
    # mappingid: int
    airlinecode:str
    aircraftid :str

class BaseAirlineAircraftUldMapping(BaseModel):
    # id : str
    mappingid :str
    uldid :str