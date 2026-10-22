# Final acceptance of the movable invariant enlargement reader

Problem 30003527 / OWR-15575-006 / queue row 1767. Reviewed 13 October 2026.

## Verdict and exact accepted edition

**ACCEPTED as a complete, scope-correct public mathematical reader after two packaging corrections.** This is an independent AI audit of the reader's transformation, completeness, provenance, version control, citations, and integrity behavior. It is not a new mathematical search pass, a fresh proof of all imported theorems, human peer review, or formal verification.

The accepted edition contains **38 regular files totaling 405,801 bytes**. Its `MANIFEST.json` is **6,371 bytes**, with SHA-256:

`3c6129f6e2cb82f78559103311f2d445abd368d40f9534e840048f22e9f208bf`

The manifest inventories the other **37 files, totaling 399,430 bytes**, and excludes its own bytes. There are **16 proof artifacts, 11 mathematical acceptance reports, one mathematical correction patch, and ten presentation, metadata, and integrity files including the manifest**. All 84 local Markdown links resolve to files inside the reader.

The complete original problem remains **UNSOLVED by this investigation** after exactly five new shared substantive passes. The continuation's search budget is exhausted; the lifetime substantive count is unknown. This reader review and its packaging corrections do not change that accounting.

The acceptance is specific to this pinned edition. This report is a separate companion artifact, outside the 38-file reader inventory. Adding a copy of this report inside the reader would require a new manifest and would no longer be the exact edition pinned above.

## Corrections required by this reader audit

The initial 38-file submission totaled 405,360 bytes and had manifest SHA-256 `a9454d0cfe221358433da4a6c195f3a9c7826ea190b451cd55e0f1e7e75651af`. It was preserved unchanged. It was not approved for publication unchanged, for two packaging reasons:

1. Its public verifier contained internal-only vocabulary in an exclusion filter. Those vocabulary checks were moved to separate private QA; the public program retains ordinary file and path integrity checks. The exact removed vocabulary and original diff are not reproduced here.
2. An unexpected FIFO filesystem entry was ignored by the original inventory scan. The corrected scan rejects nonregular entries in addition to symlinks and unexpected regular files. The FIFO case now fails in ordinary, `-O`, and `-OO` execution.

Only `verify_reader.py`, `INTEGRITY.md`, and the corresponding manifest entries changed. The other 35 files are byte-for-byte identical to the original submission. No mathematical argument, mathematical audit, source-credit statement, source identity, provenance record, disposition, or correction patch changed.

The revised integrity instructions also distinguish selected metadata checks from a complete semantic audit, document `-OO`, and state the trusted-verifier and stable-filesystem assumptions. No inventory, symlink, or path-traversal safeguard was removed.

Final changed-file identities:

| File | Bytes | SHA-256 |
|---|---:|---|
| `verify_reader.py` | 9,480 | `953f50c9a635bf2bb17f7587cb72916f18ad9c68d8fe4efb28455b8993244858` |
| `INTEGRITY.md` | 3,360 | `0d64b92c5c420baa64a751212e97ab8fcc7bf5a92ee2f1a4222d1ee1358f6917` |
| `MANIFEST.json` | 6,371 | `3c6129f6e2cb82f78559103311f2d445abd368d40f9534e840048f22e9f208bf` |

## Exact question and mathematical scope

The reader correctly asks whether every compact invariant set A of every continuous full flow on R³ has, inside every prescribed open neighborhood U, a compact invariant movable B with A⊆B⊆U. It permits B=A and disconnected B. It imposes no isolation, smoothness, nonsingularity, stability, minimality, finite-component, or dimension-one hypothesis on the original problem. Its movability definition chooses V before the later target neighborhood W, and requires an actual neighborhood homotopy.

The principal accepted restricted result remains:

> An isolated invariant compactum of a continuous full flow on R³ is movable when it has finitely many connected components and covering dimension at most one. A finite-rank hypothesis on first Čech cohomology is not required.

The summary correctly identifies the actual bridge: finite-cut block refinement, controlled entry collars, nonabelian loop surjectivity, a fixed finite-graph factorization, and the resulting neighborhood homotopies. It does not promote fundamental-group surjectivity alone to a homotopy section. Its explicit remaining gaps cover higher covering dimension, infinitely many components, and the lack of a general isolated enlargement.

The other results are described with their accepted limits:

