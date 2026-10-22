# 30005353: review-ready partial investigation

**Unresolved after five substantive approaches.** This is an authored packet awaiting independent mathematical review, not a solution, external peer review, or novelty claim. No publication or queue change has been made.

## Main results

- The supremum of aπ/a₂ over finite connected graphs with a cycle is unchanged when restricted to maximum-degree-three graphs. Both cost inequalities and walk normalization are proved.
- Explicit odd-torsion graphs satisfy a₂=162p and aπ=162p+3 for every odd p≥3. The smallest supplied example has costs 486 and 489.
- Bridge sums and uniform subdivisions cannot amplify a bounded ratio. They do yield a connected uniformly bounded-degree family with additive gap 3k.
- For every simplicial triangulation of RP², a₂=aπ=3(r−1)+s. This flags an apparent coefficient-specific inconsistency in the source's additive example, pending independent review. Odd-characteristic homology behaves differently.
- A field-dependent homological-systole criterion isolates a sufficient missing construction. A reconstruction of the credited Rizzi weakly-fundamental deletion argument gives aπ/a₂ ≤ 2 ceil(log₂(2r))+1 for r≥2. Planar equality follows from the credited planar minimum-basis theorem.

The main missing step remains either an unbounded-ratio family or a universal constant upper bound. None is supplied.

## Contents

- PROOF.md: full proofs, all hypotheses, and five route-specific gaps
- APPROACH_LEDGER.md: five actual mathematical approaches, excluding source searches and packaging
- SOURCE_AUDIT.md: primary-source identification, bounded current-literature findings, bibliographic credit, and interpretation limits
- VERIFICATION.md: commands, exact checks, and what they do not establish
- SOURCE_METADATA.json: public document metadata and byte/hash evidence only

The sibling checks directory contains three standard-library Python checkers and their reproducible JSON receipts. The sibling private_sources directory is outside this authored candidate packet and contains copied reading PDFs, page renders, extracted text, and corpus candidates. It must not be published with the authored material.

## Run finite controls

From the packet's root directory:

    python3 checks/verify.py
    python3 checks/degree_checks.py
    python3 checks/deletion_checks.py

Ordinary Python mode is required: the tests use assertions. No network or third-party Python package is needed. These checks supplement rather than replace the mathematical proofs.
