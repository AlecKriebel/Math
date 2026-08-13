# Status

## 2026-08-12: theorem complete; exact-byte audits strict pass

The T3-2 theorem is complete at its stated scope. For every finite weakly
reversible stochastic mass-action network of molecularity at most two, with
at most three species and at most two linkage classes, the minimal CTMC is
nonexplosive and every closed irreducible population class is positive
recurrent for every positive rate vector.

This is a mathematical proof with reproducible finite identities and
independent adversarial audits. It is not a claim of formal verification or
external peer review.

## Final proof chain

| Gate | Result | Frozen target / audit |
| --- | --- | --- |
| Fixed-class projection and 0/1/2-linkage routing | Strict pass | `781d2520…` / `bbc47342…` |
| Exact 46,872-pair two-linkage union | Strict pass | `dae2a58f…` / `a4f50dcb…` |
| Completed mixed orbit | 27,462 pairs | `a91e8c31…` / `32eec768…` |
| Active-invariant orbit gap | 432 pairs | `7edab78d…` / `1110efc0…` |
| Strictly positive invariant | 146 pairs | finite-class branch in final union |
| Level-set residual | 336 pairs | `6e9ddcac…` / `35b18c36…` |
| Outside-mixed remainder | 18,496 pairs | `e7b08be8…` / `192dfc3d…` |
| No-failure outside-mixed branch | 11,842 pairs | `b26742cf…` / `685206db…` |
| Failure outside-mixed branch | 6,654 pairs | `69521a82…` / `3685c749…` |

The exact finite certificate proves the pairwise-disjoint identity

\[
46{,}872=27{,}462+432+146+336+18{,}496.
\]

No potential is switched between these five branches along a stochastic
trajectory: a physical network has one fixed ordered support pair, so the
identity classifies completed theorems rather than path regions.

## Independent replay

- Global theorem SHA-256:
  `781d2520cbb3ad30e1749814f620d49d4c503c5c341ccd1add39a5fec31e2b7f`
- Global canonical audit SHA-256:
  `bbc47342d8d7b3cacf4b34d2ce2b5bd122798f41838787e8edafa4c70c859560`
- Global independent audit SHA-256:
  `109a7226a6b0bbf6aa2b314a3b2e1a4e6c247663312cfe59061c6bb076d2065a`
- Final two-linkage theorem SHA-256:
  `dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde`
- Final union certificate/test SHA-256:
  `5b249ded4b54801f7eb5ab9ced943ed566216e1228c0e07f3e205b1eef319288` /
  `dd51ce074aa43bb4722d176ef4c85face956c924150681d5cae32f3b615c5e76`

The isolated verifier passes all 418 tests without mutating its declared
scope. The publication build verifies all 40 authenticated proof-note inputs.

## Publication state

The 7-page main article and 189-page proof supplement rebuild without TeX
warnings and have received full contact-sheet plus high-resolution page
inspection. The mathematics package is release-ready. Author, license, and
submission metadata remain deliberate human choices and are not supplied.

Historical notes retain withdrawn proof attempts and local obstructions for
auditability. Any historical statement that the global theorem is open is
superseded by this status and the frozen final theorems above.