- Finite-type isolated movability is credited as a reconstruction of an already announced statement. Freeness of integral first Čech cohomology is not confused with finite rank or with movability.
- The finite-complement and second-cohomology conclusions, Hawaiian-earring realization, and actual finite-component block refinement retain their accepted hypotheses.
- The incompatible-winding satellite compactum is a topological nonmovability example, and its isolated realization is ruled out. Simultaneous invariance with further invariant structure is not ruled out by that conclusion.
- The 2013 source correction is limited to the unqualified topological circle-approximation implication. The adding-machine theorem and an interpretation imposing simultaneous invariance are not claimed refuted.
- The abstract collared-quotient example is not presented as a three-dimensional flow realization.
- Short-gap, metric-threshold, regular-radius, quadratic-contact, and Hausdorff-continuity examples refute particular construction shortcuts. They do not exclude all permitted invariant enlargements. In the examples with movable stationary C, B=C remains an admissible enlargement.
- The optional extension in `FORCED_EXTRA_STRUCTURE.md` to cyclic first-cohomology clopen connected compacta is explicitly outside separate independent acceptance in the README and index. This final reader review does not certify that extension.

These distinctions agree with the supplied mathematical acceptance reports. No new general affirmative result, all-enlargements counterexample, global-openness certificate, or novelty claim is introduced.

## Version control and the empty-entry correction

Only `ONE_DIMENSIONAL_ISOLATED_MOVABILITY_V2.md` is accepted as the current dimension-one proof. The original file is not present among the reader's current proofs. Its historical identification inside the dimension-one audit is intentional and is not a broken dependency.

The preserved original is 19,249 bytes, SHA-256 `76e335e786c9a1f908bd671bd30110bfcb2cd991cc3352cccd9e1035207f5655`. The V2 file is 19,573 bytes, SHA-256 `5a325bc382d9094bd50e13b8a17fbdf8151b31e56dc58e3e32af9355f8a0ca1c`. Independently applying the patch's single removed and single added paragraph to the original reproduces V2 exactly.

The exceptional case is stated correctly: when the entry surface E is empty, N=N⁻ and D=N⁺=K; backward flow gives the required conclusion. The incorrect identification D=N and forward-flow direction are not accepted. No theorem hypothesis or movability quantifier changes.

The correction patch is 1,593 bytes, SHA-256 `91ad5980bd093fccf4d0466e2a45963712308d2d9d39b64543cb6d49b1ded9b4`. The final dimension-one acceptance is 20,986 bytes, SHA-256 `24df75398dda97da9038ee94bf33495fb8eb1efd7d257002130e6fff58d3da0a`.

The correction record also properly resolves the earlier satellite neighborhood repair, the subsequently excluded isolated-satellite proposal, the actual meaning of planar function graphs, the stationary origin exception, the distinction between shape realization and embedding, the quadratic cap retraction, and the nonempty-set qualification for Hausdorff convergence. Historical drafting-time “pending audit” statements are clearly distinguished from final status.

## Completeness and transformation provenance

All 28 authored inputs represented in the provenance record were checked against their preserved originals: 16 proofs, 11 mathematical acceptance reports, and the correction patch. Their original byte counts and SHA-256 values match the recorded identities.

Twenty-seven public copies are byte-for-byte identical. The sole transformed authored item is the ambient-block acceptance: exactly one local input-directory prefix was removed, leaving its basename, input hash, mathematics, and citations unchanged. Reapplying that precise transformation to the original reproduces the public copy exactly.

Its original identity is 14,926 bytes, SHA-256 `b519ba9131089ad9732028d7e9e32cfa9e1a5a1bfd0ad3b9876a302aae56fe84`. Its reader identity is 14,885 bytes, SHA-256 `7dc2d31f3b4a3b6e5413340c55c35e9f614b877f185cfaddbf898c9e3836ef21`. The original hash in the dimension-one audit deliberately identifies the original audit input; `ARTIFACT_PROVENANCE.json` and `CORRECTIONS.md` explain the difference.

The complete new presentation and metadata pieces were read: README, source guide, correction record, proof index, disposition, artifact provenance, source metadata, integrity instructions, manifest, and verifier. The transformed ambient audit was read in full and compared to its original. The proof-to-audit mapping was checked against the accepted inputs and each audit's scope. Every authored mathematical file cited by basename is supplied, except the deliberately superseded original proof identified as historical evidence.

The dependency paths are complete: the dimension-one proof includes the ambient refinement and acceptance; the satellite obstruction includes the satellite geometry and cohomology; the vertical cascade includes the stretched-book input and its successive audits; and the collared-quotient argument includes both its main proof and direct-core supplement. No private coordination document is required to read these mathematical arguments.

## Source credit and inspection history

The source guide correctly distinguishes the earlier 2007 Question 14(1) from the later Oberwolfach contribution, including the report-year/publication-year difference. It preserves the original all-flow, all-neighborhood quantifiers rather than importing restrictions from the surrounding aperiodic-flow context. The supplied recovery evidence supports those exact primary locations.

