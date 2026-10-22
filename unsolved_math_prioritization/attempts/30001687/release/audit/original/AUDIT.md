# Independent audit of Fibonacci spectral thickness

## Verdict and binding

**Accept the unsolved disposition, with a minor required correction to the finite-gap lemma's statement and two precision clarifications.** No full solution, spectral counterexample, precise weak-coupling asymptotic constant, or infinite-spectrum numerical bound has been established. The investigation remains **unsolved after 5 of 5 routes**. This review is not another proof-search route.

The frozen subject is ID **30001687**, code **OWR-4793-001**, rank **620**, titled *Spectral Thickness of Fibonacci Hamiltonians*. Before reading its contents, the reviewer computed the SHA-256 of the author's `SHA256SUMS`:

`2d657668c7f2b47f4429714e3e597baee441f32f58f262dc7bfb9d62dc5b4d8d`.

All seven listed files verified before review. All seven were read, including the complete proof, code, results, source descriptions, and research log. The originals remained unchanged, and their hashes were verified again after the controls. This review performed no remote writes. Administrative intake statements about the queue, other branches, and prior attempts were not independently re-audited; they are not mathematical evidence.

## Findings requiring attention

1. **Nonempty finite collection:** As literally stated, the conditional finite-gap lemma permits zero gaps. Its quantity is then the constant infinity, which is not strictly decreasing. Require at least one gap. This is a genuine edge-case error, with no effect on the intended nonempty applications or the unsolved conclusion.
2. **Hull regularity:** State explicitly that both hull endpoints, as well as every gap endpoint, extend C1 to zero. The proof uses this. The original wording can be read as applying C1 only to the gap endpoints. An explicit countercontrol in `CORRECTIONS.md` shows that even a differentiable hull at zero is insufficient without the asserted C1 control.
3. **Presentation coverage:** Make the last sufficient comparison explicitly use a bijection of the gaps and hence a bijection of all presentations, with corresponding endpoints. A non-surjective one-way transport would bound only the image presentations, not the supremum defining the second thickness. This is a precision clarification of the intended conditional comparison, not a proof of that comparison.

The replacement statements and proofs are supplied separately in `CORRECTIONS.md`. They do not change the frozen original and do not supply the missing spectral inequality.

## Primary source verification

### Original problem

The publisher's report was retrieved independently and printed page 164 was visually inspected. Embree's contribution specifies the discrete diagonal operator on l2(Z). Its final paragraph is motivated by the square spectrum but explicitly discusses thickness of the one-dimensional spectrum. It conjectures decrease with coupling and says it “behaves like 1/λ” near zero. That wording does not specify a limiting coefficient. The author's separation of the one-dimensional target from off-diagonal and continuum problems is correct. [Oberwolfach report 03/2011, printed p.164, PDF p.24](https://ems.press/content/serial-article-files/46317).

### Established theorem

Theorem 1.2, preprint p.4, states `C3/V <= tau(Sigma_V) <= theta(Sigma_V) <= C4/V` for small positive V. It therefore establishes the claimed order of magnitude, not `V*tau(Sigma_V) -> 1`. Proposition 3.11, p.20, gives a multiplicative distortion bound uniform in gap and coupling; it does not assert a coupling derivative sign. Theorem 1.3, p.5, asserts smooth boundary dependence for positive small coupling and a positive finite limit of gap length divided by coupling. Its statement alone is not a C1-at-zero theorem for every endpoint and the hull. Section 3.1's gap-opening proof was inspected; this audit does not claim that the stronger endpoint hypotheses are impossible or unavailable elsewhere. [Damanik and Gorodetski, arXiv:1001.2552](https://arxiv.org/abs/1001.2552).

### Numerical construction

Section 7.1 supports the rational-rotation potential, periodic and antiperiodic matrices, their band-edge eigenvalues, and the two-period cover. Equation (26), the matrix display, floating-point cautions, and the Figure 8 discussion were checked. The floor-difference formula agrees with the indicator formula including the lower threshold endpoint. Problem 8.1 asks historical monotonicity questions for spectral characteristics. It does not certify their present status. No error was found in the cited method's use here. [Damanik, Embree and Gorodetski, arXiv:1210.5753](https://arxiv.org/abs/1210.5753).

