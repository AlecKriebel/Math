# Leroux entropy partial results and obstructions

## Result

The full Oleinik bound for arbitrary three-state hydrodynamic limits remains unresolved after five distinct approaches. The strongest proved specialization is the sharp bound D_x a,D_x b<=1/(2t) on each of the three invariant two-species faces, assuming the source limit's weak Cauchy equation and interior Lax entropy inequalities. The scalar initial trace is justified by the inspected Chen–Rascle theorem; no strong initial entropy assumption is inserted for this specialization.

The other routes give an exact failure of natural-order microscopic attractiveness, conditional entropy invariant regions, a smooth weighted-gradient identity, and the precise mixed derivative blocking a naive viscous maximum principle. These results are elementary consequences/specializations of known structures, and no novelty is claimed. No constructed object is a counterexample to the full hydrodynamic Oleinik conjecture.

Use the model, coordinates, and source qualifications in EXACT_TARGET.md throughout. Write d=a−b=sqrt(u²+4rho), lambda_+=2a+b and lambda_−=a+2b.

## Approach 1 Microscopic monotone coupling

### Mechanism

Try to derive order comparison and scalar-style one-sided bounds from the attractive-process coupling method, using the natural coordinatewise order −1<0<1 on spins.

### Exact obstruction

Consider configurations omega<=omega_tilde which agree except at site1. At sites(0,1), take omega=(1,−1), omega_tilde=(1,0); take all other sites−1. The increasing cylinder function F=1{omega_1=1} is zero in both configurations. Its generator values are

L_epsilon F(omega)=2+sigma_micro,
L_epsilon F(omega_tilde)=1+sigma_micro.

No other bond can create a+1 spin at site1. If an order-preserving Markov semigroup existed for this order, P_t F(omega)<=P_t F(omega_tilde) for all t>=0. Equality at t=0 would force L F(omega)<=L F(omega_tilde), contrary to these values. The same witness works on a ring of at least3 sites.

Thus this **specific** attractive coupling is impossible, independently of the stirring strength. This does not rule out a more elaborate partial order, integrated-height comparison, or a different probabilistic mechanism. The source already warns that the model is not naturally attractive; the witness makes that obstruction explicit rather than claiming a new non-attractiveness theorem.

### No pathwise empirical invariant rectangle

On a15-site ring start from(0,1,−1) repeated5 times. Every triangular block average of radius3 has(rho,u)=(1/3,0), since its weights1,2,3,2,1 give each residue class total weight3. Symmetric stirring has positive rate for every adjacent transposition. Therefore a finite sequence of such transpositions can move the five zero spins into a contiguous block of length5. At its center, the same triangular average has(rho,u)=(1,0). This is outside any sufficiently small invariant-coordinate rectangle around the initial state.

A prescribed finite sequence of effective transpositions has positive probability of occurring before any fixed positive time on this finite ring. Hence an exact pathwise empirical rectangle is not preserved. This says nothing about whether the exceptional probability vanishes in the hydrodynamic limit. It is a negative check on importing a deterministic maximum principle directly to random block profiles, not a counterexample to macroscopic invariant-region preservation.

Status: natural-order mechanism blocked; microscopic rectangle inference invalid.

## Approach 2 Affine entropy invariant regions

### Lemma 1 Scalar transport of an affine entropy

For each real c define

S_c(rho,u)=rho+c u−c²,
F_c(rho,u)=(u+c)S_c(rho,u).

Because S_c is affine and F_c=f_1+c f_2−c³, every distributional solution of(L) satisfies

(S_c)_t+(F_c)_x=0.

The known generalized convex entropy pair(|S_c|,(u+c)|S_c|), combined with the affine pair, gives for z_c^+=(S_c)^+ and z_c^−=(−S_c)^+

(z_c^±)_t+((u+c)z_c^±)_x<=0.                  (1)

This is a distributional continuity inequality for a nonnegative quantity. It requires no derivative of u. It uses exactly the explicit entropy family appearing in Fritz–Toth/OWR, or an entropy class known to include that family.

### Lemma 2 Conditional invariant rectangle

Suppose U is D-valued, satisfies(1), and the entropy inequalities include their initial terms z_c^±(U_0), for the four thresholds below. A strong local L1 initial trace is one sufficient way to obtain those terms from interior inequalities. If

0<A0<=a(U_0)<=A1<=1,
−1<=B0<=b(U_0)<=B1<0,

then the same four inequalities hold at almost every positive spacetime point.

