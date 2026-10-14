# Independent acceptance audit: relative symbols and boundary depth

**Row:** 1777 / 30005572. **Shared mathematical pass:** PASS 1/5 only. **Date:** 14 October 2026 UTC.

## Verdict

**Accept the pinned relative-symbol report as a correct partial reduction. Accept the pinned boundary calculations and boundary-localization proposition in their stated localized coefficient ranges.** No material proof defect was found. One coefficient-scope ambiguity found during review was corrected by the boundary author: the topological factorization criterion works over any coefficient ring, but its comparison with cusp-group cohomology explicitly retains inversion of 6. The final corrected input was checked and accepted; no remaining correction is required.

These acceptances do not construct the intended map. The actual bad-U identity, unrestricted parabolicity, integral theta descent and face relations, 5-primary motivic repair, and exact integral absolute target remain unproved. The original construction problem remains **UNSOLVED**. A generic obstruction to a naïve auxiliary recipe is not a counterexample to the intended construction.

This audit read the frozen construction contract and checked its hash. The auditor did not change author files, source files, a queue, remote state, or the mathematical-pass count. The boundary author made the single coefficient-scope correction noted above. Final accepted input hashes, together with the superseded audit-start hash, are in INPUT_PINS.json.

## 1. Relative-symbol proof

**Audited input:** RELATIVE_SYMBOL_DERIVATION.md, SHA-256 `06b0ae85504cae2bf55c5ffcd892cdb0db66b5641e1382dcac2b5edac99cb1c7`.

### 1.1 Generic triangle defect: accepted

For div(f)=m(0)-E[n], m=n², a nonzero rational n-torsion point T gives valuation -1 for f(x) along {T}×E and valuation zero for f(y) and f(-x-y). With the displayed tame-symbol convention, the three summands have respective residues f(y), 1, and f(-T-y)^{-1}. Their product is therefore exactly f(y)/f(-T-y).

The divisor of the denominator is m(-T)-E[n], because translation by T permutes E[n] and inversion fixes that set. The quotient consequently has divisor m(0)-m(-T). This is nonzero in the free divisor group and remains nonzero after localization at 6. It detects the claimed nonzero K₂ class over the function field. Passing to a field making T rational is legitimate for this direction: a zero original class would have zero restriction. No injectivity of restriction was assumed.

The evenness and CM-unit assertions are also valid in the asserted coefficient ring. A divisor-preserving automorphism changes f by a constant root of unity whose order divides the automorphism order. Imaginary-quadratic unit orders have no prime divisors other than 2 and 3, so symbols involving these constants vanish over Z[1/6]. This verifies the elementary orientation/unit checks while leaving the genuinely different triangle defect intact.

The report explicitly does not infer a nonzero torsion specialization from this function-field calculation. That distinction is indispensable and correctly maintained. Its discussion of the shifted Gersten primitive likewise does not promote a swap computation to full cusp-stabilizer invariance.

### 1.2 Smoothing and coefficient bookkeeping: accepted

Writing a=u^m/(σu) and b=v^m/(σv), expansion of the three symbols gives coefficients

- m² on {u,v};
- zero on both mixed pairs {u,σv} and {σu,v};
- -1 on {σu,σv}.

Thus the identity is precisely (m²-σ){u,v}={a,b}+{a,σv}+{σu,b}, integrally and without any division. Taking m=Nc yields the square of the ideal norm; for c=(n), m=n² and m²=n⁴. No interchange of these two degrees occurs.

Applying this formal identity to the intended theta system is correctly conditional on an actual distribution/reciprocity normalization. In particular, the mixed terms still involve the unsmoothed roots. Their descent, their agreement with the geometric cocycle, and division by a smoothing operator are not proved by this expansion. For a nonprincipal ideal, the report correctly retains the change of CM component instead of inventing a scalar endomorphism.

### 1.3 Root ambiguity and rational source formulas: accepted

