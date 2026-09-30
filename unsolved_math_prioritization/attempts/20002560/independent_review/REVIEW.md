# Independent review: exact forward-KL radius of RBM(3,1)

**Verdict: PASS_COMPLETE_FORWARD_KL_CERTIFICATE_WITH_SOURCE_QUALIFICATION.** The analytic argument and all six finite certificates pass independent verification. No mandatory mathematical correction was found. The exact forward-KL radius, with natural logarithms, is

$$c=-\frac34\log(2\sqrt3-3),$$

and its only maximizing targets are the two uniform parity distributions. This is a credited verification of the prior anonymous candidate, not a campaign discovery. Recommended classification: **already_solved, 1/5**, explicitly for the intended forward-KL interpretation. The AIM wording allowing an unspecified divergence has no single numerical answer and is not resolved as a universal all-divergence claim.

Reviewed `SOURCE_APPLICATION.md`: SHA-256 `ee7f56ff3427575a1892d25141a728e366262b12f01b49cacb0a1a346ed025a3`. Its mathematics was unchanged during review. This is independent adversarial AI verification, not journal peer review, authenticated independent-person review or proof-assistant formalization.

## 1. Original question and prior provenance

The cached complete [AIM item1.2](http://aimpl.org/boltzmann/1/) was inspected. It asks for the maximum divergence of RBM(3,1), then explicitly permits any divergence, giving KL as an example. The source application correctly fixes forward KL rather than pretending that this unspecified choice defines a universal number. Section9 item10 of [Montufar's 2018 review](https://arxiv.org/abs/1806.07066) independently records the precise approximation-theory question and the conjectured constant, crediting discussions with Johannes Rauh. Its base-two expression converts to the natural-log constant above. The nearby RBM(3,2) theorem concerns a different model and is not used here.

The [Evidence Press release](https://evidencepress.org/releases/rbm31-exact-kl-radius/) and the cached Zenodo metadata identify an earlier candidate dated 5September2026, DOI[10.5281/zenodo.22339153](https://doi.org/10.5281/zenodo.22339153), version0.1.0-candidate. Its status is anonymous, AI-assisted and unrefereed. These qualifications remain unchanged by this review. No scholarly authorship is inferred from the repository account name.

I read the complete relevant analytic proof, Sections2–6, from the pinned upstream manuscript. The six certificate files were independently fetched again from commit `2736c6c381c8479d4bd97883e9f1ad959a0640f2` of the [upstream repository](https://github.com/ipitchford/rbm31-exact-kl-radius) and compared byte-for-byte with the submitted data. All six match; `data_provenance.json` records their hashes and exact URLs. Only JSON data were read. No producer software was imported or executed. The original certificate data carry the stated CC0 dedication; credit must remain with the prior source.

## 2. The probability model and boundary points

A positive-parameter mixture of two Bernoulli products is a finite-parameter RBM(3,1): factor one product and express the second-to-first ratio by a hidden bias and three logit differences. Conversely, summing the binary hidden variable gives such a mixture. The compact seven-parameter cube gives the closed model. Boundary distributions cause no loss of the infimum: the uniform product supplies finite divergence, a minimizing closed-model distribution is positive on the target support, and interior approximation of its mixture parameters makes its divergence converge on that support. The use of a closed minimum and a finite-RBM infimum is therefore consistent.

The argument never identifies this two-product mixture model with an RBM having two hidden units. It does not assume a boundary characterization by tensor-rank inequalities.

## 3. The parity lower bound

The displayed star distribution is exactly a point mass/product mixture. I independently verified its normalization, strict positivity and the full mixture identity in the quadratic field Q(√3).

For every mixture with interior parameters, coordinate complements can order its two component parameters coordinatewise. Its log density is then a modular function plus a softplus of a nonnegative-coordinate linear form. Integrating the nonnegative second derivative of softplus gives every required log-supermodular inequality. Complementing all three coordinates preserves the cone by interchanging meet and join. Consequently four even complements represent all orientations while leaving the even-parity target unchanged. This parity property uses the odd number of coordinates and was checked explicitly.

At the star distribution, the three specified active face identities and positive gradient multipliers are exact. Convexity of log-sum-exp then proves the required lower bound throughout each cone. Only the necessary inclusion of mixtures in these cones is used. Interior approximation extends the conclusion to closed-model boundary points; a zero over a positive target entry gives infinite divergence and cannot invalidate the bound. The explicit mixture attains the lower bound. The odd-parity case follows by one coordinate complement.

## 4. Support reduction and the continuous upper-bound mechanism

A stochastic channel on one bit maps each product distribution to another product distribution, and therefore preserves the two-product model. The direction of the data-processing comparison is correct: distance to the model cannot increase under the channel.

The inverse-channel construction uses unnormalized slices. The minimum positive ratio makes the new table nonnegative, keeps total mass exactly one, introduces no new support entries, and removes at least one old entry. The stated channel reconstructs the original table. Empty-slice cases are handled separately: any distribution on the remaining two bits is a two-product mixture by conditioning on one of those bits. Thus the reduction terminates after finitely many genuine support decreases.

I independently enumerated the 255 nonempty supports using coordinate deletion on binary strings. There are exactly 50 terminal supports, with the six stated disjoint symmetry-orbit sizes 4,8,24,2,8,4. This enumeration does not discretize their weights.

The root simplices cover all continuous weight vectors. For the parity support, ordered weights have the displayed nonnegative barycentric decomposition into nested uniform supports. The five-point support is the cone over the analogous odd-parity cover, with the point-mass coefficient retained. The four other supports use their full standard simplices. This gives 52 roots.

Every valid edge bisection covers its parent, by the exact barycentric coefficient transformation given in the artifact. Starting with affinely independent root vertices, each such bisection preserves the simplex dimension and distinctness of its vertices. The tree validation verifies both children, unique record addresses and reachability, so there are no missing pieces or unexamined extra leaves.

A leaf has one common feasible witness for all its vertices. Its rational mixture parameters are reconstructed as exact probabilities, including zero entries; star witnesses use the exact algebraic distribution. Finite divergence is checked on every positive target coordinate. Convexity of forward KL in the target therefore extends the certified vertex bound to every real point in that leaf. This common-witness step is valid even though the mixture model is nonconvex and the chosen witness need not be optimal within the leaf.

## 5. Independent certificate implementation and rigorous arithmetic

The submitted checker uses 80-bit fixed point and 32 terms. I audited its floor/ceiling recurrence: nonnegative lower powers remain below the exact powers, upper powers remain above, the positive tail bound is added only to the upper endpoint, and negative binary scaling reverses the correct endpoints. Entropy upper bounds, witness log lower bounds and the lower endpoint for c are combined in the correct directions.

I also wrote and ran a separate checker, `independent_cover.py`, without importing either the submitted checker or any producer program. It uses **64-bit scale and 24 terms**, computing each atanh-series term through exact integer powers and separately rounding its quotient. It does not use the submitted rounded-power recurrence. The remainder bound follows from

$$2\sum_{j\ge m}\frac{y^{2j+1}}{2j+1}
\le\frac{9}{4(2m+1)3^{2m+1}},\qquad0\le y\le1/3.$$

Integer square-root inequalities bound √3, affine arithmetic bounds the star entries, and monotonicity gives the logarithm bounds. No floating-point logarithm or tolerance enters a proof decision. A further independent rational-series check strictly encloses the true logarithm inside the returned fixed-point intervals for 240 controls, including positive and negative binary exponents.

The full fresh replay passed:

- **52 roots, 16,600 leaves, 93,792 vertex incidences**
- **552 exact parity equality incidences**, accepted only with the correct parity-translated star witness
- **93,240 strict non-parity vertex inequalities**
- Maximum depth **20**
- **453,448 independent cover assertions**

The smallest independently certified strict vertex margin is

$$\frac{208691956875743}{73786976294838206464}>2\times10^{-6}\ \text{nats}.$$

This is a finite vertex-test margin, not a uniform gap from c for all nonmaximizing targets. An additional analytic checker passed **6,179 exact controls**, including the lower-bound algebra, 780 reverse-channel cases with zeros permitted, root/bisection identities and logarithm containment. Nine malformed certificate variants were independently rejected.

The author's **376,307 cover assertions** replayed with a byte-identical cover receipt. Its additional **4,135 controls**, including seven rejection cases, also passed. These are kept separate from the fresh review counts.

## 6. Equality cases

On any finite-divergence simplex, the target dependence of KL is strictly convex because the entropy term is strictly convex and the cross-entropy term is linear. Thus a nonvertex convex combination has strict inequality whenever its vertices have bounds at most c. Every non-parity leaf vertex was itself certified strictly below c. Consequently the only possible terminal-support maximizers are uniform parity laws.

If a genuine support reduction occurred before reaching parity, the final inverse channel merges both input bit states with positive witness mass. In every such pair, exactly one parity target entry is positive, so the two likelihood ratios differ. The equality criterion for the log-sum inequality therefore fails and the data-processing comparison is strict. Earlier channels preserve that strict upper bound. This rules out all additional maximizing targets. The compact-boundary and zero-target cases are covered by the same argument.

## 7. Reproduction and final scope

The review directory contains the six unchanged JSON files and attribution through `data_provenance.json`. With Python3 and SymPy available for the analytic checker:

```sh
python independent_cover.py
python independent_analytic.py
python check_rejection.py
(cd author_replay && python check_cover.py ../certificates)
(cd author_replay && python test_independent.py ../certificates)
```

The first checker uses only Python's standard library; the second uses SymPy solely for exact algebra. No unrecognized producer software is needed. The trusted computational base is the analytic proof, these locally authored checkers, integer/rational arithmetic semantics and the execution environment. This is a computer-assisted proof verification, not formal proof-assistant certification.

The complete forward-KL theorem passes. The source-qualified already_solved recommendation is appropriate only with that divergence, direction and logarithm convention stated explicitly. The arbitrary-divergence remark remains an underspecified broader formulation. Preserve prior anonymous-candidate attribution and unrefereed status; the campaign supplies verification, not a newly discovered constant or theorem.
