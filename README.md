# Flet Persian DatePicker

🇬🇧 English · [🇮🇷 فارسی](README.fa.md)

A Persian (Jalali/Shamsi) date picker widget for [Flet](https://flet.dev), built from scratch to match the look and feel of Flet's built-in `DatePicker` while adding full Persian calendar and RTL support.

## Overview
Flet's built-in `DatePicker` only supports the Gregorian calendar and English text, which makes it unsuitable for Persian-speaking users. This package provides a drop-in alternative with a similar API, built entirely on top of Flet's existing widgets. Key features:
- **Jalali calendar support**: correct leap-year handling, Persian month and day names, Persian numerals.
- **Keyboard navigation**: Enter to confirm, Escape to cancel, day/week movement, all disabled automatically while typing in input mode.
- **Input mode with validation**: type a date directly (Persian or English numerals) with format and range checking.
- **Light/dark themes** and a configurable year range.
- Built entirely with Flet's existing widgets, no external UI dependencies.

## Installation
Install the package via pip:
```bash
pip install persian-datepicker
```

## Quick Start
```python
import flet as ft
from persian_datepicker import PersianDatePicker

def main(page: ft.Page):
    datepicker = PersianDatePicker()

    def handle_result(result):
        if result:
            print(f"Selected: {result['formatted_persian']}")

    datepicker.set_result_callback(handle_result)

    def show_datepicker(e):
        datepicker.show(page)

    page.add(ft.ElevatedButton("Select Date", on_click=show_datepicker))

ft.app(target=main)
```
Run this after installing the package to see a basic datepicker with a button to open it. The selected date is printed in Persian format.

## Advanced Usage
- Set a custom year range: `PersianDatePicker(first_year=1400, last_year=1410)`.
- Set a default date: `datepicker.set_default_date(jdatetime.date(1404, 6, 1))` — this takes a `jdatetime.date` object, not a string.
- Open to a specific month/year: `datepicker.show(page, display_year=1403, display_month=6)`.
- Disable input mode or keyboard support: `PersianDatePicker(enable_input_mode=False, keyboard_support=False)`.

See `examples/example_basic.py` for all of the options above, and `examples/example_mini_project.py` for a small event-planner app built with the widget.

## Testing
This project uses `pytest` to cover the date-math and validation logic (leap years, month/year boundary crossing, input parsing).

Install the test dependencies and run the suite:
```bash
pip install -e ".[dev]"
pytest tests/
```

## Screenshots
Check out the Persian DatePicker in action:

- **Light Mode**:

<div align="center">
  <img src="screenshots/light_mode_landscape.png" alt="Light Mode">
</div>

- **Dark Mode**:

<div align="center">
  <img src="screenshots/dark_mode_landscape.png" alt="Dark Mode">
</div>

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contribute
Found a bug? Report it at [https://github.com/AliAminiCode/flet-persian-datepicker/issues](https://github.com/AliAminiCode/flet-persian-datepicker/issues).
Developed by [Ali Amini](mailto:aliamini9728@gmail.com).
Licensed under the [MIT License](https://github.com/AliAminiCode/flet-persian-datepicker/blob/master/LICENSE).