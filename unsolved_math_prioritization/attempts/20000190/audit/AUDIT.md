# Independent adversarial audit: rank 640 / 20000190

Date: 2026-10-04 UTC. Target: AIM-ALGEBRAIC_GEOMETRY-0190.

## Verdict

**PASS_WITH_SCOPE_NOTES. Retain unsolved, 5/5; do not promote to solved.**
No material mathematical correction to the frozen packet is required. The
counterexamples, finite-chart count, and feasibility reduction withstand this
independent audit. They do not establish a complete practically efficient
pre-candidate physical-feasibility algorithm, an estimator for noisy data, or
novelty. The audit preserves the author packet unchanged.

The author manifest SHA-256 is
`43493ad880a6f0a210fe75246301ab81d7575884050b182e63f4e4b71389cf2d`.
The reviewed PARTIAL.md SHA-256 is
`134d3fc65f864d0407fe9135ebd814c0d2c82706f40028c6a8795bd8159587ce`.
All eleven listed author files and the exact file set pass verification.

The author's 240 exact assertions reproduce CONTROL_RESULTS.json byte-for-byte.
A separate deterministic audit adds **676 assertions**, comprising 660
mathematical assertions and 16 integrity/replay assertions. Its tests use exact
rational or symbolic arithmetic. The independent Tarski oracle deliberately
uses exact real-root isolation; the author's tested Hermite algorithm does not.
No root approximations are used in either.

## Source identity and prior-work separation

