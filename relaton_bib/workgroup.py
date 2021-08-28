from dataclasses import dataclass


@dataclass(frozen=True)
class WorkGroup:
    content: str
    number: int = None
    type: str = None

    # to_hash -> dataclasses.asdict

    def to_xml(self, parent):
        parent.text = self.content
        if self.number:
            parent.attrib["number"] = str(self.number)
        if self.type:
            parent.attrib["type"] = self.type
        return parent

    def to_asciibib(self, prefix=""):
        pref = f"{prefix}." if prefix else prefix
        out = [f"{pref}content:: {self.content}"]
        if self.number:
            out.append(f"{pref}number:: {self.number}")
        if self.type:
            out.append(f"{pref}type:: {self.type}")
        return "\n".join(out)
