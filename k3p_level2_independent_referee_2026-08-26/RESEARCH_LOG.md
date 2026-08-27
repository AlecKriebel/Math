# Independent referee log: K3P level-2 identifiability

## 2026-08-26 — Intake checkpoint

- Scope: independent referee assessment under the supplied neutral referee prompt.
- Safety boundary: no external communication; all executable review work will occur in `package_copy`, an isolated copy of the supplied package.
- Initial state: source repository is on `main`; unrelated pre-existing changes were observed and will not be touched.
- Evidence status: referee prompt read; package inventoried; article and reader-supplement PDFs copied, text-extracted, and rendered for complete primary-source review.
- Completion estimate: 3%.

## 2026-08-26T16:58:00-07:00 — Primary-source and integrity checkpoint

- Read the 33-page article and 12-page reader supplement completely before relying on generated reports. Rendered and visually inspected all 45 pages; no material layout defect found.
- Restated the principal-domain, strict continuous-time, generic-identifiability, exact-reconstruction, ordinary-triangle, no-proper-containment, outer-obstruction, and weak-class sharpness claims with their quantifiers and exclusions.
- Inspected the top-level integrity checker before execution. The pre-environment integrity run passed: 574 outer payload files (153,326,366 bytes) and 548 proof-core members (152,714,245 bytes), both bound to source commit `983086779dab08f6a0d76d0a10c614b7cee4affe`.
- Created an offline Python 3.14.6 environment by copying the project-local environment into the isolated package. Exact installed versions: mpmath 1.3.0, networkx 3.5, numpy 2.5.2, sympy 1.14.0.
- Completion estimate: 22%.

## 2026-08-26T18:03:00-07:00 — Independent proof/code checkpoint

- Independent handwritten audit found a load-bearing but apparently repairable omitted case: equality of bridge split sets does not distinguish an ordinary trivalent component from a three-boundary cycle/sunlet, while the global proof immediately invokes a theorem restricted to cycle/theta factors. The article's own strict tree--sunlet six-circuit separator appears to supply the missing repair.
- Static code audit found that no active command regenerates or independently classifies the full 405,216 four-port relation universe (or the 27,834 post-topology cases). Active exact checks begin with the frozen 40-survivor/14-orbit lock. This remains load-bearing for exhaustiveness.
- Static code audit also found that the advertised independent probe verifier checks hashes, row structure, and stored metadata but does not reconstruct graph transports/restrictions or the row-specific quartet/tree--sunlet semantics. A coherently self-hashed semantically invalid transport was accepted by its validation function. The hour-scale producer is therefore still load-bearing for the meaning of the 574,535 probe rows.
- Representative independent exact checks support the inverse-Fourier domains, CT inclusion, tree--sunlet pullbacks, H14 pullbacks/rank/smoothness/irreducibility, bridge anchors and gluing bounds, six representative four-port separator/rank cases, Krawczyk inclusion/ranks/margins, and the cherry inverse. These are spot checks, not universe completeness proofs.
- Completion estimate: 55%.

## 2026-08-26T18:08:46-07:00 — Fresh replay checkpoint

- Added an external macOS sandbox profile: reads and local subprocesses allowed, writes confined to `package_copy`, network denied. Used an empty caller environment with no credentials. A local `mktemp` shim rewrites BSD `mktemp -t` into the runner's phase-local `TMPDIR`; this was needed because macOS ignores `TMPDIR` for that invocation.
- Preserved two failed harness attempts. Session `20260827T005735Z` reached the clean-room checks and then failed because BSD `mktemp -t` attempted a denied write under `/var/folders`. Session `20260827T005931Z` completed the ten-child integrated replay in 190.80 seconds but the outer runner rejected sandbox-degraded `platform.platform()` metadata. Allowing writes to `/dev/null` restored the canonical platform probe without broadening filesystem or network access.
- Clean session `review_runs/20260827T010421Z` passed all four requested verification commands: release-input bindings, artifact bindings, the ten-child integrated fresh replay, and active classification mutations. Total 193.749 seconds; declared workspace drift was empty. Report SHA-256 `da448cca65c7787d48a7e537ea707d6f032b019434a7c1688ba062833c5b4afa`; transcript SHA-256 `04404b9c5959c2fbb33db33b13d7757686a958125ff48e764418818125b83db2`.
- Started the required 44-command portable producer/verifier regeneration exactly once. No duplicate probe process will be launched.
- Completion estimate: 68%.
