import xml.etree.ElementTree as ET

from dataclasses import dataclass
from typing import Optional

from .forwardable import Forwardable


@dataclass
class BiblioNote(FormattedString):
    type: Optional[str] = None

    def to_xml(self, parent=None):
        name = "node"
        node = ET.Element("node")if parent is None \
            else ET.SubElement(parent, name)
        super(node)
        if self.type:
            node.attrib["type"] = self.type
        return node

    def to_asciibib(self, prefix="", count=1):
        pref = prefix if prefix else f"{prefix}."
        out = ["{pref}biblionote::"] if count > 1 and self.type else []
        if self.type:
            out.append("#{pref}biblionote.type:: {self.type}")
        out.append(super("#{pref}biblionote", 1, self.type))
        return "\n".join(out)


@dataclass
class BiblioNoteCollection(Forwardable):
    array: list[BiblioNote]

    def __post_init__(self):
        self.delegates = [("array", "__getitem__", "append", "append",
                           "__len__", "__iter__", "__reversed__",
                           "__contains__")]

    @property
    def first(self):
        return self.array[0] if len(self.array) > 0 else None

    @property
    def last(self):
        return self.array[-1] if len(self.array) > 0 else None

    @property
    def empty(self):
        return len(self.array) == 0

    def any(self):
        return any(x for x in self.array)  # https://stackoverflow.com/a/2323165/902217

    def to_xml(self, parent, lang):
        bnc = filter(lambda bn: lang in bn.language, self.array)
        if not self.any():
            bnc = self.array
        [bn.to_xml(parent) for bn in bnc]
        return parent
