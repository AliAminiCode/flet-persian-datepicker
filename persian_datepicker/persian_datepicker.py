# persian_datepicker.py
"""
A customizable Persian date picker that provides:
- Persian calendar with proper Shamsi dates
- Month and year navigation with smooth transitions
- Floating overlay display with modal behavior
- RTL (Right-to-Left) support for Persian text
- Persian numerals and month names
- Callback system for date selection results
- Default date highlighting with yellow border
- Last selected date visual distinction
- Interactive hover effects on all clickable elements
- Smooth animations for mode transitions and year selection
- Input mode for direct date entry with validation
- Light and dark theme support
- Multiple display modes: Calendar, Year selection, and Text input
- Smart mode switching (input mode always returns to calendar mode)
- Automatic input validation with Persian numeral support
- Date memory control (reset to default vs. remember last selection)
- Flexible show methods for different use cases
- Today navigation button for quick date selection
- Error handling with user-friendly Persian error messages
- Comprehensive date range validation
- Clean state management and mode isolation
- Performance optimizations with LRU cache for faster date calculations
- Comprehensive keyboard navigation support:
  * Escape key: Cancel/close datepicker
  * Enter key: Confirm selection
  * A key / Right Arrow: Navigate to previous day (crosses month boundaries)
  * D key / Left Arrow: Navigate to next day (crosses month boundaries)
  * W key: Navigate to previous week (stays within current month)
  * S key: Navigate to next week (stays within current month)
  * Keyboard events only active in calendar mode (disabled in year/input modes)
  * Smart keyboard event isolation (only captures events when datepicker is open)

Author: Ali Amini |----> aliamini9728@gmail.com
Version: 1.5.0 - Added comprehensive keyboard navigation with day/week movement
"""

import flet as ft
import re
import jdatetime
import functools
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
    DATEPICKER_CALENDAR_MODE_HEIGHT = 430
    DATEPICKER_INPUT_MODE_HEIGHT = 250
    BORDER_RADIUS = 16

    CALENDAR_CONTAINER_HEIGHT_CALENDAR_MODE = 250
    CALENDAR_CONTAINER_HEIGHT_INPUT_MODE = 170

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

    # Hover colors for light theme
    LIGHT_CELL_HOVER_COLOR = "#dbdbdb"  # Light gray hover for day cells
    LIGHT_ACTION_BUTTONS_HOVER_COLOR = "#e5e7eb"  # Slightly darker hover for year cells

    # Input mode colors for light theme
    LIGHT_INPUT_COLOR = "#353638"
    LIGHT_INPUT_FOCUS_BORDER_COLOR = "#3b82f6"
    LIGHT_ERROR_TEXT_COLOR = "#dc2626"


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

    # Hover colors for dark theme
    DARK_CELL_HOVER_COLOR = "#2c3545"  # Light gray hover for day cells
    DARK_ACTION_BUTTONS_HOVER_COLOR = "#e5e7eb"  # Slightly darker hover for year cells

    # Input mode colors for dark theme
    DARK_INPUT_COLOR = "#e6e6e6"
    DARK_INPUT_FOCUS_BORDER_COLOR = "#6366f1"
    DARK_ERROR_TEXT_COLOR = "#f87171"

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
    SELECTED_DATE_FONT_SIZE_CALENDAR_MODE = 32
    SELECTED_DATE_FONT_SIZE_INPUT_MODE = 26

    HEADER_TEXT_FONT_SIZE = 15
    MONTH_YEAR_FONT_SIZE = 18
    DAY_CELL_FONT_SIZE = 16
    YEAR_CELL_FONT_SIZE = 16
    DAY_HEADER_FONT_SIZE = 16
    INPUT_TEXT_FONT_SIZE = 16
    ERROR_TEXT_FONT_SIZE = 12

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
    TEXT_FIELD_MARGIN_TOP = 60
    EDIT_ICON_TOP_MARGIN_CALENDAR_MODE = 181
    EDIT_ICON_TOP_MARGIN_INPUT_MODE = 30
    ACTION_BUTTONS_MARGIN_TOP_CALENDAR_MODE = 0
    ACTION_BUTTONS_MARGIN_TOP_INPUT_MODE = 0
    ACTION_BUTTONS_MARGIN_TOP_YEAR_MODE = 26

    # === ICONS ===
    EDIT_ICON = ft.Icons.EDIT_OUTLINED
    EDIT_ICON_SIZE = 24
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
    NAV_BUTTON_BORDER_RADIUS = 25
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
    INPUT_MODE_PLACEHOLDER = "YYYY/MM/DD"
    INVALID_FORMAT_ERROR = "فرمت نامعتبر"
    INPUT_MODE_LABEL = "تاریخ را وارد کنید"

    # === INPUT MODE SETTINGS ===
    INPUT_MODE_ICON = ft.Icons.EDIT_OUTLINED
    INPUT_MODE_ICON_SIZE = 22
    CALENDAR_MODE_ICON = ft.Icons.CALENDAR_TODAY  # Changed to CALENDAR_TODAY
    INPUT_MODE_BUTTON_TOOLTIP = "حالت ورودی متن"
    CALENDAR_MODE_BUTTON_TOOLTIP = "حالت تقویم"

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
                'default_date_bgcolor': self.LIGHT_DEFAULT_DATE_BGCOLOR,
                'cell_hover_color': self.LIGHT_CELL_HOVER_COLOR,
                'action_buttons_hover_color': self.LIGHT_ACTION_BUTTONS_HOVER_COLOR,
                'input_color': self.LIGHT_INPUT_COLOR,
                'input_focus_border_color': self.LIGHT_INPUT_FOCUS_BORDER_COLOR,
                'error_text_color': self.LIGHT_ERROR_TEXT_COLOR,
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
                'default_date_bgcolor': self.DARK_DEFAULT_DATE_BGCOLOR,
                'cell_hover_color': self.DARK_CELL_HOVER_COLOR,
                'action_buttons_hover_color': self.DARK_ACTION_BUTTONS_HOVER_COLOR,
                'input_color': self.DARK_INPUT_COLOR,
                'input_focus_border_color': self.DARK_INPUT_FOCUS_BORDER_COLOR,
                'error_text_color': self.DARK_ERROR_TEXT_COLOR,
            }