The canonical [AIM Reconstruction page](http://aimpl.org/algvision/1/) was
retrieved afresh. Problem 1.5 matches the selected catalogue record's original
statement exactly: 298 UTF-8 bytes, SHA-256
`ac8a365219fd81759d02fcb14594f4c8b4ebc3c4b10e3a58e7cdfcb70f21ace4`.
The mathematical target is the broad question about anticipating imaginary
focal estimates before constructing a fundamental matrix. The seven-point
certificate title is not substituted for that target. The intrinsic convention
and the distinction between a matrix pencil and a constructed root matrix are
explicit in the submission.

The full supplied prior report was inspected. Its generic four-query
Sturm--Tarski count, mixed-sign example, conservative boundary, and generic
real-camera argument are inherited work. The new packet credits that result
and does not rebrand it as a new full solution. The equal-determinant example
and critical-family fixture are different from the prior report's fixture.
The broader public corpus hashes are author-recorded provenance; this audit
independently checks the selected record's statement, not the full corpus.

All four freshly retrieved primary HTML/PDF byte hashes match the source
manifest. The supplement formula was checked visually on its rendered second
page. [Kocur, Kyselica and Kukelova, CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/papers/Kocur_Robust_Self-calibration_of_Focal_Lengths_from_the_Fundamental_Matrix_CVPR_2024_paper.pdf)
places RFC after candidate generation and before scoring. Its
[supplement, Section 3 and Eq. (1)](https://openaccess.thecvf.com/content/CVPR2024/supplemental/Kocur_Robust_Self-calibration_of_CVPR_2024_supplemental.pdf)
contains the quartics used here. The [arXiv record](https://arxiv.org/abs/2311.16304)
confirms the v3 revision of 6 November 2025; this is not CVPR's publication year.

[Gaillard and Safey El Din, Theorem 2.4 and Eq. (2)](https://arxiv.org/html/2402.07782v2)
support the classical Hermite/Tarski identity and zero-aware sign determination.
Their generic parameter classification is not a solution of every exceptional
camera fiber. No priority conclusion follows from this bounded inspection or
from the audit's targeted searches.

## 1. Equal determinants and opposite focal signs

The determinant identity is exact, including the scalar normalization. The
quadratic factor has discriminant -6860, and the zero root is simple. Both
root matrices have rank two. The anisotropic image transform has determinant
one and preserves the determinant polynomial and rank-seven design relation.
It does not preserve the imposed square-pixel intrinsic convention, which is
precisely why the two fixed-convention datasets can differ in focal feasibility.

Independent nonzero 7-by-7 minors certify both design ranks. In the row-major
convention and first seven columns, the audit obtains determinant
-14482069056000 for each. The two matrix directions are independently verified
linearly independent, so the nullspaces really are the asserted pencils.

Direct Gröbner elimination of all nine radical-free essential equations gives
these complete affine calibration ideals over the rationals:

- B: `(a - 4, b - 25)`
- H^(-T)B: `(a + 112/377, b + 1925/67)`

Thus the second root does not hide a different positive calibration pair. The
explicit real rotation, translation and positive intrinsics of B also replay.
This supports the determinant-only obstruction for these supplied pencils.
It does not obstruct methods using the full design matrix, and does not certify
cheirality of the seven B correspondences.

## 2. Zero-aware Hermite count

The indicator `(s^2+s)/2` is correct on {-1,0,1}; multiplying two indicators by
the nonnegative real rank guard gives exactly formula (A). The guard is one in
sign precisely at real rank-two determinant roots and zero at lower rank. The
squarefree reduction counts distinct roots, not algebraic multiplicities.

The trace-form proof is valid: real factors contribute their sign, and each
nonreal conjugate pair contributes signature zero, including the case when the
weight vanishes. The rational congruence implementation correctly creates a
nonzero diagonal pivot from a nonzero off-diagonal entry. It need not assume
all leading principal minors are nonzero.

The audit compares the actual author Tarski routine to a separately written
exact root-isolation sign oracle on 100 deterministic polynomials. Cases
include shared roots, zero queries, repeated roots and nonreal factors. Another
25 transformed known-root pencils verify the full chart counts with rank and
zero guards. No disagreement was found.

The projective interpretation is correct only after adding infinity once when
appropriate. Fifteen GL(2,Q) basis changes preserve the total counts under an
explicit infinity wrapper. Four additional cases cover affine determinant
degrees zero and one, repeated projective roots, rank-one infinity, and
rank-two infinity. Identically singular pencils are rejected as intended.

## 3. Four zero quartics and a cheiral positive continuum

For T, all four quartics vanish and the calibration ideal is exactly `(a-b)`.
For the stated real rank-two matrix and positive a,b, this is an entire
one-parameter physical intrinsic family, not a unique solution obscured by a
removable chart factor. The critical pencil has only one real determinant
root, and an independent 7-by-7 design minor is 22680.

The author proves cheirality at unit focal length. The audit checks the
stronger all-positive-focal statement directly. For arbitrary f>0, set

`Z = f/(u' - u), X = (u Z/f, v Z/f, Z)`.

Since u<0 and u'>0, Z>0. With K=diag(f,f,1), cameras K[I|0] and
K[I|(1,0,0)^T] project X exactly to the same seven image pairs. Both depths
remain Z>0. This establishes cheirality of the entire common-focal family.

In contrast, diag(1,2,0) has calibration ideal `(a b)`, and so no strictly
positive pair. The shared zero-quartic flag therefore cannot mean either
"impossible" or "feasible" by itself. The author correctly reports it as
unclassified.

## 4. Radical-free reduction and chart sufficiency

Starting from E=K2 F K1, multiplication of the essential cubic on the left by
K2^(-1) and on the right by K1^(-1) gives equation (B) exactly. These inverses
exist because a,b>0. A real rank-two E satisfies that cubic exactly when its
two nonzero singular values agree. It therefore represents real rotation and
nonzero translation. Rank, strict positivity, and reality cannot be discarded.
The existential formulation is consequently correct for matrix calibration;
it does not impose pointwise cheirality.

Beyond examples, the audit checks a universal polynomial certificate. For a
fully symbolic 3-by-3 F, let Atilde=diag(N1,N1,D1) and
Btilde=diag(N2,N2,D2). Every entry of

`2 F Atilde F^T Btilde F - trace(F Atilde F^T Btilde) F`

is exactly divisible by det(F). This is denominator-cleared chart sufficiency,
not a statistical inference from samples. When D1 D2 is nonzero, the chart
values satisfy all essential equations at any rank-two determinant root.

Eighty independently generated exact real camera fixtures, using rational
quaternion rotations and positive rational focal lengths, pass the equations
and focal-ratio identities, including eight chart-degenerate fixtures. One
hundred additional arbitrary rank-two matrices agree with the author's quartic
implementation; all 91 with nonzero denominators satisfy the exact residuals.
None of this turns general quantifier-elimination decidability into a measured
practical algorithm.

## 5. Pole and conditioning claim

The displayed rational functions agree exactly with the quartics. Their
all-epsilon sign conclusions follow from their factorizations; the finite
six-scale checks are supporting tests, not the proof of that universal claim.
The matrices differ by entrywise maximum 4 epsilon and retain a nonzero
2-by-2 minor. Positive and negative focal classes thus meet arbitrarily closely
at this boundary.

The audit additionally eliminates a,b at the exact t=-1 matrix. Its essential
calibration ideal is `(1)`, so no finite algebraic calibration pair exists there.
This is consistent with the pole and does not contradict the positive side
limit. Other numerator and denominator boundary points are tested separately.
The argument does not rule out adaptive certification away from a boundary or
establish an impossibility theorem for every robust estimator.

## Scope notes and disposition

No frozen author file needs a mandatory mathematical edit. CORRECTIONS.md
records nonblocking API/documentation refinements. In particular, the reusable
author function is affine; its name must not be taken to promise automatic
infinity handling. The zero-aware result concerns one chart, and the exact
rational implementation is not an arbitrary-real or floating-point API.

Keep the five recorded routes and **unsolved, 5/5** disposition. Neither the
completion percentage nor a bounded search is a quantitative theorem or
priority certificate. This review is a separate AI-assisted mathematical and
computational audit, not journal peer review.

No remote write, outside communication, release or DOI action was performed.
Live queue, duplicate and publication checks are the publisher's responsibility
immediately before a separately authorized remote mutation. This mathematical
audit does not claim to refresh those mutable remote-state checks.

## Reproduction and artifact boundary

Use Python 3 with SymPy 1.14.0:

`python audit_verify.py /path/to/submission > reproduced.json`

Compare reproduced.json byte-for-byte with AUDIT_RESULTS.json. Then run
`python verify_audit_manifest.py /path/to/submission` to check the binding and
both file sets. The default submission location is the sibling `submission/`.

The audit contains authored analysis, authored verification code, and public
source verification metadata only. It contains no source full text, scholarly
PDF, dataset record, public corpus, credentials, or private coordination file.
