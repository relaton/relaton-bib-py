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

    def to_xml(parent):
        name = "validity"
        node = ET.SubElement(parent, name) if parent else ET.Element(name)

        if self.begins:
            node.attrib["validityBegins"] = begins.strftime(FORMAT)
        if self.ends:
            node.attrib["validityEnds"] = ends.strftime(FORMAT)
        if self.revision:
            node.attrib["revision"] = revision.strftime(FORMAT)

        return node

    # @param prefix [String]
    # @return [String]
    def to_asciibib(prefix=""):
        """Return AsciiBib representation

        Keyword arguments:
        prefix -- AsciiBib prefix
        """
        pref = f"{prefix}.validity." if prefix else "validity."
        out = ""
        if begins:
            out += f"{pref}begins:: {begins.strftime(FORMAT)}\n"
        if ends:
            out += f"{pref}ends:: {ends.strftime(FORMAT)}\n"
        if revision:
            out += f"{pref}revision:: {revision.strftime(FORMAT)}\n"
        return out
