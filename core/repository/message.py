import sys
sys.path.append("../..")
sys.path.append("..")
from sqlalchemy.orm import Session
from core.models import table, base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import urllib
import os.path
import pycountry
from tempfile import NamedTemporaryFile
from InvoiceGenerator.pdf import SimpleInvoice
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
import random
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uuid
import re

env_path = Path('config/.env')
load_dotenv(dotenv_path=env_path)
Postgres_user = os.getenv("POSTGRES_USER")
Postgres_password = os.getenv("POSTGRES_PASSWORD")
Postgres_db = os.getenv("POSTGRES_DB")
host = os.getenv("host")
os.environ["INVOICE_LANG"] = "en"

cred = f"{Postgres_user}:{Postgres_password}@{host}/{Postgres_db}"
SQLALCHEMY_DATABASE_URL = f"postgresql://{cred}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False , bind=engine)

if "pytest" not in sys.modules:
    table.Base.metadata.create_all(bind=engine)

def upload_to_s3(Bucket_Name,Key,Filename):
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket= Bucket_Name)
    s3.Object(Bucket_Name,Key).upload_file(Filename=Filename)

def verify_email_identity(Buyer_email_address,region):
    ses_client = boto3.client("ses", region_name=region)
    response = ses_client.verify_email_identity(
        EmailAddress=Buyer_email_address
    )
    return response

def send_email_with_attachment(user_email,Buyer_email_address):
    msg = MIMEMultipart()
    msg["Subject"] = "This is an email with invoice attached!"
    msg["From"] = user_email
    msg["To"] = Buyer_email_address
    body = MIMEText("Order confirmed!, Attached is your Invoice", "plain")
    msg.attach(body)
    filename = "/tmp/document.pdf"
    with open(filename, "rb") as attachment:
        part = MIMEApplication(attachment.read())
        part.add_header("Content-Disposition",
                        "attachment",
                        filename=filename)
    msg.attach(part)
    ses_client = boto3.client("ses", region_name="us-west-2")
    response = ses_client.send_raw_email(
        Source=user_email,
        Destinations=[Buyer_email_address],
        RawMessage={"Data": msg.as_string()}
    )
    return response


def Buyer_credit(db: Session, message: base.credit_base):
    credit_score= random.randint(0,1000)
    obj = db.query(table.Buyer_credit).filter(table.Buyer_credit.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    if obj:
        result = "Your credit score is "+ str(obj.Buyer_credit_score)
        return result
    db_message = table.Buyer_credit(Buyer_business_VAT_ID =message.Buyer_business_VAT_ID, Buyer_business_name= message.Buyer_business_name, Buyer_country=message.Buyer_country, Buyer_credit_score=credit_score)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    result = "Your credit score is "+ str(credit_score)
    return result 

def Register_buyer(db: Session, message: base.buyer_base):
    obj = db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    if obj:
        return None
    db_message = table.Buyer(Buyer_business_VAT_ID =message.Buyer_business_VAT_ID, Buyer_business_name = message.Buyer_business_name ,Buyer_country=message.Buyer_country,Buyer_shipping_address=message.Buyer_shipping_address, Buyer_shipping_city=message.Buyer_shipping_city,Buyer_shipping_zip_code=message.Buyer_shipping_zip_code,Buyer_email_address=message.Buyer_email_address,Buyer_phone_number=message.Buyer_phone_number)
    if not re.match(r"[^@]+@[^@]+\.[^@]+", message.Buyer_email_address):
        return JSONResponse(content={"detail":"enter correct email address"})
    if not pycountry.countries.get(name=message.Buyer_country):
        return JSONResponse(content={"detail":"enter correct country name"})
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def update_buyer(db: Session, message: base.buyer_base):
    obj=db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    if not obj:
        return None
    json_compatible_item_data = jsonable_encoder(message)
    if json_compatible_item_data["Buyer_business_name"] is not None:
        obj.Buyer_business_name = message.Buyer_business_name 
    if json_compatible_item_data["Buyer_country"] is not None:
        obj.Buyer_country=message.Buyer_country
    if json_compatible_item_data["Buyer_shipping_address"] is not None:
        obj.Buyer_shipping_address=message.Buyer_shipping_address
    if json_compatible_item_data["Buyer_shipping_city"] is not None:
        obj.Buyer_shipping_city=message.Buyer_shipping_city
    if json_compatible_item_data["Buyer_shipping_zip_code"] is not None:
        obj.Buyer_shipping_zip_code=message.Buyer_shipping_zip_code
    if json_compatible_item_data["Buyer_email_address"] is not None:
        obj.Buyer_email_address=message.Buyer_email_address
    if json_compatible_item_data["Buyer_phone_number"] is not None:
        obj.Buyer_phone_number=message.Buyer_phone_number
    db.commit()
    return JSONResponse(content={"detail":"Buyer's details updated"})

def get_buyer_details(db: Session, Buyer_business_VAT_ID: str):
    result = db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == Buyer_business_VAT_ID).first()
    if not result:
        return None
    return result

