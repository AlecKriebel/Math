# Optimal uniform Hurwitz lifting degree

Author-stage disposition: **claimed_solved, 3/5**. In characteristic zero, r>=3, the coarse inner lifting degree is at most 2, and an explicit C2 cover over Q(i) attains 2 over Q. The V4 base-stabilizer stratum has degree 1. Independent review is pending.

- PROOF.md gives the complete argument, conventions, source comparison, and a 15-value rational certificate.
- verify.py uses only the Python standard library. It performs 1,754 exact assertions, enumerates 120 Möbius candidates for each of a sharp example and a rejected negative control, and checks all 24 permutations of each four-point invariant.
- verify_symbolic.py requires SymPy (tested with 1.14.0). It performs 32 generic-identity and independent-replay assertions, with another complete 120-candidate enumeration.
- CONTROL_RESULTS.json and SYMBOLIC_RESULTS.json preserve reproducible output.
- SOURCE_VERIFICATION.json contains only source and dataset verification metadata. No source PDF, extracted full text, catalogue contents, or private material is included.

Run from this directory:

    python verify.py
    python verify_symbolic.py

Do not redirect verify.py onto CONTROL_RESULTS.json while reading that same certificate; use a temporary output file if comparing output. These checks verify finite algebraic certificates; they do not mechanically prove the general descent argument.

The mathematical dependencies and the distinction between coarse point fields of moduli and actual G-cover fields of definition are explicit. The result is an optimal universal constant, not a sharp bound for each separately fixed datum. No first-priority claim is made. This work used AI extensively and is unrefereed, without external human peer review.
