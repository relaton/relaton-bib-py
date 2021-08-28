import dataclasses
import inspect
import pytest

import xml.etree.ElementTree as ET

from relaton_bib.workgroup import WorkGroup


@pytest.fixture
def subj_min():
    return WorkGroup(content="value")


@pytest.fixture
def subj_full():
    return WorkGroup(content="value",
                     number=1,
                     type="type")


def test_min_to_xml(subj_min):
    host = ET.Element("host")
    result = subj_min.to_xml(host)

    assert result.text == "value"


def test_full_to_xml(subj_full):
    host = ET.Element("host")
    result = subj_full.to_xml(host)

    assert result.text == "value"
    assert result.attrib["type"] == "type"
    assert result.attrib["number"] == "1"


def test_min_to_asciibib(subj_min):
    result = subj_min.to_asciibib()

    assert result == "content:: value"


def test_full_to_asciibib(subj_full):
    result = subj_full.to_asciibib()

    assert result == inspect.cleandoc(
        """content:: value
           number:: 1
           type:: type""")


def test_min_to_asciibib_with_pref(subj_min):
    result = subj_min.to_asciibib(prefix="test")

    assert result == "test.content:: value"


def test_full_to_asciibib_with_pref(subj_full):
    result = subj_full.to_asciibib(prefix="test")

    assert result == inspect.cleandoc(
        """test.content:: value
           test.number:: 1
           test.type:: type""")


def test_hash(subj_full):
    result = dataclasses.asdict(subj_full)

    assert result["type"] == "type"
    assert result["number"] == 1
    assert result["content"] == "value"
