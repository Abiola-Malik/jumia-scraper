from enum import Enum

class ProductStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    OUT_OF_STOCK = "out_of_stock"
    ERROR = "error"
    
