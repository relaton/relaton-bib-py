from __future__ import annotations
import datetime
import logging
import xml.etree.ElementTree as ET

from dataclasses import dataclass, field
from enum import Enum
from typing import List, TYPE_CHECKING

from .typed_uri import TypedUri
from .document_identifier import DocumentIdentifier
from .copyright_association import CopyrightAssociation
from .formatted_string import FormattedString
from .contribution_info import ContributionInfo
from .bibliographic_date import BibliographicDate
from .series import Series
from .document_status import DocumentStatus
from .organization import Organization
from .localized_string import LocalizedString
from .typed_title_string import TypedTitleString, TypedTitleStringCollection
from .formatted_ref import FormattedRef
from .medium import Medium
from .classification import Classification
from .validity import Validity
from .bib_item_locality import BibItemLocality
from .biblio_note import BiblioNote, BiblioNoteCollection
from .biblio_version import BibliographicItemVersion
from .place import Place
from .structured_identifier import StructuredIdentifierCollection
from .editorial_group import EditorialGroup
from .ics import ICS

if TYPE_CHECKING:
    from .document_relation import DocumentRelation
    from .document_relation_collection import DocRelationCollection

# from .bibtex_parser import BibtexPaser
# from .xml_parser import XmlPaser


class BibliographicItemType(str, Enum):
    ARTICLE = "article"
    BOOK = "book"
    BOOKLET = "booklet"
    CONFERENCE = "conference"
    MANUAL = "manual"
    PROCEEDINGS = "proceedings"
    PRESENTATION = "presentation"
    THESIS = "thesis"
    TECHREPORT = "techreport"
    STANDARD = "standard"
    UNPUBLISHED = "unpublished"
    MAP = "map"
    ELECTRONICS = "electronics"
    RESOURCE = "resource"
    AUDIOVISUAL = "audiovisual"
    FILM = "film"
    VIDEO = "video"
    BROADCAST = "broadcast"
    GRAPHIC_WORK = "graphic_work"
    MUSIC = "music"
    PATENT = "patent"
    INBOOK = "inbook"
    INCOLLECTION = "incollection"
    INPROCEEDINGS = "inproceedings"
    JOURNAL = "journal"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


