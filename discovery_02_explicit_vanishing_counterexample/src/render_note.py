#!/usr/bin/env python3
"""Render the provisional research note as a polished PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "explicit_vanishing_counterexample.pdf"
PUBLICATION_UTC = "21 July 2026, 13:11:39 UTC"
PUBLICATION_PDT = "21 July 2026, 06:11:39 PDT"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d6dbe3"))
    canvas.line(0.68 * inch, 0.55 * inch, 7.82 * inch, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#667085"))
    canvas.drawString(0.68 * inch, 0.35 * inch, f"First public release: {PUBLICATION_UTC}")
    canvas.drawRightString(7.82 * inch, 0.35 * inch, str(doc.page))
    canvas.restoreState()


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title", parent=base["Title"], fontName="Times-Bold", fontSize=20,
            leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#172033"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle", parent=base["Normal"], fontName="Times-Italic",
            fontSize=9.5, leading=13, alignment=TA_CENTER,
            textColor=colors.HexColor("#475467"), spaceAfter=16,
        ),
        "abstract_head": ParagraphStyle(
            "AbstractHead", parent=base["Heading2"], fontName="Helvetica-Bold",
            fontSize=9.5, leading=11, alignment=TA_CENTER,
            textColor=colors.HexColor("#344054"), spaceAfter=5,
        ),
        "abstract": ParagraphStyle(
            "Abstract", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.2, leading=12.6, leftIndent=0.4 * inch,
            rightIndent=0.4 * inch, alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#273142"), spaceAfter=15,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontName="Helvetica-Bold",
            fontSize=12, leading=14, textColor=colors.HexColor("#183153"),
            spaceBefore=7, spaceAfter=5, keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.45, leading=12.8, alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1f2937"), spaceAfter=5,
        ),
        "theorem": ParagraphStyle(
            "Theorem", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.45, leading=12.9, leftIndent=0.18 * inch,
            rightIndent=0.18 * inch, borderColor=colors.HexColor("#7e9bc3"),
            borderWidth=0.8, borderPadding=7, backColor=colors.HexColor("#f3f7fc"),
            spaceBefore=5, spaceAfter=8,
        ),
        "formula": ParagraphStyle(
            "Formula", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=9.5, leading=13.7, alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"), leftIndent=0.1 * inch,
            rightIndent=0.1 * inch, spaceBefore=3, spaceAfter=6,
        ),
        "small": ParagraphStyle(
            "Small", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=7.2, leading=8.6, alignment=TA_LEFT,
            textColor=colors.HexColor("#344054"),
        ),
        "table_head": ParagraphStyle(
            "TableHead", parent=base["BodyText"], fontName="Helvetica-Bold",
            fontSize=7.4, leading=9, alignment=TA_LEFT,
            textColor=colors.white,
        ),
        "table": ParagraphStyle(
            "Table", parent=base["BodyText"], fontName="Times-Roman",
            fontSize=7.25, leading=9, alignment=TA_LEFT,
            textColor=colors.HexColor("#1f2937"),
        ),
    }


def para(text, style):
    return Paragraph(text, style)


def formula(text, S):
    return para(text, S["formula"])


def render():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    S = styles()
    doc = BaseDocTemplate(
        str(OUT), pagesize=LETTER, leftMargin=0.68 * inch, rightMargin=0.68 * inch,
        topMargin=0.62 * inch, bottomMargin=0.64 * inch,
        title="An explicit quartic counterexample to Zhao's Vanishing Conjecture",
        author="Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol",
        subject="Explicit Hessian-nilpotent quartic derived from the 3D Jacobian counterexample",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="paper", frames=[frame], onPage=footer)])

    story = []
    story.append(para("An explicit quartic counterexample to<br/>Zhao's Vanishing Conjecture", S["title"]))
    story.append(para(
        "Provisional research note - 20 July 2026<br/>"
        "Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol<br/>"
        f"First public release: {PUBLICATION_UTC} ({PUBLICATION_PDT})",
        S["subtitle"],
    ))
    story.append(para("ABSTRACT", S["abstract_head"]))
    story.append(para(
        "Starting from the newly announced three-dimensional counterexample to the "
        "Jacobian conjecture, we explicitly carry out the Bass-Connell-Wright degree "
        "reduction and the de Bondt-van den Essen symmetric reduction. Factor reuse "
        "gives a cubic homogeneous Keller map in 27 variables. Symmetrization gives "
        "a homogeneous quartic Hessian-nilpotent polynomial in 54 variables, with "
        "598 monomials, whose gradient Keller map is noninjective. Therefore Zhao's "
        "Vanishing Conjecture fails for this specific polynomial. The expanded "
        "polynomial and a two-point collision are supplied as exact certificates.",
        S["abstract"],
    ))

    story.append(para("1. Main result", S["h1"]))
    story.append(para(
        "Let <i>h</i>: C<super>27</super> -> C<super>27</super> be the cubic "
        "homogeneous map constructed below. For <i>A,B</i> in C<super>27</super>, set",
        S["body"],
    ))
    story.append(formula(
        "<b>P</b>(<i>A,B</i>) = <i>i</i> sum<sub>j=1</sub><super>27</super> "
        "<i>h</i><sub>j</sub>(<i>A</i>+<i>iB</i>)<i>B</i><sub>j</sub>. &nbsp; (1)", S
    ))
    story.append(para(
        "<b>Theorem 1.</b> The polynomial <b>P</b> is homogeneous of degree four, "
        "has 598 monomials over Q(<i>i</i>), and has nilpotent Hessian. The map "
        "Gamma(<i>Z</i>)=<i>Z</i>-grad <b>P</b>(<i>Z</i>) has Jacobian determinant "
        "one and is noninjective. Consequently Delta<super>m</super>"
        "<b>P</b><super>m+1</super> is nonzero for infinitely many <i>m</i>.",
        S["theorem"],
    ))
    story.append(para(
        "The construction, ordinary differentiation, and the listed collision form "
        "a finite exact certificate. The accompanying JSON file is the fully expanded "
        "polynomial, not merely a symbolic reference to the construction.", S["body"]
    ))

    story.append(para("2. Normalization and stable degree reduction", S["h1"]))
    story.append(para(
        "Put <i>u</i>=1+<i>xy</i>. Postcomposing the announced map by the inverse "
        "of its linear part gives the identity-linear Keller map Phi:", S["body"]
    ))
    story.append(formula(
        "Phi<sub>1</sub>=<i>x</i>-(3/2)<i>x</i><super>2</super><i>y</i>"
        "-(1/2)<i>x</i><super>3</super><i>z</i>,<br/>"
        "Phi<sub>2</sub>=<i>y</i>+3<i>xu</i><super>2</super><i>z</i>"
        "+3<i>xy</i><super>2</super>(4+3<i>xy</i>),<br/>"
        "Phi<sub>3</sub>=<i>u</i><super>3</super><i>z</i>"
        "+<i>y</i><super>2</super><i>u</i>(4+3<i>xy</i>). &nbsp; (2)", S
    ))
    story.append(para(
        "It has determinant one and sends (0,0,-1/4), (1,-3/2,13/2), and "
        "(-1,3/2,13/2) to (0,0,-1/4). To cancel a term <i>cPQ</i> in coordinate "
        "<i>k</i>, add variables <i>a,b</i> and replace",
        S["body"],
    ))
    story.append(formula(
        "<i>M</i><sub>k</sub> -> <i>M</i><sub>k</sub>"
        "-<i>c</i>(<i>a+P</i>)(<i>b+Q</i>), &nbsp; "
        "(<i>a,b</i>) -> (<i>a+P,b+Q</i>). &nbsp; (3)", S
    ))
    story.append(para(
        "This is a pre- and post-composition by triangular automorphisms. Existing "
        "output factors may be reused with a one-variable version of (3). Apply the "
        "following six operations in order:", S["body"]
    ))

    rows = [
        ["step", "target", "new or reused factors", "c"],
        ["1", "Phi1", "P=x^2; Q=xz+3y; add a1,b1", "-1/2"],
        ["2", "Phi2", "P=3x^2y; Q=2z+xyz+3y^2; add a2,b2", "1"],
        ["3", "Phi2", "P=xy; Q=a2z+3xb2; add a3,b3", "-1"],
        ["4", "Phi3", "P=xy^2; Q=7y+3xz+3xy^2+x^2yz; add a4,b4", "1"],
        ["5", "Phi3", "add a5+a4xy; reuse output b1+xz+3y", "-1"],
        ["6", "Phi3", "reuse output a3+xy; add b6+a4b1-yb4", "1"],
    ]
    table_data = []
    for row_index, row in enumerate(rows):
        style = S["table_head"] if row_index == 0 else S["table"]
        table_data.append([para(cell, style) for cell in row])
    table = Table(table_data, colWidths=[0.38*inch, 0.55*inch, 5.45*inch, 0.38*inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#31557f")),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#aeb9c8")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#f6f8fb")]),
        ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3), ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    story.append(table)
    story.append(Spacer(1, 6))
    story.append(para(
        "Finally shear the <i>b</i><sub>4</sub> output by "
        "<i>M</i><sub>b4</sub> -> <i>M</i><sub>b4</sub>"
        "-<i>M</i><sub>a3</sub><i>M</i><sub>b1</sub>. The result has 13 variables "
        "<i>X</i>=(<i>x,y,z,a</i><sub>1</sub>,<i>b</i><sub>1</sub>,...,"
        "<i>a</i><sub>5</sub>,<i>b</i><sub>6</sub>) and degree three.", S["body"]
    ))

    story.append(PageBreak())
    story.append(para("3. The 13-variable collision", S["h1"]))
    story.append(para(
        "The linear part <i>L</i> is the identity except that the "
        "<i>b</i><sub>1</sub>, <i>b</i><sub>2</sub>, and <i>b</i><sub>4</sub> "
        "outputs have additional linear terms 3<i>y</i>, 2<i>z</i>, and 7<i>y</i>. "
        "Thus det <i>L</i>=1. Write",
        S["body"],
    ))
    story.append(formula(
        "Psi=<i>L</i><super>-1</super><i>M</i>="
        "<i>X</i>+<i>H</i><sub>2</sub>(<i>X</i>)"
        "+<i>H</i><sub>3</sub>(<i>X</i>). &nbsp; (4)", S
    ))
    story.append(para(
        "Then det J Psi=1. The lifted collision is",
        S["body"],
    ))
    story.append(formula(
        "<i>p</i><sub>0</sub>=(0,0,-1/4,0,0,0,1/2,0,0,0,0,0,0),<br/>"
        "<i>p</i><sub>1</sub>=(1,-3/2,13/2,-1,-2,9/2,-10,3/2,3/4,-9/4,-6,-27/8,9/2),<br/>"
        "Psi(<i>p</i><sub>0</sub>)=Psi(<i>p</i><sub>1</sub>)="
        "(0,0,-1/4,0,0,0,1/2,0,0,0,0,0,0). &nbsp; (5)", S
    ))
    story.append(para(
        "Equations (2)-(4) are a straight-line specification of every component of "
        "Psi; the verification script expands them and checks (5) exactly.", S["body"]
    ))

    story.append(para("4. A cubic homogeneous map in 27 variables", S["h1"]))
    story.append(para(
        "For <i>X,Y</i> in C<super>13</super> and <i>t</i> in C, define",
        S["body"],
    ))
    story.append(formula(
        "<i>h</i>(<i>X,Y,t</i>)="
        "(<i>tH</i><sub>2</sub>(<i>X</i>)+<i>t</i><super>2</super><i>Y</i>, "
        "-<i>H</i><sub>3</sub>(<i>X</i>), 0). &nbsp; (6)", S
    ))
    story.append(para(
        "All components are cubic homogeneous. If <i>B</i>(<i>W</i>)="
        "<i>W+h</i>(<i>W</i>) and <i>r</i><sub>j</sub>="
        "(<i>p</i><sub>j</sub>,<i>H</i><sub>3</sub>(<i>p</i><sub>j</sub>),1), "
        "then <i>B</i>(<i>r</i><sub>0</sub>)="
        "<i>B</i>(<i>r</i><sub>1</sub>)=(<i>p</i><sub>0</sub>,0,1).",
        S["body"],
    ))
    story.append(para(
        "<b>Lemma 2.</b> The polynomial matrix J<i>h</i> is nilpotent.<br/>"
        "<i>Proof.</i> Homogeneity and det J Psi=1 give "
        "det(<i>I+t</i>J<i>H</i><sub>2</sub>+<i>t</i><super>2</super>"
        "J<i>H</i><sub>3</sub>)=det J Psi(<i>tX</i>)=1. The block determinant "
        "of <i>W</i> -> <i>W+h</i>(<i>W</i>) is the same expression. Hence "
        "det(<i>I</i>+J<i>h</i>)=1. Since J<i>h</i>(<i>sW</i>)="
        "<i>s</i><super>2</super>J<i>h</i>(<i>W</i>), its characteristic "
        "polynomial is a pure power, proving nilpotence.", S["theorem"]
    ))

    story.append(para("5. Symmetrization and a finite collision certificate", S["h1"]))
    story.append(para(
        "De Bondt and van den Essen associate "
        "<i>f</i><sub>h</sub>(<i>A,B</i>)=-<i>i</i> sum "
        "<i>h</i><sub>j</sub>(<i>A+iB</i>)<i>B</i><sub>j</sub> to any map "
        "<i>h</i>. Their characteristic-polynomial identity says Hess "
        "<i>f</i><sub>h</sub> is nilpotent exactly when J<i>h</i> is nilpotent. "
        "Since <b>P</b>=-<i>f</i><sub>h</sub>, Lemma 2 proves the Hessian claim.",
        S["body"],
    ))
    story.append(para(
        "Let <i>S</i>(<i>x,y</i>)=(<i>x-iy,y</i>). Direct differentiation gives",
        S["body"],
    ))
    story.append(formula(
        "<i>S</i><super>-1</super> Gamma <i>S</i>(<i>x,y</i>) = "
        "(<i>x+h</i>(<i>x</i>), "
        "(<i>I</i>+J<i>h</i>(<i>x</i>)<super>T</super>)<i>y</i>"
        "-<i>ih</i>(<i>x</i>)). &nbsp; (7)", S
    ))
    story.append(para(
        "For <i>K</i><sub>j</sub>=<i>I</i>+J<i>h</i>(<i>r</i><sub>j</sub>)"
        "<super>T</super>, take <i>y</i><sub>1</sub>=0 and "
        "<i>y</i><sub>0</sub>=<i>K</i><sub>0</sub><super>-1</super>"
        "(-<i>ih</i>(<i>r</i><sub>1</sub>)+<i>ih</i>(<i>r</i><sub>0</sub>)). "
        "Then the two distinct points <i>S</i>(<i>r</i><sub>j</sub>,"
        "<i>y</i><sub>j</sub>) collide under Gamma. Their 54 coordinates, of "
        "height at most 261, are in collision.json. The verifier differentiates "
        "the 598-term expansion and checks this equality over Q(<i>i</i>), with no "
        "floating-point arithmetic.", S["body"],
    ))

    story.append(para("6. Failure of the Vanishing Conjecture", S["h1"]))
    story.append(para(
        "Zhao's inversion formula for a Hessian-nilpotent polynomial <i>P</i> "
        "writes the inverse of <i>Z</i>-<i>t</i> grad <i>P</i> as "
        "<i>Z</i>+<i>t</i> grad <i>Q</i><sub>t</sub>, where",
        S["body"],
    ))
    story.append(formula(
        "<i>Q</i><sub>t</sub> = sum<sub>m>=0</sub> "
        "[<i>t</i><super>m</super> / (2<super>m</super><i>m!</i>(<i>m</i>+1)!)] "
        "Delta<super>m</super><i>P</i><super>m+1</super>. &nbsp; (8)", S
    ))
    story.append(para(
        "If the terms in (8) vanished eventually for <b>P</b>, then "
        "<i>Q</i><sub>t</sub> would be polynomial. At <i>t</i>=1 this would give a "
        "polynomial inverse of Gamma, contradicting the explicit collision. Thus "
        "Delta<super>m</super><b>P</b><super>m+1</super> is nonzero infinitely often.",
        S["body"],
    ))

    story.append(para("7. Scope and references", S["h1"]))
    story.append(para(
        "Zhang's consequence note of 20 July 2026 observes existentially that the "
        "new three-dimensional counterexample makes the Vanishing Conjecture false "
        "in some dimension. The contribution here is the explicit quartic, its "
        "finite collision certificate, and a factor-reusing reduction that holds the "
        "dimension to 54. Priority and the absence of a smaller simultaneous "
        "construction must be rechecked immediately before posting.", S["body"],
    ))
    refs = [
        "[1] H. Bass, E. H. Connell, D. Wright, Bull. Amer. Math. Soc. 7 (1982), 287-330. DOI 10.1090/S0273-0979-1982-15032-7.",
        "[2] M. de Bondt, A. van den Essen, Proc. Amer. Math. Soc. 133 (2005), 2201-2205. DOI 10.1090/S0002-9939-05-07570-2.",
        "[3] W. Zhao, Trans. Amer. Math. Soc. 359 (2007), 249-274. arXiv:math/0409534.",
        "[4] Z. Zhang, Direct Consequences of the Three-Dimensional Counterexample to the Jacobian Conjecture, 20 July 2026.",
    ]
    for ref in refs:
        story.append(para(ref, S["small"]))

    story.append(Spacer(1, 5))
    story.append(para(
        "Disclosure: Alec Kriebel is a complete amateur and cannot independently "
        "verify the mathematical claims in this note. The construction, proof "
        "organization, verifiers, and typeset draft were developed with heavy "
        "assistance from ChatGPT 5.6 Sol. Independent expert review is required.",
        S["small"],
    ))

    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    render()
