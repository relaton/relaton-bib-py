from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union

import re
import xml.etree.ElementTree as ET

from .forwardable import Forwardable
from .formatted_string import FormattedString
from .localized_string import LocalizedString
from .relaton_bib import lang_filter


@dataclass
class TypedTitleString:
    type: str = None
    title: FormattedString = None
    content: Union[str, List[LocalizedString]] = None
    language: List[str] = None
    script: List[str] = None
    format: List[str] = None

    def __post_init__(self):
        if self.title is None and self.content is None:
            raise ValueError("Argument title or content should be passed")

        if not self.title:
            self.title = FormattedString(
                content=self.content,
                language=self.language,
                script=self.script,
                format=self.format)

    @classmethod
    def from_string(cls, title, lang=None, script=None):
        types = ["title-intro", "title-main", "title-part"]
        ttls = cls.split_title(title)
        tts = [None if p is None else
               cls(type=types[i], content=p, language=lang, script=script)
               for i, p in enumerate(ttls)]
        tts = list(filter(None, tts))
        ttls = list(filter(None, ttls))
        tts.append(TypedTitleString(type="main",
                                    content=" - ".join(ttls),
                                    language=lang,
                                    script=script))
        return TypedTitleStringCollection(tts)

    @classmethod
    def split_title(cls, title):
        ttls = re.sub(r"\w\.Imp\s?\d+\u00A0:\u00A0", "", title).split(" - ")
        if len(ttls) < 2:
            return [None, str(ttls[0]), None]
        else:
            return cls.intro_or_part(ttls)

    @classmethod
    def intro_or_part(cls, ttls):
        if re.match(r"^(Part|Partie) \d+:", ttls[1]):
            return [None, ttls[0], " -- ".join(ttls[1:])]
        else:
            parts = ttls[2:]
            part = None
            if any(parts):
                part = " -- ".join(parts)
            return [ttls[0], ttls[1], part]

    def to_xml(self, parent):
        if self.type:
            parent.attrib["type"] = self.type
        self.title.to_xml(parent)
        return parent

    def to_asciibib(self, prefix="", count=1):
        pref = f"{prefix}." if prefix else prefix
        out = [f"{pref}title::"] if count > 1 else []
        if self.type:
            out.append(f"{pref}title.type:: {self.type}")
        out.append(self.title.to_asciibib(f"{pref}title", 1, bool(self.type)))
        return "\n".join(out)


def delegate(to, *methods):
    def dec(klass):
        def create_delegator(method):
            def delegator(self, *args, **kwargs):
                obj = getattr(self, to)
                m = getattr(obj, method)
                return m(*args, **kwargs)
            return delegator
        for m in methods:
            setattr(klass, m, create_delegator(m))
        return klass
    return dec


@dataclass
@delegate("titles", "append", "__getitem__", "__len__", "__iter__",
          "__reversed__", "__contains__")
class TypedTitleStringCollection():
    titles: List[TypedTitleString]

    def __post_init__(self):
        self.titles = list(map(
            lambda t: TypedTitleString(**t) if isinstance(t, dict) else t,
            self.titles))

    def lang(self, lang=None):
        return self.__class__(lang_filter(self.titles, {"lang": lang})) \
            if lang else self

    def delete_title_part(self):
        self.titles = filter(lambda t: t.type != "title-part", self.titles)

    # @param init [Array, Hash]
    # @return [RelatonBib::TypedTitleStringCollection]
    # def reduce(init)
    #   self.class.new @array.reduce(init) { |m, t| yield m, t }
    # end

    # @param title [RelatonBib::TypedTitleString]
    # # @return [self]
    # def <<(title)
    #   titles << title
    #   self
    # end

    # # @param tcoll [RelatonBib::TypedTitleStringCollection]
    # # @return [RelatonBib::TypedTitleStringCollection]
    # def +(tcoll)
    #   TypedTitleStringCollection.new titles + tcoll.titles
    # end

    # @param opts [Hash]
    # @option opts [Nokogiri::XML::Builder] XML builder
    # @option opts [String, Symbol] :lang language
    def to_xml(self, parent, opts={}):
        tl = lang_filter(self.titles, opts)
        for t in tl:
            t.to_xml(ET.SubElement(parent, "title"))

        return parent