@dataclass
class BibliographicItem:
    # all_parts: bool  # = False
    id: str = None
    type: str = None
    docnumber: str = None
    edition: str = None
    doctype: str = None  # TODO check if Enum type better then str
    title: TypedTitleStringCollection = field(default_factory=list)
    link: List[TypedUri] = field(default_factory=list)
    docid: List[DocumentIdentifier] = field(default_factory=list)
    date: List[BibliographicDate] = field(default_factory=list)
    contributor: List[ContributionInfo] = field(default_factory=list)
    version: BibliographicItemVersion = None
    biblionote: BiblioNoteCollection = None
    language: List[str] = field(default_factory=list)
    script: List[str] = field(default_factory=list)
    formattedref: FormattedRef = None
    status: DocumentStatus = None
    copyright: List[CopyrightAssociation] = field(default_factory=list)
    relation: DocRelationCollection = None
    series: List[Place] = field(default_factory=list)
    medium: Medium = None
    place: List[Place] = field(default_factory=list)
    extent: List[BibItemLocality] = field(default_factory=list)
    accesslocation: List[str] = field(default_factory=list)
    license: List[str] = field(default_factory=list)
    classification: List[Classification] = field(default_factory=list)
    validity: Validity = None
    fetched: datetime.date = None
    keyword: List[LocalizedString] = field(default_factory=list)
    editorialgroup: EditorialGroup = None
    ics: List[ICS] = field(default_factory=list)
    structuredidentifier: StructuredIdentifierCollection = None

    def __post_init__(self):
        if self.type and not BibliographicItemType.has_value(self.type):
            logging.warning(
                f"[relaton-bib] document type {self.type} is invalid")
        # TODO

    def to_xml(self, parent, opts={}):
        name = "bibdata" if opts.get("bibdata") else "bibitem"
        result = ET.Element(name) if parent is None \
            else ET.SubElement(parent, name)
        # TODO continue
        return result

    def to_asciibib(self, prefix=""):
        pass
    # @param id [String, NilClass]
    # @param title [RelatonBib::TypedTitleStringCollection,
    #   Array<Hash, RelatonBib::TypedTitleString>]
    # @param formattedref [RelatonBib::FormattedRef, NilClass]
    # @param type [String, NilClass]
    # @param docid [Array<RelatonBib::DocumentIdentifier>]
    # @param docnumber [String, NilClass]
    # @param language [Arra<String>]
    # @param script [Array<String>]
    # @param docstatus [RelatonBib::DocumentStatus, NilClass]
    # @param edition [String, NilClass]
    # @param version [RelatonBib::BibliographicItem::Version, NilClass]
    # @param biblionote [RelatonBib::BiblioNoteCollection]
    # @param series [Array<RelatonBib::Series>]
    # @param medium [RelatonBib::Medium, NilClas]
    # @param place [Array<String, RelatonBib::Place>]
    # @param extent [Array<Relaton::BibItemLocality>]
    # @param accesslocation [Array<String>]
    # @param classification [Array<RelatonBib::Classification>]
    # @param validity [RelatonBib:Validity, NilClass]
    # @param fetched [Date, NilClass] default nil
    # @param keyword [Array<String>]
    # @param doctype [String]
    # @param editorialgroup [RelatonBib::EditorialGroup, nil]
    # @param ics [Array<RelatonBib::ICS>]
    # @param structuredidentifier [RelatonBib::StructuredIdentifierCollection]
    #
    # @param copyright [Array<Hash, RelatonBib::CopyrightAssociation>]
    # @option copyright [Array<Hash, RelatonBib::ContributionInfo>] :owner
    # @option copyright [String] :from
    # @option copyright [String, NilClass] :to
    # @option copyright [String, NilClass] :scope
    #
    # @param date [Array<Hash>]
    # @option date [String] :type
    # @option date [String] :from
    # @option date [String] :to
    #
    # @param contributor [Array<Hash>]
    # @option contributor [RealtonBib::Organization, RelatonBib::Person]
    # @option contributor [String] :type
    # @option contributor [String] :from
    # @option contributor [String] :to
    # @option contributor [String] :abbreviation
    # @option contributor [Array<Array<String,Array<String>>>] :role
    #
    # @param abstract [Array<Hash, RelatonBib::FormattedString>]
    # @option abstract [String] :content
    # @option abstract [String] :language
    # @option abstract [String] :script
    # @option abstract [String] :type
    #
    # @param relation [Array<Hash>]
    # @option relation [String] :type
    # @option relation [RelatonBib::BibliographicItem,
    #                   RelatonIso::IsoBibliographicItem] :bibitem
    # @option relation [Array<RelatonBib::Locality,
    #                   RelatonBib::LocalityStack>] :locality
    # @option relation [Array<RelatonBib::SourceLocality,
    #                   RelatonBib::SourceLocalityStack>] :source_locality
    #
    # @param link [Array<Hash, RelatonBib::TypedUri>]
    # @option link [String] :type
    # @option link [String] :content
#     def initialize(**args)
#       if args[:type] && !TYPES.include?(args[:type])
#         warn %{[relaton-bib] document type "#{args[:type]}" is invalid.}
#       end

#       @title = TypedTitleStringCollection.new(args[:title])

#       @date = (args[:date] || []).map do |d|
#         d.is_a?(Hash) ? BibliographicDate.new(**d) : d
#       end

#       @contributor = (args[:contributor] || []).map do |c|
#         if c.is_a? Hash
#           e = c[:entity].is_a?(Hash) ? Organization.new(**c[:entity]) : c[:entity]
#           ContributionInfo.new(entity: e, role: c[:role])
#         else c
#         end
#       end

#       @abstract = (args[:abstract] || []).map do |a|
#         a.is_a?(Hash) ? FormattedString.new(**a) : a
#       end

