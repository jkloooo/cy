import datetime

from pydantic import BaseModel


class EmployerUpdate(BaseModel):
    id_: int
    email: str | None = None
    mobile: str | None = None
    uid: str | None = None


class EmployerBaseModel(BaseModel):
    """
    :arg name; gender;email;isadmin
    """
    name: str
    gender: str
    email: str
    mobile: str
    isadmin: bool | None = False
    uid: str


class EmployerResponse(EmployerBaseModel):
    id_emp: int


class HistoryBM(BaseModel):
    date: datetime.date
    statut: str
    id_emp_hist: int


class HistoryResponse(HistoryBM):
    id_hist: int


class Details(BaseModel):
    message: str
