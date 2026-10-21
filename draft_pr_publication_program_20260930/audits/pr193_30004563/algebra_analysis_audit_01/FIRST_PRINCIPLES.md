# First-principles reduction

Derived 2026-10-15 09:18 UTC from the primary definition, before inspecting submission proof.

Let b_i = |A_i-A_(i+1)|^alpha, indices modulo 6. The incoming quads A1 A2 A3 O, A3 A4 A5 O, A5 A6 A1 O impose

|O-A1|^alpha-|O-A3|^alpha=b1-b2,
|O-A3|^alpha-|O-A5|^alpha=b3-b4,
|O-A5|^alpha-|O-A1|^alpha=b5-b6.

The outgoing quads A2 A3 A4 X, A4 A5 A6 X, A6 A1 A2 X impose

|X-A2|^alpha-|X-A4|^alpha=b2-b3,
|X-A4|^alpha-|X-A6|^alpha=b4-b5,
|X-A6|^alpha-|X-A2|^alpha=b6-b1.

Each triple telescopes. Its necessary boundary compatibility is b1+b3+b5=b2+b4+b6. Under that identity, any two equations imply the third, in either triple. For alpha=16 all these are polynomial identities in squared distances raised to power 8, without fractional powers or squaring operations: exact satisfaction is equivalent, with no algebraic extraneous roots introduced by the reduction itself.

Independent analytic expectations: a symmetric even-focus arrangement can produce pairs of reflected outgoing intersections and an axial intersection. Five intersections require two nonzero reflected pairs and the axial point. Strict convexity of the distance-power potential in a scalar boundary variable implies unique positive boundary roots only after endpoint values straddle the target; convexity alone does not guarantee uniqueness globally. If a scalar IVT uses the positive root, prove continuity by monotone inverse/implicit-function reasoning, including parameter endpoints. For large-distance tests, evaluate differences by factorization or exact arithmetic to prevent cancellation from manufacturing signs.

Primary source: Melotti–Ramassamy–Thevenin, arXiv:2003.08941v2, Definition 2.1, Definition 2.5, Theorem 4.7 and Remark 4.8. The realization definition permits crossings; the six boundary points must be distinct and each alternating triple noncollinear.
