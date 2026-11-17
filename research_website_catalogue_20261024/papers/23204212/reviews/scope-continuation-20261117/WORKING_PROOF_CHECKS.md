# Independent working checks, not yet a final disposition

The original-only INITIAL remains untouched. No current peer/root continuation findings have been read. These are this family's deductions after actual primary reading; prior packaged-audit assertions are not premises.

## Pinned nonamenability proof: finite mechanism

Read the complete actual main.tex/macros, introduction, finite-proof.tex, consequences, auxiliary appendix, mixed-pair figure and bibliography at adc7f1241b42e322a6451854ab7e4b4c146bf78a. The consequence section's representation/percolation companions are explicitly not premises of the nonamenability proof and are outside this check.

Basic dyadic cells with intersecting interiors are nested. A sufficiently fine uniform grid resolves every PL breakpoint and dyadic intercept; on a piece x↦2^q x+b, choose n so b is a multiple of2^(q−n). All image cells are basic and their mesh tends to0. A mesh smaller than a fixed basic interval's length forces respect for that interval. Taking a finite maximum supplies simultaneous admissibility for A∪SA; there is no asserted uniform grid level for every g∈F.

For two separated internal basic cells, partition each of the three complementary gaps into basic cells. Bisection raises the count by exactly1, so match source/target gap counts independently. Matching all cells gives dyadic breakpoints and slopes powers of2, hence an element of the standard F with the required affine pair restrictions. No endpoint-touching or nested pair is transported by this argument.

Normalized restrictions obey (T_I)_J=T_(I·J), from the affine-chart identity. If h maps I affinely to I', normalized restrictions of gT and hgT coincide on the corresponding cells. This covariance is local to the selected cells; h need not preserve the remaining parent/descendant family.

The color recursion is on cell count, not geometric mesh. Each normalized restriction to an internal respected parent has fewer cells because the partition also has cells outside it. Values lie in the convex unit ball, so every call of the Lipschitz map is in-domain. All group-color functions are extended by0 outside admissibility; their scalar correlations are globally bounded by1.

Fix D and all pair transports S before choosing an arbitrary nonempty finite A. Only n may depend on A. Cancellation for a bounded scalar function gives the relative symmetric-difference bound without any limiting process or invariant mean on vector-valued functions. For all separated family pairs, their averaged real inner products lie within η of a common α. Symmetry handles reversed order. The reference correlation may be negative; no sign premise is used.

For parent mean m and the i-th descendant mean z_i, all off-diagonal parent-parent and sibling-sibling pairs are separated. Each mixed sum has D(D−1) separated terms and exactly D nested terms. Therefore

    E||m||² ≤ (1−1/D)(α+η)+1/D,
    E||z_i||² ≤ (1−1/D)(α+η)+1/D,
    E⟨z_i,m⟩ ≥ (1−1/D)(α−η)−1/D.

Subtracting twice the third expression from the first two cancels α exactly and yields E||z_i−m||²≤4/D+4(1−1/D)η. Pointwise X_i=f(z_i), hence m=D^−1∑f(z_i). Jensen plus Lipschitz continuity gives δ²≤L²D^−1∑||z_i−m||². Choosing D>4L²/δ² produces a fixed positive S-boundary lower bound, independent of A. This contradicts the usual nonempty finite left Følner criterion. The actual Moore published Theorem1.2 and its left-action footnote were read; use a smaller tolerance to pass from its sum bound to strict individual bounds. Nonemptiness is essential in the standard criterion, as it is explicitly in the OpenAI statement.

## Pinned analytic appendix: supplied displacement map checked directly

The appendix supplies the needed real Hilbert-ball map, so the external Benyamini–Sternfeld theorem is not being accepted as an unread additional analytic input. The construction works in L²([0,1];R²), with γ(t)=a(t)v(t), v(t)(w)=(cos(θ(t)w),sin(θ(t)w)).

