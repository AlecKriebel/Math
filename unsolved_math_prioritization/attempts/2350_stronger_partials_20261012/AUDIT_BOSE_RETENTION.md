# Independent audit: four-fifths Bose–Chowla retention obstruction

Date: 12 October 2026.

## Verdict

**ACCEPT THE CORRECTED EDITION, with the construction-specific scope stated below.** The original candidate contains one false, unqualified endpoint sentence and one unnecessarily strong restatement of the weighted input. Neither defect invalidates its main theorem. Both are corrected in a separately preserved edition. The source candidate remains unchanged.

The accepted conclusion is that, uniformly over the stated affine Bose–Chowla seeds and their positive canonical integer or single-coset half-integer lifts of length q=p²−1, every retained subset containing no genuine equality x+y+z=w has size at most (4/5+o(1))p, as the odd finite-field order p tends to infinity. Repeated entries remain allowed. The proof uses established polynomial Dirichlet RH and tame rank-one curve RH. It does not prove an arbitrary-Sidon bound, an unrestricted interval theorem, sharpness for actual retained subsets, a finite field-order threshold, or a resolution of Erdős 864.

**The separate elementary fallback is also accepted:** retention at most (127070161/150724800+o(1))p = (0.8430607371845907…+o(1))p, using polynomial Dirichlet RH and the accepted carry theorem only.

## 1. Inputs, independence and exact pins

The stronger candidate, elementary fallback and accepted carry dependency were inspected and their input integrity was verified. The complete accepted corrected proof, fallback and carry theorem are distributed in BOSE_FOUR_FIFTHS_PROOF.md, BOSE_ELEMENTARY_PROOF.md and BOSE_CARRY_DEPENDENCY.md. BOSE_CORRECTION_HISTORY.md records every change to the stronger candidate. [Editorial redaction: unpublished candidate, manifest, checker and provenance identity listings are omitted. No mathematical audit content is removed.] Current public-file identities are supplied by MANIFEST.json; integrity inventories remain local and do not substitute for this mathematical review.

The audit rederived the source and target equations, checked the measure and optimization arguments independently, and used a separate fresh geometry/source-applicability review. It did not rely on the author's optimization worker as an acceptance authority. Fresh diagnostic code was written for this audit rather than merely rerunning the candidate's scripts. The independent geometry report is included separately.

## 2. Corrections required before acceptance

### 2.1 Exceptional endpoint target

Original Part I §6 concluded, without qualification, that at X=1 the target limiting count is p/2. This is false for the explicitly exceptional reducible target.

There is an infinite counterexample to that sentence. Let p=3^k, choose any nonsquare δ, take d=0 and λ=θ^−1, and use the integer lift. Then λ(θ+d)=1, so B_d=q and X_d=1. Moreover

    R=(θ+d)/λ²=θ³=δθ=−8δθ.

The exceptional modular fiber consists solely of (0,0,0), because a²=−3δ=0. Its lifted equation would read 3q=q, so T(d)=0 for every generator. Thus no unqualified p/2+o(p) formula at this endpoint is possible, even along an infinite family.

The corrected sentence states: at X=1 the source count is zero; a nonexceptional target has count p/2+o(p), whereas the possible exceptional target has count at most two. The everywhere-uniform target upper bound remains valid. This matches the theorem's originally stated exception and changes no deletion constant.

For comparison, in F5 with δ=2 and d=2, the same endpoint construction gives the two modular triples (2,2,2) and (3,3,3). The genuine target count can be zero or one depending on the generator. It is not uniformly zero; the characteristic-3 family above avoids this ancillary generator issue.

### 2.2 Uniform upper degree bound rather than unqualified equality

Original Part II §1 stated equality p(D_W(t)+o(1)) uniformly at every vertex. Part I only supplies that equality away from its explicit exceptional roles, and supplies an upper bound everywhere. The next paragraph of the original already allowed O(1) exceptional vertices at O(p) cost, so its covering argument remained valid. Still, the most direct and accurate input is the everywhere-uniform **upper** bound. The corrected bullet says “at most,” and the following sentence explicitly refers to the exceptional-fiber upper bounds proved in Part I.

No new assumption, character estimate, smoothing construction, or constant is introduced. Other edits identify the correction edition and its acceptance status.

## 3. Source-fiber audit

Write M=μ(θ+a)=uθ+v and M(θ+b)=Uθ+V, where U=ub+v and V=vb+uδ. Comparing coefficients after multiplying by θ+c gives exactly Uc+V=1 and d=Uδ+Vc. Hence c=(1−V)/U when U≠0, and U=0 permits a solution only when V=1.

