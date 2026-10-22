# Modern K3 Problem 4.14 / catalog 2890: audited universal-cork partials

**Controlling disposition: unsolved, 5/5 substantive approaches. Limited pass only with the [controlling audit addendum](audit/CONTROLLING_ADDENDUM.md).**
No universal cork or obstruction to every candidate is established. There is no novelty, historical-priority, global-openness, formal-verification, or human-peer-review claim.

## Read the controlling correction first

The [controlling addendum](audit/CONTROLLING_ADDENDUM.md) supersedes the mathematical meaning of the extension-height definition in `author/PROOF.md`, Approach 4, line 120. Height is infinite exactly when **no qualifying extension exists**, not when one is unknown. For the analogous closed-pair stabilization distance, infinity likewise means the set of qualifying stabilization levels is empty. When existence is unknown, finiteness is unasserted. The addendum independently checks every downstream use and explains upward closure from an extension at a smaller level. No deduction uses lack of knowledge as evidence of nonexistence.

The ten files in `author/` and fourteen files in `audit/` remain byte-for-byte frozen. The original author fields describing an audit as pending are historical. This guide and `RELEASE_STATUS.json` record the later limited audit acceptance without rewriting either original packet. No new mathematical edit has been made during publication. Read the [full audit](audit/AUDIT.md), the addendum, and the [frozen proof](author/PROOF.md) together.

## Exact target and scope

The target is **modern K3 (2026) Problem 4.14**, not the 1997 problem with that number: one compact contractible smooth four-manifold and one fixed nonextendable boundary diffeomorphism, realizing all required closed simply connected exotic pairs by varying the embedding.

- The target permits arbitrary-order boundary maps. Ladu's inspected nonuniversality results are used only within their orientation-preserving involutive hypotheses.
- Orientation-sensitive deductions retain the oriented, orientation-preserving convention. The orientation-flexible variant and the source discrepancy concerning both orientations remain unresolved here.
- A fixed-exterior genus bound is not a bound uniform over varying embeddings of the same abstract cork.
- Complexity of a selected h-cobordism or a specified induced isometry is not the minimum over all h-cobordisms and endpoint identifications.
- Boundary-relative examples do not establish unbounded stabilization distance for closed simply connected pairs.
- Fixed-splitting double-coset classification does not classify arbitrary diffeomorphisms or varying embeddings. Finite-family constructions and varying powers do not supply one fixed cork/map for every pair.

The supported material consists of elementary complement and gluing facts, scoped necessary conditions, and conditional reductions. The five approaches explicitly identify their missing geometric statements. Credited Floer, cork-decomposition, and stable-extension results remain external inputs rather than newly proved foundations. Five approaches is not a certificate of five separate conversation turns. Research progress toward a complete target resolution is not quantitatively certified.

## Reproduce the packet

Run with Python 3.10+ and its standard library, from any working directory:

```sh
python3 -B /path/to/2890/verify_release.py
```

This checks the entire release inventory and hashes, author/audit manifests and checksum lists, and the exact immutable audit-to-author binding. It replays the 226,926 author checks, 22,339 independent checks (including 13 mathematical negative controls), and all six temporary-copy integrity mutations. Saved outputs must match byte for byte, and hashes are checked again after execution. Subprocesses explicitly remove Python optimization flags so the frozen assertion-based integrity checks remain active even if the wrapper is started with `-O`.

These finite diagnostics neither construct smooth manifolds nor calculate Floer invariants, establish geometric realizability, or prove the universal target. Source retrieval and scholarly inspection are documented historical checks and are not rerun by the verifier. Public corpus hashes are identified as reported metadata where they were not independently rehashed. An AI audit is not human peer review. Local replay is not GitHub CI; no checks is not a CI pass.

Immutable bindings:

- Author manifest: `579a41fb8e474f60df00a4ecfe5d40e221e885385d5b8ee12557a9d7d32bdc37`
- Audit manifest: `b4325adb6ec6d117e52c5b2f0f7a3aede535b0b717a1bc705536de6b9b71f32f`
- Controlling addendum: `d14b3c6f7489574c1ddd7d7a57fc99df625c8bdb4dbb9fe280642e6e5199b9e0`

Only authored proof/code/audits and public source/verification metadata are included. PDFs, source extracts, source images, dataset contents, and private coordination files are excluded. The queue edit changes only ID 2890's Status to `unsolved` and Turns to `5/5`. Findings, Chat, DOI, every other row, and the existing literal metadata-looking header are preserved. No queue regeneration, merge, release, DOI, or external outreach is part of this publication.
