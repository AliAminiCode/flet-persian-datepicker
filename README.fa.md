# Flet Persian DatePicker

[🇬🇧 English](README.md) · 🇮🇷 فارسی

یک انتخاب‌گر تاریخ فارسی (جلالی/شمسی) برای [Flet](https://flet.dev) نسخه‌ی ۱.x. `DatePicker` داخلی Flet فقط تقویم میلادی و متن انگلیسی نمایش می‌دهد. این پکیج تقویم جلالی را با نام ماه و روز فارسی، اعداد فارسی و چیدمان راست‌به‌چپ (RTL) اضافه می‌کند و ظاهرش شبیه انتخاب‌گر داخلی است.

## ویژگی‌ها

- **تقویم جلالی**: نام ماه و روز فارسی، اعداد فارسی، چیدمان RTL.
- **دو حالت**: انتخاب از روی تقویم، یا تایپ مستقیم تاریخ (با اعداد فارسی یا انگلیسی). تاریخ تایپ‌شده از نظر فرمت و محدوده بررسی می‌شود و خطاها به فارسی نمایش داده می‌شوند.
- **ناوبری با صفحه‌کلید**: تأیید، لغو و جابه‌جایی بین روزها و هفته‌ها (بخش [میانبرهای صفحه‌کلید](#میانبرهای-صفحهکلید) را ببینید).
- **دکمه‌ی «امروز»** و برجسته‌سازی تاریخ پیش‌فرض و آخرین تاریخ انتخاب‌شده.
- **تم روشن و تاریک** و محدوده‌ی سال قابل تنظیم.
- **حداقل وابستگی**: فقط `flet` و `jdatetime`.

### تفاوت با `ft.DatePicker`

ظاهر و حس استفاده از انتخاب‌گر داخلی Flet پیروی می‌کند، ولی API آن مستقل است: یک `PersianDatePicker` می‌سازید، یک callback برای نتیجه ثبت می‌کنید و `show(page)` را صدا می‌زنید. این پکیج جایگزین مستقیم (drop-in) `ft.DatePicker` نیست و هنگام جایگزینی در کد موجود، تغییرات کوچکی لازم است.

## نصب

```bash
pip install persian-datepicker
```

نیازمند **Python 3.10+** و **Flet 1.0.1+** است.

### سازگاری نسخه‌ها

| نسخه‌ی کتابخانه | نسخه‌ی Flet | دستور نصب |
|---|---|---|
| 2.x | 1.0.1 یا بالاتر (کمتر از 2.0) | `pip install persian-datepicker` |
| 1.x | 0.28.x یا قدیمی‌تر | `pip install "persian-datepicker<2" "flet<1"` |

Flet 1.0 بسیاری از API‌ها را تغییر نام داده یا حذف کرده است، بنابراین نسخه‌ی 2.0.0 و بالاتر روی Flet 0.x اجرا نمی‌شود. جزئیات تغییرات در [CHANGELOG.md](CHANGELOG.md) آمده است.

## شروع سریع

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

با کلیک روی دکمه، انتخاب‌گر باز می‌شود. وقتی تاریخی تأیید شود، callback یک دیکشنری نتیجه دریافت می‌کند؛ مقدار `result['formatted_persian']` تاریخ را با قالب فارسی نگه می‌دارد.

<!-- TODO: همه‌ی کلیدهای دیکشنری نتیجه را با یک توضیح یک‌خطی برای هرکدام فهرست کنید (مثلاً نام مقدار میلادی و شیء تاریخ). -->

## نحوه‌ی استفاده

| چه می‌خواهید | چطور |
|---|---|
| محدود کردن سال‌های قابل انتخاب | `PersianDatePicker(first_year=1400, last_year=1410)` |
| شروع از یک تاریخ مشخص | `datepicker.set_default_date(jdatetime.date(1404, 6, 1))` (یک `jdatetime.date` می‌گیرد، نه رشته) |
| باز شدن در یک ماه مشخص | `datepicker.show(page, display_year=1403, display_month=6)` |
| خاموش کردن ورود تایپی | `PersianDatePicker(enable_input_mode=False)` |
| خاموش کردن میانبرهای صفحه‌کلید | `PersianDatePicker(keyboard_support=False)` |

مثال‌های اجرایی:

- `examples/example_basic.py`: همه‌ی گزینه‌های بالا.
- `examples/example_mini_project.py`: یک برنامه‌ی کوچک برنامه‌ریز رویداد ساخته‌شده با این ویجت.

## میانبرهای صفحه‌کلید

میانبرها فقط وقتی انتخاب‌گر باز و در حالت تقویم باشد کار می‌کنند. در حالت انتخاب سال و حالت ورود تایپی غیرفعال‌اند، پس تایپ هیچ‌وقت مختل نمی‌شود.

| کلید | عملکرد |
|---|---|
| `Enter` | تأیید تاریخ انتخاب‌شده |
| `Esc` | لغو و بستن |
| `D` | روز قبل (می‌تواند به ماه قبل برود) |
| `A` | روز بعد (می‌تواند به ماه بعد برود) |
| `W` | هفته‌ی قبل (در همان ماه می‌ماند) |
| `S` | هفته‌ی بعد (در همان ماه می‌ماند) |

## تست

`pytest` منطق تاریخ و اعتبارسنجی را پوشش می‌دهد: سال کبیسه، عبور از مرز ماه و سال، و تجزیه‌ی ورودی. رفتار رابط کاربری ویجت با smoke test و تست دستی بررسی می‌شود.

```bash
pip install -e ".[dev]"
pytest tests/
```

## تصاویر

**حالت روشن**

<div align="center">
  <img src="screenshots/light_mode_landscape.png" alt="Persian DatePicker در حالت روشن">
</div>

**حالت تاریک**

<div align="center">
  <img src="screenshots/dark_mode_landscape.png" alt="Persian DatePicker در حالت تاریک">
</div>

## تاریخچه‌ی تغییرات

تاریخچه‌ی نسخه‌ها در [CHANGELOG.md](CHANGELOG.md) است.

## مشارکت و پشتیبانی

باگ پیدا کردید یا قابلیتی پیشنهاد دارید؟ یک issue باز کنید: <https://github.com/AliAminiCode/flet-persian-datepicker/issues>. هنگام گزارش باگ، نسخه‌ی Python، Flet و کتابخانه را بنویسید و یک کد کوتاه که مشکل را بازتولید می‌کند ضمیمه کنید.

## مجوز

[MIT](https://github.com/AliAminiCode/flet-persian-datepicker/blob/master/LICENSE). توسعه‌دهنده: [Ali Amini](mailto:aliamini9728@gmail.com).
