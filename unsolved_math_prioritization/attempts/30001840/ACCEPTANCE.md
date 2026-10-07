# Accepted scoped genus-two Galois-image results

Problem 30001840 / OWR-11127-008; rank 981. **Unsolved, five of five substantive author turns.** Accepted scope reviewed 2026-10-07 UTC. No novelty or full-solution claim.

Read the [complete expanded proof](audit_independent/corrected_public/PROOF.md), [full independent AI audit](audit_independent/AUDIT.md), and [actual correction patch](audit_independent/PROPOSED.patch). The [original proof](public/PROOF.md) remains frozen. The separate [prospective integral-lattice bridge](audit_independent/PROSPECTIVE_BRIDGE.md) is explicitly outside the accepted Jacobian-image coverage.

## Accepted scope

For C_t: y squared = x to the fifth minus 5 x cubed plus 5 x plus t, and K=Q(sqrt(5)):

1. At transcendental t, J_t[2] has arithmetic image F20=AGL_1(F5) over Q(t), and D5 of order ten geometrically and over K(t).
2. The generic geometric linear mod-three image has order 120, the central inverse image of projective A5. Sixty is the projective order, not the linear order.
3. For every prime ell at least seven, the generic geometric Tate-module image is SL_2(O_K tensor Z_ell), with full joint image at split primes.
4. At the same primes the arithmetic image over K(t) is the R-linear group with scalar R-determinant, and over Q(t) it is the full polarized RM normalizer.
5. The coarse geometric moduli curve has rational parameter t squared. The smooth fiber t=0 has arithmetic mod-two image C4 and one nonzero rational two-torsion class, so a generic image cannot be assigned uniformly to rational fibers.

The expanded proof details the integral RM module and polarization, the common characteristic-zero inertia element, the split-prime Goursat argument, and arbitrary-lift powering. It does not weaken the accepted local theorem. The original broad rational-fiber arithmetic question remains unresolved in this packet. Full integral images at 2,3,5, adelic independence, arbitrary rational-fiber classification, and all RM/level markings are not supplied. These are packet gaps, not certified globally open problems.

## Attribution and limits

The family and RM construction are credited to [Tautz–Top–Verberkmoes](https://doi.org/10.4153/CJM-1991-061-x) and [Darmon–Mestre](https://doi.org/10.4153/CMB-2000-037-X). The latter's residual theorem and common-inertia input are imported explicitly. The question is from Kohel's contribution to [Oberwolfach Report 35/2011](https://doi.org/10.4171/OWR/2011/35). The moduli formulas use [Takei's thesis](https://www.math.mcgill.ca/darmon/theses/takei/thesis.pdf) and are independently recomputed. Other finite-group, comparison, and lifting dependencies are identified in the proof and audit. The later [Lang–Lang Hecke index theorem](https://arxiv.org/abs/1401.0775) is prospective context; the missing integral-system bridge is not presumed. Cadoret–Moonen gives conditional openness, not exact uniform fiber images.

This is an AI-assisted mathematical investigation and independent AI audit, not conventional human peer review or formal certification. No exhaustive present-day literature search or historical novelty claim is made.

## Reproducibility correction

All acceptance tests in the original checks.py are Python assertions and disappear under actual -O/-OO. Its optimized output reproduces the frozen output but does not validate the mathematical tests. The separately preserved correction replaces assertions with explicit checks: all nine mathematical mutants are rejected under ordinary and genuine -O subprocess execution. The original rejects nine under ordinary execution and zero under -O. The wrapper also directly runs the corrected program and independent checker in real normal, -O and -OO child interpreters, checking their actual flags and complete output bytes.

Independent exact polynomial/group controls include all determinants in 1,962,930 enumerated matrices across moduli 2,3,4,5,7,9,11. Finite checks do not prove generic images, identify the actual bad-prime integral lattice, or replace the imported residual theorem. Historical output reproduction, optimization-safe validation, exact patch reconstruction, and package integrity are reported separately.

The 44 original/audit files, including the fifteen-file corrected derivative, are retained byte-for-byte. The original three manifest pins remain fixed. Historical statements that no publication or remote writes had occurred apply at their recorded freeze time. The public package contains only authored mathematics/code/audits and public bibliographic, hash, size, retrieval and inspection metadata. No source PDFs, extracted source text, datasets, private sources or coordination material are included.
