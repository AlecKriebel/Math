# E-6322: independent adversarial review, shared pass 2

Date: 16 October 2026. The frozen target was reread in full. This report audits the pass-2 results against the full finite-energy comparison class, arbitrary positive coefficients, arbitrary permitted smooth diffeomorphic full trace, and an essential Jacobian bound over the entire domain. It does not replace the target by a symmetry class, a homeomorphism closure, an inverse Sobolev class, or a regularized energy.

## Decision

**Accept the reviewed results as rigorous partial progress. E-6322 remains unresolved: this pass proves neither its unconditional assertion nor a compliant counterexample.**

The main advances that survive review are:

1. Every admissible deformation has an actual weak inverse in W^{1,9/5}, with cofactor in L^{9/4}, determinant in L^3, and the complete inverse boundary trace. This closes the weak-inverse-derivative gap expressly left conditional in pass 1.
2. A uniform Dini modulus for the positive-degree constitutive pressure tensor implies a global essential pressure bound, including boundary collars. No continuity or boundary trace of the Jacobian is additionally assumed. The modulus remains an unproved extra hypothesis for general minimizers.
3. Finite admissible material competitors produce both an exact concentric-ball identity and a quantitative whole-boundary collar inequality. Their initially L^1 source term prevents the asserted bootstrap from following just from these inequalities.
4. An Euler obstruction rules out a specified class of exact smooth-angular anisotropic power cores, including all the energy-balanced cases under its hypotheses.
5. One compatible identity-trace homeomorphism simultaneously attains all three inverse moment endpoints. Other explicit examples and regularization calculations isolate several invalid bootstrap steps. None of the exhibited maps is a minimizer.

No fatal mathematical defect remained in the frozen artifacts. The review requested a directional heading clarification in the anisotropic report; the final heading refers to the two lower-exponent components. The source report also clarified that the pass-1 collapsed-segment map is admissible. Neither correction changes a theorem.

## 1. Fixed scope and inherited facts

Write F=Dy, C=cof F, J=det F,

P(F)=a|F|^6+b|C|^3+cJ^2, and B(F)=dJ^{-2}.

For the full class, F belongs to L^6, P and B belong to L^1, and J>0 almost everywhere. Full trace equal to the permitted G gives degree one on D=G(Omega). The pass-1 degree/area-formula argument gives almost-everywhere injectivity, not everywhere injectivity. In particular it does not eliminate exceptional collapsed fibers.

The validated inner stress has the form

E=(P+3B)I-U, where U=F^T DP(F), U is positive semidefinite, and tr U=6P.

Equivalently E=pI+Q(F), with p=3B and Q=PI-U. The distributional identity div E=0 is justified by material compositions. Ordinary additive stationarity is not presumed where the Piola stress might fail to be integrable.

The full density is autonomous in the material variable. Only P is degree-six homogeneous in F: the barrier has degree minus six. Confusing these two meanings of homogeneity would invalidate several proposed growth arguments.

## 2. Actual inverse regularity and the full inverse trace

### 2.1 Primary theorem and its application

