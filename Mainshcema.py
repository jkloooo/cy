import datetime
import time
from typing import Type

from sqlalchemy import Column, String, Boolean, Integer, DATE, CHAR
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import IntegrityError

from BaseModels import EmployerBaseModel, HistoryBM, EmployerUpdate, Details, EmployerResponse
from Database.Maindatabase import base, engine
from sqlalchemy import ForeignKey
from time


def getAllEmployers_():
    with Session(engine) as session:
        return session.query(User).all()


class User(base):
    __tablename__ = 'users'
    name = Column(String(30), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(20), nullable=False, unique=True)
    gender = Column(CHAR)
    email = Column(String(100), nullable=False)
    isadmin = Column(Boolean)
    mobile = Column(String(8))
    history = relationship("History", back_populates="user")

    @classmethod
    def convertFromUserToBaseModel(cls, user):
        return EmployerResponse(
            name=user.name,
            gender=user.gender,
            email=user.email,
            mobile=user.mobile,
            uid=user.uid,
            id_emp=user.id,
            isadmin=user.isadmin
        )

    def __init__(self, mainStructure: EmployerBaseModel):
        self.name = mainStructure.name
        self.email = mainStructure.email
        self.isadmin = mainStructure.isadmin
        self.uid = mainStructure.uid
        self.mobile = mainStructure.mobile
        self.gender = mainStructure.gender

    def __str__(self):
        return f"Name {self.name}, UID {self.uid} "

    def __repr__(self):
        return f"Name {self.name}, UID {self.uid}"

    @classmethod
    def addEmployer(cls, new_employer):
        newUser = User(new_employer)
        isError = False
        with Session(engine) as session:
            session.add(newUser)
            try:
                session.commit()
            except IntegrityError as e:
                print(e)
                isError = True

        if isError:
            return None

        return cls.convertFromUserToBaseModel(cls._getUserByUID(new_employer.uid))

    @classmethod
    def _getUserByUID(cls, uid: str):

        with Session(engine) as session:
            return cls.convertFromUserToBaseModel(session.query(cls).filter(cls.uid == uid).first())

    @classmethod
    def getById(cls, id_: int):
        with Session(engine) as session:
            return cls.convertFromUserToBaseModel(session.query(cls).filter(cls.id == id_).first())

    # email, uid, tel

    @classmethod
    def getAllEmployers(cls):

        with Session(engine) as session:
            list_ = session.query(cls).all()

            new_list = list(map(cls.convertFromUserToBaseModel, list_))

            return new_list

    @classmethod
    def updateEmp(cls, emp: EmployerUpdate):
        if emp.email is None and emp.mobile is None and emp.uid is None:
            return None

        with Session(engine) as session:
            emp_ = session.query(cls).filter(cls.id == emp.id_).first()
            if emp_ is None:
                return None

            if emp.email:
                emp_.email = emp.email
            if emp.mobile:
                emp_.mobile = emp.mobile

            if emp.uid:
                emp_.uid = emp.uid

            session.commit()

            return cls.convertFromUserToBaseModel(cls.getById(emp.id_))

    @classmethod
    def deleteUser(cls, id_: int):
        with Session(engine) as session:
            emp = session.query(cls).filter(cls.id == id_).first()
            if emp is None:
                return None

            session.delete(emp)
            session.commit()

        return Details(message="Deleted Emp")


class History(base):
    __tablename__ = 'history'
    statut = Column(String(10), nullable=False)
    date = Column(DATE, nullable=False)
    id_history = Column(Integer, primary_key=True, autoincrement=True)
    id_employer = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="history")

    def __init__(self, hisbm: HistoryBM):
        self.date = hisbm.date
        self.statut = hisbm.statut
        self.id_employer = hisbm.id_emp_hist


  


    @classmethod
    def addHistory(cls, id_emp):
        statet = "retard" if time.localtime().tm_hour > 9 else "present"

        with Session(engine) as session:
            session.add(cls(HistoryBM(date = datetime.date.today(), statut = statet, id_emp_hist = id_emp)))

        return Details(message = "history added successfully")






if __name__ == '__main__':
    # base.metadata.create_all(engine)
    newE = EmployerBaseModel(
        name="si Essid",
        gender='m',
        email="helflo@go.com",
        isadmin=False,
        uid="201010",
        mobile="975815"
    )

    print(User.getAllEmployers())
