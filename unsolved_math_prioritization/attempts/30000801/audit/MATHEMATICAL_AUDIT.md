# Independent mathematical audit: ID 30000801

Audit date: 2026-10-06 UTC. This is an independently authored analysis of the
frozen conditional result, not a proposed resolution of the original problem.

## Verdict and exact scope

The conditional local theorem in the frozen `PROOF.md` is valid as stated.
No mandatory mathematical correction was found. Its hypotheses are substantially
stronger than the original Navier problem. In particular, the archive does not
prove strong quantization at arbitrary energy, boundary exclusion, or a complete
bubble-tree classification. The original target remains unresolved by this work.

The equation is Δ²u_k = λ_k u_k exp(2u_k²) in dimension four, with λ_k positive
and spatially constant, λ_k → 0, and u_k = Δu_k = 0 on the domain boundary.
The convention is Δ = Σ∂². The nonlinearity is neither λ_k u_k² exp(2u_k²)
nor λ_k u_k² exp(2u_k). The total energy is λ_k∫u_k²exp(2u_k²), and the
quantum is Q = 16π². These distinctions matter for the primitive and Pohozaev
constant.

## A. Bubble and fundamental-solution normalizations

For η(r) = −log(1+r²), the radial operator is
Dφ = r⁻³(r³φ′)′. Direct differentiation gives

Dη = −4(r²+2)/(1+r²)²,
D²η = 96/(1+r²)⁴.

The radial integral is
96 · 2π²∫₀∞ r³(1+r²)⁻⁴dr = 16π².
Thus the source normalization λ_k r_k⁴M_k²exp(2M_k²)=96 is consistent.
For u_k = M_k + η_k/M_k, the exponent difference is exactly
2u_k²−2M_k² = 4η_k+2η_k²/M_k². On each fixed rescaled ball, local
uniform convergence gives the asserted energy density limit. The integration
order must remain k → ∞ followed by the rescaled radius R → ∞. No convergence
on an expanding rescaled ball is inferred.

For w = A log(1/r), Δw = −2A/r² and ∂_rΔw = 4A/r³. Hence
∫∂B_r ∂_nΔw = 8π²A. There is no extra point mass in Δlog(1/r):
its first-order flux tends to zero like r². Applying Δ once more gives
Δ²[(8π²)⁻¹log(1/r)] = δ₀ with the chosen sign convention.

## B. The complete Pohozaev identity

Let X = x−a, z = X·∇v, and w = Δv. Define the vector field
J = z∇w − w∇z + (X/2)w².
For smooth v in dimension d,

∇·J = zΔ²v + (d−4)w²/2.

Indeed, the gradient cross terms cancel, Δz = 2w+X·∇w,
and the last divergence contributes dw²/2+wX·∇w. Integrating proves

∫B_r (X·∇v)Δ²v = P_r(v)+(4−d)∫B_r(Δv)²/2,

where P_r is exactly the three-term boundary form in the author proof.
In d=4, with F_k(t)=λ_k(exp(2t²)−1)/4 and F_k′(t)=λ_k t exp(2t²),

P_r(u_k) = r∫∂B_r F_k(u_k) − 4∫B_r F_k(u_k).

All three boundary terms and the negative bulk-primitive sign are necessary.
The artificial sphere has no Navier boundary condition. The proof does not set
u_k, Δu_k, or their derivatives to zero there.

Regularity is adequate: smooth classical u_k in a neighborhood of the closed
ball suffices for the exact integrations; C³ convergence suffices for passage
in P_r because its highest derivative is ∂_nΔu_k. No passage to the limit in
fourth derivatives is used.

## C. The local limiting mass identity

The assumptions require c_k → ∞ and, away from a,

c_k u_k → U = A log(1/|x−a|)+h in C³_loc,
A = m/(8π²), h ∈ C³(B_ρ(a)).

They also require the same finite primitive mass n₀ for every sufficiently
small fixed ball:
lim_k 4c_k²∫B_r F_k(u_k) = n₀.
Here n₀ is a scalar mass, distinct from the outward normal n; m is the source
coefficient used to normalize the logarithmic singularity.

For each fixed r, c_k u_k is uniformly bounded on the sphere. Taylor's theorem
therefore yields c_k²F_k(u_k) = (λ_k/2)(c_k u_k)²(1+O(c_k⁻²)) → 0
uniformly. The constants may depend on r. This step uses λ_k → 0 and does not
require λ_k c_k² → 0. Taking k → ∞ first gives P_r(U)=−n₀.

