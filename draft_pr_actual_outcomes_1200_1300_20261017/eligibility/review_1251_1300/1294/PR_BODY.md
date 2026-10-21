## Accepted theorem and attribution

For every integer n > 1 with n ≡ 1 (mod 4), there is a tame knot in S³ with determinant n and signature 4. The complete proof gives genus at most two for nonsquares and for squares with a prime divisor congruent to 3 modulo 4, and genus at most three for the remaining squares. No universal genus-two claim is made.

The construction is credited to Alper Ferudun, *Knots with Signature 4 and Determinant 4k+1: An Answer to a Question of Shinohara*, dated 2 October 2026, Theorem 1.1 and Lemmas 3.1–3.2: [DOI 10.5281/zenodo.23111900](https://doi.org/10.5281/zenodo.23111900), [manuscript page](https://eulersolve.org/papers/amr-103-0226/). The manuscript is publicly described as an unrefereed, AI-assisted preprint; that status was checked on 11 October 2026.

This AI-assisted acceptance audit covers the stated unrestricted-knot existence theorem. It claims no novelty, human peer review, external refereeing, or certification of ancillary classification, lattice-theoretic, knot-table, minimal-crossing, or source-author software claims.

## Complete authored proof and bounded diagnostics

Start with the [packet README](https://github.com/AlecKriebel/Math/blob/b5ca51999d3dbb901b410e2ab74bfd1671d84dec/unsolved_math_prioritization/attempts/10400226/README.md), [complete proof](https://github.com/AlecKriebel/Math/blob/b5ca51999d3dbb901b410e2ab74bfd1671d84dec/unsolved_math_prioritization/attempts/10400226/PROOF.md), and [full audit](https://github.com/AlecKriebel/Math/blob/b5ca51999d3dbb901b410e2ab74bfd1671d84dec/unsolved_math_prioritization/attempts/10400226/AUDIT.md).

The full proof and original reconstruction are byte-preserved. All twelve mathematical audit checks and acceptance caveats remain. Presentation-only edits are listed in EDITORIAL_MAP.json. The construction retains the unbounded Dirichlet step, quadratic reciprocity, CRT, Sylvester's criterion and Seifert-matrix realization. In the remaining-square case the symmetric determinant is −n; the knot determinant is its absolute value n.

Exact diagnostic outputs agree byte-for-byte under ordinary Python, -O and -OO. The finite checks cover 2,504 distinct admissible n and 1,427 alternate divisor-branch checks. These support the written proof and do not establish its universal quantifier by finite search.

## Exact publication boundary

Exactly 12 added files, 42,581 bytes, under unsolved_math_prioritization/attempts/10400226/. No QUEUE.md or unrelated changes. Public content consists of authored proof, candidate, full audit and acceptance, plus public-source bibliographic/inspection/retrieval metadata and aggregate checks. No copied source documents, source extracts, inspection images, executable scripts, raw test matrices, witness datasets or private coordination material is included.

MANIFEST.json: 1,900 bytes; SHA-256 fe004a282338b3273339851e4a03c68fcda6c6a69b025f5fa56f476726f05a06.

PROOF.md: 7,895 bytes; SHA-256 2be1f719cb6f68b3fef7f9d810a3289c356b36a4992ca02b700b3eb4673b8074.

Local preparation and exact public-packet integrity verification passed in ordinary, -O and -OO modes. GitHub CI is reported separately from local checks. Draft publication only.
