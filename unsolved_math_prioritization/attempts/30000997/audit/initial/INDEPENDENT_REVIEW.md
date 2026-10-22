# Independent proof audit: MTW local separation, problem 30000997

Review date: 2026-10-03 UTC. Frozen author packet: five turns, immutable commit `3f5d67dba43eac1c01a48a3481d8153b319fee02`, branch `research/30000997-mtw-work-in-progress`, repository `AlecKriebel/Math`, directory `unsolved_math_prioritization/attempts/30000997`.

## Verdict

**Accept the retained local and equatorial mathematical results, subject to two mandatory clarifications below. Do not accept this as a solution of the global-manifold implication.** The explicit positively curved complete sphere does fail NNCC and has strictly positive MTW on all nonzero null pairs at every non-antipodal equatorial pair. The resulting local product-domain separation is genuine. Global A3w for that sphere is neither proved nor disproved by this packet. No novelty certification is made.

No fatal sign, factor-in-the-packet, Jacobi, angular-parametrization, smooth-pole, or equatorial-minimization error was found. The packet consistently calculates the coordinate tensor S defined in its source gate. Its relation to a cited paper's differently normalized curvature needs to be explicit. TURN_5's initial hypothesis also needs repair, although its subsequent formulation on the interior injectivity domain already has the correct scope.

This is a proof audit, not a sixth author search. Original author files were not edited. No remote write was performed.

## Mandatory corrections before any reviewed publication

1. **State the tensor normalization explicitly in a current reading note.** For c=d²/2, write
   S(v;u,w) = -D²_v Hess_p c(p,exp_p v)[w,w](u,u).
   It equals the coordinate MTW expression displayed in the packet, evaluated on `(u, D exp_p(v) w)`. The cited Kim–McCann paper's Lemma 2.5 uses cross_KM = -2 ∂⁴c, so under that paper's convention **cross_KM = 2S**. Consequently the finite witness is S=7/10−8/π², whereas cross_KM=7/5−16/π². The diagonal controls are 2K/3 and 4K/3, respectively, on orthonormal transverse vectors. Nullity and all signs are identical. This is a clarification of convention, not a correction to the computed value of the packet's S. The OWR displayed coordinate definition and Kim's 2019 Definition 2.10 agree with the packet's derivative normalization.
2. **Repair the opening hypothesis in TURN_5 and every generalized smooth-cost invocation.** Replace “a minimizing nonconjugate tangent v” by “v in the interior tangent injectivity domain, equivalently the geodesic to exp_p(v) is uniquely minimizing and nonconjugate.” A minimizing nonconjugate geodesic can terminate at an ordinary cut point with a second minimizer. At such a point the squared distance need not be differentiable. Without uniqueness, the displayed Jacobi operator is at most a chosen-branch extended Hessian. No repair to the actual equatorial witnesses is needed: uniqueness is proved separately by round-metric comparison below.

Add these as a dated correction/reading note rather than rewriting the historical turns. Keep the global status exhausted/unresolved. The review does not authorize replacing “global A3w unverified” by a global result.

## Claim-by-claim audit

### 1. Source scope and conventions: accepted with the normalization clarification

