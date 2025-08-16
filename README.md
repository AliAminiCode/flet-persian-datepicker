# Persian DatePicker

A cutting-edge Persian (Shamsi) DatePicker widget for Flet, launched in 2025! This widget brings seamless navigation, stunning animations, and full RTL support with Persian numerals to your applications. Perfect for modern Persian apps, it includes:

- **Smooth Navigation**: Month and year transitions with animations.
- **Keyboard Support**: Navigate with Escape (close), Enter (confirm), A/D (days), W/S (weeks).
- **Themes**: Light and dark mode support.
- **Input Mode**: Direct date entry with validation.
- **Smart Features**: Mode switching, date memory, and today button.

## Installation
Install the package via pip:
```bash
pip install persian-datepicker
```

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

## Screenshots
Check out the Persian DatePicker in action with light and dark themes:

- **Light Mode:**  
  ![Light Mode](screenshots/light_mode_landscape.png)

- **Dark Mode:**  
  ![Dark Mode](screenshots/dark_mode_landscape.png)

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
See [CHANGELOG.md](https://github.com/AliAminiCode/persian-datepicker/blob/master/CHANGELOG.md) for detailed version history.

## License
This project is licensed under the [MIT License](https://github.com/AliAminiCode/persian-datepicker/blob/master/LICENSE).  
Developed by [Ali Amini](mailto:aliamini9728@gmail.com).

## Contribute
Feel free to open issues or pull requests on [GitHub](https://github.com/AliAminiCode/persian-datepicker).
