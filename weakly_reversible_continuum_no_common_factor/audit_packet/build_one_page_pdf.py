#!/usr/bin/env python3
"""Build the one-page specialist audit handout with ReportLab."""

from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    FrameBreak,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "specialist_audit_one_page.pdf"

NAVY = colors.HexColor("#17324D")
BLUE = colors.HexColor("#1D6A96")
PALE = colors.HexColor("#EAF3F8")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#4D5B68")
RULE = colors.HexColor("#AFC5D3")


def draw_page(canvas, document):
    width, height = LETTER
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 0.72*inch, width, 0.72*inch, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 15.2)
    canvas.drawString(0.42*inch, height - 0.35*inch,
                      "Reversible equilibrium continua without a common factor")
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(0.42*inch, height - 0.56*inch,
                      "Version 2 specialist audit statement | exact three-species construction and rate family")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(0.42*inch, 0.31*inch, width - 0.42*inch, 0.31*inch)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 6.4)
    canvas.drawString(0.42*inch, 0.17*inch,
                      "Repository concept DOI (not paper-specific): 10.5281/zenodo.21753404 | v2 DOI: 10.5281/zenodo.21753997")
    canvas.drawRightString(width - 0.42*inch, 0.17*inch, "Audit handout - 1 page")
    canvas.restoreState()


def styles():
    return {
        "h": ParagraphStyle(
            "Heading", fontName="Helvetica-Bold", fontSize=10.3,
            leading=11.5, textColor=BLUE, spaceBefore=4.2, spaceAfter=2.8,
        ),
        "b": ParagraphStyle(
            "Body", fontName="Helvetica", fontSize=8.15, leading=9.75,
            textColor=INK, alignment=TA_LEFT, spaceAfter=3.4,
        ),
        "small": ParagraphStyle(
            "Small", fontName="Helvetica", fontSize=7.35, leading=8.65,
            textColor=INK, spaceAfter=2.5,
        ),
        "mono": ParagraphStyle(
            "Mono", fontName="Courier", fontSize=6.15, leading=7.5,
            textColor=INK,
        ),
    }


def heading(text, st):
    return Paragraph(text, st["h"])


def body(text, st, style="b"):
    return Paragraph(text, st[style])


