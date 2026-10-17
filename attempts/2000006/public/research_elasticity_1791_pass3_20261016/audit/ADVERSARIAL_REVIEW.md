# E-6322: independent adversarial review, shared pass 3

Date: 16 October 2026. The complete frozen target and the prior audit were retained. This review concerns arbitrary positive coefficients, all permitted smooth diffeomorphic full boundary data, the complete finite-energy primal comparison class, and an essential determinant bound throughout the domain.

## Verdict

**Accept the reviewed results as rigorous partial progress. No unconditional proof or minimizing counterexample to E-6322 was obtained.**

This pass makes three substantial advances without changing the benchmark:

1. It characterizes the exact inverse comparison class by finite transformed energy and full-boundary transported Piola identities, proves energy-bounded compactness, and establishes admissibility of compactly supported W^{1,9/4} additive inverse differences whenever their transformed energy is finite.
2. It excludes every admissible exact interior weighted-power collapse core with C² angular data and positive exponents. The complementary exponent range left after pass 2 is now covered.
3. It proves a genuine minimizer-specific one-component energy-gap inequality, an unconditional reference-based truncation with a fixed threshold ceiling, and sharp sufficient energy moments for ordinary primal and inverse equilibrium.

The constitutive calculations also distinguish positive rank-one ellipticity from uniform ellipticity, quantify stress anisotropy, and prove constant positive determinant in the exactly conformal inner-stationary subclass. These remain restricted statements. The missing unconditional integrability, regularity, or direct all-boundary positivity argument has not been supplied.

## 1. Exact inverse class: what is now established

Let D=G(Omega), H=Dv, K=det H, and

V(H)=a|cof H|^6/K^5+b|H|^3/K^2+c/K+dK^3

for K>0, with infinite value otherwise. The pass-2 actual weak-inverse theorem is used in the primal-to-inverse direction only. In particular an admitted primal deformation has an a.e. inverse in W^{1,9/5}(D), with cof Dv in L^{9/4}, K in L³, full inverse trace, and the exact energy identity.

The first two terms of V are convex perspectives in the independent minors. The resulting polyconvexity is correct, but is not invoked as a blanket lower-semicontinuity theorem at the low inverse gradient exponent. Splitting the positive coefficient of K³ gives simultaneous coercivity for |H|^{9/5}, |cof H|^{9/4}, K³, and K^{-1}.

### 1.1 The initial explicit compatibility characterization

The first literature report imposes finite V, a measurable a.e. bijection with exact Jacobian transport, and the identity

integral_D [psi K div phi(v)+phi(v) dot (cof Dv) Dpsi]
 = integral_boundary(Omega) psi(G) phi dot nu.

Here psi is smooth near the closure of D and phi is smooth near the closure of Omega. These conditions are sufficient to recover the primal weak derivative, rather than assuming it.

Indeed, set psi(z)=z_i and phi(x)=e_j eta(x). Transport converts the compactly supported identity into

integral_Omega y_i partial_j eta
 + integral_Omega eta [(cof Dv)_{ji}/K] composed with y =0.

The coefficient in the second integral is [(Dv)^{-1}]_{ij} composed with y. Its sixth power is integrable because

integral_Omega |(Dv)^{-1} composed with y|^6
 = integral_D |cof Dv|^6/K^5.

Thus the measurable inverse is genuinely W^{1,6}. Allowing eta up to the boundary and applying Gauss–Green yields the complete primal trace G. The energy identity and positive determinant then place the recovered map in the original class. Conversely, primal Sobolev chain rule and integration by parts prove the imposed identity for every original inverse, including inverses with exceptional discontinuous fibers.

The index orientations, integrability, measurable substitutions, and full-boundary trace argument all pass review.

### 1.2 The stronger reduced characterization

The final theorem requires only v in W^{1,9/5}(D), finite V, and the same full-boundary transported Piola identity for phi in C_c^infinity(R³). It derives the range, measurable a.e. bijection, exact transport, and inverse trace.

The proof is sound:

