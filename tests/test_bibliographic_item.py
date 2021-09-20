import pytest

import datetime
from typing import TYPE_CHECKING

from relaton_bib.bibliographic_item import BibliographicItem, \
    BibliographicItemType
from relaton_bib.address import Address
from relaton_bib.contact import Contact
from relaton_bib.affiliation import Affiliation
from relaton_bib.typed_uri import TypedUri
from relaton_bib.document_identifier import DocumentIdentifier, DocumentIdType
from relaton_bib.copyright_association import CopyrightAssociation
from relaton_bib.formatted_string import FormattedString
from relaton_bib.contribution_info import ContributionInfo, ContributorRole
from relaton_bib.bibliographic_date import BibliographicDate, \
    BibliographicDateType
from relaton_bib.series import Series
from relaton_bib.document_status import DocumentStatus
from relaton_bib.organization import Organization, OrgIdentifier
from relaton_bib.localized_string import LocalizedString
from relaton_bib.typed_title_string import TypedTitleString, \
    TypedTitleStringCollection
from relaton_bib.technical_committee import TechnicalCommittee
from relaton_bib.formatted_ref import FormattedRef
from relaton_bib.medium import Medium
from relaton_bib.classification import Classification
from relaton_bib.validity import Validity
from relaton_bib.bib_item_locality import BibItemLocality, Locality, \
    BibItemLocalityType, SourceLocalityStack, SourceLocality, LocalityStack
from relaton_bib.biblio_note import BiblioNote, BiblioNoteCollection
from relaton_bib.biblio_version import BibliographicItemVersion
from relaton_bib.place import Place
from relaton_bib.person import Person, FullName, PersonIdentifier
from relaton_bib.structured_identifier import StructuredIdentifierCollection
from relaton_bib.editorial_group import EditorialGroup
from relaton_bib.ics import ICS
from relaton_bib.document_relation_collection import DocRelationCollection
from relaton_bib.document_relation import DocumentRelation
from relaton_bib.workgroup import WorkGroup
from relaton_bib.structured_identifier import StructuredIdentifier


