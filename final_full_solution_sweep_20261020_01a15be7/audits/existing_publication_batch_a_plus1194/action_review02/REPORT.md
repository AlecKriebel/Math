# Fresh independent review of the repaired eight-publication ledger action

**Verdict: accepted for this exact action, subject to its mandatory fresh live gates. No remaining substantive concern was found in this bounded review.** This is acceptance of an existing-publication accounting action; no new publication, upload, PR merge, or globally atomic execution is certified.

## Exact reviewed versions

| Component | Bytes | SHA256 |
|---|---:|---|
| `audits/existing_publication_batch_a_plus1194/append_reviewed_rows.py` | 9487 | `1df2298698807526ff93ee0c2a4cfba74e4b05b81266adb6e5227a1c8d2f3dba` |
| `EXISTING_PUBLICATION_BATCH_A_PLUS1194_PROPOSAL.json` | 24479 | `6aa80b6d6db0197d953d4b237c2477ec1421a79409321323aec94b749fe2ca8c` |
| `audits/pr1186_2274/reconcile_existing_row.py` | 9105 | `0360bb97064000502aa04a38c7f8816229b298fcdcb2295f16acc7f2e53af1a5` |

Both complete executable sources were read before simulation. Exact copies are under `inputs/`. All eight additional evidence-document pins in the plan were checked and retained. All eight four-cell arrays are byte-equivalent as strings to the independently accepted seven-row suggestions plus PR1194 suggestion. The three shared source/plan/helper hashes were rechecked unchanged after testing. The real production case and reconciliation receipt were still absent at that observation.

## Fresh, independently authored falsification

`falsify_action.py` was authored for this review. No earlier review's executable suite was loaded or run. It replaces subprocess, urllib provider, and filesystem-sync access before importing either reviewed source, and intercepts the runner's helper exec so its imports are also stubbed before execution. Every file mutation belongs to `action_review02/private_controls/`; live workbook, production case, repository index/refs and provider resources were untouched. Cached real183-row ledger data and immutable PR bodies were copied only into private observations. There were **zero real provider calls and zero subprocess executions**.

The full deterministic suite passed222 scenarios:4 successful cases,205 pre-write rejections, and13 post-write rejections without success receipts. A further7 cases used the actual standard-library four-worker ThreadPoolExecutor with fully stubbed services; all passed. These cover successful ordered publication preflight, a neutral Crossref update, bibliographic and PR-identity failures, an ambiguous write outcome, and a post-write duplicate. The full suite uses deterministic ordering to localize injected faults; it does not claim to enumerate all thread schedules. No optimization-mode replay is claimed.

The229 total outcomes are in `RESULTS_normal.json`, `RESULTS_normal_threads.json` and `TEST_SUMMARY.json`. Reviewer checks use explicit exceptions rather than removable Python asserts. Structural-validator controls intentionally replace only their isolated fixture's plan-hash constant to reach deeper validation against altered fixture plans; that bypass is recorded per scenario. Separate unmodified-hash initial/late drift tests verify the real exact-plan gate.

## Duplicate repair challenged

Every one of the76 declared aliases was independently seeded as the sole identifying lead in an otherwise unrelated row, alternating Notes and columnAQ. Every case rejected before creating an append. This includes all nine original OWR/AMR IDs and the two formerly omitted same-paper arXiv families, including their explicit arXiv DOI forms. Nine additional doubly encoded original-ID leads in columnAQ also rejected. Removing each required original-ID alias from a controlled fixture plan separately rejected, confirming that the new original-ID parser/enforcement is active. Original-ID list disagreement and missing exact PR aliases rejected as well.

Eight further cases used an unrecognized alternate DOI plus a known named author as the sole publication clue; each conservatively rejected for reconciliation. Hence the duplicate rule does not rely on the selected journal DOI or title alone. Existing row preservation and final duplicate detection apply to all43 returned columns. One post-write additional alias row and one exact duplicate each prevented success certification and never caused a rollback or retry.

This proves handling of these checkable identity forms, not exhaustive semantic equivalence between every possible mathematical paraphrase. The cached183-row baseline produced no candidate hit. It is not a new live no-duplicate observation; the production runner must obtain its mandatory fresh live reads, and any lead requires semantic reconciliation rather than inserting another row.

## Complete action safeguards challenged

