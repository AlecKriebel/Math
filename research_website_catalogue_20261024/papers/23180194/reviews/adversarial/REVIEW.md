# Independent adversarial review: Zenodo 23180194

**Verdict: PASS for the mathematical theorem at its stated hypotheses.** No substantive defect or unresolved load-bearing mathematical gap was found. This is an AI adversarial review, not human peer review, a formal proof, novelty certification, or publication authorization.

The strongest verified conclusion is the published Theorem 1: on an lcsc Hausdorff Abelian group, for a jointly measurable action on an arbitrary measurable ambient space, sigma-finite Q and a measurable covariant locally finite Radon measure xi nonzero Q-almost everywhere, full ambient invariance under every invariant, pointwise xi-preserving, xi-measurable **Markov** kernel implies full joint Campbell reversal. The credited Mecke/Palm and Palm/mass-stationarity equivalences yield mass-stationarity; credited transport invariance supplies the converse. The proof does not require a standard Borel ambient space, sigma-finite law of xi, or finite intensity.

## Exact objects and coverage

- Published `mass_stationarity_markov.pdf`: seven pages, SHA256 `3503e9351da854e882cd8ce26f1450482b44e1f5e547b06224875c3b55b391f3`.
- Published `mass_stationarity_verification.zip`: SHA256 `6007977e60dd4464e0c62309ad694697d4f927bae407531b0bee5285e80fa8a9`.
- Both match the fresh acquisition receipt. All 19 extracted regular members were compared byte-for-byte with the ZIP. The complete source binding and primary PDF hashes are in `evidence/source-binding.json`.
- Read all seven PDF pages and full `paper.tex`; visually inspected all seven rendered pages, including equations (10)–(16). No relevant mathematical expression is missing or altered by extraction.
- Read both scope documents, both READMEs, bibliography, all three submitted mathematical control scripts and the portable verifier. The packaged `PRIORITY_NOTE.md`, historical reviewer verdicts and stored expected-result bodies were not opened as review evidence. The verifier itself necessarily reads expected stdout for byte comparison.
- The complete mathematical argument is in the seven-page paper; there is no extra reader PDF.

## Independence and incidental exposure

No current sibling analytic/scope report or verdict was consulted. Coordination was limited to raw primary-source availability. This review's own exact controls were written and run before reading the submitted scientific checker implementations. A provisional analytic conclusion was logged before the submitted replay.

Required public support contains historical internal-acceptance language, prior finite-control totals and summaries of bounded priority searches. The manuscript itself also mentions earlier literature reviews. These incidental opinions were seen and are disclosed; they were not used as evidence. Consequently this review does not claim strict blindness to every historical opinion. It remained independent of current sibling conclusions. No inference of present openness or priority is made.

## Proof attacks and resolution

### 1. Test class and full ambient quantifiers

The hypothesis is stronger than merely keeping the distribution of xi fixed: f ranges over all nonnegative ambient measurable functions. The constructed kernels only use xi and the spatial starting point. In particular the arbitrary finite-Q set D used in the oriented proof is introduced through f, not through the kernel gate. This preserves the required measure-only dependence.

The quantifier over **all** such Markov kernels is essential. No claim follows here for only deterministic allocations, one fixed local kernel, canonical-state-only tests, or the smaller class of intensity-erased Cox-allocation-derived kernels. The original LT2009 §3 definitions use pointwise preserving kernels just as this paper does; its Problem 7.3 is the literal all-Markov target.

### 2. Local kernels, atoms, and holding mass

For symmetric compact C, the conductance a is symmetric and nonnegative, measurable and translation covariant. The first denominator alone bounds its row integral by mu(s+C)/(1+mu(s+C)); the second denominator cannot increase it. Thus adding `(1-r_b) delta_s` gives a Markov row even when the starting point is outside the support or mu is zero. Atoms at s are included consistently in both the jump and holding contributions.

The gate is a Borel involution-invariant indicator. Symmetry makes the incoming weighted flux equal to `r_b(t) mu(dt)`, and adding the holding flux recovers mu. Tonelli, rather than a difference of two infinite masses, proves preservation for infinite total mass. A negative control confirms that simply normalizing a symmetric jump row need not preserve the spatial measure; the specific lazy construction matters.

### 3. Oriented reversal and arbitrary ambient sigma-field

For `F={(mu,t):mu in A, theta_t mu not in A, t in B}`, F and R0F are disjoint. On F the incoming test `1_D(theta_t omega)1_A(theta_t xi)` vanishes; on R0F the outgoing test vanishes. The surviving incoming integral is exactly `(R_*m)((D x B) intersect rho^-1 F_A)`. This checks the potentially delicate minus sign and gate orientation in equation (11).

Finite Q(D) makes both jump integrals and the holding integral finite, justifying the only subtraction. For the restricted measures on rho^-1 F_A, each block D_j x G has finite mass and equality on all measurable rectangles. The finite-measure uniqueness theorem applies to the rectangle pi-system regardless of whether the ambient sigma-field is countably generated. The countable separating family is needed only on the standard Borel Radon-measure space M. Disjointifying its cover of J-complement is valid after equality has been established on every measurable subset of each piece.

