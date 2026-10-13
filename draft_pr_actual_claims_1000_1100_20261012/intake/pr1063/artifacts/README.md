# Affine incidence matching: credited prior resolution

Problem **30000391 / OWR-1183-011**, priority rank 1223.

## Accepted conclusion

For every positive finite integer d and every set P contained in R^d with affine span R^d, there is an injection from P into the affine hyperplanes spanned by subsets of P that assigns every point an incident hyperplane. Arbitrary infinite P is covered in ZFC, including singular cardinalities. There is no continuum-hypothesis, regular-cardinality or general-position restriction.

The result follows from Jonathan David Farley's published [Theorem 11](https://ajc.maths.uq.edu.au/pdf/82/ajc_v82_p228.pdf), in *A question of Björner from 1981: Infinite geometric lattices of finite rank have matchings*, Australasian Journal of Combinatorics 82(3) (2022), 228-236. The original question is Anders Björner's *Matching points to hyperplanes*, [Oberwolfach Report 1/2006](https://ems.press/content/serial-article-files/46029?nt=1), printed pages 51-52.

This edition records a credited prior resolution and its mathematical audit. It consumes **zero new proof-search turns** and makes no novelty or first-proof claim.

## Scope and audit boundary

The affine-flat lattice has rank d+1. Its atoms are the points of P, and its coatoms correspond bijectively to the P-spanned ambient hyperplanes. Farley's incidence-preserving atom-to-coatom injection therefore gives exactly the required point-to-hyperplane injection.

The literal d=0 extension is false: P=R^0 is a singleton with no incident hyperplane. The accepted theorem is explicitly restricted to d>=1; d=1 has the direct matching p -> {p}. The affine-spanning hypothesis is essential.

The complete applicability argument and internal proof audit are retained. The latter checks Farley's displayed argument relative to explicitly named external inputs; it is not a recursive proof audit of every imported reference. The general theorem remains credited to Farley and the earlier authors cited in his paper. No bijective matching, measurable or definable choice, infinite-dimensional extension, choice-free theorem, or disjoint-maximal-chain result is claimed.

## Documents and provenance

- [APPLICABILITY_CERTIFICATE.md](APPLICABILITY_CERTIFICATE.md): full reduction, injectivity and incidence transfer, cardinality scope, and mathematical boundary examples
- [INTERNAL_PROOF_AUDIT.md](INTERNAL_PROOF_AUDIT.md): complete internal proof checks, including the singular-cardinal closure step and both final geometric cases
- [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md): accepted disposition, mathematical checks, and limits
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md) and [SOURCE_LEDGER.json](SOURCE_LEDGER.json): public scholarly-source titles, URLs, PDF hashes and byte counts, publication status, and retrieval/inspection history
- [STATUS.json](STATUS.json): structured accepted scope, attribution, and zero new proof-search turns
- [MANIFEST.json](MANIFEST.json): edition file identities

Source retrieval and inspection statements belong to the originating audit dated 2026-10-10. Publication preparation does not represent a new source inspection. The authored applicability certificate and internal proof audit are AI-assisted and unrefereed. Farley's closing result remains a published journal article. The authored audit makes no claim of foundational re-proof of the imported results.
