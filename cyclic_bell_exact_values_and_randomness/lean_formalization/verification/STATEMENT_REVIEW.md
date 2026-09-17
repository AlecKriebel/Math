# Manuscript correspondence review

The bundled manuscript is the merged v1.1 dated 9 August 2026. Its exact source and PDF are identified in [reference/manuscript.json](../reference/manuscript.json). The result-by-result mapping is in [COVERAGE.md](../COVERAGE.md) and the [claim ledger](../reference/paper_claim_ledger.json).

The correspondence assessment was AI-assisted and included separate adversarial passes over definitions, source conventions, model assumptions, and theorem conclusions. It is not external human peer review. Lean verifies the encoded propositions; reviewers must still assess their relationship to the manuscript.

Particular review targets included the literal source coefficients and Bob transpose, roots-of-unity phases, physically normalized attaining strategies, arbitrary-Hilbert-space bounds, finite-input correlation model inclusions, permutation counterexamples, support rigidity, and the distinction between observed-table entropy and adversarial guessing.

The exact boundaries remain:

- The general polar identity accepts specified polar-decomposition properties; it does not construct arbitrary polar decompositions or strong limits in von Neumann algebras.
- The MUB obstruction uses a stronger constant-diagonal positivity argument instead of separately formalizing the manuscript's Toeplitz/SVD intermediates.
- Privacy and guessing statements retain their stated Eve/model assumptions. Lower bounds on adversarial guessing are not claims of exact worst-case optimizers.
- Cited external self-testing and isometry-transport results, novelty, priority, and open problems are outside the formalized claims.

The first reviewer release cleaned comments and tooling without changing mathematical code. Revision 2 adds explicit proofs for the full second-family first-harmonic matrix and local moments, Bob-adjoint/outcome convention transport with its transported functional, and all second-family residual annihilations. Existing physical definitions and main proof modules are retained; the source comparison records the precise additions and interface changes. The prior AI-assisted review identified these statement omissions, rather than an incorrect principal endpoint. Follow [REVIEWER_GUIDE.md](../REVIEWER_GUIDE.md) to inspect the formal statements directly.
