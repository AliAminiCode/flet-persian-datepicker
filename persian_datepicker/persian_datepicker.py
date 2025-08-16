# persian_datepicker.py
"""
Persian (Shamsi/Jalali) DatePicker Widget for Flet

A customizable Persian date picker that provides:
- Persian calendar with proper Shamsi dates
- Month and year navigation
- Floating overlay display
- RTL (Right-to-Left) support
- Persian numerals and month names
- Callback system for date selection

Author: Ali Amini |----> aliamini9728@gmail.com
Version: 1.0
"""

import flet as ft
import jdatetime
from typing import Optional, Callable


class PersianDatePicker:
    """A custom Persian (Jalali) date picker widget using Flet and jdatetime.

    This class creates a user interface for selecting Persian dates, featuring a calendar
    view with month and year navigation, day selection, and RTL (right-to-left) support.
    It handles date calculations, formatting, and provides a callback mechanism for
    retrieving the selected date.
    """

    def __init__(self, first_year=1300, last_year=jdatetime.date.today().year + 5,
                 default_date: Optional[jdatetime.date] = None):
        """
        Initialize the PersianDatePicker.

        Args:
            first_year (int, optional): The starting year of the date range. Defaults to 1300.
            last_year (int, optional): The ending year of the date range. Defaults to current year + 5.
            default_date (jdatetime.date, optional): The default selected date. If None, uses today's date.
        """
        self.first_year = first_year
        self.last_year = last_year
        self.current_date = jdatetime.date.today()

        # Set default selected date
        if default_date:
            self.selected_date = default_date
            self.display_month = default_date.month
            self.display_year = default_date.year
        else:
            self.selected_date = self.current_date
            self.display_month = self.current_date.month
            self.display_year = self.current_date.year

        self.result = None
        self.is_year_mode = False
        self.on_result_callback = None  # Callback for result
        self.overlay_container = None  # Store reference to overlay

        # Persian month names
        self.persian_months = [
            "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
            "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
        ]

        # Persian day names (Saturday to Friday)
        self.persian_days = ["شنبه", "یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
        self.persian_day_abbr = ["ش", "ی", "د", "س", "چ", "پ", "ج"]

        # Persian numerals
        self.persian_numerals = "۰۱۲۳۴۵۶۷۸۹"

    def set_result_callback(self, callback: Callable):
        """Set callback function to handle the result"""
        self.on_result_callback = callback

    def to_persian_num(self, num):
        """Convert English numbers to Persian numerals"""
        result = ""
        for digit in str(num):
            result += self.persian_numerals[int(digit)]
        return result

    def get_month_days(self, year, month):
        """Get number of days in a Persian month"""
        if month <= 6:
            return 31
        elif month <= 11:
            return 30
        else:  # month 12 (Esfand)
            return 30 if jdatetime.date(year, 1, 1).isleap() else 29

    def get_first_day_of_month(self, year, month):
        """Get the weekday of the first day of the month (0=Saturday)"""
        first_day = jdatetime.date(year, month, 1)
        return first_day.weekday()  # jdatetime weekday: 0=Saturday

    def format_selected_date(self):
        """Format selected date for display"""
        day_name = self.persian_days[self.selected_date.weekday()]
        month_name = self.persian_months[self.selected_date.month - 1]
        day_num = self.to_persian_num(self.selected_date.day)
        return f"{day_name}، {month_name}\n{day_num}"

    def get_selected_date_info(self):
        """Get complete selected date information"""
        return {
            'date': self.selected_date,
            'formatted_persian': f"{self.selected_date.year}/{self.selected_date.month:02d}/{self.selected_date.day:02d}",
            'formatted_display': self.format_selected_date(),
            'day_name': self.persian_days[self.selected_date.weekday()],
            'month_name': self.persian_months[self.selected_date.month - 1],
            'year': self.selected_date.year,
            'month': self.selected_date.month,
            'day': self.selected_date.day
        }

    def create_calendar_grid(self, on_date_click):
        """Create the calendar grid for the current display month"""
        days_in_month = self.get_month_days(self.display_year, self.display_month)
        first_day_weekday = self.get_first_day_of_month(self.display_year, self.display_month)

        calendar_rows = []
        current_row = []
        day_counter = 1

        # Create 6 rows of 7 days each
        for week in range(6):
            current_row = []
            for day_of_week in range(7):
                if week == 0 and day_of_week < first_day_weekday:
                    # Empty cell before month starts
                    current_row.append(ft.Container(width=33, height=33))
                elif day_counter <= days_in_month:
                    # Create day cell
                    is_selected = (day_counter == self.selected_date.day and
                                   self.display_month == self.selected_date.month and
                                   self.display_year == self.selected_date.year)

                    day_cell = ft.Container(
                        content=ft.Text(
                            self.to_persian_num(day_counter),
                            color="white" if is_selected else "#374151",
                            weight=ft.FontWeight.W_500,
                            size=16
                        ),
                        width=33,
                        height=33,
                        bgcolor="#286580" if is_selected else None,
                        border_radius=20,
                        alignment=ft.alignment.center,
                        on_click=lambda e, day=day_counter: on_date_click(day)
                    )
                    current_row.append(day_cell)
                    day_counter += 1
                else:
                    # Empty cell after month ends
                    current_row.append(ft.Container(width=33, height=33))

            calendar_rows.append(ft.Row(current_row, spacing=8))

            if day_counter > days_in_month:
                break

        return calendar_rows

    def create_year_grid(self, on_year_click):
        """Create the year grid for year selection"""
        current_year = self.display_year
        start_year = self.first_year
        end_year = self.last_year

        year_rows = []
        years = list(range(start_year, end_year + 1))

        # Create rows with 3 years each
        for i in range(0, len(years), 3):
            row_years = years[i:i + 3]
            year_cells = []

            for year in row_years:
                is_selected = (year == self.display_year)

                year_cell = ft.Container(
                    content=ft.Text(
                        self.to_persian_num(year),
                        color="white" if is_selected else "#374151",
                        weight=ft.FontWeight.W_500,
                        size=16
                    ),
                    width=80,
                    height=40,
                    bgcolor="#286580" if is_selected else None,
                    border_radius=20,
                    alignment=ft.alignment.center,
                    on_click=lambda e, y=year: on_year_click(y)
                )
                year_cells.append(year_cell)

            # Fill remaining cells if needed
            while len(year_cells) < 3:
                year_cells.append(ft.Container(width=80, height=40))

            year_rows.append(
                ft.Row(
                    year_cells,
                    spacing=15,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

        return year_rows

    def close_datepicker(self, page):
        """Close the floating datepicker"""
        if self.overlay_container and self.overlay_container in page.overlay:
            page.overlay.remove(self.overlay_container)
            page.update()

    def show(self, page: ft.Page):
        """
        Show the Persian DatePicker as a floating overlay.

        Args:
            page (ft.Page): The Flet page to display the datepicker on

        Returns:
            Container: The overlay container reference
        """
        return self.create_datepicker(page)

    def create_datepicker(self, page):
        """Create the complete datepicker UI as a floating overlay"""

        def on_date_click(day):
            """Handle date selection"""
            self.selected_date = jdatetime.date(self.display_year, self.display_month, day)
            update_calendar_view()

        def on_prev_month(e):
            """Navigate to previous month"""
            if self.display_month == 1:
                self.display_month = 12
                self.display_year -= 1
            else:
                self.display_month -= 1
            update_calendar_view()

        def on_next_month(e):
            """Navigate to next month"""
            if self.display_month == 12:
                self.display_month = 1
                self.display_year += 1
            else:
                self.display_month += 1
            update_calendar_view()

        def on_year_select_toggle(e):
            """Handle year selection button click"""
            self.is_year_mode = not self.is_year_mode
            update_calendar_view()

        def on_year_click(year):
            """Handle year selection"""
            self.display_year = year
            self.is_year_mode = False
            update_calendar_view()

        def on_ok_click(e):
            """Handle OK button click"""
            # Get complete date information
            date_info = self.get_selected_date_info()
            self.result = date_info

            # Call callback if provided
            if self.on_result_callback:
                self.on_result_callback(date_info)

            # Close the floating datepicker
            self.close_datepicker(page)

        def on_cancel_click(e):
            """Handle Cancel button click"""
            self.result = None

            # Call callback if provided
            if self.on_result_callback:
                self.on_result_callback(None)

            # Close the floating datepicker
            self.close_datepicker(page)

        def on_overlay_click(e):
            """Handle clicks on the overlay background (outside datepicker)"""
            # Close datepicker when clicking outside
            self.result = None
            if self.on_result_callback:
                self.on_result_callback(None)
            self.close_datepicker(page)

        # Selected date panel (right side for RTL)
        selected_date_text = ft.Text(
            self.format_selected_date(),
            color="#4a5051",
            size=32,
            weight=ft.FontWeight.W_400,
            text_align=ft.TextAlign.RIGHT
        )

        right_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "انتخاب تاریخ",
                            color="#4b5059",
                            size=15,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.RIGHT
                        ),
                        alignment=ft.alignment.center_right
                    ),
                    selected_date_text,
                    ft.Container(
                        content=ft.Icon(
                            ft.Icons.EDIT_OUTLINED,
                            color="#6b7280",
                            size=22
                        ),
                        margin=ft.margin.only(top=160),
                        alignment=ft.alignment.center_right
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.END
            ),
            bgcolor="#e8e9f3",
            padding=24,
            width=180
        )

        self.month_year_text = ft.Text(
            f"{self.persian_months[self.display_month - 1]} {self.to_persian_num(self.display_year)}",
            color="#374151",
            size=18,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.RIGHT
        )

        calendar_year_select_button = ft.TextButton(
            content=ft.Row(
                controls=[
                    self.month_year_text,
                    ft.Icon(
                        name=ft.Icons.ARROW_DROP_DOWN_SHARP,
                        color="#6b7280",
                        size=25
                    )
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(horizontal=10, vertical=6),
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.with_opacity(0.1, "#6b7280"),
                shape=ft.RoundedRectangleBorder(radius=6)
            ),
            on_click=on_year_select_toggle
        )

        # Navigation buttons
        nav_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_LEFT,
                    icon_color="#6f747d",
                    icon_size=22,
                    on_click=on_prev_month,
                    tooltip="ماه قبل",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=4)
                    )
                ),
                ft.IconButton(
                    icon=ft.Icons.CHEVRON_RIGHT,
                    icon_color="#6f747d",
                    icon_size=22,
                    on_click=on_next_month,
                    tooltip="ماه بعد",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=4)
                    )
                )
            ],
            spacing=0
        )

        calendar_header = ft.Row(
            [
                ft.Row(
                    [calendar_year_select_button],
                    expand=True,
                    spacing=8
                ),
                nav_buttons
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Day headers
        day_headers = ft.Row(
            [
                ft.Container(
                    content=ft.Text(day, color="#5f6471", size=16, weight=ft.FontWeight.W_600),
                    width=33,
                    height=33,
                    alignment=ft.alignment.center
                )
                for day in self.persian_day_abbr
            ],
            spacing=8
        )

        # Calendar grid (will be updated dynamically)
        calendar_container = ft.Column(
            spacing=10,
            height=250,
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True
        )

        # Action buttons
        action_buttons = (
            ft.Container(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            "تأیید",
                            style=ft.ButtonStyle(
                                bgcolor="#3b82f6",
                                color="white",
                                padding=ft.padding.symmetric(horizontal=16, vertical=8)
                            ),
                            on_click=on_ok_click
                        ),
                        ft.TextButton(
                            "لغو",
                            style=ft.ButtonStyle(
                                color="#3b82f6",
                                padding=ft.padding.symmetric(horizontal=16, vertical=8)
                            ),
                            on_click=on_cancel_click
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=12
                ),
                margin=ft.margin.only(top=0)
            )
        )

        top_calendar_container_dividers = ft.Divider(visible=False, height=1.5, color=ft.Colors.GREY_500)
        bottom_calendar_container_dividers = ft.Divider(visible=False, height=1.5, color=ft.Colors.GREY_500)

        # Left panel with calendar
        left_panel = ft.Container(
            content=ft.Column(
                [
                    calendar_header,
                    day_headers,
                    top_calendar_container_dividers,
                    calendar_container,
                    bottom_calendar_container_dividers,
                    action_buttons
                ],
                spacing=12
            ),
            padding=ft.padding.all(24),
            expand=True
        )

        # Main datepicker container
        datepicker = ft.Container(
            content=ft.Row(
                [
                    right_panel,
                    ft.VerticalDivider(width=1.5, color=ft.Colors.GREY_500),
                    left_panel
                ],
                rtl=True,
                spacing=0
            ),
            bgcolor="white",
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color="#00000019",
                offset=ft.Offset(0, 5)
            ),
            width=330 + right_panel.width,
            height=430
        )

        def update_calendar_view():
            """Update the calendar view based on current mode"""
            if self.is_year_mode:
                # Hide navigation buttons and day headers, show year grid
                nav_buttons.visible = False
                day_headers.visible = False
                top_calendar_container_dividers.visible = True
                bottom_calendar_container_dividers.visible = True
                year_rows = self.create_year_grid(on_year_click)
                calendar_container.controls = year_rows
                action_buttons.margin.top = 26
            else:
                # Show navigation buttons and day headers, show calendar grid
                nav_buttons.visible = True
                day_headers.visible = True
                top_calendar_container_dividers.visible = False
                bottom_calendar_container_dividers.visible = False
                calendar_rows = self.create_calendar_grid(on_date_click)
                calendar_container.controls = calendar_rows
                selected_date_text.value = self.format_selected_date()
                action_buttons.margin.top = 0

            self.month_year_text.value = f"{self.persian_months[self.display_month - 1]} {self.to_persian_num(self.display_year)}"
            page.update()

        # Initial calendar update
        update_calendar_view()

        # Create the overlay container (semi-transparent background)
        self.overlay_container = ft.Container(
            content=ft.Stack(
                [
                    # Semi-transparent background
                    ft.Container(
                        bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
                        expand=True,
                        on_click=on_overlay_click  # Close when clicking outside
                    ),
                    # Centered datepicker
                    ft.Container(
                        content=datepicker,
                        alignment=ft.alignment.center,
                        expand=True
                    )
                ]
            ),
            expand=True
        )

        # Add to page overlay
        page.overlay.append(self.overlay_container)
        page.update()

        return self.overlay_container