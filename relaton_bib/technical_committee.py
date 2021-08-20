from dataclasses import dataclass

import xml.etree.ElementTree as ET

from .workgroup import WorkGroup


@dataclass
class TechnicalCommittee:
    workgroup: WorkGroup

    # to_hash -> dataclasses.asdict - different

    def to_xml(self, parent=None):
        name = "technical-committee"
        node = ET.SubElement(parent, name) if parent else ET.Element(name)
        self.workgroup.to_xml(node)
        return node

    def to_asciibib(self, prefix="", count=1):
        name = "technical_committee"
        pref = f"{prefix}.{name}" if prefix else name
        out = [f"{pref}::"] if count > 1 else []
        out.append(self.workgroup.to_asciibib(pref))
        return "\n".join(out)
