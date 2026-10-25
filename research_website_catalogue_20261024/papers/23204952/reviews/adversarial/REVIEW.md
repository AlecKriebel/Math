# Independent adversarial mathematical review

Paper: *Metric rigidity at the boundary of cubic compactifications*, version 1.0, Alec Kriebel, Zenodo record 23204952. Reviewer role: independent adversarial review of the actual deposited manuscript and mathematical supports. Completed 2026-10-24 UTC. This review used the requested GPT-6.1 Sol Ultra agent; no descendant agents were spawned.

## Verdict and exact validation level

**SUPPORTED AT THE MANUSCRIPT'S DECLARED EXTERNAL-THEOREM LEVEL. No blocking mathematical defect or counterexample was identified.** The new sharp Cartier-index criterion and the singular cubic metric-fiber argument have checkable proofs under their stated hypotheses. The cubic comparison continues to depend on the expressly cited unrestricted OpenAI upper-gap theorem. Its scope matches the needed input; this review does not independently certify that external theorem's complete proof.

The complete eight-page manuscript was read, together with its full 532-line source and all substantive deposited proof/audit supports. Primary theorem statements and the relevant supporting arguments were checked directly, rather than treating old favorable audit conclusions as mathematical evidence. Independent attacks were recorded before those historical audits were read. The primary read ledger gives exact files, hashes, and reading ranges. No sibling's current report was read. The source/PDF hashes match the parent's specified intake, and all 25 members covered by the archive checksum manifest verify.

There is **no unresolved internal proof gap identified in the actual claims**. The strongest checked result is the following: accepting the precisely cited decomposition, vanishing, GH regularity, cone-minimum, classification, compactness and transfer theorems, the manuscript's deductions establish Theorem 1 and Theorem 2 in exactly their stated scopes. This is neither formal certification nor an independent reconstruction of every foundational input. In particular, the entirety of the 55-page upstream gap proof and its fourfold companion was not recertified here; their exact statements, normalizations, dependency role, and the deposited scoped audit supports were checked. Fujita's original required statement and definition were directly checked in the official two-page preview; its complete chapter proof remains an accepted external classification theorem.

Assigned review completion estimate: **100%**. This percentage describes completion of this adversarial review, not a probability of theorem correctness or an estimate of research novelty. No follow-up research task is recommended from this review.

## Claim inventory

| Claim | Hypotheses that matter | Assessment |
|---|---|---|
| High-index stable tangent sheaf and stable tangent sheaves of finite quasi-étale covers | Irreducible normal projective complex klt Fano, specified bounded-potential weak KE current, genuine ample Cartier root, integer r, strict 2(r−1)>m | Proof verified at cited-input level |
| No positive-dimensional product cover | Same genuine root; factors normal, product cover finite quasi-étale | Independent factor-dimension obstruction verified |
| Parallel orthogonal complex structure is ±J | Positive KE Ricci constant, parallel/orthogonal I, high-index stability | Local curvature and reflexive endomorphism mechanism verified |
| Sharpness | P^(r−1)×P^(r−1), r≥2, equality m=2r−2 | Exact counterexample to including equality |
| Algebraic gap implies smooth-link cone-density gap | Singular boundary-zero klt algebraic germs, all needed dimensions; smooth compact Sasaki–Einstein link | Correct global-minimum direction, canonical-form case split, and density normalization |
| Complex cubic GH/GIT homeomorphism | n≥5, upper gap in every k=2,…,n, polarized smoothable limits | Established Spotti–Sun transfer applies; no stack/scheme upgrade |
| Every boundary metric isometry is holomorphic or antiholomorphic and preserves hyperplane polarization | Actual cubic KE GH limits, not arbitrary weak KE completions | Regular-locus, chart extension, singular Picard Lefschetz, and complete linear system checks succeed |
| Ordinary metric compactification is GIT modulo conjugation | Previous complex comparison and isometry classification | Surjectivity and compact–Hausdorff quotient argument verified |

## Independent falsification attempts and proofs

### 1. Cartier root and product-cover obstruction

An apparent way to break the theorem is a product cover whose factors have incompatible indices, or a quasi-étale cover on which the root ceases to be a line bundle. Neither occurs for the stated hypothesis. For f:Y→X quasi-étale, canonical divisorial sheaves agree on an étale big open set and hence reflexively everywhere. Thus −K_Y=r f*L, with f*L ample Cartier. For a normal product Y=Z×B, choose b∈B_reg. Over Z_reg×{b}, the product canonical formula differs from ω_Z only by the fixed one-dimensional vector space det(T_b*B). Restrict the actual line bundle f*L there and extend the resulting equality of reflexive sheaves over normal Z. This produces an actual root −K_Z=rA, with A ample Cartier. It does not restrict a non-Cartier canonical Weil divisor through a singular slice. Klt of a factor follows by adjoining smooth coordinates at b, and ampleness follows from this root identity.

