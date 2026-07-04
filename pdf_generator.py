from io import BytesIO
from models import User
import re
from html import unescape
from xml.sax.saxutils import escape
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def generate_pdf(result):
    user = User.query.get(result.user_id)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Title"]
    title.alignment = TA_CENTER

    elements = []

    # Title
    elements.append(Paragraph("AI Interview Report", title))
    elements.append(Spacer(1, 20))

    # Candidate Details
    elements.append(
    Paragraph(f"<b>Candidate:</b> {user.name}", styles["Normal"])
)

    elements.append(
    Paragraph(f"<b>Email:</b> {user.email}", styles["Normal"])
)
    elements.append(Paragraph(f"<b>Interview Type:</b> {result.interview_type}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Score:</b> {result.score}%", styles["Normal"]))
    elements.append(
        Paragraph(
            f"<b>Date:</b> {result.interview_date.strftime('%d-%m-%Y %I:%M %p')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("<b>AI Feedback</b>", styles["Heading2"]))
    feedback = re.sub(r"<[^>]+>", "\n", result.feedback)
    feedback = unescape(feedback)
    feedback = escape(feedback)
    feedback = feedback.replace("\n", "<br/>")
    elements.append(Paragraph(feedback, styles["BodyText"]))
    doc.build(elements)

    buffer.seek(0)

    return buffer