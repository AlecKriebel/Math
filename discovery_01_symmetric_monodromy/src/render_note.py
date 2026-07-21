#!/usr/bin/env python3
"""Render the research note as a polished PDF using ReportLab."""

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
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "full_symmetric_monodromy.pdf"
PUBLICATION_UTC = "21 July 2026, 13:11:39 UTC"
PUBLICATION_PDT = "21 July 2026, 06:11:39 PDT"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d6dbe3"))
    canvas.line(0.75 * inch, 0.56 * inch, 7.75 * inch, 0.56 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#667085"))
    canvas.drawString(0.75 * inch, 0.36 * inch, f"First public release: {PUBLICATION_UTC}")
    canvas.drawRightString(7.75 * inch, 0.36 * inch, str(doc.page))
    canvas.restoreState()


def build_styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=20,
            leading=23,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#172033"),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Times-Italic",
            fontSize=10,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#475467"),
            spaceAfter=18,
        ),
        "abstract_head": ParagraphStyle(
            "AbstractHead",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#344054"),
            spaceAfter=6,
        ),
        "abstract": ParagraphStyle(
            "Abstract",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=9.5,
            leading=13,
            leftIndent=0.45 * inch,
            rightIndent=0.45 * inch,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#273142"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#183153"),
            spaceBefore=11,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#344054"),
            spaceBefore=8,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10.25,
            leading=14.3,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=7,
        ),
        "theorem": ParagraphStyle(
            "Theorem",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10.25,
            leading=14.3,
            leftIndent=0.22 * inch,
            rightIndent=0.22 * inch,
            borderColor=colors.HexColor("#8aa4c8"),
            borderWidth=0.8,
            borderPadding=8,
            backColor=colors.HexColor("#f4f7fb"),
            spaceBefore=5,
            spaceAfter=10,
        ),
        "formula": ParagraphStyle(
            "Formula",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=10.2,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            leftIndent=0.15 * inch,
            rightIndent=0.15 * inch,
            spaceBefore=4,
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Times-Roman",
            fontSize=8.2,
            leading=10.2,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#475467"),
            spaceAfter=2,
        ),
    }


def p(text, style):
    return Paragraph(text, style)


