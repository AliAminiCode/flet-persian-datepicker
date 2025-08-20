# Flet Persian DatePicker

**Flet Persian DatePicker: Advanced Shamsi/Jalali Date Widget (2025 Release)**  
Discover a cutting-edge Persian (Shamsi) DatePicker widget designed for Flet, launched in 2025! This powerful Flet Persian DatePicker offers seamless navigation, stunning animations, and full RTL support with Persian numerals, making it ideal for modern Persian apps. Key features include:

- **Keyboard Navigation**: Effortlessly navigate with Escape (close), Enter (confirm), A/D (previous/next day), and W/S (previous/next week).
- **Flexible Themes**: Switch between light and dark modes for a tailored user experience.
- **Input Mode with Validation**: Enter dates directly with smart validation for accuracy.
- **Smart Features**: Enjoy mode switching, date memory, and a dedicated today button.

Perfect for developers seeking a robust Jalali Calendar solution or a Shamsi Date Widget for Flet projects. Explore more at [https://github.com/AliAminiCode/flet-persian-datepicker](https://github.com/AliAminiCode/flet-persian-datepicker).

## Installation
Install the package via pip:
```bash
pip install persian-datepicker
```

## Current Version
v1.5 (See [Changelog](https://github.com/AliAminiCode/flet-persian-datepicker/blob/master/CHANGELOG.md))

## Quick Start
Here’s a simple example to get you started with the Persian DatePicker:

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
Run this code after installing the package to see a basic datepicker with a button to open it. The selected date will be printed in Persian format.

## Advanced Usage

- Customize themes: page.theme_mode = ft.ThemeMode.DARK before showing the datepicker.
- Set default date: datepicker.set_default_date("1404/06/01").
- Validate date range: Check example_mini_project.py for advanced usage.

## Screenshots
Check out the Persian DatePicker in action with light and dark themes:

- **Light Mode:**  
<img src="screenshots/light_mode_landscape.png" alt="Light Mode">

- **Dark Mode:**  
<img src="screenshots/dark_mode_landscape.png" alt="Dark Mode">

## Usage
Check the `examples/` directory for sample code:
- `example_basic.py`: Basic usage.
- `example_mini_project.py`: A mini project demo.

## Features
- Persian calendar with Shamsi dates.
- Floating overlay with modal behavior.
- Comprehensive error handling and validation.
- Performance optimized with LRU cache.

## Changelog
See [CHANGELOG.md](https://github.com/AliAminiCode/flet-persian-datepicker/blob/master/CHANGELOG.md) for detailed version history.

## Reporting Issues
Found a bug? Report it [here](https://github.com/AliAminiCode/flet-persian-datepicker/issues).

## License
This project is licensed under the [MIT License](https://github.com/AliAminiCode/flet-persian-datepicker/blob/master/LICENSE).  
Developed by [Ali Amini](mailto:aliamini9728@gmail.com).

## Contribute
Feel free to open issues or pull requests on [GitHub](https://github.com/AliAminiCode/flet-persian-datepicker).
Note: This repository was previously named persian-datepicker. Update your bookmarks to https://github.com/AliAminiCode/flet-persian-datepicker!
