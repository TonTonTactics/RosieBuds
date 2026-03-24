from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated

class wifi(BaseModel):
    wifiname: str

class NoSecurity(wifi):
    type: Literal["open"]

class WpaPersonal(wifi):
    type: Literal["wpa_personal"]
    password: str

class Wpa3(wifi):
    type: Literal["wpa3personal"]
    password: str

class LEAP(wifi):
    type: Literal["leap"]
    username: str
    password: str

class WpaEnterpriseTTLS(wifi):
    type: Literal["wpa_enterprise_ttls"]
    username: str
    password: str
    anonid: str | None = None
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    noncacert: bool = False
    innerauth: str | None = None

class WpaEnterpriseTLS(wifi):
    type: Literal["wpa_enterprise_tls"]
    tlsid: str
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    nocacert: bool = False
    usercertpassword: str | None = None
    userPKpassword: str | None = None

class WpaEnterpriseLEAP(wifi):
    type: Literal["wpa_enterprise_leap"]
    leapusername: str
    leappassword: str

class WpaEnterprisePWD(wifi):
    type: Literal["wpa_enterprise_pwd"]
    pwdusername: str
    pwdpassword: str

class WpaEnterpriseFAST(wifi):
    type: Literal["wpa_enterprise_fast"]
    anonid: str | None = None
    pacprov: str | None = None
    innerauth: str | None = None
    username: str
    password: str

class WpaEnterprisePEAP(wifi):
    type: Literal["wpa_enterprise_peap"]
    username: str
    password: str
    anonid: str | None = None
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    noncacert: bool = False
    innerauth: str | None = None

class Eopen(wifi):
    type: Literal["eopen"]

WifiPayload = Annotated[
    Union[
        NoSecurity,
        LEAP,
        WpaPersonal,
        WpaEnterprisePEAP,
        WpaEnterpriseTTLS,
        WpaEnterpriseFAST,
        WpaEnterpriseTLS,
        WpaEnterpriseLEAP,
        WpaEnterprisePWD,
        Wpa3,
        Eopen
    ],
    Field(discriminator="type"),
    ]