@pytest.fixture
def subject():
    return BibliographicItem(
        id="ISOTC211",
        title=[
            LocalizedString("Geographic information"),
            LocalizedString(content="Information géographique",
                            language="fr",
                            script="Latn"),
        ],
        type=BibliographicItemType.STANDARD,
        doctype="document",
        subdoctype="subdocument",
        docidentifier=[
            DocumentIdentifier("TC211", DocumentIdType.ISO),
            DocumentIdentifier("ISBN", "isbn"),
            DocumentIdentifier("LCCN", "lccn"),
            DocumentIdentifier("ISSN", "issn", "series"),
            DocumentIdentifier("urn:iso:std:iso:123:stage-90.93:ed-3:en,fr",
                               "URN"),
            DocumentIdentifier("XYZ"),
        ],
        docnumber="123456",
        edition="1",
        language=["en", "fr"],
        script="Latn",
        version=BibliographicItemVersion(revision_date="2019-04-01",
                                         draft=["draft"]),
        biblionote=BiblioNoteCollection([
            BiblioNote(content="An note", type="annote"),
            BiblioNote(content="How published", type="howpublished"),
            BiblioNote(content="Comment", type="comment"),
            BiblioNote(content="Table Of Contents", type="tableOfContents"),

        ]),
        docstatus=DocumentStatus(
            stage=DocumentStatus.Stage(value="30", abbreviation="CD"),
            substage=DocumentStatus.Stage(value="substage"),
            iteration="final"
        ),
        date=[
            BibliographicDate(
                type=BibliographicDateType.ISSUED, on="2014"),
            BibliographicDate(
                type=BibliographicDateType.PUBLISHED, on="2014-04"),
            BibliographicDate(
                type=BibliographicDateType.ACCESSED, on="2015-05-20")
        ],
        abstract=[
            FormattedString(
                content="ISO 19115-1:2014 defines the schema required for ...",
                language="en",
                script="Latn",
                format="text/plain"
            ),
            FormattedString(
                content="ISO 19115-1:2014 defines the schema required for ...",
                language="en",
                script="Latn",
                format="text/plain"
            ),
            FormattedString(
                content="L'ISO 19115-1:2014 définit le schéma requis pour ...",
                language="fr",
                script="Latn",
                format="text/plain"
            )
        ],
        contributor=[
            ContributionInfo(
                role=[
                    ContributorRole(
                        type="publisher",
                        description=[FormattedString("Publisher role")])
                ],
                entity=Organization(
                    name="International Organization for Standardization",
                    abbreviation="ISO",
                    subdivision="division")
            ),
            ContributionInfo(
                role=[ContributorRole(type="author")],
                entity=Person(
                    name=FullName(completename=LocalizedString(
                        content="A. Bierman",
                        language="en",
                        script="Latn")),
                    affiliation=Affiliation(Organization(
                        name="IETF",
                        abbreviation="IETF",
                        identifier=OrgIdentifier(
                            type="uri",
                            value="www.ietf.org")
                    )),
                    contact=[
                        Address(
                            street=["Street"],
                            city="City",
                            postcode="123456",
                            country="Country",
                            state="State"),
                        Contact(type="phone", value="223322")
                    ]
                )
            ),
            ContributionInfo(
                role=[
                    ContributorRole(
                        type="publisher",
                        description=[FormattedString("Publisher descr")]),
                    ContributorRole(
                        type="editor",
                        description=[FormattedString("Editor description")])
                ],
                entity=Organization(
                    name="IETF",
                    abbreviation="IETF",
                    identifier=OrgIdentifier(
                        type="uri",
                        value="www.ietf.org"))
            ),
            ContributionInfo(
                role=[ContributorRole(type="author")],
                entity=Person(
                    name=FullName(
                        completename=LocalizedString(
                            content="A. Bierman",
                            language="en", script="Latn"),
                        initial="A.",
                        surname="Bierman",
                        forename="Forename",
                        addition="Addition",
                        prefix="Prefix"),
                    affiliation=Affiliation(
                        organization=Organization(
                            name="IETF",
                            abbreviation="IETF",
                            identifier=OrgIdentifier(
                                type="uri",
                                value="www.ietf.org")),
                        description=FormattedString(
                            content="Description",
                            language="en")
                    ),
                    contact=[
                        Address(
                            street=["Street"],
                            city="City",
                            postcode="123456",
                            country="Country",
                            state="State"),
                        Contact(type="phone", value="223322")
                    ],
                    identifier=PersonIdentifier(
                        type="uri",
                        value="www.person.com")
                )
            ),
            ContributionInfo(
                entity=Organization(name="Institution"),
                role=[ContributorRole(
                    type="distributor",
                    description=[FormattedString("sponsor")])],
            )
        ],
        copyright=[CopyrightAssociation(
            owner=[ContributionInfo(
                Organization(
                    name="International Organization for Standardization",
                    abbreviation="ISO",
                    identifier=OrgIdentifier(
                        type="uri",
                        value="www.ietf.org")))],
            from_="2014",
            to="2020",
            scope="Scope"
        )],
        link=[
            TypedUri(type="src",
                     content="https://www.iso.org/standard/53798.html"),
            TypedUri(type="obp",
                     content="https://www.iso.org/obp/ui/#!iso:std:53798:en"),
            TypedUri(
                type="rss",
                content="https://www.iso.org/contents/data/standard/05/37/53798\
                         .detail.rss"),
            TypedUri(type="doi", content="http://standrd.org/doi-123"),
            TypedUri(type="file", content="file://path/file"),
        ],
        relation=DocRelationCollection([
            DocumentRelation(
                type=DocumentRelation.Type.updates,
                bibitem=BibliographicItem(
                    formattedref=FormattedRef("ISO 19115:2003")),
                locality=[
                    LocalityStack([
                        Locality(
                            type="section",
                            reference_from="Reference from")
                    ]),
                    LocalityStack([
                        Locality(type="chapter", reference_from="1"),
                        Locality(type="page", reference_from="2")
                    ])
                ],
                source_locality=[
                    SourceLocalityStack([
                        SourceLocality(type="volume", reference_from="2"),
                        SourceLocality(type="chapter", reference_from="3")

                    ])
                ]),
            DocumentRelation(
                type=DocumentRelation.Type.obsoletes,
                description=FormattedString(format="text/plain",
                                            content="supersedes"),
                bibitem=BibliographicItem(
                    type=BibliographicItemType.STANDARD,
                    formattedref=FormattedRef("ISO 19115:2003/Cor 1:2006"))),
            DocumentRelation(
                type=DocumentRelation.Type.partOf,
                bibitem=BibliographicItem(
                    title=TypedTitleStringCollection(
                        [TypedTitleString(type="main", content="Book title")]))
            )
        ]),
        series=[
            Series(
                type="main",
                title=TypedTitleString(
                    type="original",
                    content="ISO/IEC FDIS 10118-3",
                    language="en",
                    script="Latn",
                    format="text/plain"
                ),
                place="Serie's place",
                organization="Serie's organization",
                abbreviation=LocalizedString("ABVR"),
                from_="2009-02-01",
                to="2010-12-20",
                number="serie1234",
                partnumber="part5678"),
            Series(
                type="alt",
                formattedref=FormattedRef(
                    content="serieref",
                    language="en",
                    script="Latn")
            ),
            Series(
                type="journal",
                title=TypedTitleString(content="Journal"),
                number="7"
            ),
            Series(
                title=TypedTitleString(content=[
                    LocalizedString(content="Series",
                                    language="en",
                                    script="Latn"),
                    LocalizedString(content="Séries",
                                    language="fr",
                                    script="Latn")])
            ),
        ],
        medium=Medium(
            form="medium form",
            size="medium size",
            scale="medium scale"),
        place=[
            Place("bib place"),
            Place(name="Geneva", uri="geneva.place", region="Switzelznd")
        ],
        extent=[
            BibItemLocality(
                type=BibItemLocalityType.SECTION,
                reference_from="Reference from",
                reference_to="Reference to"),
            BibItemLocality(
                type=BibItemLocalityType.CHAPTER,
                reference_from="4"),
            BibItemLocality(
                type=BibItemLocalityType.PAGE,
                reference_from="10",
                reference_to="20"),
            BibItemLocality(
                type=BibItemLocalityType.VOLUME,
                reference_from="1"),
        ],
        accesslocation=["accesslocation1", "accesslocation2"],
        classification=[
            Classification(type="type", value="value"),
            Classification("keyword", "Keywords"),
            Classification("mendeley", "Mendeley Tags")
        ],
        keyword=["Keyword", "Key Word"],
        license=["License"],
        validity=Validity(
            begins=datetime.datetime.strptime("2010-10-10 12:21",
                                              Validity.FORMAT),
            ends=datetime.datetime.strptime("2011-02-03 18:30",
                                            Validity.FORMAT),
            revision=datetime.datetime.strptime("2011-03-04 09:00",
                                                Validity.FORMAT),
        ),
        editorialgroup=EditorialGroup([
            TechnicalCommittee(
                WorkGroup(
                    content="Editorial group",
                    number=1,
                    type="Type",
                    # identifier="Identifier",
                    # prefix="Prefix"
                ))
        ]),
        ics=ICS(code="01", text="First"),
        structuredidentifier=StructuredIdentifierCollection([
            StructuredIdentifier(
                type="type 1",
                agency=["agency 1", "agency 2"],
                class_="class 1",
                docnumber="123",
                partnumber="4",
                edition="1",
                version="2",
                supplementtype="type 2",
                supplementnumber="5",
                language="en",
                year="2020"),
            StructuredIdentifier(docnumber="456", agency=["agency 3"])
        ])
    )


