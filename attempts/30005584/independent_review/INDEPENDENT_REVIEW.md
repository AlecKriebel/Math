# Independent full review: expander degree30005584

**Verdict: PASS_SCOPED_PARTIALS. Original question unsolved,5/5.**

No mandatory mathematical correction is required. All five frozen author turns
are valid with their stated geometric and weighted-domain hypotheses. Neither
the unrestricted expander degree of D³×S¹ nor the boundary-connected-sum degree
law is established. The explicit final gap is substantive, not a missing finite
calculation. No historical novelty is certified.

This review binds FROZEN_MANIFEST.json SHA256
`26ed40c1c0682d14c74fa2c2a94d7ba0cb247dde9423dd8d867cb5c4aea998a5`,
PROOF_COLLECTION.md SHA256
`d942a54c053ed9f8f00346609e2fe06c8093e31726b04f47be3e1cbc282fd919`, and
TURN_5.md SHA256
`e53add5ae5c08d5182067d26bd2d9acd998c33ec86c7c0ac48bc327df268cf19`.

All39 author entries and six complete primary PDF hashes match. Every historical
manifest verifies. The five author checker outputs replay byte-for-byte in a
separate copy, with88,070 /36,465 /9,041 /30,344 /13,080 assertions. A separately
written checker passes4,538 exact controls, including a general base-geodesic
warped connection calculation rather than only the author's radial substitution.
The infinite analytic arguments were audited as proofs, not inferred from those
finite checks. I did not contribute to the author route or edit frozen files.

## 1. Source, normalization and exact original scope

The original OWR2023 contribution and its2025 repetition ask both for a relation
under **boundary** connected sum and for deg_exp(D³×S¹). I inspected the actual
original question image and read the surrounding contribution. The relevant
expanders are gradient Ricci solitons; no mean-curvature-flow degree is being
substituted. Half-balls at the boundaries are removed, not interior balls.

The full Bamler–Chen v3 source defines an ensemble using a smooth4-orbifold with
isolated singularities, a regular3-dimensional end, and a possibly infinite
smooth cover with H₂=0 and torsion-free H₁. The compact boundary must admit
positive scalar curvature. The cone and gradient soliton locus use nonnegative
**scalar** curvature. Definition3.8 fixes the vector field at infinity and the
C² asymptotic requirements, modulo compactly supported diffeomorphisms. The
finite-dimensional localized degree is not an ordinary Banach-manifold degree
of a presumed smooth gradient locus. Theorem10.49's signed index formula is
conditional on full kernel-freeness over the cone. The packet preserves these
conditions and the k*>=30 degree regularity threshold.

Rajan's published2026 paper computes the cohomogeneity-one degree. Its
Theorem1.1 and Section9 do not compute the unrestricted degree. The complete
thesis comparison chapter explicitly leaves equality unproved; I visually
inspected printed p.66 and read the surrounding argument. The two-parameter
profile family, properness and restricted count remain credited published
inputs. Its standard-action classification is not silently promoted to a
classification of all unrestricted fibers or of every possible lifted action.

The normalization conversion g_B=2g_R, f_B=f_R is correct: the connection,
(0,2) Ricci and Hessian remain unchanged by constant scaling. The new radial
coordinate is sqrt(2)r_R, slopes remain unchanged and f''(0) is divided by2.
The initial-coordinate rescaling has positive determinant but does not establish
the missing ambient orientation comparison. For the product link the scalar
cone condition is exactly b²<=1/3. Bamler–Chen Lemma3.19 transfers nonnegative
scalar curvature from such a cone to the gradient soliton once it is placed in
the actual moduli category. No curvature-operator positivity follows.

## 2. Turn1: conditional comparison and finite-dimensional obstruction

The proper equivariant gradient map on trace-free symmetric3×3 matrices is
valid. Cayley–Hamilton gives tr(A⁴)=tr(A²)²/2 and hence
||A²-tr(A²)I/3||²=||A||⁴/6. This proves properness and its single zero fiber.
The map is even on a5-dimensional real space, so composition with minus the
identity reverses domain orientation while leaving the map unchanged; its
integer degree is zero. Adding the trivial and rotation factors produces the
stated effective SO(3)×SO(2) action, with fixed-locus degree one and a full
critical fiber. The trace-gradient statement and local determinant sign checks
also agree. These are not geometric Ricci-soliton counterexamples.

