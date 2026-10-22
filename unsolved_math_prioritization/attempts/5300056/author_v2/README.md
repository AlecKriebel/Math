# 5300056: bounded Jacobian cocycles and absolute continuity

**Outcome: scoped partial results; the general target remains unresolved.**

This is an authored research note for AMR-052-0056, Przytycki's 1992 Problem 2.5. It does not claim a new solution, a counterexample to the holomorphic problem, or priority. The source's already-known cases are credited. Five substantive routes were examined; no sixth route or general resolution is claimed.

The package proves:

1. Uniformly bounded L² sums are equivalent to an L² coboundary, including noninvertible probability-preserving maps.
2. The correctly signed exponential change of measure produces an equivalent sigma-finite conformal measure, with the centering constant retained.
3. Even an ergodic fair binary shift has L² coboundaries with no integrable exponential in the needed sign and unbounded pointwise sums. This is an obstruction to an abstract shortcut, not a holomorphic counterexample.
4. Explicit all-scale inverse-branch and finite landing-mass conditions suffice for Hausdorff absolute continuity.
5. Exact dimensionality and good density estimates only on a sequence of scales do not suffice: an explicit Moran measure has dimension 1/2, zero H^(1/2) support measure, and lower density zero.

Read `PROOF.md` for every hypothesis and proof, `LITERATURE.md` for source scope and the later literature checked, and `APPROACHES.md` for the unresolved gap. `source_metadata.json` contains public provenance metadata only.

Run:

    python3 verify.py
    python3 verify_manifest.py

The checks use Python's standard library and exact rational arithmetic. They test finite identities and constructions; they do not certify infinite-dimensional functional analysis, measure theory, or imported published theorems. The written proofs carry those arguments. This is an unaudited author freeze prepared for a fresh independent review.

The archive excludes source PDFs, text extracts, page images, raw datasets, private correspondence, and coordination records. Omitted source hashes document what was inspected; the offline verifier cannot revalidate bytes that are absent.