For d=dim Z and 1≤j≤r−1, the Cartier divisor −jA satisfies

    (−jA)−K_Z=(r−j)A, ample.

Hacon's exact klt Kawamata–Viehweg formulation, Theorem 2.22, therefore gives higher-cohomology vanishing. Negative ampleness gives H^0(Z,−jA)=0. One can check the latter without smoothness: a nonzero section would give an effective Cartier divisor with intersection −j A^d<0, or trivialize a negative ample line bundle. Both are impossible.

The all-integer Euler-characteristic polynomial has degree d and leading coefficient A^d/d!>0; this includes the negative integer values, as Stacks 0BEM and 0BEL explicitly permit. Hence the r−1 distinct roots −1,…,−(r−1) force d≥r−1. Two nontrivial factors require m≥2(r−1), contradicting the strict hypothesis. This obstruction works for any algebraic product cover, not just an isometric DGP splitting.

Published DGP Theorem A supplies the needed product cover with stable factors and deals with the incomplete regular locus. Its Definition 2 agrees with the manuscript's weak KE hypotheses; Remark 3 explicitly retains the KE metric under finite quasi-étale pullback. The factor obstruction leaves one factor, so the tangent sheaf upstairs is stable.

### 2. Descent of stability and arbitrary finite covers

I tried to expose a hidden Q-factorial determinant requirement or an exceptional-divisor slope change. Take the finite étale big open set where the saturated subsheaf and quotient are locally free. Its complement, and the finite inverse image of that complement, have codimension at least two. Pull back the subsheaf there, extend reflexively, and saturate. No codimension-one divisor is introduced. A general complete-intersection curve of sufficiently positive multiples of −K_X avoids the removed codimension-two subset. Ordinary vector-bundle degrees on its étale inverse image multiply by deg f. Dividing by the curve's polarization factor and rank gives exactly the manuscript's slope formulas. A proper subsheaf with slope at least μ(T_X) would contradict stability upstairs.

Every finite quasi-étale cover that is a normal variety retains the same dimension, actual Cartier root, klt condition, and weak KE metric. Applying the same argument proves its tangent stability. The usual convention that a covering variety is irreducible is understood; a disconnected disjoint union is not a counterexample to a stability assertion about a variety.

The low-dimensional endpoint m=1 is harmless: the rank-one tangent sheaf is stable and no product decomposition is possible. The integer/root and positive-dimensional-factor requirements are used explicitly.

### 3. Local curvature, incomplete regular locus, and global sign

Hyperkähler-type rotation is the main curvature counterexample to test. It fails here because Ric(g)=λg with λ>0. For another orthogonal parallel complex structure I, η(u,v)=g(Iu,v) is a parallel real two-form. Type decomposition relative to parallel J is parallel. On Λ^p T*^(1,0), the Chern mean-curvature endomorphism is −pλ Id, up to the overall sign convention. A parallel section is annihilated by curvature and its contraction; for p=2 its (2,0) part must vanish. This is pointwise; neither integration over X_reg nor completeness is used.

Thus η is (1,1), giving −JIJ=I and hence IJ=JI. The complex-linear parallel endomorphism I is holomorphic, since the Kähler Levi-Civita and Chern connections agree. The analytic sheaf Hom(T_X,T_X) is reflexive: for a coherent domain sheaf and reflexive target on a normal space, extension from a big open set recovers the Hom sheaf. Consequently I extends across the singular locus, and GAGA Theorem 2 algebraizes it.

An independent way to check the final scalar step is to form the two algebraic eigenprojections of I using I²=−Id. If both ±i eigensheaves were nonzero, these projections would split T_X into two nonzero proper direct summands. Their slopes have weighted average μ(T_X), so they cannot both have slope strictly below μ(T_X). Stability excludes that split; one projection vanishes and I=±J with a single global sign. This verifies the manuscript's simplicity argument without assuming irreducible complete holonomy or simple connectivity.

### 4. Exact equality counterexample and failed cubic-fourfold shortcut