#       @copyright = args.fetch(:copyright, []).map do |c|
#         c.is_a?(Hash) ? CopyrightAssociation.new(**c) : c
#       end

#       @docidentifier  = args[:docid] || []
#       @formattedref   = args[:formattedref] if title.empty?
#       @id             = args[:id] || makeid(nil, false)
#       @type           = args[:type]
#       @docnumber      = args[:docnumber]
#       @edition        = args[:edition]
#       @version        = args[:version]
#       @biblionote     = args.fetch :biblionote, BiblioNoteCollection.new([])
#       @language       = args.fetch :language, []
#       @script         = args.fetch :script, []
#       @status         = args[:docstatus]
#       @relation       = DocRelationCollection.new(args[:relation] || [])
#       @link           = args.fetch(:link, []).map do |s|
#         if s.is_a?(Hash) then TypedUri.new(**s)
#         elsif s.is_a?(String) then TypedUri.new(content: s)
#         else s
#         end
#       end
#       @series         = args.fetch :series, []
#       @medium         = args[:medium]
#       @place          = args.fetch(:place, []).map do |pl|
#         pl.is_a?(String) ? Place.new(name: pl) : pl
#       end
#       @extent         = args[:extent] || []
#       @accesslocation = args.fetch :accesslocation, []
#       @classification = args.fetch :classification, []
#       @validity       = args[:validity]
#       # we should pass the fetched arg from scrappers
#       @fetched        = args.fetch :fetched, nil
#       @keyword        = (args[:keyword] || []).map do |kw|
#         LocalizedString.new(kw)
#       end
#       @license        = args.fetch :license, []
#       @doctype        = args[:doctype]
#       @editorialgroup = args[:editorialgroup]
#       @ics            = args.fetch :ics, []
#       @structuredidentifier = args[:structuredidentifier]
#     end
#     # rubocop:enable Metrics/MethodLength, Metrics/AbcSize
#     # rubocop:enable Metrics/CyclomaticComplexity, Metrics/PerceivedComplexity

#     # @param lang [String] language code Iso639
#     # @return [RelatonBib::FormattedString, Array<RelatonBib::FormattedString>]
#     def abstract(lang: nil)
#       if lang
#         @abstract.detect { |a| a.language&.include? lang }
#       else
#         @abstract
#       end
#     end

#     # @param id [RelatonBib::DocumentIdentifier]
#     # @param attribute [boolean, nil]
#     # @return [String]
#     def makeid(id, attribute)
#       return nil if attribute && !@id_attribute

#       id ||= @docidentifier.reject { |i| i.type == "DOI" }[0]
#       return unless id

#       # contribs = publishers.map { |p| p&.entity&.abbreviation }.join '/'
#       # idstr = "#{contribs}#{delim}#{id.project_number}"
#       # idstr = id.project_number.to_s
#       idstr = id.id.gsub(/:/, "-").gsub /\s/, ""
#       # if id.part_number&.size&.positive? then idstr += "-#{id.part_number}"
#       idstr.strip
#     end

#     # @param identifier [RelatonBib::DocumentIdentifier]
#     # @param options [Hash]
#     # @option options [boolean, nil] :no_year
#     # @option options [boolean, nil] :all_parts
#     # @return [String]
#     def shortref(identifier, **opts) # rubocop:disable Metrics/CyclomaticComplexity,Metrics/AbcSize,Metrics/PerceivedComplexity
#       pubdate = date.select { |d| d.type == "published" }
#       year = if opts[:no_year] || pubdate.empty? then ""
#              else ":" + pubdate&.first&.on(:year).to_s
#              end
#       year += ": All Parts" if opts[:all_parts] || @all_parts

#       "#{makeid(identifier, false)}#{year}"
#     end