Bresciani, Davoli and Kružík, *Existence results in large-strain magnetoelasticity*, AIHP ANL 40 (2023), Proposition 2.5, pp.566–567, proves the W^{1,1} inverse and weak derivative formula for an almost-everywhere injective W^{1,p} deformation with p>3 and positive determinant. Its proof and standing hypotheses were independently inspected in the primary full text. Lemma 2.1 and Remark 2.3 identify the deformed open domain with the topological image. [Primary paper](https://ems.press/content/serial-article-files/28047?nt=1)

The frozen trace makes this image exactly D, including when Omega has holes. Consequently the inverse equivalence class v satisfies

Dv=(Dy)^{-1} composed with v almost everywhere on D.

This is a genuine weak derivative, not merely the definition of a measurable matrix field. The theorem requires neither homeomorphism nor regularity of a pointwise inverse.

### 2.2 Exponents and energy transformation

The change-of-variables and Hölder calculations were independently checked:

- Integral_D |Dv|^{9/5} = integral_Omega |C|^{9/5}J^{-4/5}, bounded using weights 3/5 and 2/5 on |C|^3 and J^{-2}.
- Integral_D |cof Dv|^{9/4} = integral_Omega |F|^{9/4}J^{-5/4}, bounded using weights 3/8 and 5/8 on |F|^6 and J^{-2}.
- Integral_D (det Dv)^3 = integral_Omega J^{-2}.

The bounded range of v supplies its L^{9/5} norm. Thus v is in W^{1,9/5}, not just locally so. If K=det Dv, the transformed energy is the identity

integral_D [a|cof Dv|^6/K^5+b|Dv|^3/K^2+c/K+dK^3].

### 2.3 Collar trace argument

A sufficiently small outward parallel domain Omega-tilde exists inside the neighborhood on which G is a diffeomorphism. This remains valid for holes: the collar is attached on every boundary component, with radius below the common tubular radius. Gluing y to G gives a W^{1,6} map on the larger smooth domain because the complete traces match. It has positive determinant, finite energy, and outer trace G.

Apply the same degree and inverse theorem there. The enlarged weak inverse is equal to G^{-1} in the external target collar. The original target boundary lies strictly inside the enlarged target domain, so uniqueness of Sobolev traces across that smooth hypersurface gives Tr v=G^{-1} on the entire boundary of D. No pointwise continuity of v or trace of Dv is used.

**Accepted boundary:** these are class-level inverse facts. The primal minimizer has not been proved to minimize the transformed energy over every Sobolev map with finite displayed inverse energy and that trace. The admissible inverse comparison class remains the genuine inverses of primal competitors. The exponent 9/5 is below dimension three, and K in L^3 gives no L-infinity bound.

## 3. Global Dini pressure criterion

The positivity report proves the following conditional analytic statement. On a bounded connected C^2 domain, let p belong initially only to L^1 and let Q have a uniform Dini-continuous representative on the closure. If div(pI+Q)=0, then

||p||_infinity <= C [R^{-3}||p||_1 + omega_Q(R) + integral_0^R omega_Q(t) dt/t],

up to a fixed geometric enlargement of R. The constants and R depend on the domain. No pressure trace or pressure boundary condition is present.

### 3.1 No L^2 circularity

On each ball or connected boundary cap U, the Nečas/Bogovskii estimate gives

||p-p_U||_{L^2(U)} <= C ||Q-Q_0||_{L^2(U)}

from the initially L^1 pressure formulation. The input is a negative-norm gradient bound, not testing the distributional equation against an already square-integrable pressure. Breit–Cianchi's equations (1.1)–(1.2) explicitly include initially L^1 scalar functions. [Primary paper](https://arxiv.org/pdf/1401.4885v2)

### 3.2 Uniform boundary geometry

The delicate point is a constant uniform in shrinking caps Omega intersect B_r(b). It is justified. In a uniform C^2 graph chart t>h(z), a ball of radius kappa r centered at height r/2 lies inside the cap. For a segment from x=(z,t) in the cap to a point a in this small ball, the Hessian interpolation error of h is bounded by C L s(1-s)r^2. The height margin contributed by a is at least c s r. For uniformly small r it dominates the error. Convexity keeps the segment inside B_r(b). The cap is therefore star-shaped with respect to a ball of radius comparable to r and has volume comparable to r^3.

After scaling, the support-preserving Bogovskii construction uses a fixed-radius star ball and a fixed surrounding ball. Its operator bound is uniform. The construction and Sobolev mapping were checked in Costabel–McIntosh; the uniformity here is a direct deduction from that construction and the explicit geometric normalization. [Primary manuscript](https://costabel.perso.math.cnrs.fr/publis/PoiBogdeRhv2.pdf)

### 3.3 The boundary-to-point step

The mean-square pressure oscillation on each cap is bounded by C omega_Q(cr). Successive nested cap means therefore differ by that modulus, since their volume ratios are bounded. Dini summability bounds their telescoping sum uniformly in the boundary point and scale. For an interior Lebesgue point x at distance delta from the boundary, B_{delta/2}(x) lies in the boundary cap of radius 2delta centered at a nearest boundary point. Comparable volumes allow comparison of these two means. Ordinary-ball telescoping then reaches p(x). This establishes an essential bound even arbitrarily close to the boundary, without first constructing a pressure trace.

### 3.4 Application and exact limit

For the frozen constitutive tensor, p=3dJ^{-2} and ||p||_1<=3I(G). Hence Dini continuity of Q(Dy) implies the required determinant lower bound. A sufficient special case is Dini continuity of Dy, because on |F|<=M the degree-six tensor is Lipschitz with constant C(a+b+c)M^5. This contains the earlier C^{1,beta} conditional criterion and some slower-than-Hölder moduli.

**Accepted boundary:** the theorem is stronger than an interior estimate, but its Dini premise is additional. No lane obtained that premise, or bounded Dy, from the baseline minimizer inequality. The exact continuous-Q/unbounded-pressure example is an abstract tensor example, not a tensor proved to equal Q(Dy) of any minimizer.

## 4. Finite comparisons: admissibility, signs, and limitations

### 4.1 Exact interior concentric comparison

The proposed piecewise radial material map has core radius factor (1-t)^{1/3}, shell radius satisfying f_t(rho)^3=(1+mt)rho^3-ell t, and is fixed outside B_R. For sufficiently small t of either sign it is bi-Lipschitz, has positive determinant, and agrees across both interfaces. Composing y with its inverse is a full-class competitor. Differentiation is dominated by a fixed multiple of W(Dy), so neither an ordinary Piola equation nor a limiting nonsmooth additive comparison is being smuggled into the calculation.

With s=(r/R)^3, direct differentiation gives the exact identity

B(B_r)=s B(B_R)+(1-s)P(B_r)/3
 + (1/3) integral_{B_R minus B_r} [2(r/rho)^3-s]P
 - (1/3) integral_{B_R minus B_r} (r/rho)^3 U_nn.

All coefficients and the negative sign of the U_nn term pass independent symbolic review. Positivity of U allows its removal to produce the asserted upper bound. The logarithmic potential of P, rather than a higher-integrability norm, remains on the right.

The report also correctly proves that the scalar upper inequality alone cannot self-improve arbitrary P: B=c_0P with 0<=c_0<=1/3 satisfies it for every nonnegative integrable P. Such abstract densities need not arise from a gradient or the constitutive law. This is a limitation of the scalar implication, not a minimizer construction.

### 4.2 Entire-boundary collar comparison

Let delta be the boundary distance inside a tubular collar and f_h the triangular tent supported on [0,2h], with f_h(s)=s up to h. The field eta=-f_h(delta) grad delta is Lipschitz and zero on every boundary component. The finite map Id+t eta acts in normal coordinates by s -> s-tf_h(s), is increasing for both signs of small t, and fixes the endpoints and the entire trace. Thus the full-class material variation is valid although eta is not compactly supported in the open domain.

For sufficiently small h, |D eta|<=2, div eta<=-3/4 in C_h, and div eta<=5/4 in the remaining collar. Since |PI-U|<8P, the justified stationarity identity yields

0 <= 16P(C_{2h})-(9/4)B(C_h)+(15/4)B(C_{2h} minus C_h).

Rearrangement gives exactly

B(C_h) <= (5/8)B(C_{2h})+(8/3)P(C_{2h}).

The signs, constants, curvature terms, and all-boundary admissibility pass. Because P is only in L^1, the displayed estimate supplies no uniform positive power decay of the source, much less an essential lower bound for J on thin sets.

## 5. Exact anisotropic cores and conditional C² exclusion

### 5.1 Smooth-angular power core

Consider only the exact ansatz y_i=r^{alpha_i}phi_i(theta), with positive ordered exponents, C^2 angular data, and uniformly positive angular Jacobian j, so J=r^gamma j with gamma=alpha_1+alpha_2+alpha_3-3>0. The theorem is not an assertion about unspecified asymptotic tangent maps.

The local degree argument for a direction where phi_1=phi_2=0 is valid. The angular vector never vanishes, because a simultaneous zero would force the radial column of Dy and thus its determinant to vanish. The origin is an isolated zero. Small nonzero images of punctured points are regular values with finitely many preimages and positive local Jacobian signs; hence the degree inside a sufficiently small target ball is positive. A small point on the third target axis therefore has a preimage, giving the desired direction.

There the first two gradient rows are tangent to the sphere, so the third cofactor row is a nonzero radial vector. Piola's identity gives the barrier's third divergence component as a nonzero constant times

r^{alpha_1+alpha_2-3-3gamma}.

The positive terms' third-row divergence orders are respectively

r^{4alpha_1+alpha_3-6}, r^{3alpha_1+alpha_2+alpha_3-6}, r^{2alpha_1+2alpha_2+alpha_3-6}.

The cofactor estimate correctly uses that varying the third gradient row changes only the first two cofactor rows. The least positive exponent minus the barrier exponent is

eta=2(3alpha_1+alpha_2+2alpha_3-6).

When eta>0, the nonzero barrier term cannot be canceled near that ray. Ordinary additive stationarity is legitimate on compact subdomains of the punctured core, where J is bounded away from zero. No ordinary Euler equation across the singular point is needed.

Under the balanced relation alpha_1+alpha_2+alpha_3+3alpha_1=6, the gap becomes 2(alpha_3-alpha_1)>0. Equality of all exponents would force gamma=0, contrary to the assumptions. Thus these balanced exact cores are excluded, even without affine traces on all centered spheres.

**Accepted boundary:** this does not cover arbitrary angular degeneracy, rough angular data, logarithmic or other asymptotic corrections, boundary singularities, or general minimizers.

### 5.2 Direct C² criterion

If a minimizer already belongs to C² on the closure, H=P is C² on all matrices. On {J>0}, additive stationarity and Piola give

grad(J^{-2})=(3d)^{-1}F^T div DH(F).

The right side is uniformly bounded. A finite polygonal path from a positive-J point cannot reach a first zero, since J^{-2} would diverge along a finite path with bounded derivative. Connectedness excludes interior zeros. The finite intrinsic diameter of a bounded connected smooth domain supplies a global bound; equivalently one can exclude each boundary zero by a finite interior path followed by an inward normal segment and then use compactness. The conditional proof is correct, but no C² regularity is established for arbitrary minimizers.

## 6. Endpoint examples and failed shortcut proofs

### 6.1 Sharp simultaneous inverse moments

The exact lane's single map on B_1 is

y=(L(r)x_1,L(r)x_2,L(r)^{-5}x_3), L=r^{-1/2}[log(e/r)]^{-kappa}, 1/6<kappa<1/2.

Independent differentiation gives Dy=diag(L,L,L^{-5})(I+w tensor n), with uniformly bounded invertible second factor and J comparable to L^{-3}. Hence |Dy| is comparable to L, |cof Dy| to L², |(Dy)^{-1}| to L^5, and the inverse cofactor to L^4. The sphere images are nested ellipsoids: both relevant semiaxes increase strictly from zero to one. The map is therefore a genuine identity-trace homeomorphism, not just a formal diagonal matrix field.

The only critical energy integral is integral dr/[r log(e/r)^{6kappa}], which converges. Inverse target integrals reduce to integral r²L^{5p-3}, integral r²L^{4s-3}, and integral r²L^{3t-3}. Their exact endpoint exponents are 9/5, 9/4, and 3, all attained simultaneously; every larger exponent diverges. The weak derivatives extend across the isolated target point by vanishing integration-by-parts boundary terms.

This proves sharpness of the class-level estimates. It does not prove sharpness for minimizers: strict convexity and null-Lagrangian identities make the identity the unique full-class minimizer for these data.

### 6.2 Hard truncation and composition

For the power family (r^{-alpha}x_1,r^{-alpha}x_2,r^{5alpha}x_3), 1/3<=alpha<1/2, finite energy holds, but P/J is nonintegrable. A formal isotropic material derivative with determinant k transforms the density into P/k+k³B. Setting k=J/epsilon on small-J points gives an infinite positive contribution epsilon P/J for these admitted maps. This defect occurs before solving the separate gradient-compatibility problem for that matrix field.

A fixed bi-Lipschitz composition also preserves gradient L^p membership, as shown by the explicit two-sided norm and Jacobian bounds. It cannot directly truncate a genuinely nonintegrable tail. This does not imply that stationarity or minimality under compositions has no regularizing consequences.

### 6.3 Pressure and reverse transfer

The compactly supported logarithmic cylindrical shear has J between 1/2 and 3/2, finite energy, and gradient in no L^{6+delta}. It proves that all inverse-J moments do not algebraically bootstrap the gradient backward. The continuous tensor example with p=log log(e²/r) solves grad p+div Q=0, has all finite pressure moments, and has unbounded pressure. Its tensor has a nonsummable logarithmic modulus; subtracting a constant identity tensor even makes it negative definite. Both examples have their proper scope: the shear is nonminimizing, and the pressure tensor is not shown to be constitutive.

### 6.4 Regularization and upper growth

The tangent continuation h_epsilon of J^{-2} is finite and convex, but removes the orientation constraint. Its energy controls the measure of {J<=epsilon} and the negative determinant integral, without making each regularized minimizer admissible for the original problem.

Along -tI, with A_0=27a+3sqrt(3)b+c, any upper bound W_epsilon<=L|F|^6+C_epsilon at fixed L requires

C_epsilon >= d² epsilon^{-6}/(27L-A_0)+3d epsilon^{-2}.

This lower bound is the exact optimum over all matrices: the minor inequalities bound H(F) by A_0(|F|/sqrt(3))^6 and |det F| by (|F|/sqrt(3))^3, while the negative conformal ray attains both inequalities and the maximal regularized barrier. For L<=A_0/27 the supremum is infinite. The optimizer and constants pass the symbolic checks. The barrier rank-one Hessian near diag(1,1,epsilon) also grows as 6d epsilon^{-4}. Standard p-growth or upper-ellipticity estimates cannot simply be passed uniformly to the limit while ignoring these quantities. These are obstructions to the stated methods, not an impossibility theorem for every regularization scheme.

## 7. Source applicability and verification

The regularity screen correctly separates precise primary theorem checks from abstract-only or second-hand leads. Independent spot checks included Scheven–Schmidt Theorem 2.4 and its upper bound (2.12), Carozza–Passarelli di Napoli Theorems A/B, Guerra–Tione Theorem 1.7, and Kalayanamit Theorem 2.5. None can be substituted into the frozen problem with its missing hypotheses removed.

In particular, the complete target density is unbounded along bounded matrices diag(1,1,epsilon), and even its high-gradient ratio W/|F|^6 diverges along diag(L,L,L^{-m}) for m>5. The required finite/asymptotic upper p-growth in the inspected Scheven–Schmidt theorem therefore fails. [Primary preprint](https://cvgmt.sns.it/media/doc/paper/1765/asyI.pdf)

Other screened results have different dimensions, finite determinant densities, extra regularity, small-data or incompressibility restrictions, or only interior/partial conclusions. The screen expressly does not claim an exhaustive literature search or novelty certification. All nine downloaded primary PDF byte counts and hashes in its metadata manifest were independently checked. No primary source document or text extract is included in this authored audit.

Reproducible checks run during review:

- Exact lane: 34 symbolic checks and 3 quadrature checks passed.
- Positivity lane: its differentiation, optimizer, interpolation-sign, and Hessian checks passed; unresolved-status flags remained false.
- Independent audit script: 24 checks passed, covering exponent gaps, radial and collar coefficients, compatible-matrix identities, inverse Hölder weights, an independently derived abstract pressure identity, and nine source metadata matches.

These checks supplement the written admissibility, topology, boundary, and functional-analysis arguments. Symbolic agreement is not treated as proof of minimality.

## 8. Remaining bridge and next admissible conclusions

The pass establishes more of the correct inverse framework, a stronger conditional pressure target, and several rigorously admissible comparisons. It still lacks an unconditional improvement or geometric mechanism for the actual minimizer strong enough to exclude low-Jacobian sets throughout Omega.

A later proof would need, for example, a justified constitutive modulus/regularity estimate, a determinant-preserving replacement with controlled distortion costs that genuinely improves P, or another argument reaching an essential bound without that regularity. A later counterexample must prove full-class global minimality for permitted data; producing a finite-energy degenerating homeomorphism is insufficient. Transferring to a generic inverse Sobolev class would require a separate comparison-class theorem.

No inference here resolves Ball's wider search for adequate growth assumptions, and failure of one route does not falsify E-6322. The accepted status remains **partial results; original benchmark unresolved**.
