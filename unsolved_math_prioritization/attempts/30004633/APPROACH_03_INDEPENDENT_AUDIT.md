# Independent mathematical audit: smooth nondegenerate moving free boundaries

## Verdict and pinned dependencies

**ACCEPTED as a conditional partial convergence theorem. No mathematical correction is required.** The stated smoothness, uniform nondegeneracy, uniform tubular geometry, and physical-wall clearance provide a signed-pressure extension with the residual control required by the already audited discrete argument. No claim for arbitrary weak initial data or nonsmooth free-boundary geometry follows.

The complete frozen file audited was `APPROACH_03_REGULAR_FREE_BOUNDARIES.md`, 8,775 bytes, SHA-256:

`95c4369becb54589dab80ba0c97fb3f3a703aba68526b1ed582d159a9331758c`

The author confirmed this freeze. The audit snapshot is `FROZEN_APPROACH_03.md`. The proof depends on the discrete estimates in Approach 2 at SHA-256 `0ae49bf12019ed74fcaf614caa3c2fc14807a8d05ab7286703ac2005799832c1`, independently accepted in `APPROACH_02_INDEPENDENT_AUDIT.md`. It does not depend on the unrecovered historical Approach 1 or on later approaches. No frozen author file was changed.

The scheme identification and public primary-source checks in the A2 audit apply unchanged: the object is [GMN v2, equations (1.17) and (1.21)](https://arxiv.org/pdf/2105.12605v2), not JKO or a later cell-volume regularization.

## 1. The geometric assumptions are sufficient and meaningfully restrictive

Read the stated smoothness literally as smoothness up to the moving boundary, with a smooth spacetime family, uniform two-sided tubular coordinates, and uniform bounds on the finite jets used. The candidate explicitly allows this convenient C∞ formulation. These assumptions exclude topology change, collision of components, loss of the collar, and physical-wall contact.

Because Ω is bounded and every closure D(t) has the same positive wall clearance, the union over the compact time interval of D(t) and a sufficiently small collar is contained in a fixed compact subset of Ω. Multiple components and holes cause no difficulty: the two-sided tubular hypothesis makes nearest-boundary normal coordinates unambiguous throughout the chosen collar. None of the proof's constants depend on a particle discretization.

## 2. Normal Taylor extension preserves the required jets

In a smooth local parametrization ξ=ξ(t,z), write Ψ(t,z,s)=ξ(t,z)+s n(t,ξ(t,z)), with s positive outwards. The interior pullback p∘Ψ is smooth up to s=0 and equals zero there. Its Taylor polynomial through s⁴ is exactly

Σ_{j=1}⁴ sʲ ∂ₙʲp(t,ξ)/j!.

Here each normal derivative is along the fixed straight ray through ξ, as specified in the candidate. There is no missing j=0 term because the boundary value is identically zero in (t,z). The polynomial coefficients agree with every corresponding interior normal jet through order four. Differentiating those coefficient identities in t and tangential variables gives matching mixed jets of the required total orders. Smooth invertibility of Ψ transfers this matching to Eulerian coordinates. In particular q is C¹ in time, C³ in space, with bounded ∇q_t; the construction in fact has more finite regularity under the literal C∞ hypotheses.

Uniform −∂ₙp≥c₀>0 and bounded higher normal jets imply q_ext≤−c₀s/2 for a common small δ. The exterior cutoff combines two strictly negative functions away from s=0, so it creates no spurious positive set or new zero set. It is identically one near s=0 and zero near the outer collar boundary. Thus q=p inside, q<0 outside the closure, q₊=p1_D, and q=−κ off a fixed compact subset of Ω. Consequently u=−∇q has the required interior support.

## 3. The residual has the needed first-order vanishing

With u=−∇q, the residual is

R=q_t−|∇q|²−(m−1)qΔq.

In D(t) it is zero by the pressure PDE. The boundary trace of that PDE gives p_t=|∇p|² because p=0. The matched Eulerian q_t and ∇q therefore imply R=0 at s=0. Bounded ∇q_t, D²q, D³q, and the remaining bounded jets imply a uniform spatial Lipschitz bound for R on the collar. For fixed t, integration along the normal segment yields |R(t,Ψ(t,z,s))|≤C s.

On 0<s≤δ/3, −q≥c₀s/2, so |R|≤(2C/c₀)(−q). On the cutoff portion, q_ext≤−c₀δ/6 and −κ<0; their convex combination is bounded above by a uniform negative constant. Boundedness of R supplies the ratio bound there. Outside the collar q is constant and R=0. This proves the full residual inequality, including its vanishing right-hand side on {q≥0}.

No solution of the pressure PDE in vacuum has been assumed. Only its interior equation, boundary trace, and finite-jet extension are used. This is the central new step beyond the radial example.

## 4. Kinematic condition and transport of the domain

Along a smooth boundary parametrization, differentiating p(t,ξ(t,z))=0 gives p_t+V_n ∂ₙp=0, since all tangential pressure derivatives vanish. At the boundary |∇p|²=(∂ₙp)², hence V_n=−∂ₙp=u·n. The globally Lipschitz velocity therefore has the same normal motion as the prescribed interface.

A fully explicit justification of set transport is available in the collar. Along a u-characteristic,

(d/dt)q(t,X(t))=q_t−|∇q|²=(m−1)qΔq+R.

The residual bound and bounded Δq imply |(d/dt)q|≤C|q| near the zero set, on both sides. Grönwall, also backwards in time, prevents a nonzero signed q value from reaching zero in finite time and preserves a zero value along interface characteristics. Thus the flow maps D(a) onto D(t); this does not require arbitrary trajectories chosen along the boundary to have zero tangential velocity.

## 5. Density conservation and integral identities

Set α=1/(m−1)>0 and c=(m−1)/m. In the positive region, ρ=(cp)^α satisfies

ρ_t=αρ p_t/p,
∇ρ=αρ ∇p/p,

div(ρu)=−αρ|∇p|²/p−ρΔp.

Using p_t=(m−1)pΔp+|∇p|², the sum vanishes. Nondegeneracy and bounded jets imply p is comparable to interior distance s, hence ρ=O(s^α), its spatial and Eulerian time derivatives are O(s^{α−1}), and its flux is O(s^α). These derivatives are locally integrable for every α>0. The spacetime integration-by-parts boundary term on an interior collar cutoff is O(h^α), tending to zero. Therefore the continuity equation has no interface delta contribution. Equivalently, the smooth flow and its Jacobian give the material conservation identity in the positive region and then on all mass by integration. Initial unit mass is preserved.

For P=∫ρᵐ, use the globally defined function P=∫(c q₊)^{m/(m−1)}. Its scalar derivative is ρ, continuously also at q=0, so P'=∫ρq_t. The transport identity for ρᵐ gives

(ρᵐ)_t+div(ρᵐu)=−(m−1)ρᵐ div u.

Its interface term vanishes, with size O(h^{m/(m−1)}). Integrating proves P'=−(m−1)∫ρᵐ div u. The physical flux also equals −∇ρᵐ in the interior and across the interface in distributions, so the constructed density is a no-flux weak porous-medium solution, not merely a formal continuity solution.

## 6. Every input of the A2 estimate is now available

The A2 proof after its radial reference construction needs only:

- a probability reference density of bounded support, hence an atomless initial source with finite internal energy;
- q₊=mρ^{m−1}/(m−1);
- a globally bounded and spatially Lipschitz u=−∇q, compactly supported inside Ω;
- bounded Hessian of q and bounded gradient of |u|²−q_t;
- the two P' identities;
- |R|≤C(−q)1_{q<0};
- the material flow identity for the reference solution.

All have been established above. In particular bounded ∇(|u|²−q_t) follows from bounded u, D²q, and ∇q_t. Initial cell barycenters can lie outside a nonconvex D(a); q is globally C² so the initialization Taylor estimate still applies. Proximal reconstructed densities and particles need not avoid the wall or the vacuum.

The signed Fenchel energy, proximal variation, exact cancellation, two commutator bounds, O((τ/ε)(1+f₀)) total frozen defect, nonpositive node jumps, initialization, and material Grönwall argument therefore apply with the same scale bound. This proves candidate (4.1) for every m>1 and d≥1 under its stated geometric hypotheses. The density and signed-energy consequences proved by that argument also remain valid, although (4.1) itself only displays the material estimates.

## 7. Acceptance limits and patch disposition

The accepted assertion is conditional on a smooth, nondegenerate reference pressure geometry throughout the entire fixed interval. The proof does not establish these hypotheses from generic initial data and cannot be continued through a waiting-time interface, merging components, a singular interface, or wall contact by this argument alone. In particular its validity must not be used to label the entire OWR irregular-solution question resolved.

No mathematical patch is needed. The flow-invariance argument in §4 of this audit supplies a useful expanded justification for an inference abbreviated in the candidate, but that inference follows directly from its hypotheses and does not require a changed assumption. No finite test or numerical experiment was used as evidence for the PDE or geometric extension theorem.