If N(M)=−u, then u cannot vanish, since M is nonzero and has nonzero norm. The unique b0=−v/u satisfies M(θ+b0)=1. Substitution shows that every solution is on b=b0,d=c or c=b0,d=b, with one intersection. Positivity makes genuine zero carry impossible: either line would require B_a+B_b0=0. Thus all source counts, including every bounded nonnegative weighted count, vanish exactly on these fibers. The equation N(μ)(a²−δ)=−u(a) has nonzero quadratic coefficient, so there are at most two such vertices per seed.

Off these norm exceptions, the fiber has p or p−1 points. The rational factorization

    θ+c=−conj(M)(b−r)/(ub+v),  r=θ+1/conj(M)

is correct. The condition r∈F is exactly the norm exception. Also r=θ is impossible, and the only collision of its irreducible quadratic with that for −θ is r=−θ, equivalently M=1/(2θ). Away from this collision, the two quadratic local characters and optional linear denominator lie on pairwise coprime factors of a squarefree modulus of degree at most five. At least one nonprincipal quadratic local character ensures nontriviality by CRT; no character on the separate linear factor can cancel it.

At the collision, c=δ/b, d=(b+δ/b)/2, b≠0, and θ+c=θ(θ+b)/b. Its degree-three Dirichlet character is principal precisely when q divides n+m and p−1 divides m. For each fixed nonzero integer pair (n,m), these two conditions cannot hold for sufficiently large p. Thus the collision is not a permanent obstruction to the needed fixed-frequency equidistribution. A field-dependent resonant pair, such as n=−m with m=p−1, must not be misrepresented as covered by this nontriviality argument.

The degree-five and degree-three Dirichlet bounds, together with p+O(1) fiber masses and harmless λ/half-coset phases, give uniform Haar convergence in the two free source coordinates. The audit accepts every source law and its stated exceptions.

## 4. Target-curve audit

### 4.1 Equations and geometry

Expanding the product gives ab+ac+bc+δ=s and abc+δ(a+b+c)=t. Eliminating c yields exactly the stated bidegree-(2,2) equation. At a+b=0 its value factors as (a²−δ)(a²+s−δ). Since δ is a nonsquare, every F-point of this exceptional projection locus has s=δ−a²≠0 and the uniquely recovered c=t/s. Thus the affine F-points really parametrize the original target fiber; this is not a generically correct map with unaccounted F-rational points.

The simultaneous product model in (P¹)³ has exactly six boundary points. Two coordinates cannot both be infinite, because the remaining coordinate would be forced simultaneously to −θ and +θ. With one infinite coordinate, the two others must have these opposite values. At each boundary point the linear parts are 2θx−Rz and −2θy−conj(R)z, of rank two; R and conj(R) are nonzero. Taking z as local uniformizer proves ord(x)=ord(y)=ord(z)=1. All six points are distinct and smooth.

A geometrically irreducible (2,2) curve has arithmetic genus one. Its normalization has genus at most one. The total singularity delta invariant is at most one, so changing a bounded trace sum from the finite affine model to the normalization costs an absolute O(1), uniformly across parameters. This remains valid in characteristic 3, including singular irreducible fibers; smoothness of every fiber is not required. None of the six boundary points is damaged by normalization.

### 4.2 Reducibility

The independently expanded discriminant agrees exactly with the candidate. The quadratic coefficients in b are primitive as polynomials in a: any common factor would divide a²−δ, but at a=±θ the linear coefficient is t−sa, nonzero because t²−δs²=N(R)≠0. Thus the discriminant square test has no missing vertical components.

For t≠0, comparison with (2θa²+Aa+B)² forces A=−t/θ and B=θ(s−2δ), then t²=δs², a contradiction. For t=0, the remaining identity factors exactly as s³(s+8δ)=0. The s=0 option would make R=0, leaving only R=−8δθ.

At that value the two displayed factors are distinct, are exchanged by Frobenius, and have simultaneous affine F-points exactly a=b, a²=−3δ. The original equations then give c=a. This conclusion is also correct in characteristic 3; the only such triple is (0,0,0). Therefore the exceptional target fiber has at most two ordered triples. Since the map from d to R is injective, there is at most one exceptional target vertex.

### 4.3 Character sheaf and external theorem

The primary source is Lei Fu and Daqing Wan, *A Class of Incomplete Character Sums*, arXiv:1303.3650v3, 6 January 2025: https://arxiv.org/pdf/1303.3650v3 . The checked statements are Proposition 1.2, the rank-one Kummer calculation of §2, Proposition 4.1 and Theorem 4.2. The correction to Theorem 4.6 is unrelated to this argument. The separate geometry audit records the direct source inspection.

