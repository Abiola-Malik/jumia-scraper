from pydantic import BaseModel
from .enums import ProductStatus
from datetime import datetime
from typing import Optional
from pydantic import Field

class Product(BaseModel):
    id: Optional[int] = None
    
    product_url: str
    name: str
    site: str = "jumia"
    
    current_price: float = Field(..., gt=0)          # price must be positive
    original_price: Optional[float] = None
    
    last_checked: Optional[datetime] = None
    status: ProductStatus = ProductStatus.ACTIVE
    
    # Optional extra fields
    image_url: Optional[str] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True   # Useful when loading from database
    