The piecewise scalar profiles are C¹ at their junctions, have bounded Lipschitz first derivatives in the needed combinations, and γ' has squared norm a'²+a²θ'²/3. For t≤2, a'=1/8. For t≥2, a≥1/4 and θ'=1, so speed is at least1/(4√3)>1/8. Thus the global lower speed is exactly1/8; normalization gives a uniformly Lipschitz tangent u. Its correlation with v is a'/||γ'||≥0, including the negative straight ray where u=v.

The sinc identity for ⟨v(s),v(t)⟩ shows injectivity. Uniform separation at parameter distance≥d is stronger than pointwise injectivity and is actually proved: finite limits, two negative infinities, mixed finite/infinite limits and two positive infinities are all covered. On the positive tail, sup_(q≥d)sinc(q)<1 follows from continuity and decay, so the bounded tail has no unwanted near-returns at fixed parameter separation.

Choose d with Kd≤c/2 and then ρ with4ρ<σ(d), ρK_u<c/4 andρ<1/32. A minimizing sequence for a point withinρ of the curve is eventually confined to a compact parameter interval, giving attainment despite noncompactness of the curve. Orthogonality at minima and the tangent estimate yield ||x−y||≥(c/2)|t(x)−t(y)| for nearby tube points; taking x=y proves uniqueness, and2/c=16 gives the stated local parameter bound.

The rank-two rotation R=Id+A+A²/(1+κ), with κ=⟨u,v⟩≥0, maps u to v and is orthogonal. Its denominator is bounded below by1, so there is no singularity when u=v; the family is Lipschitz in operator norm. The correction q=min(a,−1/8)−a is bounded although a is unbounded on the negative ray. The two radial cutoffs glue the tube formula to the identity; their boundary decay controls cross-boundary pairs. Uniform boundedness controls distant pairs.

The nonvanishing estimate distinguishes all radial cases: insideρ/4 the v-coefficient is≤−1/8; betweenρ/4 andρ/2 the orthogonal rotated residual has norm≥ρ/4; in the outer shell the bounded correction vanishes and either the positive radial part dominatesρ or the straight-ray residual stays perpendicular. Outside the tube, γ(0)=0 gives ||x||≥ρ. Hence ||G(x)||≥ρ/4 everywhere. If ||x||≥1/2, reverse triangle inequality forces the nearest curve parameter onto the negative ray where both corrections vanish, so G(x)=x. Normalization f=−G/||G|| is Lipschitz; for ||x||<1/2 its unit norm gives displacement>1/2, and for the complementary region the displacement is1+||x||. No compactness of the Hilbert ball, Brouwer theorem or finite-dimensional substitute is used.

## Exact native corroboration and its limit

The complete7192-byte self-contained native Python program and both identical documented BUILD copies were read before the sole ordinary isolated invocation. There are no project-local imports; standard-library Fraction, lru_cache, json and seeded random are ordinary runtime dependencies. The run used current Python3.14.6, exit0, stdout274bytes/stderr0,2.184s. It checked1969transport pairs,31504local covariance cells,17recursive identities and one fully enumerated1024-cell image at level10. Original/copy input hashes remained exact. Its scalar color deliberately has a fixed point; it is not a displacement witness. This run corroborates bounded dyadic algebra only, not the analytic or infinite-group theorem, C*-simplicity or a Lean kernel build.

## LMB classical reduction: actual proof, not just corollary headlines

Read published LMB Sections2.1–2.5,3.1–3.2 with all supplied proofs, plus the intervening3.3–3.4 text and4.1 through Corollary4.4. The consumed route is3.1/3.2 and4.1; the stronger extreme-proximal results are not needed. Theorem3.7 requires a countable faithful subgroup of Homeo(X), X Hausdorff, with every nonempty-open rigid stabilizer nonamenable. It does not require minimality of the original action. Thus the standard F circle action's fixed point is not an omitted obstruction.

