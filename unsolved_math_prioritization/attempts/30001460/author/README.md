# K-sheet quotients: type-A gluing and the separation obstruction

Problem 30001460 / OWR-4332-001. Research date: 2026-10-06.

**Status: partial resolution of the general question.** A proof below constructs a geometric quotient in the category of possibly nonseparated schemes for every K-sheet when the ambient Lie algebra is gl_n (and, by the trace-zero reduction explained below, sl_n), over an algebraically closed field of characteristic zero. More generally it gives an explicit connected-centralizer sufficient criterion. The construction glues p-Slodowy slices and is a deduction from established theorems of Katsylo, Bulois, and Bulois–Hivert. No novelty is claimed.

The requirement of a **separated** quotient has a negative answer already for sl_2: two distinct regular nilpotent orbits would have to be identified. This example and its doubled-origin quotient are already in the published literature. It does not disprove existence of nonseparated quotients.

The quotient for the entire regular K-sheet in arbitrary symmetric type is independently covered by Hameister–Morrissey (2025). The general nonregular, arbitrary-type problem is not resolved here.

Files:
- RESULT.md: assumptions, credited inputs, detailed gluing proof, rank-one proof, and remaining gap
- APPROACHES.md: five bounded approaches and their outcomes
- SOURCES.json: public source locators, inspection history, hashes, and input identity checks; no source text
- certificate.py and EXPECTED.json: exact symbolic checks of the rank-one formulas only
- verify.py and MANIFEST.json: strict inventory and source-pinned replay

Run Python 3.10 or later, with no third-party packages:

    python -B verify.py
    python -O -B verify.py

The checker validates the sealed files and symbolic identities. It does not formally verify algebraic geometry or turn a finite experiment into a proof. RESULT.md is the mathematical deliverable. This is an author package awaiting independent review.
