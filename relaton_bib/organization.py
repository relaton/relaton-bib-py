from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union, TYPE_CHECKING

import re
import logging
import xml.etree.ElementTree as ET

from .localized_string import LocalizedString
from .formatted_string import FormattedString
from .relaton_bib import lang_filter
if TYPE_CHECKING:
    from .contributor import Address, Contact, Contributor


class OrgIdentifierType(Enum):
    ORCID = "orcid"
    URI = "uri"


@dataclass(frozen=True)
class OrgIdentifier:
    type: str
    value: str

    def __post_init__(self):
        if not (OrgIdentifierType.has_value(self.type)):
            logging.warning(
                f"[relaton-bib] invalid locality type: {self.type}")

    def to_xml(self, parent):
        name = "identifier"
        node = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)
        node.text = self.value
        node.attrib["type"] = self.type
        return node

    def to_asciibib(self, prefix="", count=1):
        pref = f"{prefix}." if prefix else prefix
        out = [f"{pref}identifier::"] if count > 1 else []
        out.append(f"{pref}identifier.type:: {self.type}")
        out.append(f"{pref}identifier.value:: {self.value}")
        return "\n".join(out)


@dataclass(frozen=True)
class Organization(Contributor):
    name: List[LocalizedString]
    abbreviation: LocalizedString = None
    subdivision: List[LocalizedString] = field(default_factory=List)
    identifier: List[OrgIdentifier] = field(default_factory=List)
    contact: List[Union[Address, Contact]] = field(default_factory=List)

    # TODO revisit later
    # def initialize(**args)
    #   raise ArgumentError, "missing keyword: name" unless args[:name]

    #   super(url: args[:url], contact: args.fetch(:contact, []))

    #   @name = if args[:name].is_a?(Array)
    #             args[:name].map { |n| localized_string(n) }
    #           else
    #             [localized_string(args[:name])]
    #           end

    #   @abbreviation = localized_string args[:abbreviation]
    #   @subdivision  = (args[:subdivision] || []).map do |sd|
    #     localized_string sd
    #   end
    #   @identifier   = args.fetch(:identifier, [])
    # end

    def to_xml(self, parent, opts={}):
        name = "organization"
        result = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)
        for n in lang_filter(self.name, opts):
            n.to_xml(ET.SubElement(result, "name"))
        for s in lang_filter(self.subdivision, opts):
            s.to_xml(ET.SubElement(result, "subdivision"))
        if self.abbreviation:
            self.abbreviation.to_xml(ET.SubElement(result, "abbreviation"))
        if self.uri:
            ET.SubElement(result, "uri").text = self.uri
        for idntfr in self.identifier:
            idntfr.to_xml(result)
        super().to_xml(result)
        return result

    def to_asciibib(self, prefix="", count=1):
        pref = re.sub(r"\*$", "organization", prefix)
        out = [f"{pref}::"] if count > 1 else []
        for n in self.name:
            out.append(n.to_asciibib(f"{pref}.name", len(self.name)))
        if self.abbreviation:
            out.append(self.abbreviation.to_asciibib(f"{pref}.abbreviation"))
        for sd in self.subdivision:
            if len(self.subdivision) > 1:
                # TODO originally it was without \n
                out.append(f"{pref}.subdivision::")
            out.append(sd.to_asciibib(f"{pref}.subdivision"))
        for idtfr in self.identifier:
            out.append(n.to_asciibib(pref, len(self.identifier)))
        out.append(super().to_asciibib(pref))
        return "\n".join(out)


@dataclass
class Affiliation:
    name: LocalizedString = None
    description: List[FormattedString] = None
    organization: Organization

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
