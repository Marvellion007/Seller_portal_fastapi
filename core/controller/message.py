import sys
sys.path.append("../..")
sys.path.append("..")
from typing import List
from fastapi import HTTPException, Depends, APIRouter
from core.service import message
from core.models import table, base
from pydantic import constr
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional


router = APIRouter()

def get_db():
    db = message.a
    try:
        yield db
    finally:
        db.close()        

@router.get("/credit_score/{Buyer_business_VAT_ID}/{Buyer_business_name}")
def Buyer_credit(Buyer_business_VAT_ID: str, Buyer_business_name: str,  Buyer_country: str, db: Session = Depends(get_db)):
    Message_obj = base.credit_base(Buyer_business_VAT_ID = Buyer_business_VAT_ID, Buyer_business_name = Buyer_business_name, Buyer_country = Buyer_country )
    result = message.Buyer_credit(db, Message_obj)
    return result

@router.post("/buyer/{Buyer_business_VAT_ID}/{Buyer_business_name}")
def Register_buyer(Buyer_business_VAT_ID: str, Buyer_business_name: str,Buyer_country: str,Buyer_shipping_address: str,Buyer_shipping_city: str,Buyer_shipping_zip_code: str,Buyer_email_address: str,Buyer_phone_number: str,db: Session = Depends(get_db)):
    Message_obj = base.buyer_base(Buyer_business_VAT_ID = Buyer_business_VAT_ID, Buyer_business_name = Buyer_business_name ,Buyer_country=Buyer_country,Buyer_shipping_address=Buyer_shipping_address,Buyer_shipping_city=Buyer_shipping_city,Buyer_shipping_zip_code=Buyer_shipping_zip_code,Buyer_email_address=Buyer_email_address,Buyer_phone_number=Buyer_phone_number)
    result = message.Register_buyer(db, Message_obj)
    if not result:
        raise HTTPException(status_code=400, detail="Buyer already registered")
    return result

@router.patch("/buyer/{Buyer_business_VAT_ID}")
def Update_buyer(Buyer_business_VAT_ID: str, Buyer_business_name: Optional[str] = None, Buyer_country: Optional[str] = None, Buyer_shipping_address: Optional[str] = None ,Buyer_shipping_city: Optional[str] = None, Buyer_shipping_zip_code: Optional[str] = None,Buyer_email_address: Optional[str] = None,Buyer_phone_number: Optional[str] = None,db: Session = Depends(get_db)):
    Message_obj = base.buyer_base(Buyer_business_VAT_ID = Buyer_business_VAT_ID, Buyer_business_name = Buyer_business_name ,Buyer_country=Buyer_country,Buyer_shipping_address=Buyer_shipping_address,Buyer_shipping_city=Buyer_shipping_city,Buyer_shipping_zip_code=Buyer_shipping_zip_code,Buyer_email_address=Buyer_email_address,Buyer_phone_number=Buyer_phone_number)
    result = message.update_buyer(db, Message_obj)
    if not result:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return result

@router.get("/buyer/{Buyer_business_VAT_ID}")
def Get_buyer_details(Buyer_business_VAT_ID: str, db: Session = Depends(get_db) ):
    result = message.get_buyer_details(db, Buyer_business_VAT_ID = Buyer_business_VAT_ID)
    if not result:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return result

@router.delete("/buyer/{Buyer_business_VAT_ID}")
def Delete_buyer(Buyer_business_VAT_ID: str, db: Session = Depends(get_db) ):
    result = message.delete_buyer(db, Buyer_business_VAT_ID = Buyer_business_VAT_ID)
    if not result:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return result

@router.post("/invoice/{Buyer_business_VAT_ID}/{Product_name}")
def Generate_invoice(Buyer_business_VAT_ID: str, Product_name: str, Product_price: int, Number_of_pieces: int, Send_mail: bool, Status:Optional[str] = None, db: Session = Depends(get_db)) :
    message_obj = base.invoice(Buyer_business_VAT_ID=Buyer_business_VAT_ID, Product_name=Product_name, Product_price=Product_price ,Number_of_pieces=Number_of_pieces, Status=Status, Send_mail=Send_mail)
    result = message.generate_invoice(db, message_obj)
    if not result:
        raise HTTPException(status_code=400, detail="Invoice already sent")
    return result

@router.get("/invoices")
def List_invoices(db: Session = Depends(get_db)) :
    result = message.list_invoices(db)
    if result is None:
        raise HTTPException(status_code=404, detail="No invoice generated yet")
    return result

@router.get("/invoices/{Buyer_business_VAT_ID}")
def Get_invoice(Buyer_business_VAT_ID: str, db: Session = Depends(get_db) ):
    result = message.get_invoice(db, Buyer_business_VAT_ID = Buyer_business_VAT_ID)
    if result is None:
        raise HTTPException(status_code=404, detail="No invoice generated yet")
    return result

@router.patch("/invoice/{Buyer_business_VAT_ID}")
def Update_invoice(Buyer_business_VAT_ID: str, Resend_mail: bool, Product_name: Optional[str] = None, Product_price: Optional[str] = None, Number_of_pieces: Optional[str] = None,Status:Optional[str] = None, db: Session = Depends(get_db)):
    message_obj = base.invoice(Buyer_business_VAT_ID=Buyer_business_VAT_ID, Product_name=Product_name, Product_price=Product_price ,Number_of_pieces=Number_of_pieces, Status=Status, Send_mail=Resend_mail)
    result = message.update_invoice(db, message_obj)
    if not result:
        raise HTTPException(status_code=404, detail="Invoice not present")
    return result

