# de Gennes bound: scoped variational results

**Original problem 30005598 / OWR-14297736-004 remains unresolved, 5/5.**

The all-domain question concerns the magnetic Neumann ground state with the
fixed standard uniform-field potential. The disk case was already proved by
Corentin Lena and Mikael Sundqvist in May 2026. This packet claims neither that
prior theorem nor a universal solution as a new result.

The packet proves:
- the optimal constant-modulus quadratic-phase bound in terms of covariance;
- a precise obstruction to a naive tangent-half-plane trial, even on large disks;
- the exact affine transplantation factor for ellipses;
- the thin circular-annulus limit, whose ratio to the field is at most 1/4;
- an exact certificate for all ellipses with semiaxis ratio at most 101/100 and
  0 < beta times the product of semiaxes <= 131.

Read SOURCE_GATE.md, PROOF.md, and ATTEMPTS.md. The ellipse certificate uses
credited rational disk data in witnesses.json. Reproduce all finite checks with
Python 3 and its standard library only:

    python3 verify.py > reproduced.json
    cmp reproduced.json verification.json

The frozen result has 1,435 assertions, including 60 disk endpoint signs, 60
source-table exact equalities, 60 ellipse endpoint signs, and 30 cross-checks
between Beta-function and monomial integration. Additional rational algebra
controls supplement, and do not replace, the written continuum proofs.

The cited numerical lower bound for the de Gennes constant is an external
published theorem. This script does not recompute that half-line spectral
certificate, prove the whole disk theorem at arbitrarily large field, or prove
the original universal conjecture.

Source documents and extracted texts are excluded. The public manifest lists
only this packet's files. No human peer review, formal verification, or historical
novelty is claimed. Independent review status is pending in this frozen author
packet; any subsequent review must be supplied separately without changing it.
