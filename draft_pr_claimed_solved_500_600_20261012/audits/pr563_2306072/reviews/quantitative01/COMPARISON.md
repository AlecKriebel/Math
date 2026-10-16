# Frozen audit comparison

The main independent derivation and executable certificate were written and
run before reading `original/.../independent-audit/INDEPENDENT_AUDIT.md`.
The prior audit was then read at the 2026-10-13T06:07:58Z checkpoint.

Agreement: exact coefficient extraction, area-theorem weights, tip gate,
quadratic-differential sign, negative double cover, square-root/inverse
remainders, division error, and all three angle conclusions. No quantitative
conflict or blocking defect was found. The factor 7/2 in the original function
value estimate requires the stronger existing bound
|H+H0|<=10/3+5*eta<7/2; the separately stated |H|<2 alone would be too
weak. We reconstructed this intermediate estimate independently.

New checks in this review: coefficient recurrence rather than the frozen
geometric-series extraction; a disk-2 reconstruction reducing the Z error
to <768*epsilon*eta; injectivity by integrating p-1 along straight segments;
Schwarz's lemma on V-t, proving Re Z>0 for the full punctured target disk;
and nine defect-specific mutation controls. These provide independent
mechanisms, though they still share the necessary classical mathematical
premises with the original proof.

The original negative controls are truthful but limited: a3-only and a4-only
perturbations fail to reverse at the selected two points, zero epsilon loses
strictness, and an oversized uncertainty loses certification. Those controls
do not show that an arbitrary malformed analytic argument is detected. A
wrong inverse first-order sign, for example, would still yield opposite
endpoint signs; our inverse-equation mutation catches that defect separately.

The author verifier replay passes all 56 checks and exactly matches the
frozen CHECKS.json. The prior audit's whole-proof PASS is not adopted as an
independent source-level conclusion by this quantitative family. Our scoped
PASS remains conditional on the classical source/global-support premises
being confirmed by the separately assigned family. A supplemental actual
near-infinity series check was reconstructed after comparison and is marked
as such in DERIVATION.md and quantitative_checks.py.