Bilinearity gives exactly the three extra terms recorded under a change of two roots. If both roots of unity have orders dividing n, their sum is n-torsion; it need not vanish after inverting only 6. The example over Q(ζ₅), at a prime above 11, is valid: the fifth root reduces to an element of order 5, and the chosen valuation-one element gives a tame residue of that order. This is a formal example of retained 5-torsion, not an identified value of the sought CM map.

For any module, localization at n has kernel the elements killed by some power of n. A lift is therefore a coset of this kernel, if it exists. The report makes no unwarranted finiteness assertion about K₂ of a number field; its statement about finite modules is explicitly conditional.

The source comparison is accurate. Goncharov's Corollary 2.6 places the intrinsic unit in k×⊗Z[1/N]; Definition 2.8 uses N^{-5} and a rational Bloch-group target; Theorem 2.10 supplies the resulting rational boundary identity. These statements do not recover the N-primary data required over Z[1/6]. The source's averaging proof introduces the stated N³ and N² factors. The report does not silently replace its rational theorem by an integral theorem.

### 1.4 Relative extension, Smith criterion and saturation: accepted

The long exact sequence for a finite discrete cusp set gives

0 → H₁(X;R) → H₁(X,C;R) → ker(H₀(C;R)→H₀(X;R)) → 0.

The last module D is free, including when X is disconnected or some components miss C, so the sequence splits. This proves abstract extension for every target R-module. A splitting neither constructs theta values nor enforces the arithmetic calibration.

After a splitting, the prescribed corrections r_i must define a homomorphism on the endpoint submodule D_S. The exact sequence of Hom and Ext gives precisely the stated obstruction in Ext¹_R(D/D_S,M). Since R=Z[1/6] is a PID and D is finitely generated free, Smith normal form applies, and extension is equivalent to q_S(n_jb_j) belonging to n_jM. No division in a torsion target has been presumed.

For genuine unweighted edges, D_S is the graph-incidence image. Its quotient in R[C] is free on graph components, and D/D_S is the kernel of the map from these components to the components of X. Thus D/D_S is free and the endpoint submodule is saturated. This remains true for disconnected admissible-edge graphs and loops. The surviving condition is exact agreement of all endpoint-balanced sums with the already defined absolute map, including nonzero absolute cycles. Checking only triangle boundaries would be insufficient, as the report correctly states.

The resulting proposed integral theta/face lemma is labeled outstanding, not proved. Its polygonal obligations and all-component CM markings are substantive rather than claimed consequences of saturation. Goncharov §4.2 indeed has quadrilateral faces for discriminants -8 and -7 and hexagonal faces for -11. No theorem about non-Euclidean generation or integral elliptic symbols is imported without proof.

## 2. Local boundary computation

**Audited input:** LOCAL_BAD_LEVEL_LEMMA.md, SHA-256 `6d2edef937610dd887cf8185c798e86f010c786d31f5fa5b68c0cb69a0726509`.

### 2.1 Support and normalizations: accepted

The convention is unnormalized induction with left B-character α(x)β(z), right K₁(n)-invariance, and unnormalized finite sums of right translations. This matches the source's local good-prime calculation Qμ₁(π)+μ₂(π). It must not be conflated with normalized induction or an arbitrarily normalized adjoint Hecke action.

The bottom-row invariant min(v(c),n) classifies the displayed B(O)\GL₂(O)/K₁(n) double cosets. Computing k_j^{-1}hk_j gives independent diagonal ranges 1+π^{n-j}O and 1+π^jO for interior indices. At j=0 the second character must be unramified; at j=n the first must be unramified. Consequently, when a,b>0, the supported indices are exactly b≤j≤n-a, and the dimension is max(0,n-a-b+1). Reducibility of the principal series causes no exception to this calculation.

The two double-coset decompositions each have Q representatives. Both displayed matrix factorizations multiply out exactly. In the first factorization, β(1+π^jt)=1 because j≥b; in the second, α(1+π^{n-j}t)=1 because n-j≥a. The rightmost diagonal matrices belong to K₁(n). Hence the respective basis actions are exactly