Let d=r−1≥1 and X=P^d×P^d with L=O(1,1). Then −K_X=rL and m=2r−2, exactly equality. The equal-normalization product Fubini–Study metric is positive KE. Partial conjugation is an isometry and produces I=(−J_1,J_2), which is neither J nor −J. The tangent sheaf also splits into equal-slope factors. This is a concrete simultaneous failure of the stability and sign-rigidity conclusions if equality is included.

I checked the mixed complex structure by exact real matrices in the owned verification script. This checks its algebra, while the Fubini–Study product supplies the geometric example. The sharpness statement concerns the uniform general-Fano threshold; it does not claim an example in every fixed odd dimension or a cubic-fourfold failure.

The tempting quotient Sym²(P²) does not give a contrary cubic-fourfold isometry: partial conjugation does not normalize the factor swap. The deposited notes correctly reject that shortcut and do not assert a fourfold result.

### 5. Cone eligibility, infimum direction, and normalization

I tested the dangerous inference “upper bound on an infimum implies an upper bound at the metric Reeb valuation.” The manuscript does not make that inference without minimization. Li–Liu Section 6 assumes an equivariant top form and proves a minimum over **all** centered real valuations, including irregular Reeb fields (Theorem 6.2). Its quasi-regular approximation, Lemma 6.8 and final proof, uses Ricci lower bounds approaching the Einstein value; it does not assume every approximation is Einstein.

Van Coevering Section 3 constructs the normal affine completion of a smooth compact Sasakian cone through a CR-preserving quasi-regular structure; Proposition 3.2 gives Q-Gorensteinness in the Sasaki–Einstein setting. Collins–Székelyhidi Lemma 6.1 uses positive pluricanonical Reeb weight to give klt. Thus the algebraic-gap application is to a boundary-zero singular klt germ, with no hidden quotient boundary. Rational plus Q-Gorenstein alone would not suffice, and the manuscript correctly avoids that substitution.

The non-simply-connected case is independently bounded by Myers and Bishop: a finite universal cover of degree d≥2 gives density≤1/d≤1/2≤b_k. In the simply-connected case the punctured Ricci-flat Kähler cone has a parallel holomorphic top form; its radial weight is k and the cone torus acts on its one-dimensional parallel-form space. The homogeneous form extends reflexively. This matches Li–Liu's canonical-form setup.

Li–Liu Lemma 6.3 and its approximation argument give A(v_ξ)=k and volhat(v_ξ)=k^k Θ. The ratio of contact volumes to the round sphere removes the fixed contact/Riemannian conversion. Flat C^k would give Θ=1 and volhat=k^k and is expressly excluded from the singular assertion. The ODP degree valuation has discrepancy k−1 and volume 2, reproducing 2(k−1)^k. There is no sign or factorial mismatch.

### 6. Every transverse dimension, Cartier root, and cubic embedding

Spotti–Sun's A′(n) involves products of Euclidean factors with isolated cones whose links are smooth. It does not require applying Li–Liu directly to singular links. Spotti–Sun's iteration handles those links. The dimensions needed are every k=2,…,n, including the lower-dimensional bases, exactly as stated by the manuscript and the pinned OAI upper-gap theorem. Normal boundary-zero klt curves introduce no singular k=1 case.

For t>1,

    d/dt log[2(1−1/t)^t] = u−log(1+u)>0,  u=1/(t−1).

Euclidean products preserve density. Therefore A′(n)≤b_n. The cubic anticanonical volume is 3(n−1)^n, and the required strict inequality reduces to

    (1+1/n)^n < e < 3.

No endpoint equality is hidden at n=5 or in the limit n→∞. Spotti–Sun Theorem 5.2 concludes that the root itself is Cartier and −K_Z=(n−1)L_Z, as well as Gorenstein canonical singularities. The root conclusion is essential; canonical singularities alone would not suffice.

Fujita's original preview explicitly defines the Gorenstein del Pezzo class using the canonical identity and all-integer intermediate-cohomology vanishing. Klt vanishing at t≥2−n and Gorenstein Serre duality for t≤−1 cover every integer when n≥3. Its degree-three statement gives very ampleness and Δ=1, hence h^0=n+2. A very ample degree-three n-fold in P^(n+1) is a cubic hypersurface. A terminal-singularity classification was not substituted for this canonical/Gorenstein result.

### 7. CM sign, complex topology, and smoothing locus

On P^(n+1)×S, the coefficient of h^(n+1)s in (rh−s)^(n+1)(3h+s) is r^(n+1)−3(n+1)r^n. The leading minus and r=n−1 give 2(n+2)(n−1)^n>0. The universal-divisor factor is present, so the pushforward has the correct relative dimension. This also agrees with the older K/GIT hypersurface comparison, OSS Corollary 3.5.

