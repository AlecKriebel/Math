# Independent full review request: 10400139

Review the unchanged manifest-bound author packet. Proposed status is **already_solved, 1/5**, credited to Kashaev, Murakami–Murakami and Baseilhac–Benedetti. No PR before the parent's publication gate.

Please attack all of the following, not merely the finite receipts:

1. The exact original source: Ohtsuki printed pp.485–487, nonempty links in oriented S³, odd N>1, Borel trivial bundle, and the Nth power of the original state sum. Does binding the literal normalization to reference[43] rather than silently correcting it accurately answer Problem7.24?
2. The face-gauge comparison: both CG scalar normalizations, direction of the 6j basis-change factor, the additional (x_pq/x_qr)^m face coboundary, negative-orientation inverse factor, and the ac/2 phase conventions. Verify that the remaining phase is independent of all states and only an Nth root. Arbitrary square-root basis signs must cancel.
3. Global cancellation on an arbitrary globally ordered closed triangulation, not just the boundary-of-simplex control. The link Hamiltonian condition and full unipotent coboundary are admissible, and all relevant parameters are nonsingular.
4. Orientation and signs: the2001 index−1 versus2002 index+1 labels, Kashaev's right tetrahedron, face indices, negated vertex cochain, and the2011 convention/mirror. A hidden mirror or surviving sign would be a mandatory correction.
5. The factor N^(−2N). Compare2001 equation(2),2002 long equation(7), Kashaev1994 equation(4.4) and1995 paragraph following(4.19),2011 equation(30)/normalization remark. Challenge the old unknot value. The short2002 survey's printed positive edge exponent is explicitly recorded as inconsistent, not used as a definition.
6. The exact scope of the published all-link theorems: Kashaev1995 Theorem1, Murakami–Murakami Theorem4.9, and2011 root-only Corollary4.6. Do not infer a root-only assertion from the2011 generic =_N notation, which includes a sign. Distinguish the later general H_N from the original Borel/Kashaev sum.
7. Split-link zeros, arbitrary component orientations, ambient-isotopy enhancement, the exclusion of empty links/even N, and separation from the unresolved adjacent phase/asymptotic questions.
8. Replay the three checkers and build independent controls if useful. `verify.py` gives412,133 exact bookkeeping/factor checks and30,67590-digit diagnostics; `gauge_check.py` independently evaluates the finite-rho CG formulas in2,925 diagnostics; `unknot_check.py` directly sums59,049 states for the old N=3 unknot. Numeric receipts are explicitly non-interval; none substitutes for the all-N proof or the published all-link theorem.

All nine complete PDFs and relevant rendered pages are in the worktree's `sources/`, outside the public attempt packet; hashes/URLs are in source_manifest.json. SOURCE.md is named SOURCES.md. Author files remain frozen. Report a flaw immediately before writing a review; do not patch the frozen mathematics.
