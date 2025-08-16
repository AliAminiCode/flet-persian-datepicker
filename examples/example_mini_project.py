"""
Persian DatePicker Mini Project: Event Planner
==============================================
A simple event planning app using Persian DatePicker.
Users can add events with Persian dates and view them in a list.
"""

import flet as ft
import jdatetime
from persian_datepicker_project.persian_datepicker import PersianDatePicker


def main(page: ft.Page):
    page.title = "برنامه‌ریز رویداد فارسی"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 800
    page.window.height = 600
    page.padding = 20

    # Data storage
    events = []

    # UI Components
    event_title = ft.TextField(
        label="نام رویداد",
        hint_text="مثال: جلسه کاری، تولد، مسافرت",
        width=300
    )

    selected_date_text = ft.Text("تاریخی انتخاب نشده", size=14, color=ft.Colors.GREY_600)
    selected_date = None

    events_list = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)

    def on_date_selected(result):
        """Handle date selection"""
        nonlocal selected_date
        if result:
            selected_date = result['date']
            selected_date_text.value = f"📅 {result['formatted_persian']} ({result['day_name']})"
        else:
            selected_date = None
            selected_date_text.value = "تاریخی انتخاب نشده"
        page.update()

    def show_datepicker(e):
        """Show date picker"""
        picker = PersianDatePicker()
        picker.set_result_callback(on_date_selected)
        picker.show(page)

    def add_event(e):
        """Add new event"""
        if not event_title.value.strip():
            show_snackbar("لطفاً نام رویداد را وارد کنید")
            return

        if not selected_date:
            show_snackbar("لطفاً تاریخ را انتخاب کنید")
            return

        # Create event
        event = {
            'title': event_title.value.strip(),
            'date': selected_date,
            'formatted_date': f"{selected_date.year}/{selected_date.month:02d}/{selected_date.day:02d}",
            'day_name': PersianDatePicker().persian_days[selected_date.weekday()]
        }
        events.append(event)

        # Update UI
        update_events_list()
        event_title.value = ""
        selected_date_text.value = "تاریخی انتخاب نشده"
        page.update()

        show_snackbar("رویداد اضافه شد! ✅")

    def delete_event(index):
        """Delete event"""

        def delete_handler(e):
            events.pop(index)
            update_events_list()
            show_snackbar("رویداد حذف شد")

        return delete_handler

    def update_events_list():
        """Update events display"""
        events_list.controls.clear()

        if not events:
            events_list.controls.append(
                ft.Text("هنوز رویدادی اضافه نکرده‌اید",
                        style=ft.TextThemeStyle.BODY_MEDIUM,
                        italic=True,
                        color=ft.Colors.GREY_500)
            )
        else:
            # Sort events by date
            sorted_events = sorted(events, key=lambda x: x['date'])

            for i, event in enumerate(sorted_events):
                # Determine if event is today, past, or future
                today = jdatetime.date.today()
                if event['date'] == today:
                    date_color = ft.Colors.GREEN
                    date_prefix = "🎯 امروز"
                elif event['date'] < today:
                    date_color = ft.Colors.GREY_500
                    date_prefix = "⏮️ گذشته"
                else:
                    date_color = ft.Colors.BLUE
                    date_prefix = "⏭️ آینده"

                event_card = ft.Container(
                    content=ft.Row([
                        ft.Column([
                            ft.Text(event['title'],
                                    size=16,
                                    weight=ft.FontWeight.BOLD),
                            ft.Text(f"{date_prefix} - {event['formatted_date']} ({event['day_name']})",
                                    size=12,
                                    color=date_color),
                        ], expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_400,
                            tooltip="حذف رویداد",
                            on_click=delete_event(i)
                        )
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE),
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.BLUE))
                )
                events_list.controls.append(event_card)

        page.update()

    def show_snackbar(message):
        """Show snackbar message"""
        page.snack_bar = ft.SnackBar(ft.Text(message))
        page.snack_bar.open = True
        page.update()

    # Initial events list
    update_events_list()

    # UI Layout
    page.add(
        ft.Column([
            # Header
            ft.Text("📅 برنامه‌ریز رویداد فارسی",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER),

            ft.Divider(),

            # Add event section
            ft.Container(
                content=ft.Column([
                    ft.Text("➕ افزودن رویداد جدید", size=18, weight=ft.FontWeight.W_500),

                    event_title,

                    ft.Row([
                        ft.ElevatedButton(
                            "انتخاب تاریخ",
                            icon=ft.Icons.CALENDAR_TODAY,
                            on_click=show_datepicker
                        ),
                        selected_date_text,
                    ], spacing=15),

                    ft.ElevatedButton(
                        "افزودن رویداد",
                        icon=ft.Icons.ADD,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE,
                        ),
                        on_click=add_event
                    ),
                ], spacing=15),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREEN),
                border_radius=15,
                margin=ft.margin.only(bottom=20)
            ),

            # Events list
            ft.Text("📋 رویدادهای شما", size=18, weight=ft.FontWeight.W_500),
            ft.Container(
                content=events_list,
                height=300,
                padding=10,
                bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.GREY),
                border_radius=10,
            )

        ], spacing=10, expand=True)
    )


if __name__ == "__main__":
    ft.app(target=main)