Tensor induction of the Kummer sheaf for f=(a+θ)^n(b+θ)^m has trace χ(f(x)) at an F-point, rather than its square or a norm character mistakenly inserted in the trace. After base change to K its rank-one geometric character is the product of the sheaf for χ,f and the sheaf for χ^p,conj(f). Thus the geometric Kummer function is f·conj(f)^p. The same conjugation calculation applies to the curve's function field; the proof does not rely on extending an affine-space theorem by unsupported analogy.

At P12 and P21 the valuations are n+pm and m+pn. For |n|,|m|<p−1 they have absolute value less than q. If both were divisible by q, both would be zero, forcing n=m=0. Every fixed nonzero Fourier pair is consequently geometrically nonconstant for all sufficiently large p, uniformly over the curve parameters and primitive character/generator choices. Multiplying the exponents by a unit modulo q preserves this divisibility test.

The remaining hypotheses are all satisfied: the normalized nonexceptional curve is smooth and geometrically connected; the sheaf has rank one and finite monodromy of order prime to the characteristic; it is lisse away from the six boundary points and tame at those points; finite monodromy supplies weight zero; and geometric nontriviality removes invariant coinvariants. The genus/puncture bound is at most 6√p. The trivial coefficient is p+O(√p), after the uniformly bounded normalization and boundary corrections.

The conclusion is for every fixed Fourier pair. Neither this audit nor the accepted theorem claims nontriviality for all field-dependent character tuples. Such a stronger claim is unnecessary for fixed-test equidistribution and would require additional analysis.

## 5. Uniform weighted incidence and arbitrary deletions

Fixed-frequency estimates are uniform in every allowed seed parameter. Positivity and uniform boundedness of fiber masses pass this to each fixed continuous torus test function. Moving triangle cutoffs are handled by a finite mesh in X, with area discrepancy O(mesh size), followed by p→∞ and then refinement. Their boundaries have Haar measure zero. Integer seam changes affect only O(1) points of a conditional nonexceptional fiber by strong Sidonicity; norm-exceptional source fibers are handled exactly. Half-integer lifts use μ=λ²g, never division by two modulo q.

For W continuous with compact support in the open simplex, its four conditional test-function families are uniformly continuous in the fixed coordinate and compact in the uniform norm. Their periodic extensions are continuous because the support stays away from all source-coordinate seams. For the target family, W(y,z,x−y−z) is zero unless it represents a genuine positive zero-carry third source. A finite uniform-norm net therefore proves uniform convergence for the entire family. This step does not use equidistribution for a p-dependent shrinking kernel.

The four displayed marginal formulas are exactly the role degrees divided by p at nonexceptional roles. Exceptional source degree zero and exceptional target degree at most 2||W||∞ yield the same **upper** estimate uniformly at every vertex. In explicit quantifiers, for each fixed W there is ε_W(p)→0 such that every vertex v satisfies

    deg_W(v) ≤ p D_W(X_v)+p ε_W(p),

where deg counts all role appearances. The full equation weight is p²(M+o(1)), from the accepted global carry equidistribution; compact support removes its carry-boundary and seam problems too.

If a deleted set D meets every genuine equation, every edge weight appears at least once in the sum of deleted role incidences. Hence

    p²(M+o(1)) ≤ Σ_{v∈D} deg_W(v)
                   ≤ p Σ_{v∈D} D_W(X_v)+p² ε_W(p).

This inequality holds for every deletion pattern without approximating it by intervals or presuming its equidistribution. Repeated source entries and repeated appearances of a deleted vertex only overcount on the right. If D_W≤1, it gives |D|/p≥M−o(1), uniformly over the subset and seed parameters.

## 6. Coupling, smoothing and optimality audit

With t uniform on [0,1/5], the unpermuted source triple t,t+1/5,3/5−t sums to 4/5+t. After random source permutation and assigning total mass 1/5, every source marginal has density 1/3 on [0,3/5]; the target has density one on [4/5,1]. Aggregate capacity is at most one. The singular law is not used directly as a test density.

For fixed 0<η<1/20, scale each source by s=1−4η and translate by η, translate the scaled target by 3η, and reduce total mass to s/5. This last mass rescaling is necessary and present: it preserves the respective marginal bounds 1/3 and one. Independent smooth noises of size at most ε=η/10 in the three sources, with their sum added to the target, preserve the equation exactly.

