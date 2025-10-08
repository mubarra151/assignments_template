import datetime
import xml.sax.saxutils as saxutils
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
 </Types>
"""

RELS = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""

def build_core_xml(title: str = "LLM Security Draft", creator: str = "") -> str:
    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    return f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<cp:coreProperties xmlns:cp=\"http://schemas.openxmlformats.org/package/2006/core-properties\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:dcterms=\"http://purl.org/dc/terms/\" xmlns:dcmitype=\"http://purl.org/dc/dcmitype/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">
  <dc:title>{saxutils.escape(title)}</dc:title>
  <dc:creator>{saxutils.escape(creator)}</dc:creator>
  <cp:lastModifiedBy>{saxutils.escape(creator or 'generator')}</cp:lastModifiedBy>
  <dcterms:created xsi:type=\"dcterms:W3CDTF\">{now}</dcterms:created>
  <dcterms:modified xsi:type=\"dcterms:W3CDTF\">{now}</dcterms:modified>
</cp:coreProperties>
"""

APP = """<?xml version="1.0" encoding="UTF-8"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Python zip writer</Application>
</Properties>
"""

DOC_XML_HEADER = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
    "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
    "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
    "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
    "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
    "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
    "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
    "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
    "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
    "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
    "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
    "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
    "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
    "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
    "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
    "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" mc:Ignorable=\"w14 wp14\"><w:body>"
)

DOC_XML_FOOTER = "<w:sectPr><w:pgSz w:w=11906 w:h=16838/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\" w:header=\"708\" w:footer=\"708\" w:gutter=\"0\"/></w:sectPr></w:body></w:document>"


def para_xml(text: str, bold: bool = False) -> str:
    text = saxutils.escape(text)
    if bold:
        return f"<w:p><w:r><w:rPr><w:b/></w:rPr><w:t>{text}</w:t></w:r></w:p>"
    return f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>"


def md_lines_to_paragraphs(md_text: str) -> str:
    xml_parts = []
    for raw in md_text.splitlines():
        line = raw.rstrip("\n")
        if not line.strip():
            xml_parts.append("<w:p/>")
            continue
        if line.startswith("### "):
            xml_parts.append(para_xml(line[4:].strip(), bold=True))
            continue
        if line.startswith("## "):
            xml_parts.append(para_xml(line[3:].strip(), bold=True))
            continue
        if line.lstrip().startswith("- "):
            text = line.lstrip()[2:].strip()
            xml_parts.append(para_xml("• " + text, bold=False))
            continue
        xml_parts.append(para_xml(line))
    return "".join(xml_parts)


def write_docx_from_markdown(src_md: Path, dst_docx: Path, title: str = "LLM Security Draft", creator: str = "") -> None:
    md_text = src_md.read_text(encoding="utf-8")
    document_xml = DOC_XML_HEADER + md_lines_to_paragraphs(md_text) + DOC_XML_FOOTER
    with ZipFile(dst_docx, "w", ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", CONTENT_TYPES)
        zf.writestr("_rels/.rels", RELS)
        zf.writestr("docProps/core.xml", build_core_xml(title=title, creator=creator))
        zf.writestr("docProps/app.xml", APP)
        zf.writestr("word/document.xml", document_xml)


def main():
    src = Path("/workspace/llm-security-intro-related-methodology.md")
    dst = Path("/workspace/llm-security-intro-related-methodology.docx")
    if not src.exists():
        raise SystemExit(f"Source not found: {src}")
    write_docx_from_markdown(src, dst, title="Prompt Injection and Data Leakage", creator="Thesis Draft")
    print(f"Wrote {dst}")


if __name__ == "__main__":
    main()

