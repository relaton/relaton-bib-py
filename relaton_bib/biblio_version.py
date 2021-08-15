import xml.etree.ElementTree as ET

from dataclasses import dataclass
from typing import Optional


@dataclass
class BibliographicItemVersion:
    revision_date: Optional[str] = None
    draft: list[str] = []

    def to_xml(self, parent=None):
        name = "version"
        node = ET.SubElement(parent, name) if parent else ET.Element(name)
        if self.revision_date:
            ET.SubElement(node, "revision-date").text = revision_date
        for d in self.draft:
            ET.SubElement(node, "draft").text = d
        return node

    def to_asciibib(prefix=""):
        pref = prefix if prefix else f"{prefix}."
        out = []
        if self.revision_date:
            out.append(f"{pref}version.revision_date:: {revision_date}")
        for d in self.draft:
            out.append(f"{pref}version.draft:: {d}")
        return "\n".join(out)