def test_subject_created(subject):
    assert type(subject) == BibliographicItem

# RSpec.describe "RelatonBib" => :BibliographicItem do
#   context "instance" do
#     subject do
#       hash = YAML.load_file "spec/examples/bib_item.yml"
#       hash_bib = RelatonBib::HashConverter.hash_to_bib hash

#       RelatonBib::BibliographicItem.new(**hash_bib)
#     end

#     it "is instance of BibliographicItem" do
#       expect(subject).to be_instance_of RelatonBib::BibliographicItem
#     end

#     it "has array of titiles" do
#       expect(subject.title).to be_instance_of(
#         RelatonBib::TypedTitleStringCollection
#       )
#       expect(subject.title(lang: "fr")[0].title.content).to eq(
#         "Information g\u00E9ographique"
#       )
#     end

#     it "has urls" do
#       expect(subject.url).to eq "https://www.iso.org/standard/53798.html"
#       expect(subject.url(:rss)).to eq "https://www.iso.org/contents/data/"\
#                                           "standard/05/37/53798.detail.rss"
#     end
#     it "returns shortref" do
#       expect(subject.shortref(subject.docidentifier.first)).to eq "TC211:2014"
#     end

#     it "returns abstract with en language" do
#       expect(subject.abstract(lang: "en")).to be_instance_of(
#         RelatonBib::FormattedString
#       )
#     end

