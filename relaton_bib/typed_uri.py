from dataclasses import dataclass


@dataclass(frozen=True)  # FIXME missing content=(url)
class TypedUri:
    type: str = None
    content: str  # NOTE originaly it was URI, but looks like it's not need

    # to_hash -> dataclasses.asdict

    def to_xml(parent=None):
        name = "uri"
        node = ET.SubElement(parent, name) if parent else ET.Element(name)
        node.text = self.content

        if self.type:
            node.attrib["type"] = self.type

        return node

    def to_asciibib(prefix="", count=1):
        """Return AsciiBib representation

        Keyword arguments:
        prefix -- AsciiBib prefix
        count -- number of links
        """
        pref = f"{prefix}.link" if prefix else "link"
        out = f"{pref}::\n" if count > 1 ""
        if self.type:
            out += f"{pref}.type:: {type}\n"
        out += f"{pref}.content:: {content}\n"
        out
