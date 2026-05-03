from victoria.template import TemplateZpl, TemplateJson
from victoria.schema.message import VictoriaPrintMessage
from victoria.schema.type import PrinterDialectEnum
import json


def _make_msg(**kwargs):
    defaults = {
        "device": "test-device",
        "origin": "test-origin",
        "title": "Test Title",
        "barcode": "ABC123",
    }
    defaults.update(kwargs)
    return VictoriaPrintMessage(**defaults)


class TestTemplateZpl:
    def test_dialect(self):
        t = TemplateZpl(width=100, height=150)
        assert t.dialect == PrinterDialectEnum.ZEBRA_ZPL

    def test_defaults(self):
        t = TemplateZpl()
        assert t.width == 0
        assert t.height == 0
        assert t.rotate is False

    def test_render_contains_zpl_commands(self):
        t = TemplateZpl(width=100, height=150)
        msg = _make_msg()
        result = t.render(msg)
        assert "^XA" in result
        assert "^XZ" in result

    def test_render_contains_title(self):
        t = TemplateZpl(width=100, height=150)
        msg = _make_msg(title="My Product")
        result = t.render(msg)
        assert "My Product" in result

    def test_render_contains_barcode(self):
        t = TemplateZpl(width=100, height=150)
        msg = _make_msg(barcode="BARCODE99")
        result = t.render(msg)
        assert "BARCODE99" in result

    def test_render_width_height_used(self):
        t = TemplateZpl(width=100, height=200)
        msg = _make_msg()
        result = t.render(msg)
        assert "100" in result
        assert "200" in result

    def test_render_rotation_flag(self):
        t_no_rot = TemplateZpl(width=100, height=150, rotate=False)
        t_rot = TemplateZpl(width=100, height=150, rotate=True)
        msg = _make_msg()
        result_no_rot = t_no_rot.render(msg)
        result_rot = t_rot.render(msg)
        assert result_no_rot != result_rot

    def test_render_returns_string(self):
        t = TemplateZpl(width=100, height=150)
        msg = _make_msg()
        result = t.render(msg)
        assert isinstance(result, str)


class TestTemplateJson:
    def test_dialect(self):
        t = TemplateJson(width=100, height=150)
        assert t.dialect == PrinterDialectEnum.JSON

    def test_defaults(self):
        t = TemplateJson()
        assert t.width == 0
        assert t.height == 0

    def test_render_valid_json(self):
        t = TemplateJson(width=100, height=150)
        msg = _make_msg(title="Hello", barcode="XYZ789")
        result = t.render(msg)
        data = json.loads(result)
        assert isinstance(data, dict)

    def test_render_contains_title(self):
        t = TemplateJson(width=100, height=150)
        msg = _make_msg(title="Hello")
        result = t.render(msg)
        data = json.loads(result)
        assert data["title"] == "Hello"

    def test_render_contains_barcode(self):
        t = TemplateJson(width=100, height=150)
        msg = _make_msg(barcode="XYZ789")
        result = t.render(msg)
        data = json.loads(result)
        assert data["barcode"] == "XYZ789"

    def test_render_contains_width_height(self):
        t = TemplateJson(width=100, height=150)
        msg = _make_msg()
        result = t.render(msg)
        data = json.loads(result)
        assert data["width"] == "100"
        assert data["height"] == "150"

    def test_render_returns_string(self):
        t = TemplateJson(width=100, height=150)
        msg = _make_msg()
        result = t.render(msg)
        assert isinstance(result, str)