The convolution is a nonnegative C∞ density with total mass (1−4η)/5. Its sources lie in [9η/10,3/5−13η/10] and its target in [4/5−η/2,1−7η/10]. These bounds put the entire support strictly inside the open zero-carry simplex. Source and target supports are separated by 1/5+4η/5. Convolution with probability measures preserves each L∞ marginal bound. Because the target support is disjoint from the combined source support, summing all four roles still gives D_W≤1 everywhere.

Consequently |D|/p≥(1−4η)/5−o_η(1). For any desired error, first choose a fixed η and then choose p sufficiently large for that one fixed density. Taking η→0 only after the p-asymptotic proves the uniform 1/5 deletion bound. There is no hidden interchange of a shrinking mollifier with the field-order limit.

The dual h(x)=(3/5−x)_+ +(x−4/5)_+ is nonnegative. On any edge x+y+z=w, the sources contribute at least 9/5−w. If w≤4/5 this is at least one; otherwise the target contributes at least w−4/5. Thus the total dual weight of every edge is at least one. Its integral is 9/50+1/50=1/5. For an edge measure with aggregate marginal dominated by Lebesgue measure, integrating gives mass≤∫h=1/5. The smooth construction approaches this bound. This establishes exactly the claimed supremum of the stated nonnegative fractional first-moment method, not sharpness of actual Bose–Chowla subsets or of all conceivable first-moment arguments with additional information.

## 7. Separate elementary fallback

The fallback source analysis is the same accepted rational/Dirichlet calculation above. For a fixed target, dividing R by θ+a yields exactly the displayed sum and product of b,c, so n_a=1+φ(D(a)). Its quartic has nonsquare leading coefficient 4δ and does not vanish at ±θ. If its squarefree odd-multiplicity part is constant, n_a vanishes outside at most four roots. Otherwise its quadratic-character factors are coprime to T²−δ, and adding any nonprincipal K-character there produces a nonprincipal CRT character of squarefree modulus degree at most six. Even-multiplicity zeros change only O(1) terms. Thus each modular source marginal of a nonnegligible target fiber converges uniformly to Lebesgue measure.

The genuine zero-carry marginal is a submeasure of that modular marginal. Along any parameter subsequence its weak limit ρ satisfies 0≤ρ≤dx. Permutation symmetry and exact addition give ∫y dρ=xβ/3, where β is its mass. The rearrangement inequality ∫y dρ≥β²/2 implies β≤2x/3. Compactness makes this bound uniform, including negligible target fibers. The endpoint issue corrected in the stronger proof does not occur in this fallback argument.

For arbitrary deletions, the empirical deletion measures converge subsequentially to d(x)dx with 0≤d≤1. Target-deletion incidence measures converge to e(x)dx with e≤g=x²/2 by domination by the full target marginal, and e≤kd with k=2x/3 by the pointwise target bound tested against nonnegative continuous functions. The cutoff causes no convergence gap, because the dominating limiting measures have no atoms. Weighted coverage is therefore valid without any microscopic regularity of the deletion set.

The pointwise piecewise-linear knapsack dual is correct: the first segment has slope u=s+φk, length c=g/k=3x/4, and the second slope s, length 1−c. Subtracting λd and retaining the positive portions gives the stated upper bound. At a=7/10 and λ=1163/1800, the positive regions are [0,107/810] below the cutoff and [29/30,1] above it. Independent exact integration gives

    M=219/2000,
    J1=11449/1458000,
    J2=6409/25920000,
    (M−J1−J2)/λ=23654639/150724800.

The complementary retention fraction is exactly 127070161/150724800. This proof needs no positive-genus character-sheaf estimate.

## 8. Computation, limits and final disposition

The fresh independent diagnostic uses explicit finite-field arithmetic, including polynomial-basis fields of orders 9,25,27 and 49. Across orders 3,5,7,9,11,13,25,27,49 it checks every nonzero M and R, exact source formulas and exceptional line unions, target quadratic counts, the complete exceptional triple lists, collision formulas, and explicit exceptional seam examples. It also checks symbolic elimination, the discriminant and reducible factorization, the smoothing gap, and the fallback integrals with rational arithmetic. Low-frequency and near-p Fourier sums are recorded only as floating-point diagnostics.

Normal, -O and -OO executions pass. The script uses explicit runtime checks, so Python optimization does not discard its tests. Comparison of the three outputs after removal of elapsed time shows identical substantive records. The finite tests validate the algebra and provide useful prime-power/characteristic-3 adversarial coverage; they do not establish asymptotic equidistribution.

No fatal gap remains in the corrected construction-specific proof. The original two statements are not accepted verbatim; the separately pinned corrected edition is accepted. The elementary fallback is accepted without mathematical changes. The unrestricted problem remains unresolved. No publication or remote mutation was performed by this audit.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.
