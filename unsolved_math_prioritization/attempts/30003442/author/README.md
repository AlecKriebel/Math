# Largest Roots of Doubly Stochastic Stable Polynomials

Problem 30003442 / OWR-15219-012. Status: partial result; unrestricted question unresolved. No novelty claim.

The self-contained comparison in PROOF.md proves the target for every positive m,d with min(m,d)≤3. The accompanying verifier checks exact identities, low-dimensional admissible examples, two negative controls against invalid symmetry/flow arguments, and a finite product-polynomial search. A finite search is not a proof of the unrestricted statement.

Primary source: Petter Brändén, “The van der Waerden and Kadison-Singer conjectures with symmetries,” in Oberwolfach Report 14/2017, printed pp. 825–826, https://doi.org/10.4171/OWR/2017/14. The requested inequality is Conjecture 1. Its symmetric-case conclusion is announced as Theorem 4, with proof deferred; the displayed flow sign and monotonicity direction have exact counterchecks in PROOF.md. These defects in auxiliary printed formulas do not refute Conjecture 1.

Verification: Python 3.11+ and SymPy 1.14; run `python verify.py`. Run `python verify.py --self-test` for the deliberately false-claim controls. Run `python audit_manifest.py` for package integrity, or add `--self-test` to check rejection of 14 damaged packages. The generated JSON is deterministic and contains only original exact computations and public-source metadata. No network, source PDFs, dataset or private inputs are required.

Safe package boundary: only this directory's manifested files are candidates for sharing. Source PDFs, extracted text, screenshots, raw dataset records and private coordination material are excluded. Independent audit is required before publication. This package performs no remote writes.
