# Current reading entrypoint: audited partial MTW note

Updated 2026-10-03. Problem 30000997 / OWR-2042-006. **The original global problem remains unresolved after 5/5 author turns.** This is an AI-assisted partial research packet, not a global counterexample and not a novelty claim.

Read [CURRENT_READING_NOTE.md](CURRENT_READING_NOTE.md) before the historical turns. That note supplies the mandatory tensor-convention and off-cut-domain corrections, the equatorial uniqueness proof, numerical qualifications, and prior credit. It governs the reading of all frozen mathematical files. No sixth research turn has been undertaken.

The independent full audit accepted the local and equatorial mathematics subject to those clarifications. The corrections have now been added; their narrow re-review is pending. The audit is an internal mathematical check, not external peer review or priority certification. See [the full audit](audit/initial/INDEPENDENT_REVIEW.md) and [its correction list](audit/initial/CORRECTIONS.md).

## Retained partial result, with convention made explicit

For the smooth complete sphere metric

g=dx²+[cos x+(1/10)cos³x sin⁴x]²dy²,

Gaussian curvature is positive everywhere. At the uniquely minimizing equatorial pair p=(0,0), q=(0,π/2), the packet's tensor on source-tangent directions u=w=e1 has

S_packet=7/10−8/π²<0.

The endpoint tangent is Dexp_p((π/2)e2)e1=(2/π)∂x at q. Kim–McCann's cross-curvature convention in their Riemannian-products paper is twice this tensor:

cross_KM=2S_packet=7/5−16/π²<0.

Strict positivity on every nonzero null pair is proved at all non-antipodal equatorial pairs, and on a sufficiently small product neighborhood of the displayed pair. **A3w has not been established on the whole off-cut-locus domain of this sphere.** The local separation and equatorial slice therefore do not settle the global implication.

## Reading and provenance

- [Current reading note and corrections](CURRENT_READING_NOTE.md)
- [Current scoped status](CURRENT_STATE.json)
- [Corrected packet manifest](CORRECTED_PACKET_MANIFEST.json)
- [Historical source gate](PUBLIC_SOURCE_GATE.md), [final author summary](FINAL_RESULT.md), and TURN_1.md through TURN_5.md, read with the current note
- [State provenance](STATE_PROVENANCE.json), preserving the distinct historical local and remote state files

All 17 files covered by FINAL_AUTHOR_MANIFEST.json remain byte-for-byte unchanged, including the old README.md and FINAL_RESULT.md. They are frozen historical documents; this file is the current entrypoint. The original remote and local TURN_STATE.json files also remain preserved and are not claimed to have identical bytes. The new current status is in CURRENT_STATE.json. The corrections and audit do not reset or extend the five-turn budget.

Earlier Jacobi, angular-MTW, and surface-of-revolution methods are credited to Figalli–Rifford–Villani, *On the Ma–Trudinger–Wang curvature on surfaces*, §§2 and 6.1. The product obstruction is credited to Kim–McCann. Priority for the particular partial statements has not been established.
