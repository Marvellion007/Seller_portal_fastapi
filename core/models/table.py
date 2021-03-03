import sys
sys.path.append("../..")
sys.path.append("..")
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()


class Buyer_credit(Base):
    __tablename__ = "Buyer credit"

    Buyer_business_VAT_ID = Column(String, primary_key=True,index=False)
    Buyer_business_name = Column(String)
    Buyer_country = Column(String)
    Buyer_credit_score= Column(Integer)

class Buyer(Base):
    __tablename__ = "Buyer"

    Buyer_business_VAT_ID= Column(String, primary_key=True,index=False)
    Buyer_business_name = Column(String)
    Buyer_country = Column(String)
    Buyer_shipping_address = Column(String)
    Buyer_shipping_city = Column(String)
    Buyer_shipping_zip_code = Column(String)
    Buyer_email_address = Column(String)
    Buyer_phone_number = Column(String)

class invoice(Base):

    __tablename__ = "Invoice"

    Buyer_business_VAT_ID= Column(String,primary_key=True,index=False)
    Product_name= Column(String)
    Product_price= Column(Integer)
    Number_of_pieces= Column(Integer)
    Status= Column(String)