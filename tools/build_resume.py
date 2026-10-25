"""
Build resume.pdf from the same content the site uses.

    python tools/build_resume.py

One source of truth: the resume is generated from content/, so if a job title
changes on the site it changes here too. A resume that disagrees with the site
it is linked from is worse than either one alone.

Built with reportlab Platypus (flowables, not canvas.drawString) so every
paragraph wraps to the frame and nothing can run off the page.
"""

from __future__ import annotations

import sys
import unicodedata
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from content import EDUCATION, EXPERIENCE, PROFILE, WORK_PROJECTS  # noqa: E402

OUT = ROOT / "resume.pdf"

INK = colors.HexColor("#14161C")
MUTED = colors.HexColor("#5A6172")
ACCENT = colors.HexColor("#2F3A56")
RULE = colors.HexColor("#C9CEDB")

# The 14 built-in PDF fonts cover Latin-1 only. Anything outside it renders as a
# black box, silently. So the text is folded to ASCII before it is written.
_ASCII_FOLD = {
    "\u2014": " - ",   # em dash
    "\u2013": "-",     # en dash
    "\u2019": "'",     # right single quote
    "\u2018": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u00b7": "-",
    "\u2192": "->",
    "\u00b0": " deg",
}


def plain(text) -> str:
    """Fold to ASCII so nothing can render as a missing glyph."""
    out = str(text)
    for source, target in _ASCII_FOLD.items():
        out = out.replace(source, target)
    out = unicodedata.normalize("NFKD", out)
    return out.encode("ascii", "ignore").decode("ascii")


styles = getSampleStyleSheet()

S_NAME = ParagraphStyle(
    "name", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=21, leading=23, textColor=INK, spaceAfter=2,
)
S_TITLE = ParagraphStyle(
    "title", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10.5, leading=13, textColor=ACCENT, spaceAfter=3,
)
S_CONTACT = ParagraphStyle(
    "contact", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.8, leading=11.5, textColor=MUTED, spaceAfter=0,
)
S_SUMMARY = ParagraphStyle(
    "summary", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.3, leading=12.6, textColor=INK, spaceAfter=0,
)
S_HEADING = ParagraphStyle(
    "heading", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=10, leading=12, textColor=ACCENT, spaceBefore=0, spaceAfter=0,
    keepWithNext=1,
)
S_ROLE = ParagraphStyle(
    "role", parent=styles["Normal"], fontName="Helvetica-Bold",
    fontSize=9.8, leading=12, textColor=INK, keepWithNext=1,
)
S_META = ParagraphStyle(
    "meta", parent=styles["Normal"], fontName="Helvetica",
    fontSize=8.6, leading=11, textColor=MUTED, keepWithNext=1,
)
S_BODY = ParagraphStyle(
    "body", parent=styles["Normal"], fontName="Helvetica",
    fontSize=9.1, leading=12.2, textColor=INK, alignment=TA_LEFT, spaceAfter=0,
)
S_BULLET = ParagraphStyle(
    "bullet", parent=S_BODY, fontSize=9.0, leading=11.8,
)
S_SKILL = ParagraphStyle(
    "skill", parent=S_BODY, fontSize=9.0, leading=12.0, spaceAfter=1.5,
)


def heading(text: str) -> list:
    return [
        Spacer(1, 9),
        Paragraph(plain(text).upper(), S_HEADING),
        HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=2.5, spaceAfter=5),
    ]


def bullets(items: list[str]) -> ListFlowable:
    return ListFlowable(
        [ListItem(Paragraph(plain(item), S_BULLET), leftIndent=12) for item in items],
        bulletType="bullet",
        bulletFontSize=6,
        bulletOffsetY=-1,
        leftIndent=12,
        spaceBefore=2,
        spaceAfter=2,
    )