Ue_j=Qα(π)e_{j-1}, and V_ope_j=Qβ(π)e_{j+1}.

### 2.2 Oldvectors and integral consequence: accepted

Both operators are nilpotent with exponent at most d=n-a-b+1 when d>0. If d≥2, the adjacent-shift coefficients are nonzero in characteristic zero, so the operators are not identically zero. The n=a+b+1 case is already a nonzero square-zero example. The two shifts need not commute with each other; only one operator per bad prime is used in the subsequent commutative Hecke algebra.

Inversion of a correspondence rather than taking its adjugate differs by an invertible central scalar on each characteristic-zero constituent. This preserves nilpotence; it does not identify the convention satisfying the desired K₂-map relation.

For any T with T^d=0, 1-T has the finite geometric-series inverse. Nilpotence descends from a rationalization to a preserved torsion-free lattice by injectivity into that rationalization. There is no division by Q or a character value in this inference, and no integral decomposition into individual principal-series pairs is needed.

## 3. Global boundary proposition

**Audited input:** BOUNDARY_REPORT.md, SHA-256 `613dce536eca6a92c7ec316b97750857e2e44a47ea3839a1f94ae928452db678`.

**Accepted with its existing residual-character exclusions and p≥7.** The new assertion is boundary localization at arbitrary depth, for the explicit double-coset operators. Application to the specialized K₂ map remains conditional.

The finite integral Hecke-image argument is sound. The boundary H¹ module is finite torsion-free over the coefficient DVR. Its faithful Hecke image A is finite torsion-free as well. Minimal primes of A avoid the uniformizer, and any maximal ideal in the support admits a characteristic-zero branch specializing to it. Faithfulness makes this generic branch occur on the module. This avoids any need to assume that different ordered pairs of residual characters define distinct maximal ideals.

The source's boundary description is an induced-representation realization. Its construction from cusp stabilizers is natural for right finite-adelic translation and the associated restriction/conjugation/transfer operations. Thus the level double cosets act by the local sums used above, just as the good-prime operators do. The companion pair (μ₂N^{-1},μ₁N) exchanges ramification places, since the norm character is unramified. If both characters ramify at one prime above p, either chosen local operator has eigenvalue zero on the entire corresponding invariant space. Such an eigenvalue cannot specialize to 1. At least one inducing character is therefore unramified at every prime above p on a surviving branch.

The good-prime congruences give ων₁+ν₂=ω+ν₁ν₂ and ν₁ν₂=χ. Character independence yields ν₁=1 or ν₂=ω. The ensuing local cases check exactly:

- ν₁=1 forces μ₁ ramified at the distinguished prime, so μ₂ is unramified and χ restricts to ξ;
- ν₂=ω in the split case forces μ₂ ramified at the conjugate prime, so χ restricts there to ξ̄;
- ν₂=ω in the inert and ramified cases forces χ to restrict respectively to ξ^p and ξ.

Only the forward implications of source Remark 5.2.5 are used. No single-depth converse is reintroduced. These are precisely the excluded loci, so the stated localization vanishes. The proof does not show nonvanishing on the exceptional loci.

The explicit distinction between the two bad-level specialization directions is correct. A nonunit lower-right entry lowers the torsion order; the opposite direction lacks the extra branch of the unramified double coset. Neither is handled automatically by good-prime specialization. The finite-coset identity (U) is a well-formed constant-coefficient transpose/transfer condition for the actual specialized homomorphisms. It is clearly left unproved. Local representation theory does not establish it.

## 4. Stabilizers, compactification and the remaining cusp test

**Audited input:** STABILIZERS_AND_OBSTRUCTION.md, SHA-256 `55300f71adeef0e0d8e8dea4a578122c9f49116cf1a6b9119fb028e06da04055`.

