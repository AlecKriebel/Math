# Research log: 2303003

All times below are 4 October 2026 UTC. Percentage estimates describe completion of this bounded source-verification/reconstruction goal, not probability of correctness.

## Initial source gate, 08:04–08:06 (20%)

Tried the exact catalogue URL first; retrieved the numerical record through the pinned public dataset after HTTP 403. Read the entire original Problem 3.3 and Update 3.3, with visual inspection of printed p.60. The update directly contradicts the generated catalogue/prior-report openness claim: the −K/2 bound had already been disproved. Read the live queue row, repository policy and actual repository tree/directory evidence. No prior exact attempt was found.

## Primary-source tracing, 08:06–08:11 (45%)

Distinguished the original half-plane conjecture from the later optimal-constant problem and from disk projection inequalities. Detected the 2018 update's mismatched book-volume reference. Located Hayman's 1974 *On a theorem of Tord Hall* through primary bibliographic metadata and opened the publisher's article record in the cloud research browser. The complete freely available p.25 preview gives the construction explicitly; p.26 is paywalled and was not read. Downloaded the offered first-page preview for precise local visual/source checking.

## Substantive turn 1: reconstruct Hayman's construction, 08:11–08:18 (100% author reconstruction)

Mechanism: express Hayman's example as the negative of a positive Poisson integral plus a half-plane Green function. Remove a short boundary interval around i; add a pole slightly inside the half-plane, with weight below the amount needed to restore the lost real-axis harmonic measure. The pole repairs all radii through the missing boundary interval.

Chose c=90, a=1/100, epsilon=10^-6. On the positive axis, compare artanh(q sin eta) to the removed interval's arctangent exactly, uniformly for all q in (0,1]. For radii in the closed gap, use the point r zeta, bound its Green value below by log 90>4, and bound the removed Poisson mass above by 5/(2c). For all other radii use the boundary limit on the positive imaginary axis. Cap the positive superharmonic function at 1 to obtain a finite, continuous, bounded subharmonic counterexample without changing positive-axis values.

PROOF.md now establishes every hypothesis and the strict counterexample at every positive real point. `verify.py` checks 16 exact rational/symbolic assertions, plus nine noncertifying numerical axis samples and six noncertifying gap samples. The singular radius and both endpoint radii are covered analytically. The numerical comparison uses both the direct source formula and a stable real-axis formula.

No unresolved proof step has been identified in the author's reconstruction. This is not independent verification. A fresh adversarial audit remains necessary before any remote publication. No source is used as a substitute for the inaccessible second-page proof, and no historical novelty is claimed.

## Stopping point

The exact catalogue target is already negatively resolved by prior work. Recommended `already_solved`, `1/5`. The separate optimal universal constant has not been determined. Further proof-search turns would silently change the target and were not undertaken.
