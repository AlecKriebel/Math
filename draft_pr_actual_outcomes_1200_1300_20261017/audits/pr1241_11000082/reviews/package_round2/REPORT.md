# PR1241 independent whole-package adversarial review, round 2

**CHANGES_REQUIRED: one actionable publication-coordinator finding, F01.** The mathematical theorem, original arithmetic proof, alternative compact-core proof, six-page paper, portable archive and eight workflow helpers pass this independent review at the explicitly stated import and offline-test level. The newly frozen concrete deposit coordinator can publish nonexact metadata before rejecting it. This must be repaired and the changed package must receive a DIFFERENT NEW full review before a clean final gate is issued. No counterfactual CLEAN verdict is supplied.

The exact target is Farb Question7.6 / problem11000082 / AMR-109-0082: for each fixed closed genus g>=2 and fixed finite Johnson depth k>=3, every N is attained by N distinct ambient orientation-preserving Mod_g conjugacy classes of pseudo-Anosovs in I_g(k) having a common exact dilatation. Powers are included; the common value may depend on N.

## F01: strict metadata check occurs after publication

**Priority P1.** Operative file: `draft_pr_actual_outcomes_1200_1300_20261017/_local/run_pr1241_deposit.py`, lines37–44, especially the subprocess invocation at41 and normalization check at44. The byte-identical read-only provenance copy is `REVIEWED_COORDINATOR_READONLY.py` in this review. Its SHA256 is `ad1690233c038de11f3c86849194766b9498d5dd5a8dccaaf24ce3e619c72418` and it is attributed as a COPY, not newly authored production code.

For `publish`, the coordinator checks a positive known STAGE_RECEIPT ID and calls the generic kit. It does not require an exact inspected-draft receipt or perform a strict exactness check on the kit's pre-publication verification. The kit intentionally accepts narrow metadata normalizations. Its `run()` stores a nonempty normalization list and still calls `client.publish()`; the coordinator refuses that list only after the subprocess has returned. The reviewed actual metadata has U+2019 apostrophes in a description consisting of plain p paragraphs, precisely one normalization the kit deliberately accepts.

The new offline reproducer executes the coordinator source with ONLY its absolute REPO constant redirected to a private copy. Its actual frozen gate, input-freeze authentication, source/PDF/ZIP/current-edition comparisons, original-draft/branch checks and read-only tracker preflight execute. Subprocesses are intercepted. The Zenodo action is implemented by the actual reviewed `zenodo.py` `run()` with an in-memory fake client and patched state/DOI persistence. The remote's actual supplied description has only its U+2019 apostrophes converted to ASCII before `publish` starts. No live operation occurs.

Observed order:

1. Read-only original PR, branch and tracker preflight all succeed.
2. Kit GET77 returns the known unpublished draft with that normalized description and the exact two files.
3. Actual kit verifier accepts and reports `paragraph_apostrophes_u2019_to_ascii`.
4. Kit invokes **one simulated publication POST** for77.
5. Kit GET77 confirms publication and returns the normalization list.
6. Coordinator raises `RuntimeError: Nonexact metadata; no further mutation` and saves **no PUBLICATION_RECEIPT.json**.

The positive exact fixture also publishes successfully with no STAGE_INSPECT receipt at all, confirming that the required inspect-before-publish stage is not enforced. F01 does not allege a live incident: there were zero real publication POSTs. `COORDINATOR_RESULTS.json` preserves exact events and counts, and `coordinator_probes.py` is independently replayable.

Required correction: enforce same-known-ID, ready unpublished draft, complete exact supplied metadata/files and `metadata_normalizations=[]` BEFORE any publish POST, including the verification actually used by the mutating operation. An absent or stale inspected-draft state must not silently authorize publication. Canonicalizing the current description can avoid this known transformation, but cannot replace a pre-mutation exactness guard. Preserve known-ID/uncertain-outcome reconciliation and read-only treatment of an already published record. Add negative tests showing that the actual current-description normalization and absent/nonexact inspect state cause ZERO publish POSTs. Review any changed metadata/coordinator and resulting exact release in a fresh whole-package round. Root must make the fix after this seal; this reviewer made no input edit.

## Scope, identity and independence

