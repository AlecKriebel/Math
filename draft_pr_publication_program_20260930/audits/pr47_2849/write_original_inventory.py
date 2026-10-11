"""Author first-party inventory of original PR47 only, without accepting its claims."""
from pathlib import Path
import datetime as dt, json, hashlib, os
A=Path(__file__).resolve().parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def write(name,b):
    with (A/name).open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
def main():
    source=Path(__file__).read_bytes();write('INVENTORY_PRELAUNCH_SOURCE.py',source)
    m=json.loads((A/'original_pr_metadata.json').read_bytes());snap=json.loads((A/'snapshot_manifest.json').read_bytes());native=json.loads((A/'ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json').read_bytes());sql=json.loads((A/'ORIGINAL_SELECTED_NATIVE_SOURCE_READ.json').read_bytes());at=now()
    body=r'''# PR47 original claim and provenance inventory

This is source preparation for a future independent audit, not a mathematical verdict, acceptance, current literature certification, novelty review, or merge recommendation. The exact original sources are frozen separately from any later root or family work. Independent scientific/source review is **PENDING**. Merge remains pending. No original scientific helper was imported, compiled, or run.

## Git and GitHub authority

Actual read-only GitHub REST captures identify open draft [PR47](https://github.com/AlecKriebel/Math/pull/47), title `2849: reviewed instanton obstruction; original target unresolved`, branch `dot/math-2849`, base branch `main`. Its original HEAD is `487327b2412c436ae69e8c52bf353a9a1fb7594e`. GitHub base is `c6975ca76f9f667f1250ba403d0e6da2aafe14d0`; actual `git merge-base` was separately queried and happens to equal that SHA. These are distinct authorities even when equal. The GitHub metadata body, changed-file API result, Git commit records, complete binary-capable diff, and every scientific blob are retained as first-party procedural evidence.

The whole diff has **17 changed paths / 59,460 bytes**, SHA-256 `17a6b488f85b54d22af865a5e0c9644b016211c3c985bd352631b46632dedc27`. It adds **16** blobs under `unsolved_math_prioritization/attempts/2849/` and changes one row of `unsolved_math_prioritization/QUEUE.md`. The scientific full Git tree was independently queried and matches all16 exported bodies exactly. Each original Git mode is `100644`; exported scientific files have full filesystem permission mode `0444`. Literal path, relative path, byte length, SHA-256 and Git blob identity appear individually in `snapshot_manifest.json`.

Initial missing-object query failed with exit128 and empty stdout; its stderr is preserved. Fetching this exact SHA supplied the object without checking out or changing a branch. No index, branch, native queue, state or history mutation, commit, push, external communication, release, DOI or paper action was performed by this preparer.

## Exact target and scope boundaries

The original hypothesis concerns every closed oriented rational homology3-sphere Y for which every homomorphism from its fundamental group to SU(2) has abelian image. The exact target is equality `dim_C I#(Y;C) = |H1(Y;Z)|`. It does not require irreducibility, a surgery presentation, cyclic first homology, cyclic finiteness, or Morse–Bott nondegeneracy. A proof of the entire equality under those hypotheses, or an actual manifold satisfying the hypotheses and violating equality, is the full success criterion. An abstract analytic germ or an auxiliary preprint inconsistency cannot settle that target.

The package explicitly says **unresolved** and claims only an obstruction to one proof shortcut plus a narrow source diagnostic. The representation orbit count gives the expected ordinary homology rank for the reducible representation set. The original then identifies a gap between that set and the transverse adjoint deformation cohomology / degenerate local Floer data. Its claimed split uses the squared character `chi^2`, with `dim_R H1(Y;ad rho_chi) = 2 dim_C H1(Y;C_(chi^2))` because ordinary real H1 vanishes.

The claimed abstract diagnostic is the circle-invariant quartic `(abs(z1)^2-abs(z2)^2)(abs(z1)^2-2abs(z2)^2)`. It is said to have only the origin critical, zero Hessian, lower link `T^2 x [1/2,2/3]`, and local critical groups of ranks2 in degree2 and1 in degree3: total rank3 with Euler characteristic1. No assertion realizes this germ as a Chern–Simons slice or a3-manifold. Even if all of that diagnostic is independently confirmed, it blocks the abstract shortcut only.

The narrow auxiliary check concerns the printed unsquared-root Definition5.3 and torus-knot clause of Corollary5.4 in `arXiv:2608.20551v1`. The original claims slope6 surgery on the right-handed trefoil has fundamental group `C2*C3`, first homology `C6`, only abelian SU(2) images, and Alexander polynomial `Phi6(t)=t^2-t+1`; it fails the unsquared sixth-root test while passing the squared test. The resulting filling is itself claimed to be a known instanton L-space. Scope is exactly this versioned clause and definition, with no conclusion about the paper as a whole, motives, or author conduct. Future source reviewers must freshly authenticate the literal applicable version, surgery conventions and exclusion cases before relying on this check.

The original credits the known cyclic-finiteness / Morse–Bott sufficient theorem, including central-representation cases. Its other literature boundaries are Li–Ye's restricted prime-power or twice-prime-power surgery numerator result and the different Heegaard Floer conclusion in the specified graph-manifold family. These are recorded original-source claims awaiting fresh independent authentication here.

## Strongest original result and exact gap

Strongest claimed result: an explicitly unresolved, elementary diagnostic package for the degeneracy shortcut, accompanied by a narrowly delimited trefoil source check. Strongest newly verified preparatory fact: source identities, typed receipt counts and cross-referenced hashes are structurally consistent, while source/prior/native representations have the precise distinctions below. No new mathematical PASS is issued.

The route is stopped at the exact missing mechanism: prove vanishing of all relevant normal deformation cohomology under the full SU(2)-abelian hypothesis, or control actual degenerate Chern–Simons local Floer contributions and differentials without this vanishing. Simply identifying the ordinary representation-set homology transfers the central difficulty into an unsupported stronger assertion. It may be reopened only with materially new structure/evidence.

## Ledger, prior report, and original attribution

`turns.json` is a complete **JSON object**, not JSONL. It records `count=1`, a one-entry attempts array, one unresolved route, and the exact artifact hash. `readiness.json` records maximum5 substantive attempts, used1, historical start/deadline and author model `gpt-6-astra` at `xhigh`. Those model/runtime fields and the September30 completion estimate10% are historical attribution only. New substantive attempts by this preparer:0.

The original `source_record.json` is the plain selected problem, not a wrapper from `queue.py show`. It exactly matches numeric ID2849 in the in-place raw problem cache and the read-only SQLite selected payload. Source statement SHA-256 is `188f17358a3473bb923cea166ac35ba16f5fa503641f207cdaf5852ba8f1621b`.

Original `prior_report.json` is literal `null` plus newline. **That is not evidence that an upstream report key exists.** In actual in-place `cache/research_results.json`, `KP-3.51` is **ABSENT**; read-only SQLite stores the queue import's absent-report default `{}` (literal2 bytes, SHA-256 `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`). `queue.py sync` uses `reports.get(problem_number,{})` and `queue.py show` wraps parsed problem/report as `problem` / `prior_research`. The original-null packaging differs from the actual absent/default representation. The actual source review hash comes from `[problem,{}]`, matching readiness, selected catalog and assessment: `75fc89712b85944d60898e4411f4c6017ed9d911f6c21b9d1ffeda1fc8dd5b36`. No report was invented or converted into a present-null report.

The first inspector assumed null equivalence and failed; full stdout/stderr, actual PID and exit1 remain preserved. `inspect_original_v2.py` records the actual ABSENT/default distinction and succeeded. Separately, the adapted export template's substring selection initially matched incidental ID digits inside unrelated catalog hashes. The exact-ID correction records prior/corrected hashes and removed IDs in `ORIGINAL_SELECTION_CORRECTION.json`, preserves the original operator source, and retains only problem2849 selected bodies. This is a disclosed preparation correction, not a scientific revision.

## Complete personal reading and typed inspection

The preparer personally read every unique original mathematical/prose/helper source and all complete original JSON receipts. The scientific files are four prose files (`OBSTRUCTION.md`, `README.md`, `RESEARCH_LOG.md`, `review/REVIEW.md`), three helper files (`verify.py`, `review/submitted_verify.py`, `review/independent_checks.py`), and nine JSON files (`prior_report.json`, `readiness.json`, `source_checksums.json`, `source_record.json`, `turns.json`, `verification.json`, `review/independent_results.json`, `review/submitted_results.json`, `review/verdict.json`). The first two helpers are byte-identical; their complete bodies were read as text. Nothing in these helpers was imported, compiled or executed.

The complete whole diff was byte-read and all16 added-file hunks reconstructed byte-exact against the exported files. The one queue hunk was personally read. The nine JSON bodies were parsed with duplicate-key and nonfinite-token rejection and are preserved in `ORIGINAL_COMPLETE_READ_RECEIPT.json`; there are no scientific JSONL receipt files. Every original author check label (114) and independent label/value (100) was read and structurally inspected. Original author receipt uses boolean `passed=true` plus `assertions=114`; independent receipt uses integer `passed=100`, `failed=0`, and100 `PASS` values. Reduced submitted results match the author receipt excluding checks. The receipt's six raw rank-one H1 dimensions are `[0,1,0,0,0,1]`, with all six squared dimensions zero. These are historical receipts, not fresh reproduction.

`OBSTRUCTION.md` SHA-256 `8822d3fb47154229752a40e3f3fcc22b09a823b653521da2344b26bc1a2d31d4` matches the attempt and verdict references. `review/REVIEW.md` SHA-256 `ae5a34685a49604c49ceb8f8c8500b10a78676fa9237a8975f5c029a23c73001` matches the verdict. Original verdict `PASS_UNRESOLVED_OBSTRUCTION_AND_NARROW_SOURCE_CHECK` and reviewer model/effort/date are historical attribution, not adopted current verdicts. The opening obstruction's review-pending text is older internal chronology; the frozen README and later review/log report review completion. Independent current review is PENDING.

Complete current `queue.py`, README, AGENTS, policy and related-target-group bodies were read as text/data. Native record counts and selected complete records, code/source hashes and raw-cache provenance were independently inspected without running queue commands. Whole foreign caches and native catalog corpora remain in place; they were hashed and selected by exact ID, not copied as corpus bodies into this archive.

## Original versus current native state

The original PR queue row says `unsolved`, `1/5`, while the PR-HEAD native catalog still says `queued`, turns0, and the PR-HEAD state has no2849 entry or selected history events. Original source data and historical ledger therefore need later native-mirror reconciliation if the partial is accepted; an old queue row must not be replayed over future main.

At the latest independent dated current read, main HEAD was **MAINHEAD**, read at **NATIVETIME**. Current selected queue row is queued0/5, selected catalog is queued with turns0, state key2849 is absent, selected history and assessment-history counts are both0. Global current counts are catalog15458, assessments15458, state35, history35 and assessment-history23. Selected statement/review hashes match the original selected source; this does not reconcile the historical turn automatically.

The canonical13 native/program inputs are each individually bound by whole actual bytes, SHA-256, full mode and timestamp in `original_native_input_bindings.json` and the later `ORIGINAL_CURRENT_NATIVE_SELECTED_READ.json`: program inventory; QUEUE, state, history, catalog, assessments, queue.py, policy, manifest, cache/problems, cache/research_results, cache/catalog.sqlite, and related_target_groups. Raw foreign caches remain ignored and in place. These bindings describe two actual dated observations only. They convey **no authority for future main**; other work concurrently changes main. No transition was made here.

## Primary-source priorities for the independent review

1. [K3 original problem, printed pp167–168](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf) and [upstream K3 link](https://aimath.org/pastworkshops/kirbylistrep.pdf): establish exact scope, authorship and version continuity.
2. [Baldwin–Sivek published paper](https://msp.org/gt/2018/22-7/gt-v22-n7-p13-p.pdf), §4.1, Propositions4.4–4.5/4.7 and Theorem4.6, printed pp4350–4357; [author version](https://www.ma.imperial.ac.uk/~ssivek/papers/stein_fillings.pdf): confirm precise cyclic-finiteness meaning, equivariance/Morse–Bott hypotheses, framed instanton conventions, Euler-characteristic and spectral-sequence bounds, and the square in surgery coefficients.
3. [Bascapè2608.20551v1](https://arxiv.org/abs/2608.20551v1), global conventions/§2 p3, Theorem3.5 p5, Definition5.3 and Corollary5.4/proof p9: authenticate applicable version/date and all exclusions, especially reducible and slope6 fillings; inspect later revisions separately.
4. [Sivek–Zentner surgery paper](https://spiral.imperial.ac.uk/server/api/core/bitstreams/31fba2ba-24ed-45cb-9374-dad47877adcc/content), Proposition4.3/proof p14: independently verify peripheral surgery convention and connected-sum/group identity.
5. [Li–Ye2511.17877v1](https://arxiv.org/abs/2511.17877v1), Lemma7.1 p32, and [Bascapè2408.16635v2](https://arxiv.org/abs/2408.16635v2), introductory criterion/Theorem1.5: verify numerator restrictions and distinction between framed instanton and Heegaard Floer conclusions.
6. Context credited in the original source: [Boyer–Nicas1990](https://doi.org/10.2307/2001712) and [Daemi–Iida–Scaduto rank-three paper](https://arxiv.org/abs/2402.10448), with exact relevance to SU(2) established before importing SU(3) evidence.

The original six PDF size/hash receipts and K3 hash/pages are individually retained as **unverified historical hash claims** in `ORIGINAL_FOREIGN_SOURCE_BINDINGS.json`. This preparation performed no fresh PDF download, OCR or rendered-page inspection. No raw foreign PDF/OCR/pixel/access-header/cookie/cache/SQLite/corpus body was copied here. Source chronology and status as of now remain unverified.

## Falsifiable verification plan and closure boundary

Independent families should first challenge materially distinct mechanisms: literal source/version/peripheral scope; group and squared local-system algebra; analytic/topological cone-pair diagnostic; and actual gauge-theoretic scope plus current literature. Adversaries should test degree/sign conventions, all characters including central ones, rational-homology and reducible boundary cases, off-diagonal square action, and the distinction between ordinary local groups and equivariant Floer contributions. Reproduce exact computations from freshly read source in an isolated writable work directory only after source/operator approval by the root audit. Runtime counters alone cannot authenticate source truth or instanton conclusions. The fixed scientific ledger remains1/5; an independent check cannot quietly add new unfinished proof-search turns.

The preparer will freeze only explicitly enumerated original-authorship root files and directory roots in `ORIGINAL_PREPARATION_MANIFEST.json`, recording exact topology, bytes, hashes and full permission modes. The manifest excludes itself from its file list. The outer closure CAP is a separate directory outside that enumerated authorship, written by the genuine operator only after the actual closure child exits; its completion is not circularly certified by the child manifest. Future root/family directories may coexist beside this closed original scope and are excluded from its authorship.

Preparation estimate at this authored checkpoint:95%; independent current mathematical/source validation:0%; original-target full discovery by this preparer:0%. These percentages are source preparation estimates, not a certification of the original historical10% estimate. Acceptance, mathematical PASS, current source priority and merge remain PENDING.
'''
    body=body.replace('MAINHEAD',native['observed_main_head']).replace('NATIVETIME',native['read_at_utc'])
    write('ORIGINAL_CLAIM_INVENTORY.md',body.encode())
    log=f'''# PR47 original source preparation research log

- 2026-10-03T04:10:27.089869+00:00 — Began actual GitHub metadata capture; pinned expected open draft HEAD/base. Preparation20%; independent current claim validation0%; no discovery claim.
- 2026-10-03T04:10:28.392792+00:00 — Exact head initially absent locally; actual git object query exit128 preserved with empty stdout. Fetch exact SHA completed at04:10:38.623159+00:00. Branch stayed main. Preparation30%; independent validation0%.
- 2026-10-03T04:12:19.716209+00:00 — Export child PID75836 completed literal16-file scientific snapshot and17-file whole diff; tree modes100644 and snapshot0444. Separately bound canonical13 actual native/program files at observed main5699688113d25839ae415002decfafa13f39a3b8. Preparation55%; independent validation0%.
- 2026-10-03T04:15:17.130177+00:00 — Inspection child PID78223 failed on the unproved assumption that original-null and selected native prior were equal. Actual SQLite uses{{}}, upstream KP-3.51 report key absent. Preserved failure streams/source; corrected assumption. Also disclosed/corrected substring native selection to exact ID. Preparation70%; independent validation0%.
- 2026-10-03T04:16:08.504685+00:00 — V2 child PID78706 completed strict full-byte/typed source inspection. Original ledger is JSON count1/5;9 JSON bodies, author114 and review100 historical labels inspected; no old helper execution. Current native queued0/5 with no selected state/history events; native mirror gap reserved for later root decision. Dated current main859a836402f92f3a78dd7aecd9199e973ab666fb has no future authority. Preparation85%; independent validation0%.
- {at} — Inventory authored by actual child PID{os.getpid()} after personal complete original math/prose/helper/receipt/ledger/source/code reading. Recorded strongest claimed result, exact degenerate Floer gap, primary source priorities and falsifiable verification plan. All historical PASS/model/runtime attributions remain historical. Preparation95%; independent current mathematical/source validation0%; full-target discovery0%; new substantive attempts0. Independent review and merge PENDING.
'''
    write('RESEARCH_LOG.md',log.encode())
    assert Path(__file__).read_bytes()==source
    print(json.dumps(dict(status='ORIGINAL_INVENTORY_AUTHORED_ONLY',created_utc=at,actual_pid=os.getpid(),original_files=len(snap['files']),source_preparation_percent=95,independent_claim_validation_percent=0,acceptance_verdict=None),sort_keys=True))
if __name__=='__main__':main()
