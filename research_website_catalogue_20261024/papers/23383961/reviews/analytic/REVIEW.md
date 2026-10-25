# Independent analytic review: support-slit monotonicity

Reviewer: GPT-6.1 Sol, Ultra. Review completed 25 October 2026 UTC.

**Analytic verdict: the published Theorem 1 is verified relative to the stated classical foundations. No substantive proof defect or remaining analytic gap was found. This is an analytic review, not publication or priority clearance.**

## Exact object, claim, and success criterion

The object reviewed is *Nonmonotone Argument and Radial Angle of a Support Slit*, Alec Kriebel, version 1.0, dated 14 October 2026, Zenodo record 23383961. The actual five-page reader has SHA-256 `a6d227d606fda3e68adc6db4eab462ee3f12b0544a201121b5c3a21aa5099e3d`. Its supporting ZIP has SHA-256 `58853fd56272184efe8232c58c356b1a669ba43032e3c4f35e4b17e317898f51`; current TeX has SHA-256 `c4e557a58999b938578eb105c03d7224f087c04f273dbbd86e09ab45b855a4b3`. I read all five PDF pages, visually inspected each rendered page, and read the complete current TeX. No mismatch affecting the claims or proof was found.

Let S consist of normalized analytic univalent maps on the disk. For epsilon = 10^-24 and eta = 10^-12, set L(f) = a2 + i epsilon (a4 - 3a3). The exact claim is that global maximizers of Re L exist and **every** maximizer has an omitted analytic arc with nonmonotone continuous polar argument, signed outward radial angle, and ordinary unsigned outward radial angle. A proof merely constructing a positive quadratic-differential trajectory would not establish this. The required check is that the trajectory is part of each actual omitted slit, with sufficient uniform estimates independent of maximizing selection or uniqueness.

The strongest verified result is precisely that theorem. The proof provides strict endpoint signs on an actual omitted subarc, not an approximate extremizer or a numerical candidate. The ordinary angle conclusion also follows independently of an assumed implication from signed-angle nonmonotonicity.

## Primary classical inputs and their hypotheses

The primary-source read ledger records exact paths and hashes. I inspected actual theorem bodies, not only citation snippets.

