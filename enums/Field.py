from enum import Enum, auto

class Field(Enum):
    ORIGINAL_LOAN = auto()
    REMAINING_BALANCE = auto()
    MONTHS_LEFT = auto()
    NOMINAL_ANNUAL_INTEREST = auto() 
    ADJUSTED_ANNUAL_INTEREST = auto() 
    MARKET_NOMINAL_INTEREST = auto()  
    MARKET_ADJUSTED_INTEREST = auto() 
    CALCULATE = auto()
    RESULTS = auto()
    EXPLANATION = auto()