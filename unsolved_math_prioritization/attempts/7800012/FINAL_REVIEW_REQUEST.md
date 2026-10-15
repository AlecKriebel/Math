# Full independent source/proof review request

Target7800012 / AMR-077-0012. Proposed disposition: original unresolved,5/5. Please audit all five proofs and the exact finite versus thermodynamic scope, not only the scalar check totals. No source-level solution or counterexample is claimed.

## Source and domain

Read the complete original_lieb.html, including its technical TeX. Its legacy PDF link returns404; the HTML contains the full finite-matrix question. Read Lieb1994 for half-filled scope and Lieb–Loss1992 SectionII for the all-circuit gauge statement, with the introductory uniform-field history. The source's local-plaquette wording needs the two torus loop holonomies retained; a correction of this auxiliary wording is not itself a resolution.

The public SOURCE_MANIFEST.json binds these three raw source inputs, which are not uploaded. Finite square tori in the proofs have even L>=4; moment arguments require L>=8; uniform four-band formulas require L divisible by4; the exact Hessian theorem is only for L=8. The thermodynamic theorem allows arbitrary phases and even side lengths, with the canonical particle count exactly L²/4.

## Audit-sensitive proof points

- Turn1: spanning-tree reconstruction and total flux compatibility; correct loop phases; orientation in the projection minimization; Gaussian-integer4x4 polynomial certificate and its spectral multiplicities; unique length3 walk restriction L>=8.
- Turn2: closed-walk coefficients232/144/24, no noncontractible length6 walks; exact sum-of-squares identity; norm/singular-value conversion and constants; polynomial-defect sharpness does not identify an energy optimizer.
- Turn3: full characteristic polynomial, number of occupied fibers and uniform band gap; complete Chebyshev divided-difference monotonicity including endpoint multiplicities; derivative signs; both loop twists; rigorous continuum error and concavity enclosure.
- Turn4: exact spectral projection polynomials, Hessian sign/factor/denominators, full128 by128 construction, translation/gauge checks, completeness of the Fourier positivity reduction and every radical interval; local gauge slice and absence of any global inference.
- Turn5: fixed-rank boundary perturbation constant; trial-projection tiling with exact leftover rank; limit/infimum quantifiers; all-rank redistribution and two-point convexification; lower cut count2L²/l; scope of finite-to-bulk counterexample criteria.

## Reproduction

Run `python REPLAY_ALL.py` or `python REPLAY_ALL.py --sources PATH`. Standard-library Python only. The five TURN_n_CHECKS.json files must replay byte-for-byte. verify_turn4.py regenerates and compares the entire TURN_4_CERTIFICATE.json, which is an exact algebraic certificate, not rounded numerical output. The author manifest binds all immutable files.

A successful review should be a scoped PASS only, leaving the original unsolved5/5 unless a genuinely valid unrestricted implication is found. No sixth author search is authorized; subsequent corrections should be additive and clearly separated from the freeze.
