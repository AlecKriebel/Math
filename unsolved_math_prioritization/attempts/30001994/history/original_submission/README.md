# 30001994: degenerate conductivity and the correction potential

**Complete first-turn counterexample candidate for the source's ordinary-potential map; independent review pending.**

`PROOF.md` gives a smooth compactly supported nonnegative conductivity and a smooth compactly supported divergence-free input A for which no H¹-local scalar potential satisfies div(σ(A+∇φ))=0. The conductor has Lipschitz boundary and connected exterior, and conductivity is positive almost everywhere inside it, but vanishes on a meridional cut. Weighted gradients can approximate cancellation of a circulation that no ordinary single-valued Sobolev gradient can cancel.

This excludes extension of the original Lemma3.1 gradient map and its W(curl) reconstruction to arbitrary nonnegative bounded conductivity. It does not exclude a weighted-completion projection, which the proof constructs, nor every generalized scalar distribution or alternative eddy-current formulation.

- `SOURCE_GATE.md`: exact PDE, function spaces, topology and later-source qualifications
- `PROOF.md`: full construction, strong weighted approximation, admissible distributional tests and dual contradiction
- `check_turn1.py`, `turn1_checks.json`:323 exact symbolic controls, replayed identically
- `source_manifest.json`: pinned primary reading inputs
- `REVIEW_REQUEST.md`: required adversarial checks

One of five substantive author turns has been used. If a source mismatch or mathematical gap remains after review, four turns remain. No historical novelty claim or final PR before independent review and publication authorization.