The involution is measurable in both directions because it is its own inverse, so images such as R0F are measurable without an unmentioned image-measurability theorem.

### 4. From a local weighted identity to global Campbell reversal

Covariance and symmetry give `w o R=w`. The weight is finite and strictly positive on Omega x C. Truncating 1/w and taking a monotone limit removes the weight without integrability assumptions. A separate admissible kernel argument is made for each compact symmetric neighborhood in an exhaustion of G. This yields equality for every measurable subset of J-complement, not merely equality on one local set.

The Campbell measure is sigma-finite through the explicit product sets `(D_j intersect {xi(C_n)<=k}) x C_n`. Their union covers all of Omega x G because local finiteness holds pointwise. This is a proof about the joint measure, not the marginal law of xi.

### 5. Period subgroups: preservation and measurable dependence

H_mu is a closed subgroup and its graph is Borel. Abelianity gives `H_(theta_s mu)=H_mu` and later inversion invariance of subgroup Haar measure. The construction integrates this graph against the measure kernel; it never needs a jointly measurable selection of subgroup Haar measures.

For a **fixed** mu, `(theta_s mu)|H` is an H-invariant Radon measure and hence either zero or a scalar multiple of Haar measure. That scalar is finite: evaluate on a compact H-neighborhood with positive finite Haar measure and use local finiteness. The scalar need not be selected measurably because it is used only inside this fixed-mu preservation proof.

If Haar(H intersect B)=0, every row holds. Otherwise the positive-denominator rows all have the same normalized Haar displacement law. The set E of such starting points is measurable and H-invariant; so mu restricted to E is H-invariant. Translating that restricted measure proves preservation, while the complement holds. This also handles mixed measures with singular period cosets and zero denominator rows.

### 6. Ambient information on periods and infinite expectations

Every displacement of kappa_B lies in H_mu, including the zero branch. Thus it preserves xi and w_B pointwise while it may change the ambient state. Applying the assumed invariance to `w_B(xi) f` cancels the normalization. At w_B=0 both relevant nonnegative integrands are zero, including when f is infinite. No subtraction or finite-expectation assumption occurs.

Haar inversion on Abelian H gives w_-B=w_B. Equation (15) consequently is the required rectangular Campbell reversal on J. For the final uniqueness argument, the same explicit finite product cover bounds both restricted measures by the rectangle identity. Intersections with rectangles still form a generating pi-system. A common countable generator for the ambient space is not required.

### 7. Completion, support and the sampling convention

J and its complement are invariant under reversal, so their two established equalities add to full Campbell reversal for every nonnegative product-measurable g. LT2009 equation (2.7) is precisely the needed arbitrary-ambient, sigma-finite Mecke/Palm characterization, and Theorem 6.3 has the same setting. Its Theorem 4.1 yields necessity for the paper's pointwise-preserving Markov tests.

Origin-in-support follows rather than being presumed: reversal sends the event `{0 outside supp xi}` to `{t outside supp xi}`, which has zero xi-mass. The exhaustion and nonzeroness then force Q-nullity. For Haar-almost every r in a continuity set C, r is interior, so C-r is a neighborhood of zero; the sampling denominator is positive on these Palm states. The stated holding convention in zero-denominator rows introduces no new positive-measure branch in the conclusion.

## Boundary controls beyond finite enumeration

These are direct checks of the proof's mechanism, not extra theorems asserted by computation.

- **Pure Haar measure:** H=G and the off-period contribution is absent. Normalized restrictions test the full ambient state. With a constant xi and a biased marked state, canonical xi-law invariance is automatic but ambient invariance fails. The independent negative control detects this.
- **Diffuse periodic measure on R:** for `(2+sin(2*pi*x)) dx`, H=Z but mu(H)=0. Hence the Campbell period part vanishes even though H is nontrivial; off-period reversal covers everything of positive Campbell mass.
- **Mixed periodic measure:** for `dx + sum_{k in Z} delta_k`, H=Z. The restriction to H is counting measure. Positive period rows occur on lattice cosets with atoms, while Lebesgue-almost-every nonlattice starting point holds. Restricting to the H-invariant E makes the preservation proof valid for both components.
- **Non-sigma-finite marginal law:** take counting Q on N, a trivial action and fixed nonzero Haar xi. Q is sigma-finite but its pushforward is infinite mass at one measure and is not sigma-finite. The joint Campbell measure is sigma-finite and all the paper's proof steps remain meaningful; no disintegration over xi is needed.
- **Zero measure:** the canonical zero state satisfies all transport-invariance tests but is excluded by the source mass-stationarity convention. The hypothesis is necessary, not cosmetic. The independent zero controls have no Campbell constraints.
- **Trivial group, zero Q, finite compact groups, unbounded local masses across omega, infinite xi(G):** none invalidates the argument. Nonzero local finite measures on the trivial group automatically have origin support; finite-Q truncation handles unbounded masses; all infinite integrations elsewhere are nonnegative.
- **Non-Abelian or non-locally-finite settings:** not established. Removing Abelianity breaks stated period-subgroup identifications/inversion steps; removing local finiteness breaks the conductance/normalization bounds. No extension is inferred.