def render():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    doc = BaseDocTemplate(
        str(OUT),
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.68 * inch,
        bottomMargin=0.72 * inch,
        title="Full symmetric monodromy in an Alpoge-Gallagher subfamily",
        author="Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol",
        subject="Provisional research note on explicit Keller maps",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="paper", frames=[frame], onPage=footer)])

    S = []
    S.append(p("Full symmetric monodromy in a uniform<br/>Alpoge-Gallagher subfamily", styles["title"]))
    S.append(p(
        "Provisional research note - 20 July 2026<br/>"
        "Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol<br/>"
        f"First public release: {PUBLICATION_UTC} ({PUBLICATION_PDT})",
        styles["subtitle"],
    ))
    S.append(p("ABSTRACT", styles["abstract_head"]))
    S.append(p(
        "Gallagher's weighted-lift construction, posted after Alpoge's announced "
        "counterexample, produces a three-dimensional Keller map of every generic "
        "degree <i>n</i> >= 3. We isolate a simple uniform subfamily and prove that "
        "its function-field extension has full symmetric Galois closure "
        "<i>S</i><sub>n</sub>, hence no nonidentity rational deck transformations. "
        "A uniform rational collision is also given. This is a structural "
        "refinement of the Alpoge-Gallagher examples, not an independent "
        "construction of the underlying counterexamples.",
        styles["abstract"],
    ))

    S.append(p("1. The explicit family", styles["h1"]))
    S.append(p(
        "Fix an integer <i>n</i> >= 3 and put",
        styles["body"],
    ))
    S.append(p(
        "<i>u</i> = 1 + <i>xy</i>, &nbsp;&nbsp; "
        "<i>gamma</i> = 1 - [<i>n</i>/(<i>n</i>-1)]<i>xy</i> + <i>x</i><super>2</super><i>z</i>.",
        styles["formula"],
    ))
    S.append(p(
        "Define <i>F</i><sub>n</sub> = (<i>A</i><sub>n</sub>, <i>B</i><sub>n</sub>, "
        "<i>C</i><sub>n</sub>) by",
        styles["body"],
    ))
    S.append(p(
        "<i>A</i><sub>n</sub> = {(<i>n</i>-2)<i>u</i> + <i>u</i><super>2</super> - "
        "(<i>n</i>-1)<i>u</i><super>n</super><i>gamma</i><super>n-2</super>} / "
        "{(<i>n</i>-2)<i>x</i><super>2</super>},",
        styles["formula"],
    ))
    S.append(p(
        "<i>B</i><sub>n</sub> = {(<i>n</i>-2) + 2<i>u</i> - "
        "<i>n u</i><super>n-1</super><i>gamma</i><super>n-2</super>} / "
        "{(<i>n</i>-2)<i>x</i>}, &nbsp;&nbsp; "
        "<i>C</i><sub>n</sub> = <i>x gamma</i>. &nbsp; (1)",
        styles["formula"],
    ))
    S.append(p(
        "The apparent quotients by <i>x</i><super>2</super> and <i>x</i> cancel "
        "identically, so (1) is a polynomial map over Q.",
        styles["body"],
    ))
    S.append(p(
        "<b>Theorem 1.</b> For every <i>n</i> >= 3, the map "
        "<i>F</i><sub>n</sub> is polynomial and det J<i>F</i><sub>n</sub> = 1; "
        "the extension C(<i>x,y,z</i>)/C(<i>F</i><sub>n</sub>) has degree <i>n</i> "
        "and Galois closure <i>S</i><sub>n</sub>; and every rational map "
        "<i>sigma</i> satisfying <i>F</i><sub>n</sub> o <i>sigma</i> = "
        "<i>F</i><sub>n</sub> is the identity.",
        styles["theorem"],
    ))

    S.append(p("2. Polynomiality and constant Jacobian", styles["h1"]))
    S.append(p(
        "Set <i>v</i> = <i>xy</i>, <i>tau</i> = <i>x</i><super>2</super><i>z</i>, "
        "and <i>w</i> = <i>u gamma</i>. Define",
        styles["body"],
    ))
    S.append(p(
        "<i>p</i><sub>n</sub>(<i>w</i>) = [2<i>w</i> - <i>n w</i><super>n-1</super>]/(<i>n</i>-2), &nbsp; "
        "<i>q</i><sub>n</sub>(<i>w</i>) = [<i>w</i><super>2</super> - (<i>n</i>-1)<i>w</i><super>n</super>]/(<i>n</i>-2).",
        styles["formula"],
    ))
    S.append(p(
        "Then <i>q</i><sub>n</sub>' = <i>w p</i><sub>n</sub>' and (1) is "
        "(<i>alpha</i>/<i>x</i><super>2</super>, <i>beta</i>/<i>x</i>, "
        "<i>x gamma</i>), where <i>alpha</i> = <i>u</i> + "
        "<i>q</i><sub>n</sub>(<i>w</i>)/<i>gamma</i><super>2</super> and "
        "<i>beta</i> = 1 + <i>p</i><sub>n</sub>(<i>w</i>)/<i>gamma</i>. "
        "As polynomials in (<i>v,tau</i>), beta lies in (<i>v,tau</i>) and "
        "alpha lies in (<i>v</i><super>2</super>,<i>tau</i>); substitution proves "
        "the required divisibility.",
        styles["body"],
    ))
    S.append(p(
        "Put <i>P</i> = <i>BC</i> = <i>gamma</i> + <i>p</i><sub>n</sub>(<i>w</i>) "
        "and <i>Q</i> = <i>AC</i><super>2</super> = <i>w gamma</i> + "
        "<i>q</i><sub>n</sub>(<i>w</i>). The output change "
        "(<i>A,B,C</i>) -> (<i>P,Q,C</i>) has Jacobian -<i>C</i><super>3</super>. "
        "The input changes through (<i>x,w,gamma</i>) and the identity "
        "<i>w p</i>' - <i>q</i>' - <i>gamma</i> = -<i>gamma</i> give the same "
        "Jacobian -<i>C</i><super>3</super>. Therefore det J<i>F</i><sub>n</sub> = 1.",
        styles["body"],
    ))

    S.append(p("3. Inverse equation and degree", styles["h1"]))
    S.append(p(
        "With <i>R</i><sub>n</sub>(<i>w</i>) = (<i>w</i><super>2</super> - "
        "<i>w</i><super>n</super>)/(<i>n</i>-2), the identity "
        "<i>q</i><sub>n</sub> = <i>w p</i><sub>n</sub> - <i>R</i><sub>n</sub> "
        "eliminates gamma and gives <i>R</i><sub>n</sub>(<i>w</i>) = <i>wP</i> - <i>Q</i>. "
        "Thus the fiber polynomial is",
        styles["body"],
    ))
    S.append(p(
        "<i>H</i><sub>n</sub>(<i>T</i>) = <i>T</i><super>n</super> - <i>T</i><super>2</super> "
        "+ (<i>n</i>-2)<i>BCT</i> - (<i>n</i>-2)<i>AC</i><super>2</super>. &nbsp; (2)",
        styles["formula"],
    ))
    S.append(p(
        "A root <i>w</i> with <i>gamma</i> = <i>P</i> - <i>p</i><sub>n</sub>(<i>w</i>) nonzero "
        "recovers the source rationally: <i>x</i> = <i>C/gamma</i>, "
        "<i>u</i> = <i>w/gamma</i>, <i>y</i> = (<i>u</i>-1)/<i>x</i>, and "
        "<i>z</i> = {<i>gamma</i>-1 + [<i>n</i>/(<i>n</i>-1)](<i>u</i>-1)}/<i>x</i><super>2</super>.",
        styles["body"],
    ))
    S.append(p(
        "Writing <i>U</i> = (<i>n</i>-2)<i>BC</i> and "
        "<i>V</i> = -(<i>n</i>-2)<i>AC</i><super>2</super>, the target field is "
        "K = C(<i>A,B,C</i>) = C(<i>U,V,C</i>) = C(<i>U,V</i>)(<i>C</i>), since "
        "<i>B</i> = <i>U</i>/((<i>n</i>-2)<i>C</i>) and "
        "<i>A</i> = -<i>V</i>/((<i>n</i>-2)<i>C</i><super>2</super>). "
        "Here <i>C</i> is transcendental over C(<i>U,V</i>). Equation (2) is "
        "<i>h</i><sub>n</sub>(<i>T</i>) = <i>T</i><super>n</super> - "
        "<i>T</i><super>2</super> + <i>UT</i> + <i>V</i>. It is irreducible over "
        "C(<i>U,V</i>): being linear in <i>V</i> with coefficient one, any "
        "factor independent of <i>V</i> would be a unit. Gauss's lemma preserves "
        "irreducibility under the purely transcendental base change to K. Hence "
        "the extension degree is <i>n</i>.",
        styles["body"],
    ))

    S.append(p("4. Full symmetric monodromy", styles["h1"]))
    S.append(p(
        "The discriminant curve of <i>h</i><sub>n</sub> is parametrized by",
        styles["body"],
    ))
    S.append(p(
        "<i>t</i> -> (<i>U,V</i>) = "
        "(2<i>t</i> - <i>n t</i><super>n-1</super>, "
        "(<i>n</i>-1)<i>t</i><super>n</super> - <i>t</i><super>2</super>). &nbsp; (3)",
        styles["formula"],
    ))
    S.append(p(
        "It is irreducible. At <i>t</i> = 0 the polynomial is "
        "<i>T</i><super>2</super>(<i>T</i><super>n-2</super>-1), with exactly one "
        "double root. It is the unique parameter over (<i>U,V</i>) = (0,0), and "
        "the derivative of (3) has first coordinate 2, so this is a smooth "
        "discriminant point. The one-double-root condition is nonempty "
        "and Zariski open on the irreducible curve, so generic inertia is a "
        "transposition. The root-incidence "
        "variety is A<super>2</super>, hence connected, so the monodromy action "
        "is transitive. Quotienting the Galois closure by the normal subgroup "
        "generated by finite inertia yields a cover of A<super>2</super> unramified "
        "in codimension one. Purity makes it finite etale, and A<super>2</super> "
        "has no nontrivial connected finite etale cover. Therefore the monodromy "
        "group is generated by conjugate transpositions. A transitive group "
        "generated by transpositions is <i>S</i><sub>n</sub>. Finally, a finite "
        "algebraic extension is linearly disjoint from the purely transcendental "
        "extension C(<i>U,V</i>)(<i>C</i>), so this remains the Galois group over "
        "the actual target field K.",
        styles["body"],
    ))
    S.append(p(
        "<b>Corollary.</b> The rational deck group is trivial. In the "
        "<i>S</i><sub>n</sub>-closure, the root field is fixed by a point "
        "stabilizer <i>S</i><sub>n-1</sub>, which is self-normalizing; hence "
        "Aut<sub>K</sub>(<i>L</i>) = N(<i>S</i><sub>n-1</sub>)/<i>S</i><sub>n-1</sub> = 1.",
        styles["theorem"],
    ))

    S.append(p("5. Uniform rational collision", styles["h1"]))
    S.append(p(
        "Let <i>s</i><sub>n</sub> = (4 - 2<super>n</super>)/(<i>n</i>-2). At the "
        "target (<i>s</i><sub>n</sub>,<i>s</i><sub>n</sub>,1), the fiber polynomial "
        "is <i>T</i><super>n</super> - <i>T</i><super>2</super> + "
        "(4-2<super>n</super>)(<i>T</i>-1), with simple roots 1 and 2. For "
        "<i>r</i> in {1,2}, set <i>g</i><sub>r</sub> = "
        "<i>s</i><sub>n</sub> - <i>p</i><sub>n</sub>(<i>r</i>) and",
        styles["body"],
    ))
    S.append(p(
        "<i>X</i><sub>n,r</sub> = (1/<i>g</i><sub>r</sub>, "
        "<i>r</i>-<i>g</i><sub>r</sub>, "
        "<i>g</i><sub>r</sub><super>2</super>[<i>g</i><sub>r</sub>-1 + "
        "<i>n</i>/(<i>n</i>-1)(<i>r</i>/<i>g</i><sub>r</sub>-1)]). &nbsp; (4)",
        styles["formula"],
    ))
    S.append(p(
        "Here <i>g</i><sub>1</sub> = (<i>n</i>+2-2<super>n</super>)/(<i>n</i>-2) "
        "and <i>g</i><sub>2</sub> = 2<super>n-1</super>, both nonzero. Exact "
        "substitution gives <i>F</i><sub>n</sub>(<i>X</i><sub>n,1</sub>) = "
        "<i>F</i><sub>n</sub>(<i>X</i><sub>n,2</sub>) = "
        "(<i>s</i><sub>n</sub>,<i>s</i><sub>n</sub>,1). For <i>n</i> = 3: "
        "<i>F</i><sub>3</sub>(-1/3,4,-54) = <i>F</i><sub>3</sub>(1/4,-2,36) "
        "= (-4,-4,1).",
        styles["body"],
    ))

    S.append(p("6. Status and reproducibility", styles["h1"]))
    S.append(p(
        "The every-degree lift and cubic <i>S</i><sub>3</sub> analysis predate this "
        "note. Its narrow residual claims are the subfamily (1), uniform collision, "
        "all-degree <i>S</i><sub>n</sub> theorem, and trivial deck group. Searches on "
        "20 July 2026 found no prior statement, but establish no priority. The exact "
        "checker accompanies the note; expert review is required before submission.",
        styles["body"],
    ))

    S.append(p("References", styles["h1"]))
    refs = [
        "[1] O.-H. Keller, <i>Ganze Cremona-Transformationen</i>, Monatsh. Math. Phys. 47 (1939), 299-306.",
        "[2] H. Bass, E. Connell, D. Wright, <i>The Jacobian conjecture: reduction of degree and formal expansion of the inverse</i>, Bull. Amer. Math. Soc. 7 (1982), 287-330.",
        "[3] L. Alpoge, announcement of an explicit counterexample, 19 July 2026.",
        "[4] A. Gallagher, <i>An infinite family of counterexamples to the Jacobian Conjecture in dimension three: every generic fiber degree n >= 3 occurs</i>, 20 July 2026.",
        "[5] MathOverflow 513387, <i>Galois structure of the new counterexample to the Jacobian conjecture</i>, 20 July 2026.",
    ]
    for ref in refs:
        S.append(p(ref, styles["small"]))

    S.append(Spacer(1, 2))
    S.append(p(
        "Disclosure: Alec Kriebel is a complete amateur and cannot independently "
        "verify the mathematical claims in this note. The formulas, proof "
        "organization, verifier, and typeset draft were developed with heavy "
        "assistance from ChatGPT 5.6 Sol. Independent expert review is required.",
        styles["small"],
    ))

    doc.build(S)
    print(OUT)


if __name__ == "__main__":
    render()
