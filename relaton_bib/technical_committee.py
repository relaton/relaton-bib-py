from .workgroup import WorkGroup
import xml.etree.ElementTree as ET


@dataclass
class TechnicalCommittee:
    workgroup: WorkGroup

    # to_hash -> dataclasses.asdict - different

    def to_xml(parent=None):
        name = "technical-committee"
        node = ET.SubElement(parent, name) if parent else ET.Element(name)
        self.workgroup.to_xml(node)
        node

    def to_asciibib(prefix="", count=1):
        pref = prefix if prefix else f"{prefix}."
        pref += "technical_committee"
        out = f"{pref}::\n" if count > 1 else ""
        out += self.workgroup.to_asciibib(pref)
        return out