* **Compactness and admissible functionals.** Pfluger (1971), p.3, defines the locally uniform topology, states compactness of S, and gives the coefficient-kernel functional class. The present finite coefficient functional has kernel K(z) = z^-3 - 3i epsilon z^-4 + i epsilon z^-5. It is in that class. Cauchy's coefficient formula also directly proves continuity on H(D). Koebe and the identity give Re L equal to 2 and 0, respectively, so its real part is nonconstant.
* **Actual support-slit geometry and sign.** Duren (1981), actual pp.352–355, gives the analytic omitted arc, increasing modulus from a finite tip to infinity, and Q(w)dw^2 > 0 with Q = L(f^2/(f-w))/w^2. His signed radial angle is arg(w'/w) for outward parametrization. Pfluger §§3.3 and 4.1–4.5 gives the original geometry, nonzero leading coefficient at infinity, single analytic boundary arc, and radial ordering. His differential uses the opposite sign. The current manuscript consistently uses Duren's positive convention. The hypotheses apply to every global maximizer of this nontrivial finite coefficient functional. I read Duren's entire 14-page article text (the cached PDF also has a cover), and Pfluger's relevant definition and theorem/proof sections; the critical theorem pages were also visually inspected.
* **Coefficient bounds.** De Branges (1985), pp.137–138, states the normalized Bieberbach conclusion. Only n=2,3,4 is used. I credit this standard theorem; I have not independently re-proved its full proof.
* **Area theorem and boundary distance.** Pavlović–Peláez (2011), Theorem 1, p.909, restates the classical area theorem for an analytic phi with phi(z)/z meromorphically univalent. It applies here with phi(z)=z/g(z)=H(z^2), since g is univalent. Rearranging its coefficients gives sum (2n-1)|c_n|^2 <= 1. Equation (1.4), p.910, has the required direction dist(F(z),boundary Omega) <= (1-|z|^2)|F'(z)| for a simply connected proper conformal image. I also independently derive that upper bound below. This source is a restatement, not attribution of historical origin.
* **Target and angle conventions.** Hayman–Lingham arXiv:1809.07200v2, printed p.143/PDF p.144, asks the two questions exactly as stated. Its 2018 update does not establish present openness. Brown (1979), actual p.375 and the proof on pp.379–380, concerns point evaluations and uses A=arg(w/w'), the negative of the signed outward convention here. I read the complete article text and visually checked p.375. It supplies a restricted positive family, not an obstruction to the present coefficient example.

These sources justify application of the central imported geometry. The remaining complex-analysis tools—Cauchy's formula, analytic logarithms, Schwarz's lemma, Rouché, local inversion, and local natural coordinates—are standard foundations. No assumption that every positive trajectory is an extremal slit is credited.

## Independent reconstruction of the proof

### Uniform coefficient and tail controls

Comparison with Koebe gives Re a2 >= 2-13 epsilon because |a4-3a3| <= 4+9. Combining |a2|<=2 with that lower bound gives |a2-2|^2 <= 52 epsilon and 0<=1-|a2|^2/4<=13 epsilon. In particular |a2-2|<8 eta. These inequalities hold separately for every maximizer.

The normalized square root g(z)^2=f(z^2) exists: f(z)/z has no zeros in the simply connected disk, and the normalized root of its composition with z^2 is even. Thus g is odd. If g(z1)=g(z2), injectivity of f gives z1=±z2; oddness in the negative case forces g=0 and hence z1=z2=0. Consequently the reciprocal exterior map is univalent and its first coefficients are -a2/2 and 3a2^2/8-a3/2. The area theorem gives |a3-3a2^2/4|<=2 sqrt(13/3) eta<5 eta, hence |a3-3|<29 eta. For A=2a3+a2^2-6a2 and B=3a2-3 this yields |A+2|<106 eta and |B-3|<24 eta. The identity A+2=2(a3-3)+(a2-2)(a2-4), together with |a2-4|<=6, checks the first constant.

Writing H=sqrt(z/f(z))=1-a2 z/2+sum c_n z^n gives the full tail bound sum_{n>=2}(2n-1)|c_n|^2<=13 epsilon. Weighted Cauchy–Schwarz on |z|<=2/3 gives |H-(1-z)|<5 eta and |H'+1|<10 eta. I checked the two tail bounds 16/135<1/4 and 56/25<9/4, including n^2/(2n-1)<=n. Differentiated series converge inside the disk, so no boundary convergence premise is needed.

### The actual tip bound

At z*=-2/3 the baseline H0=5/3 and k(z*)=-6/25, k'(z*)=9/125. The stated H controls imply 3/2<|H|<11/6, |H+H0|<7/2, and |H^2+HH0+H0^2|<11. Direct division gives |f-k|<2 eta. For f'=(H-2zH')/H^3, the numerator error is below 19 eta, contributing below 6 eta; the inverse-cube error contributes below 2 eta. Thus |f'-k'|<8 eta.

For any disk of radius rho contained in Omega about f(z), compose the inverse map on that disk with the disk automorphism sending z to zero. Schwarz gives rho/[(1-|z|^2)|f'(z)|]<=1. Taking rho to boundary distance proves the required upper bound with the correct direction. A nearest boundary point exists because the boundary is closed and nonempty. Therefore some point of the actual slit has modulus below 7/25+7 eta<3/10. Radial ordering makes the finite tip the minimum. This step does not infer convergence of boundary tips from locally uniform convergence of maps.

### Exact differential, inversion, and actual slit identification

Expanding (f-w)^-1 through coefficient degree four gives

    Q(w)=-a/w^3-b/w^4-c/w^5,
    a=1+i epsilon A, b=i epsilon B, c=i epsilon.

This identity uses the coefficients of f^2, f^3, f^4 and does not presume an explicit extremizer. Under w=-v^-2, direct multiplication by (dw/dv)^2 gives 4P(v)dv^2 with P=a-bv^2+cv^4. On |v|<=3, P=1+i epsilon P0+error, P0=-2-3v^2+v^4, and the error is bounded by 322 epsilon eta. Hence |P-1|<111 epsilon.

The root p=sqrt(P) with positive real part is analytic and nonzero on that disk. From |p+1|>1 follows |p-1|<=111 epsilon. Its primitive G satisfies |G-v|<=333 epsilon. On |v|=3 and |t|<2, |v-t|>1, so Rouché gives one root of G(v)=t, counting multiplicity. Since G'=p is nonzero, these roots give a holomorphic inverse V on |t|<2. Evenness of p gives oddness of G and V. In addition to Rouché, integrating p-1 along any segment in the convex disk directly proves G is injective there.

For 0<t<=7/4, W=-V^-2 is regular, has Q(W)W'^2=4, tends to infinity like -a/t^2, and satisfies |W|>25/81>3/10. If W(t1)=W(t2), then V(t1)=±V(t2); applying odd G gives t1=±t2, proving injectivity for positive parameters.

The actual omitted tail lifts to v tending to zero. Positivity of the actual differential means dG is real and nonzero along the lifted tail, hence Im G is constant; its limit is zero. Its two possible real rays project to the same W by oddness. Thus W agrees with the actual slit near infinity. The set of t for which W belongs to the slit is nonempty and relatively closed. Each such point has radius strictly beyond the actual tip, with separation at least 7/810 between the chosen coarse radius gates. Q is finite and nonzero there. A local root primitive of Q makes both arcs horizontal trajectories and supplies local uniqueness, so that set is relatively open. Connectedness proves the entire candidate interval belongs to the actual slit. This closes the essential realizability step; it never asserts a converse extremality criterion.

Finally Z=tV'/V=(G(V)/V)/p(V), where G(v)/v is the average of p along a radial segment. It follows that |Z-1|<=222 epsilon/(1-111 epsilon)<223 epsilon for all 0<t<=7/4, with no division loss at t=0. Thus Re Z>0, d log|W|/dt=-2 Re Z/t<0, and -W' is indeed the outward tangent.

### Uniform error budget and all angle conclusions

Set d=t+t^3/2-t^5/10 and q=d'-d/t=t^2-2t^4/5. The exact square-root identity in the manuscript bounds the error in p by 161 epsilon eta+(111^2/2)epsilon^2<162 epsilon eta. Integrating gives 486 epsilon eta. Replacing d(V) by d(t), using |d'|<=55 and |V-t|<=333 epsilon, costs 18315 epsilon^2; therefore |V-t-i epsilon d|<=487 epsilon eta.

For V', the complex Taylor remainder of (1+x)^-1/2 is at most 2|x|^2 on |x|<=1/4. Its second derivative has modulus below 4 there, which checks the factor. The three costs are 161 epsilon eta, 24642 epsilon^2, and 20979 epsilon^2, giving |V'-1-i epsilon d'|<=162 epsilon eta. All relevant line segments stay within the convex radius-three disk. No uncertain coefficient is assumed real.

The exact identity

    V(Z-1-i epsilon q)=t R_V' - R_V - i epsilon q(V-t)

then gives |Z-1-i epsilon q|<=1541 epsilon eta+4662 epsilon^2<2000 epsilon eta, since |V|>1/2 and |q|<7 on [1,7/4]. I independently checked each arithmetic absorption, including the products dropped by a naive first-order expansion. Since q(1)=3/5 and q(7/4)=-441/640, the errors leave Im Z(1)>epsilon/2 and Im Z(7/4)<-epsilon/2.

A continuous argument theta of W has theta'=-2 Im Z/t. These opposite strict derivative signs preclude either direction of monotonicity. Both test points are regular interior points of the actual slit; t=7/4 is only the endpoint of the tested parameter interval, not the physical tip.

The signed outward angle is beta=arg((-W')/W)=arg Z. The positive-real branch is fixed globally by Re Z>0. It tends to zero as t decreases to zero, is positive at 1, and negative at 7/4. A nondecreasing function with initial limit zero cannot take the negative value, and a nonincreasing one cannot take the positive value. The limiting value is essential: opposite signs alone would not prove nonmonotonicity. Continuity supplies an interior beta-zero between the two nonzero endpoint values. Thus |beta| has positive values at both ends and zero inside, proving the unsigned conclusion separately. Since |beta|<pi/2, the ordinary outward vector angle is exactly |beta|; inward vectors give its supplement and tangent-line acute angles again give |beta|.

## Adversarial and limiting-case checks

I tested the possible breaks at the actual tip, the pole at infinity, the double-cover sign, branch continuation, a zero of P, a zero of V, orientation reversal, complex coefficient errors, and derivative signs at a subinterval endpoint. The radius gate, disk root bounds, oddness, and local uniqueness resolve these without an additional unsupported claim. Continuous argument lifts differ only by a constant multiple of 2pi and parameter reversal preserves failure of monotonicity.

At epsilon=0 all strict angle sign margins vanish; Koebe's radial slit has zero radial angle. The proof does not claim that its conclusion extends to zero, or to arbitrary larger epsilon. No uniqueness or formula for a maximizing map follows. Central-enclosure numerical trajectories need not themselves be realizable extremal slits; actual realization is established analytically only after starting with a true maximizer.

Tangent-direction reversal is a distinct observable from polar-argument or radial-angle reversal. The supplied analytic angle-distinction construction has monotone theta and beta but changing arg(w') derivative; I checked its exact trigonometric margins. It is not asserted to arise from a support point. This control prevents substitution of a tangent-waver claim for the target theorem, but it does not settle priority.

## Reproducibility, independence, and custody

`independent_controls.py` was written for this review without importing any submitted module. It verifies 21 positive Fraction margins and rejects six targeted changes: dropping the quartic q term, removing -3a3, enlarging eta without reproof, reversing the actual/candidate radius comparison, assuming a strict sign at zero epsilon, and identifying the inward tangent as outward. It also computes the nonlinear natural-coordinate inverse using an independently integrated binomial series and standard-library Decimal complex arithmetic at 100 and 130 digits. All 17 coefficient-enclosure samples have the required endpoint reversal; all three negative controls fail reversal. Normalized endpoint values at the central enclosure are about 0.6 and -0.6890625; the largest precision discrepancy is below 6.2e-99. These computations are supplemental and are not an extremal solver, interval certificate, or proof of the imported theorems.

After full static review, I copied only the selected quantitative and angle scripts into `runtime/quarantine`, together with a byte copy of the legacy proof that the quantitative script hashes as data. The legacy proof body was not read or executed. The selected replays returned 97 and eight successful checks respectively. The entire `run_all.py` was statically reviewed but not run: its other job scripts were outside this analytic execution scope and were not presumed safe from its entry point alone. Old PASS strings and seals are not evidence for the mathematics.

Early independence was preserved: the manuscript and primary-source geometry were used for my derivation before reading the current mathematical support derivations. No sibling current review verdict was read. Legacy audit, acceptance, historical judgment, PRE_GOH, and PRIMARY_AUDIT bodies remain unread. Disclosure: reading the complete current `ROOT_ANALYTIC_DERIVATION.md` for its mathematical support also incidentally exposed its final historical no-gap sentence. The mathematical portion of the quantitative derivation contains incidental old assessment wording. The angle-distinction note contains a historical unread-source statement. None is adopted as evidence or priority assessment; the conclusions here follow from the independent reconstruction above.

All 259 source-tree files were hashed before and after. The file sets and bytes agree. Existing scope files and seals were only read. The original PDF, ZIP, extracted sources, and all original support bytes are preserved. The local review seal is a content manifest, not external authenticity or scientific certification.

## Exact remaining limitations and disposition

There is **no unresolved analytic gap identified in Theorem 1** after this review. The strongest verified result remains the theorem as stated, conditional on accepted classical foundations whose relevant source statements and hypotheses have been checked. Full formalization of those foundational proofs was not attempted.

This review does not verify every historical comparison in manuscript §5, worldwide novelty, completeness of later literature, or claims of present open status. The manuscript expressly disclaims historical firstness and identifies uninspected leads. Those limitations must survive any public description. No proof repair, source modification, outreach, Git operation, spreadsheet update, website action, release, or publication clearance was performed. Root review of all independent reports remains required.
