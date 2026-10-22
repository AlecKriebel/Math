# AIM Hilbert Problem 16: monomial component signatures

Problem ID: **20000817** · Code: **AIM-ARITHMETIC_GEOMETRY-0063** · Rank: **760**

**Disposition: rigorous partial progress; the general question is unresolved by this work. No novelty claim.**

The original question asks whether the full set of monomial ideals on an irreducible component determines that component, first for affine Hilbert schemes of points and then for ordinary projective Hilbert schemes. The catalog title describes an earlier partial result, rather than the full question.

## Results

- Complete monomial signature of the nonsmoothable length-eight component: the quotient has cube-zero maximal ideal and embedding dimension at least four. A closed-condition argument and explicit flat families prove this in characteristic different from 2 and 3.
- Its signature has size \(\sum_{e=4}^{\min(7,n)}\binom ne\binom{e(e+1)/2}{7-e}\). In dimensions 4–7 the counts are 120, 705, 2451, 6553.
- The usual length-at-most-eight injectivity result holds in characteristic different from 2 and 3. The projective result with at most two Borel-fixed points holds in every characteristic, using Ramkumar and Staal.
- Every affine monomial ideal is smoothable, so a genuine counterexample requires two nonsmoothable components. Searching for an ambient-smooth monomial anchor on either such component cannot work.
- An explicit saturated monomial ideal separates the published pair of components of \(\operatorname{Hilb}^{3t+2}(\mathbb P^3)\) with equal double-generic initial ideal. That collision is not a full-signature counterexample.

See [PROOFS.md](PROOFS.md) for proofs and [RESEARCH_REPORT.md](RESEARCH_REPORT.md) for prior-work reconciliation, the five approaches and remaining gaps. Source and input verification metadata are in [sources.json](sources.json) and [provenance.json](provenance.json).

## Replay

Run `python3 verify_packet.py` from this directory. It checks the safe file manifest and independently re-executes `code/verify_signatures.py`, comparing its exact output with `results/verification.json`.

The finite checks enumerate all length-eight monomial ideals in dimensions 1–7, verify 247 flat multiplication models over the integer polynomial ring, compute all 120 relevant four-variable tangent dimensions over the rationals, and check the projective witness's Hilbert function. They are controls, not substitutes for the imported classification or the geometric proofs. Author replay is not independent review.

The packet contains only authored work and verification/bibliographic metadata. Source PDFs, source extracts, raw dataset records and coordination files are excluded. No repository write was performed in this investigation.
