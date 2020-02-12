import unittest
from datetime import datetime

import filters


class Test_Filters(unittest.TestCase):

    def test_date_only(self):
        """expects a datetime object """

        # too short
        self.assertEqual(filters.date_only('07/15/74'), '07/15/74')
        # wrong input type is just spat out
        self.assertEqual(filters.date_only('07/15/1974 22:14'), '07/15/1974 22:14')
        # accidentally passing time passes out time
        self.assertEqual(filters.date_only('12:20'), '12:20')
        # None returns None
        self.assertIsNone(filters.date_only(None))
        # empty string returns empty string
        self.assertEqual(filters.date_only(""), "")
        # wrong type is just passed out
        self.assertEqual(filters.date_only("MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM"),
                         "MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM")
        # full datetime object passed in, formatted string passed out
        self.assertEqual(filters.date_only(datetime(2020, 2, 2, 11, 16, 25, 730)), '02/02/2020')
        # datetime object with no timezone, formatted string passed out
        self.assertEqual(filters.date_only(datetime(2020, 6, 2, 11, 16, 25)), '06/02/2020')
        # datetime object witn no milliseconds, formatted string passed out
        self.assertEqual(filters.date_only(datetime(2020, 6, 2, 11, 16)), '06/02/2020')
        # datetime object witn no times, formatted string passed out
        self.assertEqual(filters.date_only(datetime(2020, 6, 2)), '06/02/2020')
        # wrong type returns itself
        self.assertEqual(filters.date_only(1), 1)

    def test_date_range(self):
        """expects a string 16 in length of this format: MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM"""

        # too short
        self.assertEqual(filters.date_range('07/15/74'), '07/15/74')
        # exact None passed in, None comes out
        self.assertIsNone(filters.date_range(None))
        # empty string returns empty string
        self.assertEqual(filters.date_range(""), "")
        # wrong format is just passed out
        self.assertEqual(filters.date_range("MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM"),
                         "MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM")
        #  range of one minute long passed out
        self.assertEqual(filters.date_range('07/15/1974 14:47 - 07/15/1974 14:48'),
                         '07/15/1974: <br>2:47 PM to 2:48 PM')
        #  multi day passed out, am pm, leading time 0 validation
        self.assertEqual(filters.date_range('07/15/1974 07:47 - 12/06/1974 22:48'),
                         '07/15/1974 7:47 AM<br>&nbsp;&nbsp;&nbsp;to<br>12/06/1974 10:48 PM')
        # wrong type returns itself
        self.assertEqual(filters.date_range(1), 1)

    def test_alt_icon(self):
        # numbers, dashes are removed, leading, trailing spaces trimmed and no double spaces, no file extension
        self.assertEqual(filters.icon_alt("002-football-field.svg"), "football field")
        # verify internal removal and file extension of 4 is removed
        self.assertEqual(filters.icon_alt("football 20-field.jpeg"), "football field")
        # verify  leading & trailing spaces removed
        self.assertEqual(filters.icon_alt(" football 20-field.jpeg "), "football field")
        # verify leading & trailing dash removed
        self.assertEqual(filters.icon_alt("-football 20-field.jpeg-"), "football field")
        # verify number before file extension is removed
        self.assertEqual(filters.icon_alt("football 20-field2.jpeg"), "football field")
        # verify dash before file extension is removed
        self.assertEqual(filters.icon_alt("football 20-field-.jpeg"), "football field")
        # verify space before file extension is removed
        self.assertEqual(filters.icon_alt("football 20-field .jpeg"), "football field")
        # verify tailing number on file extension is removed and combo before file extension is cleaned out
        self.assertEqual(filters.icon_alt("football 20-field- 2.jpeg2"), "football field")
        # try passing in something without a file extension
        self.assertEqual(filters.icon_alt("football"), "football")
        # try passing in wrong type int
        self.assertEqual(filters.icon_alt(1), 1)
        # try passing in None
        self.assertIsNone(filters.icon_alt(None))

    def test_myround(self):
        """extends existing round to only pass back desired decimals or none if whole number"""
        # get rounding down to one decimal
        self.assertTrue(filters.myround(1.445, 1), 1.4)
        # get rounding up to two decimals
        self.assertTrue(filters.myround(1.445, 2), 1.45)
        # no decimals because whole number
        self.assertTrue(filters.myround(1.00, 2), 1)
        # no decimals because whole number
        self.assertTrue(filters.myround(-1.00, 2), 1)
        # string get rounding down to one decimal
        self.assertIsNone(filters.myround('1.445', 1))
        # string get rounding up to two decimals
        self.assertIsNone(filters.myround('1.445', 2))
        # string no decimals because whole number
        self.assertIsNone(filters.myround('1.00', 2))
        # str negative fails int get rounding down to one decimal
        self.assertIsNone(filters.myround('-1.445', 1))
        # string get rounding up to two decimals
        self.assertIsNone(filters.myround('1.445', 2))
        # string no decimals because whole number
        self.assertIsNone(filters.myround('1.00', 2))
        # string no decimals because whole number
        self.assertIsNone(filters.myround('st', 2))
        # string fails
        self.assertIsNone(filters.myround('1', 2))

    def test_time_only(self):
        """expects a string 16 in length of this format: MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM"""

        # too short
        self.assertEqual(filters.time_only('07/15/74'), '07/15/74')
        # exact None passed in, None comes out
        self.assertIsNone(filters.time_only(None))
        # empty string returns empty string
        self.assertEqual(filters.time_only(""), "")
        # wrong format is just passed out
        self.assertEqual(filters.time_only("MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM"),
                         "MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM")
        #  range of one minute long passed out
        self.assertEqual(filters.time_only('07/15/1974 14:47 - 07/15/1974 14:48'), '2:47 PM to 2:48 PM')
        #  multi day passed out
        self.assertEqual(filters.time_only('07/15/1974 07:47 - 12/06/1974 22:48'),
                         '07/15/1974 07:47 - 12/06/1974 22:48')
        # time passed out with AM/PM/leading 0 removal
        self.assertEqual(filters.time_only('07/15/1974 07:47 - 07/15/1974 22:48'),
                         '7:47 AM to 10:48 PM')

        # wrong type returns itself
        self.assertEqual(filters.time_only(1), 1)


# allow the file to run without needing '-m unittest'
if __name__ == "__main__":
    unittest.main()
