# Full five-turn independent review request: ID159

Audit the complete frozen packet against the exact finite, independent, integer-valued, arbitrary-support convolution problem. Original status: unresolved 5/5. No full resolution or novelty claim is requested. Do not undertake a sixth author search.

## Source inputs

The original statement is Green's current Problem 28, printed p16, with full comments and source link read and visually checked. The complete imported ID159/GREEN-071 record is an alias, not a distinct problem. SOURCE_MANIFEST.json pins the five local PDFs and reading scopes: Green, Ghidelli 2209.09843, Hare 2307.07363, Dvorsky 2608.19173v2 and Nguyen Xuan/Pham/Pham Lan 2609.09215v1. SOURCE_ADDITION_TURN_3.json pins the explicit classical palindromic proof presentation used for the localized reflection criterion. No external code or Lean project was installed or run.

The exact residual system in Turn 4 is from David Zhang's primary MathOverflow answer linked in SOURCE_MANIFEST.json. Only its displayed system is used for our small certificate. The reported degree-66 computation was not replayed. Dvorsky's finite companion manuscript was not retrieved. Long analytic proofs and quantitative epsilon-unfair estimates are not independently certified by this author packet. The negative coefficient in the epsilon-unfair statement is explicit and essential.

## Main adversarial obligations

- Verify leading normalization and the separate deduction of both constant coefficients being 1. Preserve monicity, nonnegativity, finite support and arbitrary real weights; do not replace arbitrary support by an interval.
- Check algebraic integrality, rational-factor rigidity, common coefficient fields and the first fractional index from both ends. The conjugate-positivity condition must not be assumed from one positive embedding.
- Check exact supports versus possible zero coefficients in the unique-sum obstruction and the residue-class trinomial proof. The exhaustive degree box is m,n≤8, not all total degree 16 and certainly not arbitrary degree.
- Verify the outer-reflection induction uses only c_k=c_(m+n−k) through floor(m/2), with all indices valid, and that it forces the *smaller* factor palindromic and Boolean. The larger factor is Boolean but need not be palindromic without full product symmetry. Check both failed symmetrizations.
- Reconstruct the residual support U={0,1,3,7}, V={0,1,2,3,5,9,11,13}; its forced unit at degree 11 is necessary. Check the seven coefficient equations and exact polynomial identity, including strict-positive support assumptions and all-scale extension.
- Check the finite root-multiplicity enumeration, algebraic decidability scope, compact coefficient cube, possibly empty zero set, and all compactness quantifiers. No uniform delta, bound on degree or termination of the universal verification is claimed.
- Check that the formal-power-series example and negative epsilon-unfair factors are not represented as finite nonnegative counterexamples or probability laws uniform on infinite supports.

## Replay and integrity

Run python verify_turn1.py through python verify_turn5.py from the packet directory and compare stdout byte-exactly with TURN_n_CHECKS.json. No author checker imports another. Reconstruct separate controls for the strongest claims, especially the reflection step and degree-20 certificate. Verify all historical TURN_n_MANIFEST.json files and FINAL_FROZEN_MANIFEST.json. Source PDFs and imported raw records are local audit inputs, excluded from public artifact hashes except their recorded source hashes.

Give a scoped PASS or FAIL with required corrections and explicit source/dependency limitations. Preserve all author bytes. The correct final outcome remains unsolved 5/5 unless a valid full-scope implication was actually proved within the frozen packet.
