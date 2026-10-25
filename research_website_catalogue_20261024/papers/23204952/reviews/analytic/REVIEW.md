# Independent analytic review — Zenodo 23204952

**Paper:** *Metric rigidity at the boundary of cubic compactifications*, Alec Kriebel, manuscript dated October 6, 2026, eight-page deposited PDF.  
**Review role:** independent analytic proof reconstruction, adversarial boundary checks and source-hypothesis matching.  
**Review completed:** 2026-10-25 UTC (October 24, 2026 Pacific time).  
**Scoped completion estimate:** 100%. This means completion of this analytic review, not proof certification, novelty clearance, or permission to promote a result.

## Verdict and strongest verified result

I found **no substantive mathematical defect in the stated new Cartier-index theorem, the conditional algebraic-gap-to-cubic comparison, or the singular-boundary isometry argument**. Each central implication has a checkable mechanism; no route in the manuscript substitutes an equivalent open assertion for its central task. Theorem 1 follows from the cited singular KE decomposition theorem and standard vanishing/reflexivity facts, with the strict threshold and equality counterexample as stated. Theorem 2 follows after accepting the explicitly identified unrestricted OpenAI upper-gap theorem and the other named external results. The note does not reprove the upstream gap; this review does not independently certify its complete proof or its fourfold companion.

This is a favorable mathematical assessment of the **precise deductions actually stated**. It is not a recommendation to advertise a new all-dimensional complex cubic K/GIT solution: the manuscript expressly attributes that comparison to established transfer and to the stronger publicly available Kong–Shen–Zhao–Zhao result. The exact novelty of the additional singular criterion is not established by this review. No paperworthy follow-up is identified.

The exact reviewed inputs are:

| Object | SHA-256 |
|---|---|
| Deposited `paper.pdf` | `daafa11716afef6207809b02fe567ca5c53c35191f3eb67fcb8f3bd94fe3b71c` |
| Deposited `source-and-verification.zip` | `fb1d5a800e6be789fe94a227940a7df4888343fe444a9f64fe1c6b602514cfda` |
| Extracted `main.tex` | `de80fb7f84555b632956f21ed8e6e0d1ae6b32da010ee6a89b69a72eb3cf8193` |

All 532 lines of `main.tex` and the complete extracted text of PDF pages 1–8 were read. The PDF and source statements agree on the central claims. The read ledger records exact primary-source bytes, URLs, retrieval dates, inspected pages/sections, and the limits of the inspection. Input hashes and review-output hashes are sealed separately.

## Independence, scope and success criteria

The first reconstruction was recorded in `RESEARCH_LOG.md` before reading favorable historical audit reports. Its independent mechanism was: retain a true Cartier root on each DGP factor; force at least `r−1` dimensions per factor by negative Hilbert roots; exclude two factors; use positive Einstein curvature to force commutation of parallel complex structures; then use tangent-sheaf simplicity to force a single sign. After reconstructing this mechanism, I checked its hypotheses against the primary sources and then read the supplemental historical notes as evidence about their scope. I did not infer validity from their favorable verdicts, their completion percentages, a clean build, a hash, or successful arithmetic scripts.

The exact mathematical success criteria were:

1. For an irreducible normal projective complex klt Fano of dimension `m≥1`, with the specified bounded-potential weak KE current and an **actual ample Cartier identity** `ω_X^[−1]≅L^r`, prove stable tangent sheaf on X and on every finite quasi-étale cover, exclude nontrivial algebraic product covers, and prove `I=±J` for every parallel orthogonal complex structure on the regular locus when `r>m/2+1`.
2. Under the singular boundary-zero algebraic normalized-volume gap in **every dimension `2≤k≤n`**, prove the smooth-link cone density bound with the correct direction and normalization, obtain the genuine limiting Cartier hyperplane root, and justify the complex/polarized GH/GIT comparison on the cubic smoothing locus.
3. For the **actual GH limits** in that compactification, prove regular-locus preservation, local smoothness of an isometry, global holomorphic/antiholomorphic extension, preservation of the cubic hyperplane polarization, and exactly conjugation-orbit metric fibers, including singular points.

These are pure mathematical deductions, not empirical or fitted-model claims. The KE existence, klt, Cartier, smoothability, and external theorem assumptions are substantive hypotheses. No numerical experiment establishes them. The numerical and algebraic checks below test constants and compatibility only.

## 1. Cartier root on factors and the index bound

