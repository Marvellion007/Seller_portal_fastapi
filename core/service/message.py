import sys
sys.path.append("../..")
sys.path.append("..")
from core.repository import message
from core.models import table, base

a=message.SessionLocal()

def Buyer_credit(db: message.Session, message_obj: base.credit_base):
    return message.Buyer_credit(db, message_obj)
    
def Register_buyer(db: message.Session, message_obj: base.buyer_base):
    result = message.Register_buyer(db, message_obj)
    return result

def update_buyer(db: message.Session, message_obj: base.buyer_base):
    result = message.update_buyer(db, message_obj)
    return result

def get_buyer_details(db: message.Session, Buyer_business_VAT_ID: str):
    result = message.get_buyer_details(db, Buyer_business_VAT_ID)
    return result

def delete_buyer(db: message.Session, Buyer_business_VAT_ID: str):
    result = message.delete_buyer(db, Buyer_business_VAT_ID = Buyer_business_VAT_ID)
    return result

def generate_invoice(db: message.Session, message_obj: base.invoice):
    return message.generate_invoice(db, message_obj)

def get_invoice(db: message.Session, Buyer_business_VAT_ID: str):
    result = message.get_invoice(db, Buyer_business_VAT_ID)
    return result

def list_invoices(db: message.Session):
    return message.list_invoices(db)

def update_invoice(db: message.Session, message_obj: base.invoice):
    return message.update_invoice(db, message_obj)