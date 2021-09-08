# yearmonth 

A simple dataclass type that interfaces with pydantic.


Example usage: 
```python

from yearmonth import YearMonth

ym = YearMonth(2021, 1)  

validated_ym = YearMonth.create((2021, 1))
from_iso_str = YearMonth.create('2021-01')


# import pydantic 

class UseWithPydantic(pydantic.BaseModel): 
    
    ym : YearMonth

    @pydantic.validater('ym')
    def validate_ym(cls, v): 
        if v.year == 2020:
            raise ValueError('2020 sucks')
        return v

```