For a subgroup whose conjugacy closure avoids the identity, Lemma2.1 gives a finite witness P. Lemma3.1 chooses disjoint Ui and giUi, with an auxiliary neighborhood disjoint from the relevant supports. In Proposition3.8 the commuting rigid factors form L=∏G_Ui. The sets Yi of elements conjugating gi into the subgroup cover L. The finite-coset lemma yields a finite-index difference subgroup; projecting to one rigid factor retains finite index. The displayed product of two conjugates belongs to the target subgroup and restricts on Uℓ to γδ^−1, since its middle conjugated factor has disjoint support. The actual printed p577 pixel was inspected to disambiguate Greek factors lost in text extraction. This realizes a finite-index rigid factor as a subquotient of the subgroup. Amenability is inherited by subgroups/quotients and finite extensions, so a nontrivial amenable URS would contradict nonamenable rigid factors. The boundary/URS C*-simplicity equivalence is also given with exact countable scope in2.25/2.26; its boundary characterization is re-proved in the actual BKKO Sections2–3 read below.

The standard local affine copy construction supplies nonamenable rigid stabilizers conditional on the checked nonamenability input. Overgroups within Homeo(S¹) inherit them. This gives LMB4.1; F and T are countable standard circle overgroups, giving the needed forward direction of4.2. The reverse T implication is separately checked against HO, not inferred from subgroup inheritance of C*-simplicity.

## BKKO trace and boundary interfaces

Read actual published BKKO Sections2,3 through Theorem3.9, the full trace Theorem4.1/Corollary4.3 proof, and Section5's normal-subgroup theorem proof. Its setting is discrete groups, not arbitrary simple C*-algebras. The boundary construction supplies amenable point stabilizers and identifies the kernel with the amenable radical. G-injectivity extends a tracial state into the boundary crossed product; rigidity makes the boundary algebra a multiplicative domain. For s outside the radical choose a point moved by s and a continuous function separating that point from its s-inverse. The covariance identity forces the constant valueτ(λ_s) to0. Density identifies the remaining trace with the canonical one. Printed pages49–50 were individually viewed to recover not-equal signs lost in text extraction.

The normal-subgroup theorem is also checked in its actual proof: boundary actions extend via conjugation, the centralizer controls fixed elements, and the product-boundary argument gives normal-subgroup inheritance of C*-simplicity. This is the precise tool used by the reverse commensurator equivalence, not a general subgroup-inheritance claim.

A detail to keep precise: the converse trace construction works with the conjugation-invariant trivial character on an amenable normal subgroup. The printed proof's broad phrase about any trace is unnecessary; an arbitrary non-invariant trace need not compose with conditional expectation to a group trace. The specific character selected there has the required invariance. The target note uses the forward trivial-radical consequence, unaffected by that broader wording.

## Full Aut/Comm realizations and conventions under checking

Brin's actual Theorem1(i), definitions and complete Section2 argument were read. The normalizer is defined in full Homeo(R), and its conjugation map is an isomorphism onto full Aut(F). Section2 verifies approximate order transitivity and a bounded-support element, then applies the stated McCleary–Rubin reconstruction theorem. The latter is an established classical reconstruction input here, not claimed re-proved. No classification of every PL normalizer is needed for the required faithful Homeo(R) embedding.

Read BCRv4 in full, including its full proof of Theorem3.1. Finite-index subgroups contain F', so their local-moving and2-interval-transitive actions allow reconstruction of each isomorphism by a unique monotone real-line homeomorphism. This makes the commensurator map well defined and injective, including decreasing realizers. The explicit reflection t↦−t and the index-two positive subgroup make the full scope unambiguous. Its period calculations identify the precise full subgroup of line homeomorphisms, but the needed implication uses only the faithful embedding containing standard line F. Compare its earlier edition and the consumed addendum before final disposition.

Published LMB p582's surrounding PL notation should not be used to silently discard orientation-reversing elements. Its displayed line-tail threshold also lacks the negative sign on the left-hand bound. Brin's actual near−∞/near+∞ model and full Homeo(R) normalizer remove this ambiguity without changing a source file. A direct conjugator between the interval and line model, and its extension to all line homeomorphisms on the circle, will be written in the final derivation. Theorem4.3's ambient Homeo(R) itself has no positive-orientation restriction.