The mathematical dependencies are credited to their stated sources and locations. In particular, the 2024 Sánchez-Gabites block results are not silently strengthened by dropping finite-cohomology hypotheses from a different theorem; Richards and Armstrong are credited for the surface and relative-collar inputs; Bing supplies an actual embedding; Borsuk supplies the cited movability framework; and Rataj–Zajíček supplies the precise regular-level implication. The direct folded-core supplement is correctly distinguished from the alternative free-group ascending-chain route. Historical or contextual sources are not promoted to audited universal theorems.

The 2016 announcement is explicitly historical credit, with the structural audit's attribution-check limitation retained. The supplementary embedding/shape distinction, unsuccessful later retrieval, text-only inspections, and inherited inspections remain explicit. “Independent AI mathematical audit” is the stated review type; neither human refereeing nor formal proof verification is implied.

Seven locally available primary PDF copies were independently rehashed during this reader audit, and all seven match the recorded retrieved-byte hashes and counts in `SOURCE_METADATA.json`. The two further PDF identities agree with the inherited satellite and regular-radius audit records. No publisher-provided checksum was checked, and these matches are not independent source authentication. The two text-view source records correctly have null PDF size and hash fields. These eleven source-identity records are a selected metadata inventory, not a claim that every cited bibliography item has a locally hashed PDF.

This reader audit did not perform fresh third-party page retrieval or repeat the earlier visual source inspections. Inspection history is checked against the supplied records, not redescribed as a new inspection. Public URLs are preserved scholarly citations; current external reachability and redirected website contents are not certified. Source hashes identify particular bytes and do not authenticate the truth of source statements.

The final public files contain authored mathematics, citations, and safe verification metadata. They contain no redistributed third-party PDFs, source extracts, datasets, private correspondence, or operational coordination material. All public text files, including the corrected verifier, passed the separate publication-hygiene checks.

## Integrity tests and assurance limits

The corrected reader was tested using ordinary Python, `python -O`, and `python -OO`. Each mode produced the same intended outcomes. A total of **150 executed checks** matched their explicit expectations: **135 rejection checks, 12 clean or permitted-empty-directory checks, and three demonstrations of the documented unpinned semantic limitation**.

The rejection cases covered:

- changed payload bytes of the same length, appended bytes, missing files, unexpected ordinary files and PDFs, and changed verifier bytes;
- symlink roots, listed payloads, manifests, directories, ordinary links, and dangling links;
- an unexpected FIFO, invalid UTF-8, invalid JSON, duplicate JSON keys, duplicate manifest records, self-referential manifest records, malformed byte counts and digests;
- absolute, parent-traversing, noncanonical, and backslash manifest paths;
- wrong manifest target/schema, wrong external pin, and malformed external pin;
- consistently resealed false solved status, an extra substantive pass, invented lifetime count, and novelty claim;
- a resealed alteration of the hard-pinned V2 proof, reintroduction of the superseded original, a source-body flag, missing provenance, and broken or escaping local links, including percent-encoded traversal;
- a consistently rewritten theorem-metadata field when checked against the original external manifest pin.

The clean direct entry point was tested as well as a trusted verifier invoked against separate test copies. The pinned reader stayed byte-for-byte unchanged. Empty directories are intentionally immaterial, as the instructions state. A Unix-socket fixture could not be created in the execution environment and was not counted as a tested rejection; the ordinary FIFO fixture exercised the added nonregular-entry rejection branch.

The deliberately retained limitation is important: if some theorem metadata and its manifest are rewritten consistently and no external pin is supplied, the program can still pass. It is not a complete semantic theorem checker. The same rewrite is rejected with the trusted external manifest pin. The final mathematical scope was reviewed separately against the actual supplied proofs and acceptance reports.

The tests used temporary copies and ordinary Python subprocesses. They do not establish an operating-system sandbox, resistance to concurrent hostile filesystem changes, or trustworthiness of an arbitrarily replaced verifier. A manifest is not a signature. A successful run proves only the stated byte, inventory, selected-metadata, and local-link properties under the documented assumptions. It does not prove mathematics, source authenticity, novelty, or the unrestricted conjecture.

## Final disposition

The corrected, externally pinned 38-file reader is accepted for publication within the stated authored-material scope. Its mathematical artifacts and previously accepted theorem boundaries are unchanged. The original dimension-one error stays superseded, the optional extension remains separately uncertified, and the full invariant movable-enlargement problem remains unresolved after five new shared passes.

No remote mutation or additional proof search was performed by this reader audit.
