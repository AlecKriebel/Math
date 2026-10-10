# Compactly supported Nijenhuis tensors with prescribed real Jordan type

## Result

For every n >= 1, exactly the Segre/Jordan types with entirely real spectrum
can occur on a nonempty open subset of R^n for a globally smooth, compactly
supported real Nijenhuis (1,1)-tensor. Any specified numerical real eigenvalues
and any Jordan block sizes and multiplicities are allowed. The type and the
eigenvalues may change outside the realization domain.

The [complete mathematical report](MATHEMATICAL_REPORT.md) constructs the
prescribed matrix on a torus collar, proves the exact ordered torsion identity
(A-lambda I)A'=0, and gives a finite block-by-block path to zero. Smooth endpoint
plateaus, the same-dimensional torus embedding, and exact zero extension make
the construction global with compact support. These analytic arguments cover
all dimensions and all real Jordan partitions; finite symbolic tests are only
corroboration.

Necessity is the credited prior theorem of Bolsinov–Konyaev–Matveev,
[Nijenhuis Geometry](https://arxiv.org/abs/1903.04603v2), Theorem 6.1, applied
to the zero extension on S^n. The nonreal obstruction, real semisimple cases
and two-dimensional Jordan examples were already credited by the problem
source. The report does not claim them as discoveries.

## Exact source and scope

The target is problem 2100509 / AMR-020-0509. The primary source is Bolsinov,
Matveev, Miranda and Tabachnikov,
[Open Problems, Questions, and Challenges in Finite-Dimensional Integrable Systems](https://arxiv.org/abs/1804.03737v2),
Problem 5.11, PDF page 29. The earlier v1 has Problem 4.10 on PDF page 37.
The corpus label 5.9 is reconciled by the full wording; it is not the locator
in either inspected primary version.

This is a smooth classification. It makes no assertion of a nonzero
real-analytic compactly supported field, a globally fixed Segre type, or a
prescribed matrix in the ambient Cartesian frame. The prescribed matrix holds
in a commuting local frame on the realization domain, which is sufficient
for the algebraic-type question.

## Review and contents

This is an AI-assisted, unrefereed manuscript with a separate mathematical
audit. Acceptance means that the written proof and its cited prior theorem
passed that audit. It is not external human peer review, journal acceptance,
formal proof-assistant verification, or a certificate of bibliographic
priority or of the problem's preexisting current openness.

- [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md): full general proof
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): independent derivations,
  boundary-case review, aggregate supporting checks and acceptance limits
- [ACCEPTANCE.json](ACCEPTANCE.json): exact public proof/audit identities and verdict
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): source identification, prior hypotheses,
  attribution and bounded literature observations
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source hashes, byte counts,
  locators and recorded inspection history
- [STATUS.json](STATUS.json): exact accepted scope and review limits
- [MANIFEST.json](MANIFEST.json): complete eight-file inventory and hashes of
  the other seven members; the draft PR body independently pins the manifest

No source PDF, copied source text, source image, program, dataset, raw generated
output, or private coordination material is distributed. No omitted file is a
premise of the general proof. Source inspection and finite-check observations
are explicitly recorded historical evidence; editorial preparation claims no
new source retrieval, inspection, literature search or computation rerun.

This edition changes no QUEUE entry or unrelated repository content and adds
no substantive proof-attempt response. Publication preparation does not
constitute a merge, journal submission, release, DOI, or outside outreach.
