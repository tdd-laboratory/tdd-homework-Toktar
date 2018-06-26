import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # unit test; prove that if we look for date, we find it.
    def test_dates_iso8601(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601,
                            '2015-07-25')

    # unit test; prove that if we look for date, we find it.
    def test_dates_fmt2(self):
        self.assert_extract('It happened on 2018-06-22 18:22:19.', library.dates_fmt2,
                            '2018-06-22 18:22:19')

    def test_dates_with_timestamps_with_milliseconds(self):
        self.assert_extract("It happened on 2018-06-22 18:22:19.123.",
                library.dates_iso8601, "2018-06-22 18:22:19.123")

    def test_dates_with_timestamps_with_seconds(self):
        self.assert_extract("It happened on 2018-06-22 18:22:19.",
                library.dates_iso8601, "2018-06-22 18:22:19")

    def test_dates_with_timestamps_with_minute(self):
        self.assert_extract("It happened on 2018-06-22 18:22.",
                library.dates_iso8601, "2018-06-22 18:22")

    def test_dates_with_timestamps_with_t_delimiter(self):
        self.assert_extract("It happened on 2018-06-22T18:22:19.123.",
                library.dates_iso8601, "2018-06-22T18:22:19.123")

    def test_dates_with_timestamps_with_offset(self):
        self.assert_extract("It happened on 2018-06-22T18:22:19.123-0800.",
                library.dates_iso8601, "2018-06-22T18:22:19.123")

    def test_dates_with_timestamps_with_MDT(self):
        self.assert_extract("It happened on 2018-06-22T18:22:19.123MDT.",
                library.dates_iso8601, "2018-06-22T18:22:19.123")

    def test_dates_with_timestamps_with_z(self):
        self.assert_extract("It happened on 2018-06-22T18:22:19.123Z.",
                library.dates_iso8601, "2018-06-22T18:22:19.123")

    def test_dates_with_comma_after_month(self):
        self.assert_extract("I was born on 25 Jul, 2015.",
                library.dates_fmt2, "25 Jul, 2015")

    def test_integers_separate_with_comma(self):
        self.assert_extract("Lost numbers: 4,8,15,16,23,42", library.integers,
                            '4', '8', '15', '16', '23', '42')
        
    # unit test; prove that if we look for dates where there are none, we get no results.
    def test_iso_dates_with_incorrect_month(self):
        self.assert_extract('I was born on 2015-14-25.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_day(self):
        self.assert_extract('I was born on 2015-07-40.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_day_and_month(self):
        self.assert_extract('I was born on 2015-14-40.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_hour(self):
        self.assert_extract('I was born on 2015-14-40 43:20.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_minute(self):
        self.assert_extract('I was born on 2015-14-40 11:90:10.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_second(self):
        self.assert_extract('I was born on 2015-14-40 11:10:90.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_separator(self):
        self.assert_extract('I was born on 2015-14-40A11:10:90.', library.dates_iso8601)

    def test_iso_dates_with_incorrect_offset(self):
        self.assert_extract('It happened on 2018-06-22T18:22:19.123-09000.', library.dates_iso8601)

    def test_fmt2_dates_with_incorrect_day(self):
        self.assert_extract('I was born on 40 Jan 2017.', library.dates_fmt2)

    def test_fmt2_dates_with_incorrect_month(self):
        self.assert_extract('I was born on 25 Jaan 2017.', library.dates_fmt2)

    def test_integer_with_incorrect_separator(self):
        self.assert_extract("Lost numbers: 48_15_16_23_42", library.integers)


if __name__ == '__main__':
    unittest.main()