The stabilizer theorem is correct: if a prime ℓ divides the order of a finite subgroup of GL₂(F), an order-ℓ element has a primitive ℓth-root eigenvalue of degree at most two over F. This forces ℓ≤5. For ℓ=5, the only quadratic subfield of Q(ζ₅) is real, whereas F is imaginary quadratic, so the degree over F is four, a contradiction. Thus only 2 and 3 occur. This is a statement about prime divisors of stabilizer orders, not a claim that all stabilizer groups have order 2 or 3.

The arithmetic groups in question have finite point stabilizers, including their finite scalar kernels. On a proper contractible cellular model, subdivision removes inversions. Inverting the stabilizer orders kills all positive stabilizer homology, so the equivariant spectral sequence identifies group and coarse quotient homology over Z[1/6]. The same applies to the Borel–Serre model. Hecke compatibility uses the transferred finite-index correspondences under this comparison, not an assertion that every map of coarse orbifolds is an unramified covering.

Collapsing each connected Borel–Serre boundary component to its own cusp gives the exact sequence H₁(D)→H₁(M)→H₁(X)→0. The final surjectivity follows from the isomorphism on H₀ from boundary components to their separate cusp points. Thus annihilation of the particular boundary image is exactly the criterion for factorization, and factorization is unique.

**Scope correction verified:** the topological sequence and criterion hold over arbitrary coefficients. Equivalence with restriction to cusp-group cohomology invokes the group/coarse comparison and requires 6 invertible. The author corrected §2 to say this explicitly. The final hash above contains that correction, and all asserted applications over Z[1/6], Z[1/30], or Z_p with p≥7 remain valid.

A cusp stabilizer has a rank-two unipotent lattice and finite unit quotient. After inversion of 6, its H₁ is a quotient of the lattice tensored with the coefficient ring. Vanishing on two lattice generators, for every cusp and component, therefore suffices for the exact boundary test (P). The report requires the actual descended specialization and does not identify Galois invariance with integral descent. It also correctly retains the source's unit-injectivity restriction when discussing maps already constructed there.

The geometric comparison does not eliminate the motivic trace-fixed complex's inversion of 5. The separate arithmetic, geometric, and auxiliary-removal issues remain distinct throughout.

## 5. Primary-source checks and verification boundary

The audit inspected the retained primary texts, using PDF extracts for formulas and section references:

- [Sharifi, Oberwolfach report contribution](https://ems.press/content/serial-article-files/47022), printed pp.1565–1568: integral target, relative-symbol ambition, all components, and missing theta normalization.
- [Lecouturier–Sharifi–Shih–Wang, arXiv:2504.19125v1](https://arxiv.org/pdf/2504.19125v1), and the distinct [author-hosted manuscript](https://www.math.ucla.edu/~sharifi/publ/imagquad.pdf): introductions, §§3.2, 3.4, 4.1, 4.3, and the relevant §5.2 statements and proofs. The local induction conventions, source coefficient localization, broader auxiliary removal, forward residual implications, and unproved status of Remark 5.2.10 were checked. The author-hosted file was not assigned an unsupported revision label.
- [Goncharov, arXiv:math/0510310v5](https://arxiv.org/pdf/math/0510310v5), Corollary 2.6, Definition 2.8, Theorem 2.10 and its proof, and §4.2: localized/rational coefficients and polygonal-face distinctions.
- [Sharifi–Venkatesh, Eisenstein cocycles in motivic cohomology](https://math.ucla.edu/~sharifi/eisensymbol.pdf), §1.2, formula (2.4), and §6.3: normalized auxiliary theta divisor, reciprocal tame-symbol convention, and trace-fixed theta primitives.

The current arXiv landing pages were also checked for source identity and version metadata. No copied source text is included in this audit. The audit independently checks the displayed partial proofs; it is not a reproof of the full cited motivic constructions or Harder's boundary theory, a literature-exhaustiveness certificate, or a novelty claim.
