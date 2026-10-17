# PASS2 concentration-audit receipt

14 October 2026. Problem row 1778 /30005770. This is the completed independent concentration audit within the shared second pass. It makes no priority or novelty claim.

## Overall disposition

The universal exact-uniform weak diagonal-permuton target remains unresolved in the audited lanes. The uniform 1324 anti-diagonal case, equivalent by complement to the target alpha=312 / forbidden 4231 case, also remains unresolved here.

The accepted results sharpen both the available reductions and the precise missing steps. They do not turn an exponential-rate obstruction into a weak-limit counterexample, or an abstract numerical tree into an avoidance-class counterexample.

## Accepted statements

1. **Fixed canonical staircase prefixes in uniform 1324.** For each fixed K and epsilon>0, the first K canonical greedy cells have total size at least epsilon n only exponentially rarely. The constants may depend on K and epsilon. The exact law, arbitrary-deletion reconstruction factors, uniformity over the deletion sizes and induction are valid. The canonical at-most-K-cell subclass has a strict growth gap. This does not cover arbitrary K-cell griddings or a largest cell whose index escapes with n.

2. **Repaired abstract completion-bound obstruction.** The six-A4-prologue tree satisfies every stated scalar numerical input, including the all-size binomial completion upper bound, Catalan lower bound, finite growth and supermultiplicativity. Exact uniform leaves have a linear marked A-spine, and the proposed averaged completion-weighted frontier criterion fails. The all-size proof is accepted, including Jacobi positivity/log-convexity, small-depth cases, convolution bounds and the marked simple-pole law. Its counts exclude every principal avoidance class. This refutes only the proposed implication from those numerical inputs.

3. **Actual first-hit-prefix state reduction.** The full minimum-insertion continuation tree is determined by the standardized prefix through the first alpha occurrence, retaining the entire permutation and an absent flag when there is no occurrence. The frozen suffix can be discarded exactly. The scalar label, even supplemented by a present/absent flag, does not determine completions; explicit containing states already have different depth-two counts for alpha=132 and alpha=312.

4. **Exact 1324 directed transfer and two-sided bias.** The accepted canonical encoding gives exact weights z^|A| ell_A h_A for a distinguished cell and the correct full-class normalization. All path sums converge for real 0<z<rho. The increasing-to-decreasing kernel formula is correct, and ell_(J_m)(z) grows exponentially in m at every fixed positive subcritical z. A uniform all-state subexponential incoming-weight bound is therefore false in the actual class.

5. **Conditional squared-kernel route.** If beta=limsup_n(sum_(|A|+|C|=n)K(A,C)^2)^(1/n) is strictly smaller than the actual class growth lambda, then the largest canonical cell has exponential tails at every fixed positive linear scale. The non-self-adjoint compact-truncation argument proves strict subcritical spectral radius, and the strict Hilbert–Schmidt margin provides exponential smoothing of both path vectors. The beta<lambda hypothesis is wholly unproved. Finite squared-kernel coefficients do not establish it.

## Rejected or unproved extrapolations

- Boundary-frontier tails do not imply weighted middle-ancestor tails merely from the accepted scalar numerical bounds.
- Exact state reduction does not establish a finite-state or positive-recurrent transfer process.
- Fixed K prefix estimates do not imply maxcell=o(n); a moving-index bottleneck remains.
- An induced cell or deletion residual is not uniform without its completion weights.
- First-cell weights cannot replace arbitrary-cell weights by dropping ell_A.
- Exponentially large incoming bias does not prove significant probability of a macroscopic cell.
- Ordinary domino counts, finite coefficient ratios, or nonsymmetric kernel formulas do not establish the required strict squared-kernel gap.
- Weak permuton concentration is not total-variation convergence or maximum-displacement concentration. The previously accepted inversion-to-weak equivalence and exact-law caveats continue to apply.

## Detailed acceptance reports and pins

- `FIXED_STAIRCASE_ACCEPTANCE.md`: 8078 bytes, SHA-256 `0c9d6c9966913b6abe8b090bd0cead610c90364cae3e911c647db19ffb78bf5c`.
- `COMPLETION_COUNTERMODEL_ACCEPTANCE.md`: 9355 bytes, SHA-256 `93ca2f6c4b4172e46671e27c3bc089e43014299a6cb24293fd6101fdc5e26304`.
- `TRANSFER_ANALYTIC_ACCEPTANCE.md`: 13018 bytes, SHA-256 `46d78f751706a082a32b171cb39c5a4ea10f49ae33be4a1fffef407533eadeac`.
- `FINAL_CHECKER_RECEIPT.json`: 3095 bytes, SHA-256 `a6968cc57edafd7109683196a93cb8ca3165ea249699139133b0a5eecb09ca9b`.

Those reports pin the exact reviewed proofs and explain the all-size mathematical checks. The transfer report also records direct inspection of the primary spectral inputs and the complementary structural acceptance.

The reviewer-authored preliminary `COARSE_TREE_COUNTERMODEL.md` is 7348 bytes, SHA-256 `35ac9aef233a2b29a752f5f393fe4c01c5084efdc240b2e0c54563e21c453cc5`. Its narrower scope and explicit 51>50 failure of the avoidance-style upper completion bound remain visible. It was independently accepted in `pass2_bijection_audit/COARSE_COUNTERMODEL_ACCEPTANCE.md`, SHA-256 `8ced82bcfc74038f9ca17321bdca2908437d304396430f0fb03bdf7d5c0ef618`. The separately authored repaired model strengthens the numerical obstruction without altering that preliminary artifact.

## Finite checks and preservation

The supplied repaired-model normal/-O/-OO reports have identical mathematical records and match the frozen proof and checker hashes. They contain 4960 A recurrences, 10287 completion-bound checks within labels<=64 and depths<=80, 861 weighted-ancestor identities, independent Jacobi multiplication and marked-spine calculations through size 400.

The prefix-state normal/-O/-OO reports also match: 32 alpha classes, 3498 present-prefix checks, 4460 absent flags and two scalar-state counterexample pairs, all at the explicitly bounded parent sizes and continuation depth 2. The transfer normal/-O/-OO reports are byte-identical and compare normalized canonical state-chain distributions through size 8. These reports were inspected and compared; this receipt does not pretend that the audit independently reran the author's programs. The complementary geometry reviewer supplied separate kernel regressions.

All finite checks are regression evidence, not asymptotic proofs. The full proofs were audited separately.

The earlier main audit and bulk appendix acceptance were preserved byte-for-byte. Their SHA-256 values remain `0b1aaed351f9df13aa0f2e9f2ba41df131cef3cfeb82fe111bf189a3e57c7e0d` and `4f92efae50122b5b217361efb696f81825682c4b85c2dd005973a602a2fc5799`. The accepted PASS1 bulk appendix remains `a877146631fe0f5552de95a9dd599d468cc77076a594caa1e8b09ebbb24b96f8`.

Source copies and inspection extracts are excluded from the authored deliverable manifest.