Spotti–Sun Section 4.2 describes the precise continuity, uniqueness, openness, connectedness, compactness and surjectivity method reused for cubics in Section 5.2. The complex structure and polarization are retained in this GH compactification. The manuscript separately defines ordinary metric GH closure, so it does not falsely identify conjugate complex points before taking a quotient.

LWX Theorems 1.1 and 1.3 have exactly the Q-Gorenstein smoothability and closed-polystable-point interpretation used. The specified closure is the cubic smoothing locus; equal dimension and volume alone would not identify it. The manuscript does not claim a scheme/stack comparison or a stability equivalence for each nonclosed orbit.

### 8. Intrinsic regularity, local isometries, chart compatibility, and polarization

Donaldson–Sun II Proposition 2.14 identifies the metric and analytic singular sets for the actual GH limits. Thus any metric isometry preserves the algebraic regular locus. Smoothness of its restriction is local Myers–Steenrod: choose relatively compact regular neighborhoods and smaller neighborhoods whose short distances cannot be shortened by leaving the larger one. Their local distances are ordinary smooth Riemannian distances, so the local isometry is smooth and pulls back J_Z to a parallel orthogonal I. No completeness of X_reg is needed.

Theorem 1 yields I=±J. For singular extension, continuity is essential. A sufficiently small source neighborhood maps into one analytic target chart. Its finitely many coordinate pullbacks are bounded holomorphic functions on the source regular locus. Normal Riemann extension gives holomorphic functions on the whole neighborhood. They equal the original continuous functions by density and obey the target equations. Uniqueness makes these local extensions agree on chart overlaps. Repeating for F^−1 produces a global biholomorphism to Z or its conjugate, algebraic by GAGA Proposition 15. An arbitrary birational map on a big open set would not justify this step; the actual continuous isometry does.

SGA2 XII Corollary 3.7 expressly covers global projective complete intersections of dimension at least three without a nonsingularity assumption. It gives Pic(X)=Z[H_X]. Canonical preservation and torsion freeness recover H_X from (n−1)H_X=−K_X. For an antiholomorphic isometry, this calculation is performed with the conjugate target and its conjugate hyperplane line bundle. It would be wrong to demand equality of the un-conjugated complex line bundle under an antiholomorphic pullback. The manuscript states the appropriate conjugate convention. The hypersurface sequence gives the complete hyperplane embedding, so the recovered polarized isomorphism is projective linear and represents the correct GIT point.

Finally every ordinary metric limit has a complex/polarized subsequential lift by compactness. Therefore the forgetful map is onto the metric closure. Its fibers are exactly the conjugation orbits just established; conversely conjugation reverses both J and the real Kähler two-form and preserves the Riemannian metric. A continuous bijection from the compact conjugation quotient to the Hausdorff metric GH space is a homeomorphism. There is no residual global chart, polarization, or topology gap identified.

## Reproducibility, source issues, and limits

The two deposited arithmetic/example scripts exit successfully. They check the rational upper-tail certificate, fourfold moment constants, polynomial identities and line incidence; they do not prove KE existence, cited classification results, or the gap theorem. The owned independent script checks exact threshold/CM formulas for n=2,…,128, the integer product-dimension boundary, and the excluded mixed complex structure. These finite checks supplement the all-dimensional derivations above and are not offered as proofs of those derivations.

The archive contains explicit historical discussion of two DGP proof typos: omission of a common product multinomial coefficient and writing slope zero at an equality-slope step. I checked the original published context. The coefficient occurs on both sides and cancels; the preceding equality-slope second-fundamental-form argument supplies the intended splitting. These are not defects newly found in this manuscript or reasons to replace its invoked theorem. No source or manuscript repair was made.

The attribution level is appropriate: smooth stability/rigidity, DGP splitting, the conjugation convention, and the complex cubic comparison are credited as prior results. Current KSZZ Theorem 1.1 indeed states the stronger algebraic comparison; it does not serve here as a freshly certified proof of the metric-fiber assertion. Neither a historical finite search nor this review establishes first disclosure of the exact singular criterion.

No external individual was contacted, no outreach was prepared, and no site, sheet, UI, rendering, deployment, Git, release, or publication operation was performed. All authored files lie in this adversarial review directory. No follow-up is requested: the precise limitations above should travel with the verdict, rather than being converted into a new research program or a heuristic unrestricted “PASS.”
