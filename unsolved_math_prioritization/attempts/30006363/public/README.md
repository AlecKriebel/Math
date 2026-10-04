# Topological invariance of helicity

Problem 30006363 / OWR-14299512-001, catalogue rank 557.

**The general problem is unresolved by this investigation.**

This packet gives complete proofs of bi-Lipschitz invariance and an
isolated-zero boundary-growth criterion, plus explicit obstacles to naive
approximation arguments. It preserves the source's orientation, measure,
exactness, and time-conjugacy assumptions. Five approaches and their remaining
gaps are recorded; no original full-resolution or priority claim is made.

- PROOF.md: mathematical results, proofs, and explicit limits.
- SOURCE_GATE.md: exact scope, current sources, prior-attempt checks, and
  payload boundary.
- ATTEMPT_LOG.md: five substantive approaches and their outcomes.
- verify.py: 38 exact symbolic checks of the explicit examples.
- verification.json: deterministic results from those checks.
- requirements.txt: pinned symbolic-check dependency.
- SHA256SUMS: hashes of the frozen files other than the manifest itself.

## Reproduce

Use Python 3.11 or newer with SymPy 1.14.0 installed, then run from this
directory:

    python verify.py
    sha256sum --check SHA256SUMS

The script performs no network access and needs no source PDFs or corpus.
Exact arithmetic verifies the displayed curls, primitives, Jacobians,
helicities, indices, norm identity, and variation lower bound. Passing these
checks does not verify the general analytic proofs or settle the question.

The nonsingular theorem used as background is by Oliver Edtmair and Sobhan
Seyfaddini: https://arxiv.org/abs/2508.10609v1 .
