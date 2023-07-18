from sqlalchemy import Column, String, Integer, Date, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User_Registration_Form(Base):
    __tablename__ = "user_registration"

    name = Column("username", String(50), primary_key=True)
    fname = Column("firstname", String(100))
    lname = Column("lastname", String(100))
    date = Column("dob", Date)
    password = Column("pwd", VARCHAR)
    cpassword = Column("confirm_password", VARCHAR)
    mail = Column("email", VARCHAR)
    ph = Column("phone", Integer)
    add = Column("address", VARCHAR)
    category = Column("category", String)
    created_date = Column("created_datetime", Date)