### Recent apparent match and other exclusions

The v4 abstract and introduction of the 2026 monotonicity paper assume analytic Type I potentials. Theorem 1.3 concerns open spectral gaps in the supercritical regime. Section 1.4 and the discrete Hellmann--Feynman discussion explicitly concern the energy parameter E. The Fibonacci step potential is discontinuous, and neither the hypotheses nor conclusion give its thickness monotonicity in coupling. The author's exclusion is justified. [Li, Xu and Zhou, arXiv:2601.02222v4](https://arxiv.org/abs/2601.02222v4).

The abstract of *The Fibonacci Hamiltonian* lists other spectral/dynamical characteristics and all-gap opening, not a thickness-monotonicity result. An abstract alone cannot exclude every theorem in a paper. [Damanik, Gorodetski and Yessen](https://arxiv.org/abs/1403.7823).

The current spectral-size paper's abstract and the available full-text occurrences of thickness/monotonicity were checked. No matching thickness-coupling theorem was located; algorithmic or approximation-index monotonicity is a different statement. [Colbrook, Embree and Fillman](https://arxiv.org/abs/2407.20353).

Embree's current publication list and fresh targeted searches were also checked. This bounded search did not find an applicable full resolution. It is not a universal certification of open status. [Author publication list](https://personal.math.vt.edu/embree/).

## Proof by proof adversarial review

### Route 1

For `f(t)=1/t+sin(1/t^2)`, positivity on `(0,1)`, the limit `t*f(t)->1`, the derivative, and its positivity at the stated sequence all check. This invalidates inference from asymptotic equivalence to monotonicity. It is correctly identified as a non-spectral example. A derivative estimate is needed to obtain monotonicity by differentiating an asymptotic expansion; this is a requirement of that route, not a claim that every possible monotonicity proof must differentiate.

### Route 2

The operator difference is positive, and the finite-dimensional ordered-eigenvalue and simple-eigenvalue derivative statements are correct. The four diagonal entries remain ordered on the stated interval. The induced one-gap quantity is `(1+t)/(2-t)` because its left band is the shorter band, and its derivative is positive. Its endpoint values are 1/2 and 1. The text correctly avoids claiming that the two intervals are the spectrum of the diagonal matrix.

### Route 3

The half-trace initial conditions, recursion, invariant, and differentiated recursion agree. The displayed eight derivatives are correct. They refute a global raw-coordinate sign induction, but say nothing by themselves about signs along actual moving spectral endpoints. The restriction of a possible cone argument to a dynamically relevant set remains a real distinction. No spectral counterexample is obtained.

### Route 4 and the ordering lemma

The exchange argument is valid. In the component written spatially as `A,g,M,h,C`, the old four affected ratios are

`A/g, (M+h+C)/g, M/h, C/h`.

If `g<=h`, the four new ratios are

`(A+g+M)/h, C/h, A/g, M/g`.

Every new ratio is at least the old minimum. Earlier removals and later removals are unchanged, since after the two steps the same two gaps are removed. Separate components are independent. For `g=h`, both minima are exactly `min(A,M,C)/g`; ties therefore have no effect on the optimum. Bubble-sorting inversions gives an optimal decreasing-length presentation.

The nearest-gap-of-at-least-equal-size formula is also correct at ties. A tied gap on the opposite side can be removed later, so the formula need not equal every individual endpoint ratio in one sorted presentation. It equals the global minimum: for any two tied neighboring blockers, whichever is removed second witnesses the same intervening distance divided by their common length. `CORRECTIONS.md` gives a proof that also treats unequal blockers and hull boundaries.

All matrices have period at least three, so the special period-one/two corner-entry cases are avoided. Pairing sorted periodic and antiperiodic eigenvalues is consistent with Floquet band edges. The 1e-12 merge tolerance is a floating-point heuristic; neither it nor an eigensolver comparison provides interval-certified endpoints. At the finest reported case the smallest band is about 3.24e-9, but this observation is not an error enclosure.

The Hausdorff countercontrol is valid. The cluster diameter is `1/N^2`, the first intercluster gap is `1/N-1/N^2`, and the bridge on its left is no longer than the first cluster under every presentation. The last cluster extends to `1+1/N^2`, which does not obstruct Hausdorff convergence to `[0,1]`. The thickness bound tends to zero. The example correctly addresses geometric convergence only.

### Route 5

After the stated scope correction, every fixed-order bridge is C1 with positive value at zero, while its gap opens with positive first derivative. Thus `B'g-Bg'` tends to a strictly negative number. There are only finitely many endpoint/order ratios, so a common interval exists. Finite minima and finite maxima preserve strict decrease; changing the optimal order or active endpoint does not invalidate the argument.

Filling bounded gaps while preserving the hull cannot lower thickness: restricting any presentation leaves longer or equal bridges and fewer endpoint constraints. The proof is sound.

There is a useful precision point about the remaining limit step. For an exhaustion by **actual bounded gaps** of a fixed Cantor set, an exact finite-gap exhaustion identity can be proved from the same blocker formula; it is recorded in `CORRECTIONS.md`. This does not make arbitrary spectral covers into gap fillers. In particular, the packet's periodic two-period covers have not been identified as true-gap fillers with exact endpoints. Even for true-gap fillers, a common coupling interval and parameter comparisons uniform over every gap generation remain missing. Local strict decrease separately for each truncation does not provide one common interval, and a pointwise limit of decreasing functions need only be nonincreasing.

The audit supplies an explicit family of one-gap examples satisfying the corrected lemma but whose intervals of decrease shrink to zero. This confirms that the missing uniformity cannot be discarded as a merely technical detail.

## Reproduction and independent controls

The frozen author script was run with `OPENBLAS_NUM_THREADS=1`. Its output was byte-for-byte identical to the frozen `control_results.json` in this environment:

- 1,536 exact finite-gap configurations
- 120 exact substitution-word transfer-matrix comparisons and trace invariants
- Six middle-third construction levels
- Nine free-operator periods: 3, 5, 8, 13, 21, 34, 55, 89, 144
- 36 floating-point spectral cases, with zero increases on the sampled coupling grid

The count 1,536 is `4^5+2^9`, representing 1,024 two-gap configurations and 512 four-gap configurations. These exhaustions are exact rational arithmetic. The free-operator tests and spectral scores use floating-point arithmetic and are not exact controls.

The separate script `independent_controls.py` imports no author functions. It uses an independently derived dynamic program optimizing over first removals, with optimal subproblems on the two resulting components. It passed:

- 4,235 additional exhaustive finite configurations (`3^7+2^11`), with three or five gaps
- 360 random-seeded rational configurations with one through twelve gaps, plus affine and reflection checks
- 1,875 adjacent exchanges, including 625 equal-length exchanges
- A symbolic trace-invariant identity
- 120 exact Floquet characteristic determinant identities and 60 rational-word trace-recursion matches
- The empty-gap counterexample and 100 exact tests of the nonuniformity family

An independent NumPy eigenvalue calculation reconstructed all 36 cases and the nine free periods. Band counts agreed in every case. The maximum absolute difference between finite scores was `1.5634047875745516e-11`. No sampled increase occurred. Shared floating-point infrastructure and a second implementation do not establish certified numerical errors or infinite-spectrum bounds.

## Publication and claim boundary

Retain the known-theorem attribution, five-route unsolved status, and absence of novelty. Apply the small finite-gap statement correction and presentation-coverage clarification before presenting the lemma as a formally quantified result. The audit binds the precise frozen manifest above; a changed author packet requires its own new manifest and a recorded reconciliation with these corrections.

No source PDF, source screenshot, full-text extract, catalogue corpus, or private coordination inventory is included in this audit package. No commit, push, publication, external message, or other remote modification was made.