1. With psi=1, the finite measure mu=v_#(K dz) satisfies D(mu-1_Omega dx)=0 on all of R³. A finite measure with zero distributional derivative is a constant distribution; convolution makes this explicit, and integrability on R³ forces that constant to be zero. No unsupported compact-support assumption on mu is needed.
2. Therefore mu is Lebesgue measure on Omega. Positivity of K gives v in Omega almost everywhere.
3. Apply the area formula on a Borel, full-measure, approximately differentiable good set with a countable Lipschitz decomposition. Its multiplicity must be exactly one almost everywhere on Omega. No Lusin N property is assumed for the discarded null set or for an arbitrary pointwise representative.
4. Remove preimages of exceptional target null sets using the established transport formula and K>0. This leaves full-measure sets on which v is a bijection. The measurable fiber-sum formula, or Borel injectivity, gives a measurable inverse.
5. The coordinate-test proof above now recovers the primal W^{1,6} map and its full trace.

The primary area formula and weighted fiber-sum statement were independently checked in Barchiesi–Henao–Mora-Corral–Rodiac, Proposition 2.1 and Definition 2.2, p.5. Their hypotheses are approximate differentiability on the relevant good set; they are not the more restrictive hypotheses of the later neo-Hookean variational theorem. [Primary paper](https://arxiv.org/pdf/2311.02952v2)

**Exact scope:** full-boundary transported Piola is still imposed. It has not been derived for every finite-V map having an ordinary inverse trace. The theorem does not identify that larger class with the genuine inverses.

### 1.3 Energy-bounded weak closure and relaxation

The closure proof avoids unproved inverse-minor continuity. Lift an energy-bounded inverse sequence to its primal maps y_n. They are bounded in W^{1,6}, have a weakly convergent subsequence with finite-energy limit, and converge uniformly on the closure by compact Sobolev embedding. The inverses are bounded in W^{1,9/5}, with a subsequence converging almost everywhere.

Passing in y_n(v_n(z))=z gives y(v(z))=z. For z in the interior target, v(z) cannot lie on the primal boundary because the fixed trace maps that boundary to the target boundary. The previously established a.e. uniqueness of the entire inverse fiber identifies v with the genuine inverse of y. Primal lower semicontinuity then supplies inverse lower semicontinuity.

This proves sequential weak compactness of energy sublevels and lower semicontinuity of the functional extended by infinity outside the exact inverse class, both for weak W^{1,9/5} convergence and strong L¹ convergence. Its corresponding sequential finite-cost relaxations add no maps. It does not assert closure for sequences whose energies diverge, density of diffeomorphisms, or equivalence to an unconstrained low-exponent inverse problem.

## 2. Additive inverse comparisons: a genuine new admissibility theorem

The full-boundary characterization closes a comparison gap for an explicit class of differences.

**Accepted statement:** if v is a genuine inverse, zeta has compact essential support in D and belongs to W^{1,9/4}(D), and V(Dv+Dzeta) is integrable, then v+zeta is another genuine inverse of an original full-class competitor. This includes compactly supported smooth and Lipschitz additions.

The proof was independently checked in all three stages.

### 2.1 Preservation of weak Piola

The full identity for v, tested with a target vector field constant on its bounded range, gives Div(cof Dv)=0. Since the cofactor is quadratic,

cof(Dv+Dzeta)=cof Dv+M(Dv,Dzeta)+cof Dzeta.

The mixed polarization has zero divergence. Approximate v strongly in W^{1,9/5} and zeta strongly in W^{1,9/4}; their mixed gradient products converge strongly in L¹ by conjugacy. The pure cof Dzeta converges in L^{9/8}. Classical smooth Piola therefore passes to distributions for both terms. No ordinary weak Piola theorem at exponent 9/5 is silently invoked for an arbitrary map.

### 2.2 Transported chain rule

Finite V of the perturbed map restores its cofactor in L^{9/4}. This is conjugate to its gradient in L^{9/5}. Weak Piola may therefore be tested against psi phi(v+zeta) by Sobolev density. The pointwise cofactor identity gives the interior transported Piola equation. Boundedness of zeta is unnecessary: the target test phi and its derivative are bounded.

### 2.3 The boundary term

The perturbed map and its gradient equal the original ones on a collar because zeta has compact essential support. The difference of their transported fluxes is compactly supported and integrable. A compact cutoff allows its interior divergence identity to be tested with every psi smooth up to the boundary, showing that the full boundary flux remains unchanged. The reduced characterization then recovers the range, bijection, actual primal inverse and prescribed traces.

Consequently an inverse of a primal global minimizer is a local minimizer against **every compact W^{1,9/4} additive difference**: finite-energy comparisons are admissible, and infinite-energy comparisons satisfy the minimizer inequality trivially.

**Limits that must remain explicit:** this proves neither an open interval of finite-energy amplitudes for each test nor ordinary stress integrability. It does not cover all W^{1,9/5} differences. In particular, the standard cutoff difference eta(v-affine) has only the latter regularity at baseline. Its determinant positivity and finite V also remain nontrivial. These facts prevent importing an unrestricted inverse Caccioppoli or Euler equation merely from the new comparison theorem.

An additional conditional consequence follows by the same proof: if v already belongs to W^{1,2}, then compact W^{1,2} differences with finite V are admissible, since both mixed gradients are in L² and their products converge in L¹. This does not remove the finite-energy constraint or provide that extra inverse regularity unconditionally.

## 3. The complete exact weighted-power core exclusion

The counterexample report now treats every exact interior ansatz

y_i(r theta)=r^{alpha_i} phi_i(theta),

with positive ordered exponents, C² angular data, and s=sum alpha_i>3, provided it belongs to the original finite-energy class. It proves that such a core cannot occur in a local minimizer. Translations of the two origins are harmless. No asymptotic representation or boundary statement is substituted for the exact hypotheses.

### 3.1 Angular positivity follows from the energy

Write J=r^{s-3}j(theta). Finite barrier energy on any fixed annulus implies integral_{S²} j^{-2}<infinity. Almost-everywhere orientation and continuity give j>=0. Since C² angular data makes j C¹ and hence Lipschitz, a zero would force j<=C times spherical distance. Its inverse square then has logarithmically divergent two-dimensional integral. Therefore min j>0.

This removes the separate uniformly positive angular Jacobian hypothesis required in pass 2, within this exact smooth-angular class. Nonzero rows and compactness give the radial restrictions alpha_1>1/2 and s<9/2. They do not themselves imply the pass-2 exponent inequality; the report's explicit admissible negative-gap example is correct.

### 3.2 The remaining exponent range

Let m=alpha_1 and eta=2(3m+alpha_2+2alpha_3-6). The pass-2 third-row ray argument excludes eta>0. If eta<=0, equality alpha_2=m would imply eta=4(s-3)>0. Hence the minimum exponent is unique. Also m<1 and s+3m<6.

On every compact punctured subset, the exact map is C² with positive determinant bounded below, so ordinary additive stationarity there is justified. Its first equation has leading term 6a div(|grad y_1|^4 grad y_1), of degree 5m-6. All remaining terms have strictly positive gaps above this degree:

- sixth-power correction: 2(alpha_2-m)
- cofactor-cubic contribution: 3(alpha_2-m)
- determinant-square contribution: 2s-6m
- barrier contribution: 2(6-s-3m)

The cofactor estimate correctly uses only the cofactor rows changed by differentiating the first gradient row. Differentiation loses at most one radial power, with bounded angular coefficients. Dividing by the leading power and taking the radial limit therefore gives the exact scalar 6-Laplace equation for u=y_1 on the punctured ball.

### 3.3 The critical exponent is handled, not omitted

For u=r^m varphi(theta), the spherical equation yields

integral A|grad_S varphi|² = m(5m-3) integral A varphi²,

where A=(m²varphi²+|grad_S varphi|²)².

For 1/2<m<3/5, the signs force varphi=0, impossible for a positive Jacobian. At m=3/5, varphi is constant. A nonzero constant would make the first target coordinate have one sign throughout the punctured neighborhood. The continuous map has an isolated zero and positive local degree, since its punctured Jacobian is positive. Small target points on both signs of the first coordinate axis must therefore be attained, a contradiction. This degree argument remains valid for the weighted rather than ordinary homogeneous map.

For 3/5<m<1, the scalar stress flux on a shrinking sphere is O(r^{5m-3}) and vanishes. The scalar weak equation thus extends across the origin; u belongs to W^{1,6}. Uhlenbeck's scalar interior regularity corollary then supplies bounded first derivatives, contradicting the nonzero homogeneous gradient r^{m-1}.

The original Uhlenbeck p.222 was independently visually inspected. Its parameter p=4 gives precisely the weak 6-Laplace equation and W^{1,6} hypothesis used here. The theorem is applied only after the scalar reduction and puncture-removal proof, never directly to the elasticity system. [Original paper](https://doi.org/10.1007/BF02392316)

**Conclusion and limitation:** all exponent cases for these exact C²-angular interior weighted powers are excluded. Less regular angular data, genuinely nonhomogeneous cores, asymptotic expansions with additional terms, and boundary degenerations remain outside the theorem. This is a complete ansatz exclusion, not a regularity theorem for arbitrary minimizers.

## 4. One-component minimizer coercivity and relative-minor excess

### 4.1 A full-class energy-gap inequality

If a competitor differs from a minimizer in one fixed target direction, every minor is affine along their straight interpolation. Positive determinant and convexity in the independent minors make the entire segment admissible. This remains true without injectivity, a derivative trace, ordinary stress integrability, or an Euler equation.

The midpoint argument gives

I(v)-I(y) >= (a/32) integral |Dv-Dy|^6
 + (b/4) integral |cof Dv-cof Dy|^3
 + (c/2) integral |J_v-J_y|²
 + d integral |J_v^{-1}-J_y^{-1}|².

The Euclidean uniform-convexity constants and reciprocal-square midpoint identity pass independent review. This is genuinely minimizer-specific, unlike a generic finite-energy example. It implies uniqueness within a fixed-component slice, strong convergence for same-slice near-minimizers, and the stated conditional low-J repair-cost bound.

It still supplies no repair with controlled energy. The cofactor-row constraint J_new=J+X dot grad phi includes a cutoff error (w_3-y_3)X dot grad eta. The report's affine-minimizer example shows that this error can make the determinant negative even when both unlocalized endpoints have positive determinant. Demanding X dot grad eta=0 does not generally provide nontrivial compact cutoffs. No scalar uniform-convexity argument is allowed to skip this admissibility constraint.

### 4.2 Relative-minor formulation for arbitrary full trace

The Bregman remainder R_A at any fixed A in GL^+(3) is nonnegative and controls gradient, cofactor, determinant, and reciprocal-determinant differences. The exact barrier remainder and its lower bound by the squared reciprocal difference are correct.

The difference W-R_A is constant plus a constant-coefficient linear combination of the first, second and third minors. Their integrals depend only on the complete trace, justified at W^{1,6} by strong approximation and the polynomial null-Lagrangian identities. Hence minimizing W over the prescribed class is exactly equivalent to minimizing the integral of R_A, even for nonaffine data.

This provides a faithful positive excess, not permission to compare against an affine map with the wrong trace. The affine specialization yields strong quasiconvex lower coercivity and uniqueness; it is not a proof for all permitted data. Likewise the Hessian-based uniform-convexity estimate for the independent minor norms is not convexity of the full W in arbitrary matrix directions.

### 4.3 An unconditional reference truncation, with its essential threshold ceiling

The late reference-truncation result also passes independent review. Set w=y-G and extend it by zero to R³. Complete zero trace makes this a W^{1,6} function. On the good set where M(|Dw|)<=lambda, the standard telescoping/Poincaré estimate gives a C lambda-Lipschitz restriction. For an interior good point, uniform exterior volume density and the zero extension give the separate boundary estimate

|w(x)|<=C_Omega dist(x,Omega^c) M(|Dw|)(x).

This is the necessary justification for adjoining the entire exterior with prescribed value zero: the exterior maximal function itself need not vanish. A componentwise McShane extension preserves all good-set values and the zero exterior data, with gradient bounded by C_Omega lambda. Sobolev locality then guarantees equality of the old and new gradients almost everywhere on the good set.

Let m be the positive minimum singular value of DG. If lambda<=m/(2C_Omega), adding the Lipschitz extension to G leaves every matrix segment within distance m/2 of DG. All singular values stay at least m/2, and the determinant retains its positive sign. Thus the new map has determinant at least (m/2)^3, correct full trace, and uniformly bounded energy density. With M_0=max|DG|, the stated bound

C_G=[a+b/(3sqrt(3))+c/27](M_0+m/2)^6+d(2/m)^6

is correct. Minimality and good-set cancellation imply

integral_{E_lambda} W(Dy)<=C_G |E_lambda|,
where E_lambda={M(|D(y-G)|)>lambda}, and 0<lambda<=m/(2C_Omega).

This is a genuine finite, orientation-preserving competitor construction for every original minimizer. It does not require topological injectivity or a stress equation. It also does not give this estimate at arbitrarily high truncation levels, nor on arbitrary subsets of E_lambda. Its fixed upper ceiling is exactly what blocks the proposed distribution-function or reverse-Hölder bootstrap. For low thresholds the bad set may be the entire domain. The result corrects any overbroad claim that no admissible additive truncation exists, while leaving the high-level and localized replacement problem open.

## 5. Constitutive spectrum, conformal subclass and ellipticity

The exact principal-stress identity was checked. If C=F^T F has eigenvalues x_i, S=sum x_i, T=sum_{i<j}x_ix_j, and U=F^T DH(F) for the positive-degree energy H, then

u_i-u_j=(x_i-x_j)[6aS²+3b sqrt(T)x_k].

Thus |dev U|>=6aS²|dev C|. The ensuing anisotropy dichotomy is correct. The exact lane's sharper tracefree determinant formula also passes: with tau=|dev U|/(6aS³)<1/sqrt(6),

J² >= S³ (1-sqrt(6)tau)(2+sqrt(6)tau)²/108.

It controls determinant relative to the gradient scale under a stress-isotropy condition. Neither the stress condition nor a positive lower gradient scale has been obtained for general minimizers.

For the exact conformal subclass F^TF=lambda²I, inner stationarity reduces to the distributional constancy of

3d lambda^{-6}-(27a+3sqrt(3)b+c)lambda^6.

This strictly decreasing function determines one positive constant lambda on the connected domain. Therefore J is constant and positive almost everywhere. No Liouville theorem or unproved smoothness is needed. The subclass restriction is essential.

The rank-one Hessian formula and its isotropic minimum/maximum also pass independent calculation. At F=tI, the minimum is

mu(t)=(54a+3sqrt(3)b)t^4,

and the maximum is

Lambda(t)=(126a+10sqrt(3)b+2c)t^4+6d t^{-8}.

The condition number grows like t^{-12}; the shear stiffness itself tends to zero. The determinant barrier therefore does not imply uniform rank-one ellipticity across strong isotropic compression. These are constitutive matrix facts, not examples of matrices actually reached by a singular minimizer.

## 6. Coupled variations and ordinary-equilibrium thresholds

### 6.1 Stress orientation and safe finite differentiation

With primal Piola stress Pi, T=Pi F^T, E=WI-F^T Pi, and inverse S=DV(H), exact differentiation gives

S=K E F^T, S H^T=K E,
H^T S=K(WI-T), and VI-H^T S=K T.

All evaluations on the inverse side are through the actual inverse. Change of variables cancels K in the safe multiplicative stress integrals. Inverse inner and outer first-order composition identities therefore reproduce the two primal composition identities; they are not a new independent system merely by changing coordinates.

The finite coupled energy is differentiable twice under domination by the original energy. This must be checked through transformed minors, not by separately integrating possibly nonintegrable Piola/Hessian pieces. The barrier and determinant-square mixed coefficients are respectively -6B tr M tr N and -2cJ² tr M tr N. The remaining positive-energy mixed terms have no discardable favorable sign. No reverse-Hölder gain is extracted.

### 6.2 Ordinary inverse equilibrium at w in L^{7/6}

Let w=W(Dy). The exact formula gives

integral_D |S| = integral_Omega |EF^T| <= C integral_Omega w^{7/6}.

If w belongs to L^{7/6}, then F belongs to L^7 and E belongs to L^{7/6}. Pulling a smooth compact target test zeta back as eta=zeta composed with y gives a W_0^{1,7} material test. The full boundary trace and continuity of y ensure its zero trace. Density extends the safe inner equation to that test and gives ordinary inverse equilibrium. No inverse additive-amplitude interval is assumed.

The prior pressure estimate makes Dy in L^7 sufficient for the extra energy moment. It has not proved that gradient gain.

### 6.3 Ordinary primal equilibrium at w in L^{11/6}

From w in L^r one obtains

Dv in L^{(6r+3)/5}(D), and sigma=(T/J) composed with v in L^{(2r+1)/3}(D).

At r=11/6 these are the conjugate exponents 14/5 and 14/9. The test phi composed with v has zero inverse trace and belongs to W_0^{1,14/5}. Extending the safe Cauchy-stress equation by density and changing variables gives ordinary primal equilibrium. The direct bound |Pi|<=C(w^{5/6}+w^{11/6}) ensures Pi is integrable.

This is a derived weak equation, not an assumption that y+t phi has finite energy for all small amplitudes. Dy in L^{11} is a sufficient conditional premise via the pressure estimate. Neither premise is obtained unconditionally.

### 6.4 Sharpness and correct meaning of the thresholds

The anisotropic admissible power family has w comparable to r^{-6alpha}. Its primal Piola component has a uniformly nonzero leading term of order r^{-11alpha}; this disproves every smaller universal energy-moment implication to Pi in L¹. For the inverse stress, unit coefficients and alpha=3/7 give a nonzero leading EF^T coefficient on an entire angular cone, of order r^{-7alpha}, producing logarithmic nonintegrability while w has every moment below 7/6.

These examples are nonminimizers. They prove sharpness of energy-only integrability implications, not impossibility of recovering equilibrium below those thresholds by a genuinely minimizer-specific argument. Ordinary weak equilibrium, even when justified, is not itself the global determinant lower bound.

## 7. Source and reproducibility audit

Primary-source inspection was narrowly applied:

- The actual inverse theorem retains its primal p>3 hypothesis; it is not applied backward to p=9/5.
- The general area formula is used on a good approximate-differentiability/Lipschitz-decomposition set. It supplies measurable weighted fibers without a hidden global N assumption.
- Uhlenbeck's scalar corollary is used only for the reduced weak scalar 6-Laplace equation after removal of the puncture.
- The source screen correctly distinguishes other divergence-identity theorems requiring p>dimension-1, and neo-Hookean relaxation results with thick boundary data and different energies/classes. These are not imported into the frozen inverse class.

The audit reread the relevant primary theorem text and visually inspected Uhlenbeck p.222. Source documents remain inspection material; only public bibliographic/hash metadata is included in authored manifests. No novelty or exhaustive literature-search claim is made.

Checks run independently:

- 48 exact-lane checks passed.
- 22 positivity-lane symbolic checks passed, with unresolved-status flags retained.
- 29 independent audit checks passed, covering weighted-core gaps, scalar critical exponent, inverse matrix orientations, inverse coercivity exponents, reciprocal barrier identities, duality threshold, constitutive spectrum, general rank-one stiffness, and two primary PDF metadata matches.

These symbolic checks supplement the written topology, admissibility, weak-derivative, boundary-flux and compactness proofs. They do not certify global minimality of any singular example.

## 8. Final stopping point

The comparison class has genuinely expanded beyond the previously certified compositions, and the exact smooth-angular weighted-power route has genuinely been closed. Neither fact furnishes an unconditional quantitative gain for arbitrary full-class minimizers. The one-component coercivity, relative-minor excess, spectral constraints and coupled stability still need an admissible replacement or another estimate that controls arbitrary low-Jacobian sets, including boundary collars.

No narrow conditional or structural result here resolves the original benchmark. A positive resolution still requires its whole-domain essential bound for every permitted datum and coefficient choice. A negative resolution still requires a singular map proved globally minimizing in the full original class. Ball's broader adequate-growth question remains distinct from either outcome for E-6322.
