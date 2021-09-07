from typing import List
from yearmonth.yearmonth import YearMonth
import pydantic 


class MyModel(pydantic.BaseModel):
    ym: YearMonth 


def test_pydantic_validators(): 

    MyModel(ym=(2021, 1))
    MyModel(ym='2021-01')
    MyModel(ym=('2021', '01'))


def test_pydantic_schema(): 

    schema = MyModel.schema()

    check_examples = ['2021-01', (2021, 1)]
    check_string = 'ISO 8601 compliant reduced precision calendar date'

    assert check_examples == schema['properties']['ym']['examples']
    assert check_string == schema['properties']['ym']['description']


def test_pydantic_json(): 

    m = MyModel(ym='2021-01')
    assert m.json() == '{"ym": {"year": 2021, "month": 1}}'