For a full regular value of a proper equivariant map, the fiber is finite and
a connected group fixes every point in that fiber. The derivative preserves
fixed and normal representation spaces; the determinant factorization gives
the stated conditional mod2 and signed comparison. Fixed-slice regularity is
insufficient, exactly as the constructed example demonstrates. The mod2
geometric implication under(A)-(C) is valid via the full regular-value count and
the identified entire restricted fiber. Normal signs and compatible ambient
orientation are additional requirements for an integer identification. They
are not supplied by connectedness or by a restricted ODE degree.

## 3. Exact independent warped-tensor reconstruction

Here is the reconstruction used to check all signs and factors. At a base point
choose a g_B-geodesic orthonormal frame e_i, i=0,1,2, and e_3=a^(-1)∂θ. Write
L=dlog a and T=a^(-1)Hess_B a. The extra connection coefficients are
∇_3e_i=L_i e_3 and ∇_3e_3=-sum L_i e_i; base derivatives of e_3 vanish.
The mixed curvature tensor has R_(3ij3)=-T_ij, in the convention Rm(g)=Ric.

For h=e³⊙eta, with no half in the symmetric product, the exact contractions are

    |∇h|²=2|∇^B eta|²+2|L|²|eta|²+6<L,eta>²,
    <Rm(h),h>=2<T eta,eta>.

These imply the author's radial formula, including the8A² radial term and the
minus4C curvature term. For an even tensor h=S+q(e³)², the extra derivative
norm is2|S(L,.)-qL|² and the curvature cross contribution is
-2q<T,S>. Expanding Q leaves the cross term
4q<T-L⊗L,S>=4q<Hess_B log a,S>. Thus the coefficient4 and its sign in the
Schur complement are confirmed independently.

The fresh checker constructs the full connection matrices and mixed curvature
array for general base vectors and symmetric Hessians, rather than assuming
that only one Hessian component is nonzero. It verifies both contractions and
the even Hessian cross term on independent rational controls.

## 4. Turns2–3: circle parity and the full odd Hodge sector

The nonzero real circle weights occur in two-dimensional rotation summands,
so their contribution to the finite negative-space dimension is even. This
says nothing about whether a nonzero-weight kernel exists. The text preserves
that distinction. The coexact sphere sector is reducing: Hodge splitting is
orthogonal for the radial and L² pairings, and the sphere rough Laplacian differs
from the Hodge Laplacian by a scalar Ricci term. Its cross term with the radial
component integrates to zero. The resulting nonnegative form has no zero vector
because S² has no nonzero parallel one-form.

For the whole odd sector put eta=a alpha. Its L² density becomes a³e^(-f),
including the constant factor2 times the circle volume. The rescaling can be
checked invariantly: in that density,

    div_mu(L)=Delta_B log a+<3L-df,L>=lambda+2|L|².

The circle soliton equation used here is tr(T)-<df,L>=lambda. Integrating the
rescaling cross term gives the zeroth-order tensor

    -2T+3L⊗L-lambda g_B = Ric_B+Hess_B(f-3log a).

The weighted one-form Weitzenböck formula with delta_F=delta+i_(grad F) therefore
gives exactly the nonnegative Hodge form stated in Turn3. The sign of the drift
and the factor a³ both check. The unitary normalization divides U by the square
root of twice the circle volume.

The closure argument is sound. Curvature is bounded, so a shifted tensor form
norm is equivalent to weighted H¹. Smooth compactly supported tensors are a
core, as also explicitly used in Bamler–Chen's spectral proof. Averaging circle
symmetries preserves that core. Cutting away the smooth codimension3 core has
error O(epsilon) for bounded smooth tensors; infinity is handled by weighted
H¹ and L² tails. The equality of the nonnegative forms on the core identifies
their closures. It does **not** require delta_F, whose drift is unbounded, to be
a bounded operator on ordinary H¹.