Proof. The factorization is S_c=(a−c)(c−b). Thus the required zero violations are

(S_{A1})^+=0,   (−S_{A0})^+=0,
(S_{B0})^+=0,   (−S_{B1})^+=0.

For c∈[−1,1], |u+c|<=2. Apply(1) with smooth approximations of a backward expanding cone cutoff. For any interval I=[x0−R,x0+R] and almost every t>0, the usual integral inequality is

∫_I z_c^±(t,x) dx <= ∫_{x0−R−2t}^{x0+R+2t} z_c^±(0,x) dx.

To see the sign directly, choose a nonnegative cutoff psi(s,x) with psi_s+2|psi_x|<=0, equal to the target interval cutoff at s=t and with enlarged support at s=0; the weak inequality yields ∫z(t)psi(t)<=∫z(0)psi(0). The right side vanishes. Exhausting bounded intervals proves the claim. The zero-threshold bounds a>=0,b<=0 already follow from D, so limiting rectangles may be handled with those trivial sides. No claim of differentiability at a=b=0 is needed. QED.

If, in addition, A1+2B1<2A0+B0, the resulting rectangle satisfies the cited strengthened hyperbolicity condition. This still does **not** produce a derivative estimate. Even if the initial trace and invariant region are available, arbitrary oscillations inside the rectangle have not been excluded.

Status: rigorous conditional invariant-region lemma; no full-source initial entropy trace or Oleinik decay is established by this route. SOURCE_SCOPE_AUDIT.md explains why weak initial convergence cannot be silently promoted to the required entropy trace.

## Approach 3 Inviscid weighted characteristic gradients

### Lemma 3 Exact Riccati cancellation

Let U be a C² classical solution in a region with d>0. Put p=a_x, q=b_x, D_+=∂t+lambda_+∂x, D_−=∂t+lambda_−∂x. Differentiating the diagonal equations gives

D_+p=−2p²−pq,    D_−q=−2q²−pq,
D_+d=−dq,       D_−d=−dp.

Consequently

D_+(p/d)=−2d(p/d)²,
D_−(q/d)=−2d(q/d)².                            (2)

Along a characteristic from time0, if P0=p(0)/d(0)>0, integration gives

p(t)/d(t)=1/[1/P0+2∫_0^t d(s) ds].             (3)

If P0<=0, its sign stays nonpositive for as long as the classical solution exists; a negative denominator blow-up terminates the classical interval rather than continuing through infinity. The corresponding statement holds for q.

Thus if0<delta<=d<=M along all backward characteristics to time0, then

p(t)<=M/(2delta t),    q(t)<=M/(2delta t).        (4)

This does not require a bound on the positive initial gradients. It is a genuine one-sided estimate in the smooth regime and displays the precise dependence on a hyperbolicity gap.

### Why it does not prove the target

Equation(2) was derived by the classical chain rule and needs products of spatial derivatives. Hydrodynamic limits need not have BV regularity, let alone differentiable characteristics. At a shock these identities do not hold as ordinary differential equations without a transmission analysis; using a front-tracking semigroup to supply that analysis would assume the very membership still to be proved. At d=0 even the weights p/d and q/d are singular. A strong L1 limit alone cannot pass these identities or their derivative bounds unless uniform versions are proved for the approximants.

Status: proved smooth partial bound; extending the estimate past shocks and through the degenerate state remains unsupported.

## Approach 4 Viscous maximum principle

### Mechanism and exact transformed equations

The strong stirring suggests comparison with the deterministic isotropic viscosity regularization

U_t+f(U)_x=nu U_xx,    nu>0.

This is a test of a possible analytic bridge, not an assertion that random block averages solve that equation without errors. For a C³ viscous solution with d>0, the exact equations are

a_t+lambda_+a_x=nu(a_xx−2a_x b_x/d),
b_t+lambda_−b_x=nu(b_xx+2a_x b_x/d).             (5)

Indeed U=(-ab,a+b) has U_ab=(-1,0). Applying the inverse Jacobian gives these opposite mixed terms. Dropping them would incorrectly replace the physical viscosity by another equation.

Write P=a_x/d, Q=b_x/d. A further exact calculation gives

D_+P=−2dP²+nu[P_xx+2(P−2Q)P_x−2P Q_x+2PQ(P+Q)].       (6)

At a positive spatial maximum of P, P_x=0 and P_xx<=0, but Q_x has no fixed sign. Therefore the scalar Riccati maximum-principle argument from Approach3 does not close.

### Explicit local jet test

