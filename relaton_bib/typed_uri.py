import datetime
import typing

from dataclasses import dataclass

import xml.etree.ElementTree as ET


@dataclass(frozen=True)  # FIXME missing content=(url)
class TypedUri:
    type: str = None
    content: str  # NOTE originaly it was URI, but looks like it's not need

    # to_hash -> dataclasses.asdict

    def to_xml(self, parent=None):
        name = "uri"
        node = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)
        node.text = self.content

        if self.type:
            node.attrib["type"] = self.type

        return node

    def to_asciibib(self, prefix="", count=1):
        """Return AsciiBib representation

        Keyword arguments:
        prefix -- AsciiBib prefix
        count -- number of links
        """
        pref = f"{prefix}.link" if prefix else "link"
        out = [f"{pref}::"] if count > 1 else []
        if self.type:
            out.append(f"{pref}.type:: {self.type}")
        out.append(f"{pref}.content:: {self.content}")
        return "\n".join(out)
