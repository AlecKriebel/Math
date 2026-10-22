# Independent adversarial audit: Function Theory 6.83

## Verdict

**PASS for a five-attempt partial-results investigation. The unrestricted problem is not solved.**

No blocking mathematical defect was found in the frozen proof. The necessary Dirichlet-space condition is correctly credited to Overholt. The weighted Blaschke construction proves the stated sufficient condition, including the complete criterion inside a finite union of fixed Stolz regions. The two failed-converse examples have the limited consequences claimed for them.

The appropriate completion is an **unsolved investigation with five substantive attempts**, not a solved problem or a claim of new research priority. This audit does not establish that the full problem remains open in the current literature.

All seven authored input files retain their frozen hashes. The author verifier reproduces its saved output byte for byte. Independently implemented exact-rational controls also pass. No remote state was changed.

## Scope and evidence

The review covers `PROOF.md`, `README.md`, `SOURCE_GATE.md`, `RESEARCH_LOG.md`, `STATUS.json`, `verify.py`, and `verification.json` in `artifacts/`. The frozen author-manifest digest is:

`9dea14eb76f7e6044e1edc13b8a51675793df3e1bb08e759b69f06f68779d5e6`

The exact primary question and Update 6.83 were read in Hayman and Lingham, including the printed-page image. The complete three-page Overholt article was read in text and page images. The primary update identifies Overholt as a partial result, and reference [621] identifies the same 2000 article. These sources support the problem identification and historical credit:

