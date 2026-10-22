# Exact deductions for connected sum ropelength

## Scope and conventions

Let K be a tame knot or finite link type in Euclidean three-space. For a
rectifiable embedded representative Γ, use thickness τ(Γ) equal to reach,
which is the radius of the embedded normal tube. Define

R(K) = inf { Len(Γ)/τ(Γ) : Γ represents K, τ(Γ)>0 }.

For links, length means the sum of component lengths. A link connected sum
includes a choice of one component of each link and an ordinary connected-sum
band in a separating-ball construction. No claim is made for arbitrary band
sums. Knot types are the smooth/tame types, although minimizing representatives
may be only C^{1,1}. Positive thickness implies this regularity; its curvature
is at most 1/τ almost everywhere. These facts and attainment of the infimum
are established in [CKS02], Lemmas 1, 2, 4 and Theorem 7. Attainment is not
needed in the arguments below: arbitrarily close competitors suffice.

## Proposition 1  The unknot value and the scope obstruction

For the unknot U, R(U)=2π. For every tame knot or finite link K, connecting
an unknot to a chosen component gives K#U=K. Consequently its exact
ropelength saving is 2π.

Proof. A round circle of radius r has length 2πr and reach r. Indeed, any
point at distance less than r from the circle lies off its perpendicular
axis and has a unique nearest point; the center has every circle point as
a nearest point at distance r. Thus R(U)≤2π.

For the lower bound, scale any positive-thickness competitor to thickness
one. Its arclength parametrization γ is C^{1,1}, is periodic of period ℓ,
has |γ'|=1, and has |γ''|≤1 almost everywhere. Fenchel's total-curvature
inequality for a regular smooth closed curve gives total curvature at least
2π; see [Milnor50]. Its application to this regularity can be made explicit:
periodically mollify γ. The smooth derivatives γ'_η converge uniformly to
γ', so m_η = min |γ'_η| tends to 1 and is positive eventually. Convolution
also gives |γ''_η|≤1. The total curvature of γ_η is bounded by

∫_0^ℓ |γ''_η(t)| / |γ'_η(t)| dt ≤ ℓ/m_η.

Hence 2π≤ℓ/m_η, and letting η tend to zero gives ℓ≥2π. This applies
to every positive-thickness closed competitor, not just to the circle or
to an assumed minimizer. Zero-thickness competitors do not have finite
ropelength. Therefore R(U)≥2π.

The unknot is the identity for ordinary connected sum. Substitution into
the saving R(K)+R(U)−R(K#U) gives 2π. In particular, the literal part (a)
applied to U#U would demand

2π ≤ 2π+2π−(4π−4) = 4,

which is false since π>2. Equivalently, 4π−4 exceeds the available saving
2π by 2π−4. This is an elementary formulation obstruction. It does not
refute a version whose two knot summands must be nontrivial. □

Corollary. A saving c valid for all knot types including U must satisfy
0<c≤2π. Conversely, if some c₀>0 works for every pair of nontrivial
knots, then min(c₀,2π) works for every pair of knots, by handling a pair
with an unknot separately. Thus the existence question in part (b) is
equivalent in these two knot domains. The unknot calculation leaves that
existence question open.

## Proposition 2  Split spectators cancel exactly

For a split union A ⊔ B of tame finite link types,

R(A ⊔ B) = R(A)+R(B).

Proof. Normalize any representative of the split union to thickness one.
Deleting components cannot decrease their thickness: this follows, for
example, from the three-point formula for thickness in [CKS02]. Each
sublink has length at least its own minimum ropelength. Summing gives
the lower bound.

For the upper bound, choose thickness-one representatives with lengths
within ε of their respective infima and place them in disjoint distant
balls, with their mutual distance strictly greater than two. Each has
reach at least one. Their union has reach at least one as well: a point
at distance less than one cannot have nearest points in both sublinks,
since those points would be less than two apart. Within one sublink the
nearest point is unique. The total length is at most R(A)+R(B)+2ε.
Let ε tend to zero. The distant placement represents the split union. □

Suppose L_i = A_i ⊔ B_i is split and the designated summing component
lies in A_i. Using the ordinary separated connected sum,

L_1#L_2 = (A_1#A_2) ⊔ B_1 ⊔ B_2.

Proposition 2 gives the exact cancellation identity

R(L_1)+R(L_2)−R(L_1#L_2)
= R(A_1)+R(A_2)−R(A_1#A_2).

Thus a universal saving question for links reduces to the nonsplit blocks
containing the selected components; any split spectator blocks cancel.
If a selected block is U, the saving is exactly 2π. In particular, simply
requiring the whole links to be nontrivial does not repair part (a):
take L_1=J_1⊔U and L_2=J_2⊔U for nontrivial knots J_i and sum their
split U components. A link formulation must specify the summing components
and address this case. This is a scope correction, not progress on the
inequality for two nontrivial nonsplit selected blocks.

## Proposition 3  What a controlled splice must certify

Fix the two summand types and let S=R(K_1)+R(K_2). Let ε≥0,
0≤δ<1, and s be real. Suppose thickness-one representatives have total
length at most S+ε, and a specified surgery produces an embedded
representative Γ of the required connected sum with

Len(Γ) ≤ S+ε−s,     τ(Γ) ≥ 1−δ.

Then

R(K_1#K_2) ≤ (S+ε−s)/(1−δ)
= S − (s−ε−δS)/(1−δ).

Proof. The infimum R(K_1#K_2) is at most the ropelength of Γ.
Divide the length bound by the positive thickness bound and simplify. □

Therefore this certificate proves a target saving c exactly when its
upper bound is at most S−c, or equivalently

s−ε−δS ≥ c(1−δ).

When S>c this is equivalently δ≤(s−ε−c)/(S−c). The condition is for
this particular sufficient upper-bound certificate; it is not a necessary
condition for the conjecture itself. A fixed positive loss δ in reach and
a fixed raw length saving s do not by themselves provide a uniform
positive saving as S varies. For a given fixed S, a construction retaining
a positive uniform s while ε and δ tend to zero would avoid this problem;
no such construction for arbitrary summands is provided here.

The open geometric step is to find compatible exposed arcs, join them with
controlled tangents and curvature, prove the output has the required
connected-sum type, and bound all nonlocal contacts while retaining the
claimed saving. A bound on curvature alone is insufficient: [CKS02],
Lemma 1, also includes the doubly critical self-distance in thickness.
Existence of minimizers supplies neither the exposed arcs nor these bounds.

## References

[CKS02] Jason Cantarella, Robert B. Kusner, John M. Sullivan, On the Minimum
Ropelength of Knots and Links, Inventiones Mathematicae 150 (2002), 257–286.
https://arxiv.org/abs/math/0103224
https://doi.org/10.1007/s00222-002-0234-y

[Milnor50] J. W. Milnor, On the Total Curvature of Knots, Annals of
Mathematics 52 (1950), 248–257. Introduction and Theorem 3.4 (printed p. 254).
https://people.reed.edu/~ormsbyk/milnor-total-curvature.pdf
https://www.jstor.org/stable/1969467
