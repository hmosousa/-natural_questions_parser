import json
import pytest

from main import Offset, Entry


@pytest.fixture
def entry():
    with open("example.json") as f:
        content = json.load(f)
    return content


class TestOffset:
    def test_contains(self):
        assert Offset(10, 20) in Offset(0, 30)
        assert Offset(0, 30) not in Offset(10, 20)
        assert Offset(10, 20) in Offset(10, 20)
        assert Offset(10, 20) in Offset(10, 30)
        assert Offset(10, 20) in Offset(0, 20)


class TestEntry:
    def test_format(self, entry):
        e = Entry(**entry)
        r = e.format()
        assert r is not None
