# PR23 independent primary-source and scope audit

**Verdict: mathematical/source PASS for an `already_solved` source-status correction in the interpreted whole-space and box-local blow-up setting; current draft scope metadata requires correction. No new theorem, paper, or DOI is justified.**

Reviewed exact head: `ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d`.
All 14 attempt files in the parent snapshot match the head and manifest byte-for-byte. This family's criterion was sealed before historical review or candidate code was consulted. The old PASS was treated as a claim to test.

## Exact target and positive coverage

The complete [OWR contribution](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1), pp.2247-2249, asks about the fixed symmetric-product line while explaining an already published blow-up proof. It neither labels this an open conjecture nor supplies a self-contained domain/regularity/conclusion. The imported `statement_verification` assertion of self-contained cleanup is therefore too strong. The PR identifies this deficiency rather than endorsing it.

The [published De Philippis-Rindler theorem](https://www.aimspress.com/aimspress-data/mine/2020/3/PDF/mine-02-03-018.pdf), Theorem 2.10, pp.399-402, genuinely covers signed scalar measures on R^d. Its complete proof and arXiv v1/v2 were read; the relevant published content matches v2. Earlier 2011 two-dimensional results and the two cited 2016 papers' relevant type/quantifier statements and dependencies were also read. The 2016 singular-polar and selected-good-blow-up results alone would not certify arbitrary signed coefficient classification. The 2020 theorem does.

The independent certificate reconstructs smooth necessity using compatibility equations in every dimension, supplies the nonorthogonal domain/codomain congruence, and checks collinear/nonunit/negative/zero/d=1 cases. It resolves the printed `a != +/-b` normalization ambiguity by the PR's correct independent/parallel split. It also supplies explicit connected Lipschitz nonconvex domains for which a single global profile representation fails, both independent and parallel. These controls show why the PR's global-domain caveat is essential and why that caveat does not leave a gap in its scoped R^d claim.

Strongest verified result: every sufficiently regular whole-space solution has the known indicated structure modulo a rigid motion, with the corresponding local structure on adapted boxes; the published theorem extends this to locally BD maps and signed scalar Radon measures. The original explanatory passage does not identify a surviving autonomous open problem. Exact remaining gap: any distinct arbitrary-domain global question would require a separately specified target and different formulation; it is not claimed settled. No relevant mathematical route is blocked or transferred to an unsupported central claim.

## Findings and precise locations

| ID | Severity | Location at reviewed head | Finding and repair |
| --- | --- | --- | --- |
| PS-1 | P2, current draft metadata | `unsolved_math_prioritization/attempts/30002145/PR_DRAFT.md:24`; `unsolved_math_prioritization/QUEUE.md:36` | Draft says only attempt files and no shared queue edits. Exact merge-base diff changes the selected queue row to `already_solved`. Refresh current PR scope prose to include that single row, while preserving the old audit and historical log bytes. This is not a mathematical flaw. |
| PS-2 | P2, deferred legacy durability | `unsolved_math_prioritization/state.json:1`; exact-head `history.jsonl` contains no selected-target event; `queue.py:158` and `queue.py:161`; current `assessments.json` selected numeric-ID record | Manually preserved QUEUE has the accepted scope, while legacy machine state has no disposition and the old desk assessment remains `candidate`. Generator logic would default the target to `queued`; generator was not run. Root reports the same legacy operational convention across accepted PRs, so this is a global persistence migration item, not a blocker to mathematical/source acceptance. Synchronize accepted disposition and evidence without regenerating the operational queue or changing historical desk priors. |
| PS-3 | P3, imported upstream defect preserved as evidence | `unsolved_math_prioritization/attempts/30002145/source_record.json:71` | The pinned record calls the cleanup self-contained although domain, regularity and requested conclusion remain unspecified. Preserve the immutable upstream bytes; annotate the accepted contextual interpretation and defect in current acceptance/source notes. `SOURCE_STATUS.md:9` and `SOURCE_STATUS.md:86` already give the required qualifications. |

The dated original statements of no shared edits in `provenance.json` (checked 2026-09-30 03:34 UTC) and the dated log are historical evidence. They must not be silently rewritten into present-tense claims. The presently presented PR scope sentence PS-1 is the concrete mismatch to repair. The old desk probabilities are historical planning assumptions; they do not supersede the new accepted source verdict and should not be erased merely to make metadata look uniform.

## Persistent-state repair recommendation for the parent

Do not invoke the existing `queue.py status` command during this migration: its final `rank(None)` call regenerates the operational queue and can replace its preserved custom columns and historical notes.

After the parent's accepted classification and only as a separately reviewed bookkeeping change, append an event for numeric ID `30002145` and mirror it in `state.json`. Use `status: already_solved`, `turns_used: 0`, the unchanged current source `review_hash` and `statement_hash`, a UTC timestamp, and a note explicitly limiting acceptance to this known whole-space/box-local source correction. Evidence should identify reviewed PR/head, acceptance artifact and its hash, primary Theorem 2.10 location/version/hash, independent audit artifact/hash, exact accepted claim, nonconvex-domain exclusion, and `new_discovery: false`. Preserve any pre-existing fields and budgets. Do not synthesize readiness, candidate-turn, verified-solved, or proof-attempt events.

The same state/history-only method can synchronize other accepted dispositions under their own artifacts. First validate every referenced hash and numeric identity and preserve the existing queue bytes, catalog bytes, policy, scores and historical assessments. Add a regression or dry-run check that the state overlay selects `already_solved` with 0/5 for this source hash; do not write generated outputs. A future generator migration must separately preserve the operational queue's extended columns and user-maintained history. No generator or shared mutation was performed by this family.

## Provenance and reproduction

`check_pinned_sources.py` verifies both corpus SHA-256/length values against the pinned revision `37e53eabe540fb458758e198be61634bd02ee008`. It finds one numeric-ID/code match, no normalized duplicate, no report value/key matching ID/code/title, and no related-target group entry. Semantic statement/title queries are listed precisely in the receipt; their limited scope is not a claim that all differently worded mathematical relatives have been ruled out. The preserved `source_record.json` is exactly the pinned record.

Both head-bound verifiers were copied into ignored scratch space and rerun successfully with SymPy 1.14.0: 8 original symbolic checks and 11 old independent checks. Outputs match the preserved receipts exactly. Failed initial runs due solely to absent SymPy in the default Python are retained; the dependency was installed only in this family's ignored temporary environment. The 10 new exact controls pass and are distinct domain/type/congruence tests. Their scope does not certify BD completeness by computation.

Receipts: `pinned_corpus_receipt.json`, `reproduction_receipts.json`, `source_domain_type_results.json`, `primary_version_check.json`, `download_receipts.json`. Proof/countercontrols: `SOURCE_DOMAIN_TYPE_CERTIFICATE.md`. The first-party manifest binds all retained audit artifacts; foreign PDFs, HTML, extracted text, diffs and renders remain under ignored `tmp/`.

Original proof budget: 0/5, corroborated by the selected queue row, zero-attempt ledger and empty selected state/history. No formal new-discovery validation lifecycle entry exists at head; the old symbolic/reviewer PASS artifacts remain evidence of source verification. This family used no substantive new proof-search response, contacted no outside person, changed no canonical file, and performed no git, PR, release or publication mutation.

Audit completion estimate: 100%. Novel-discovery completion estimate: 0%, because positive prior coverage is established.
