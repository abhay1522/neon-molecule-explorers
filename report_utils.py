"""PDF report generation with ReportLab."""
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def build_pdf(title, college, rows, png_bytes=None, student=None, reg_no=None):
    """Return PDF bytes. rows = [(property, value), ...]."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    ss = getSampleStyleSheet()
    story = [Paragraph(title, ss["Title"]), Paragraph(college, ss["Heading3"]), Spacer(1, 8)]
    if student or reg_no:
        story.append(Paragraph(f"<b>Student:</b> {student or '-'} &nbsp;&nbsp; "
                               f"<b>Reg. No:</b> {reg_no or '-'}", ss["Normal"]))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now():%d-%m-%Y %H:%M}", ss["Normal"]))
    story.append(Spacer(1, 12))
    if png_bytes:
        story += [Image(io.BytesIO(png_bytes), width=9 * cm, height=6.3 * cm), Spacer(1, 12)]
    data = [["Property", "Value"]] + [[Paragraph(str(k), ss["Normal"]), Paragraph(str(v), ss["Normal"])]
                                      for k, v in rows]
    t = Table(data, colWidths=[6.5 * cm, 10.5 * cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b3d5c")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t)
    story += [Spacer(1, 16), Paragraph("Generated with the Cheminformatics Virtual Laboratory "
                                       "(Python, Streamlit and RDKit).", ss["Italic"])]
    doc.build(story)
    return buf.getvalue()