class PersianDatePicker:
    """A comprehensive Persian (Jalali) date picker widget using Flet and jdatetime.

    This class creates a feature-rich user interface for selecting Persian dates with:
    - Complete Persian calendar with proper Shamsi dates and Persian numerals
    - Month and year navigation with smooth transitions and animations
    - Floating overlay display with modal behavior and theme support
    - Full RTL (right-to-left) support for Persian text and interface
    - Advanced keyboard navigation (Enter, Escape, A/D for days, W/S for weeks, Arrow keys)
    - Multiple input modes: Calendar view, Year selection, and Text input with validation
    - Visual highlighting system for default dates, selected dates, and previously chosen dates
    - Comprehensive customization through centralized configuration system
    - Performance optimizations with LRU cache for date calculations
    - Smart boundary handling and seamless month/year transitions
    - Professional error handling with Persian error messages
    """

    def __init__(self, first_year=PersianDatePickerConfig.DEFAULT_FIRST_YEAR,
                 last_year=PersianDatePickerConfig.DEFAULT_LAST_YEAR,
                 default_date: Optional[jdatetime.date] = None,
                 config: Optional[PersianDatePickerConfig] = None,
                 enable_input_mode: bool = True,
                 keyboard_support: bool = True):
        """
        Initialize the PersianDatePicker.

        Args:
            first_year (int, optional): The starting year of the date range. Defaults to 1300.
            last_year (int, optional): The ending year of the date range. Defaults to current year + 5.
            default_date (jdatetime.date, optional): The default selected date. If None, uses today's date.
            config (PersianDatePickerConfig, optional): Custom configuration object for styling and behavior. If None, uses default config.
            enable_input_mode (bool, optional): Enable text input mode toggle button. Default is True.
            keyboard_support (bool, optional): Enable keyboard navigation (Enter, Escape, A/D, W/S, Arrows). Default is True.
        """

        if first_year and last_year and first_year >= last_year:
            raise ValueError("first_year must be less than last_year")

        self.config = config or PersianDatePickerConfig()
        self.first_year = first_year
        self.last_year = last_year
        self.current_date = jdatetime.date.today()
        self.enable_input_mode = enable_input_mode
        self.keyboard_support = keyboard_support
        self.is_datepicker_open = False

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
        self.is_input_mode = False  # New input mode state
        self.input_error = ""  # Store input validation error
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

    def move_to_previous_day(self):
        """Move to previous day, crossing month boundaries if needed"""
        if self.selected_date.day > 1:
            # Move within current month
            new_day = self.selected_date.day - 1
            self.selected_date = jdatetime.date(self.selected_date.year, self.selected_date.month, new_day)
        else:
            # Move to last day of previous month
            if self.selected_date.month > 1:
                # Previous month in same year
                prev_month = self.selected_date.month - 1
                prev_year = self.selected_date.year
            else:
                # Previous month is December of previous year
                prev_month = 12
                prev_year = self.selected_date.year - 1

            # Check if the new year is within valid range
            if prev_year >= self.first_year:
                days_in_prev_month = self.get_month_days(prev_year, prev_month)
                self.selected_date = jdatetime.date(prev_year, prev_month, days_in_prev_month)
                self.display_year = prev_year
                self.display_month = prev_month

    def move_to_next_day(self):
        """Move to next day, crossing month boundaries if needed"""
        days_in_current_month = self.get_month_days(self.selected_date.year, self.selected_date.month)

        if self.selected_date.day < days_in_current_month:
            # Move within current month
            new_day = self.selected_date.day + 1
            self.selected_date = jdatetime.date(self.selected_date.year, self.selected_date.month, new_day)
        else:
            # Move to first day of next month
            if self.selected_date.month < 12:
                # Next month in same year
                next_month = self.selected_date.month + 1
                next_year = self.selected_date.year
            else:
                # Next month is Farvardin of next year
                next_month = 1
                next_year = self.selected_date.year + 1

            # Check if the new year is within valid range
            if next_year <= self.last_year:
                self.selected_date = jdatetime.date(next_year, next_month, 1)
                self.display_year = next_year
                self.display_month = next_month

    def to_english_num(self, persian_text):
        """Convert Persian numerals to English numbers"""
        result = ""
        for char in str(persian_text):
            if char in self.persian_numerals:
                result += str(self.persian_numerals.index(char))
            else:
                result += char
        return result

    def validate_date_input(self, date_string):
        """Validate date input string and return jdatetime.date object or None"""
        try:
            # Convert Persian numerals to English
            date_string = self.to_english_num(date_string.strip())

            # Check format using regex
            if not re.match(r'^\d{4}/\d{1,2}/\d{1,2}$', date_string):
                return None, "فرمت نامعتبر"

            parts = date_string.split('/')
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])

            # Validate ranges
            if not (self.first_year <= year <= self.last_year):
                return None, f"سال باید بین {self.first_year} و {self.last_year} باشد"

            if not (1 <= month <= 12):
                return None, "ماه نامعتبر"

            if not (1 <= day <= 31):
                return None, "روز نامعتبر"

            # Try to create the date
            date_obj = jdatetime.date(year, month, day)
            return date_obj, ""

        except (ValueError, TypeError):
            return None, "تاریخ نامعتبر"

    def format_date_for_input(self, date_obj):
        """Format date for input field"""
        return f"{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}"

    @functools.lru_cache(maxsize=128)
    def get_month_days(self, year, month):
        """Get number of days in a Persian month (cached for performance)"""
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

    def handle_cell_hover(self, e, original_bg, hover_color, page):
        """Handle hover effect for cells - only applies hover color if not already selected"""
        if e.data == "true":  # Mouse enter
            if original_bg is None:  # Only change if no existing background (not selected)
                e.control.bgcolor = hover_color
        else:  # Mouse leave
            e.control.bgcolor = original_bg
        page.update()

    def create_calendar_grid(self, on_date_click, theme_colors, page):
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
                        on_click=lambda e, day=day_counter: on_date_click(day),
                        on_hover=lambda e, original_bg=bg_color: self.handle_cell_hover(e, original_bg, theme_colors[
                            'cell_hover_color'], page)
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

    def create_year_grid(self, on_year_click, theme_colors, page):
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

                bg_color = theme_colors["text_primary_bgcolor"] if is_selected else None

                year_cell = ft.Container(
                    content=ft.Text(
                        self.to_persian_num(year),
                        color=theme_colors["selected_text_color"] if is_selected else theme_colors["text_primary"],
                        weight=self.config.YEAR_CELL_FONT_WEIGHT,
                        size=self.config.YEAR_CELL_FONT_SIZE
                    ),
                    width=self.config.YEAR_CELL_WIDTH,
                    height=self.config.YEAR_CELL_HEIGHT,
                    bgcolor=bg_color,
                    border_radius=self.config.YEAR_CELL_BORDER_RADIUS,
                    alignment=ft.alignment.center,
                    on_click=lambda e, y=year: on_year_click(y),
                    on_hover=lambda e, original_bg=bg_color: self.handle_cell_hover(e, original_bg,
                                                                                    theme_colors['cell_hover_color'],
                                                                                    page)
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

    def create_input_mode_view(self, theme_colors):
        """Create the input mode view with text field"""
        input_field = ft.TextField(
            color=theme_colors["input_color"],
            value=self.format_date_for_input(self.selected_date),
            hint_text=self.config.INPUT_MODE_PLACEHOLDER,
            text_align=ft.TextAlign.CENTER,
            rtl=False,  # Date format is LTR
            border_color=theme_colors["input_color"],
            focused_border_color=theme_colors["input_focus_border_color"],
            text_size=self.config.INPUT_TEXT_FONT_SIZE,
            content_padding=ft.padding.all(12),
        )

        error_text = ft.Text(
            value=self.input_error,
            color=theme_colors["error_text_color"],
            size=self.config.ERROR_TEXT_FONT_SIZE,
            visible=bool(self.input_error),
            text_align=ft.TextAlign.CENTER
        )

        input_container = ft.Column(
            [
                ft.Container(
                    content=ft.Text(
                        "تاریخ را وارد کنید:",
                        color=theme_colors["text_primary"],
                        size=self.config.HEADER_TEXT_FONT_SIZE,
                        text_align=ft.TextAlign.CENTER
                    ),
                    margin=ft.margin.only(bottom=20)
                ),
                input_field,
                error_text
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            height=self.config.CALENDAR_CONTAINER_HEIGHT
        )

        return input_container, input_field, error_text

    def close_datepicker(self, page):
        """Close the floating datepicker"""
        if self.overlay_container and self.overlay_container in page.overlay:
            page.overlay.remove(self.overlay_container)

            # Restore original keyboard handler if it was stored
            if self.keyboard_support and hasattr(self, '_original_keyboard_handler'):
                page.on_keyboard_event = self._original_keyboard_handler

            self.is_datepicker_open = False
            page.update()

    def show(self, page: ft.Page, is_theme_light: bool = True, display_year: Optional[int] = None,
             display_month: Optional[int] = None, reset_to_default: bool = True):
        """
        Show the Persian DatePicker as a floating overlay.

        Args:
            page (ft.Page): The Flet page to display the datepicker on
            is_theme_light (bool): True for light theme, False for dark theme
            display_year (int, optional): The year to display when opening. If provided, selects first day of specified period.
            display_month (int, optional): The month to display when opening (1-12). If provided, selects first day of specified period.
            reset_to_default (bool): If True, resets selected_date to default_date when showing (only if no display params provided). Default is True.

        Returns:
            Container: The overlay container reference

        Behavior:
        - No display_year, No display_month: Show default_date (today or custom default)
        - Only display_year: Select first day of first month (Farvardin) of given year
        - Only display_month: Select first day of given month in current year
        - Both display_year and display_month: Select first day of given month in given year
        """
        # Determine the target date based on provided parameters
        current_year = jdatetime.date.today().year

        if display_year is not None or display_month is not None:
            # User provided specific year/month parameters - select first day of that period

            if display_year is not None and display_month is not None:
                # Case 3: Both year and month provided - first day of given month in given year
                target_year = display_year
                target_month = display_month
            elif display_year is not None and display_month is None:
                # Case 1: Only year provided - first day of first month (Farvardin) of given year
                target_year = display_year
                target_month = 1  # Farvardin (first month)
            else:  # display_month is not None and display_year is None
                # Case 2: Only month provided - first day of given month in current year
                target_year = current_year
                target_month = display_month

            # Set selected date to first day of the determined period
            self.selected_date = jdatetime.date(target_year, target_month, 1)
            self.display_year = target_year
            self.display_month = target_month

        else:
            # No specific year/month provided - use default behavior
            if reset_to_default:
                self.selected_date = self.default_date

            # Navigate to selected date's month/year
            self.display_year = self.selected_date.year
            self.display_month = self.selected_date.month

        # Reset modes to ensure clean start
        self.is_year_mode = False
        self.is_input_mode = False
        self.input_error = ""

        return self.create_datepicker(page, is_theme_light)

    def show_specific_date(self, page: ft.Page, target_date: jdatetime.date, is_theme_light: bool = True):
        """
        Show datepicker navigated to target_date's month, with target_date selected.
        This makes target_date the new default and selects it.

        Args:
            page (ft.Page): The Flet page to display the datepicker on
            target_date (jdatetime.date): The date to select and navigate to
            is_theme_light (bool): True for light theme, False for dark theme
        """
        # Set target_date as new default and selected date
        self.default_date = target_date
        self.selected_date = target_date

        # Set display to show target_date's month/year
        self.display_year = target_date.year
        self.display_month = target_date.month

        # Reset modes to ensure clean start
        self.is_year_mode = False
        self.is_input_mode = False
        self.input_error = ""

        return self.create_datepicker(page, is_theme_light)


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
            if not self.is_input_mode:  # Only toggle year mode if not in input mode
                self.is_year_mode = not self.is_year_mode

                # Rotate the dropdown icon based on mode
                if self.is_year_mode:
                    dropdown_icon.rotate = 3.14159  # π radians = 180 degrees
                else:
                    dropdown_icon.rotate = 0  # 0 degrees

                update_calendar_view()

        def on_year_click(year):
            """Handle year selection"""
            self.display_year = year
            self.is_year_mode = False
            update_calendar_view()

        def on_mode_toggle(e):
            """Toggle between input mode and calendar mode"""
            if not self.enable_input_mode:
                return

            self.is_input_mode = not self.is_input_mode

            if self.is_input_mode:
                # Switching to input mode
                self.temp_input_value = self.format_date_for_input(self.selected_date)
                if mode_toggle_button:
                    mode_toggle_button.icon = self.config.CALENDAR_MODE_ICON
                    mode_toggle_button.tooltip = self.config.CALENDAR_MODE_BUTTON_TOOLTIP
                datepicker.height = self.config.DATEPICKER_INPUT_MODE_HEIGHT
            else:
                # Switching FROM input mode - ALWAYS go to calendar mode (not year mode)
                self.is_year_mode = False  # Force calendar mode

                # Reset dropdown icon rotation to normal (not rotated)
                dropdown_icon.rotate = 0  # Reset year button icon

                # Validate and apply input date if valid
                if hasattr(update_calendar_view, 'input_field') and update_calendar_view.input_field:
                    input_value = update_calendar_view.input_field.value
                    date_obj, error = self.validate_date_input(input_value)

                    if date_obj:
                        # Valid date - update everything
                        self.selected_date = date_obj
                        self.display_year = date_obj.year
                        self.display_month = date_obj.month
                        self.input_error = ""
                    else:
                        # Invalid date - keep current date and show error briefly
                        self.input_error = error

                if mode_toggle_button:
                    mode_toggle_button.icon = self.config.INPUT_MODE_ICON
                    mode_toggle_button.tooltip = self.config.INPUT_MODE_BUTTON_TOOLTIP
                datepicker.height = self.config.DATEPICKER_CALENDAR_MODE_HEIGHT

                # Clear error when switching to calendar mode (if no validation error)
                if not hasattr(update_calendar_view, 'input_field') or not update_calendar_view.input_field:
                    self.input_error = ""

            update_calendar_view()

        def on_ok_click(e):
            """Handle OK button click"""
            # If in input mode, validate input first
            if self.is_input_mode and hasattr(update_calendar_view, 'input_field'):
                input_value = update_calendar_view.input_field.value
                date_obj, error = self.validate_date_input(input_value)

                if date_obj:
                    self.selected_date = date_obj
                    self.input_error = ""
                else:
                    # Show error and don't close
                    self.input_error = error
                    update_calendar_view.error_text.value = error
                    update_calendar_view.error_text.visible = True
                    page.update()
                    return

            # Get complete date information
            date_info = self.get_selected_date_info()
            self.result = date_info

            # Call callback if provided
            if self.on_result_callback:
                self.on_result_callback(date_info)

            # Restore original keyboard handler (only if keyboard support is enabled)
            if self.keyboard_support and hasattr(self,
                                                 '_original_keyboard_handler') and self._original_keyboard_handler is not None:
                page.on_keyboard_event = self._original_keyboard_handler
                self.is_datepicker_open = False

            # Close the floating datepicker
            self.close_datepicker(page)

        def on_cancel_click(e):
            """Handle Cancel button click"""
            self.result = None

            # Call callback if provided
            if self.on_result_callback:
                self.on_result_callback(None)

            # Restore original keyboard handler (only if keyboard support is enabled)
            if self.keyboard_support and hasattr(self,
                                                 '_original_keyboard_handler') and self._original_keyboard_handler is not None:
                page.on_keyboard_event = self._original_keyboard_handler
                self.is_datepicker_open = False

            # Close the floating datepicker
            self.close_datepicker(page)

        def on_today_click(e):
            """Handle today button click - navigate to current date"""
            today = jdatetime.date.today()
            self.selected_date = today
            self.display_year = today.year
            self.display_month = today.month
            self.is_year_mode = False  # Ensure we're in calendar mode
            self.is_input_mode = False  # Exit input mode
            self.input_error = ""  # Clear any errors
            update_calendar_view()

        def on_overlay_click(e):
            """Handle clicks on the overlay background (outside datepicker)"""
            # Close datepicker when clicking outside
            self.result = None
            if self.on_result_callback:
                self.on_result_callback(None)

            # Restore original keyboard handler (only if keyboard support is enabled)
            if self.keyboard_support and hasattr(self,
                                                 '_original_keyboard_handler') and self._original_keyboard_handler is not None:
                page.on_keyboard_event = self._original_keyboard_handler
                self.is_datepicker_open = False

            self.close_datepicker(page)

        # Keyboard event handling (only if keyboard support is enabled)
        if self.keyboard_support:
            def on_page_keyboard(e: ft.KeyboardEvent):
                """Handle keyboard events when datepicker is open"""
                # Only handle events if datepicker is open
                if not self.is_datepicker_open:
                    # Call original handler if it exists
                    if self._original_keyboard_handler:
                        self._original_keyboard_handler(e)
                    return

                if e.key == "Escape":
                    on_cancel_click(e)
                elif e.key == "Enter":
                    on_ok_click(e)
                elif not self.is_year_mode and not self.is_input_mode:  # Only in calendar mode
                    if e.key == "D":
                        # Move to previous day with month boundary crossing
                        self.move_to_previous_day()
                        update_calendar_view()
                    elif e.key == "A":
                        # Move to next day with month boundary crossing
                        self.move_to_next_day()
                        update_calendar_view()
                    elif e.key == "W":
                        # Move to previous week (W key - minus 7 days) - stay within month
                        if self.selected_date.day > 7:
                            new_day = self.selected_date.day - 7
                            self.selected_date = jdatetime.date(self.selected_date.year, self.selected_date.month, new_day)
                            update_calendar_view()
                    elif e.key == "S":
                        # Move to next week (S key - plus 7 days) - stay within month
                        days_in_current_month = self.get_month_days(self.selected_date.year, self.selected_date.month)
                        new_day = self.selected_date.day + 7
                        if new_day <= days_in_current_month:
                            self.selected_date = jdatetime.date(self.selected_date.year, self.selected_date.month, new_day)
                            update_calendar_view()
                else:
                    # For other keys or modes, call original handler if it exists
                    if self._original_keyboard_handler:
                        self._original_keyboard_handler(e)

        # Selected date panel (right side for RTL)
        selected_date_text = ft.Text(
            self.format_selected_date(),
            color=theme_colors['text_secondary'],
            size=self.config.SELECTED_DATE_FONT_SIZE_CALENDAR_MODE,
            weight=self.config.SELECTED_DATE_FONT_WEIGHT,
            text_align=ft.TextAlign.RIGHT
        )

        buttons_row = None
        mode_toggle_button = None  # Initialize before creating the row

        if self.enable_input_mode:
            # Create the mode toggle button separately for easier reference
            mode_toggle_button = ft.IconButton(
                icon=self.config.INPUT_MODE_ICON,
                icon_size=self.config.EDIT_ICON_SIZE,
                icon_color=theme_colors['text_header'],
                tooltip=self.config.INPUT_MODE_BUTTON_TOOLTIP,
                on_click=on_mode_toggle,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=self.config.NAV_BUTTON_BORDER_RADIUS)
                )
            )

            buttons_row = ft.Row(
                [
                    mode_toggle_button,  # Use the variable we created
                    ft.ElevatedButton(
                        text=self.config.TODAY_BUTTON_TEXT,
                        style=ft.ButtonStyle(
                            bgcolor=theme_colors['secondary_color'],
                            color=theme_colors['selected_text_color'],
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=on_today_click,
                        tooltip=self.config.TODAY_BUTTON_TOOLTIP
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                spacing=8
            )
        else:
            # If input mode is disabled, show only today button
            buttons_row = ft.Row(
                [
                    ft.ElevatedButton(
                        text=self.config.TODAY_BUTTON_TEXT,
                        style=ft.ButtonStyle(
                            bgcolor=theme_colors['secondary_color'],
                            color=theme_colors['selected_text_color'],
                            padding=ft.padding.symmetric(horizontal=12, vertical=6),
                            shape=ft.RoundedRectangleBorder(radius=8)
                        ),
                        on_click=on_today_click,
                        tooltip=self.config.TODAY_BUTTON_TOOLTIP
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )

        action_buttons_row_control = ft.Container(
            content=buttons_row,
            margin=ft.margin.only(top=self.config.EDIT_ICON_TOP_MARGIN_CALENDAR_MODE),
            alignment=ft.alignment.center_right
        )

        right_panel_controls = [
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
            action_buttons_row_control
        ]

        right_panel = ft.Container(
            content=ft.Column(
                right_panel_controls,
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

        dropdown_icon = ft.Icon(
            name=self.config.DROPDOWN_ICON,
            color=theme_colors['text_muted'],
            size=self.config.DROPDOWN_ICON_SIZE,
            rotate=0,  # Initial rotation
            animate_rotation=ft.Animation(duration=250, curve=ft.AnimationCurve.EASE_OUT_SINE)
        )

        calendar_year_select_button = ft.TextButton(
            content=ft.Row(
                controls=[
                    self.month_year_text,
                    dropdown_icon
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
                margin=ft.margin.only(top=self.config.ACTION_BUTTONS_MARGIN_TOP_CALENDAR_MODE)
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
            width=self.config.DATEPICKER_WIDTH + self.config.RIGHT_PANEL_WIDTH,
            height=self.config.DATEPICKER_CALENDAR_MODE_HEIGHT,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        )

        # In the update_calendar_view function, find this section and update it:
        def update_calendar_view():
            """Update the calendar view based on current mode"""
            if self.is_input_mode:
                # Show input field instead of calendar
                nav_buttons.visible = False
                day_headers.visible = False
                calendar_header.visible = False
                selected_date_text.size = self.config.SELECTED_DATE_FONT_SIZE_INPUT_MODE
                action_buttons_row_control.margin.top = self.config.EDIT_ICON_TOP_MARGIN_INPUT_MODE
                calendar_container.height = self.config.CALENDAR_CONTAINER_HEIGHT_INPUT_MODE

                top_calendar_container_dividers.visible = False
                bottom_calendar_container_dividers.visible = False

                # Create input field - STORE THE TEXTFIELD DIRECTLY, NOT THE CONTAINER
                input_field = ft.TextField(
                    color=theme_colors["input_color"],
                    label=self.config.INPUT_MODE_LABEL,
                    label_style=ft.TextStyle(
                        color=theme_colors["input_color"],
                    ),
                    value=self.format_date_for_input(self.selected_date),
                    hint_text=self.config.INPUT_MODE_PLACEHOLDER,
                    text_align=ft.TextAlign.RIGHT,
                    rtl=False,  # Date format is LTR
                    border_color=theme_colors.get("input_color", theme_colors["text_muted"]),
                    focused_border_color=theme_colors.get("input_focus_border_color", theme_colors["secondary_color"]),
                    text_size=getattr(self.config, 'INPUT_TEXT_FONT_SIZE', 16),
                    content_padding=ft.padding.all(12),
                )

                input_container = ft.Container(
                    content=input_field,
                    margin=ft.margin.only(top=self.config.TEXT_FIELD_MARGIN_TOP)
                )

                error_text = ft.Text(
                    value=self.input_error,
                    color=theme_colors["error_text_color"] if "error_text_color" in theme_colors else ft.Colors.RED,
                    size=self.config.ERROR_TEXT_FONT_SIZE if hasattr(self.config, 'ERROR_TEXT_FONT_SIZE') else 12,
                    visible=bool(self.input_error),
                    text_align=ft.TextAlign.CENTER
                )

                main_input_container = ft.Column(
                    [
                        input_container,
                        error_text
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )

                calendar_container.controls = [main_input_container]

                # Store references for OK button validation - NOW STORING THE TEXTFIELD OBJECT
                update_calendar_view.input_field = input_field  # This is now the TextField, not Container
                update_calendar_view.error_text = error_text

                # Ensure input mode height
                datepicker.height = self.config.DATEPICKER_INPUT_MODE_HEIGHT
                action_buttons.margin.top = self.config.ACTION_BUTTONS_MARGIN_TOP_INPUT_MODE

            elif self.is_year_mode:
                # Hide navigation buttons and day headers, show year grid
                nav_buttons.visible = False
                day_headers.visible = False
                calendar_header.visible = True
                selected_date_text.size = self.config.SELECTED_DATE_FONT_SIZE_CALENDAR_MODE
                action_buttons_row_control.margin.top = self.config.EDIT_ICON_TOP_MARGIN_CALENDAR_MODE
                calendar_container.height = self.config.CALENDAR_CONTAINER_HEIGHT_INPUT_MODE

                top_calendar_container_dividers.visible = True
                bottom_calendar_container_dividers.visible = True
                year_rows = self.create_year_grid(on_year_click, theme_colors, page)
                calendar_container.controls = year_rows
                action_buttons.margin.top = self.config.ACTION_BUTTONS_MARGIN_TOP_YEAR_MODE
                # Ensure full height for year mode
                datepicker.height = self.config.DATEPICKER_CALENDAR_MODE_HEIGHT
                calendar_container.height = self.config.CALENDAR_CONTAINER_HEIGHT_CALENDAR_MODE

            else:
                # Show navigation buttons and day headers, show calendar grid
                nav_buttons.visible = True
                day_headers.visible = True
                calendar_header.visible = True
                selected_date_text.size = self.config.SELECTED_DATE_FONT_SIZE_CALENDAR_MODE
                action_buttons_row_control.margin.top = self.config.EDIT_ICON_TOP_MARGIN_CALENDAR_MODE
                calendar_container.height = self.config.CALENDAR_CONTAINER_HEIGHT_CALENDAR_MODE

                top_calendar_container_dividers.visible = False
                bottom_calendar_container_dividers.visible = False
                calendar_rows = self.create_calendar_grid(on_date_click, theme_colors, page)
                calendar_container.controls = calendar_rows
                selected_date_text.value = self.format_selected_date()
                action_buttons.margin.top = self.config.ACTION_BUTTONS_MARGIN_TOP_CALENDAR_MODE
                # Ensure full height for calendar mode
                datepicker.height = self.config.DATEPICKER_CALENDAR_MODE_HEIGHT

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

        if self.keyboard_support:
            self._original_keyboard_handler = page.on_keyboard_event
            page.on_keyboard_event = on_page_keyboard
            self.is_datepicker_open = True
        else:
            # If keyboard support is disabled, don't override page handler
            self._original_keyboard_handler = None
            self.is_datepicker_open = False

        # Add to page overlay
        page.overlay.append(self.overlay_container)
        page.update()

        return self.overlay_container