The externally supplied INPUT_FREEZE SHA256 is `e7f5c3a83a264da8978c6f95cb18e60bfa68d74b2a365ae98d1632874b5edefd`. All271 internal files and all3 external read-only inputs authenticated at the start and again at the end. External inputs include the actual coordinator and both Zenodo-kit files. The input manifest itself retains the outside anchor. Start/end receipts enumerate every size and digest, rather than sampling the release files.

| Artifact | Exact reviewed identity |
|---|---|
| PDF | 94,186 bytes, six pages; SHA256 `2e81d976955f4d46aaebf9b8ae30fbde5a8ca91236cd2a43ab5e6ef213eeb948` |
| ZIP | 288,996 bytes,105 unique file members; SHA256 `9b6fd471b6aaff24b8597c5dca4267141c7c13e8ae910869a41ef09c94dc55c6` |
| TeX | SHA256 `946560bb03e583795eef5202488d937f58cca0019b39b8ac37afec6a2ce01ff7` |
| Metadata | SHA256 `0f1048dfaf642d2c49efd0432b359112a9538819c2e397c6071e9acaa570b5e1`; all11 supplied fields |
| Original target | PR1241, head `493a764dec034b7b645be76a284c4e6edc0583eb`, eight original Git blobs |

AGENTS.md was read. This is one fresh whole-package adversarial reviewer; no other reviewer agents or shards were contacted or spawned. Independent first-pass mathematics and code notes were written in INITIAL_INDEPENDENT_NOTES.md before any semantic reading of R1's conclusions. Initial checksum authentication read prior files as bytes only. R1 was subsequently consulted for history consistency. Its report expressly excludes the then-unfrozen concrete coordinator; F01 concerns that newly included implementation and does not claim R1 silently certified it.

All mutations in probes were on copies or in-memory adapters. No original input, actual Git object/index/branch/ref, remote, PR, Zenodo object, DOI, tracker row or Google Workspace object was changed. The repository's independent-research no-outreach rule was respected. No credentials were read. Relevant primary source bodies were read-only; source retention and actual inspection are distinguished in PRIMARY_INSPECTION_RECEIPTS.json. Narrow parent progress reports were authorized by the parent; no external individual communication occurred.

## Mathematical review

MATHEMATICAL_REVIEW.md records the independent derivations and boundary attacks. The strongest verified mathematical result is the complete target relative to the correctly identified standard imports; no unresolved mathematical gap was found.

The outer Johnson centrality proof correctly adjusts quotient-inner representatives, and separating twists lie in I_g(2). The separating filling-pair import covers every closed g>=2; Euler characteristic and parity force even mu>=4. The explicit commutator has q_next=-mu*q^2 and trace2+mu^2*q^2, giving q_r=-mu^(2^r-1) and trace2+mu^(2^r) for r>=2. The prescribed fixed r reaches I_g(k). Nonzero q excludes endpoint0, and a fixed parabolic conjugation separates the two endpoint pairs, including an infinite endpoint. Common large powers produce a real Schottky group with compact convex core. Freeness of the images proves derivative faithfulness on H alone.

The fusion lemma fixes one reference u and ONE axis point x for all ambient conjugators of u. The same finite set S determined by compact K and discrete G controls every resulting intrinsic class. The constant is independent of the trace words and length. Torsion in G, proper powers and finite full derivative kernel do not add a missing factor. Every ambient Mod_g conjugator preserves the unique invariant disk, so the argument uses the full stabilizer image. The infinite-index normal-subgroup counterexample violates compact-core compactness and supplies no counterexample to the actual lemma.

Horowitz's stage exponents are linear2m, with2^m sign choices. The unique positive odd and closing y markers recover all signs, including the m1 case U=x with no y-syllables. The rank-two trace-coordinate sign-flip argument proves equality under EVERY SL2(C) representation, not just checked examples. Nontriviality plus the Schottky property supplies hyperbolicity. SL2 lifts exist because H is free, and the factor2 between H2 length and log(lambda) is correct. Genus, depth, H,J and fusion constant precede N and m.

The original arithmetic proof separately passes: all signed saddle holonomies form a rank-two integer lattice preserved by every affine derivative; the modular index-six free commutator subgroup and finite covering core control fusion including proper powers; unique disk handles every ambient conjugator. Its explicit genus-two branched-cover seed is valid. The current eight-file edition contains the original proof verbatim under a historical heading and states the complete alternative proof. Historical execution and source statements remain historical and are not retroactively recertified.

