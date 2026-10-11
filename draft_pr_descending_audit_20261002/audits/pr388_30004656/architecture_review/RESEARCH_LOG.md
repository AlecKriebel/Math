# PR 388 independent architecture audit log

All work in this directory is by an independent adversarial reviewer. The frozen candidate is not edited. This audit concerns Turns 4–5 and the required additive chaining clarification; it does not certify resolution or priority of the original unrestricted problem.

## 2026-10-02 17:40 PDT (2026-10-03 00:40 UTC) — 60% complete

Reconstructed both analytic mechanisms before consulting the existing review. Turn 4 needs full row rank to realize every activation cone, positive homogeneity and an empty pattern to compare sphere and global norms, and a deterministic-base centered-label chaining event. Turn 5 needs label-balanced selection, exact trace cancellation, antipodal separation and spectral spread, and two scalar concentration arguments.

No central mathematical defect has emerged. The additive clarification is essential: the chaining base point must be fixed before the sample, even though the empty-pattern point in the deterministic energy argument may depend on the network. Remaining work: independent exact/numerical controls, parity and limiting-case attacks, compare with the existing review only after preserving the independent derivation, and write final disposition with the exact scope.

## 2026-10-02 17:46 PDT (2026-10-03 00:46 UTC) — 100% complete

Independent analytic reconstruction is preserved in `INDEPENDENT_DERIVATION.md`; its SHA-256 before consulting prior review was ea04438e875528449e07e4ec389907c199ed4970edfb645a4122f2e62f57b431. Then compared with the existing adversarial review and author controls. There was agreement on the required deterministic-base correction, moment symmetrization, norm domains and rank split; no new defect emerged.

New implementation `independent_controls.py` imports no author or prior-review code and passes 168,007 exact assertions. It includes all qualifying label counts for n=16 through600 (both parities), near-dependent full-rank orthants, non-diagonal 2D quadratics, large eigenvalue shifts, both Bernstein regimes and activation-core boundaries. Deliberate dependent-row and radial-constant negative controls succeed as counterexamples to broader claims. Receipt saved in `CONTROLS_RECEIPT.json`.

Final verdict: PASS for both restricted architecture theorems with `ADDITIVE_CHAINING_CLARIFICATION.md` attached. No further repair is needed in the audited statements. Neither their combination nor this review resolves the original arbitrary-activation/parameter conjecture. No priority certificate, merge or publication action was performed by this reviewer.
