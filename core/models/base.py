from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class credit_base(BaseModel):
    Buyer_business_VAT_ID: str
    Buyer_business_name: str
    Buyer_country: str

    class Config:
        orm_mode = True

class buyer_base(BaseModel):
    Buyer_business_VAT_ID: str
    Buyer_business_name: str = None
    Buyer_country: str = None
    Buyer_shipping_address: str = None
    Buyer_shipping_city: str = None
    Buyer_shipping_zip_code: str = None
    Buyer_email_address: str = None
    Buyer_phone_number: str = None

    class Config:
        orm_mode = True

class invoice(BaseModel):
    Buyer_business_VAT_ID: str
    Product_name: str = None
    Product_price: int = None
    Number_of_pieces: int = None
    Status: Optional[str]  = None
    Send_mail: bool

    class Config:
        orm_mode = True
