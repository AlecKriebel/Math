# Exact-source and status gate

Checked 2026-10-04 UTC.

## Identity and scope

The requested catalogue URL was attempted first: https://www.unsolvedmath.com/problems/2304009 . The web reader could not retrieve it. The fallback was the immutable UnsolvedMath dataset revision `37e53eabe540fb458758e198be61634bd02ee008`, which is the revision recorded by the repository's live manifest. Its problems file matched SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`. Numeric ID 2304009 is AMR-022-4009, Hayman–Lingham Problem 4.9. The selected record is identical in the later cached dataset revision also inspected.

The isolated imported statement omits the earlier definition of `E_f^(n)` and the monic normalization. The surrounding primary source identifies the closed unit polynomial sublevel set; Erdős's original analysis section starts with a monic degree-n polynomial. The proof uses the monic class, so it also refutes any broader interpretation without that restriction. The exponent in the printed 2018 problem is genuinely `c^2`, checked in the rendered PDF; it is not a footnote or an OCR repair. The parameterization `1+c` ranges over the same thresholds as `1+c^2` when the positive parameter varies.

The imported record contains only the original degree-independent bound. The later update's proposed sublinear/subpolynomial counting estimates are not in that statement, and are not silently bundled into the result here.

## Primary-source chain

1. P. Erdős, *Some unsolved problems* (1961), §IV.1, printed pp.246–247: monic convention and original diameter bound. Retrieved from the Hungarian Academy repository and checked against the 2018 wording.
2. P. Erdős, *Extremal problems on polynomials* (1976), §3, printed p.349: the problem's proposer explicitly attributes the negative result with arbitrarily many near-diameter-4 components to Pommerenke; he then asks separate asymptotic questions.
3. Hayman–Lingham, arXiv:1809.07200v2 (2018), printed pp.74–75: Problem 4.9 is followed immediately by the negative status update and reference [644], Pommerenke (1961). Both pages were rendered and checked. Its original conjecture is already false according to this source itself.
4. L. Huang, arXiv:2509.11597v2 (2025), Theorem 1.1 and §2: a complete later capacity-and-Hilbert-approximation proof. The note added on p.2 expressly acknowledges Pommerenke's prior resolution and identifies this as rediscovery. The v2 was checked, rather than relying on the uncorrected novelty impression of the v1 abstract.
5. Bloom–Levenberg–Lyubarskii, *A Hilbert Lemniscate Theorem in C^2* (2008), introduction: confirms the exact one-variable Hilbert theorem used in the reconstruction. Both the publisher PDF and the 2006 arXiv preprint were checked.

The publisher endpoint for Pommerenke's 1961 paper returned an HTML bot-block page, including when trying its historical PDF link; these bytes were detected as non-PDF and were not treated as mathematical evidence. We do not claim to have read Pommerenke's original proof. Historical credit is instead supported by Erdős's primary retrospective, Hayman–Lingham's update, and Huang's explicit acknowledgment. The mathematical verification uses the retrieved later complete proof and the independently spelled-out reconstruction.

Huang's displayed energy kernel contains a typographical error (`1/log|w-z|`). The correct logarithmic kernel is recorded in PROOF.md. The proof uses exterior-map and Green-function capacity identities; it does not rely on that erroneous display. Open regions in informal capacity expressions are replaced here with their compact closures, and the separated pieces are specified as compact segments.

## Correction of the imported report

The linked upstream report labels the problem open as of the 2018 edition and says that no resolution was found. That status conclusion contradicts the explicit Update 4.9 in the very cited source. It is not a proof attempt and supplies no mathematical obstruction. This package records the correction without redistributing that report.

## Repository duplicate and budget gate

Live main at the check was `bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b`. Row 574 was queued at 0/5. The corresponding numeric attempt directory returned 404; code and branch searches for `2304009` returned no matches. PR searches for the numeric identifier, AMR code, Function Theory 4.9, Pommerenke, and Huang's arXiv identifier found no relevant prior attempt. A broad query mentioning 511 produced an unrelated PR numbered 511, not a mathematical duplicate. No listed related-target group contains 2304009. Dataset searches did not identify a separate EP-511 record in the inspected snapshot; the external Erdős #511 is the same classical question.

This is one substantive source-verified reconstruction, so the proposed count is **1/5**, not 0/5. The public classification is **already_solved**, not a new claimed solution. No remote write was performed by the author. The only proposed queue changes are this row's Status and Turns cells; Findings and all other row content remain unchanged.

## Remaining boundary

The exact original conjecture has been negatively resolved. The source's additional asymptotic questions, precise all-sufficiently-large-degree formulation, effective coefficient construction, and best degree-versus-component bounds are not settled by this package. No claim about their current complete literature status is made.
