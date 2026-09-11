# Formalization status — continuation v0.2.0

**The full Lean proof is not complete. No Lean compiler ran.**

The project now contains **280 theorem declarations with proof attempts**, in
**4,038 source lines / 25 source files**, excluding the generated audit module.
The preceding checkpoint had 114 theorem attempts. **Zero** declarations in
either checkpoint have been kernel-checked in this environment.

## Material progress

The explicit separation branch now has an unconditional physical proof-source
path. An independently replayed rational operator sum-of-squares certificate
gives the stronger bound **289/10 = 28.9** for the paper's PVM functional. The
paper's witness is strictly larger, with margin greater than **1/50**. All three
auxiliary support pairs, scalar/degenerate observables, arbitrary complex density
matrices, and shared-randomness convexification are addressed in the source.
The kernel has not checked that source.

The one-input equality now has an unconditional source attempt using genuine
qubit PVM mixtures. The projective-fiber proof source covers the generic case,
all four exceptional divisors and their intersections through explicit inverse
maps. The rank-one obstruction, labelled rank-zero rigidity/simulation, and a
simpler high-rank uphill construction are also written at the algebraic level.

Executed checks and their individual scope boundaries are recorded in README.md
and in the JSON reports. In particular, the SOS positivity was replayed by both
rational LDL multiplication and an independent integer Bareiss determinant
calculation. None of the Python checks is Lean verification.

## Still missing

`UniversalTwoInputEquality` has no unconditional proof-source derivation yet.
The missing work includes compactness/extremal maximizer selection, the cone and
filtering reductions, actual Lorentz-incidence physical reconstruction and its
smoothness, POVM strong duality/strict multiplier positivity, and the derivative
and curve arguments connecting the algebraic rank cases to physical Bell maxima.
The final minimum-input theorem and `MainClaims` therefore remain conditional.
Appendix B's stronger physical attainment is also not formalized.

This is **not merely a finished proof waiting for a compiler**: both the compiler
check and those mathematical formalization obligations remain.

## First unfinished computation

```bash
cd bell_lean
bash scripts/check.sh --bootstrap
```

The saved invocation exited **127** at toolchain discovery, before any Lean build.
A usable pinned toolchain and dependencies are needed to obtain actual errors and
repair the source. Direct installation/download attempts failed, available
connector runtime archives were oversized or unsuitable, and GitHub rejected an
isolated branch-creation attempt with HTTP 403. No remote files were changed.

After a working build, the generated axiom audit must pass for every declaration.
Only then may the *written subset* be called kernel-checked. The open universal
statement still requires its own full proof, not an added axiom, a `sorry`, a
conditional theorem, or a finite test suite.

## Files to retain

- `Bell/`, `Bell.lean`, the pinned toolchain and dependency manifest.
- `certificates/binary_pair_sos.json` and `docs/SOS_CERTIFICATE.md`.
- `docs/RANK_TRICHOTOMY_SHORTCUTS.md`, `docs/COVERAGE.md`, `docs/BLUEPRINT.md`.
- All exact checkers and their JSON/log evidence, plus the source/axiom audit scripts.
- `reports/status.json`, `reports/continuation_progress.json`, and source provenance.

Every status flag distinguishes uncompiled source, executed exact algebra,
finite regressions, and kernel verification. No full-paper completion is claimed.
