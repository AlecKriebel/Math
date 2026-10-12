# Original source intake — PR60 / 10300054

PR60 at head `1e762651b698c1fb519901bd924c5bd3717cc5ef` preserves an **unresolved** attempt at Calegari Question 13.1. Its proposed disposition is `unsolved`, **1/5 substantive attempts**, no full resolution and no novelty claim. This is source authentication and claim preparation, not an additional mathematical attempt or independent mathematical verdict. The preparer previously handled PR56/57/58 audits and preparation; that continuity is disclosed.

## Literal target and success condition

The pinned record is 10300054 / AMR-102-0054. Calegari's *Problems in foliations and laminations of 3-manifolds*, arXiv math/0209081, printed page 29, §13.1, Question 13.1, fixes a minimal taut C² foliation of an atoroidal 3-manifold with nonzero Godbillon–Vey evaluation. It asks for global defining/auxiliary forms satisfying
$$
T\mathscr F=\ker\alpha,\qquad d\alpha=\alpha\wedge\omega,
$$
with `ω∧dω≥0` everywhere or `ω∧dω≤0` everywhere. Zeros are allowed. The requested choice changes forms for the fixed foliation. A complete solution must prove existence for every eligible foliation, or construct a genuine eligible foliation for which every allowed choice fails.

The submitted artifact explicitly interprets global forms through coorientation and the fundamental-class evaluation through a closed oriented manifold; these are its stated conventions, not additional primary wording silently inserted by the preparer. Its formulas are smooth-category statements, and it does not upgrade general C² data to smooth data (original OBSTRUCTION.md lines9–19). The source's four remarks distinguish torus-leaf/nonminimal splicing from the required hypotheses, ask separately about weak-sign zero sets, and give an Euler-class obstruction for the strictly contact case. Question13.2 is separate. No nonzero Euler-class argument alone excludes the weak sign asked here.

## Exact submitted claim and boundary

The submitted deliverables are the smooth gauge parametrization and transgression (OBSTRUCTION.md lines23–41), the scalar fixed-gauge equation and invariant-measure necessity (lines45–60), strict/approximate averaging criteria for general smooth flows (lines64–86), an explicit Liouville transport nonattainment diagnostic (lines90–111), and the distinction between strict contact and weak sign (lines115–117). This describes what the author claims; fresh mathematical assessment belongs to the two parent-assigned independent families.

The displayed scalar target is `v−Yf+X_fh≥0` after orienting the total invariant positively (lines121–125). The exact missing steps are a globally admissible gauge `f` using the minimal/taut/atoroidal assumptions and an attained smooth weak-sign correction `h` when invariant-measure averages lie on the boundary. The artifact supplies neither a general existence proof nor an actual eligible counterexample. Approximate nonnegativity and a nonzero integral alone do not constitute the claimed target. Its abstract torus diagnostics are explicitly not realizations of the source's three-manifold gauge data.

## Authenticity and source domain

The REST metadata confirms 18 changed files: generated QUEUE.md plus 17 scientific/support files under attempts/10300054. All17 saved bodies have authenticated Git blob SHA1 (including Git blob framing), SHA256, size, and exact scoped immutable-tree modes100644. Their local preservation modes became0444 after retrieval; directories remain0755. ORIGINAL_AUTHENTICATION.json records initial body authentication, and SOURCE_ACCOUNTING.json subsequently authenticates Git modes and the scoped tree. The original ten author files plus seven historical review/replay files are unchanged. The three replay duplicates equal the corresponding author bodies exactly.

