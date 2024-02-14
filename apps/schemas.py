from pydantic import BaseModel
from typing import Optional, Union

from datetime import datetime


class DealerBaseSchema(BaseModel):
    name: str
    address: str
    phone: str
    

class CarBaseSchema(BaseModel):
    name: str
    componentry: Optional[str] 
    year_release: Optional[int]
    price: float
    date_purchase: Optional[datetime]
    reg_no : str
    km_travelled: Optional[float]
    modelname: str
    dealer_id: int 

    class Config:
        from_attributes = True
        populate_by_name = True
    
    