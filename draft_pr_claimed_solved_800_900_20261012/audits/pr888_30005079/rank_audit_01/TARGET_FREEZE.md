# Target and attack-plan freeze

UTC: 2026-10-16 05:18:32. Audit completion estimate: 8%.
Pinned task: PR 888 / PID 30005079, candidate head a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7. This is validation of the original effort (1/5), not a new central search.

## Exact target
Native canonical_pair.json was read before candidate files or previous audit verdicts. Its exact clean claim is: “Construct an explicit nontrivial canonical degeneration of a Fano variety whose entropy-minimizing valuation is nondivisorial.”

The actual primary report was independently fetched from https://ems.press/content/serial-article-files/46955?nt=1 (DOI https://doi.org/10.4171/OWR/2022/17), SHA256 c997329409f016d06867ecc06dd38c59cea4919aa9ecf34791ed6a95f63345ec. The relevant contribution is Harold Blum, printed pp. 888–889, PDF pp. 28–29. The official discussion identifies the first, H-minimizing degeneration in the canonical two-step process. Its sought nontriviality is a change in variety X ≄ Z, beyond a nonzero field or a product degeneration. A suitable valuation must be the canonical H-minimizer, have finitely generated associated graded anticanonical ring, and produce the stated first degeneration. Nondivisoriality must concern that valuation on C(X), not merely a chosen higher-rank filtration or a soliton on an unrelated central fiber.

## Independent arithmetic/rank attack plan
Before inspecting the candidate, I will test: (i) the exact moment integral and its strict convexity, root existence and uniqueness, and rational endpoint sign certificates; (ii) whether the claimed irrationality is of a coordinate or the ratio needed for rational rank; (iii) the valuation value group on the function field rather than the section ring, its rational rank, residue transcendence degree, and divisorial obstruction; (iv) all coordinate, sign, scale and twisting changes; (v) the actual statements and hypotheses of primary transcendence/valuation results; and (vi) whether any algebraic arithmetic argument silently depends on numerics or on a possible transcendence conjecture.

Falsifiable failure conditions include an integration residual, a rational slope compatible with the equations, a lost degree direction on passing from the section ring to C(X), an irrational scalar multiple of a divisorial valuation mislabeled rank two, or a valuation that never induces the official nontrivial canonical degeneration. Geometric and global-minimizer verification are separate families; I will not consult their reports before the substantive analytic freeze.

No candidate file or older source audit has been opened before this freeze. No original source edits or publication/Git mutations are authorized in this family.