#     # @param opts [Hash]
#     # @option opts [Nokogiri::XML::Builder] :builder XML builder
#     # @option opts [Boolean] :bibdata
#     # @option opts [Symbol, NilClass] :date_format (:short), :full
#     # @option opts [String, Symbol] :lang language
#     # @return [String] XML
#     def to_xml(**opts, &block)
#       if opts[:builder]
#         render_xml **opts, &block
#       else
#         Nokogiri::XML::Builder.new(encoding: "UTF-8") do |xml|
#           render_xml builder: xml, **opts, &block
#         end.doc.root.to_xml
#       end
#     end

#     # @return [Hash]
#     def to_hash # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/MethodLength, Metrics/PerceivedComplexity
#       hash = {}
#       hash["id"] = id if id
#       hash["title"] = single_element_array(title) if title&.any?
#       hash["link"] = single_element_array(link) if link&.any?
#       hash["type"] = type if type
#       hash["docid"] = single_element_array(docidentifier) if docidentifier&.any?
#       hash["docnumber"] = docnumber if docnumber
#       hash["date"] = single_element_array(date) if date&.any?
#       if contributor&.any?
#         hash["contributor"] = single_element_array(contributor)
#       end
#       hash["edition"] = edition if edition
#       hash["version"] = version.to_hash if version
#       hash["revdate"] = revdate if revdate
#       hash["biblionote"] = single_element_array(biblionote) if biblionote&.any?
#       hash["language"] = single_element_array(language) if language&.any?
#       hash["script"] = single_element_array(script) if script&.any?
#       hash["formattedref"] = formattedref.to_hash if formattedref
#       hash["abstract"] = single_element_array(abstract) if abstract&.any?
#       hash["docstatus"] = status.to_hash if status
#       hash["copyright"] = single_element_array(copyright) if copyright&.any?
#       hash["relation"] = single_element_array(relation) if relation&.any?
#       hash["series"] = single_element_array(series) if series&.any?
#       hash["medium"] = medium.to_hash if medium
#       hash["place"] = single_element_array(place) if place&.any?
#       hash["extent"] = single_element_array(extent) if extent&.any?
#       if accesslocation&.any?
#         hash["accesslocation"] = single_element_array(accesslocation)
#       end
#       if classification&.any?
#         hash["classification"] = single_element_array(classification)
#       end
#       hash["validity"] = validity.to_hash if validity
#       hash["fetched"] = fetched.to_s if fetched
#       hash["keyword"] = single_element_array(keyword) if keyword&.any?
#       hash["license"] = single_element_array(license) if license&.any?
#       hash["doctype"] = doctype if doctype
#       if editorialgroup&.presence?
#         hash["editorialgroup"] = editorialgroup.to_hash
#       end
#       hash["ics"] = single_element_array ics if ics.any?
#       if structuredidentifier&.presence?
#         hash["structuredidentifier"] = structuredidentifier.to_hash
#       end
#       hash
#     end

#     # @param bibtex [BibTeX::Bibliography, NilClass]
#     # @return [String]
#     def to_bibtex(bibtex = nil) # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/MethodLength
#       item = BibTeX::Entry.new
#       item.type = bibtex_type
#       item.key = id
#       bibtex_title item
#       item.edition = edition if edition
#       bibtex_author item
#       bibtex_contributor item
#       item.address = place.first.name if place.any?
#       bibtex_note item
#       bibtex_relation item
#       bibtex_extent item
#       bibtex_date item
#       bibtex_series item
#       bibtex_classification item
#       item.keywords = keyword.map(&:content).join(", ") if keyword.any?
#       bibtex_docidentifier item
#       item.timestamp = fetched.to_s if fetched
#       bibtex_link item
#       bibtex ||= BibTeX::Bibliography.new
#       bibtex << item
#       bibtex.to_s
#     end

#     # @param lang [String, nil] language code Iso639
#     # @return [RelatonIsoBib::TypedTitleStringCollection]
#     def title(lang: nil)
#       @title.lang lang
#     end

#     # @param type [Symbol] type of url, can be :src/:obp/:rss
#     # @return [String]
#     def url(type = :src)
#       @link.detect { |s| s.type == type.to_s }&.content&.to_s
#     end