#     it "to most recent reference" do
#       item = subject.to_most_recent_reference
#       expect(item.relation[3].bibitem.structuredidentifier[0].year).to eq "2020"
#       expect(item.structuredidentifier[0].year).to be_nil
#     end

#     it "to all parts" do
#       item = subject.to_all_parts
#       expect(item).to_not be subject
#       expect(item.all_parts).to be true
#       expect(item.relation.last.type).to eq "instance"
#       expect(item.title.detect { |t| t.type == "title-part" }). to be_nil
#       expect(item.title.detect { |t| t.type == "main" }.title.content).to eq(
#         "Geographic information"
#       )
#       expect(item.abstract).to be_empty
#       expect(item.docidentifier.detect { |d| d.id =~ /-\d/ }).to be_nil
#       expect(item.docidentifier.reject { |d| d.id =~ %r{(all parts)} }.size)
#         .to eq 1
#       expect(item.docidentifier.detect { |d| d.id =~ /:[12]\d\d\d/ }).to be_nil
#       expect(item.structuredidentifier.detect { |d| !d.partnumber.nil? })
#         .to be_nil
#       expect(item.structuredidentifier.detect { |d| d.docnumber =~ /-\d/ })
#         .to be_nil
#       expect(
#         item.structuredidentifier.detect { |d| d.docnumber !~ %r{(all parts)} }
#       ).to be_nil
#       expect(
#         item.structuredidentifier.detect { |d| d.docnumber =~ /:[12]\d\d\d/ }
#       ).to be_nil
#     end

#     it "returns bibitem xml string" do
#       file = "spec/examples/bib_item.xml"
#       subject_xml = subject.to_xml
#       File.write file, subject_xml, encoding: "utf-8" unless File.exist? file
#       xml = File.read(file, encoding: "utf-8").gsub(
#         /<fetched>\d{4}-\d{2}-\d{2}/, "<fetched>#{Date.today}"
#       )
#       expect(subject_xml).to be_equivalent_to xml
#       schema = Jing.new "grammars/biblio.rng"
#       errors = schema.validate file
#       expect(errors).to eq []
#     end

#     it "returns bibdata xml string" do
#       file = "spec/examples/bibdata_item.xml"
#       subject_xml = subject.to_xml bibdata: true
#       File.write file, subject_xml, encoding: "utf-8" unless File.exist? file
#       xml = File.read(file, encoding: "utf-8").gsub(
#         /<fetched>\d{4}-\d{2}-\d{2}/, "<fetched>#{Date.today}"
#       )
#       expect(subject_xml).to be_equivalent_to xml
#       schema = Jing.new "spec/examples/isobib.rng"
#       errors = schema.validate file
#       expect(errors).to eq []
#     end

#     it "render only French laguage tagged string" do
#       file = "spec/examples/bibdata_item_fr.xml"
#       xml = subject.to_xml bibdata: true, lang: "fr"
#       File.write file, xml, encoding: "UTF-8" unless File.exist? file
#       expect(xml).to be_equivalent_to File.read(file, encoding: "UTF-8")
#         .sub /(?<=<fetched>)\d{4}-\d{2}-\d{2}/, Date.today.to_s
#     end

#     it "render addition elements" do
#       xml = subject.to_xml { |b| b.element "test" }
#       expect(xml).to include "<element>test</element>"
#     end

#     it "add note to xml" do
#       xml = subject.to_xml note: [{ text: "Note", type: "note" }]
#       expect(xml).to include "<note format=\"text/plain\" type=\"note\">"\
#       "Note</note>"
#     end

#     it "deals with hashes" do
#       file = "spec/examples/bib_item.yml"
#       h = RelatonBib::HashConverter.hash_to_bib(YAML.load_file(file))
#       b = RelatonBib::BibliographicItem.new(**h)
#       expect(b.to_xml).to be_equivalent_to subject.to_xml
#     end

