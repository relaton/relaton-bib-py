from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Union, TYPE_CHECKING

import xml.etree.ElementTree as ET

from .formatted_string import FormattedString
from .localized_string import LocalizedString
if TYPE_CHECKING:
    from .organization import Organization


@dataclass
class Address:
    street: list[str]
    city: str
    state: Optional[str] = None
    country: str
    postcode: Optional[str] = None

    def to_xml(self, parent):
        name = "address"
        result = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)
        for st in self.street:
            ET.SubElement(result, "street").text = st
        ET.SubElement(result, "city").text = self.city
        ET.SubElement(result, "country").text = self.country
        if self.state:
            ET.SubElement(result, "state").text = self.state
        if self.postcode:
            ET.SubElement(result, "postcode").text = self.postcode
        return result

    def to_asciibib(self, prefix="", count=1):
        pref = f"{prefix}.address" if prefix else "address"
        out = [f"{pref}::"] if count > 1 else []
        for st in self.street:
            out.append(f"{pref}.street:: {st}")
        out.append(f"{pref}.city:: {self.city}")
        if self.state:
            out.append(f"{pref}.state:: {self.state}")
        out.append(f"{pref}.country:: {self.country}")
        if self.postcode:
            out.append(f"{pref}.postcode:: {self.postcode}")
        return "\n".join(out)


class ContactType(Enum):
    PHONE = "phone"
    EMAIL = "email"
    URI = "uri"


@dataclass
class Contact:
    type: str
    value: str

    def to_xml(self, parent):
        result = ET.Element(self.type) if parent is None \
            else ET.SubElement(parent, self.type)
        result.text = self.value
        return result

    def to_asciibib(self, prefix="", count=1):
        pref = [f"{prefix}."] if prefix else [prefix]
        out = [f"{pref}contact::"] if count > 1 else []
        out.append(f"{pref}contact.type:: {self.type}")
        out.append(f"{pref}contact.value:: {self.value}")
        return "\n".join(out)


@dataclass
class Contributor:
    uri: str = None
    contact: List[Union[Address, Contact]]

    @property
    def url(self):
        return self.uri

    def to_xml(self, parent):
        for c in self.contact:
            self.contact.to_xml(parent)

    def to_asciibib(self, prefix=""):
        pref = f"{prefix}." if prefix else prefix
        out = []
        if self.uri:
            out.append(f"{pref}url:: {self.uri}")
        addr = [x for x in self.contact if isinstance(x, Address)]
        for a in addr:
            out.append(a.to_asciibib(prefix, len(addr)))
        cont = [x for x in self.contact if isinstance(x, Contact)]
        for c in cont:
            out.append(c.to_asciibib(prefix, len(cont)))
        return "\n".join(out)