def build():
    width, height = LETTER
    margin = 0.42*inch
    gutter = 0.19*inch
    frame_y = 0.36*inch
    frame_h = height - 1.13*inch
    frame_w = (width - 2*margin - gutter)/2
    frames = [
        Frame(margin, frame_y, frame_w, frame_h, leftPadding=0, rightPadding=2,
              topPadding=0, bottomPadding=0, id="left"),
        Frame(margin + frame_w + gutter, frame_y, frame_w, frame_h,
              leftPadding=2, rightPadding=0, topPadding=0, bottomPadding=0,
              id="right"),
    ]
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=LETTER, leftMargin=margin, rightMargin=margin,
        topMargin=0.78*inch, bottomMargin=0.34*inch,
        title="Version 2 specialist audit statement",
        author="Independent research project",
        subject="Reversible mass-action equilibrium continuum without a common factor",
    )
    doc.addPageTemplates([PageTemplate(id="two-column", frames=frames, onPage=draw_page)])
    st = styles()
    story = []

    story += [heading("Problem / answer", st)]
    story += [body(
        "<b>Problem.</b> Can a finite weakly reversible mass-action system have a "
        "positive-dimensional continuum of positive equilibria in one compatibility "
        "class while gcd(F1,F2,F3)=1? <b>Answer: yes.</b> The explicit system below "
        "is reversible, has one linkage class, three species, ten complexes, ten "
        "reversible pairs, positive integer rates, and S=R^3. Its unique positive "
        "class is the positive orthant.", st)]

    story += [heading("Main explicit theorem", st)]
    story += [body(
        "Complexes: 0, Z, 3Z, Y+Z, 3Y, X+Z, X+Y, X+Y+Z, 2X+Y, 3X. "
        "Reversible edges: 01, 04, 06, 17, 24, 27, 29, 34, 59, 89. "
        "Directed order is forward then reverse in that edge order.", st)]
    rate_data = [[Paragraph(
        "1160, 10296, 976, 23, 560, 5977, 1800, 25, 1629, 1237,<br/>"
        "1, 9152, 653, 1214, 5368, 1, 5368, 70, 6039, 915", st["mono"])] ]
    rate_table = Table(rate_data, colWidths=[frame_w-5])
    rate_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.45, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [rate_table, Spacer(1, 2)]
    story += [body(
        "The equilibrium ellipse is L=z-x-y+1=0 and "
        "Q=7x^2-2xy-16x+7y^2-16y+16=0. It is compact and entirely positive. "
        "A rational parametrization is x=(t^2+3)/(2D), y=(3t^2+1)/(2D), "
        "z=(t^2+t+1)/D, with D=t^2-t+1.", st)]
    story += [body(
        "The reconstructed field is:<br/>"
        "F1=-4697x^3+6039x^2y-9177xyz-5977xy+10736xz+1960z^3+1800z+560;<br/>"
        "F2=915x^3-6039x^2y-9177xyz-5977xy-3782y^3+10736yz+4888z^3+1800z+3488;<br/>"
        "F3=3712x^3+18304xyz-5368xz+3712y^3-5368yz-6848z^3-10296z+1160.",
        st, "small")]
    story += [body(
        "Exactly: Fi belongs to (L,Q), gcd(F1,F2,F3)=1 over Q, R, and C, and "
        "the steady ideal is radical. Its components are the conic prime and a "
        "disjoint degree-15 maximal ideal (15 reduced isolated points over an "
        "algebraic closure).", st)]

    story += [FrameBreak()]
    story += [heading("Complete fixed-support family theorem", st)]
    story += [body(
        "On the same 20 directed edges, all conic-preserving rate vectors form a "
        "four-dimensional rational linear space. Free coordinates are "
        "(a,b,c,d)=(k29,k43,k95,k98). The other 16 rates are explicit rational "
        "linear forms certified by a canonical 21x20 remainder matrix of rank 16. "
        "All 20 rates are positive exactly when a,b,c,d&gt;0, b&lt;c, and "
        "192a+221c&lt;154d.", st)]
    story += [body(
        "A nonempty Zariski-open subset of this positive family is geometrically "
        "coprime. The displayed system is (a,b,c,d)=(653,1,70,915). Under primitive "
        "positive-integral normalization and within this fixed support/family, it "
        "simultaneously minimizes the maximum rate (10296) and rate sum (52464). "
        "No global support-minimality claim is made.", st)]

    story += [heading("Reaction table and exact replay", st)]
    story += [body(
        "Complete table: manuscript_v2_draft/rates.csv. Human-readable table: "
        "MANUSCRIPT_V2.md, Appendix A. Family formulas and rank certificate: "
        "family/README.md and family/remainder_matrix.csv.", st)]
    command = Table([[Paragraph(
        ".venv/bin/python weakly_reversible_continuum_no_common_factor/<br/>"
        "manuscript_v2_draft/verify_v2_claims.py", st["mono"])]],
        colWidths=[frame_w-5])
    command.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F7F8")),
        ("BOX", (0, 0), (-1, -1), 0.45, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [command, Spacer(1, 2)]

    story += [heading("Likely failure points already tested", st)]
    items = [
        "edge/rate ordering, reverse edges, graph connectivity, and linkage count;",
        "positive rates, exact rank three, and the full-orthant compatibility class;",
        "conic primeness, compact positivity, parametrization, and exact vanishing;",
        "affine and homogenized gcd, including scalar extension to R and C;",
        "family exhaustivity, positivity sufficiency, and origin/degree-drop cases;",
        "radical decomposition, residual separability, and disjointness;",
        "bounded integer optimum without floating point; and",
        "strict separation of frozen-rate stability claims from the clean system.",
    ]
    story += [body("<br/>".join("- " + item for item in items), st, "small")]

    story += [heading("Metadata and scope", st)]
    story += [body(
        "Repository-wide Zenodo concept DOI: <b>10.5281/zenodo.21753404</b>. It "
        "groups unrelated releases from the AlecKriebel/Math monorepo and is not "
        "a paper-specific all-versions DOI. Cite this paper using its Version 2 "
        "version-specific DOI: <b>10.5281/zenodo.21753997</b>. This packet does not "
        "publish, deposit, or contact anyone. A DOI is not a correctness certificate.", st)]
    story += [body(
        "Not claimed: global minimality in complexes/reactions/deficiency; "
        "persistence outside the four-dimensional family; or universal priority. "
        "See audit_packet/AUDIT_CHECKLIST.md for the adversarial test map.", st)]

    doc.build(story)
    reader = PdfReader(str(OUTPUT))
    if len(reader.pages) != 1:
        raise RuntimeError(f"expected one page, built {len(reader.pages)}")
    print(f"built {OUTPUT}")


if __name__ == "__main__":
    build()