The reported GitHub base and separately retrieved GitHub merge base are both `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; three commits are ahead. The current pinned head was absent in the initial local object database. Local object and merge-base reads failed; no fetch occurred. Read-only GitHub retrieval supplies the pinned authentication rather than claiming a locally computed merge base. FULL_PR_DIFF.patch is the complete retrieved patch; the administrative control reconstructs all17 new-file bodies and compares them with the immutable blob bodies. The queue edit is isolated from those scientific files.

## Prior report and attempt accounting

The imported raw problem equals the original source_record.json after JSON decoding, and equals the selected SQLite payload. Both upstream cache files match the manifest revision `37e53eabe540fb458758e198be61634bd02ee008` and whole-file bytes/SHA256; neither corpus nor the SQLite catalog is copied into this packet.

The prior report is **present**, a direct upstream dictionary at key `AMR-102-0054` with eight fields and classification `OPEN-TRIAGE`. It is not an absent value or an empty flat wrapper. SQLite stores it as TEXT:988B, SHA256 `8c2af2f7b8875c20b01084f20ad9315d65aac38588f9ddff36943868c802b2c4`; its decoded value equals the raw upstream object. RAW_PRIOR_SQL_TEXT.txt preserves its exact SQL text, and SELECTED_RAW_PRIOR.json preserves the selected decoded object. Its bounded earlier literature report says open as stated; it is not an exhaustive current-priority certificate.

Original turns.json declares one substantive gauge/transgression attempt, budget five, outcome unsolved, and the explicit global/attainment gap. This intake and the two independent verification families add no search turn or novelty credit. The author's historical source audit reports no prior local attempt and distinct related IDs10300044,10300060,10300067; the preparer independently confirms no selected native state key or related-target-group match, not every historical campaign/search claim. The native queue read at line87 has rank76 queued0/5; PR_QUEUE_SELECTED.json records the proposed head row unsolved1/5. No native queue/state mutation occurred. Manual generated-queue tracking and older regeneration behavior are repository-wide history; this discrepancy alone is not promoted to a new mathematical defect or merge blocker.

Native branch observations are main. Initial HEAD was `1d9831741c4f3ee56f590d45240a9d56559a8df2`; the later17:22 observation was `f7a312db106451c8641b422eb78bd82995f1c3e3`. Concurrent foreign work changed the checkout head. The accounting control's output label `native_unchanged_main` records branch observation and absence of preparer mutation, not frozen checkout bytes or a claim that HEAD never changed. Foreign work is preserved.

## Actual reading and reproduction limits

The preparer model-read the complete unique original claim, source audit, source record, provenance, attempt log/accounting, README/PR draft, submitted checker/result, and historical review/checker/summary/result after recording initial scope. The three replay duplicates were authenticated bytewise, without a redundant model reread. Full source bytes are checked administratively; the preparer does not claim a new universal mathematical verification. No findings from either fresh mathematical family were read or shared before their initial independent analyses.

The primary Question13.1 and all four remarks were personally read in the selected extracted text, lines1377–1413, printed page29. The reused private PR56 PDF348322B has SHA256 `dd77919a55a546000be384974a5c771a7de4f88a36b37fc25294045355fb651e`, matching author provenance. Its extraction123065B/SHA256 `a9ef91250a0dd1335010a921a302af39d79fb76593d174ee775972369dceeec7` is bound in place. No new download, rendering or image inspection occurred for this intake. The full PDF/text remain private temporary reading inputs outside this fixed handoff and are not redistributed. Hurder–Langevin and the bounded current literature search are historical author/reviewer reading claims; this preparer has not newly verified their entire sources or the worldwide absence of a later solution.

Original verification.json reports61 submitted checks, and the historical independent receipt reports209 assertions. These are preserved historical receipts, not freshly executed proof certificates from the preparer. Submitted and independent code were read and will be syntax/body-checked only. Actual replay is assigned to the differential-form family; its future results are not anticipated here. Finite algebraic controls cannot certify existence of a global foliation or the C² conclusion.

## Actual execution and failures

The first retrieval operator PID13717 encountered an HTTP404 for a trailing-slash directory request; the failing gh child PID13733 ran17:17:04.778007–17:17:05.250895UTC, exit1, full stdout127B and stderr25B, preserved with prelaunch operator source. The corrected operator PID14242 retrieved all17 immutable bodies successfully, confirmed stable PR head before/after, and preserved full command captures. The retrieval operators were launched through the tool, without a separate source-controlled outer stdout/stderr capsule; their internal gh subprocess capsules are complete. No fictitious outer capsule is claimed.

The owned accounting controller PID17710 launched child17711 at17:22:09.264282UTC, completed17:22:12.711497UTC, exit0, full stdout301B and empty stderr. It records scoped-tree/body/source/prior checks, not mathematical acceptance. Its source and controller snapshots precede launch. Initial uncaptured read-only Git/object failures and a truncated preliminary patch view are disclosed in INITIAL_SCOPE.md; no complete capture is invented for them. The later immutable retrieval and complete stored patch replace that preliminary access for authentication.

## Custody handoff

ROOT_verify_original.py, ROOT_close_original.py and ROOT_readback_original.py are source-only helpers, unexecuted by the preparer. Their full07777 byte/mode verification is administrative custody only. They do not import or execute submitted checkers, read remote/private corpora, adjudicate mathematics, or create scientific approval. Closure output must be outside this fixed packet; readback is a separate ROOT process. SOURCE.json is a self-excluding fixed index, files0444/directories0755. READY.json means prepared for ROOT reading and custody, not an executed ROOT closure, accepted solution, paper, or native acceptance action.

Remaining intake gap after freezing: ROOT's actual full reading/closure/readback and the two fresh mathematical family assessments. Original scientific gap remains exactly global gauge selection, weak-sign attainment and C² scope. No paper, external individual communication, native/Git/remote mutation, publication, or DOI was produced.
