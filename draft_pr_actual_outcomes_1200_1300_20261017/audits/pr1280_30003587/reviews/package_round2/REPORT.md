# PR1280 whole-package review, round 2

**Verdict: CLEAN for the exact frozen package. No actionable finding or required repair remains.** This is a new independent AI whole-package review, not a repeat of the earlier review or a review limited to its repairs. The conclusion concerns the mathematical deductions, current attribution, actual local artifacts and operative release controls assessed below. It does not claim live service integration or perform publication.

PR 1280; problem 30003587; original head `f5085a4c954f814cde1bc3be0727ff30373aea95`, single parent `a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f`, original branch `publish-diagonal-30003587-20261011`. Current context SHA256 `15af9fbbc467a5458d96373cf90b3d503b3d49234cfebd1958bef3bf4ed2e7a1`. Input freeze SHA256 `7520928e1b97250902a17474992bb84a298c5db257a0527f463158bc9ec69960`.

## Authentication and exact reviewed artifacts

The START and END authentication receipts check **every one of the 586 stable audit records and 186 external read-only records**, with exact byte length, SHA256 and case-sensitive component spelling. Neither receipt recursively interprets inventory paths as package membership. All 772 records remain unchanged. The checkout was independently observed on main. Read-only Git object inspection also authenticated the actual original head/parent and every one of the nine original blobs against the preserved submitted files. No index, worktree, ref or remote mutation was made.

| Assessed artifact | Bytes / count | SHA256 |
|---|---:|---|
| Current manuscript main.tex | 18,149 bytes | c9e6a6c1661a0a235644bd10e642a7d57a253c7d40c52e1a794ea29869697545 |
| Actual five-page PDF | 76,727 bytes; five pages | 42285ef1e7f0f7f7fa98b5879b2f9b46000609db2a50ff3e28ab37465ce684f7 |
| Actual verification ZIP | 784,065 bytes; 245 file members | f7aa63de23c1acfcc4b0d6d43576356a2934ec323f281349ae8949b184bf170b |
| Current edition correction | Nine original/current bindings; six changed files | 126706384a2ba998dcc115f95df0870e1165271c00803525d61ab6cafa446127 |
| Exact eleven-field metadata manifest | Two supplied artifacts | 17c08e9187ee55b5c7c88c9641a1474227c65241348cda0b7255e2311763c47f |

The PDF was independently rendered at 100 dpi and all five page images were visually inspected. Text, formulas, margins, page transitions and references are legible and complete; no clipping, overlap, missing glyph or unresolved citation was found. I read the full source and compared the displayed mathematical statements and equations. A new TeX compilation is not claimed: the frozen actual compiler/source/PDF receipt is authenticated, and compiler-control execution in workflow tests uses a clearly synthetic compiler.

`ARTIFACT_INSPECTION.json` records independent extraction and structural checks of the actual ZIP, using the outside frozen BUILD_RECEIPT anchors rather than trusting anchors computed only from the ZIP. Its root manifest has 244 nonself members, exactly matching the 245-member archive after the manifest itself is included. The original and current editions each have exactly nine files; both eight-nonself dictionary manifests authenticate. All original Git blob hashes agree. All **19 explicit family registries** and **217 portable records** authenticate using their declared literal entries/path/size schema. Absolute input, deployment, source and search inventories remain receipts; they are not inferred as additional members. Raw third-party bodies, extracts and private scratch are absent from the archive.

The current change map binds **15 changed UTF-8 byte spans and all 18 intervening/prefix/suffix unchanged gaps** across PROOF.md, INDEPENDENT_AUDIT.md and README.md. Historical acceptance and the historical editorial map are nested verbatim. The six documentary changes and both complete nine-file maps match the explicit correction. The unavailable older proof/audit/supplement bytes and missing historical aggregate-test inputs are expressly not reconstructed or authenticated. Historical assertion-based programs are preserved separately from the current durable evidence.

## Mathematics and attribution

`MATHEMATICAL_REVIEW.md` contains the detailed independent derivations, source locators and falsification boundaries. The full target remains the original OWR2017/42 printed page 2621 / PDF page 21 Question 1: every finite abelian diagonal quasi-free action on a simple purely infinite essential finite 0–1 Cuntz–Krieger algebra has, for each g, implementing unitaries fixed by the whole original action. Periodic, nonouter and nonfaithful actions are included. No approximate group law is asserted.