This is not merely an unspecified error term. At a point take a=1/2,b=−1/2,d=1, a_x=1,b_x=0, a_xx=1, b_xx=−M, a_xxx=M+1, and b_xxx=0. These jets give P=1,Q=0,P_x=0,P_xx=0,Q_x=−M. Equation(6) then gives

D_+P=−2+2nu M,

which is positive for M>1/nu. Smooth functions attaining these jets can be chosen on a sufficiently small spatial neighborhood while keeping a,b strictly inside their allowed intervals. If a strict local maximum is desired, reduce a_xxx by any small positive number to make P_xx<0; choose M correspondingly larger. Hence no inequality of the naive form D_+P<=nu P_xx−2delta P² follows from the viscous equations at maxima.

This jet test refutes that proposed differential comparison, not every possible viscous Oleinik estimate. It is not a hydrodynamic counterexample. The microscopic problem would additionally require stochastic martingale and replacement-error estimates with the appropriate sign; vanishing errors only in a weak Sobolev norm do not justify this pointwise comparison.

Status: precise mixed-derivative obstruction found; no valid viscous/stochastic bound obtained.

## Approach 5 Actual invariant two-species faces

### Theorem 4 Sharp face specialization

Let U be a D-valued weak solution of(L) with prescribed bounded initial value U_0 in the weak Cauchy formulation, and satisfying the interior generalized convex Lax entropy inequalities. Suppose U takes values in one of the following faces for almost every spacetime point, and U_0 lies in that face:

F0: rho=0,      −1<=u<=1;
F+: rho=1+u,    −1<=u<=0;
F−: rho=1−u,     0<=u<=1.

Then U is uniquely determined by U_0 within that face class, and for almost every t>0

D_x a(t,.)<=1/(2t) dx,    D_x b(t,.)<=1/(2t) dx.        (7)

These are actual microscopic invariant faces for normalized empirical averages: F0 corresponds to no0 spins, F+ to no−1 spins, and F− to no+1 spins. Pure exchanges never create an absent spin value. Thus if the microscopic initial law gives probability1 to configurations omitting that spin value, every subsequent average with nonnegative weights summing exactly to1 lies in the corresponding face.

The unnormalized smooth empirical profiles used in the saved OWR note and Fritz–Toth v2 require a normalization correction at finite scale. Write K for their kernel, so K>=0, K has compact support, K is at least C1 (v2 assumes C2), and integral K=1. With weights w_k(x)=ell^(-1) K((x/epsilon−k)/ell), let W_epsilon(x)=sum_k w_k(x). Then absence of0 gives rho_hat=0, absence of−1 gives rho_hat=W_epsilon+u_hat, and absence of+1 gives rho_hat=W_epsilon−u_hat. These are exact identities; W_epsilon need not equal1.

Here is the uniform correction. The sampling nodes have spacing h=1/ell. Partition the real line into length-h intervals centered at these nodes. On each interval, the fundamental theorem of calculus bounds the difference between h times the midpoint value of K and its integral by h times the integral of |K'| on that interval. Summing gives

sup_x |W_epsilon(x)−1| <= ell^(-1) integral |K'| ->0.

This estimate is uniform in the node shift, and also applies to the periodized sums on the torus. The stated block scales imply ell->infinity and epsilon ell->0. For all sufficiently small epsilon, W_epsilon>0. Dividing both empirical components by W_epsilon gives an exactly normalized face-valued profile. Since each microscopic component has absolute value at most1, the difference in each component between the raw and normalized profiles is at most |W_epsilon−1|, uniformly in configurations and time. Hence every strong local L1 subsequential limit of either profile lies in the same closed physical face.

This normalization argument only establishes face membership. Theorem4 still requires the prescribed weak Cauchy equation and interior entropy inequalities; it does not repair the separate initial-trace issue in the full system. The assertion is global absence of one microscopic species, not merely pointwise initial membership in a union of different faces.

### Proof of the entropy reduction

The second equation becomes u_t+(u²+beta u+gamma)_x=0, with(beta,gamma) respectively(0,0),(1,1),(−1,1). The first equation is redundant on each face. Every scalar Kruzhkov entropy is obtained by restricting the known system family |S_c|:

