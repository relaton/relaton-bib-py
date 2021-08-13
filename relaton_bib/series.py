import logging
from enum import Enum
from typing import Optional
import xml.etree.ElementTree as ET


class SeriesType(Enum):
    MAIN = "main"
    ALT = "alt"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


@dataclass(frozen=True)
class Series:
    type: Optional[str]
    formattedref: Optional[FormattedRef]
    title: Optional[FormattedString]
    place: Optional[str]
    organization: Optional[str]
    abbreviation: Optional[LocalizedString]
    from_: Optional[str]
    to: Optional[str]
    number: Optional[str]
    partnumber: Optional[str]

    def __post_init__(self):
        if not(self.title is TypedTitleString or self.formattedref):
            raise ValueError("arg `title` or `formattedref` should present")

        if self.type and !SeriesType.has_value(self.type):
            logging.warn(f"[relaton-bib] Series type is invalid: {self.type}")

    # to_hash -> dataclasses.asdict

    def to_xml(parent):
        name = "series"
        node = ET.SubElement(parent, name) if parent else ET.Element(name)

        if self.formattedref:
            self.formattedref.to_xml(node)
        else:
            if self.title:
                self.title.to_xml(ET.SubElement(node, "title"))
            if self.place:
                ET.SubElement(node, "place").text = self.place
            if self.organization:
                ET.SubElement(node, "organization").text = self.organization
            if self.abbreviation:
                self.abbreviation.to_xml(ET.SubElement(node, "abbreviation"))
            if self.from_:
                ET.SubElement(node, "from").text = self.from_
            if self.to:
                ET.SubElement(node, "to").text = self.to
            if self.number:
                ET.SubElement(node, "number").text = self.number
            if self.partnumber:
                ET.SubElement(node, "partnumber").text = self.partnumber

        if self.type:
            node.attrib["type"] = self.type

        return node

    def to_asciibib(prefix="", count=1):
        pref = "series" if prefix else f"{prefix}.series"

        out = [f"{pref}::" if count > 1 else ""]
        if self.type:
            out.append(f"{pref}.type:: #{type}")
        if self.formattedref:
            out.append(self.formattedref.to_asciibib(pref))
        if self.title
            out.append(title.to_asciibib(pref))
        if 
        out += f"{pref}.place:: #{place}\n" if place
        if  self.organization:
            out += f"{pref}.organization:: #{organization}\n"
        out += abbreviation.to_asciibib "#{pref}.abbreviation" if abbreviation
        out += f"{pref}.from:: {from}\n" if from
        out += f"{pref}.to:: {to}\n" if to
        out += f"{pref}.number:: {number}\n" if number
        out += f"{pref}.partnumber:: {partnumber}\n" if partnumber
        out
    end

module RelatonBib
  #
  # Series class.
  #
  class Series
    TYPES = %w[main alt].freeze

    # @return [String, NilClass] allowed values: "main" or "alt"
    attr_reader :type

    # @return [RelatonBib::FormattedRef, NilClass]
    attr_reader :formattedref

    # @return [RelatonBib::FormattedString, NilClass] title
    attr_reader :title

    # @return [String, NilClass]
    attr_reader :place

    # @return [String, NilClass]
    attr_reader :organization

    # @return [RelatonBib::LocalizedString, NilClass]
    attr_reader :abbreviation

    # @return [String, NilClass] date or year
    attr_reader :from

    # @return [String, NilClass] date or year
    attr_reader :to

    # @return [String, NilClass]
    attr_reader :number

    # @return [String, NilClass]
    attr_reader :partnumber

    # rubocop:disable Metrics/AbcSize, Metrics/MethodLength

    # @param type [String, NilClass] title or formattedref argument should be
    #   passed
    # @param formattedref [RelatonBib::FormattedRef, NilClass]
    # @param title [RelatonBib::TypedTitleString, NilClass]
    # @param place [String, NilClass]
    # @param orgaization [String, NilClass]
    # @param abbreviation [RelatonBib::LocalizedString, NilClass]
    # @param from [String, NilClass]
    # @param to [String, NilClass]
    # @param number [String, NilClass]
    # @param partnumber [String, NilClass]
    def initialize(**args)
      unless args[:title].is_a?(RelatonBib::TypedTitleString) ||
          args[:formattedref]
        raise ArgumentError, "argument `title` or `formattedref` should present"
      end

      if args[:type] && !TYPES.include?(args[:type])
        warn "[relaton-bib] Series type is invalid: #{args[:type]}"
      end

      @type         = args[:type] # if %w[main alt].include? args[:type]
      @title        = args[:title]
      @formattedref = args[:formattedref]
      @place        = args[:place]
      @organization = args[:organization]
      @abbreviation = args[:abbreviation]
      @from         = args[:from]
      @to           = args[:to]
      @number       = args[:number]
      @partnumber   = args[:partnumber]
    end
    # rubocop:enable Metrics/MethodLength

    # rubocop:disable Metrics/CyclomaticComplexity, Metrics/PerceivedComplexity

    # @param builder [Nokogiri::XML::Builder]
    def to_xml(builder) # rubocop:disable Metrics/MethodLength
      xml = builder.series do
        if formattedref
          formattedref.to_xml builder
        else
          builder.title { title.to_xml builder }
          builder.place place if place
          builder.organization organization if organization
          builder.abbreviation { abbreviation.to_xml builder } if abbreviation
          builder.from from if from
          builder.to to if to
          builder.number number if number
          builder.partnumber partnumber if partnumber
        end
      end
      xml[:type] = type if type
    end
    # rubocop:enable Metrics/AbcSize, Metrics/CyclomaticComplexity
    # rubocop:enable Metrics/PerceivedComplexity

    # @return [Hash]
    def to_hash # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/MethodLength, Metrics/PerceivedComplexity
      hash = {}
      hash["type"] = type if type
      hash["formattedref"] = formattedref.to_hash if formattedref
      hash["title"] = title.to_hash if title
      hash["place"] = place if place
      hash["organization"] = organization if organization
      hash["abbreviation"] = abbreviation.to_hash if abbreviation
      hash["from"] = from if from
      hash["to"] = to if to
      hash["number"] = number if number
      hash["partnumber"] = partnumber if partnumber
      hash
    end

    # @param prefix [String]
    # @param count [Integer]
    # @return [String]
    def to_asciibib(prefix = "", count = 1) # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/MethodLength,Metrics/PerceivedComplexity
      pref = prefix.empty? ? "series" : prefix + ".series"
      out = count > 1 ? "#{pref}::\n" : ""
      out += "#{pref}.type:: #{type}\n" if type
      out += formattedref.to_asciibib pref if formattedref
      out += title.to_asciibib pref if title
      out += "#{pref}.place:: #{place}\n" if place
      out += "#{pref}.organization:: #{organization}\n" if organization
      out += abbreviation.to_asciibib "#{pref}.abbreviation" if abbreviation
      out += "#{pref}.from:: #{from}\n" if from
      out += "#{pref}.to:: #{to}\n" if to
      out += "#{pref}.number:: #{number}\n" if number
      out += "#{pref}.partnumber:: #{partnumber}\n" if partnumber
      out
    end
  end
end
