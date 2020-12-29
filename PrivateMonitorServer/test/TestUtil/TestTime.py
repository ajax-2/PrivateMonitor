# coding: utf-8
from datetime import datetime
from src.tools.DateTools import DateTools


def test_date_format():
    dt = datetime.now()
    print DateTools.date_format(dt)


def test_str_format():
    s_time = "1982-02-5 12:25:32"
    dt = DateTools.str_format(s_time)
    print dt
    print type(dt)


def test_compute():
    dt = datetime.now()
    dt1 = DateTools.update_time(dt)
    assert dt.minute == dt1.minute
    dt2 = DateTools.update_time(dt, minutes=2)
    if dt.minute < 57:
        assert dt.minute == dt2.minute - 2
    else:
        assert dt.minute == dt2.minute + 60 - 2
    dt3 = DateTools.update_time(dt, minutes=2, add=False)
    if dt.minute > 2:
        assert dt.minute == dt3.minute + 2
    else:
        assert dt.minute == dt3.minute + 2 - 60


if __name__ == "__main__":
    # print "dt"
    # test_date_format()
    #
    # print "st"
    # test_str_format()
    test_compute()