- F0: S_c=c(u−c). For any nonzero threshold k∈[−1,1], put c=k and divide the entropy/flux pair by|k|. This gives |u−k| and sign(u−k)(u²−k²). The k=0 inequality follows by uniform convergence as k→0.
- F+: for k∈[−1,0], put c=k+1∈[0,1]. Then S_c=(1+c)(u−k). Dividing by1+c gives |u−k| and sign(u−k)[(u²+u)−(k²+k)].
- F−: for k∈[0,1], put c=k−1∈[−1,0]. Then S_c=(c−1)(u−k). Dividing by1−c gives |u−k| and sign(u−k)[(u²−u)−(k²−k)].

Thresholds outside the range give affine inequalities already contained in the conservation equation. By the usual integral representation of convex functions in terms of absolute-value entropies, all smooth convex scalar entropy inequalities follow. Each scalar flux has f''=2 and no affine interval. Chen–Rascle's inspected main theorem applies to the weak Cauchy equation plus these interior inequalities and identifies u as the unique Kruzhkov solution. This step uses the genuinely scalar equation and does not claim the same trace repair for the two-component interior.

### Proof of the sharp bound

Set z=2u+beta. Then z is the Kruzhkov solution of z_t+(z²/2)_x=0. Let H_0 be a Lipschitz primitive of z_0. The entropy solution is the spatial derivative of

H(t,x)=inf_y [H_0(y)+(x−y)²/(2t)].

The minimum exists since the quadratic dominates the at-most-linear growth of H_0. At points where H_x exists, choose a minimizer y_x; then z(t,x)=(x−y_x)/t. If x<x', optimality of the two minimizers and addition of the two cost inequalities give y_x<=y_{x'}. It follows that z(t,x')−z(t,x)<=(x'−x)/t, hence u(t,x')−u(t,x)<=(x'−x)/(2t), with the distributional interpretation at shocks.

On F+, a=u+1 and b=−1. On F−, a=1 and b=u−1. On F0, a=max(u,0) and b=min(u,0). Both maximum and minimum maps here are nondecreasing and1-Lipschitz; if u(y)>=u(x), their increments are at most u(y)−u(x), while otherwise their increments are nonpositive. Thus both preserve this one-sided upper bound, proving(7), including at u=0 on F0.

The common constant1/2 is sharp: for any allowed scalar Riemann data u_L<u_R, the rarefaction fan has u(t,x)=(x/t−beta)/2 between speeds2u_L+beta and2u_R+beta. Thus u_x=1/(2t) there. Choose u_L=−3/4,u_R=−1/4 on F+, u_L=1/4,u_R=3/4 on F−, and u_L=−1/2,u_R=1/2 on F0. The nonconstant invariant on either sloping face, and each invariant on its corresponding nonzero-sign part of the F0 fan, attain this slope. The constant invariant on each sloping face has the stronger bound0. QED.

### Scope of this success

This is a boundary specialization by familiar scalar theory, not a reduction of the general model to Burgers. It proves no estimate for configurations genuinely containing all three species. An initial macroscopic profile that lies on a face without a justified microscopic or entropy invariant-face statement is not automatically covered. No unknown three-state uniqueness theorem has been used.

Status: rigorous sharp partial theorem for three genuinely invariant submodels; full coupled target remains open in this program.

## What would close the full target

One still needs a sign-sensitive estimate on the positive spatial increments of both invariants for arbitrary permitted three-state initial laws, uniform at the chosen hydrodynamic scaling and strong enough to survive shocks and d=0. Alternatively, an independent uniqueness/regularity theorem could identify every relevant entropy limit with a semigroup having the bound. Neither is obtained here. The initial trace and the exact domain of any uniqueness theorem must also be checked. Strong spacetime compactness, entropy dissipation, and the existence of a deterministic semigroup are individually insufficient bridges.

## Verification and references

The read-only verifier verify_algebra.py checks flux signs, coordinate identities, affine entropy factorization, scalar-face reductions, natural-order generator obstruction, a reachable empirical-block rectangle violation, the inviscid cancellation, the viscous identity, and the explicit jet. It uses exact rational/symbolic arithmetic and explicit exceptions, not Python assert. It does not prove analytic compactness, PDE existence, the cited uniqueness theorems, or the stochastic limit. Optimized-mode and mutation results are recorded in VERIFICATION.json.

Primary sources, theorem locators, and version limitations are in EXACT_TARGET.md, SOURCE_SCOPE_AUDIT.md and SOURCE_METADATA.json. In particular the affine entropy family and hydrodynamic framework are due to Fritz–Toth/Fritz; Temple semigroup uniqueness is credited to Bressan–Goatin and later work; scalar trace uniqueness is credited to Chen–Rascle. No third-party source body is part of this report.