## Primary imports and attribution limits

The raw primary PDF hashes and URLs are retained in `evidence/source-binding.json`. Actual passages were read rather than relying on abstracts or inherited review statements.

1. **Last–Thorisson 2009**, official electronic reprint arXiv:0906.2062v1, SHA256 `0a4c4813cef44e99c232d0687aa704554248675c621755be85568d0588999719`: §§2–3 supply the arbitrary measurable ambient flow, locally finite measures, sigma-finite Q/P and pointwise preserving definitions. Equation (2.7), reprint p.7, explicitly supplies the Mecke/Palm equivalence in this ambient setting and discusses the extension from Mecke's canonical formulation. Theorem 4.1, pp.12–13, supplies transport invariance; Definition 6.1 and Theorem 6.3, pp.17–21, supply the matching mass-stationarity definition/equivalence. §7, pp.22–24, distinguishes bounded weighted kernels (Theorem 7.2) from Markov kernels (Problem 7.3). All load-bearing imported hypotheses match.
2. **Last–Thorisson retained 2015 author v2**, SHA256 `b265c6d7984627f4b186ffbef8efa8faf75a94db674f55ae1333698d20c7c0cb`: §6, pp.9–10, Theorem 6 has the positive density field, line integrability and infinite half-line integral conditions described by the note. It tests the joint pair containing Z. The final journal body was not authenticated here; no author/final identity is asserted. This is antecedent comparison, not a load-bearing implication in the proof.
3. **OWR47/2008**, SHA256 `cdeba309c149d8dcce1f0b5c6e0e38e5d19ce4a36e6e97c0dd557a1da7fa7a23`: Last p.2673 poses the allocation-derived Cox question; Thorisson pp.2692–2694 defines transport kernels as Markov and discusses the broader converse. The paper correctly avoids claiming the smaller-test-class Cox result.
4. **LT2011 COSA:** authenticated full body was not acquired in this review; only the official LSU bibliographic page and documented failed primary-body attempts are available. Therefore the exact numbered antecedent comparisons (Propositions 3.6/3.8, Remark 3.11) are not freshly authenticated by this reviewer. They are not premises of the present proof. This is a non-load-bearing bibliographic coverage limit, not a reason to infer correctness or novelty.
5. **Mecke1967 and general measure/Haar background:** the full original Mecke body was not reacquired. The proof explicitly uses the audited ambient statement in LT2009 (2.7), which credits Mecke. Standard Radon-space Borel facts, Haar uniqueness and finite-measure uniqueness are used at their ordinary stated hypotheses; the relevant usages were reconstructed above. No unspecified modern theorem replaces the main argument.

Online primary version records were checked at https://arxiv.org/abs/0906.2062v1 and https://arxiv.org/abs/1405.7566v2. This is not a forward-citation or exhaustive priority search.

## Fresh computational evidence and reproduction

`evidence/fresh_controls.py` is a new standard-library implementation using exact rational arithmetic and independently coded Gaussian elimination. It compares the row space of ambient transport stationarity constraints to the full Campbell-reversal constraints, rather than only checking one guessed Palm law. It covers 45 finite cases (44 nonzero and one zero boundary), cyclic groups up to order 12 and Z4 x Z2, Z3 x Z3, Z2 x Z2 x Z2, with 955 kernels. For every nonzero case, the two constraint row spaces coincide and have rank |G|-1. Checks include Markov rows, spatial balance and equality of displacement rows whenever the observed measure is equal. Four negative controls detect canonical-only blindness, omission of period tests, failed naive row normalization and the excluded zero case. Results: `evidence/fresh-controls.json`.

After this independent implementation and provisional analytic conclusion, all published controls were replayed with Sympy 1.14.0, enabled assertions and `-E -B`. The portable verifier returned `PASS_FINITE_CONTROLS_AND_PACKAGE_HASHES`; all three complete stdout streams matched their archived expected bytes, stderr was empty, and exit status was zero. Their assertion totals were freshly reproduced (18,814; 75,172; 186,869), not accepted from README claims. Results: `evidence/published-replay.json`; environment installation log retained separately.

The historical Cox checks in two scripts are ancillary and do not prove the narrower Cox allocation converse. None of these finite computations verifies arbitrary ambient measurability, infinite groups, sigma-finite extensions or the universal theorem. Those judgments rest on the audited analytical argument above.

## Remaining gaps and disposition

**No unresolved substantive mathematical gap was identified in the main theorem.** The unacquired LT2011 body, full Mecke original, final 2015 journal body, and current-literature/priority coverage remain explicit limits. They do not conceal an unverified load-bearing main-proof import: the precise cited LT2009 imports were checked in their actual primary body.

The theorem is supported exactly as an all-measure-only-Markov, full-ambient equivalence in the stated Abelian/local-finiteness/sigma-finite/nonzero setting. No stronger allocation, Cox, non-Abelian, zero-measure, or novelty conclusion is approved by this review. No manuscript repair or public mutation was made.