I recomputed the short route: exact CK/graph correspondence; essentiality plus simplicity forcing strong connectivity; diagonal-MASA/periodic-path necessity; normalized all-group vertex representation; outer quotient; equivariant phase homotopy; Gabe–Szabó uniqueness with both its implementation and cocycle-defect limits; finite averaging and polar correction; honest-cocycle restoration of exact original fixedness. The actual v1 Definition 1.15, Proposition 3.14 and Theorem 5.8 at pages 13, 29 and 45–46 have the hypotheses used. No UCT, extra stable-target or path-start-at-one requirement has been imported.

The retained Barlak–Szabó route was separately checked: cyclic classes, primitive length-d return graph with distinct path edges, corner injectivity and surjectivity including zero-length paths, outerness on a full invariant corner, fixed-point simplicity, fixed-frame lifting and the vertex pinch/polar step. The later ambient-full orbit-frame and honest-cocycle alternatives also check and explain why the former necessity language was too strong. A projective Pauli family cannot replace the honest graph representation. Trivial groups/quotients, all-inner and nonfaithful actions, one-vertex multiple-loop graphs, directed-cycle exclusion and periodic graphs were expressly considered. The revised intermediate edge hypothesis excludes the edgeless singleton before Kirchberg/infinite-path arguments; it removes no case of the original essential-matrix target.

Positive credit matches the actual source passages: Matsumoto's diagonal coboundary/periodic-point mechanism, Crisp–Gow's return-corner construction, Izumi's standard finite Cuntz predecessor, Barlak–Szabó's outer aperiodic theorem, Gabe–Szabó's general uniqueness theorem and Christensen–Neagu–Szabó's weaker strong-approximate-innerness duality infrastructure. Version-specific preprint locators are distinguished from final publication metadata. The full Zacharias chapter and final Izumi body remain explicit historical-priority gaps. I did not conduct a new worldwide literature search. No unclaimed firstness needs to be proved.

The note, current-edition qualifications and all eleven supplied metadata fields consistently describe attributed exposition and explicit verification of known consequences. They claim no new solution/mechanism, first combination, independent discovery, earliest consequence date, current worldwide openness, external human peer review or formal proof-assistant certification. Extensive AI use and finite-test limitations are disclosed.

## Operative release controls

All eight actual publication helpers, both actual coordinators, the pinned shared Zenodo kit and the actual private ready/merge driver were reviewed. `OPERATIVE_SOURCE_AUTHENTICATION.json` records their exact twelve source bindings and equality of the six repaired deployed files with their revision-family mirrors. The shared kit SHA256 is `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca`.

| Operative component | Behavior checked |
|---|---|
| prepare_package.py | Authenticate current context, original/current editions and explicit portable membership before replacing package copies; no receipt-based source-body inference. |
| build_package.py | Bind current source/PDF/actual page count and compile/layout receipts; exact archive inventory and bytes; outside trust anchors and isolated diagnostics. |
| compile_note.py | Exact target/gates/original/current source qualification; separate reproducible stamp from actual compile time; preserve source on failure. Fixture compiler is explicitly synthetic. |
| verification/verify.py | Strict paths/casing, exact root/edition/family schemas, outside anchors, source/correction/context/gate bindings and isolated durable replay. |
| append_tracker.py | Shared bounded identity predicate in every cell; exact four-cell row with blank B; designated gid/title; one exclusive intent; uncertain outcomes reconcile by exact row without blind append. |
| update_pr_publication.py | Main branch, reviewed context/metadata/artifacts/public/tracker identity; nine current records plus five additions; one original parent and every intended blob; exact branch/body recovery; no shared-index path. |
| check_public_downloads.py | Exact eleven supplied metadata fields after explicit public-schema projection only; exact production record/DOI identity; exact two public file names, bytes and SHA256. |
| workflow_regression.py | Full worker/entrypoint and fixture layout inspected before invocation; actual functions/mains exercised under clearly synthetic services, Git, compiler, reviewer and mathematical gates. |
| Deposit coordinator | Pinned actual shared kit, strict rejection of every normalization, fresh same-ID inspection and second strict GET before publish POST, persistent exclusive intents and read-only uncertain-result recovery. |
| Postmerge coordinator | main base, exact reviewed head/body, immutable two-parent merge with reviewed head as second parent, all fourteen blobs, DOI HTTP 200, exact unique designated tracker row and exact prior program state before advancement. |
| Ready/merge driver | Complete operative updater main reexecuted read-only; both completed intent/receipt identities, single original parent and all fourteen blobs; regular immutable controls; fresh live branch/base/body/scope/remote head; repeated authentication; one expected-head merge; no blind retry. |