- **Publication identity:** Independent faults in every projected Crossref field (DOI, title, named authors, type, publisher, container, volume, issue, page, article number and both date projections) rejected. Per-publication registry-status, HTTP, DOI-resolution, head and body faults rejected before writing. A neutral indexed-date update and empty unnamed author object passed because they do not change the defined bibliographic identity. Actual publication preflight remains mandatory at execution.
- **Pinned evidence:** Initial and post-intent changes to the plan, helper and each of the eight evidence documents rejected without an append. Every pinned evidence path replaced by a fixture-only symlink rejected. Late faults were injected by the directory-sync hook after INTENT existed, so they directly exercise the final input gate.
- **Sheet identity and complete reads:** Wrong book/gid/title/type/column count, duplicate gid, altered metadata, wrong header/filter/dimension, a truncated extent and rows wider than43 rejected. Formula/value disagreement and change on the third preflight read also rejected.
- **Concrete request:** Successful cases issued exactly one native appendCells request to numericgid1254632077 in the exact workbook, with eight ordered rows of four `stringValue` cells each and blankB throughout. No values-range update, upload, auxiliary write or formula interpretation was used. Wrong action target/order, duplicate batch DOI, nonblankB and a nonstring literal all rejected in structural controls.
- **Before intent and persistence calls:** The stub write verifies the prior value/formula snapshots, eight-publication preflight and INTENT all exist, that the intent hashes the exact plan/helper and equals the exact native request, and that file fsync and containing-directory sync calls occurred before writing. A directory-sync failure rejected before mutation. This checks the call ordering and ordinary local behavior; it is not a hardware power-loss guarantee.
- **One attempt and ambiguous outcomes:** Nonzero CLI results before/after synthetic application, a thrown transport exception, malformed success JSON and unexpected replies all prevented a success receipt. Every fixture that created a case, including positive and post-write cases, was invoked again; the existing-case guard produced zero additional provider/CLI calls and no second write. All post-write failure fixtures retain INTENT.
- **Readback and concurrent changes:** Missing/changed/reversed/interleaved batch rows, prior-row edits and extra duplicate leads rejected after the single write, with no rollback. Concurrent unrelated appends just before or after the native append passed; all earlier rows remained identical, every exact result appeared once, and the eight results stayed contiguous and in order. Reported row positions correctly accommodate unrelated concurrent additions.

## Mathematical and attribution boundaries preserved

This review checks the row content against already accepted evidence identities and qualifications; it does not redo all eight complete theorem proofs or establish new priority.

| PR | Preserved material qualification |
|---|---|
|1021|Canonical degree12 onto the singular quadric; degree27 auxiliary cover is separate; inspected preprint repairs are not attributed to an uninspected journal body.|
|1065|Bounded-degree edge reinforcement with ordinary common finite integer initial counts; nonmonotone weights allowed; no arbitrary-real-offset or vertex/unbounded-degree extension.|
|1068|Original field assumptions char(k)≠p and pth roots, Chow grading/topological factor2; version-specific arXiv qualifications remain.|
|1142|Negative additive spectral bound via sufficiently large indices, including connected boundary; thesis2019, Crossref registration, later accession not thesis date.|
|1145|Complete integral closure computed in the same fraction field, with a nonarchimedean counterexample; no rank-one or archimedean claim.|
|1146|Historical characteristic-zero ladder assertion, including residue characteristic2; literal positive/equal-characteristic extensions and separate general necessity remain uncertified.|
|1152|Maximal-spectrum core bridge is an explicit checked deduction from the prior Poisson example; no false claim of literal corollary wording or all-prime-core theorem.|
|1194|Full finite classification for n≥k≥1 and six order3 residues, using arbitrary index subsets; existing named external authors and no new project theorem.|

The cells do not relabel established journal/thesis publications as AI-authored or unrefereed because their separate repository expositions used AI. They retain the named authors, correct DOI and publication metadata. ColumnB stays blank because a valid chat URL was not independently established.

## Limits and execution disposition

No substantive objection remains against the exact pinned action. Production execution must retain all its live registry/DOI/PR, fresh complete ledger, duplicate and input gates. If any gate fails or an outcome is ambiguous, inspect and reconcile the existing case instead of repeating an append. Cross-service global atomicity, prevention of every concurrent race, disk power-loss recovery, a fresh whole-literature priority search and new mathematical proofs are not certified.

All retained raw ledger data, cached PR bodies and fixture action snapshots are marked private in the manifest. Source/proposal copies, aggregate results and this report contain no credentials. This reviewer made no live mutation and no changes outside this new review directory. Bounded action review100%; overall sweep remains79%.