The conservative Kapovich deduction is explicitly a2026 assembly of older ingredients, not a historical solution date. Its ambient torsion-free group is the modular commutator subgroup and its deep subgroup need not be finitely generated. The optional FLM small-component incidence seed remains source-qualified/unreconstructed, unpromoted and absent from the paper's dependencies. No orientation-reversing/inversion, ambient-primitivity, simple-loop, single-value infinite-multiplicity or all-depth-intersection conclusion is imported.

Fresh finite controls add2,058 exact generic commutator cases,24 deep/endpoint cases, degenerate q-zero and trace2 controls, and five Horowitz word levels in rational/trivial/lift-sign representations. These checks supplement the infinite written arguments and do not prove geometric realizability of arbitrary algebraic parameters or ambient nonconjugacy.

## Primary sources, priority and disclosures

The same-scope known theorem in Alper Ferudun's unrefereed preprint DOI10.5281/zenodo.23301731, Theorem1.1, was independently read in the authenticated primary PDF. PDF1–2 and7–9 establish the exact printed theorem and the restricted arithmetic/full-conjugator/virtually-free comparison relevant here. Its stronger extended/inversion and optional numerical claims were not adopted. The abstract, introduction, bibliography, deposit description, current edition and planned tracker/PR prose all explicitly credit this known result and describe an alternative convex-core proof. There is no firstness, new-existence, new-mechanism, current-openness or disclosure-lineage assertion.

Leininger's precise disk/discreteness/kernel/length and unique-disk restatements and Aougab-Taylor's all-genus pair lemma were checked through primary PDF material. Horowitz's Example8.2 and the relevant trace-polynomial interface were read; physicalPDF14/printed648 was also rendered and visually checked to remove OCR ambiguity in the exponents. Farb's actual author-volume PDF21/58 confirms conventions and target: printed14/51; the published chapter range11–55 is deliberately not treated as that version's pagination.

Anderson's author-hosted primary PDF1–2/18–20 was newly hash-authenticated and read. Section5 discusses the intrinsic-to-ambient conjugacy obstacle, malnormality/Kapovich and a compact-core argument. This supports contextual credit, not a novelty claim for the present mechanism. The Anderson catalogue/Crossref final-range conflict307–341 versus307–342 and author-PDF running pages470–502 is explicitly retained in the bibliography QA; the actual paper omits the disputed range and cites section5 of the identified author version. No unsupported final-page or date mapping is made. Direct web access failure to the author PDF is recorded as such; use of an existing authenticated body is not misrepresented as a fresh successful body retrieval. Original Bers proof remains an accepted import through the specified restatement, not an inspected original proof.

The chronology records are bounded: PR/Git creation fields, currently observed repository visibility and record creation date do not establish historical content/visibility, discovery order, dependence, independence or misconduct. The paper's extensive-AI, unrefereed, no-external-human-peer-review and no-proof-assistant-certification disclosures are consistent. Raw third-party inventories are receipts, not portable source bodies authenticated by the archive. No unsupported worldwide-priority search certificate is implied.

## Archive, rendering and actual reproduction

The PDF skill was used read-only. All six pages were rendered with Poppler and individually inspected. LAYOUT_REVIEW.json records clear matrices, exponents, markers, references, author metadata and page continuations, with no clipping, overlap, missing glyph or unresolved citation. The short bibliography continuation on page6 is acceptable.

The source recompiled with Tectonic0.16.9 and the recorded compiler SHA256, using SOURCE_DATE_EPOCH1792267200. A cached-only rerun explicitly redirected TECTONIC_CACHE_DIR to a PRIVATE COPY of the macOS Tectonic cache and reproduced the exact PDF bytes. The chosen epoch is a reproducible20:00:00Z build stamp, not the compilation or review completion time. No universal cross-environment determinism is inferred. The absent XDG cache target on macOS was handled by explicit private-cache selection in this review; it is not a paper correctness finding.

The ZIP has105 unique safe regular-file members; every root binding, seven real family freezes/53 members, both edition manifests, all local/archive current8 and submitted8 files, exact TeX copy, and all original8 Git blob SHA1 identities were independently checked. The custom `new_authored_files`/`path_relative_to_family_root` schema was exercised explicitly. Fourteen new coupled-corruption probes alter one member in each actual family and rewrite the outer inventory, then also rewrite the nested freeze; the preserved outside anchors reject every case.

