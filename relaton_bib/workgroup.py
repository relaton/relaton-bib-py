from dataclasses import dataclass, field
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class WorkGroup:
    content: str
    number: int = field(None)
    type: str = None

    # to_hash -> dataclasses.asdict

    def to_xml(self, parent):
        parent.text = self.content
        if self.number:
            parent.attrib["number"] = self.number
        if self.type:
            parent.attrib["type"] = self.type

    def to_asciibib(self, prefix=""):
        """Return AsciiBib representation

        Keyword arguments:
        prefix -- AsciiBib prefix
        """
        pref = prefix + "." if prefix else prefix  # TODO is that correct?
        out = f"{pref}content:: {self.content}\n"
        if self.number:
            out += f"{pref}number:: {self.number}\n"
        if self.type:
            out += f"{pref}type:: #{self.type}\n"
        return out
