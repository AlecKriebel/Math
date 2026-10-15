# Independent starting hypotheses

Recorded 2026-10-12 06:32:43 UTC after reading only the frozen release/PROOF.md, before inspecting historical audit conclusions, checker source, checker results, or peer reports. Completion estimate: 10% of this independent audit.

The target assertion is absence of a finite, same-order inverse Wasserstein constant for all probabilities on the intrinsic unit sphere. The antipodal point-mass argument appears immediately decisive for the unrestricted problem. Its hypotheses are n >= 2 and 1 <= p < infinity; normalized equators do not exist at n = 1.

The strengthened target is that, for n >= 3, fixed a in (0,1), and every fixed finite real p >= 1, the even positive densities 1 + a Re(x_1+i x_2)^k (k even) have unbounded input/output distance ratio. I regard the moment formulas, transport flow, and asymptotic exponent as hypotheses requiring independent reconstruction. Finite computations alone cannot establish this infinite-family conclusion.

Likely falsification points are a Hermitian rather than bilinear complex contraction, an off-by-one dimension in the equatorial moment, a radial Beta parameter error, an omitted tangential correction in the gradient energy, a sign error in the continuity equation, or cancellation of the wrong logarithmic exponents at real p. The strict denominator positivity and the circle boundary case also require explicit reasoning.

My independent mechanism will expand harmonics and projected equatorial polynomials in coordinates and integrate monomials by normalized Gaussian/Wick moments; this avoids importing either supplied checker or trusting its summaries. I will derive the exact tangential energy separately by projection and integration. I will also check the fixed-real-p asymptotic analytically, including p = 1 and the failure to extend its divergence argument to p = infinity.

Success criteria: derive a complete proof of the stated scope or exhibit a concrete mathematical gap; reproduce each original checker in normal and optimized Python against its frozen expected output; validate every listed manifest hash; and demonstrate that independent controls reject specific false alternatives, including under optimization. Publishable artifacts must contain only my authored reports, valid checker, and original run diagnostics. Copies, mutations, and foreign sources stay private and are excluded from the publication whitelist.

No source edits, Git or cloud actions, external contact, or other chat messages are authorized for this subtask.