The actual complete workflow worker was independently invoked **serially in normal, -O and -OO modes** with only REPORT_ROOT redirected into this review's scratch. Results are identical. Each run covers 900 identity/action cases, 350 complete postmerge cases, 88 ready-main negatives, five positive/recovery controls and 17 deposit cases. Every intended blob is corrupted separately in the ready tests. Missing/wrong/multiple parents, forged minimal receipts, all identity fields, completion flags, body/control drift, wrong/missing live base, remote scope, metadata/public/tracker defects, lost responses and exclusive-intent races are exercised. Wrong initial cases issue no ready/merge request; retargeting after a valid ready transition issues no merge. Actual local metadata is projected and compared independently of synthetic metadata.

The independent actual-archive verifier also passes in all three outer modes, with identical results. Each outer run executes all six current diagnostic programs in normal/-O/-OO isolated copies: **54 successful diagnostic executions** total. The six current ASTs contain no assertions. **18 isolated injected false predicates** fail in the required modes. My separate probes pass in every mode: **26 archive/schema corruptions rejected, 112 additional identity probes, and eleven actual-metadata field corruptions rejected per mode**. Case-mismatched paths, source/context/snapshot corruption, extra/missing payloads, unsafe paths, guessed member keys, selected absolute paths, duplicate nested members and nested bad hashes are included. Unselected absolute receipt fields remain ignored. Additional in-memory protocol fixtures call the actual recursive put/tree and saved-commit validator over fourteen intended files, preserving two unrelated paths and rejecting bad parent/foreign-path controls. These are supplemental protocol fixtures, not actual Git construction or service integration.

## Earlier findings and chronology

The earlier CHANGES_REQUIRED review is preserved with its 25 authored members, verdict/freeze anchors and 614-record historical inventory. Its superseded inputs are not required to equal the repaired current bytes. Its completion at 03:22:59Z precedes the root resolution at 03:35:26Z, which precedes this review's first durable authentication checkpoint at 03:36:11Z. I reviewed the current package before reading the earlier verdict's detailed finding metadata late in this review.

All four earlier concerns are resolved in the assessed current package: F1 complete publication authentication before ready/merge; F2 bounded shared tracker identities and exact-row recovery; F3 main base at every live phase; F4 the explicit intermediate edge hypothesis. The new tests and independent derivations support these resolutions; the resolution receipt alone was not treated as proof.

## Limits, resources and final disposition

No live network mutation, upload, public record creation, PR update/ready/merge, tracker change, Git mutation or external-person communication occurred. Only the assigned review folder was written. Primary bodies were read at relevant passages from authenticated private frozen inputs; not every page of every source was read, no raw source body was redistributed and no new outside input was sought. AI review and finite computations do not certify novelty or replace the imported operator-algebra theorems.

The actual local PDF/source/ZIP/metadata were assessed. No real future deposit, DOI resolution, public download, tracker append or merge is asserted by the fixture tests. Those operative live checks remain mandatory when the authorized parent workflow eventually executes. The final release gate was not edited or created by this reviewer.

All heavy workers ran serially, with temporary fixtures confined to the assigned _local directory and disposed on completion. No compiler cache was copied; no other research input/cache/scratch was deleted. There was no resource failure. A dated reviewer-script development KeyError is preserved separately in VALIDATOR_DEVELOPMENT_FAILURES.json; its cause was an incorrect local test-script field assumption, corrected before the passing artifact inspection, and it is not a package failure.

The END receipt confirms all 772 frozen inputs unchanged. There are no unresolved review findings or required repairs. Review completion estimate: **100% of this fresh whole-package review**, with the stated source, fixture and live-integration limits.