def delete_buyer(db: Session, Buyer_business_VAT_ID: str):
    result = db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == Buyer_business_VAT_ID).first()
    if not result:
        return None
    db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == Buyer_business_VAT_ID).delete()
    db.commit()
    return JSONResponse(content={"detail":"Buyer's details deleted"})

def generate_invoice(db: Session, message: base.invoice):
    obj = db.query(table.invoice).filter(table.invoice.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    if obj:
        return None
    obj2=db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    if not obj2:
        return JSONResponse(content={"detail":"Buyer's details not found, first onboard buyer"})
    client = Client(obj2.Buyer_business_name,address=obj2.Buyer_shipping_address, city=obj2.Buyer_shipping_city, zip_code=obj2.Buyer_shipping_zip_code, phone=obj2.Buyer_phone_number, email=obj2.Buyer_email_address, vat_id=obj2.Buyer_business_VAT_ID)
    provider = Provider('My company', bank_account='2600420569', bank_code='IFSC2010')
    Accountant = Creator('Ajitesh')
    invoice = Invoice(client,provider, Accountant)
    country = pycountry.countries.get(name=obj2.Buyer_country)
    currency = pycountry.currencies.get(numeric=country.numeric)
    invoice.currency= currency.alpha_3
    invoice.number=uuid.uuid4()
    invoice.currency_locale = 'en_US.UTF-8'
    invoice.add_item(Item(message.Number_of_pieces,message.Product_price,description=message.Product_name))
    pdf = SimpleInvoice(invoice)
    pdf_name="/tmp/invoice_"+message.Buyer_business_VAT_ID+".pdf"
    pdf.gen(pdf_name, generate_qr_code=True)
    if message.Send_mail==True:
        print("Mail sent")
    db_message = table.invoice(Buyer_business_VAT_ID=message.Buyer_business_VAT_ID, Product_name=message.Product_name, Product_price=message.Product_price ,Number_of_pieces=message.Number_of_pieces, Status=message.Status)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_invoice(db: Session, Buyer_business_VAT_ID: str):
    result = db.query(table.invoice).filter(table.invoice.Buyer_business_VAT_ID == Buyer_business_VAT_ID).first()
    if not result:
        return None
    return result

def list_invoices(db: Session):
    obj= db.query(table.invoice).all()
    l=[]
    if obj is not None:
        for i in obj:
            obj2=db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == i.Buyer_business_VAT_ID).first()
            name="Buyer's Name not found"
            if obj2 is not None:
                name=obj2.Buyer_business_name
            l.append({"Buyer_business_VAT_ID": i.Buyer_business_VAT_ID , "Buyer_business_name": name,"Product_name": i.Product_name, "Product_price": i.Product_price ,"Number_of_pieces": i.Number_of_pieces, "Status": i.Status})
        return l
    else:
        return None

def update_invoice(db: Session, message: base.invoice):
    obj = db.query(table.invoice).filter(table.invoice.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    obj2=db.query(table.Buyer).filter(table.Buyer.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    if not obj:
        return None
    if not obj2:
        return JSONResponse(content={"detail":"Buyer's details not found, first onboard buyer"})
    json_compatible_item_data = jsonable_encoder(message)
    if json_compatible_item_data["Product_name"] is not None:
        obj.Product_name = message.Product_name 
    if json_compatible_item_data["Product_price"] is not None:
        obj.Product_price=message.Product_price
    if json_compatible_item_data["Number_of_pieces"] is not None:
        obj.Number_of_pieces=message.Number_of_pieces
    if json_compatible_item_data["Status"] is not None:
        obj.Status=message.Status
    db.commit()
    obj = db.query(table.invoice).filter(table.invoice.Buyer_business_VAT_ID == message.Buyer_business_VAT_ID).first()
    client = Client(obj2.Buyer_business_name,address=obj2.Buyer_shipping_address, city=obj2.Buyer_shipping_city, zip_code=obj2.Buyer_shipping_zip_code, phone=obj2.Buyer_phone_number, email=obj2.Buyer_email_address, vat_id=obj2.Buyer_business_VAT_ID)
    provider = Provider('My company', bank_account='2600420569', bank_code='IFSC2010')
    Accountant = Creator('Ajitesh')
    invoice = Invoice(client,provider, Accountant)
    country = pycountry.countries.get(name=obj2.Buyer_country)
    currency = pycountry.currencies.get(numeric=country.numeric)
    invoice.currency= currency.alpha_3
    invoice.number=uuid.uuid4()
    invoice.currency_locale = 'en_US.UTF-8'
    invoice.add_item(Item(obj.Number_of_pieces,obj.Product_price,description=obj.Product_name))
    pdf = SimpleInvoice(invoice)
    pdf_name="/tmp/invoice_"+obj.Buyer_business_VAT_ID+".pdf"
    pdf.gen(pdf_name, generate_qr_code=True)
    if message.Send_mail==True:
        print("Mail sent")
    return JSONResponse(content={"detail":"Invoice updated and sent"})