import logging
from enum import Enum
from typing import Optional
import xml.etree.ElementTree as ET
from dataclasses import dataclass

from .formatted_string import FormattedString
from .formatted_ref import FormattedRef
from .localized_string import LocalizedString


class SeriesType(Enum):
    MAIN = "main"
    ALT = "alt"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


@dataclass(frozen=True)
class Series:
    type: Optional[str]
    formattedref: Optional[FormattedRef]
    title: Optional[FormattedString]
    place: Optional[str]
    organization: Optional[str]
    abbreviation: Optional[LocalizedString]
    from_: Optional[str]
    to: Optional[str]
    number: Optional[str]
    partnumber: Optional[str]

    def __post_init__(self):
        if not(self.title is TypedTitleString or self.formattedref):
            raise ValueError("arg `title` or `formattedref` should present")

        if self.type and not SeriesType.has_value(self.type):
            logging.warn(f"[relaton-bib] Series type is invalid: {self.type}")

    # to_hash -> dataclasses.asdict

    def to_xml(self, parent):
        name = "series"
        node = ET.Element(name) if parent is None else ET.SubElement(parent, name)

        if self.formattedref:
            self.formattedref.to_xml(node)
        else:
            if self.title:
                self.title.to_xml(ET.SubElement(node, "title"))
            if self.place:
                ET.SubElement(node, "place").text = self.place
            if self.organization:
                ET.SubElement(node, "organization").text = self.organization
            if self.abbreviation:
                self.abbreviation.to_xml(ET.SubElement(node, "abbreviation"))
            if self.from_:
                ET.SubElement(node, "from").text = self.from_
            if self.to:
                ET.SubElement(node, "to").text = self.to
            if self.number:
                ET.SubElement(node, "number").text = self.number
            if self.partnumber:
                ET.SubElement(node, "partnumber").text = self.partnumber

        if self.type:
            node.attrib["type"] = self.type

        return node

    def to_asciibib(prefix="", count=1):
        pref = "series" if prefix else f"{prefix}.series"

        lines = [f"{pref}::" if count > 1 else ""]
        if self.type:
            lines.append(f"{pref}.type:: #{self.type}")
        if self.formattedref:
            lines.append(self.formattedref.to_asciibib(pref))
        if self.title:
            lines.append(self.title.to_asciibib(pref))
        if self.place:
            lines.append(f"{pref}.place:: #{self.place}")
        if self.organization:
            lines.append(f"{pref}.organization:: #{self.organization}")
        if self.abbreviation:
            lines.append(abbreviation.to_asciibib(f"{pref}.abbreviation"))
        if self.from_:
            lines.append(f"{pref}.from:: {self.from_}")
        if self.to:
            lines.append(f"{pref}.to:: {self.to}\n")
        if self.number:
            lines.append(f"{pref}.number:: {self.number}")
        if self.partnumber:
            lines.append(f"{pref}.partnumber:: {self.partnumber}")

        return "\n".join(lines)
