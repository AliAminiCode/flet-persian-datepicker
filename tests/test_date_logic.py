import jdatetime
import pytest

from persian_datepicker import PersianDatePicker


@pytest.fixture
def picker():
    return PersianDatePicker()


class TestGetMonthDays:
    def test_first_six_months_have_31_days(self, picker):
        for month in range(1, 7):
            assert picker.get_month_days(1403, month) == 31

    def test_months_seven_to_eleven_have_30_days(self, picker):
        for month in range(7, 12):
            assert picker.get_month_days(1403, month) == 30

    def test_esfand_has_30_days_in_leap_year(self, picker):
        # 1403 is a leap year in the Jalali calendar
        assert jdatetime.date(1403, 1, 1).isleap()
        assert picker.get_month_days(1403, 12) == 30

    def test_esfand_has_29_days_in_non_leap_year(self, picker):
        # 1402 is not a leap year in the Jalali calendar
        assert not jdatetime.date(1402, 1, 1).isleap()
        assert picker.get_month_days(1402, 12) == 29


class TestMoveToNextDay:
    def test_moves_within_month(self, picker):
        picker.selected_date = jdatetime.date(1403, 1, 15)
        picker.move_to_next_day()
        assert picker.selected_date == jdatetime.date(1403, 1, 16)

    def test_crosses_month_boundary(self, picker):
        picker.selected_date = jdatetime.date(1403, 1, 31)
        picker.move_to_next_day()
        assert picker.selected_date == jdatetime.date(1403, 2, 1)

    def test_crosses_year_boundary_from_leap_esfand(self, picker):
        picker.selected_date = jdatetime.date(1403, 12, 30)
        picker.move_to_next_day()
        assert picker.selected_date == jdatetime.date(1404, 1, 1)

    def test_crosses_year_boundary_from_non_leap_esfand(self, picker):
        picker.selected_date = jdatetime.date(1402, 12, 29)
        picker.move_to_next_day()
        assert picker.selected_date == jdatetime.date(1403, 1, 1)

    def test_does_not_cross_last_year_boundary(self):
        picker = PersianDatePicker(first_year=1403, last_year=1405)
        picker.selected_date = jdatetime.date(1405, 12, 29)
        picker.move_to_next_day()
        assert picker.selected_date == jdatetime.date(1405, 12, 29)


class TestMoveToPreviousDay:
    def test_moves_within_month(self, picker):
        picker.selected_date = jdatetime.date(1403, 1, 15)
        picker.move_to_previous_day()
        assert picker.selected_date == jdatetime.date(1403, 1, 14)

    def test_crosses_month_boundary(self, picker):
        picker.selected_date = jdatetime.date(1403, 3, 1)
        picker.move_to_previous_day()
        assert picker.selected_date == jdatetime.date(1403, 2, 31)

    def test_crosses_year_boundary_into_esfand(self, picker):
        picker.selected_date = jdatetime.date(1403, 1, 1)
        picker.move_to_previous_day()
        assert picker.selected_date == jdatetime.date(1402, 12, 29)

    def test_does_not_cross_first_year_boundary(self):
        picker = PersianDatePicker(first_year=1403, last_year=1405)
        picker.selected_date = jdatetime.date(1403, 1, 1)
        picker.move_to_previous_day()
        assert picker.selected_date == jdatetime.date(1403, 1, 1)


class TestValidateDateInput:
    def test_valid_date(self, picker):
        date_obj, error = picker.validate_date_input('1403/01/15')
        assert date_obj == jdatetime.date(1403, 1, 15)
        assert error == ""

    def test_valid_date_with_persian_numerals(self, picker):
        date_obj, error = picker.validate_date_input('۱۴۰۳/۰۱/۱۵')
        assert date_obj == jdatetime.date(1403, 1, 15)
        assert error == ""

    def test_valid_date_without_leading_zeros(self, picker):
        date_obj, error = picker.validate_date_input('1403/1/5')
        assert date_obj == jdatetime.date(1403, 1, 5)
        assert error == ""

    def test_valid_date_with_surrounding_whitespace(self, picker):
        date_obj, error = picker.validate_date_input('  1403/01/15  ')
        assert date_obj == jdatetime.date(1403, 1, 15)
        assert error == ""

    def test_day_31_in_31_day_month_is_valid(self, picker):
        # Ordibehesht (month 2) has 31 days
        date_obj, error = picker.validate_date_input('1403/02/31')
        assert date_obj == jdatetime.date(1403, 2, 31)
        assert error == ""

    def test_day_31_in_30_day_month_is_invalid(self, picker):
        # Mehr (month 7) has only 30 days
        date_obj, error = picker.validate_date_input('1403/07/31')
        assert date_obj is None
        assert error != ""

    def test_esfand_30_valid_in_leap_year(self, picker):
        date_obj, error = picker.validate_date_input('1403/12/30')
        assert date_obj == jdatetime.date(1403, 12, 30)
        assert error == ""

    def test_esfand_30_invalid_in_non_leap_year(self, picker):
        date_obj, error = picker.validate_date_input('1402/12/30')
        assert date_obj is None
        assert error != ""

    def test_year_outside_configured_range(self):
        picker = PersianDatePicker(first_year=1300, last_year=1410)
        date_obj, error = picker.validate_date_input('1250/01/01')
        assert date_obj is None
        assert error != ""

    def test_invalid_format_rejected(self, picker):
        date_obj, error = picker.validate_date_input('not a date')
        assert date_obj is None
        assert error != ""

    def test_empty_string_rejected(self, picker):
        date_obj, error = picker.validate_date_input('')
        assert date_obj is None
        assert error != ""

    def test_invalid_month_rejected(self, picker):
        date_obj, error = picker.validate_date_input('1403/13/01')
        assert date_obj is None
        assert error != ""


class TestNumeralConversion:
    def test_to_persian_num(self, picker):
        assert picker.to_persian_num(1403) == "۱۴۰۳"

    def test_to_english_num(self, picker):
        assert picker.to_english_num("۱۴۰۳") == "1403"

    def test_to_english_num_passes_through_non_numerals(self, picker):
        assert picker.to_english_num("۱۴۰۳/۰۱") == "1403/01"


class TestConstructorValidation:
    def test_raises_when_first_year_not_less_than_last_year(self):
        with pytest.raises(ValueError):
            PersianDatePicker(first_year=1405, last_year=1400)

    def test_default_date_sets_selected_and_display(self):
        default = jdatetime.date(1400, 5, 10)
        picker = PersianDatePicker(default_date=default)
        assert picker.selected_date == default
        assert picker.display_month == 5
        assert picker.display_year == 1400

    def test_no_default_date_uses_today(self, picker):
        assert picker.selected_date == jdatetime.date.today()


class TestGetSelectedDateInfo:
    def test_returns_expected_keys(self, picker):
        picker.selected_date = jdatetime.date(1403, 1, 15)
        info = picker.get_selected_date_info()
        assert info['year'] == 1403
        assert info['month'] == 1
        assert info['day'] == 15
        assert info['formatted_persian'] == "1403/01/15"
        assert info['day_name'] in picker.persian_days
        assert info['month_name'] == picker.persian_months[0]
