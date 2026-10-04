# Corrections and non-corrections

## C1 — Required certification correction

Affected frozen file: `verify_controls.py`; affected interpretation:
`control_results.json` and `control_results_high_precision.json` as decimal
endpoint certificates.

The comment in `bracket` says interval endpoint strings are outward-safe.
The helper is unused, and direct `str(...)` calls serialize the actual results.
In mpmath 1.3.0, that is a nearest-rounded display. Its extra digits do not
turn nearest rounding into directed rounding.

Reproducible witness: set iv.dps=40 and form y=(2+iv.sqrt(8))/2. Parse its
displayed lower endpoint as an exact decimal rational and compare it with
the exact rational represented by y._mpi_[0]. The displayed value is greater.
See the complete exact witness in `verification_results.json`.

Required remedy: use directed decimal export or exact binary-rational endpoint
export. The separate `verify_controls_outward.py` is a corrected, version-pinned
variant. It converts (sign, mantissa, exponent, bitcount) to a Fraction, rounds
the lower decimal down and upper decimal up, and rejects nonfinite endpoints.
Every result interval uses this serializer. The mathematics and event engine
are unchanged. Its two corrected output files supersede the originals only
for the outward-endpoint certification claim.

Suggested documentation sentence:

“Sign assertions are performed on in-memory interval values. Exported decimal
endpoints are separately rounded outward by exact rational arithmetic.”

This issue does not change the eleven signs or invalidate the stationary-Wilton
theorem. The independent integer-interval certificates additionally establish
the finite exclusions without mpmath.

## C2 — Optional clarity, not a defect

The parity squeeze can be shortened. From S_(2k+1)≤S_(2k),
liminf S_(2k+1)≥D and limsup S_(2k)≤D, both subsequences already converge
to D. The extra inequality S_(2k−1)≤S_(2k) is true but not needed.

## Claims that need no correction

- Positive odd-K and negative even-K BM secants; their availability at every irrational
- The x>1 composition A(1/t)=A(t)/t and its positive Υ coefficient
- Derivative identity (14), with the rational point x=1 explicitly excluded
- Oriented stationary increment formula (11), for both signs of h
- Event-cell primitive, unambiguous interval comparisons, and tail bound 1/T
- Positive reciprocal derivatives m=1,…,9; negative ones m≥10
- No full resolution, no novelty claim, and the stated two-sided stationary gap

The frozen originals are unchanged. This document is an audit correction
record, not an authorization to change or publish them.