The extracted standalone verifier ran in normal,-O,-OO modes. It matches the root finite diagnostic in all three modes and runs the two essential-assertion family programs in fresh NORMAL interpreters with inherited PYTHONOPTIMIZE cleared, on copies only. Frozen result bytes match. No missing historical program is claimed as replayed.

Actual copied `prepare_package.main()` and `build_package.main()` reproduced both the exact PDF AND ZIP. The only preparer Git-facing query, ignore classification, was replaced by an in-memory adapter declaring scratch candidates ignored; explicit registered members are still restored by actual preparation. No real Git command ran. The real portable verifier and pdfinfo executed on the copy. Build receipts and outputs are retained at this review root.

## Workflow coverage and adversarial tests

Every line of all eight requested scripts was reviewed: prepare_package, build_package, compile_note, verification/verify, append_tracker, update_pr_publication, check_public_downloads and workflow_regression. WORKFLOW, WORKFLOW_ADAPTATION, both read-only Zenodo-kit files and the newly frozen actual coordinator were reviewed. Supplied regressions were replayed in normal,-O,-OO modes, but the conclusion also rests on newly authored complete-main probes.

| Fresh check family | Scope and outcome |
|---|---|
| Coordinator,32 cases | Full frozen-input/gate/kit/source/release checks precede live preflight; all eight actual helper drifts, an actual nonclean verdict with updated digest, frozen-input drift, kit drift, original PR/draft/head/body/branch drift, canonical tracker tab/gid/header/problem preflight and existing local publication receipt stop before simulated publication. Known-published kit state makes zero POSTs. **F01 remains the one expected failing safeguard.** |
| Public complete main,18 cases | Positive same-record/two-file fixture; corruption of each of all11 supplied metadata fields, record ID, record DOI, metadata DOI, inventory and bytes is rejected. |
| Tracker complete main,11 cases | Exactly four cells with blankB and canonical A:D readback; a successful exact retry and accepted-append/lost-response recovery cause only ONE append. Duplicates, alteredB, uncertain intent without a row, headers, gid/title, readback and append dimensions are rejected. |
| PR complete main,six families | Actual tree-assembly logic runs through an in-memory Git-object adapter. Success yields one commit directly parented to the original, precisely13changed paths with exact blobs, and preserved unrelated content. Only a nonforce pinned push and one body edit occur. API lag, lost push and lost body responses recover without duplicate writes. Outside body/branch changes stop. |
| Saved/actual commit identity | In each successful PR family,16 saved identity fields are independently corrupted and rejected by COMPLETE main; actual modeled wrong parent, extra path and differing blob bytes are also rejected. |
| Actual document bindings,17 cases | Real six-page PDF and real pdfinfo on a copy; stale source/PDF, absent/failed compile, wrong epoch/source/PDF bindings, incomplete/duplicate page indices, wrong page count and invalid context page typing are rejected. |
| Seven actual nested families | All53members authenticate;14coupled outer/nested corruptions are rejected. |

These are offline adapters, not actual remote Git, GitHub, Zenodo, DOI or Sheets integrations. They validate the modeled state transitions and production function behavior; no strict server/concurrency guarantee is claimed. Future live publication, public downloads, tracker, ready/merge and merged-byte receipts remain necessary. Their absence at this stage and the intentionally not-yet-authored final gate are NOT findings.

## Final disposition and seal

One actionable finding remains: F01. No other mathematical, source/priority, disclosure, layout, archive or tested helper defect was found. The mathematical theorem passes within its named imports; the complete publication package is **not CLEAN**. No original or external object was repaired by this reviewer. The parent has acknowledged F01 and will repair only after this review is sealed, followed by a different new complete review.

INPUT_AUTHENTICATION_END.json repeats every declared input and the outside manifest anchor. Authored root reports, scripts, results, logs, authentication receipts and dotfiles are sealed in FREEZE_MANIFEST.json. The pre-existing INPUT_FREEZE and the output manifest itself are excluded from the authored list. scratch_local contains copied/generated fixtures, raw text, caches and renders, deliberately ignored; its authored .gitignore is included in the seal. The root-level coordinator provenance copy is explicitly a byte-identical read-only copy. The final outside SHA256 of the output manifest is delivered separately to the parent. Completion estimate:100% of this assigned whole-package review, with one required fix and no advance live-publication certification.