def build_story() -> list:
    story: list = []

    # ---------------------------------------------------------------- header
    story.append(Paragraph(plain(PROFILE["name"]), S_NAME))
    story.append(
        Paragraph(
            plain("Dot Net Full Stack Developer / Senior Software Engineer"), S_TITLE
        )
    )
    contact = " &nbsp;|&nbsp; ".join(
        [
            plain(PROFILE["location"]),
            plain(PROFILE["email"]),
            plain("github.com/" + PROFILE["handle"]),
        ]
    )
    story.append(Paragraph(contact, S_CONTACT))
    story.append(HRFlowable(width="100%", thickness=1.1, color=ACCENT, spaceBefore=6, spaceAfter=2))

    # --------------------------------------------------------------- summary
    summary = (
        "Full-stack developer with 4+ years of hands-on experience building and "
        "delivering enterprise .NET and cloud applications. Depth across .NET 8, C#, "
        "ASP.NET Core and Web API, Microsoft Azure (Functions, App Services, SQL, Key "
        "Vault), and Angular front ends, with a recent focus on AI and GenAI "
        "integration. Contributes across development, release and production support "
        "in hybrid modern and legacy applications."
    )
    story.append(Spacer(1, 7))
    story.append(Paragraph(plain(summary), S_SUMMARY))

    # ---------------------------------------------------------------- skills
    story += heading("Technical skills")
    for group in SKILLS_FOR_RESUME:
        story.append(
            Paragraph(
                f'<font color="#2F3A56"><b>{plain(group["label"])}</b></font> '
                f'{plain(", ".join(group["items"]))}',
                S_SKILL,
            )
        )

    # ------------------------------------------------------------ experience
    story += heading("Work experience")
    for job in EXPERIENCE:
        block = [
            Paragraph(
                f'{plain(job["role"])} <font color="#5A6172">&middot;</font> '
                f'<font color="#2F3A56">{plain(job["company"])}</font>',
                S_ROLE,
            ),
            Paragraph(plain(f'{job["period"]}  |  {job["location"]}'), S_META),
            Spacer(1, 2.5),
            Paragraph(plain(job["summary"]), S_BODY),
            bullets(job["highlights"]),
            Paragraph(
                f'<font color="#5A6172">Stack:</font> {plain(", ".join(job["stack"]))}',
                S_META,
            ),
            Spacer(1, 8),
        ]
        # Keep the role header with at least its summary - never orphan the title.
        story.append(KeepTogether(block[:5]))
        story += block[5:]

    # -------------------------------------------------------------- projects
    story += heading("Selected projects")
    for project in WORK_PROJECTS:
        block = [
            Paragraph(
                f'{plain(project["name"])} <font color="#5A6172">&middot;</font> '
                f'<font color="#2F3A56">{plain(project["client"])}</font>',
                S_ROLE,
            ),
            Paragraph(
                plain(
                    f'{project["role"]}  |  {project["duration"]}  |  '
                    f'team of {project["team"]}'
                ),
                S_META,
            ),
            Spacer(1, 2.5),
            Paragraph(plain(project["summary"]), S_BODY),
            bullets(project["contributions"]),
            Spacer(1, 8),
        ]
        story.append(KeepTogether(block[:4]))
        story += block[4:]

    # ------------------------------------------------------------- education
    story += heading("Education")
    for item in EDUCATION:
        story.append(
            KeepTogether(
                [
                    Paragraph(
                        f'{plain(item["qualification"])} <font color="#5A6172">&middot;</font> '
                        f'<font color="#2F3A56">{plain(item["institution"])}</font>',
                        S_ROLE,
                    ),
                    Paragraph(
                        plain(f'{item["affiliation"]}  |  {item["period"]}'), S_META
                    ),
                    Spacer(1, 6),
                ]
            )
        )

    return story


# The resume groups skills slightly differently from the site: fewer groups,
# because a resume is read in ten seconds and eight categories is seven too many.
SKILLS_FOR_RESUME = [
    {
        "label": "Backend:",
        "items": [
            "ASP.NET Core", ".NET 8", ".NET Core", "C#", "Web API", "MVC",
            "ASP.NET Web Forms", "REST APIs", "SOLID",
        ],
    },
    {
        "label": "Frontend:",
        "items": [
            "Angular", "TypeScript", "JavaScript", "RxJS", "HTML5", "CSS3",
            "Bootstrap", "PrimeNG",
        ],
    },
    {
        "label": "Data:",
        "items": [
            "SQL Server", "Azure Cosmos DB", "Entity Framework Core",
            "Code First & Database First", "Stored Procedures", "Normalisation",
        ],
    },
    {
        "label": "Azure:",
        "items": [
            "App Services", "Functions (Blob, Queue, Service Bus, Cosmos, Timer)",
            "Logic Apps", "API Management", "Storage Accounts", "Key Vault",
            "App Configuration", "Service Bus",
        ],
    },
    {
        "label": "AI & GenAI:",
        "items": [
            "LLM integration", "Anthropic Claude via Cloudflare AI Gateway",
            "Prompt engineering", "Prompt layering",
            "Automated prompt training & validation", "RAG concepts",
            "Claude Code", "GitHub Copilot",
        ],
    },
    {
        "label": "Testing & observability:",
        "items": [
            "xUnit", "SonarQube", "Serilog", "Elastic Cloud (ELK)",
            "GitLab CI/CD", "code coverage",
        ],
    },
    {
        "label": "Tools:",
        "items": ["Git", "TFS", "Visual Studio", "VS Code"],
    },
]


def footer(canvas, doc) -> None:
    canvas.saveState()
    width, _height = doc.pagesize
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        doc.leftMargin, 12 * mm, plain(f'{PROFILE["name"]} - {PROFILE["email"]}')
    )
    canvas.drawRightString(width - doc.rightMargin, 12 * mm, f"Page {canvas.getPageNumber()}")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, 15 * mm, width - doc.rightMargin, 15 * mm)
    canvas.restoreState()


def main() -> int:
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=19 * mm,
        title=plain(f'{PROFILE["name"]} - Resume'),
        author=plain(PROFILE["name"]),
        subject="Resume",
    )

    doc.build(build_story(), onFirstPage=footer, onLaterPages=footer)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
