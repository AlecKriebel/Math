# Discovery 07: one inverse-series mechanism, two every-order obstructions

Status: **canonical research draft; not peer reviewed**.

This directory accompanies the paper

> **A 14-variable unipotent Keller map and every-order image and vanishing
> obstructions**

The paper consolidates the mathematical content of Discoveries 03, 05, and
06 around one theorem rather than counting closely related consequences as
separate discoveries. Its spine is a formal inverse pencil and a linear
observable:

1. the Abhyankar--Gurjar formula transfers every nonzero inverse coefficient
   to an every-exponent obstruction for the Special Image Conjecture;
2. the symmetric Hessian construction and Zhao's inverse formula transfer the
   same coefficients to every-order failure of the Vanishing Conjecture.

The flagship object is the explicit 24-term vector

    g in Q[Z]^14

whose determinant pencil is one, whose generic Jacobian type is the single
nilpotent block `(14)`, and whose identity-linear map has an exact reduced
three-point rational fiber. The two homogeneous endpoints are complementary:

- a 30-variable degree-eight Hessian-nilpotent polynomial, optimized here for
  ambient dimension;
- a 44-variable quartic Hessian-nilpotent polynomial, addressing the classical
  homogeneous-quartic formulation.

In both cases `Delta^m(P^(m+1))` is proved nonzero for **every** `m >= 0` by
closed coefficient formulas. No high power of either large polynomial is
formed.

Start with [the manuscript](unified_consequences.tex) or
[the rendered PDF](output/pdf/unified_consequences.pdf). The concise artifact
overview is in [NOTE.md](NOTE.md), and [MANIFEST.md](MANIFEST.md) maps every
headline claim to its exact checker.

## Reproduce

From this directory, create the repository-level environment and install the
pinned dependency:

```bash
python3 -m venv ../.venv
../.venv/bin/python -m pip install -r requirements.txt
```

The main exact checker uses SymPy:

```bash
../.venv/bin/python verify_symbolic.py
```

Regenerate and check the deterministic sparse certificate:

```bash
../.venv/bin/python export_certificate.py
python3 verify_exported_stdlib.py
node verify_exported_node.mjs
```

Build the PDF:

```bash
python3 render_paper.py
```

The expected SHA-256 of `output/unified_every_order.json` is

    deb01a83cea8543b17c13e8849cead0159d5d8feac07ae18034fd880a274495c

The reference symbolic run used approximately 74 MiB maximum resident memory.
The checkers rely on structural identities and sparse arithmetic rather than
large multivariate powers, so they are suitable for a 16 GB workstation.

## What is and is not one result

The 14-variable collision gives several named injectivity and fixed-point
counterexamples by direct transformations. Those statements form one
consequence cascade; they are not marketed as independent breakthroughs. The
Special Image and Vanishing obstructions require additional inverse-series
transfer theorems and are the substantive operator-theoretic upgrades.

Discovery 04, on iterated wreath-product monodromy, remains a separate current
paper because it studies different mathematics. Discoveries 03, 05, and 06
remain public as timestamped technical precursors and certificate sources.
Future incremental corollaries of this mechanism belong in this paper's log or
appendices. A further numbered discovery should require a genuinely smaller
construction, a new reduction class, or a new conceptual theorem.

## Authorship and warning

Author: Alec Kriebel, with heavy assistance from ChatGPT 5.6 Sol (OpenAI).

Alec Kriebel is a complete amateur exploring the limits of AI-assisted
mathematics and cannot independently verify these claims. The manuscript,
programs, and exact certificates are released for expert review. Passing the
checks is evidence about the encoded algebra; it is not peer review and does
not establish novelty or correctness of the mathematical interpretation.
