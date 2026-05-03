from victoria.transformer import JsonTransformer, RawTransformer
from victoria.transformer.base import MessageTransformer
from victoria.schema.message import VictoriaPrintMessage, IpcMessageType
import json
import pytest


class TestJsonTransformer:
    def test_is_message_transformer(self):
        t = JsonTransformer()
        assert isinstance(t, MessageTransformer)

    def test_transform_valid_json(self):
        t = JsonTransformer()
        data = {
            "device": "my-device",
            "origin": "my-origin",
            "title": "Test Title",
            "barcode": "ABC123",
        }
        result = t.transform(json.dumps(data))
        assert isinstance(result, VictoriaPrintMessage)
        assert result.device == "my-device"
        assert result.origin == "my-origin"
        assert result.title == "Test Title"
        assert result.barcode == "ABC123"

    def test_transform_with_number(self):
        t = JsonTransformer()
        data = {
            "device": "dev",
            "origin": "app",
            "title": "T",
            "barcode": "B",
            "number": 5,
        }
        result = t.transform(json.dumps(data))
        assert result.number == 5

    def test_transform_default_number(self):
        t = JsonTransformer()
        data = {
            "device": "dev",
            "origin": "app",
            "title": "T",
            "barcode": "B",
        }
        result = t.transform(json.dumps(data))
        assert result.number == 1

    def test_transform_default_type(self):
        t = JsonTransformer()
        data = {
            "device": "dev",
            "origin": "app",
            "title": "T",
            "barcode": "B",
        }
        result = t.transform(json.dumps(data))
        assert result.type == IpcMessageType.PRINT

    def test_transform_invalid_json_raises(self):
        t = JsonTransformer()
        with pytest.raises(json.JSONDecodeError):
            t.transform("not valid json")

    def test_transform_missing_fields_raises(self):
        t = JsonTransformer()
        with pytest.raises(TypeError):
            t.transform(json.dumps({"device": "dev"}))


class TestRawTransformer:
    def test_is_message_transformer(self):
        t = RawTransformer()
        assert isinstance(t, MessageTransformer)

    def test_transform_returns_message(self):
        t = RawTransformer()
        result = t.transform("some-raw-input")
        assert isinstance(result, VictoriaPrintMessage)

    def test_transform_barcode_set_to_content(self):
        t = RawTransformer()
        result = t.transform("hello-world")
        assert result.barcode == "hello-world"

    def test_transform_device_empty(self):
        t = RawTransformer()
        result = t.transform("input")
        assert result.device == ""

    def test_transform_origin_empty(self):
        t = RawTransformer()
        result = t.transform("input")
        assert result.origin == ""

    def test_transform_title_empty(self):
        t = RawTransformer()
        result = t.transform("input")
        assert result.title == ""

    def test_transform_default_number(self):
        t = RawTransformer()
        result = t.transform("input")
        assert result.number == 1

    def test_transform_default_type(self):
        t = RawTransformer()
        result = t.transform("input")
        assert result.type == IpcMessageType.PRINT

    def test_transform_empty_string(self):
        t = RawTransformer()
        result = t.transform("")
        assert result.barcode == ""
