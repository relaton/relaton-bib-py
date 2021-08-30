import dataclasses
import inspect
import pytest

import xml.etree.ElementTree as ET

from relaton_bib.editorial_group import EditorialGroup
from relaton_bib.workgroup import WorkGroup
from relaton_bib.technical_committee import TechnicalCommittee


@pytest.fixture
def subject():
    return EditorialGroup([
        TechnicalCommittee(WorkGroup(content="g1", number=1, type="work")),
        TechnicalCommittee(WorkGroup(content="g2", number=2)),
        TechnicalCommittee(WorkGroup(content="g3")),
        ])


def test_to_xml(subject):
    host = ET.Element("host")
    subject.to_xml(host)

    assert len(host.findall("./editorialgroup/technical-committee")) == 3


def test_to_asciibib(subject):
    result = subject.to_asciibib()

    assert result == inspect.cleandoc(
        """editorialgroup.technical_committee::
           editorialgroup.technical_committee.content:: g1
           editorialgroup.technical_committee.number:: 1
           editorialgroup.technical_committee.type:: work
           editorialgroup.technical_committee::
           editorialgroup.technical_committee.content:: g2
           editorialgroup.technical_committee.number:: 2
           editorialgroup.technical_committee::
           editorialgroup.technical_committee.content:: g3""")


def test_to_asciibib_with_pref(subject):
    result = subject.to_asciibib(prefix="g")

    assert result == inspect.cleandoc(
        """g.editorialgroup.technical_committee::
           g.editorialgroup.technical_committee.content:: g1
           g.editorialgroup.technical_committee.number:: 1
           g.editorialgroup.technical_committee.type:: work
           g.editorialgroup.technical_committee::
           g.editorialgroup.technical_committee.content:: g2
           g.editorialgroup.technical_committee.number:: 2
           g.editorialgroup.technical_committee::
           g.editorialgroup.technical_committee.content:: g3""")


def test_hash(subject):
    result = dataclasses.asdict(subject)

    assert result["technical_committee"][0]["workgroup"]["content"] == "g1"
    assert result["technical_committee"][0]["workgroup"]["number"] == 1
    assert result["technical_committee"][0]["workgroup"]["type"] == "work"
    assert result["technical_committee"][1]["workgroup"]["content"] == "g2"
    assert result["technical_committee"][1]["workgroup"]["number"] == 2
    assert result["technical_committee"][2]["workgroup"]["content"] == "g3"
