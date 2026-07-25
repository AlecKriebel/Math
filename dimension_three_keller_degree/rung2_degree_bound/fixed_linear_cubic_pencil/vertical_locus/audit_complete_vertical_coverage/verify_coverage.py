#!/usr/bin/env python3
"""Dependency-free combinatorial audit of the triple-vertical branch tree.

This checks coverage and disjoint routing only.  It does not replace the
algebraic checkers attached to the terminal lemmas.
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

if not __debug__:
    raise SystemExit("FAIL: refusing optimized Python")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PROGRAM = ROOT.parents[1]
MUTATION = os.environ.get("VERTICAL_COVERAGE_MUTATION", "")


def require(relative: str, needle: str | None = None) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise SystemExit(f"FAIL: missing coverage artifact {relative}")
    if needle is not None and needle not in path.read_text(encoding="utf-8"):
        raise SystemExit(
            f"FAIL: coverage artifact {relative} lacks marker {needle!r}"
        )
    return path


# Inputs and every terminal proof/audit used by the routing certificate.
require("WORKING_VERTICAL_FIXED_LINEAR_CUBIC_PENCIL.md", "Vertical multiplicity theorem")
require("E8_E4_RANK_LEDGER.md", "complete \\(E_7\\) families")
require("NONVERTICAL_NONTRIPLE_LEMMA.md", "nonvertical nontriple companion")
require("NONVERTICAL_TRIPLE_ROOT_LEMMA.md", "nonvertical triple-root companion")
require("audit_nonvertical_companion/REPORT.md", "**Verdict:** **PASS**")
require("VERTICAL_ELL_ZERO_NONTRIPLE_LEMMA.md", "zero-\\(\\ell\\), nontriple")
require("audit_vertical_ell_zero_nontriple/REPORT.md", "**Verdict:** **PASS**")
require(
    "VERTICAL_NONZERO_ELL_NONTRIPLE_LEMMA.md",
    "nonzero-\\(\\ell\\), nontriple",
)
require(
    "audit_vertical_nonzero_ell_nontriple/REPORT.md",
    "**Verdict:** **PASS**",
)
require("VERTICAL_TRIPLE_GAMMA0_ELL0_LEMMA.md", "zero-\\(\\gamma\\), zero-\\(\\ell\\)")
require("audit_vertical_triple_gamma0_ell0/REPORT.md", "**Verdict:** **PASS**")
require("VERTICAL_TRIPLE_GAMMA0_REDUCTION.md", "reduces to zero \\(\\ell\\)")
require("audit_vertical_triple_gamma0_reduction/REPORT.md", "**Verdict:** **PASS**")
require("VERTICAL_TRIPLE_GAMMA_NONZERO_EXCLUSION.md", "nonzero-\\(\\gamma\\)")
require(
    "audit_vertical_triple_gamma_nonzero/REPORT.md",
    "**Verdict:** **PASS**",
)
require("VERTICAL_A0_W0_ZERO_EXCLUSION.md", "zero-\\(a\\), zero-\\(W_0\\)")
require("audit_vertical_a0_w0_zero/REPORT.md", "**Verdict:** **PASS**")
require("a0_w0_nonzero_attack/NOTE.md", "zero-companion-parameter branch")
quadratic_exit = PROGRAM / "WORKING_QUADRATIC_COMPONENT_EXIT.md"
if not quadratic_exit.is_file():
    raise SystemExit("FAIL: missing quadratic-component exit")
if "independently adversarially audited" not in quadratic_exit.read_text(
    encoding="utf-8"
):
    raise SystemExit("FAIL: quadratic-component exit lacks audited status")

a0_nonzero_audit = ROOT / "audit_a0_w0_nonzero/REPORT.md"
a0_nonzero_audited = False
if a0_nonzero_audit.is_file():
    audit_text = a0_nonzero_audit.read_text(encoding="utf-8")
    a0_nonzero_audited = (
        "**Verdict:** **PASS**" in audit_text
        or "**Verdict: PASS" in audit_text
    )
    if not a0_nonzero_audited:
        raise SystemExit("FAIL: a=0,W0!=0 hostile report exists without PASS verdict")


def state(**kwargs: str) -> tuple[tuple[str, str], ...]:
    return tuple(sorted(kwargs.items()))


states: list[tuple[tuple[str, str], ...]] = [
    state(m="1"),
    state(m="2"),
    state(m="3", companion="zero"),
]

q_cells = (
    ("squarefree", "-"),
    ("double", "-"),
    ("triple", "C"),
    ("triple", "B"),
    ("triple", "E"),
)

# Nonvertical companion G3=q.
for root, chart in q_cells:
    states.append(state(m="3", companion="q", root=root, chart=chart))

# Vertical companion G3=z^3, a!=0, nontriple q0.
ell_positions = {
    "squarefree": ("zero", "generic", "root_x", "root_y", "root_x_minus_y"),
    "double": ("zero", "generic", "double_root_x", "simple_root_y"),
}
for root, positions in ell_positions.items():
    for ell in positions:
        states.append(
            state(
                m="3",
                companion="z3",
                a="nonzero",
                root=root,
                ell=ell,
            )
        )

# Vertical companion G3=z^3, a!=0, triple-root q0.
for chart in ("C", "B", "E"):
    states.append(
        state(
            m="3",
            companion="z3",
            a="nonzero",
            root="triple",
            chart=chart,
            gamma="nonzero",
        )
    )
    for ell in ("zero", "nonzero"):
        states.append(
            state(
                m="3",
                companion="z3",
                a="nonzero",
                root="triple",
                chart=chart,
                gamma="zero",
                ell=ell,
            )
        )

# Vertical companion G3=z^3, a=0, W0=0: the five q charts.
for root, chart in q_cells:
    states.append(
        state(
            m="3",
            companion="z3",
            a="zero",
            W0="zero",
            root=root,
            chart=chart,
        )
    )

# Vertical companion G3=z^3, a=0, W0!=0.  This branch uses its own
# complete W0-rank/root-incidence atlas rather than the q-tail chart atlas.
incidence = {
    ("rank2", "squarefree"): ("none", "one", "both"),
    ("rank2", "double"): ("none", "double_root", "simple_root", "both"),
    ("rank2", "triple"): ("none", "triple_root"),
    ("rank1", "squarefree"): ("m0", "m1"),
    ("rank1", "double"): ("m0", "m1_simple", "m2_double"),
    ("rank1", "triple"): ("m0", "m3"),
}
for (w_rank, root), positions in incidence.items():
    for position in positions:
        states.append(
            state(
                m="3",
                companion="z3",
                a="zero",
                W0="nonzero",
                W0_rank=w_rank,
                root=root,
                incidence=position,
            )
        )

if len(states) != len(set(states)):
    raise SystemExit("FAIL: duplicate atomic coverage state")
if len(states) != 47:
    raise SystemExit(f"FAIL: expected 47 atomic states, found {len(states)}")


def mapping(cell: tuple[tuple[str, str], ...]) -> dict[str, str]:
    return dict(cell)


def terminal_predicates(cell: tuple[tuple[str, str], ...]) -> dict[str, bool]:
    c = mapping(cell)
    m = c["m"]
    companion = c.get("companion")
    root = c.get("root")
    a = c.get("a")
    ell = c.get("ell")
    gamma = c.get("gamma")
    w0 = c.get("W0")
    predicates = {
        "quadratic_exit": m in {"1", "2"} or (m == "3" and companion == "zero"),
        "nonvertical_nontriple": (
            m == "3" and companion == "q" and root in {"squarefree", "double"}
        ),
        "nonvertical_triple": (
            m == "3" and companion == "q" and root == "triple"
        ),
        "vertical_a1_nontriple_ell0": (
            companion == "z3"
            and a == "nonzero"
            and root in {"squarefree", "double"}
            and ell == "zero"
        ),
        "vertical_a1_nontriple_ellnz": (
            companion == "z3"
            and a == "nonzero"
            and root in {"squarefree", "double"}
            and ell not in {None, "zero"}
        ),
        "vertical_a1_triple_gamma_nz": (
            companion == "z3"
            and a == "nonzero"
            and root == "triple"
            and gamma == "nonzero"
        ),
        "vertical_a1_triple_gamma0_ell0": (
            companion == "z3"
            and a == "nonzero"
            and root == "triple"
            and gamma == "zero"
            and ell == "zero"
        ),
        "vertical_a1_triple_gamma0_ellnz": (
            companion == "z3"
            and a == "nonzero"
            and root == "triple"
            and gamma == "zero"
            and ell == "nonzero"
        ),
        "vertical_a0_w0_zero": (
            companion == "z3" and a == "zero" and w0 == "zero"
        ),
        "vertical_a0_w0_nonzero": (
            companion == "z3" and a == "zero" and w0 == "nonzero"
        ),
    }
    if MUTATION == "drop_a0_w0_nonzero":
        predicates["vertical_a0_w0_nonzero"] = False
    elif MUTATION == "overlap_nonvertical":
        predicates["quadratic_exit"] = predicates["quadratic_exit"] or (
            companion == "q"
        )
    elif MUTATION:
        raise SystemExit(f"FAIL: unknown mutation {MUTATION}")
    return predicates


routes: Counter[str] = Counter()
for cell in states:
    hits = [name for name, hit in terminal_predicates(cell).items() if hit]
    if len(hits) != 1:
        raise SystemExit(f"FAIL: atomic state has {len(hits)} terminal routes: {cell}")
    routes[hits[0]] += 1

expected = Counter(
    {
        "quadratic_exit": 3,
        "nonvertical_nontriple": 2,
        "nonvertical_triple": 3,
        "vertical_a1_nontriple_ell0": 2,
        "vertical_a1_nontriple_ellnz": 7,
        "vertical_a1_triple_gamma_nz": 3,
        "vertical_a1_triple_gamma0_ell0": 3,
        "vertical_a1_triple_gamma0_ellnz": 3,
        "vertical_a0_w0_zero": 5,
        "vertical_a0_w0_nonzero": 16,
    }
)
if routes != expected:
    raise SystemExit(f"FAIL: terminal counts differ: {routes!r}")

for name in sorted(routes):
    print(f"{name}={routes[name]}")
print("COVERAGE_ATOMIC_CELLS=47")
print(
    "A0_W0_NONZERO_STATUS="
    + ("HOSTILE_PASS" if a0_nonzero_audited else "PROVISIONAL")
)
print("TRIPLE_VERTICAL_COVERAGE_PASS_4E7B19")
