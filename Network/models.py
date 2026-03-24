from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated


class WifiBase(BaseModel):
    wifiname: str


class NoSecurity(WifiBase):
    type: Literal["open"]


class WpaPersonal(WifiBase):
    type: Literal["wpa_personal"]
    password: str


class Wpa3(WifiBase):
    type: Literal["wpa3personal"]
    password: str


class LEAP(WifiBase):
    type: Literal["leap"]
    username: str
    password: str


class Eopen(WifiBase):
    type: Literal["eopen"]


class WpaEnterpriseTLS(WifiBase):
    type: Literal["wpa_enterprise_tls"]
    tlsid: str
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    nocacert: bool = False
    usercert: str | None = None
    usercertpassword: str | None = None
    userprivatekey: str | None = None
    userPKpassword: str | None = None


class WpaEnterpriseLEAP(WifiBase):
    type: Literal["wpa_enterprise_leap"]
    leapusername: str
    leappassword: str


class WpaEnterprisePWD(WifiBase):
    type: Literal["wpa_enterprise_pwd"]
    pwdusername: str
    pwdpassword: str


class WpaEnterpriseFAST(WifiBase):
    type: Literal["wpa_enterprise_fast"]
    username: str
    password: str
    anonid: str | None = None
    pacprov: str | None = None
    pacfile: str | None = None
    innerauth: str | None = None


class WpaEnterpriseTTLS(WifiBase):
    type: Literal["wpa_enterprise_ttls"]
    username: str
    password: str
    anonid: str | None = None
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    noncacert: bool = False
    innerauth: str | None = None


class WpaEnterprisePEAP(WifiBase):
    type: Literal["wpa_enterprise_peap"]
    username: str
    password: str
    anonid: str | None = None
    domain: str | None = None
    ca_cert: str | None = None
    cacertpassword: str | None = None
    noncacert: bool = False
    innerauth: str | None = None


WifiPayload = Annotated[
    Union[
        NoSecurity,
        WpaPersonal,
        Wpa3,
        LEAP,
        Eopen,
        WpaEnterpriseTLS,
        WpaEnterpriseLEAP,
        WpaEnterprisePWD,
        WpaEnterpriseFAST,
        WpaEnterpriseTTLS,
        WpaEnterprisePEAP,
    ],
    Field(discriminator="type"),
]