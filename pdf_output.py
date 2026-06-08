import os
from datetime import date
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, ListFlowable, ListItem
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black
from reportlab.lib.units import mm

OUTPUT_DIR = "output"
OUTPUT_FILE = "market_intelligence_report.pdf"

DARK_BLUE = HexColor("#00008B")
DARK_GRAY = HexColor("#404040")
BLACK = black


def build_styles():
    base = getSampleStyleSheet()

    report_title = ParagraphStyle(
        "ReportTitle",
        parent=base["Title"],
        fontSize=20,
        textColor=BLACK,
        fontName="Helvetica-Bold",
        spaceAfter=4,
    )

    report_date = ParagraphStyle(
        "ReportDate",
        parent=base["Normal"],
        fontSize=10,
        textColor=BLACK,
        fontName="Helvetica",
        spaceAfter=12,
    )

    company_heading = ParagraphStyle(
        "CompanyHeading",
        parent=base["Heading1"],
        fontSize=14,
        textColor=DARK_BLUE,
        fontName="Helvetica-Bold",
        spaceBefore=10,
        spaceAfter=6,
    )

    section_label = ParagraphStyle(
        "SectionLabel",
        parent=base["Normal"],
        fontSize=11,
        textColor=BLACK,
        fontName="Helvetica-Bold",
        spaceBefore=8,
        spaceAfter=3,
    )

    content_text = ParagraphStyle(
        "ContentText",
        parent=base["Normal"],
        fontSize=10,
        textColor=DARK_GRAY,
        fontName="Helvetica",
        spaceAfter=4,
        leading=14,
    )

    return {
        "report_title": report_title,
        "report_date": report_date,
        "company_heading": company_heading,
        "section_label": section_label,
        "content_text": content_text,
    }


def add_section(story, styles, label, value):
    if not value:
        return

    story.append(Paragraph(label, styles["section_label"]))

    if isinstance(value, list):
        items = []
        for item in value:
            if item:
                items.append(ListItem(Paragraph(str(item), styles["content_text"]), bulletColor=DARK_GRAY))
        if items:
            story.append(ListFlowable(items, bulletType="bullet", leftIndent=16, bulletFontSize=8))
    else:
        story.append(Paragraph(str(value), styles["content_text"]))


def save_to_pdf(results):
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    except OSError as e:
        print(f"[ERROR] Could not create output directory '{OUTPUT_DIR}': {e}")
        return

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    try:
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm,
        )
    except Exception as e:
        print(f"[ERROR] Could not initialise PDF document: {e}")
        return

    styles = build_styles()
    story = []

    story.append(Paragraph("TIMOCOM Market Intelligence Report", styles["report_title"]))
    story.append(Paragraph(f"Date Generated: {date.today().strftime('%B %d, %Y')}", styles["report_date"]))
    story.append(HRFlowable(width="100%", thickness=1, color=BLACK, spaceAfter=12))

    for idx, company_result in enumerate(results):
        company = company_result.get("company", "Unknown Company")
        analysis = company_result.get("analysis", {})

        story.append(Paragraph(company, styles["company_heading"]))

        if not analysis:
            story.append(Paragraph("No analysis available.", styles["content_text"]))
        elif isinstance(analysis, dict) and "error" in analysis:
            story.append(Paragraph(f"Error: {analysis['error']}", styles["content_text"]))
        else:
            try:
                add_section(story, styles, "Summary", analysis.get("summary"))
            except Exception as e:
                print(f"  [WARNING] Could not write Summary for {company}: {e}")

            try:
                add_section(story, styles, "Key Insights", analysis.get("key_insights"))
            except Exception as e:
                print(f"  [WARNING] Could not write Key Insights for {company}: {e}")

            try:
                add_section(story, styles, "Trends", analysis.get("trends"))
            except Exception as e:
                print(f"  [WARNING] Could not write Trends for {company}: {e}")

            try:
                add_section(story, styles, "Recommendations", analysis.get("recommendations"))
            except Exception as e:
                print(f"  [WARNING] Could not write Recommendations for {company}: {e}")

        if idx < len(results) - 1:
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="100%", thickness=0.5, color=DARK_GRAY, spaceAfter=10))

    try:
        doc.build(story)
        print(f"[SUCCESS] PDF report saved to: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"[ERROR] Failed to save PDF file: {e}")


if __name__ == "__main__":
    from scraper import scrape_websites, WEBSITES
    from processor import process_results

    scraped_data = scrape_websites(WEBSITES)
    results = process_results(scraped_data)
    save_to_pdf(results)
