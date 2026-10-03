# Attempt 3 of 5: automatic symmetry inheritance

## Target and verdict

The cached report excludes pairs that are both left invariant on SU(2). That leaves a potentially misleading escape: could a left-invariant Lorentz metric have a non-left-invariant partner? This attempt closes that escape and proves a general compact-symmetry inheritance lemma. It does not establish that an arbitrary candidate metric has a useful isometry group.

## The global mobility input, with its exact hypothesis

Matveev–Mounoud, Corollary 5.2 of https://arxiv.org/abs/0909.5344, states that a non-affinely equivalent pair on a closed connected manifold of dimension greater than one has degree of mobility two, unless constant multiples of the metrics are positive-definite curvature-one metrics. This result applies to incomplete metrics. For an indefinite pair on S^3, affine rigidity excludes the affine alternative and signature excludes the round alternative. Thus the vector space S(g) of global self-adjoint solutions of the compatibility equation has dimension two.

## Lemma: compact connected isometries fix the whole solution space

Suppose D(g)=2 and K is a compact connected group acting by isometries of g. Pullback acts linearly on S(g), because the compatibility equation is natural under isometries. It fixes the solution I. Average any positive-definite inner product on the two-dimensional real vector space S(g) over K. The orthogonal complement of RI is a K-invariant real line. Its orthogonal group consists of ±1, and connectedness of K makes the action on that line trivial. K fixes I and its complement, so its representation on S(g) is the identity.

Consequently every compatible L, and every metric reconstructed by

gbar = |det L|^(-1) g(L^(-1)·,·),

is K-invariant. This conclusion uses a finite-dimensional representation, not averaging gbar itself. Averaging projectively equivalent metrics is generally not legitimate because the correspondence with solutions is nonlinear.

## Theorem: no compact-transitive candidate on S^3

Suppose one metric g in a proposed nonproportional indefinite projectively equivalent pair on S^3 admits a transitive compact connected isometry group K. Then D(g)=2 and the lemma makes L K-invariant. Therefore tr L is constant by transitivity. Compatibility gives ∇L=0, hence gbar is affinely equivalent to g. Affine rigidity on S^3 makes it a constant multiple, a contradiction.

In particular, no left-invariant Lorentz metric on SU(2) has an arbitrary nonproportional projectively equivalent metric, whether or not the partner was initially required to be left invariant. The standard left-translation action of SU(2) is compact, connected and transitive.

This implication is stronger in scope than applying only the statement about two invariant metrics. The published restricted result is Bokan–Šukilović–Vukmirović, https://arxiv.org/abs/1805.08240. The present proof instead obtains the second metric's invariance from the global mobility theorem.

## Reduction for a cohomogeneity-one attack

If g is invariant under the standard T² action on S³, then every projective partner is automatically T²-invariant as well. Thus it is legitimate to write both metrics in one-variable torus-invariant form, without separately assuming symmetry of the partner. This is useful for the next attempt, but it does not justify imposing a diagonal metric: off-diagonal orbit terms and radial-orbit terms remain possible.

## Failed extension and gap

A compact connected isometry group need not act transitively. Its invariant trace may vary on the orbit space, so the proof stops there. Moreover, neither the original question nor the preceding reductions guarantee any nontrivial isometry of an arbitrary candidate. A homogeneous or torus-invariant classification cannot be promoted to the full answer.

The symmetry inheritance argument is elementary representation theory combined with a published global theorem. No historical novelty claim is made.
