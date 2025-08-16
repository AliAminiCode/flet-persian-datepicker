"""
Basic Persian DatePicker Example
================================
Simple demonstration of Persian DatePicker features and options.
Run this file to see different ways to use the datepicker.
"""

import flet as ft
import jdatetime
from persian_datepicker_project.persian_datepicker import PersianDatePicker


def main(page: ft.Page):
    page.title = "Persian DatePicker - Basic Examples"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 700
    page.window.height = 500
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Result display
    result_text = ft.Text("تاریخی انتخاب نشده است", size=16, text_align=ft.TextAlign.CENTER)

    def on_date_result(result):
        """Callback when date is selected or canceled"""
        if result:
            result_text.value = f"📅 تاریخ انتخابی: {result['formatted_persian']} ({result['day_name']})"
        else:
            result_text.value = "❌ انتخاب لغو شد"
        page.update()

    # Example 1: Simple datepicker
    def show_simple(e):
        picker = PersianDatePicker()
        picker.set_result_callback(on_date_result)
        picker.show(page)

    # Example 2: With custom date range
    def show_custom_range(e):
        picker = PersianDatePicker(first_year=1400, last_year=1410)
        picker.set_result_callback(on_date_result)
        picker.show(page)

    # Example 3: With default date
    def show_with_default(e):
        custom_date = jdatetime.date(1403, 1, 1)  # 1st Farvardin 1403
        picker = PersianDatePicker(default_date=custom_date)
        picker.set_result_callback(on_date_result)
        picker.show(page)

    # Example 4: Dark theme
    def show_dark_theme(e):
        picker = PersianDatePicker()
        picker.set_result_callback(on_date_result)
        picker.show(page, is_theme_light=False)

    # Example 5: Open to specific month/year
    def show_specific_month(e):
        picker = PersianDatePicker()
        picker.set_result_callback(on_date_result)
        picker.show(page, display_year=1403, display_month=6)  # Shahrivar 1403

    # Example 6: Without input mode (keyboard only)
    def show_no_input(e):
        picker = PersianDatePicker(enable_input_mode=False)
        picker.set_result_callback(on_date_result)
        picker.show(page)

    # Example 7: Without keyboard support
    def show_no_keyboard(e):
        picker = PersianDatePicker(keyboard_support=False)
        picker.set_result_callback(on_date_result)
        picker.show(page)

    # Example 8: Minimal (no input mode, no keyboard)
    def show_minimal(e):
        picker = PersianDatePicker(enable_input_mode=False, keyboard_support=False)
        picker.set_result_callback(on_date_result)
        picker.show(page)

    # UI Layout
    page.add(
        ft.Column([
            ft.Text("🗓️ Persian DatePicker Examples",
                   size=24, weight=ft.FontWeight.BOLD),

            ft.Text("Keyboard: Enter=OK, Escape=Cancel, A/D=Days, W/S=Weeks (if enabled)",
                   size=12, italic=True, color=ft.Colors.GREY_600),

            ft.Divider(),

            # Buttons
            ft.Row([
                ft.ElevatedButton("Simple", on_click=show_simple, width=120),
                ft.ElevatedButton("Date Range", on_click=show_custom_range, width=120),
                ft.ElevatedButton("With Default", on_click=show_with_default, width=120),
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                ft.ElevatedButton("Dark Theme", on_click=show_dark_theme, width=120),
                ft.ElevatedButton("Specific Month", on_click=show_specific_month, width=120),
                ft.ElevatedButton("No Input Mode", on_click=show_no_input, width=120),
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Row([
                ft.ElevatedButton("No Keyboard", on_click=show_no_keyboard, width=120),
                ft.ElevatedButton("Minimal Mode", on_click=show_minimal, width=120),
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Divider(),

            # Result display
            result_text,

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15)
    )


if __name__ == "__main__":
    ft.app(target=main)