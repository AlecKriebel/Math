# Independent publication-package acceptance

**Verdict: ACCEPT FOR AUTHORIZED SCOPED PUBLICATION.** No blocking packaging, replay, scope, or disclosure finding. Row **1793**, catalog ID **20000200**, retains **scoped_resolved1/5**.

This review verifies the frozen publication package against the already accepted mathematical record. It does not consume an additional mathematical pass, claim a new theorem audit, or authorize any action beyond the existing publication scope. The frozen payload and accepted originals were not modified. No publication was performed.

## 1. Frozen identity and inventory

All three independently supplied SHA-256 anchors match:

- Public manifest: `a73a86ab48c4b3b69649967257fa690aa7d73cc2ac856aae1e84e5614fab99f0`
- Archive: `272dd219644410a00badaa71c2b715fe1bbfe3fed3816383d41224e047b83ad3`
- Separate freeze receipt: `83087911988d91b0580df5d6dab54f3e683da9dab548386cf688c3c88879556e`

The archive is 56,494 bytes. It contains exactly 30 regular files totaling 192,481 uncompressed bytes. Its contents match the frozen public directory byte for byte. Its inventory contains no duplicate paths, escaping paths, links, or other special members. The manifest binds the other 29 files; its separate digest supplies the external trust anchor. All 15 Markdown local links resolve.

The accepted original report remains bound by SHA-256 `856cf9b1560aeee8f26f1197f587e1d81838a8cb423c8c3f320be1aaa5c21ad5`. The accepted input-manifest and acceptance-receipt bindings also match their original bytes.

## 2. Complete-content preservation

All 27 original research files retain their pre-packaging hashes and byte counts. The 16 entries in the accepted pre-audit manifest and five audit-artifact entries were also checked against the original acceptance record.

Every complete file in the 15-artifact public edition map was compared with its accepted original:

- Nine artifacts are byte-identical, including all four executable checker sources and their four output receipts.
- Six documents contain exactly 15 disclosed presentation substitutions.
- Applying those substitutions to the complete accepted originals reproduces the public editions byte for byte. There are no additional edits or omitted sections.

The substitutions replace coordination references with document references, update cross-report descriptions, remove a source-storage reference, and clarify theoretical effectivity rather than implemented general software. The full proofs, displayed formulas, hypotheses, examples, degeneracy analysis, exact-image argument, and field-generation argument are preserved. The new contract and summary accurately carry the accepted scope and qualifications.

## 3. Independent clean replay and negative controls

Replay used an independently extracted archive in a fresh temporary directory, with the externally supplied manifest hash. All five caller modes passed:

- Normal Python
- `-O`
- `-OO`
- `PYTHONOPTIMIZE=1`
- `PYTHONOPTIMIZE=2`

Each mode reproduced the four output receipts byte for byte: **49 + 67 + 12 + 30 = 158 named checks**. The **108 rational homogeneous-slope comparisons** occur inside one aggregate named check. These are the same checks repeated across interpreter modes; neither slope comparisons nor repeated runs inflate the named-check count.

All **80 negative controls** were independently reproduced:

- **60 integrity controls:** twelve mutations or incorrect anchors, each in five modes. These cover changed proof bytes, a missing checker, changed output, an unexpected file, a symlink, an unsafe manifest path, a duplicate entry, incorrect disposition, incorrect target, incorrect accepted-report anchor, a scope expansion with refreshed file hash, and an incorrect external manifest anchor.
- **20 semantic controls:** one deliberately false algebraic identity in each of the four original checker sources, each in five modes. These were executed through the package's assertion-safe launcher with integrity bypassed only by the test harness. Every run failed with an actual `AssertionError` and `CHECKER_FAILED`, rather than a hash-only rejection.

The verifier contains no optimizable assertions. Each original checker runs in an isolated, nonoptimized child with explicit `compile(..., optimize=0)` and a deliberately failing assertion probe. The positive runs confirm that all four child guards remain active under every caller mode. Neither the clean extracted package nor the frozen public package changed during testing.

## 4. Scope, prior art, and disclosure

The public result consistently retains complex `SE(2,C)`, the fixed ordered pair `(κ², κ_s)`, every reduced integral one-dimensional target, smooth-projective normalization, and rational image-closure realization. Constant-`u` and identically zero-`v` targets are treated explicitly. Point signatures remain a boundary statement.

Uniform effectivity retains the exact coefficient model: an explicitly presented finite extension of `Q(T)`, a declared algebraically independent transcendence basis, exact input coefficients, and a chosen embedding in `C`. The theorem over `C` is distinguished from algorithmic input representation. Risch's classical two-good-reductions mechanism remains credited. The package makes no broad AIM, novelty, practical-complexity, or implemented general-decision-software claim.

Inspection of the complete inventory and readable contents found authored mathematical material and permitted public verification/source metadata. No copied source paper, source-text payload, dataset contents, private source, private coordination material, or private personal material is included. Scholarly source histories retain their retrieval failures and inspection limits. This packaging review did not freshly retrieve those scholarly sources or extend the priority search.

## 5. Queue change and publication boundary

The proposed queue was compared byte for byte with its supplied base. Exactly one line changes, for row 1793 / ID 20000200, and exactly three cells change: **Status**, **Turns**, and **Findings**. The new disposition is `scoped_resolved`, `1/5`. All unrelated bytes, including existing notes and chat links, are preserved. The new findings contain an authored scope summary and the public package link. The queue is not included in the portable archive.

The supplied base commit is `0e5b5cb9b69ed2088d181a02e222f99bec7535ff`; its queue Git-blob identity and both snapshot hashes were verified locally. This review did not recheck the live remote. Before publication, recheck the remote head and queue and preserve intervening unrelated changes.

Machine-readable evidence: [review receipt](REVIEW_RECEIPT.json) and [independent execution record](INDEPENDENT_REPLAY.json).
