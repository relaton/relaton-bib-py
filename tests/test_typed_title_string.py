import dataclasses
import inspect
import pytest

import xml.etree.ElementTree as ET

from relaton_bib.typed_title_string import TypedTitleString
from relaton_bib.formatted_string import FormattedString


def test_missing_title_or_content():
    with pytest.raises(ValueError) as excinfo:
        TypedTitleString(type="type")
    assert "Argument title or content should be passed" in str(excinfo.value)


@pytest.fixture
def subject():
    return TypedTitleString(
        type="main",
        title=FormattedString(content="Title", format=None)
    )


def test_valid_instance(subject):
    assert type(subject) is TypedTitleString


def test_to_xml(subject):
    host = ET.Element("host")
    result = subject.to_xml(host)

    assert host.attrib["type"] == "main"
    assert host.text == "Title"


def test_to_hash(subject):
    result = dataclasses.asdict(subject)

    assert result["type"] == "main"
    assert result["title"]["content"] == "Title"


def test_to_asciibib(subject):
    result = subject.to_asciibib()

    assert result == inspect.cleandoc(
        """title.type:: main
           title.content:: Title""")


def test_from_string_empty():
    t = TypedTitleString.from_string("")
    assert len(t) == 2
    assert t[0].title.content == ""
    assert t[0].type == "title-main"
    assert t[1].title.content == ""
    assert t[1].type == "main"


def test_with_main():
    t = TypedTitleString.from_string("Main")
    assert len(t) == 2
    assert t[0].title.content == "Main"
    assert t[0].type == "title-main"
    assert t[1].title.content == "Main"
    assert t[1].type == "main"


def test_with_main_and_part():
    t = TypedTitleString.from_string("Main - Part 1:")
    assert len(t) == 3
    assert t[0].title.content == "Main"
    assert t[0].type == "title-main"
    assert t[1].title.content == "Part 1:"
    assert t[1].type == "title-part"
    assert t[2].title.content == "Main - Part 1:"
    assert t[2].type == "main"


def test_with_intro_and_main():
    t = TypedTitleString.from_string("Intro - Main")
    assert len(t) == 3
    assert t[0].title.content == "Intro"
    assert t[0].type == "title-intro"
    assert t[1].title.content == "Main"
    assert t[1].type == "title-main"
    assert t[2].title.content == "Intro - Main"
    assert t[2].type == "main"


def test_with_intro_and_main_and_part():
    t = TypedTitleString.from_string("Intro - Main - Part 1:")
    assert len(t) == 4
    assert t[0].title.content == "Intro"
    assert t[0].type == "title-intro"
    assert t[1].title.content == "Main"
    assert t[1].type == "title-main"
    assert t[2].title.content == "Part 1:"
    assert t[2].type == "title-part"
    assert t[3].title.content == "Intro - Main - Part 1:"
    assert t[3].type == "main"


def test_with_extra_part():
    t = TypedTitleString.from_string("Intro - Main - Part 1: - Extra")
    assert len(t) == 4
    assert t[0].title.content == "Intro"
    assert t[0].type == "title-intro"
    assert t[1].title.content == "Main"
    assert t[1].type == "title-main"
    assert t[2].title.content == "Part 1: -- Extra"
    assert t[2].type == "title-part"
    assert t[3].title.content == "Intro - Main - Part 1: -- Extra"
    assert t[3].type == "main"
