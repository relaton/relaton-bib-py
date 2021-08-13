from dataclasses import dataclass
from enum import Enum
import logging


class BibItemLocalityType(Enum):
    SECTION = "section"
    CLAUSE = "clause"
    PART = "part"
    PARAGRAPH = "paragraph"
    CHAPTER = "chapter"
    PAGE = "page"
    WHOLE = "whole"
    TABLE = "table"
    ANNEX = "annex"
    FIGURE = "figure"
    NOTE = "note"
    LIST = "list"
    EXAMPLE = "example"
    VOLUME = "volume"
    ISSUE = "issue"
    TIME = "time"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 


@dataclass(frozen=True)
class BibItemLocality:
    """Bibliographic item locality."""

    type: str
    reference_from: str = text()
    reference_to: str = text(None)

    def __post_init__(self):
        if not (BibItemLocalityType.has_value(self.type)
                or re.match("locality:[a-zA-Z0-9_]+", self.type)):
            logging.warn(f"[relaton-bib] invalid locality type: {self.type}")

    # FIXME
    # @param builder [Nokogiri::XML::Builder]
    # def to_xml(builder)
    #   builder.parent[:type] = type
    #   builder.referenceFrom reference_from # { reference_from.to_xml(builder) }
    #   builder.referenceTo reference_to if reference_to
    # end

    # @param prefix [String]
    # @param count [Integeg] number of localities
    # @return [String]
    def to_asciibib(prefix="", count=1):
        pref = prefix + "." if prefix else prefix
        out = f"{prefix}::\n" if count > 1 else ""
        out += f"{pref}type:: {self.type}\n"
        out += f"{pref}reference_from:: {self.reference_from}\n"
        if reference_to:
            out += f"{pref}reference_to:: {self.reference_to}\n"
        return out


class Locality(BibItemLocality)
# @param builder [Nokogiri::XML::Builder]
def to_xml(builder)
  builder.locality { |b| super(b) }
end
end

  class LocalityStack
    include RelatonBib

    # @return [Array<RelatonBib::Locality>]
    attr_reader :locality

    # @param locality [Array<RelatonBib::Locality>]
    def initialize(locality)
      @locality = locality
    end

    # @param builder [Nokogiri::XML::Builder]
    def to_xml(builder)
      builder.localityStack do |b|
        locality.each { |l| l.to_xml(b) }
      end
    end

    # @returnt [Hash]
    def to_hash
      { "locality_stack" => single_element_array(locality) }
    end
  end

  class SourceLocality < BibItemLocality
    # @param builder [Nokogiri::XML::Builder]
    def to_xml(builder)
      builder.sourceLocality { |b| super(b) }
    end
  end

  class SourceLocalityStack < LocalityStack
    # @param builder [Nokogiri::XML::Builder]
    def to_xml(builder)
      builder.sourceLocalityStack do |b|
        locality.each { |l| l.to_xml(b) }
      end
    end

    # @returnt [Hash]
    def to_hash
      { "source_locality_stack" => single_element_array(locality) }
    end
  end
end
