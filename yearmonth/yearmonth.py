from typing import Any, Dict, Generator, Tuple, Union, List
import datetime 
from dataclasses import dataclass
import calendar
import functools
import datetime

import re
_ym_re = re.compile(r'[0-9]{4}-[0-9]{2}')

YearMonthBoundary = Union[str, Tuple[int, int], Tuple[str, str], 'YearMonth']

@dataclass(eq=True, order=True)
class YearMonth(object):
    """A custom YearMonth type. 
    """
    year: int
    month: int 

    @classmethod
    def _parse_yearmonth_str(cls, v: 'YearMonth') -> Tuple[int, int]:
        if not _ym_re.match(v): 
            raise ValueError(f'str format not correct. Must be {_ym_re.pattern}')
        return (int(x) for x in v.split('-'))


    @classmethod 
    def _parse_yearmonth_tuple(cls, v: Tuple[Union[int, str], Union[int, str]]): 
        return (int(x) for x in v)    


    @classmethod 
    def _validate_ym(cls, year: int, month: int) -> None: 
        if year < 1 or month < 1 or month > 12:
            raise ValueError(f'{year}-{month} is out of range')


    @classmethod 
    def __get_validators__(cls): 
        yield cls.create 


    @classmethod 
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None: 
        field_schema.update(
            examples=['2021-01', (2021,1)], 
            description="ISO 8601 compliant reduced precision calendar date"
        )

    
    @classmethod 
    def create(cls, v: YearMonthBoundary) -> 'YearMonth':
        """A factory method that runs a set of validators before returning a YearMonth. 
        Will validate against 'YYYY-MM', ('YYYY', 'MM') or (int, int). If a YearMonth is passed to 
        this method will return a new instance of the object.  

        Args:
            v (YearMonthBoundary): A Union type of ISO string, 
                Tuple of either int or string that can be casted to an int or a YearMonth instance. 

        Returns:
            [type]: [description]
        """
        if isinstance(v, str): 
            year, month = cls._parse_yearmonth_str(v)
        elif isinstance(v, tuple):
            year, month = cls._parse_yearmonth_tuple(v)
        elif isinstance(v, YearMonth): 
            year, month = v.year, v.month 
        cls._validate_ym(year, month)
        return cls(year=year, month=month)  


    @functools.cached_property
    def ldom(self) -> int:
        """Get the last day of the month for this year.

        Returns:
            int: last day of month.
        """
        return ndays(self.year, self.month)


    def as_date(self, first: bool=True) -> datetime.date:
        """Convert this yearmonth to a datetime.date. If first is True (default).
        Will set `day` to the first of the month. Otherwise will set `day` to the last
        day of the month.

        Args:
            first (bool, optional): [description]. Defaults to True.

        Returns:
            datetime.date: [description]
        """
        if first:
            return datetime.date(self.year, self.month, 1)
        else:
            return datetime.date(self.year, self.month, self.ldom)        


    def range_from(self, initial: 'YearMonth') -> List['YearMonth']:
        """Create a range from the initial date to this YearMonth. 

        Raises:
            ValueError: If the initial YearMonth is gte this instance.

        Returns:
            List[YearMonth]: A List of YearMonth objects of the specified range.
        """
        if initial > self:
            raise ValueError('Initial YearMonth must be gte this instance to create a range.')
        start = initial.as_date() 
        end = self.as_date(first=False)
        return [date_to_ym(d) for d in monthrange(start, end)]


    def __contains__(self, d: datetime.date) -> bool:
        """Overrides the `in` operator to allow to check if a datetime.date object 
        falls within this YearMonth.

        Args:
            d (datetime.date): A datetime.date object.

        Returns:
            bool: Whether d is in this YearMonth.
        """
        if d.year == self.year and d.month == self.month: 
            return True 
        return False





def date_to_ym(d: datetime.date) -> YearMonth:
    """Convert a datetime.date to a YearMonth. Drops the day value.

    Args:
        d (datetime.date): A datetime.date object

    Returns:
        YearMonth: The converted YearMonth.
    """
    tt = d.timetuple()
    return YearMonth(tt.tm_year, tt.tm_mon)


def monthrange(start: datetime.date, end: datetime.date) -> Generator[datetime.date, None, None]: 
    """Given two arbitrary datetimes will yield datetimes at each month boundary.

    NOTE: based on based on https://stackoverflow.com/questions/35650793/python-get-all-months-in-range

    Args:
        start (datetime.date): [description]
        end (datetime.date): [description]

    Returns:
        [type]: [description]

    Yields:
        Generator[YearMonth, None, None]: [description]
    """

    assert end >= start, "end date must greater then or equal to start date"    
    s = datetime.date(start.year, start.month, 1)
    e = datetime.date(end.year, end.month, end.day)
    
    while s <= e:
        yield s
        s += datetime.timedelta(days=32)
        s = s.replace(day=1)




def ndays(year: int, month: int) -> int:
    """Wrapper around calendar.monthrange that returns only the days in the specified yearmonth.
    Args:
        year (int): The year
        month (int): The month
    Returns:
        int: The n days in the year-month
    """
    _, ndays = calendar.monthrange(year, month) 
    return ndays