#     def abstract=(value)
#       @abstract = value
#     end

#     def deep_clone
#       dump = Marshal.dump self
#       Marshal.load dump # rubocop:disable Security/MarshalLoad
#     end

#     def disable_id_attribute
#       @id_attribute = false
#     end

#     # remove title part components and abstract
#     def to_all_parts # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/MethodLength,Metrics/PerceivedComplexity
#       me = deep_clone
#       me.disable_id_attribute
#       me.relation << DocumentRelation.new(type: "instance", bibitem: self)
#       me.language.each do |l|
#         me.title.delete_title_part!
#         ttl = me.title.select do |t|
#           t.type != "main" && t.title.language&.include?(l)
#         end
#         tm_en = ttl.map { |t| t.title.content }.join " – "
#         me.title.detect do |t|
#           t.type == "main" && t.title.language&.include?(l)
#         end&.title&.content = tm_en
#       end
#       me.abstract = []
#       me.docidentifier.each(&:remove_part)
#       me.docidentifier.each(&:all_parts)
#       me.structuredidentifier.remove_part
#       me.structuredidentifier.all_parts
#       me.docidentifier.each &:remove_date
#       me.structuredidentifier&.remove_date
#       me.all_parts = true
#       me
#     end

#     # convert ISO:yyyy reference to reference to most recent
#     # instance of reference, removing date-specific infomration:
#     # date of publication, abstracts. Make dated reference Instance relation
#     # of the redacated document
#     def to_most_recent_reference
#       me = deep_clone
#       disable_id_attribute
#       me.relation << DocumentRelation.new(type: "instance", bibitem: self)
#       me.abstract = []
#       me.date = []
#       me.docidentifier.each &:remove_date
#       me.structuredidentifier&.remove_date
#       me.id&.sub! /-[12]\d\d\d/, ""
#       me
#     end

#     # If revision_date exists then returns it else returns published date or nil
#     # @return [String, NilClass]
#     def revdate # rubocop:disable Metrics/CyclomaticComplexity,Metrics/PerceivedComplexity
#       @revdate ||= if version&.revision_date
#                      version.revision_date
#                    else
#                      date.detect { |d| d.type == "published" }&.on&.to_s
#                    end
#     end

#     # @param prefix [String]
#     # @return [String]
#     def to_asciibib(prefix = "") # rubocop:disable Metrics/AbcSize, Metrics/CyclomaticComplexity, Metrics/MethodLength, Metrics/PerceivedComplexity
#       pref = prefix.empty? ? prefix : prefix + "."
#       out = prefix.empty? ? "[%bibitem]\n== {blank}\n" : ""
#       out += "#{pref}id:: #{id}\n" if id
#       out += "#{pref}fetched:: #{fetched}\n" if fetched
#       title.each { |t| out += t.to_asciibib(prefix, title.size) }
#       out += "#{pref}type:: #{type}\n" if type
#       docidentifier.each do |di|
#         out += di.to_asciibib prefix, docidentifier.size
#       end
#       out += "#{pref}docnumber:: #{docnumber}\n" if docnumber
#       out += "#{pref}edition:: #{edition}\n" if edition
#       language.each { |l| out += "#{pref}language:: #{l}\n" }
#       script.each { |s| out += "#{pref}script:: #{s}\n" }
#       out += version.to_asciibib prefix if version
#       biblionote&.each { |b| out += b.to_asciibib prefix, biblionote.size }
#       out += status.to_asciibib prefix if status
#       date.each { |d| out += d.to_asciibib prefix, date.size }
#       abstract.each do |a|
#         out += a.to_asciibib "#{pref}abstract", abstract.size
#       end
#       copyright.each { |c| out += c.to_asciibib prefix, copyright.size }
#       link.each { |l| out += l.to_asciibib prefix, link.size }
#       out += medium.to_asciibib prefix if medium
#       place.each { |pl| out += pl.to_asciibib prefix, place.size }
#       extent.each { |ex| out += ex.to_asciibib "#{pref}extent", extent.size }
#       accesslocation.each { |al| out += "#{pref}accesslocation:: #{al}\n" }
#       classification.each do |cl|
#         out += cl.to_asciibib prefix, classification.size
#       end
#       out += validity.to_asciibib prefix if validity
#       contributor.each do |c|
#         out += c.to_asciibib "contributor.*", contributor.size
#       end
#       out += relation.to_asciibib prefix if relation
#       series.each { |s| out += s.to_asciibib prefix, series.size }
#       out += "#{pref}doctype:: #{doctype}\n" if doctype
#       out += "#{pref}formattedref:: #{formattedref}\n" if formattedref
#       keyword.each { |kw| out += kw.to_asciibib "#{pref}keyword", keyword.size }
#       out += editorialgroup.to_asciibib prefix if editorialgroup
#       ics.each { |i| out += i.to_asciibib prefix, ics.size }
#       out += structuredidentifier.to_asciibib prefix if structuredidentifier
#       out
#     end

