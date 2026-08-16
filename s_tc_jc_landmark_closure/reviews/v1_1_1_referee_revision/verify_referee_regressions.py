#!/usr/bin/env python3
"""Fail-closed regressions for the v1.1.1 referee-hardening revision."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import re

from pypdf import PdfReader


PROJECT = Path(__file__).resolve().parents[2]
PAPER = PROJECT / "source/paper/main.tex"
SUPPLEMENT = PROJECT / "source/supplement/supplement.tex"
FIGURE = PROJECT / "source/paper/figures/core_atlas.tex"
TITLE = (
    "Strong Tree-Childness Is a Sharp Generic-Identifiability Boundary for "
    "Level-2 Jukes-Cantor Networks"
)
PDF_TITLE = TITLE.replace("Jukes-Cantor", "Jukes–Cantor")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strip_tex_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def check_paper(text: str) -> None:
    text = strip_tex_comments(text)
    compact = " ".join(text.split())
    required = (
        r"P_v(0,\ldots,0)=1",
        "componentwise normalized tensor locus",
        "both normalized subtree contractions have all-zero",
        r"\{Y_\tau\}_{\tau\in\mathcal T}",
        "some $Y_\\tau$ contains a nonempty relatively open",
        "one intersection with $U$ has dimension $d$",
        r"\phi_{\rm selected}\circ\delta_R",
        r"T_{\phi_{\rm full}(\theta)}M_{\rm full}",
        "preimage of the smooth locus of the irreducible full-model",
        "certificate assigns every canonical decorated directed relation",
        "connected positive physical context-parameter chart",
        "associated incidence normalizations have no holonomy",
        r"Z_N(N')=",
        "orbit rows $(A,B,C,D,E,F)$ and columns",
        r"projection to $(A,\ldots,H)$ is a local coordinate system",
    )
    for needle in required:
        require(needle in compact, f"paper regression phrase missing: {needle}")
    prohibited = (
        r"\circ d_R",
        "positive tensor--context chart",
        "Bridge choices are independent because",
        "universe, exactly one of the following holds",
        "one member has dimension $d$",
        "Sharp Identifiability Boundary",
    )
    for needle in prohibited:
        require(needle not in compact, f"withdrawn wording returned: {needle}")
    require(text.index(r"\emph{complete factor}") <
            text.index(r"\begin{proposition}[Primitive-core theorem]"),
            "complete factor is defined after its first technical use")


def check_figure(text: str) -> None:
    clearances = []
    positions = []
    for scope in re.split(r"\\begin\{scope\}(?:\[[^]]*\])?", text)[1:]:
        label = re.search(
            r"\\node at \(0,(-?[0-9.]+)\) \{\$\\theta_[0-3]\$\};", scope
        )
        if label is None:
            continue
        label_y = float(label.group(1))
        graph_y = [float(value) for value in re.findall(
            r"\\node(?:\[[^]]*\])? \([^)]+\) at \([^,]+,(-?[0-9.]+)\)", scope
        )]
        require(graph_y, "theta scope has no graph nodes")
        positions.append(label_y)
        clearances.append(min(graph_y) - label_y)
    require(len(positions) == 4, "did not find all four theta-label positions")
    require(all(value <= -2.25 for value in positions),
            "theta labels are too close to the graph nodes")
    require(all(value >= 0.75 for value in clearances),
            "a theta graph node intrudes into its label clearance")


def check_scalar_regression() -> None:
    """The old unnormalized ambient locus has a scalar not in the action."""
    c = Fraction(3, 2)
    p_u0 = p_v0 = Fraction(1)
    q_u0, q_v0 = c * p_u0, p_v0 / c
    require(q_u0 * q_v0 == p_u0 * p_v0,
            "constant scalar should preserve the contracted all-zero entry")
    require((q_u0, q_v0) != (Fraction(1), Fraction(1)),
            "counterexample scalar unexpectedly preserves normalization")
    # Every incidence multiplier is raised to 1[h != 0], so at h=0 it is 1.
    incidence_exponent_at_zero = 0
    a = Fraction(7, 5)
    require(a ** incidence_exponent_at_zero == 1,
            "incidence action should preserve component all-zero coordinates")


def check_title_sync() -> None:
    final = json.loads((PROJECT / "FINAL_OUTCOME.json").read_text())
    metadata = json.loads((PROJECT / "RELEASE_METADATA.json").read_text())
    require(final["title"] == metadata["title"] == TITLE,
            "machine-readable titles disagree")
    require(final["release_revision"] == metadata["release_revision"] ==
            "stc-jc-sharp-boundary-v1.1.1", "release revision disagrees")
    biorxiv = (PROJECT / "biorxiv_submission/BIORXIV_METADATA.md").read_text()
    require(PDF_TITLE in biorxiv, "bioRxiv title is stale")
    main_pdf = PdfReader(
        PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf"
    )
    supplement_pdf = PdfReader(
        PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf"
    )
    require(main_pdf.metadata.title == PDF_TITLE, "main PDF title is stale")
    require(supplement_pdf.metadata.title == f"Supplement to {PDF_TITLE}",
            "supplement PDF title is stale")


def mutation_tests(paper: str, figure: str) -> None:
    mutations = {
        "remove-normalization": paper.replace(r"P_v(0,\ldots,0)=1", "1=1", 1),
        "remove-finite-cover-selection": paper.replace(
            "some $Y_\\tau$ contains a nonempty relatively open", "some target exists", 1
        ),
        "restore-cover-dimension-overclaim": paper.replace(
            "one intersection with $U$ has dimension $d$",
            "one member has dimension $d$", 1
        ),
        "restore-descriptor-collision": paper.replace(
            r"\phi_{\rm selected}\circ\delta_R",
            r"\phi_{\rm selected}\circ d_R", 1
        ),
        "restore-category-overclaim": paper.replace(
            "certificate assigns every canonical decorated directed relation",
            "universe, exactly one of the following holds", 1
        ),
    }
    for name, mutated in mutations.items():
        try:
            check_paper(mutated)
        except AssertionError:
            continue
        raise AssertionError(f"mutation was not rejected: {name}")
    comment_only = paper.replace(
        r"P_v(0,\ldots,0)=1", "1=1\n% P_v(0,\\ldots,0)=1", 1
    )
    try:
        check_paper(comment_only)
    except AssertionError:
        pass
    else:
        raise AssertionError("mutation was not rejected: comment-only-normalization")
    close_labels = figure.replace("-2.35", "-2")
    try:
        check_figure(close_labels)
    except AssertionError:
        pass
    else:
        raise AssertionError("mutation was not rejected: close-theta-labels")
    lowered_node = figure.replace("(x) at (0,-1.4)", "(x) at (0,-2.05)", 1)
    try:
        check_figure(lowered_node)
    except AssertionError:
        pass
    else:
        raise AssertionError("mutation was not rejected: lower-theta-node")


def main() -> None:
    paper = PAPER.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    figure = FIGURE.read_text(encoding="utf-8")
    check_paper(paper)
    check_figure(figure)
    check_scalar_regression()
    check_title_sync()
    require(r"P_v(0,\ldots,0)=1" in supplement,
            "supplement P3 omits component normalization")
    require("Sharp Generic-Identifiability Boundary" in supplement,
            "supplement title is stale")
    mutation_tests(paper, figure)
    print(json.dumps({
        "status": "VERIFIED",
        "revision": "v1.1.1",
        "theta_label_positions": [-2.35] * 4,
        "mutations_rejected": 8,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
