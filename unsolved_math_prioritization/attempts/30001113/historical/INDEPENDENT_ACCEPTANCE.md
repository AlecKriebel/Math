# Independent acceptance report

Date: 9 October 2026 UTC.

## Decision

**ACCEPTED: complete counterexample to the literal unrestricted local-action fibre-product question.**

The proof uses k=F4, G=(F4,+), N=F2, and rho(a)(t)=t/(1+at). Its two decisive facts have been independently proved:

1. A nonzero first-order quotient deformation is sent to the basepoint by every natural transformation from D_Q to a prorepresentable functor. This follows from explicit identity-reducing conjugacy over k[e]/e³ and naturality, without a hull substitution or an infinite Yoneda assumption.
2. The tangent restriction from D_G to D_N is injective, because Theta^N is equivariantly y k[[y]]∂_y and H¹(Q,Theta^N)=0 by a complete formal-series calculation.

Consequently the point (0,v) belongs to every proposed target fibre product but has no preimage. Formal smoothness fails already for k[e]/e²→k. The requested tangent-space condition on F does not repair the example.

## Source and hypothesis checks

- OWR pp.3038–3040 and 2011 Question 4.4 do not assume that D_N or D_Q is prorepresentable.
- Their conditional obstruction-space results state those assumptions separately.
- The field, characteristic, faithful action, normal subgroup, Artinian W(k)-category, nilpotent constant terms, and actual set-valued deformation equivalences all match the source definitions.
- The map out of D_Q alone is forced to kill v. No map out of D_N^Q is extended to D_N.
- The same proof covers the introductory and refined formulations; they are not separate results.
- No conclusion is claimed for an amended question imposing prorepresentability of D_N and D_Q.

## Corrections and validation

The original mathematical proof was correct. A separate proof-precision patch clarifies which inverse of the coordinate change appears under the source's reversed substitution-composition convention. It does not change the equivalence class or any mathematical conclusion.

The original auxiliary checker used assertions that disappear under optimized Python. A separate corrected checker uses explicit exceptions. Both it and the independent checker pass normally and under -O/-OO. Meaningful mutants fail in all modes after correction. Frozen-input write attempts were actually denied under nonroot UID 1000; original and frozen hashes remained unchanged.

The independent mathematical audit, corrected proof/checker, exact checker, validation results, and manifests are separate deliverables. Third-party source PDFs, source-body text, rendered source pages, and private coordination files are excluded from the publication-ready artifact list.

## Limits

This accepts mathematical completeness for the statement as printed. It is not a guarantee of novelty, exhaustive later-literature coverage, journal acceptance, or formal proof-assistant certification. The 2009 involution conjugacy is explicitly credited as prior work.