#     private

#     # @return [String]
#     def bibtex_title(item)
#       title.each do |t|
#         case t.type
#         when "main" then item.tile = t.title.content
#         end
#       end
#     end

#     # @return [String]
#     def bibtex_type
#       case type
#       when "standard", nil then "misc"
#       else type
#       end
#     end

#     # rubocop:disable Metrics/AbcSize, Metrics/MethodLength

#     # @param [BibTeX::Entry]
#     def bibtex_author(item) # rubocop:disable Metrics/CyclomaticComplexity,Metrics/PerceivedComplexity
#       authors = contributor.select do |c|
#         c.entity.is_a?(Person) && c.role.map(&:type).include?("author")
#       end.map &:entity

#       return unless authors.any?

#       item.author = authors.map do |a|
#         if a.name.surname
#           "#{a.name.surname}, #{a.name.forename.map(&:to_s).join(' ')}"
#         else
#           a.name.completename.to_s
#         end
#       end.join " and "
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_contributor(item) # rubocop:disable Metrics/CyclomaticComplexity
#       contributor.each do |c|
#         rls = c.role.map(&:type)
#         if rls.include?("publisher") then item.publisher = c.entity.name
#         elsif rls.include?("distributor")
#           case type
#           when "techreport" then item.institution = c.entity.name
#           when "inproceedings", "conference", "manual", "proceedings"
#             item.organization = c.entity.name
#           when "mastersthesis", "phdthesis" then item.school = c.entity.name
#           end
#         end
#       end
#     end
#     # rubocop:enable Metrics/AbcSize, Metrics/MethodLength

#     # @param [BibTeX::Entry]
#     def bibtex_note(item) # rubocop:disable Metrics/CyclomaticComplexity,Metrics/AbcSize
#       biblionote.each do |n|
#         case n.type
#         when "annote" then item.annote = n.content
#         when "howpublished" then item.howpublished = n.content
#         when "comment" then item.comment = n.content
#         when "tableOfContents" then item.content = n.content
#         when nil then item.note = n.content
#         end
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_relation(item)
#       rel = relation.detect { |r| r.type == "partOf" }
#       if rel
#         title_main = rel.bibitem.title.detect { |t| t.type == "main" }
#         item.booktitle = title_main.title.content
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_extent(item)
#       extent.each do |e|
#         case e.type
#         when "chapter" then item.chapter = e.reference_from
#         when "page"
#           value = e.reference_from
#           value += "-#{e.reference_to}" if e.reference_to
#           item.pages = value
#         when "volume" then item.volume = e.reference_from
#         end
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_date(item)
#       date.each do |d|
#         case d.type
#         when "published"
#           item.year = d.on :year
#           item.month = d.on :month
#         when "accessed" then item.urldate = d.on.to_s
#         end
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_series(item)
#       series.each do |s|
#         case s.type
#         when "journal"
#           item.journal = s.title.title
#           item.number = s.number if s.number
#         when nil then item.series = s.title.title
#         end
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_classification(item)
#       classification.each do |c|
#         case c.type
#         when "type" then item["type"] = c.value
#         # when "keyword" then item.keywords = c.value
#         when "mendeley" then item["mendeley-tags"] = c.value
#         end
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_docidentifier(item)
#       docidentifier.each do |i|
#         case i.type
#         when "isbn" then item.isbn = i.id
#         when "lccn" then item.lccn = i.id
#         when "issn" then item.issn = i.id
#         end
#       end
#     end