The published [Druel–Guenancia–Păun paper](https://doi.org/10.5802/crmath.612), Theorem A (printed p.94), gives exactly the finite quasi-étale isometric algebraic product cover with stable tangent factors used here. Published Definition 2 (pp.96–97) matches the bounded-potential weak KE hypothesis, and Remark 3 (p.97) explicitly preserves it under finite quasi-étale pullback. Thus neither completeness nor a complete de Rham theorem on `X_reg` has been silently used.

The factorwise Cartier restriction is sound. Put `M=f*L` on a product cover `Y=Z×B`. At a regular point `b∈B`, restrict to `Z×{b}`. On `Z_reg` the smooth canonical product formula gives

`ω_Y|_(Z_reg×{b}) ≅ ω_(Z_reg) ⊗ det(T_b*B)`.

The second factor is a fixed one-dimensional vector space and hence a trivial line bundle on Z. The restriction `A=M|_(Z×{b})` is ample Cartier, and uniqueness of reflexive extension on normal Z gives `ω_Z^[−1]≅A^r` on all of Z. This avoids restricting an unproved Cartier Weil canonical divisor through a singular fiber. A factor of an arbitrary normal product cover is klt because this can be tested after adjoining smooth coordinates at a regular complementary point. Its anticanonical bundle is ample by the resulting identity. Therefore the same obstruction applies to algebraic product covers not selected by the metric decomposition.

For a positive-dimensional klt factor Z of dimension d and `−K_Z=rA`, take `N=−jA` for `1≤j≤r−1`. Then `N−K_Z=(r−j)A` is ample, so the klt Kawamata–Viehweg theorem (Hacon, Theorem 2.22, printed pp.10–11) gives `H^q(Z,N)=0` for `q>0`. Anti-ampleness rules out nonzero sections: an effective nonzero divisor in `|−jA|` has intersection `−jA^d<0`, while a nowhere-vanishing section would contradict `A^d>0`. Hence `χ(Z,−jA)=0`.

[Stacks tag 0BEM](https://stacks.math.columbia.edu/tag/0BEM) supplies the all-integer Euler-characteristic polynomial, not just agreement for large positive twists. Amplitude gives degree d and positive leading coefficient. Thus the `r−1` distinct roots `−1,…,−(r−1)` imply `d≥r−1`. Two positive-dimensional factors force

`m≥2(r−1)`,

contradicting the theorem's strict hypothesis. The DGP cover has one factor, so its tangent sheaf is stable. This argument does not need a Picard-number-one, very-ampleness, terminality, or Q-factoriality assumption.

## 2. Stability descent, every cover, and parallel complex structures

The descent argument is valid without Q-factorial determinants. For a proper saturated candidate `F⊂T_X`, remove the singular, non-locally-free, and non-étale loci, all of codimension at least two. Pull back the resulting subbundle with locally free quotient; its saturated reflexive extension `G⊂T_Y` has the same intermediate rank. A general complete-intersection curve of sufficiently large multiples of `−K_X` avoids the removed set. On its inverse image, ordinary bundle degrees multiply by `deg f`; saturation adds no codimension-one contribution. Dividing by the common complete-intersection multiple and rank gives the manuscript's slope scaling. It contradicts stability upstairs. For dimension one, X is the normal klt Fano curve P¹ and tangent rank one is automatically stable; no curve-avoidance difficulty arises. Reapplying the same hypotheses and DGP argument to any finite quasi-étale cover proves the claimed stability on every such cover.

Independently of any integration or global form-vanishing theorem, the pointwise curvature calculation is correct. If I is parallel and orthogonal, `η=g(I·,·)` is a parallel real two-form. Its `(2,0)` component α is parallel because J is parallel. For a KE metric with positive Einstein constant λ, the mean Chern curvature of `Λ^p(T^(1,0))*` is the nonzero scalar `−pλ`, up to curvature convention. Curvature annihilates a parallel section, so α vanishes. Consequently `η` is `(1,1)`, equivalently `−JIJ=I`, hence `IJ=JI`.

A separate check uses curvature operators: a parallel I commutes with every `R(u,v)`, while the Kähler contraction `ΣR(e_a,Je_a)` is `±λJ`. Thus I commutes with J. Both calculations are local and remain valid on the incomplete regular locus. Positive λ is essential; Ricci-flat hyperkähler examples would defeat the weakened claim.

The commuting I is a holomorphic endomorphism of `T^(1,0)` on `X_reg`. The reflexive analytic sheaf `Hom(T_X,T_X)` extends it across the codimension-two complement. GAGA Theorem 2 algebraizes it. Stable torsion-free sheaves are simple: intermediate-rank kernel/image slope inequalities exclude a generically deficient nonzero endomorphism; the characteristic polynomial coefficients extend to global functions on normal projective X and are constant. Subtract a complex eigenvalue to conclude that I is scalar. Its square is `−1`, so the scalar is `±i`, giving one global sign `I=±J`. Commutation alone would not have supplied this sign conclusion.

Sharpness is correctly scoped. For `X=P^(r−1)×P^(r−1)`, `L=O(1,1)`, the dimension is `2r−2` and `−K_X=rL`, exactly at equality. The equally normalized product Fubini–Study metric is KE; conjugating one positive-dimensional factor yields `(-J_1,J_2)`, neither global sign. The tangent product is also not stable. This disproves adding equality to the general uniform criterion. It does not disprove cubic-fourfold rigidity. The supplemental observation that partial conjugation does not descend through the factor-swap quotient of `P²×P²` is correct and prevents a false cubic counterexample.

## 3. Algebraic gap to the smooth-link metric gap

The upstream [pinned OpenAI manuscript](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-ordinary-double-point-gap-in-every-dimension-September-24-2026/paper.pdf), Theorem 1.1, has the exact external scope claimed: singular closed points of normal complex algebraic boundary-zero klt k-folds, `k≥2`, without isolated/lci/toric assumptions, and upper bound `2(k−1)^k`. The downloaded PDF SHA matches the deposit's pin. I inspected its theorem and conventions, not its complete proof. Reading the historical geometric/semigroup audit narratives and rerunning selected constants does not change that limit. The manuscript accurately labels this a principal external input and uses no equality classification.

[van Coevering](https://arxiv.org/abs/0806.3728), §3 and Proposition 3.2, gives the normal affine algebraic completion and Q-Gorenstein property for the smooth compact Sasaki–Einstein links at issue. Collins–Székelyhidi Lemma 6.1 (published pp.1384–1385) uses positive pluricanonical weight to give klt. The note correctly does not infer klt from rationality plus Q-Gorensteinness alone. Orbifold boundaries on a quotient are not a nonzero boundary on the affine cone germ.

The link-fundamental-group split repairs a real eligibility concern in Li–Liu's §6 setup. If the link has nontrivial fundamental group, Myers gives a finite cover of degree `d≥2`, and Bishop on that cover gives density at most `1/d≤1/2`. Since `b_2=1/2` and the sequence increases, this is sufficient. For simply connected link, the punctured Ricci-flat cone has trivial canonical holonomy and a genuine parallel holomorphic top form. Its Euler weight is k (`∇E=Id`), and torus action on its parallel line makes it equivariant. Reflexive extension gives the genuine top-form setup actually stated in Li–Liu §6.

[Li–Liu](https://arxiv.org/abs/1602.05094), Theorem 6.2 (=1.9), minimizes over **all** centered real valuations, not only Reeb directions. Their Lemma 6.8 and final limiting proof cover irregular Reeb fields by smooth quasi-regular approximations; the approximants need a Ricci lower bound tending to the Einstein value, not Einstein metrics themselves. Lemma 6.3 and that limit give

`A_X(v_ξ)=k`,  `volhat_X(v_ξ)=k^k Θ(C)`.

The contact/Riemannian conversion cancels against the sphere. Hence the infimum equals this metric Reeb value and the upper gap implies `Θ(C)≤2(1−1/k)^k`. An upper bound on an infimum without the minimizing identity would have the wrong logical direction; the manuscript uses the required identity. Checks: flat C^k has density 1 and normalized volume k^k, and is excluded; the ODP degree valuation has discrepancy `k−1` and volume 2, giving the claimed density. A free spherical quotient has density `1/d`, agreeing with the cover argument.

## 4. Limiting polarization, Fujita, and complex comparison

The derivative computation

`d/dt log[2(1−1/t)^t] = u−log(1+u)>0`, `u=1/(t−1)`,

is correct. Product with Euclidean space preserves the density. [Spotti–Sun](https://arxiv.org/abs/1705.00377), §5.1, defines `A′(n)` by products with isolated singular smooth-link factors and uses iterated cones for other singular links. Thus bounds in **all** transverse dimensions `2,…,n` suffice; direct Li–Liu application to arbitrary singular-link cones is neither needed nor asserted.

For cubics, `V=3(n−1)^n`. Spotti–Sun Theorem 5.2 requires `V>(1/2)A′(n)(n+1)^n`. The proposed estimate gives

`(1/2)b_n(n+1)^n = (n−1)^n(1+1/n)^n < e(n−1)^n < V`.

Strictness holds at n=5 and in the limiting large-dimension regime. The theorem explicitly supplies both Gorenstein canonical singularities **and** the Cartier root `−K_Z=(n−1)L_Z`. The latter is load bearing. It is not inferred from canonical singularities alone, and the theorem's GH smoothability assumptions have not been dropped.

The official [Fujita preview](https://page-one.springer.com/pdf/preview/10.1007/BFb0083337), pp.117–118, states the Gorenstein del Pezzo definition, the all-twist intermediate-cohomology condition, very-ampleness for degree at least three, and `Δ=n+L^n−h^0(L)=1`. The full chapter proof was not accessible/read; its conclusion is an established external classification also explicitly applied in Spotti–Sun §5.2. The manuscript checks the omitted cohomology hypothesis: KV handles `t≥2−n`, and Gorenstein Serre duality transfers `t≤−1` to that range. These cover all integers for `n≥3`. Klt gives Cohen–Macaulay and the Cartier canonical bundle gives Gorenstein. Since `L_Z^n=3`, the result gives `h^0=n+2` and a very ample embedding as a degree-three codimension-one variety, hence a cubic. No terminality hypothesis has been inserted.

The CM sign calculation independently checks out: extract `h^(n+1)s` from `(rh−s)^(n+1)(3h+s)` with `r=n−1`, obtaining `r^(n+1)−3(n+1)r^n`. Negating gives `2(n+2)(n−1)^n>0`. Thus the inherited GIT polarization has the asserted sign. Positive rescaling conventions do not change it.

Spotti–Sun Theorem 1.3(2), §4.2 and §5.2 provide the conditional comparison being instantiated. Fermat cubics supply the KE seed; Zhuang Corollary 4.17 independently confirms this in every required dimension. Connected smooth cubic moduli plus openness and the limit/CM closedness argument gives all smooth cubics. The continuous compact complex GH image then contains the dense smooth GIT locus and is the entire Hausdorff GIT quotient. KE uniqueness gives injectivity. Li–Wang–Xu Theorems 1.1(iii) and 1.3 match the smoothable K-polystable closed-point interpretation. Equal dimension and anticanonical volume alone would not pick out the cubic smoothing locus; the manuscript explicitly retains it.

This establishes the stated topological/closed-point result relative to the named inputs. It does not establish a scheme or stack isomorphism, a moduli-functor equivalence, or stability of every nonclosed semistable representative, and none is claimed.

## 5. Singular isometries, polarization and metric fibers

[Donaldson–Sun II](https://arxiv.org/abs/1507.05082), Proposition 2.14 (printed pp.9–10), identifies the metric and analytic singular sets in precisely the GH-limit setting used. Hence an intrinsic isometry maps `X_reg` to `Z_reg`. The local Myers–Steenrod assertion is legitimate: sufficiently small regular neighborhoods have their smooth Riemannian distances locally, since paths leaving a larger relatively compact neighborhood have a positive length cost. Global intrinsic distances on the incomplete regular locus need not agree with completion distances; the proof only requires the local statement.

Pulling back the target J yields a parallel orthogonal I. Theorem 1 applies because `n−1>n/2+1` exactly for `n>4`. It supplies a global sign, and F is holomorphic or antiholomorphic on the regular locus. The extension argument uses essential additional information, namely continuity in the matching metric/analytic topology. Target chart coordinates composed with F are locally bounded holomorphic functions on the regular locus. Normal Riemann extension, also used in DSII Proposition 2.4, extends them; density identifies them with the original continuous coordinates and preserves target equations. Apply the same argument to the inverse. GAGA Proposition 15 gives an algebraic isomorphism to Z or its conjugate. This is not a normality-only extension claim for arbitrary birational maps.

[SGA2](https://arxiv.org/abs/math/0511279), Exposé XII Corollary 3.7 (corrected edition printed p.121, PDF p.129), explicitly includes singular global projective complete intersections of dimension at least three; Remark 3.8 emphasizes removing smoothness. It gives `Pic(X)=Z[H_X]`. Canonical preservation yields `(n−1)(F*H_Z−H_X)=0`, with conjugate target in the antiholomorphic case. Torsion-freeness gives root uniqueness. The hypersurface sequence gives `h^0(H_X)=n+2`, so polarized isomorphisms induce projective linear equivalences and therefore the corresponding GIT points. Merely numerical equality of anticanonical classes would not suffice on arbitrary Fanos.

Forgetting complex structure is continuous. A metric limit has a polarized subsequential lift by the compactness used for the complex space, giving surjectivity onto the defined metric closure. The preceding classification identifies fibers exactly as conjugation orbits. Conjugation reverses J and the real Kähler form together and preserves the Riemannian metric, giving the converse inclusion. The compact quotient maps continuously and bijectively to a Hausdorff GH space, so it is a homeomorphism. This proves the full boundary assertion; no boundary stratum was omitted.

## 6. Falsification matrix and exact limits

| Attack / approach family | Mechanism or evidence | Outcome / exact gap |
|---|---|---|
| Algebraic index obstruction | Cartier restriction, KV, all-integer Hilbert polynomial, cover-degree comparison | All claimed cases supported; a merely Q-Cartier root would invalidate the integer-root argument and is excluded. |
| Local differential geometry | Curvature on `(2,0)` forms and independent curvature-contraction commutation check | Supported without completeness/integration; fails for zero Einstein constant, outside hypotheses. |
| Reflexive extension and global sign | Reflexive Hom, GAGA, stable simplicity | Supported; commuting mixed signs are excluded by stability, not by commutation alone. |
| Equality / low dimension | `P^(r−1)×P^(r−1)`, rank-one curve case, cubic n=4 arithmetic | Strict threshold verified; n=1 harmless; no cubic-fourfold failure or solution follows. |
| Cone normalization and eligibility | Myers/Bishop case split, genuine canonical form, all-valuation Li–Liu minimum | Supported; arbitrary singular-link use is avoided. Upstream unrestricted upper gap is accepted external input, not certified here. |
| Smoothability / Cartier root | Exact SS Theorem 5.2, all transverse dimensions, strict volume threshold | Supported for actual GH limits; no arbitrary Q-Fano generalization. |
| Singular map and polarization extension | DSII regular sets, local isometry smoothness, continuity/normality, SGA2 | Supported on actual GH boundary; no arbitrary weak-KE completion assertion. |
| Moduli topology and prior scope | Compact–Hausdorff quotient, LWX closed points, KSZZ/PW/Spotti/OSS statements | Supported as stated; exact additional novelty and first priority remain unestablished. |

There is no identified substantive fault requiring manuscript repair, and no replacement theorem or repaired source was produced. No route is marked blocked because none was shown to move the central difficulty to an equivalent unsupported claim. The remaining limits are explicit external theorem dependence, the unrecertified upstream gap/companion proofs, the unexamined full Fujita proof, and incomplete global novelty clearance. These are not counterexamples to the stated deductions.

## 7. Reproducibility, attribution and research outcome

Both shipped standard-library arithmetic scripts ran successfully; command, UTC time, script hash, exit code, stdout and scope are in `reproducibility_receipts.json`. The exact values include `3879/2000<2` and the fourfold margin `209183/1440000>0`. The boundary script verifies a polynomial identity, line incidence and quotient-degree arithmetic. These calculations are peripheral consistency checks, not verification of KE existence, DGP, the OAI gap, or the whole metric theorem. The main new theorem is validated by the reconstructed argument above. No document build or rendering was performed or used as mathematical evidence.

Primary-source scope comparisons confirm the paper's attribution: PW covers smooth complete-intersection tangent stability; Spotti's thesis covers smooth positive-KE splitting/sign rigidity; OSS explicitly uses the ordinary metric conjugation quotient for singular del Pezzo surface compactifications; DGP supplies the singular decomposition; SS supplies the complex transfer. The currently downloadable KSZZ PDF has SHA `6813e3d3be36c087e60b696f40652f8a837da7fcd9e3bdbd7af7df030c3ad65e`, matching the deposited provenance, and its Theorem 1.1 states the stronger complex stack/good-moduli comparison. Its manuscript date does not prove earliest public posting. These comparisons support the modest attributed framing, not first-disclosure certification.

**Paperworthy follow-ups: none established.** The general equality example leaves the cubic-fourfold isometry question untouched, and extending to arbitrary weak-KE completions would need a valid regular-locus/completion theorem. Neither observation alone meets the high bar for a novel, feasible independent contribution, so neither is promoted as a research result or recommended paper.

The reviewer wrote only within `reviews/analytic/`, used no children, made no source repair, and performed no outreach, prepared outreach, Sheet/UI/website/deployment, Git, release, or promotion action. Local third-party reading caches are not intended for publication or relicensing. The parent must synthesize this complete report with its separate independent review before making any disposition.
