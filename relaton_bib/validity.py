import datetime
import typing

import xml.etree.ElementTree as ET

from dataclasses import dataclass


@dataclass(frozen=True)
class Validity:
    FORMAT: typing.ClassVar[str] = "%Y-%m-%d %H:%M"

    begins: datetime.datetime = None
    ends: datetime.datetime = None
    revision: datetime.datetime = None

    # to_hash -> dataclasses.asdict TODO original convert datetime -> str

    def to_xml(self, parent):
        name = "validity"
        node = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)

        if self.begins:
            node.attrib["validityBegins"] = self.begins.strftime(self.FORMAT)
        if self.ends:
            node.attrib["validityEnds"] = self.ends.strftime(self.FORMAT)
        if self.revision:
            node.attrib["revision"] = self.revision.strftime(self.FORMAT)

        return node

    # @param prefix [String]
    # @return [String]
    def to_asciibib(self, prefix=""):
        """Return AsciiBib representation

        Keyword arguments:
        prefix -- AsciiBib prefix
        """
        pref = f"{prefix}.validity." if prefix else "validity."
        out = []
        if self.begins:
            out.append(f"{pref}begins:: {self.begins.strftime(self.FORMAT)}")
        if self.ends:
            out.append(f"{pref}ends:: {self.ends.strftime(self.FORMAT)}")
        if self.revision:
            out.append(
                f"{pref}revision:: {self.revision.strftime(self.FORMAT)}")
        return "\n".join(out)
