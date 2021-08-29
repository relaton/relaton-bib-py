import dataclasses
import inspect
import pytest

import xml.etree.ElementTree as ET

from relaton_bib.workgroup import WorkGroup
from relaton_bib.technical_committee import TechnicalCommittee


@pytest.fixture
def subject():
    return TechnicalCommittee(WorkGroup(content="value",
                                        number=1,
                                        type="type"))


def test_to_xml(subject):
    host = ET.Element("host")
    result = subject.to_xml(host)

    assert host.find("./technical-committee") is not None
    assert result.text == "value"
    assert result.attrib["number"] == "1"


def test_to_asciibib(subject):
    result = subject.to_asciibib()

    assert result == inspect.cleandoc(
        """technical_committee.content:: value
           technical_committee.number:: 1
           technical_committee.type:: type""")


def test_to_asciibib_with_pref(subject):
    result = subject.to_asciibib(prefix="a")

    assert result == inspect.cleandoc(
        """a.technical_committee.content:: value
           a.technical_committee.number:: 1
           a.technical_committee.type:: type""")


def test_hash(subject):
    result = dataclasses.asdict(subject)

    assert result["workgroup"]["type"] == "type"
    assert result["workgroup"]["number"] == 1
    assert result["workgroup"]["content"] == "value"
