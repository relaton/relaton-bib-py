import dataclasses
import inspect
import xml.etree.ElementTree as ET

from relaton_bib.classification import Classification


def test_to_xml():
    c12n = Classification(type="type", value="value")

    host = ET.Element("host")
    result = c12n.to_xml(host)

    assert result.attrib["type"] == "type"
    assert host.find("./classification").text == "value"


def test_to_asciibib():
    c12n = Classification(type="type", value="value")

    result = c12n.to_asciibib(prefix="test")

    assert result == inspect.cleandoc("""test.classification.type:: type
                                         test.classification.value:: value""")


def test_hash():
    c12n = Classification(type="type", value="value")

    result = dataclasses.asdict(c12n)

    assert result["type"] == "type"
    assert result["value"] == "value"