- W. K. Hayman and E. F. Lingham, [Research Problems in Function Theory](https://arxiv.org/abs/1809.07200), Problem and Update 6.83, printed p. 146; bibliography entry [621]. Source PDF SHA-256: `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.
- M. Overholt, [Sets of Uniqueness for Univalent Functions](https://doi.org/10.4153/CMB-2000-016-x), Canadian Mathematical Bulletin 43 (2000), 105–107. Source PDF SHA-256: `92b4b79f9f5879b3e813c8450c77f3d09e85777f78d5d797eee8dba80854a49d`.

Overholt proves the reciprocal-difference reduction and reports additional existence consequences using earlier Dirichlet zero-set results. The present construction does not depend on independently re-proving those earlier results. Lappan's 1985 article is related prior work, not an invoked theorem dependency. Its full text was not reviewed here. Consequently neither this audit nor the note establishes novelty relative to Lappan.

This was a frozen-artifact audit. No new online literature or repository search was performed. The source gate's bounded search history is not upgraded into a proof of exhaustive prior-work coverage or present-day open status. No third-party source PDF or extracted source text is included in the audit deliverable.

## 1. Reciprocal differences and the necessary condition

**Accepted.** A normalized univalent function has precisely one zero, at the origin, and that zero is simple. The principal parts of its reciprocal and that of another normalized univalent function agree. Their difference is therefore holomorphic throughout the disk.

For the exterior map `F(ζ)=1/f(1/ζ)`, injectivity follows from injectivity of the component maps. Its restriction to a circle of radius greater than one is a smooth Jordan curve. The orientation in the displayed area calculation is correct: the exterior maps to the unbounded complementary component. The Fourier/Laurent calculation yields the asserted area formula; letting the radius decrease to one yields the area-theorem coefficient budget. Applying the elementary squared triangle inequality to the two coefficient sequences gives the bound 4 for the reciprocal difference.

The origin is handled correctly. The reciprocal difference need not vanish there. Multiplication by `z` preserves the Dirichlet space and provides a nonzero function vanishing on the entire prescribed set. No claim is made that this necessary-condition function has exactly the prescribed zeros. For an explicit check of the exception, `f=z` and `g=z/(1+cz)`, with `0<|c|<1`, have a nonzero constant reciprocal difference.

The coefficient budget 4 is consistent with a sharp algebraic control: `f=z/(1-z²)` and `g=z/(1+z²)` have reciprocal difference `-2z`. Both maps are injective because an equality at distinct points would force a product of two disk points to have modulus one.

The inclusion of the Dirichlet space in the Hardy space `H²`, followed by Jensen's formula, gives the distinct-point Blaschke condition. Removing a finite-order origin zero is legitimate. The note explicitly excludes enumeration multiplicity: repeating one coincidence point cannot create a uniqueness set. An interior accumulation point is independently handled by the identity theorem.

## 2. Bounded-derivative perturbations and finite interpolation

**Accepted.** A bounded derivative supplies a global Lipschitz bound on the disk because the straight segment between any two disk points remains in the disk. The lower estimate for the perturbation therefore proves global injectivity, rather than merely nonvanishing of the derivative.

The double zero of `H` ensures both normalization conditions. Integrating from zero also proves `|H(z)|≤M|z|`, hence boundedness of the constructed map. Nonzero `H` and nonzero perturbation parameter ensure the two functions are distinct. Their coincidence set is exactly the zero set of `H`.

The polynomial coefficient budget bounds the derivative everywhere in the disk. The finite construction has zeros only at the prescribed nonzero points and the mandatory origin. The origin has multiplicity two in the difference, as normalization requires; the question concerns points, so no prescribed multiplicity is lost. The empty prescribed nonzero set is also covered by `H=z²`.

## 3. Weighted Blaschke construction

**Accepted, including convergence and the exact zero set.** The weighted hypothesis dominates the usual Blaschke sum and excludes interior accumulation. The normalized factor identity gives a summable bound for `|1-b_a(z)|` on each compact subdisk. This proves locally uniform product convergence. At zero the product is the product of the positive radii; that product is positive because the radii have summable deficits and none is zero. Thus the limit is not identically zero.

There is also no hidden enlargement of the zero set. At any point different from the assigned zeros, the summable factor deviations make the product nonzero. At a prescribed zero, isolating its factor leaves a nonzero product, so that zero is simple. The factors `(1-conjugate(ζ)z)` have their zeros on the boundary, outside the open disk. Consequently the constructed difference has exactly the prescribed nonzero zeros and the origin, with multiplicity two at the origin.

For finite products, the product rule and `|b_a|≤1` give the derivative estimate term by term. Locally uniform convergence of holomorphic products implies convergence of their derivatives on smaller compact subsets. The comparison

`|1-conjugate(ζ)z| / |1-conjugate(a)z| ≤ 1 + |ζ-a|/(1-|a|)`

is valid throughout the disk by the triangle inequality and the denominator lower bound. Multiplication by the squared boundary factor controls the full limiting derivative by the weighted sum. The bound 12 on the derivative of `z²(1-conjugate(ζ)z)²` is correct. The chosen parameter makes the total perturbation derivative at most one half, so the global perturbation lemma applies.

For `m≥1` boundary points, differentiating the polynomial factor gives `(m+2)4^m`. Each derivative summand of the Blaschke product uses its assigned boundary factor, and the other `m-1` factors contribute at most `4^(m-1)`. This gives precisely the stated finite-union budget. Assignments need not be unique or optimized: one assignment with finite total weight suffices. Finite exceptional points add finite summands.

The radial example's constants are correct: the sum of `1-a_n²` is `5/3`, the weight is `20/3`, the derivative budget is `56/3`, and the proposed parameter `3/112` uses half that budget.

## 4. Stolz-region quantifiers

**Accepted with exactly the stated geometric restriction.** Each region has a fixed boundary vertex and a fixed finite comparison constant. Within a finite union of such regions, the weighted sum is at most a fixed multiple of the distinct-point Blaschke sum. Necessity holds for all pairs in the original univalent class; sufficiency constructs bounded members of that class. There is no mismatch between these directions.

This does not assert a Blaschke characterization for arbitrary sequences, infinitely many uncontrolled boundary vertices, or points merely tending to one boundary point. In particular, the result does not conflict with Overholt's reported Blaschke uniqueness examples tending to one boundary point: convergence to that point alone does not impose the fixed Stolz inequality. Divergence of the weighted series supplies no uniqueness conclusion, as the note correctly states.

## 5. Small Dirichlet reconstruction

**Accepted as a failed uniform reconstruction principle.** Direct differentiation yields the stated numerator `1-N^(1/4)z^(N+1)`. The denominator has no zero in the disk. The positive numerator root is strictly inside the disk, so the rational map fails the necessary local-injectivity condition. Both the uniform size of `h_N` and its Dirichlet energy tend to zero.

This is a counterexample to guaranteeing univalence from uniform smallness in these norms for the proposed reconstruction. It is not a counterexample to a Dirichlet zero-set characterization and does not exclude a different univalent realization. The note preserves that distinction. Indeed the functions in this control have only the origin as a zero, and that point set is easily realizable.

## 6. Finite interpolation and compactness

**Accepted.** The finite interpolation parameters give derivative budgets strictly below one and differences bounded uniformly by `2^(-N)`. The maps therefore remain distinct at each finite stage while converging to the identity. For the example accumulating at zero, the infinite coincidence condition would force equality by the identity theorem.

The proposed compact-separation reformulation is correct. A fixed distinct pair gives some compact disk and a positive separation. Conversely, compactness of the normalized univalent class provides a common convergent subsequence; the derivative normalization excludes a constant limit. Every fixed interpolation condition persists eventually along that subsequence. Uniform convergence on the selected compact disk preserves the positive lower bound on the maximum difference.

The reformulation still quantifies over univalent pairs. It is not an independent sequence criterion, and finite interpolation does not provide its uniform separation. The note makes both limitations explicit.

## Independent computation and reproducibility

`verify_independent.py` is a separate standard-library implementation with exact rational real and imaginary parts. It constructs finite Blaschke products as polynomial quotients and differentiates those quotients, rather than reusing the author's product-derivative implementation.

The saved result in `verification_independent.json` records:

- Seven frozen-file hashes checked before and after execution.
- The author verifier's output reproduced byte for byte.
- 2,988 individual complex-factor controls, including non-radial point-to-boundary assignments.
- 498 product evaluations covering one boundary point with four zeros and three boundary points with eight zeros.
- Exact normalization, prescribed-zero, denominator, multiplicity, derivative-budget, and perturbation-budget checks.
- Independent geometric-series constants and reciprocal-origin controls.
- Exact polynomial derivations and rational sign-change certificates for three small-Dirichlet critical-point examples.
- A control exhibiting failure of an unrestricted perturbation, plus finite-collapse budgets.

These are finite algebraic regression controls. The infinite-product argument, global injectivity, all-sequence quantifiers, and compactness reasoning are established by the analytic review above; they are not inferred from a grid.

To reproduce from the deliverable root, run:

```sh
python3 audit/verify_independent.py > audit/verification_independent.regenerated.json
cmp audit/verification_independent.json audit/verification_independent.regenerated.json
```

`AUDIT_MANIFEST.json` contains hashes for the authored snapshot and the audit outputs, excluding itself. No change to the frozen authored files is required by this review.

## Final classification

Five substantive approaches were actually developed: the necessary reciprocal reduction, finite bounded-derivative interpolation, infinite boundary-damped interpolation, a small-Dirichlet reconstruction obstruction, and a finite-to-infinite compactness obstruction with its exact separation gap. They are sufficiently distinct to support the stated five-attempt record.

**Required corrections: none. Blocking findings: none.**

The deliverable is suitable as a carefully scoped partial-results and failed-converse investigation. The missing unrestricted characterization remains explicitly missing. No proof of a new theorem's priority, complete literature coverage, or a present-day resolution status is supplied or implied.
