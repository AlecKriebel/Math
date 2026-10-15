# Five-turn partial result: sigma–rho Poisson summation and L-functions

**Original target: unsolved after five substantive author turns. Frozen for independent partial-scope review.** No proof of the general Langlands continuation/functional-equation conjecture, no counterexample to an actual automorphic L-function, and no novelty claim.

## Exact formulation and strongest deductions

The original OWR39/2021 contribution, pp.2113–2115, states a weak existential pair of nontrivial k×-invariant functionals intertwined by the sigma–rho Fourier operator. It then expects an implication for the associated L-function. The published Jiang–Luo2023 paper gives a more informative restricted-theta refinement. This package does not substitute the refinement for the original premise without saying so.

The source data are a number field, split reductive group, finite-dimensional dual-group representation, cuspidal sigma, and assumed local transfers pi_v. The analytic arguments assume the uniform source Satake/growth bounds for pi and its dual, supplied by the cited theorem in the unitary-sigma setting. Global automorphy of pi is never assumed in the partial implications. The local Mellin exponent is s−1/2, with the source's Haar, additive character, basic-function and epsilon normalizations.

1. `TURN_1.md`: Genuine theta inversion for a two-finite-place test with nonzero local Mellin factors gives completed-L meromorphic continuation and the functional equation. The argument proves the necessary uniform large-norm theta decay, unfolds and cancels a finite nonzero meromorphic multiplier. Classical Tate/Godement–Jacquet/local ingredients are credited.
2. `TURN_2.md`: The bare two-functional identity can be manufactured by transporting a nonzero right-half-plane zeta evaluation through the invertible Fourier operator. Its power-law idele orbit does not identify it with theta. Domain and continuity are specified only for the algebraic restricted tensor product with explicit weighted-integral seminorms.
3. `TURN_3.md`: With **both** functionals explicitly equal to theta on the source's double-circle subspaces, Fourier-square and translation stability yield the genuine theta inversion needed in turn 1. The printed refinement's one-sided wording is not treated as an automatic proof of the second equality.
4. `TURN_4.md`: Requiring a self-dual single functional or coherent identities in both directions still allows nonzero symmetrized right-half-plane functionals when the necessary Fourier-square scalar kappa is 1. The kappa condition is explicit; no unproved central-character compatibility of general local transfer is silently imported. These functionals need not have theta normalization.
5. `TURN_5.md`: A **finite power-log defect of the actual averaged theta pair** for one nonzero-Mellin test suffices for the same continuation and functional equation. The proof calculates all boundary Mellin pole terms and their reversal signs. A finite-dimensional continuous translation module for the difference between the Poisson functionals and theta is a sufficient additional condition, but is not provided by the weak statement. The constructed weak functionals can fail that module condition; this does not imply failure of the arithmetic theta defect itself.

## Unresolved original step

Derive canonical theta normalization or adequate finite analytic boundary control from the source's actual weak conjectured functional identity and arithmetic hypotheses. The functional-transport constructions show a gap in that proof route; they are not formal countermodels satisfying every arithmetic hypothesis with a false L-function conclusion. The general target therefore remains unsolved5/5, despite complete conditional lemmas.

No higher-level conclusion about L-function pole locations, entire continuation, vertical-strip growth, all nonunitary twists, or automorphic global transfer is asserted. The finite pole list in turn5 concerns its test-function integral before division by local multipliers.

## Verification and review

`verify_exact.py`, using pre-existing SymPy1.14.0, passes552 exact symbolic controls of the lower Mellin derivative, reflected boundary signs, half shift, finite-dimensional Fourier covariance/square, Jordan translation modules and multiplier cancellation. These are algebra checks, not a computer verification of the analytic proofs or Langlands theory. Run `python verify_exact.py`; the receipt is deterministic.

Primary PDFs/text are kept outside the public packet in the sibling source cache. Their hashes and primary URLs are in `source_manifest.json`. `FROZEN_MANIFEST.json` binds the exact public inputs for separate review. Historical source-only and earlier-turn status sentences are preserved as chronological records; this overview and metadata give the current five-turn disposition.
