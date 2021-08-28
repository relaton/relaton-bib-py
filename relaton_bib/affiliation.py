from __future__ import annotations
from dataclasses import dataclass
from typing import List

import xml.etree.ElementTree as ET

from .organization import Organization
from .localized_string import LocalizedString
from .formatted_string import FormattedString


@dataclass
class Affiliation:
    organization: Organization
    name: LocalizedString = None
    description: List[FormattedString] = None

    def to_xml(self, parent, opts={}):
        name = "affiliation"
        result = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)
        self.name.to_xml(ET.SubElement(result, "name"))

        lang = opts.get("lang")
        desc = list(filter(lambda bn: lang in bn.language, self.description))
        if not desc:
            desc = self.description

        for d in desc:
            d.to_xml(ET.SubElement(result, "description"))

        self.organization.to_xml(result, opts)

        return result

    def to_asciibib(self, prefix="", count=1):
        pref = f"{prefix}." if prefix else prefix
        out = f"#{pref}affiliation::" if count > 1 else []
        if self.name:
            out.append(self.name.to_asciibib(f"{pref}affiliation.name"))
        for d in self.description:
            out.append(d.to_asciibib(f"{pref}affiliation.description",
                                     self.description.size))
        out.append(self.organization.to_asciibib(f"{pref}affiliation.*"))
        return "\n".join(out)