#     it "converts item to hash" do
#       hash = subject.to_hash
#       file = "spec/examples/hash.yml"
#       File.write file, hash.to_yaml unless File.exist? file
#       h = YAML.load_file(file)
#       h["fetched"] = Date.today.to_s
#       expect(hash).to eq h
#       expect(hash["revdate"]).to eq "2019-04-01"
#     end

#     context "converts to BibTex" do
#       it "standard" do
#         bibtex = subject.to_bibtex
#         file = "spec/examples/misc.bib"
#         File.write(file, bibtex, encoding: "utf-8") unless File.exist? file
#         expect(bibtex).to eq File.read(file, encoding: "utf-8")
#           .sub(/(?<=timestamp = {)\d{4}-\d{2}-\d{2}/, Date.today.to_s)
#       end

#       it "techreport" do
#         expect(subject).to receive(:type).and_return("techreport")
#           .at_least :once
#         bibtex = subject.to_bibtex
#         file = "spec/examples/techreport.bib"
#         File.write(file, bibtex, encoding: "utf-8") unless File.exist? file
#         expect(bibtex).to eq File.read(file, encoding: "utf-8")
#           .sub(/(?<=timestamp = {)\d{4}-\d{2}-\d{2}/, Date.today.to_s)
#       end

#       it "manual" do
#         expect(subject).to receive(:type).and_return("manual").at_least :once
#         bibtex = subject.to_bibtex
#         file = "spec/examples/manual.bib"
#         File.write(file, bibtex, encoding: "utf-8") unless File.exist? file
#         expect(bibtex).to eq File.read(file, encoding: "utf-8")
#           .sub(/(?<=timestamp = {)\d{4}-\d{2}-\d{2}/, Date.today.to_s)
#       end

#       it "phdthesis" do
#         expect(subject).to receive(:type).and_return("phdthesis").at_least :once
#         bibtex = subject.to_bibtex
#         file = "spec/examples/phdthesis.bib"
#         File.write(file, bibtex, encoding: "utf-8") unless File.exist? file
#         expect(bibtex).to eq File.read(file, encoding: "utf-8")
#           .sub(/(?<=timestamp = {)\d{4}-\d{2}-\d{2}/, Date.today.to_s)
#       end
#     end

#     it "convert item to AsciiBib" do
#       file = "spec/examples/asciibib.adoc"
#       bib = subject.to_asciibib
#       File.write file, bib, encoding: "UTF-8" unless File.exist? file
#       expect(bib).to eq File.read(file, encoding: "UTF-8").gsub(
#         /(?<=fetched::\s)\d{4}-\d{2}-\d{2}/, Date.today.to_s
#       )
#     end
#   end

#   it "initialize with copyright object" do
#     org = RelatonBib::Organization.new(
#       name: "Test Org", abbreviation: "TO", url: "test.org"
#     )
#     owner = [RelatonBib::ContributionInfo.new(entity: org)]
#     copyright = RelatonBib::CopyrightAssociation.new(owner: owner, from: "2018")
#     bibitem = RelatonBib::BibliographicItem.new(
#       formattedref: RelatonBib::FormattedRef.new(content: "ISO123"),
#       copyright: [copyright]
#     )
#     expect(bibitem.to_xml).to include(
#       "<formattedref format=\"text/plain\">ISO123</formattedref>"
#     )
#   end

#   it "warn invalid type argument error" do
#     expect { RelatonBib::BibliographicItem.new type: "type" }.to output(
#       /\[relaton-bib\] document type "type" is invalid./
#     ).to_stderr
#   end

#   context RelatonBib::CopyrightAssociation do
#     it "initialise with owner object" do
#       org = RelatonBib::Organization.new(
#         name: "Test Org", abbreviation: "TO", url: "test.org"
#       )
#       owner = [RelatonBib::ContributionInfo.new(entity: org)]
#       copy = RelatonBib::CopyrightAssociation.new owner: owner, from: "2019"
#       expect(copy.owner).to eq owner
#     end
#   end

#   private

#   # @param content [String]
#   # @return [IsoBibItem::LocalizedString]
#   def localized_string(content, lang = "en")
#     RelatonBib::LocalizedString.new(content, lang)
#   end
# end