For the kernel, elliptic regularity supplies a smooth alpha, and Q=0 gives
dalpha=delta_F alpha=0. On the genuine smooth baseR³ it has a global smooth
potential psi. No L² assumption on psi is made. The weighted Dirichlet energy
is finite. Spherical projection yields (pu')'-j(j+1)pb^(-2)u=0, with
p=a³b²e^(-f). Smoothness at the origin makes the integration boundary term
vanish. For j>=1 the outer cutoff error is bounded by the tail of the angular
energy, using b comparable to r. It tends to zero, forcing that coefficient
to vanish. For j=0 the constant pu' vanishes at the origin, leaving only a
constant potential and zero one-form. The argument correctly uses the
one-ended R³ base; it would not be valid on an arbitrary two-ended interval.
Thus no negative or zero odd-sector modes remain.

## 5. Turn4: closed Schur reduction and compactness

The even scalar block H has form integral(|dq|²+2|dlog a|²q²)dmu, with
mu=a e^(-f)dvol_B. Its zero form forces a constant, which cannot be L² because
the conical volume and bounded-above f give infinite measure. The Hessian
multiplication R is bounded for each fixed soliton: smoothness handles the core
and the actual conical curvature/profile estimates give quadratic decay at
infinity. Likewise dlog a is bounded. Base curvature is bounded as a subblock
of the full warped curvature.

Absence of a zero mode alone would not prove a spectral gap. The text correctly
adds compactness. I read Proposition5.38 and its proof: the weighted gradient
inequality and proper potential control tails; local Rellich compactness then
gives compact embedding of the weighted form domain into L². Restriction to
the scalar subspace gives compact scalar form embedding because its form is
exactly the scalar restriction. This subspace need not be reducing for that
argument. Hence H has compact resolvent and a positive inverse. The source's
Claim5.43 heading reverses the embedding arrow typographically, but its proof
and the author's use are the actual H¹-to-L² compact embedding.

Completing the square gives a bounded invertible **form congruence**, not a
unitary spectral equivalence. R and H^(-1) are bounded, and H^(-1)R maps into
the scalar operator domain, so it is bounded in the scalar form norm as well.
The effective correction is L²-bounded; Q_eff stays closed and has compact
form embedding. Projection of a negative subspace and the minimizing graph
prove exact inertia equality. Polarizing the form and varying q gives
q=-2H^(-1)RS and the precise weak kernel correspondence. The original local
elliptic system then gives smooth representatives. The negative sign of the
Schur error is essential and is retained.

## 6. Turn5: exact uniform scalar gap and spherical inverse inequality

The circle soliton equation gives Delta_f^B a=lambda a. The identities for
Delta log a show Delta_(f-log a)log a=lambda exactly, including through the
smooth origin. For w=a^(-c), direct differentiation gives
Hw/w=c lambda+(2-c²)|dlog a|². Taking c=sqrt2 gives the exact positive formal
solution at sqrt2 lambda.

For compactly supported q the ground-state transform follows by ordinary
weighted integration by parts. Extension by form closure proves
H>=sqrt2 lambda and the inverse bound. No L² claim for w is required. Equality
in the closed transform would imply q/w constant. The density of w²mu is bounded
below by a positive multiple of r^(3-2sqrt2), which is not integrable at infinity.
Thus equality has no nonzero L² eigenvector. Compact resolvent for each fixed
soliton then makes its first eigenvalue strictly above the displayed threshold.
Only the non-strict bound is uniform over the family, as stated. At lambda=1/2
the threshold is1/sqrt2 and inverse norm bound sqrt2.

The secondary bound A<=sqrt(lambda)tanh(sqrt(lambda)r) follows from the sourced
monotonicities and scalar differential comparison. It is not a Hessian or
curvature-operator bound. The general angular decomposition yields the extra
potential j(j+1)/b² on the actual smooth degree-j domain. This singular polar
potential adds no artificial boundary at the base origin. Closure controls
its angular integral; the reciprocal potential is bounded and vanishes at the
origin for j>0.

The inverse inequality is valid by the variational formula and the pointwise
square. It neither assumes that H and V commute nor that V^(-1)z belongs to
the H form domain. Equivariance makes R map a tensor degree-j isotypic sector
into the same scalar degree or zero, so the refined local Schur bound applies
to the stated tensor sectors. The associated positive tensor criterion is only
sufficient; its sign for all actual profiles has not been established.

## 7. Final scope

The partials remove the odd invariant sector and reduce the remaining even
sector to an explicit form with a uniformly controlled scalar inverse. They do
not exclude nonzero-circle Fourier kernels, classify all full fibers, produce
full regular symmetric targets, identify the ambient orientation, or establish
the sign of every remaining nonspherical tensor mode. There is no valid
boundary-connected-sum gluing/degree theorem in the packet.

The original target therefore remains **unsolved5/5**, and the complete partial
manuscript is suitable for publication only with that disposition and its
published source credits. No further author research turn is supplied by this
review. The seven top-level portable files constitute the review packet;
reading copies and the author replay directory are excluded.
