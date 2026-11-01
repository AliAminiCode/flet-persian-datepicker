# Flet Persian DatePicker

🇬🇧 English · [🇮🇷 فارسی](README.fa.md)

A Persian (Jalali/Shamsi) date picker for [Flet](https://flet.dev) 1.x. Flet's built-in `DatePicker` shows only the Gregorian calendar with English text. This package adds a Jalali calendar with Persian month and day names, Persian numerals and an RTL layout, styled to look like the built-in picker.

## Features

- **Jalali calendar**: Persian month and day names, Persian numerals, RTL layout.
- **Two modes**: pick from the calendar, or type a date directly (Persian or English digits). Typed dates are checked for format and range, and errors are shown in Persian.
- **Keyboard navigation**: confirm, cancel and move between days and weeks (see [Keyboard shortcuts](#keyboard-shortcuts)).
- **Today button** and highlighting of the default date and the last selected date.
- **Light and dark themes**, configurable year range.
- **Small footprint**: the only dependencies are `flet` and `jdatetime`.

### How it differs from `ft.DatePicker`

The look and feel follow Flet's built-in picker, but the API is its own: you create a `PersianDatePicker`, register a result callback, and call `show(page)`. It is not a drop-in replacement for `ft.DatePicker`, so existing code needs small changes when you switch.

## Installation

```bash
pip install persian-datepicker
```

Requires **Python 3.10+** and **Flet 1.0.1+**.

### Version compatibility

| Library version | Flet version | Install |
|---|---|---|
| 2.x | 1.0.1 or newer (below 2.0) | `pip install persian-datepicker` |
| 1.x | 0.28.x or older | `pip install "persian-datepicker<2" "flet<1"` |

Flet 1.0 renamed and removed many APIs, so version 2.0.0 and newer will not run on Flet 0.x. See [CHANGELOG.md](CHANGELOG.md) for what changed.

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

    page.add(ft.Button("Select Date", on_click=show_datepicker))

ft.run(main)
```

Clicking the button opens the picker. When a date is confirmed, the callback receives a result dictionary; `result['formatted_persian']` holds the date formatted in Persian.

<!-- TODO: list every key of the result dictionary (e.g. what the Gregorian value and the date object are called) with a one-line description each. -->

## Usage

| What you want | How |
|---|---|
| Limit the selectable years | `PersianDatePicker(first_year=1400, last_year=1410)` |
| Start from a given date | `datepicker.set_default_date(jdatetime.date(1404, 6, 1))` (takes a `jdatetime.date`, not a string) |
| Open on a specific month | `datepicker.show(page, display_year=1403, display_month=6)` |
| Turn off typed input | `PersianDatePicker(enable_input_mode=False)` |
| Turn off keyboard shortcuts | `PersianDatePicker(keyboard_support=False)` |

Runnable examples:

- `examples/example_basic.py`: every option above.
- `examples/example_mini_project.py`: a small event-planner app built with the widget.

## Keyboard shortcuts

Shortcuts work only while the picker is open and in calendar mode. They are disabled in year-selection and input modes, so typing is never interrupted.

| Key | Action |
|---|---|
| `Enter` | Confirm the selected date |
| `Esc` | Cancel and close |
| `D` | Previous day (can cross into the previous month) |
| `A` | Next day (can cross into the next month) |
| `W` | Previous week (stays within the current month) |
| `S` | Next week (stays within the current month) |

## Testing

`pytest` covers the date logic and validation: leap years, month and year boundary crossing, and input parsing. The widget's UI behavior is checked with smoke tests and manual testing.

```bash
pip install -e ".[dev]"
pytest tests/
```

## Screenshots

**Light mode**

<div align="center">
  <img src="screenshots/light_mode_landscape.png" alt="Persian DatePicker in light mode">
</div>

**Dark mode**

<div align="center">
  <img src="screenshots/dark_mode_landscape.png" alt="Persian DatePicker in dark mode">
</div>

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing and support

Found a bug or want a feature? Open an issue: <https://github.com/AliAminiCode/flet-persian-datepicker/issues>. When reporting a bug, include your Python, Flet and library versions and a short snippet that reproduces it.

## License

[MIT](https://github.com/AliAminiCode/flet-persian-datepicker/blob/master/LICENSE). Developed by [Ali Amini](mailto:aliamini9728@gmail.com).
