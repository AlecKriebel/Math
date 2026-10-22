# Reviewed de Gennes partial results

**Problem 30005598 / OWR-14297736-004 remains unsolved after 5/5 attempts.**

Start with [the exact source gate](public/SOURCE_GATE.md), [the proofs](public/PROOF.md),
and [the complete independent audit](audit/AUDIT.md).

The strongest certified consequence is

    lambda(E_a,b,beta) < Theta_0 beta
    for 1 <= a/b <= 101/100 and 0 < beta*a*b <= 131.

The audit passes for this scoped result and the other stated partials. The
published half-line enclosure implying Theta_0 > 5901/10000 is an external
theorem; its numerical implementation has not been independently recertified.
The general smooth-domain question remains unproved and unrefuted here.
Lena--Sundqvist's May and September 2026 disk results are credited prior work.
No historical novelty, formal-verification, or human-peer-review claim is made.

## Angular normalization clarification

The quantities N and q_s in Section 5 of the frozen proof are radial integrals.
With the unnormalized angular factor exp(i m theta), the full two-dimensional
mass and energy are 2*pi*N and 2*pi*q_s. Equivalently use the normalized angular
factor exp(i m theta)/sqrt(2*pi); then they are exactly N and q_s. This common
factor cancels in every Rayleigh quotient and changes no sign or certified
inequality. The clarification addresses the audit's nonblocking notation point
without changing any frozen author or audit byte.

## Reproduction and preservation

From this directory, with Python 3 and its standard library:

    python3 public/verify.py > author-reproduced.json
    cmp author-reproduced.json public/verification.json
    python3 audit/independent_controls.py > independent-reproduced.json

The author run has 1,435 assertions. The independent portable run has 467;
its optional separate-source comparison has 588 and reproduced the included
independent-controls.json exactly. The optional source TeX is not distributed.

All 11 author files and all 9 audit files are preserved byte-for-byte, including
their manifests. Historical pending-review/remote-write statements inside the
frozen author packet describe its creation state; this publication wrapper and
the separate audit give the later review outcome. PUBLICATION_MANIFEST.json
binds the combined release files and this additive clarification.

The repository change is limited to this packet and the target row's status,
turn count, and previously blank Findings cell. Existing queue header, unrelated
rows, and links are preserved. Source PDFs, source archives, extracted articles,
screenshots, raw catalogues, and private context are excluded. Draft only.
