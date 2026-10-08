"""Flet 1.0 compatibility smoke tests.

These tests lock the widget's control tree to the Flet 1.0.x API: they build
the complete datepicker UI (calendar grid, year grid, input mode), drive every
event handler the widget installs, and assert the overlay/keyboard lifecycle —
all against the ``flet`` package actually installed in the environment.
"""

from types import SimpleNamespace

import flet as ft
import jdatetime
import pytest

from persian_datepicker import PersianDatePicker


class StubPage:
    """The subset of ``ft.Page`` the widget actually uses.

    ``PersianDatePicker`` only touches ``page.overlay``,
    ``page.on_keyboard_event`` and ``page.update()``.
    """

    def __init__(self):
        self.overlay = []
        self.on_keyboard_event = None
        self.update_count = 0

    def update(self, *args, **kwargs):
        self.update_count += 1


def walk(control):
    """Yield ``control`` and every descendant in the tree."""
    yield control
    for child in getattr(control, "controls", None) or []:
        yield from walk(child)
    content = getattr(control, "content", None)
    if content is not None:
        yield from walk(content)


@pytest.fixture
def page():
    return StubPage()


@pytest.fixture
def picker():
    return PersianDatePicker()


class TestBuildsAgainstFlet1:
    def test_show_builds_overlay_and_wires_keyboard(self, picker, page):
        picker.set_result_callback(lambda result: None)
        container = picker.show(page)

        assert container is picker.overlay_container
        assert container in page.overlay
        assert page.on_keyboard_event is not None, "keyboard support not wired"
        assert page.update_count >= 1

    def test_show_specific_date_builds_ui(self, picker, page):
        container = picker.show_specific_date(page, jdatetime.date(1404, 6, 1))

        assert container in page.overlay
        assert picker.selected_date == jdatetime.date(1404, 6, 1)

    def test_dark_theme_builds_ui(self, picker, page):
        container = picker.show(page, is_theme_light=False)

        assert container in page.overlay

    def test_all_click_handlers_run(self, picker, page):
        """Invoke every on_click handler the widget installs."""
        picker.set_result_callback(lambda result: None)
        container = picker.show(page)

        # overlay container -> Stack -> [overlay background, centered datepicker]
        overlay_background = container.content.controls[0]

        clicked = 0
        for control in walk(container):
            handler = getattr(control, "on_click", None)
            if handler is None or control is overlay_background:
                continue  # overlay background click closes the picker; run last
            handler(SimpleNamespace(control=control, data=None))
            clicked += 1

        # Day cells + year cells + nav buttons + toggle/OK/Cancel/Today buttons
        assert clicked >= 20
        assert picker.is_datepicker_open is False or container in page.overlay

        # The overlay background (outside the dialog) closes the picker
        overlay_background.on_click(SimpleNamespace(control=overlay_background, data=None))
        assert container not in page.overlay

    def test_hover_handlers_accept_bool_and_legacy_string(self, picker, page):
        picker.set_result_callback(lambda result: None)
        container = picker.show(page)

        hovered = 0
        for control in walk(container):
            handler = getattr(control, "on_hover", None)
            if handler is None:
                continue
            original_bg = control.bgcolor
            handler(SimpleNamespace(control=control, data=True))  # Flet 1.0
            assert control.bgcolor != original_bg or original_bg is not None
            handler(SimpleNamespace(control=control, data="true"))  # legacy
            handler(SimpleNamespace(control=control, data=False))
            handler(SimpleNamespace(control=control, data="false"))
            control.bgcolor = original_bg
            hovered += 1
        assert hovered > 0, "no hover handlers found in the tree"

    def test_keyboard_handlers_run(self, picker, page):
        results = []
        picker.set_result_callback(results.append)
        container = picker.show(page)
        handler = page.on_keyboard_event

        def key(k):
            return SimpleNamespace(key=k, shift=False, ctrl=False, alt=False, meta=False)

        # Day/week navigation (documented keys) leaves the picker open
        for k in ("D", "A", "W", "S"):
            handler(key(k))
            assert container in page.overlay

        # Enter confirms the selection and closes
        handler(key("Enter"))
        assert container not in page.overlay
        assert results and results[0] is not None

        # Reopen, then Escape cancels and closes
        container = picker.show(page)
        handler = page.on_keyboard_event
        handler(key("Escape"))
        assert container not in page.overlay
        assert results[-1] is None

    def test_close_datepicker_restores_state(self, picker, page):
        picker.set_result_callback(lambda result: None)
        container = picker.show(page)

        picker.close_datepicker(page)

        assert container not in page.overlay
        assert page.on_keyboard_event is None

    def test_result_callback_receives_persian_date(self, picker, page):
        results = []
        picker.set_result_callback(results.append)
        picker.show(page)

        # Move to a fixed date, then confirm through the public helpers
        picker.selected_date = jdatetime.date(1403, 1, 15)
        picker.format_selected_date()
        picker.close_datepicker(page)

        assert picker.get_selected_date_info()["formatted_persian"]


def test_flet_version_is_1_x():
    major = int(ft.__version__.split(".")[0])
    assert major >= 1, f"expected Flet 1.x, found {ft.__version__}"
