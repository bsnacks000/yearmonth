from yearmonth.yearmonth import date_to_ym
import pytest 
from yearmonth import YearMonth 
import yearmonth.yearmonth as ym

import datetime

def test_yearmonth_create_correctly_validates_string(): 

    ym = YearMonth.create('2021-01')
    assert ym.year == 2021 
    assert ym.month == 1 

    with pytest.raises(ValueError): 
        YearMonth.create('202020-01')
    
    with pytest.raises(ValueError): 
        YearMonth.create('afdsdf')

    with pytest.raises(ValueError): 
        YearMonth.create('2020-01-01')

    with pytest.raises(ValueError): 
        YearMonth.create('2020')


def test_yearmonth_create_correctly_validates_tuple(): 

    ym = YearMonth.create((2021, 1))
    assert ym.year == 2021 
    assert ym.month == 1

    ym = YearMonth.create(('2021','01'))

    assert ym.year == 2021 
    assert ym.month == 1

    with pytest.raises(ValueError): 
        YearMonth.create(('2020.0', '1.0'))


def test_yearmonth_create_raises_valueerror_on_invalid_year_and_month(): 

    
    with pytest.raises(ValueError): 
        YearMonth.create((2020, 13))
    
    with pytest.raises(ValueError): 
        YearMonth.create((2020, 0))
    
    with pytest.raises(ValueError): 
        YearMonth.create((2020, -1))
    
    with pytest.raises(ValueError): 
        YearMonth.create((0, 12))

def test_yearmonth_create_returns_clone_if_passed_yearmonth(): 

    ym = YearMonth(2021, 1)

    test = YearMonth.create(ym)

    assert test == ym 
    assert test is not ym

def test_yearmonth_comparisons(): 

    ym1 = YearMonth(2021, 1)
    ym2 = YearMonth(2022, 1)
    ym3 = YearMonth(2021, 1)

    assert ym1 < ym2 
    assert ym2 > ym1 
    assert ym1 == ym3 
    assert ym1 >= ym3 
    assert ym1 <= ym3 
    assert ym1 == ym3 
    assert ym1 != ym2 


def test_yearmonth_contains_returns_true_on_match(): 

    ym = YearMonth(2021, 1)

    d1 = datetime.date(2021, 1, 20)
    d2 = datetime.date(2022, 1, 20)

    assert d1 in ym
    assert d2 not in ym


def test_date_to_ym(): 
    d = datetime.date(2021, 1, 20)
    ym = date_to_ym(d)
    assert isinstance(ym, YearMonth)
    assert ym.year == 2021 
    assert ym.month == 1


def test_ndays_returns_correct_number_of_days(): 

    # this is tight wrap around monthrange so just check a couple
    assert ym.ndays(2021, 1) == 31 
    assert ym.ndays(2021, 2) == 28
    assert ym.ndays(2020, 2) == 29


def test_monthrange_yields_correct_range(): 

    s = datetime.date(2020, 1, 1)
    e = datetime.date(2021, 12, 1)

    mr = [d for d in ym.monthrange(s, e)] 

    assert len(mr) == 24

    assert mr[0] == datetime.date(2020,1,1)
    assert mr[-1] == datetime.date(2021,12,1)


def test_monthrange_yields_one_date_if_start_and_end_are_equal(): 

    s = datetime.date(2020, 1, 1)
    e = datetime.date(2020, 1, 1)

    mr = [d for d in ym.monthrange(s, e)] 
    assert len(mr) == 1 
    assert mr[0] == datetime.date(2020,1,1)


def test_yearmonth_rangefrom_calls_monthrange(mocker): 

    mock = mocker.patch('yearmonth.yearmonth.monthrange')

    ym = YearMonth(2021, 1)
    ym2 = YearMonth(2020, 1)

    ym.range_from(ym2)

    mock.assert_called_once_with(datetime.date(2020,1,1), datetime.date(2021,1,31))


def test_yearmonth_rangefrom_fails_if_initial_gt_instance(): 

    ym = YearMonth(2021, 1)
    ym2 = YearMonth(2020, 1)

    with pytest.raises(ValueError):
        ym2.range_from(ym)