For the pure logarithm, X·∇w=−A and ∂_n(X·∇w)=0. Its integrated terms are
−8π²A², 0, and +4π²A², respectively. Thus P_r(w)=−4π²A².

The regular-part estimate works without radial symmetry. On ∂B_r,
X·∇h=O(r), ∂_n(X·∇h)=O(1), Δh=O(1), and ∂_nΔh=O(1).
After multiplication by the area O(r³), the four possible nonzero mixed
contributions are bounded by O(r³), O(r), O(r), and O(r²).
The pure-h contributions are O(r³) or smaller. All vanish as r ↓ 0.
Consequently n₀=4π²A²=m²/(16π²), with the positive sign claimed.

This is a two-stage limit: k → ∞ on a fixed sphere, then r ↓ 0.
Taking a k-dependent sphere directly would require estimates absent here.
H2's fixed-radius constancy is stronger than merely assuming a convergent
iterated mass; it is explicitly a hypothesis, so it causes no logical defect.

## D. What the one-bubble algebra establishes

On the j-th spherical bubble, a_j = lim c_k/M_{j,k} ∈ (0,∞) gives
source mass Qa_j and primitive mass Qa_j². The primitive's subtracted constant
contributes 96(c_k/M_{j,k})²exp(−2M_{j,k}²) on a fixed rescaled region, so it
vanishes there. These are local calculations and do not prove exhaustion.

If both total masses are exhausted by the finite bubble family, then
m = QΣa_j and n₀ = QΣa_j². Substitution gives
Σa_j² = (Σa_j)², equivalently 2Σ_{i<j}a_i a_j = 0.
Finite, strictly positive weights force q=1. No claim about a family with
zero weights, divergent weights, infinitely many levels, or signed weights
follows. The controls (1,0) and (1,1,−1/2) correctly expose those distinctions.

With defects m/Q=S₁+d₁ and n₀/Q=S₂+d₂, expansion gives exactly

d₂ − 2S₁d₁ − d₁² = 2Σ_{i<j}a_i a_j.

The stated example a=(1,1/2), d₁=0, d₂=1 satisfies this equation.
It is a moment configuration, not a constructed solution of the PDE.

The energy/source/primitive densities obey the exact identities
cf=(c/u)e and 4c²F=(c/u)²(1−exp(−2u²))e.
A nonnegative measure model with u=N, c=N² and energy N⁻² has source N⁻¹
and primitive 1−exp(−2N²). This fully retains the primitive's subtraction and
still shows why ordinary vanishing neck energy alone does not control the
second weighted mass. It is expressly not a PDE counterexample.

For the alternative Cauchy–Schwarz calculation, m_k² ≤ E_k ñ_k has the
correct direction. If ñ_k → n₀, the mass identity implies E ≥ Q. It supplies
no upper bound excluding another energy quantum.

## E. Counting and the other four approaches

The source extraction separates centers relative to each bubble scale; it
need not separate their limiting locations. For example, abstract center
sequences ±N⁻¹e₁ with scales N⁻³ have the same limiting point and diverging
relative separation. This is a logical control, not an example of PDE solutions.
Both ordered separation conditions imply that fixed-R balls are disjoint
for sufficiently large k. Their positive energy therefore gives Λ ≥ IQ.
Since the source gives 1 ≤ I and Λ=LQ, 0<Λ<2Q forces L=I=1. That valid
low-energy consequence does not settle arbitrary L.

The exact chain rule for v=u²/2 contains (Δu)², 4∇u·∇Δu and 2|D²u|²
in addition to uΔ²u. The cross term lacks a prescribed sign. Boundary data
are also lost: u(r)=2−3r²+r⁴ on the unit ball satisfies u=Δu=0 at r=1,
but Δ(u²/2)=4 there. This is a boundary-identity control only; it is not
claimed to solve the nonlinear equation.

The Navier system w=−Δu, −Δw=λu exp(2u²), −Δu=w yields positivity and
radial monotonicity under the stated classical setting. One radial maximum
does not by itself rule out further concentrating scales at the same point.

## Missing analysis required for the original problem

To promote this result to the original target, one still needs a justified
bubble accounting and common normalization for every relevant cluster;
positive finite height ratios for every relevant bubble; an exterior logarithmic
profile with sufficiently controlled regular part; a finite primitive-mass
limit; both weighted-mass exhaustion statements; and appropriate treatment of
any boundary concentration and of coincident selected-center limits.
The package proves none of those difficult estimates from the original hypotheses.
The independent code checks finite identities and safeguards, not these estimates.
