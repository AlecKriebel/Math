# Additive clarification of the audited construction

This note makes explicit several consequences and formulations recorded by the independent audits. It does not replace or alter any definition, lemma, structure map, or conclusion in the frozen proof. The relevant detailed arguments are in the [measure audit, Sections 3 and 9](INDEPENDENT_MEASURE_FACTORIZATION_REVIEW.md) and the [continuity/core audit, Sections 5–8](independent_reviews/CONTINUITY_CORE_REVIEW.md).

## 1. Sigma-finite prefix identity and two-way equivalence

The differential notation in Lemma 1 can be read as the following integral identity, valid for every nonnegative Borel function f on C:

∫ f(x) μ(dx) = ∫_C ∫_(R^k) f(p_k(v,y)) q_k(v;y) dv μ(dy).

This follows directly by Tonelli and a finite-dimensional Gaussian change of variables after splitting prefix and tail; no probability disintegration of an infinite-total-mass measure is required. Every q_k is finite and strictly positive, and its integral over v is one. Therefore both measures have exactly the same null sets. The canonical unitary from the product measure to μ multiplies by q_k^(-1/2).

Every concatenation map used in the proof has this **two-way measure-class equivalence**. A bijection nonsingular only in one direction would not suffice for a surjective L² unitary; that weaker assertion is not what is being used.

## 2. Full structural continuity

Let H be the global word Hilbert space and J=H⊛H. Let P_t be the interval-support projection and P_vac the vacuum projection. On the centered part of H put A_t=P_t−P_vac. Define Q(s,t) on J as the vacuum projection plus, on each alternating-word summand, the tensor product of A_s and A_t in that summand's color order. Its range is the embedded E_s⊛E_t.

Strong continuity of P and finite-word approximation give strong continuity of Q. Extend the structural unitary by zero outside its source fibre:

V(s,t)=u_(s,t)Q(s,t): J→H.

The fixed-concatenation argument in the proof gives strong continuity of V. Its initial projection is Q(s,t) and its final projection is P_(s+t). For p=(s,t) tending to p₀=(s₀,t₀), the identity

‖V(p)*h−V(p₀)*h‖² = ‖P_(s+t)h‖² + ‖P_(s₀+t₀)h‖² − 2 Re⟨h,V(p)V(p₀)*h⟩

shows strong continuity of the adjoints as well. Thus the structural maps and their inverses are continuous between the continuous source and target fields, including at zero. This operator argument does not require a single conull set supporting every real cut simultaneously.

## 3. Continuous subsystem and support-projection interpretation

The projection onto finite decreasing words and the projection onto all finite words are fixed orthogonal projections on H commuting with every P_t. Their restrictions consequently define continuous subfields F and K. Dilation preserves both projections, and the multiplication properties already proved make them continuous tensor and free subsystems, respectively.

In the free-hull argument, a set of finite tuples separated by rational partition cells means a full L² support rectangle in the appropriate free-word summand. Countably many such supports cover almost every finite tuple. The closed span of their support ranges is therefore the entire finite-word sector. Individual tuples are not being used as Hilbert-space basis vectors. Since K is closed and orthogonal to the infinite-word sectors, completion cannot add a grade-ω vector to that hull.
