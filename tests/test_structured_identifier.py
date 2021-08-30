import dataclasses
import inspect
import pytest

import xml.etree.ElementTree as ET

from relaton_bib.structured_identifier import StructuredIdentifier, \
                                              StructuredIdentifierCollection
from relaton_bib.document_identifier import DocumentIdType


def test_remove_data_for_cn_std():
    sid = StructuredIdentifier(
        docnumber="TEST-1999",
        type=DocumentIdType.CN_STD.value)
    sid.remove_date()
    assert sid.docnumber == "TEST"


@pytest.fixture
def subject():
    return StructuredIdentifier(
        docnumber="AGNT-007",
        type=DocumentIdType.CN_STD.value,
        agency=["agncy1", "agency2"],
        klass="class",
        partnumber="1",
        edition="2",
        version="3.4.5",
        supplementtype="sup",
        supplementnumber="6",
        language="en",
        year="1007")


def test_to_xml(subject):
    host = ET.Element("host")
    result = subject.to_xml(host)

    assert host.find("./structuredidentifier") is not None
    assert result.attrib["type"] == DocumentIdType.CN_STD.value
    assert len(result.findall("./agency")) == 2
    assert result.find("./class_").text == "class"
    assert result.find("./docnumber").text == "AGNT-007"
    assert result.find("./partnumber").text == "1"
    assert result.find("./edition").text == "2"
    assert result.find("./version").text == "3.4.5"
    assert result.find("./supplementtype").text == "sup"
    assert result.find("./supplementnumber").text == "6"
    assert result.find("./language").text == "en"
    assert result.find("./year").text == "1007"


def test_to_asciibib(subject):
    result = subject.to_asciibib()

    assert result == inspect.cleandoc(
        """docnumber:: AGNT-007
           agency:: agncy1
           agency:: agency2
           class:: class
           type:: Chinese Standard
           partnumber:: 1
           edition:: 2
           version:: 3.4.5
           supplementtype:: sup
           supplementnumber:: 6
           language:: en
           year:: 1007""")


def test_to_asciibib_with_pref(subject):
    result = subject.to_asciibib(prefix="test")

    assert result == inspect.cleandoc(
        """test.docnumber:: AGNT-007
           test.agency:: agncy1
           test.agency:: agency2
           test.class:: class
           test.type:: Chinese Standard
           test.partnumber:: 1
           test.edition:: 2
           test.version:: 3.4.5
           test.supplementtype:: sup
           test.supplementnumber:: 6
           test.language:: en
           test.year:: 1007""")


def test_hash(subject):
    result = dataclasses.asdict(subject)

    assert result["type"] == DocumentIdType.CN_STD.value
    assert len(result["agency"]) == 2
    assert result["klass"] == "class"
    assert result["docnumber"] == "AGNT-007"
    assert result["partnumber"] == "1"
    assert result["edition"] == "2"
    assert result["version"] == "3.4.5"
    assert result["supplementtype"] == "sup"
    assert result["supplementnumber"] == "6"
    assert result["language"] == "en"
    assert result["year"] == "1007"


def test_collection(subject):
    col = StructuredIdentifierCollection([subject])
    assert len(col) == 1

    col.remove_part()
    assert col[0].docnumber == "AGNT"
    assert col[0].partnumber is None
    col.all_parts()
    assert col[0].docnumber == "AGNT (all parts)"
