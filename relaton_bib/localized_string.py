from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union, List

import xml.sax.saxutils as saxutils
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class LocalizedString:
    content: Union[str, list[LocalizedString]]
    language: List[str] = field(default_factory=list)
    script: List[str] = field(default_factory=list)

    def __post_init__(self):
        inv = None
        if isinstance(self.content, list):
            def reject(x): return not isinstance(x, (LocalizedString, dict))
            inv = list(filter(reject, self.content))

        if not (isinstance(self.content, str)
                or inv and any(self.content)):
            klass = type(inv[0]) if isinstance(self.content, list) \
                                 else type(self.content)
            klass = klass.__name__
            raise ValueError(f"invalid LocalizedString content type: {klass}")

        # modify froozen dataclass https://stackoverflow.com/a/54119384/902217
        if isinstance(self.language, str):
            object.__setattr__(self, "language", [self.language])

        if isinstance(self.script, str):
            object.__setattr__(self, "script", [self.script])

        if isinstance(self.content, list):
            def dict_to_loc_str(c):
                if isinstance(c, dict):
                    return LocalizedString(c.get("content"),
                                           c.get("language"),
                                           c.get("script"))
                else:
                    return c

            object.__setattr__(self, "content",
                               map(dict_to_loc_str, self.content))

    def __str__(self):
        return self.content if isinstance(self.content, str) \
                            else str(self.content[0] if self.content else None)

    def __len__(self):
        return len(self.content)

    def empty(self):
        return len(self) == 0

    def to_xml(self, node):
        if not self.content:
            return

        if isinstance(self.content, list):
            for c in self.content:
                c.to_xml(ET.SubElement(node, "variant"))
        else:
            if any(self.language):
                node.attrib["language"] = ",".join(filter(None, self.language))
            if any(self.script):
                node.attrib["script"] = ",".join(filter(None, self.script))
            # TODO do we really need double encoding for content
            node.text = saxutils.escape(self.content)

        return node

    # TODO revisit
    # def to_hash
    #   if content.is_a? String
    #     return content unless language || script

    #     hash = { "content" => content }
    #     hash["language"] = single_element_array(language) if language&.any?
    #     hash["script"] = single_element_array(script) if script&.any?
    #     hash
    #   else content.map &:to_hash
    #   end
    # end

    def to_asciibib(self, prefix="", count=1, has_attrs=False):
        pref = f"{prefix}." if prefix else prefix

        if isinstance(self.content, list):
            return "".join(map(
                lambda c: c.to_asciibib(f"{pref}variant", len(self.content)),
                self.content))
        else:
            if not (any(self.language) or any(self.script) or has_attrs):
                return f"{prefix}:: {self.content}"

            out = [f"{prefix}::"] if count > 1 else []
            out.append(f"{pref}content:: {self.content}")
            for lang in self.language:
                out.append(f"{pref}language:: {lang}")
            for script in self.script:
                out.append(f"{pref}script:: {script}")
            return "\n".join(out)
