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
- Default date highlighting with yellow border
- Last selected date visual distinction

Author: Ali Amini |----> aliamini9728@gmail.com
Version: 1.1 - Enhanced with default date highlighting
"""

import flet as ft
import jdatetime
from typing import Optional, Callable


# =============================================================================
# CONFIGURATION SECTION - Customize all parameters here
# =============================================================================

class PersianDatePickerConfig:
    """Centralized configuration for Persian DatePicker customization"""
    # === DATE RANGE SETTINGS ===
    DEFAULT_FIRST_YEAR = 1300
    DEFAULT_LAST_YEAR = jdatetime.date.today().year + 5

    # === LAYOUT & DIMENSIONS ===
    # Main container
    DATEPICKER_WIDTH = 330  # Base width (right panel width will be added)
    DATEPICKER_HEIGHT = 430
    BORDER_RADIUS = 16

    # Right panel (date display)
    RIGHT_PANEL_WIDTH = 180
    RIGHT_PANEL_PADDING = 24
    RIGHT_PANEL_BGCOLOR = "#e8e9f3"

    # Left panel (calendar)
    LEFT_PANEL_PADDING = 24
    CALENDAR_CONTAINER_HEIGHT = 250

    # Day cells
    DAY_CELL_WIDTH = 33
    DAY_CELL_HEIGHT = 33
    DAY_CELL_BORDER_RADIUS = 20

    # Year cells
    YEAR_CELL_WIDTH = 80
    YEAR_CELL_HEIGHT = 40
    YEAR_CELL_BORDER_RADIUS = 20
    YEARS_PER_ROW = 3

    # === COLORS ===
    # === LIGHT THEME COLORS ===
    LIGHT_PRIMARY_COLOR = "#286580"
    LIGHT_SECONDARY_COLOR = "#3b82f6"
    LIGHT_TEXT_PRIMARY = "#374151"
    LIGHT_TEXT_PRIMARY_BGCOLOR = "#374151"
    LIGHT_TEXT_SECONDARY = "#4a5051"
    LIGHT_TEXT_MUTED = "#6b7280"
    LIGHT_TEXT_HEADER = "#4b5059"
    LIGHT_TEXT_DAY_HEADER = "#5f6471"
    LIGHT_MAIN_BGCOLOR = "white"
    LIGHT_RIGHT_PANEL_BGCOLOR = "#e8e9f3"
    LIGHT_SELECTED_TEXT_COLOR = "white"
    LIGHT_DIVIDER_COLOR = ft.Colors.GREY_500
    # Default date highlighting colors
    LIGHT_DEFAULT_DATE_BORDER_COLOR = "#fbbf24"  # Yellow border for default date
    LIGHT_DEFAULT_DATE_BGCOLOR = "#fef3c7"  # Light yellow background for default date

    # === DARK THEME COLORS ===
    DARK_PRIMARY_COLOR = "#6eabf5"
    DARK_SECONDARY_COLOR = "#88abfc"
    DARK_TEXT_PRIMARY = "#e5e7eb"
    DARK_TEXT_PRIMARY_BGCOLOR = "#abc7ff"
    DARK_TEXT_SECONDARY = "#d1d5db"
    DARK_TEXT_MUTED = "#9ca3af"
    DARK_TEXT_HEADER = "#f3f4f6"
    DARK_TEXT_DAY_HEADER = "#d1d5db"
    DARK_MAIN_BGCOLOR = "#1f2937"
    DARK_RIGHT_PANEL_BGCOLOR = "#374151"
    DARK_SELECTED_TEXT_COLOR = "#111827"
    DARK_DIVIDER_COLOR = ft.Colors.GREY_600
    # Default date highlighting colors for dark theme
    DARK_DEFAULT_DATE_BORDER_COLOR = "#f59e0b"  # Orange-yellow border for default date
    DARK_DEFAULT_DATE_BGCOLOR = "#451a03"  # Dark yellow background for default date

    # === BORDER SETTINGS FOR DEFAULT DATE ===
    DEFAULT_DATE_BORDER_WIDTH = 2
    DEFAULT_DATE_BORDER_STYLE = ft.BorderSide(width=2)

    # Main colors
    PRIMARY_COLOR = "#286580"  # Selected date/year background
    SECONDARY_COLOR = "#3b82f6"  # OK button and cancel button text
    TEXT_PRIMARY = "#374151"  # Main text color
    TEXT_SECONDARY = "#4a5051"  # Selected date text
    TEXT_MUTED = "#6b7280"  # Icons and secondary text
    TEXT_HEADER = "#4b5059"  # Header text
    TEXT_DAY_HEADER = "#5f6471"  # Day abbreviation headers

    # Backgrounds
    MAIN_BGCOLOR = "white"
    OVERLAY_BGCOLOR_OPACITY = 0.5  # Semi-transparent overlay
    SELECTED_TEXT_COLOR = "white"

    # Button colors
    BUTTON_HOVER_OPACITY = 0.1
    DIVIDER_COLOR = ft.Colors.GREY_500

    # === TYPOGRAPHY ===
    # Font sizes
    SELECTED_DATE_FONT_SIZE = 32
    HEADER_TEXT_FONT_SIZE = 15
    MONTH_YEAR_FONT_SIZE = 18
    DAY_CELL_FONT_SIZE = 16
    YEAR_CELL_FONT_SIZE = 16
    DAY_HEADER_FONT_SIZE = 16

    # Font weights
    SELECTED_DATE_FONT_WEIGHT = ft.FontWeight.W_400
    HEADER_FONT_WEIGHT = ft.FontWeight.W_500
    MONTH_YEAR_FONT_WEIGHT = ft.FontWeight.W_500
    DAY_CELL_FONT_WEIGHT = ft.FontWeight.W_500
    YEAR_CELL_FONT_WEIGHT = ft.FontWeight.W_500
    DAY_HEADER_FONT_WEIGHT = ft.FontWeight.W_600

    # === SPACING ===
    # General spacing
    CALENDAR_ROW_SPACING = 8  # Space between day cells
    CALENDAR_COLUMN_SPACING = 10  # Space between calendar rows
    YEAR_ROW_SPACING = 15  # Space between year cells
    BUTTON_ROW_SPACING = 12  # Space between action buttons
    MAIN_COLUMN_SPACING = 12  # Space between main sections
    SELECTED_DATE_COLUMN_SPACING = 8  # Space in right panel

    # Margins
    EDIT_ICON_TOP_MARGIN = 184
    ACTION_BUTTONS_MARGIN_TOP_NORMAL = 0
    ACTION_BUTTONS_MARGIN_TOP_YEAR_MODE = 26

    # === ICONS ===
    EDIT_ICON = ft.Icons.EDIT_OUTLINED
    EDIT_ICON_SIZE = 22
    DROPDOWN_ICON = ft.Icons.ARROW_DROP_DOWN_SHARP
    DROPDOWN_ICON_SIZE = 25
    NAV_ICON_SIZE = 22
    PREV_MONTH_ICON = ft.Icons.CHEVRON_LEFT
    NEXT_MONTH_ICON = ft.Icons.CHEVRON_RIGHT

    # === SHADOWS ===
    SHADOW_SPREAD_RADIUS = 1
    SHADOW_BLUR_RADIUS = 20
    SHADOW_COLOR = "#00000019"
    SHADOW_OFFSET_X = 0
    SHADOW_OFFSET_Y = 5

    # === BUTTON STYLES ===
    # Action buttons
    OK_BUTTON_PADDING_H = 16
    OK_BUTTON_PADDING_V = 8
    CANCEL_BUTTON_PADDING_H = 16
    CANCEL_BUTTON_PADDING_V = 8

    # Navigation buttons
    NAV_BUTTON_BORDER_RADIUS = 4
    YEAR_SELECT_BUTTON_PADDING_H = 10
    YEAR_SELECT_BUTTON_PADDING_V = 6
    YEAR_SELECT_BUTTON_BORDER_RADIUS = 6

    # === TEXT CONTENT ===
    # Persian text labels
    HEADER_TEXT = "انتخاب تاریخ"
    OK_BUTTON_TEXT = "تأیید"
    CANCEL_BUTTON_TEXT = "لغو"
    PREV_MONTH_TOOLTIP = "ماه قبل"
    NEXT_MONTH_TOOLTIP = "ماه بعد"
    TODAY_BUTTON_TEXT = "برو به امروز"
    TODAY_BUTTON_TOOLTIP = "انتخاب تاریخ امروز"

    # === DIVIDERS ===
    DIVIDER_HEIGHT = 1.5
    VERTICAL_DIVIDER_WIDTH = 1.5

    # === CALENDAR GRID ===
    CALENDAR_WEEKS = 6  # Number of weeks to display
    DAYS_PER_WEEK = 7

    def get_theme_colors(self, is_light_theme: bool):
        """Get color configuration based on theme"""
        if is_light_theme:
            return {
                'primary_color': self.LIGHT_PRIMARY_COLOR,
                'secondary_color': self.LIGHT_SECONDARY_COLOR,
                'text_primary': self.LIGHT_TEXT_PRIMARY,
                'text_secondary': self.LIGHT_TEXT_SECONDARY,
                'text_muted': self.LIGHT_TEXT_MUTED,
                'text_header': self.LIGHT_TEXT_HEADER,
                'text_day_header': self.LIGHT_TEXT_DAY_HEADER,
                'main_bgcolor': self.LIGHT_MAIN_BGCOLOR,
                'right_panel_bgcolor': self.LIGHT_RIGHT_PANEL_BGCOLOR,
                'selected_text_color': self.LIGHT_SELECTED_TEXT_COLOR,
                'divider_color': self.LIGHT_DIVIDER_COLOR,
                'text_primary_bgcolor': self.LIGHT_TEXT_PRIMARY_BGCOLOR,
                'default_date_border_color': self.LIGHT_DEFAULT_DATE_BORDER_COLOR,
                'default_date_bgcolor': self.LIGHT_DEFAULT_DATE_BGCOLOR
            }
        else:
            return {
                'primary_color': self.DARK_PRIMARY_COLOR,
                'secondary_color': self.DARK_SECONDARY_COLOR,
                'text_primary': self.DARK_TEXT_PRIMARY,
                'text_secondary': self.DARK_TEXT_SECONDARY,
                'text_muted': self.DARK_TEXT_MUTED,
                'text_header': self.DARK_TEXT_HEADER,
                'text_day_header': self.DARK_TEXT_DAY_HEADER,
                'main_bgcolor': self.DARK_MAIN_BGCOLOR,
                'right_panel_bgcolor': self.DARK_RIGHT_PANEL_BGCOLOR,
                'selected_text_color': self.DARK_SELECTED_TEXT_COLOR,
                'divider_color': self.DARK_DIVIDER_COLOR,
                'text_primary_bgcolor': self.DARK_TEXT_PRIMARY_BGCOLOR,
                'default_date_border_color': self.DARK_DEFAULT_DATE_BORDER_COLOR,
                'default_date_bgcolor': self.DARK_DEFAULT_DATE_BGCOLOR
            }


class PersianDatePicker:
    """A custom Persian (Jalali) date picker widget using Flet and jdatetime.

    This class creates a user interface for selecting Persian dates, featuring a calendar
    view with month and year navigation, day selection, RTL (right-to-left) support,
    and visual highlighting for default and previously selected dates.
    """

    def __init__(self, first_year=PersianDatePickerConfig.DEFAULT_FIRST_YEAR,
                 last_year=PersianDatePickerConfig.DEFAULT_LAST_YEAR,
                 default_date: Optional[jdatetime.date] = None,
                 config: Optional[PersianDatePickerConfig] = None):
        """
        Initialize the PersianDatePicker.

        Args:
            first_year (int, optional): The starting year of the date range.
            last_year (int, optional): The ending year of the date range.
            default_date (jdatetime.date, optional): The default selected date. If None, uses today's date.
            config (PersianDatePickerConfig, optional): Custom configuration object. If None, uses default config.
        """
        self.config = config or PersianDatePickerConfig()
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

        # Store the initial default date for highlighting
        self.default_date = default_date or self.current_date

        # Store the original selected date (last time selected) for highlighting
        self.original_selected_date = self.selected_date

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

    def set_default_date(self, default_date: jdatetime.date):
        """Set a new default date that will be highlighted with yellow border"""
        self.default_date = default_date

    def set_original_selected_date(self, original_date: jdatetime.date):
        """Set the original selected date (last time selected) for visual distinction"""
        self.original_selected_date = original_date

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
            'day': self.selected_date.day,
            'is_default': self.selected_date == self.default_date,
            'was_originally_selected': self.selected_date == self.original_selected_date
        }

    def is_date_equal(self, date1: jdatetime.date, date2: jdatetime.date) -> bool:
        """Check if two dates are equal"""
        return (date1.year == date2.year and
                date1.month == date2.month and
                date1.day == date2.day)

    def create_calendar_grid(self, on_date_click, theme_colors):
        """Create the calendar grid for the current display month with enhanced date highlighting"""
        days_in_month = self.get_month_days(self.display_year, self.display_month)
        first_day_weekday = self.get_first_day_of_month(self.display_year, self.display_month)

        calendar_rows = []
        current_row = []
        day_counter = 1

        # Create rows of days
        for week in range(self.config.CALENDAR_WEEKS):
            current_row = []
            for day_of_week in range(self.config.DAYS_PER_WEEK):
                if week == 0 and day_of_week < first_day_weekday:
                    # Empty cell before month starts
                    current_row.append(ft.Container(
                        width=self.config.DAY_CELL_WIDTH,
                        height=self.config.DAY_CELL_HEIGHT
                    ))
                elif day_counter <= days_in_month:
                    # Create day cell with enhanced highlighting
                    current_date = jdatetime.date(self.display_year, self.display_month, day_counter)

                    # Determine the state of this date
                    is_selected = self.is_date_equal(current_date, self.selected_date)
                    is_default = self.is_date_equal(current_date, self.default_date)
                    is_original = self.is_date_equal(current_date, self.original_selected_date)

                    # Determine colors and styling based on date state
                    text_color = theme_colors["text_primary"]
                    bg_color = None
                    border = None

                    if is_selected:
                        # Currently selected date - highest priority
                        text_color = theme_colors["selected_text_color"]
                        bg_color = theme_colors["text_primary_bgcolor"]
                    elif is_default:
                        # Default date - yellow border and light background
                        text_color = theme_colors["text_primary"]
                        bg_color = theme_colors["default_date_bgcolor"]
                        border = ft.border.all(
                            width=self.config.DEFAULT_DATE_BORDER_WIDTH,
                            color=theme_colors["default_date_border_color"]
                        )
                    elif is_original and not is_selected:
                        # Originally selected date but not currently selected - subtle highlighting
                        text_color = theme_colors["text_primary"]
                        bg_color = ft.Colors.with_opacity(0.1, theme_colors["text_primary_bgcolor"])

                    day_cell = ft.Container(
                        content=ft.Text(
                            self.to_persian_num(day_counter),
                            color=text_color,
                            weight=self.config.DAY_CELL_FONT_WEIGHT,
                            size=self.config.DAY_CELL_FONT_SIZE
                        ),
                        width=self.config.DAY_CELL_WIDTH,
                        height=self.config.DAY_CELL_HEIGHT,
                        bgcolor=bg_color,
                        border=border,
                        border_radius=self.config.DAY_CELL_BORDER_RADIUS,
                        alignment=ft.alignment.center,
                        on_click=lambda e, day=day_counter: on_date_click(day)
                    )
                    current_row.append(day_cell)
                    day_counter += 1
                else:
                    # Empty cell after month ends
                    current_row.append(ft.Container(
                        width=self.config.DAY_CELL_WIDTH,
                        height=self.config.DAY_CELL_HEIGHT
                    ))

            calendar_rows.append(ft.Row(current_row, spacing=self.config.CALENDAR_ROW_SPACING))

            # Stop if we've added all days
            if day_counter > days_in_month:
                break

        return calendar_rows

    def create_year_grid(self, on_year_click, theme_colors):
        """Create the year grid for year selection"""
        current_year = self.display_year
        start_year = self.first_year
        end_year = self.last_year

        year_rows = []
        years = list(range(start_year, end_year + 1))

        # Create rows with specified years per row
        for i in range(0, len(years), self.config.YEARS_PER_ROW):
            row_years = years[i:i + self.config.YEARS_PER_ROW]
            year_cells = []

            for year in row_years:
                is_selected = (year == self.display_year)

                year_cell = ft.Container(
                    content=ft.Text(
                        self.to_persian_num(year),
                        color=theme_colors["selected_text_color"] if is_selected else theme_colors["text_primary"],
                        weight=self.config.YEAR_CELL_FONT_WEIGHT,
                        size=self.config.YEAR_CELL_FONT_SIZE
                    ),
                    width=self.config.YEAR_CELL_WIDTH,
                    height=self.config.YEAR_CELL_HEIGHT,
                    bgcolor=theme_colors["text_primary_bgcolor"] if is_selected else None,
                    border_radius=self.config.YEAR_CELL_BORDER_RADIUS,
                    alignment=ft.alignment.center,
                    on_click=lambda e, y=year: on_year_click(y)
                )
                year_cells.append(year_cell)

            # Fill remaining cells if needed
            while len(year_cells) < self.config.YEARS_PER_ROW:
                year_cells.append(ft.Container(
                    width=self.config.YEAR_CELL_WIDTH,
                    height=self.config.YEAR_CELL_HEIGHT
                ))

            year_rows.append(
                ft.Row(
                    year_cells,
                    spacing=self.config.YEAR_ROW_SPACING,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )

        return year_rows

    def close_datepicker(self, page):
        """Close the floating datepicker"""
        if self.overlay_container and self.overlay_container in page.overlay:
            page.overlay.remove(self.overlay_container)
            page.update()

    def show(self, page: ft.Page, is_theme_light: bool = True, display_year: Optional[int] = None,
             display_month: Optional[int] = None):
        """
        Show the Persian DatePicker as a floating overlay.

        Args:
            page (ft.Page): The Flet page to display the datepicker on
            is_theme_light (bool): True for light theme, False for dark theme
            display_year (int, optional): The year to display when opening. If None, uses current display_year.
            display_month (int, optional): The month to display when opening (1-12). If None, uses current display_month.

        Returns:
            Container: The overlay container reference
        """
        # Set display year and month if provided
        if display_year is not None:
            self.display_year = display_year
        if display_month is not None:
            self.display_month = display_month

        return self.create_datepicker(page, is_theme_light)

    def show_with_date(self, page: ft.Page, target_date: jdatetime.date, is_theme_light: bool = True):
        """
        Show the Persian DatePicker with a specific date displayed.

        Args:
            page (ft.Page): The Flet page to display the datepicker on
            target_date (jdatetime.date): The date to navigate to when opening
            is_theme_light (bool): True for light theme, False for dark theme

        Returns:
            Container: The overlay container reference
        """
        return self.show(page, is_theme_light, display_year=target_date.year, display_month=target_date.month)

    def show_current_month(self, page: ft.Page, is_theme_light: bool = True):
        """
        Show the Persian DatePicker displaying the current month.

        Args:
            page (ft.Page): The Flet page to display the datepicker on
            is_theme_light (bool): True for light theme, False for dark theme

        Returns:
            Container: The overlay container reference
        """
        today = jdatetime.date.today()
        return self.show(page, is_theme_light, display_year=today.year, display_month=today.month)

    def create_datepicker(self, page, is_theme_light: bool = True):
        """Create the complete datepicker UI as a floating overlay"""

        theme_colors = self.config.get_theme_colors(is_theme_light)

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

        def on_today_click(e):
            """Handle today button click - navigate to current date"""
            today = jdatetime.date.today()
            self.selected_date = today
            self.display_year = today.year
            self.display_month = today.month
            self.is_year_mode = False  # Ensure we're in calendar mode
            update_calendar_view()

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
            color=theme_colors['text_secondary'],
            size=self.config.SELECTED_DATE_FONT_SIZE,
            weight=self.config.SELECTED_DATE_FONT_WEIGHT,
            text_align=ft.TextAlign.RIGHT
        )

        right_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            self.config.HEADER_TEXT,
                            color=theme_colors['text_header'],
                            size=self.config.HEADER_TEXT_FONT_SIZE,
                            weight=self.config.HEADER_FONT_WEIGHT,
                            text_align=ft.TextAlign.RIGHT
                        ),
                        alignment=ft.alignment.center_right
                    ),
                    selected_date_text,
                    ft.Container(
                        content=ft.ElevatedButton(
                            text=self.config.TODAY_BUTTON_TEXT,
                            style=ft.ButtonStyle(
                                bgcolor=theme_colors['secondary_color'],
                                color=theme_colors['selected_text_color'],
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                shape=ft.RoundedRectangleBorder(radius=8)
                            ),
                            on_click=on_today_click,
                            tooltip=self.config.TODAY_BUTTON_TOOLTIP
                        ),
                        margin=ft.margin.only(top=self.config.EDIT_ICON_TOP_MARGIN),
                        alignment=ft.alignment.center_right
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=self.config.SELECTED_DATE_COLUMN_SPACING,
                horizontal_alignment=ft.CrossAxisAlignment.END
            ),
            bgcolor=theme_colors['right_panel_bgcolor'],
            padding=self.config.RIGHT_PANEL_PADDING,
            width=self.config.RIGHT_PANEL_WIDTH
        )

        self.month_year_text = ft.Text(
            f"{self.persian_months[self.display_month - 1]} {self.to_persian_num(self.display_year)}",
            color=theme_colors['text_primary'],
            size=self.config.MONTH_YEAR_FONT_SIZE,
            weight=self.config.MONTH_YEAR_FONT_WEIGHT,
            text_align=ft.TextAlign.RIGHT
        )

        calendar_year_select_button = ft.TextButton(
            content=ft.Row(
                controls=[
                    self.month_year_text,
                    ft.Icon(
                        name=self.config.DROPDOWN_ICON,
                        color=theme_colors['text_muted'],
                        size=self.config.DROPDOWN_ICON_SIZE
                    )
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            style=ft.ButtonStyle(
                padding=ft.padding.symmetric(
                    horizontal=self.config.YEAR_SELECT_BUTTON_PADDING_H,
                    vertical=self.config.YEAR_SELECT_BUTTON_PADDING_V
                ),
                bgcolor=ft.Colors.TRANSPARENT,
                overlay_color=ft.Colors.with_opacity(self.config.BUTTON_HOVER_OPACITY, self.config.TEXT_MUTED),
                shape=ft.RoundedRectangleBorder(radius=self.config.YEAR_SELECT_BUTTON_BORDER_RADIUS)
            ),
            on_click=on_year_select_toggle
        )

        # Navigation buttons
        nav_buttons = ft.Row(
            [
                ft.IconButton(
                    icon=self.config.PREV_MONTH_ICON,
                    icon_color=theme_colors['text_muted'],
                    icon_size=self.config.NAV_ICON_SIZE,
                    on_click=on_prev_month,
                    tooltip=self.config.PREV_MONTH_TOOLTIP,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=self.config.NAV_BUTTON_BORDER_RADIUS)
                    )
                ),
                ft.IconButton(
                    icon=self.config.NEXT_MONTH_ICON,
                    icon_color=theme_colors['text_muted'],
                    icon_size=self.config.NAV_ICON_SIZE,
                    on_click=on_next_month,
                    tooltip=self.config.NEXT_MONTH_TOOLTIP,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=self.config.NAV_BUTTON_BORDER_RADIUS)
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
                    content=ft.Text(
                        day,
                        color=theme_colors['text_header'],
                        size=self.config.DAY_HEADER_FONT_SIZE,
                        weight=self.config.DAY_HEADER_FONT_WEIGHT
                    ),
                    width=self.config.DAY_CELL_WIDTH,
                    height=self.config.DAY_CELL_HEIGHT,
                    alignment=ft.alignment.center
                )
                for day in self.persian_day_abbr
            ],
            spacing=self.config.CALENDAR_ROW_SPACING
        )

        # Calendar grid (will be updated dynamically)
        calendar_container = ft.Column(
            spacing=self.config.CALENDAR_COLUMN_SPACING,
            height=self.config.CALENDAR_CONTAINER_HEIGHT,
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True
        )

        # Action buttons
        action_buttons = (
            ft.Container(
                ft.Row(
                    [
                        ft.ElevatedButton(
                            self.config.OK_BUTTON_TEXT,
                            style=ft.ButtonStyle(
                                bgcolor=theme_colors['secondary_color'],
                                color=theme_colors['selected_text_color'],
                                padding=ft.padding.symmetric(
                                    horizontal=self.config.OK_BUTTON_PADDING_H,
                                    vertical=self.config.OK_BUTTON_PADDING_V
                                )
                            ),
                            on_click=on_ok_click
                        ),
                        ft.TextButton(
                            self.config.CANCEL_BUTTON_TEXT,
                            style=ft.ButtonStyle(
                                color=theme_colors['secondary_color'],
                                padding=ft.padding.symmetric(
                                    horizontal=self.config.CANCEL_BUTTON_PADDING_H,
                                    vertical=self.config.CANCEL_BUTTON_PADDING_V
                                )
                            ),
                            on_click=on_cancel_click
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=self.config.BUTTON_ROW_SPACING
                ),
                margin=ft.margin.only(top=self.config.ACTION_BUTTONS_MARGIN_TOP_NORMAL)
            )
        )

        top_calendar_container_dividers = ft.Divider(
            visible=False,
            height=self.config.DIVIDER_HEIGHT,
            color=theme_colors['divider_color']
        )
        bottom_calendar_container_dividers = ft.Divider(
            visible=False,
            height=self.config.DIVIDER_HEIGHT,
            color=theme_colors['divider_color']
        )

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
                spacing=self.config.MAIN_COLUMN_SPACING
            ),
            padding=ft.padding.all(self.config.LEFT_PANEL_PADDING),
            expand=True
        )

        # Main datepicker container
        datepicker = ft.Container(
            content=ft.Row(
                [
                    right_panel,
                    ft.VerticalDivider(width=self.config.VERTICAL_DIVIDER_WIDTH, color=theme_colors['divider_color']),
                    left_panel
                ],
                rtl=True,
                spacing=0
            ),
            bgcolor=theme_colors['main_bgcolor'],
            border_radius=self.config.BORDER_RADIUS,
            shadow=ft.BoxShadow(
                spread_radius=self.config.SHADOW_SPREAD_RADIUS,
                blur_radius=self.config.SHADOW_BLUR_RADIUS,
                color=self.config.SHADOW_COLOR,
                offset=ft.Offset(self.config.SHADOW_OFFSET_X, self.config.SHADOW_OFFSET_Y)
            ),
            width=self.config.DATEPICKER_WIDTH + right_panel.width,
            height=self.config.DATEPICKER_HEIGHT
        )

        def update_calendar_view():
            """Update the calendar view based on current mode"""
            if self.is_year_mode:
                # Hide navigation buttons and day headers, show year grid
                nav_buttons.visible = False
                day_headers.visible = False
                top_calendar_container_dividers.visible = True
                bottom_calendar_container_dividers.visible = True
                year_rows = self.create_year_grid(on_year_click, theme_colors)
                calendar_container.controls = year_rows
                action_buttons.margin.top = self.config.ACTION_BUTTONS_MARGIN_TOP_YEAR_MODE
            else:
                # Show navigation buttons and day headers, show calendar grid
                nav_buttons.visible = True
                day_headers.visible = True
                top_calendar_container_dividers.visible = False
                bottom_calendar_container_dividers.visible = False
                calendar_rows = self.create_calendar_grid(on_date_click, theme_colors)
                calendar_container.controls = calendar_rows
                selected_date_text.value = self.format_selected_date()
                action_buttons.margin.top = self.config.ACTION_BUTTONS_MARGIN_TOP_NORMAL

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
                        bgcolor=ft.Colors.with_opacity(self.config.OVERLAY_BGCOLOR_OPACITY, ft.Colors.BLACK),
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