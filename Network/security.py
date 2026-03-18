from pydantic import BaseModel

class NoSecurity(BaseModel):
    wifiname: str

class LEAP(BaseModel):
    wifiname: str
    leapusername: str
    leappassword: str

class WpaPersonal(BaseModel):
    wifiname: str
    password: str

class WpaEnterpriseTLS(BaseModel):
    wifiname: str
    tlsid: str
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    nocacert: bool = False
    usercertpassword: str | None = None
    userPKpassword: str | None = None

class WpaEnterpriseLEAP(BaseModel):
    wifiname: str
    leapusername: str
    leappassword: str

class WpaEnterprisePWD(BaseModel):
    wifiname: str
    pwdusername: str
    pwdpassword: str

class WpaEnterpriseFAST(BaseModel):
    wifiname: str
    anonid: str | None = None
    pacprov: str | None = None
    innerauth: str | None = None
    username: str
    password: str

class WpaEnterpriseTTLS(BaseModel):
    wifiname: str 
    anonid: str | None = None
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    noncacert: bool = False
    innerauth: str | None = None
    username: str
    password: str

class WpaEnterprisePEAP(BaseModel):
    wifiname: str
    anonid: str | None = None
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    noncacert: bool = False
    innerauth: str | None = None
    username: str
    password: str

class Wpa3(BaseModel):
    wifiname: str
    password: str

class Eopen(BaseModel):
    wifiname: str