#     # @param [BibTeX::Entry]
#     def bibtex_link(item)
#       link.each do |l|
#         case l.type
#         when "doi" then item.doi = l.content
#         when "file" then item.file2 = l.content
#         when "src" then item.url = l.content
#         end
#       end
#     end

#     # rubocop:disable Metrics/AbcSize, Metrics/MethodLength
#     # rubocop:disable Metrics/CyclomaticComplexity, Metrics/PerceivedComplexity
#     # rubocop:disable Style/NestedParenthesizedCalls, Metrics/BlockLength

#     # @param opts [Hash]
#     # @option opts [Nokogiri::XML::Builder] :builder XML builder
#     # @option opts [Boolean] bibdata
#     # @option opts [Symbol, NilClass] :date_format (:short), :full
#     # @option opts [String] :lang language
#     def render_xml(**opts)
#       root = opts[:bibdata] ? :bibdata : :bibitem
#       xml = opts[:builder].send(root) do |builder|
#         builder.fetched fetched if fetched
#         title.to_xml **opts
#         formattedref&.to_xml builder
#         link.each { |s| s.to_xml builder }
#         docidentifier.each { |di| di.to_xml **opts }
#         builder.docnumber docnumber if docnumber
#         date.each { |d| d.to_xml builder, **opts }
#         contributor.each do |c|
#           builder.contributor do
#             c.role.each { |r| r.to_xml **opts }
#             c.to_xml **opts
#           end
#         end
#         builder.edition edition if edition
#         version&.to_xml builder
#         biblionote.to_xml **opts
#         opts[:note]&.each do |n|
#           builder.note(n[:text], format: "text/plain", type: n[:type])
#         end
#         language.each { |l| builder.language l }
#         script.each { |s| builder.script s }
#         abstr = abstract.select { |ab| ab.language&.include? opts[:lang] }
#         abstr = abstract unless abstr.any?
#         abstr.each { |a| builder.abstract { a.to_xml(builder) } }
#         status&.to_xml builder
#         copyright&.each { |c| c.to_xml **opts }
#         relation.each { |r| r.to_xml builder, **opts }
#         series.each { |s| s.to_xml builder }
#         medium&.to_xml builder
#         place.each { |pl| pl.to_xml builder }
#         extent.each { |e| builder.extent { e.to_xml builder } }
#         accesslocation.each { |al| builder.accesslocation al }
#         license.each { |l| builder.license l }
#         classification.each { |cls| cls.to_xml builder }
#         kwrd = keyword.select { |kw| kw.language&.include? opts[:lang] }
#         kwrd = keyword unless kwrd.any?
#         kwrd.each { |kw| builder.keyword { kw.to_xml(builder) } }
#         validity&.to_xml builder
#         if block_given? then yield builder
#         elsif opts[:bibdata] && (doctype || editorialgroup || ics&.any? ||
#                                  structuredidentifier&.presence?)
#           builder.ext do |b|
#             b.doctype doctype if doctype
#             editorialgroup&.to_xml b
#             ics.each { |i| i.to_xml b }
#             structuredidentifier&.to_xml b
#           end
#         end
#       end
#       xml[:id] = id if id && !opts[:bibdata] && !opts[:embedded]
#       xml[:type] = type if type
#       xml
#     end
#     # rubocop:enable Metrics/AbcSize, Metrics/MethodLength
#     # rubocop:enable Metrics/CyclomaticComplexity, Metrics/PerceivedComplexity
#     # rubocop:enable Style/NestedParenthesizedCalls, Metrics/BlockLength
#   end
# end
