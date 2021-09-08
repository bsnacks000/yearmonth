# yearmonth 

A simple ISO8601 compliant dataclass type that is interoperable with `pydantic`. 


Example usage: 
```python

from yearmonth import YearMonth

ym = YearMonth(2021, 1)  
ym1 = YearMonth(2022, 1)

# validators
validated_ym = YearMonth.create((2021, 1))
from_iso_str = YearMonth.create('2021-01')

# YearMonth.create('not-right') >>> raises ValueError

# comparability
ym1 > ym  # True

# hashable 
d = { YearMonth(2021,1): 42 }

# use with pydantic
import pydantic 

class UseWithPydantic(pydantic.BaseModel): 
    
    ym : YearMonth

    @pydantic.validator('ym')
    def validate_ym(cls, v): 
        if v.year == 2020:
            raise ValueError(':(')
        return v

```