The official [OWR report, printed p. 1752](https://ems.press/content/serial-article-files/46174) asks the perpendicular-to-full implication for Riemannian squared distance without explicitly specifying completeness or the whole cut complement. Its surrounding transport hypotheses do not themselves settle that quantifier ambiguity. The [cited Kim–McCann paper, §1.2](https://www.math.toronto.edu/mccann/papers/RiemSub.pdf) explicitly adopts complete manifolds and N=M×M minus the cut-locus relation. Thus the packet correctly distinguishes a restricted-domain negative example from the complete/global question, rather than silently substituting one for the other. The global interpretation is a supported convention, not a claim that the short OWR sentence literally lists all those hypotheses. Neither densities nor mutual c-convexity are used in this geometric audit.

Kim–McCann Lemma 2.5 and its diagonal formula verify the factor-two distinction. Its Theorem 1.2(3–4) also confirms the product obstruction's prior-art status. These convention differences must not be conflated with the harmless positive scaling between the costs d² and d²/2.

### 2. Hessian, source/target, and mixed nullity: accepted

Fix an off-cut pair q=exp_p(v). Let y(t)=exp_p(v+tw), η=y'(0)=D exp_p(v)w. The identity -D_p c(p,y(t))=g_p(v+tw,·) implies

c_{i,bar j}u^i η^bar j = -g_p(u,w).

Differentiating twice gives c_{i,bar j}y''^bar j+c_{i,bar j bar k}η^bar jη^bar k=0. Substitution in -d²/dt²[c_{ij}(p,y(t))u^iu^j] gives exactly

(-c_{ij,bar k bar l}+c_{ij,bar a}c^{bar a b}c_{b,bar k bar l})u^iu^jη^bar kη^bar l.

Replacing coordinate Hessian by covariant Hessian adds a Christoffel multiple of D_p c, which is affine in v; its second v-derivative vanishes. Thus the packet's formula is coordinate-invariant and has the stated sign. Nullity is source-tangent orthogonality after applying `(D exp)^{-1}` to the endpoint vector, not ordinary endpoint/parallel-transport orthogonality.

On a surface, take a parallel unit normal along the geodesic. The boundary Jacobi field with values u_perp at p and zero at q has scalar coefficient

Z(s)=C(s)−[C(r)/J(r)]J(s),

where C(0)=1,C'(0)=0,J(0)=0,J'(0)=1. Second variation gives H=−r Z'(0)=r C(r)/J(r). The longitudinal eigenvalue is 1, and symmetry eliminates the mixed longitudinal/transverse entries. This proves A(v)=I+(H(v)−1)(I−vvᵀ/|v|²).

The source orientation matters: using r J'(r)/J(r) would instead be the endpoint-centered Hessian and is generally wrong here. Independent series controls give the cubic curvature-gradient coefficients −K₁/12 for rC/J and −K₁/4 for rJ'/J. They coincide on constant curvature, so a round-sphere-only check would miss this error; the packet uses the correct one.

### 3. TURN_1 local plane: accepted

Solving the scalar Jacobi equation by a polynomial-residual calculation independently gives

rC/J=1−K₀r²/3−K₁r³/12−(K₂/60+K₀²/45)r⁴+O(r⁵).

Multiplying by the normal projection gives the packet's A(v) expansion. Smooth Taylor theory, rather than an undifferentiated big-O assertion alone, justifies the two v derivatives. Both displayed metrics are analytic, so there is ample regularity.

For f=(1+x²)^(-1/2), direct warped-metric curvature gives K=(1−2x²)/(1+x²)²=1−4x²+O(x⁴). At p=(0,0), f'=0, so the coordinate frame is orthonormal with zero Christoffel symbols and Hess K(e₁,e₁)=−8, Hess K(e₂,e₂)=0. For u=w=e₁ and v=ae₁+re₂, the area term |u∧v|²=r² is independent of a. Hence

S(re₂;e₁,e₁)=[−8/30+2/45]r²+O(r³)=−2r²/9+O(r³).

The reflection y↦−y makes this expression even in r, upgrading the remainder to O(r⁴). This is a non-null negative pair. At the diagonal, S=(2/3)K|u∧w|²; on unit orthogonal pairs near p it is uniformly positive. Smoothness and compactness of the normalized orthogonal-pair bundle give strict positivity on U×U after shrinking to a relatively compact strongly convex normal neighborhood. This is an actual open product cost domain containing the negative full pair, not merely a prescribed jet.

Completeness is also correct: finite length bounds total x variation; in the resulting bounded strip f has a positive lower bound, hence total y variation is bounded. No finite-length curve escapes compact sets. K(1)=−1/4 gives diagonal null S=−1/6, so the ambient complete plane definitely fails global A3w.

### 4. TURN_2 compact sphere and positive curvature: accepted

At either pole use inward distance ρ. The warp is sinρ+a sin³ρ cos⁴ρ, an odd analytic function with derivative 1 at 0. In polar Cartesian coordinates its squared ratio to ρ² is a smooth even function equal to 1 at 0. This is the standard smooth rotational-pole condition, with no cone angle or boundary. The longitude period 2π is essential and is specified. Both poles satisfy it. Positive warp in the interior makes a smooth metric on S², and compactness gives completeness.

Differentiating -f''/f gives exactly the stated rational expression in z=sin²x. The numerator decomposition is correct; 49z²−6z+6 has discriminant −1140. For 0≤z≤1 and 0≤a<1/6, the numerator is positive and 1≤1+a(z²−z³)≤1+4a/27. The curvature limit at either pole is 1−6a. Thus the asserted strict-positivity range is correct; no assertion of maximality for all real a is needed.

At the equator f⁽⁴⁾(0)=1+24a and K_xx=−24a. Substitution in the independently checked local formula gives (2/45−4a/5)r²+O(r⁴). It is negative precisely for a>1/18 at this order; for a=1/10 the coefficient is −8/225. Together with local diagonal null positivity this proves the claimed compact, globally positively curved, local separation. It supplies no global A3w certificate.

The positive-concave-warp obstruction on R×R is sound: global A3w implies K≥0 on the diagonal, hence f''≤0. A positive concave function on all R is constant, since any positive or negative derivative forces eventual negativity at one end. Completeness is not a substitute for this diagonal calculation.

### 5. TURN_3 equatorial minimizing domain: accepted

The comparison proof establishes uniqueness, not just existence. As tensors g_a≥g_round because f_a≥cos x. For equatorial endpoints separated by the shorter longitude angle 0<r<π, every curve satisfies L_a≥L_round≥r. The shorter equatorial arc has L_a=r, hence is minimizing. Any other g_a minimizer would have round length r and therefore be the unique round minimizing arc between these non-antipodal endpoints. No second distinct minimizing path exists.

Along this arc K=1, so the transverse exponential Jacobi factor is sin r/r and does not vanish before π. Thus the arc is both uniquely minimizing and nonconjugate. The pair belongs to the actual squared-distance smooth domain. Smoothness on a neighborhood follows from the inverse function theorem and stability of this unique minimizing branch. At r=π the argument changes; that case is deliberately excluded. This is not a claim about off-equator cut loci.

### 6. TURN_3 boundary variation and full tensor: accepted

Use affine time t∈[0,1], initial velocity (b,r). The first latitude variation X=∂_b x|₀ solves X''+r²X=0, X(0)=0,X'(0)=1; hence X=sin(rt)/r. Reflection gives x_b=bX+O(b³). Constant squared speed is r²+b² and K=1+(κ/2)x²+O(x⁴), so

V_b=(r²+b²)K(x_b)=r²+b²[1+(κ/2)sin²(rt)]+O(b⁴).

No r² factor is missing. Let Z_b''+V_bZ_b=0, Z_b(0)=1,Z_b(1)=0. H=−Z_b'(0). For a variation δZ, the Wronskian satisfies (ZδZ'−Z'δZ)'=−δV Z². The endpoint boundary terms yield δH=−∫₀¹δV Z²dt. Thus

H_bb=−2I₀−κI₁,
I₀=(r−sin r cos r)/(2r sin²r),
I₁=[r(1+2cos²r)−3sin r cos r]/(8r sin²r).

These closed forms follow independently by product-to-sum integration; they verify the author's integrals and their small-r limits. Define k=1−r cot r and h=r cot r. Differentiating A independently along z(λ)=re₂+λw gives, for arbitrary u=(u₁,u₂), w=(w₁,w₂), the full expression

S = F u₁²w₁² + P u₁²w₂² + Q u₂²w₁² + T u₁u₂w₁w₂,
F=2I₀+κI₁−2k/r²,
P=−h''=2csc²r k,
Q=2k/r²,
T=−8I₀+4k/r².

All other monomials vanish by the equatorial reflection/radial structure. Substituting u=(cosθ,sinθ), w=(−sinθ,cosθ) gives exactly the packet's quartic, with R=F−T=10I₀+κI₁−6k/r². In two dimensions this parametrizes every unit orthogonal pair up to an irrelevant sign of w; separate positive length factors cover every nonzero null pair. No direction is omitted.

For 0<r<π, k>0. The inequalities 0≤I₁≤I₀ follow pointwise in the integrands. The remaining inequality k/r²<I₀ is equivalent to F₀=r²+r sinr cosr−2sin²r>0. Here F₀(0)=F₀'(0)=0 and F₀''=4sinr(sinr−r cosr)>0. Therefore P,Q>0 and, for −4<κ<0,

R>10I₀−6I₀+κI₀=(4+κ)I₀>0.

This proves strict null positivity at every such equatorial pair. The signs are exact throughout the open interval; no discretization is used. The diagonal follows separately from K=1.

### 7. TURN_4 finite witness and open product neighborhood: accepted

At a=1/10, κ=−12/5 and r=π/2, one has h=0,I₀=1/2,I₁=1/8,H_bb=−7/10. Therefore F=S(v;e₁,e₁)=7/10−8/π²<0. Since the normal frame is parallel along the equator, D exp_p(v)e₁=(sin r/r)∂x=(2/π)∂x at q, exactly as stated. The witness is not the same numerical evaluation on an unscaled unit endpoint vector.

The null quartic is 2c⁴+(8/π²)s⁴+(47/10−24/π²)c²s². The mixed coefficient is positive. More quantitatively, it exceeds 2(8/π²), since π²>9 gives 47/10−40/π²>0. Thus the normalized null minimum is exactly 8/π², attained at c=0. This yields a uniform positive margin at the pair.

To pass to a neighborhood, work in a local orthonormal source frame and the smooth inverse-exp coordinates around the uniquely minimizing pair. The unit orthogonal-pair circle is compact. Uniform continuity keeps the null tensor positive on a sufficiently small product U×V contained in the smooth-cost domain. The negative full witness is already in that product; indeed it also persists after continuous extension of u,w and shrinking. This establishes a genuine local product-domain implication failure. It does not assert one common-radius neighborhood of the entire noncompact equatorial off-cut slice, and it does not cover all of M×M minus Cut.

The product principle is correct and already known: S is additive for summed factor costs, while product nullity is g_M(u,w)+αβ=0. Choose α=1,β=−g_M(u,w) for any negative full pair; the flat factor contributes zero. Thus M×R is A3w iff M is NNCC on the full product smooth domain. A flat circle gives the same local null witness using a displacement below its injectivity radius, including zero. This construction obstructs rather than repairs the missing antecedent.

### 8. TURN_5 general quartic: accepted after off-cut repair

The nine displayed second derivatives of the 2×2 Hessian matrix are correct. An independent derivation differentiates the scalar expression

|u|²+(H(z)−1)(u₁z₂−u₂z₁)²/|z|²

along z=(−λ sinθ,r+λ cosθ), without using the author's matrix-derivative calculation. It gives all five coefficients, including the odd terms +2H_bs cos³θ sinθ and +(4H_b/r)cosθ sin³θ. Their signs and factors are correct. No reflection symmetry is available for a general source/endpoint pair.

For cosθ≠0, divide by cos⁴θ and put t=tanθ. The remaining vertical direction has value Q. Thus the real-quartic nonnegativity criterion is valid. Explicitly listing Q≥0 is harmless even though it follows from nonnegativity of a degree-at-most-four polynomial on all R. Homogeneity covers arbitrary lengths; r=0 requires the separate smooth diagonal limit. The concluding formulation v∈D_p uses the correct off-cut domain, unlike the insufficient wording at the start.

This is a reformulation, not global progress beyond a criterion. The packet establishes neither the relevant injectivity domains nor the quartic signs on them away from the equator.

### 9. Diagnostics: appropriately noncertifying, with one terminology warning

The ten author SymPy controls pass when replayed from a copy. They check encoded identities only. Twenty independently implemented controls also pass, including source-versus-target sensitivity, pole jet, explicit integrals, all-direction full tensor, odd quartic coefficients, and the endpoint normalization. An independently coded local ODE finite difference gives H_bb≈−0.700000849, −0.700000214, −0.700000051 at steps 0.002,0.001,0.0005. This is a consistency diagnostic at the analytically certified pair, not part of the proof.

The author JSON confirms the reported latitude-0.5 sign reversal under step refinement. The two latitude-0.25 shooting diagnostics report candidate lengths about 2.9996742 and 2.9996881 versus 3. Those are not validated interval bounds, exact endpoint matches, or proofs of nonminimization. Their use to reject the original coarse samples as *certified evidence* is appropriate. They do not establish the opposite global statement either.

The program field `safe_no_conj_poles` is misleading if read literally: it tests numerical solver success, a positive endpoint Jacobi value, and sampled pole avoidance. A positive endpoint value alone does not prove absence of earlier zeros or global minimization. Treat this field as a heuristic filter, not a certificate. Prefer a corrective note saying “numerically suspected nonminimizing branches,” especially wherever a brief summary drops the longer disclaimer. No numerical result is needed for any accepted theorem above.

### 10. Prior art and remaining exclusions

The [Figalli–Rifford–Villani primary paper](https://people.math.ethz.ch/~afigalli/papers-pdf/On-the-Ma-Trudinger-Wang-curvature-on-surfaces.pdf), §2 and §6.1, already develops Jacobi-Hessian formulas, two-dimensional angular MTW expressions, and curvature variations along symmetry geodesics on surfaces of revolution. Its special quarter-period formula independently matches the present mixed null coefficient after changing basis and normalization: m⁽⁴⁾m−(m'')²=24a gives 5−24/π²−3a. This agrees with 47/10−24/π² at a=1/10.

That overlap supports the calculation and prevents claiming the method itself is novel. The review did not establish whether this particular elementary warp, exact witness, local separation statement, or whole equatorial positivity interval has appeared previously. Neither absence from a bounded search nor an independently correct proof certifies priority. No new survey claiming the global conjecture is still open as of today is made here; the reviewed packet itself does not resolve it.

## Provenance and preservation

- All 17 entries in FINAL_AUTHOR_MANIFEST.json match local byte lengths and SHA-256 hashes.
- The remote immutable directory has 19 entries. Eighteen, including all five turns, proofs, scripts, numerical data, manifest, and summary, match independently computed local Git blob hashes. Remote TURN_STATE.json is 226 bytes; the local operational version is 266 bytes. Both record five turns and an exhausted/unresolved global outcome, but their ancillary fields differ. Neither was edited. This mismatch must not be described as a byte-identical whole-directory snapshot.
- The live branch ref was read and confirmed at the stated immutable commit during the audit. Remote reads only.
- The original replay was run in the review directory so it could not overwrite the author's receipt. The original author tree remains unchanged.
- Input binding, correction list, independent controls, receipts, and a review manifest accompany this file. They certify the scope of this audit, not global A3w, complete cut loci, novelty, or a solved original problem.

## Final disposition

Retain TURN_1–TURN_4 partial results and TURN_5's correctly scoped criterion. Add the normalization and off-cut/uniqueness note, clarify the heuristic numerical flag, and retain the local-versus-global distinction. Publication should call this an independently audited partial note with corrections, never a complete counterexample to the global A3w⇒NNCC implication.
