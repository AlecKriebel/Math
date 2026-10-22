# Independent early-sweep classification adversary

Review completed: 2026-10-21T01:20:49.357668+00:00.

## Verdict and scope

**PASS for PR9–96 classification and existing-publication coverage.** I found no eligible unpublished full-solution claim accidentally excluded in this interval, and no case that presently requires a new mathematical audit under the user's eligibility rules. This is a false-negative and publication-identity review, not a renewed certification of the old proofs or priority audits.

All **88** PR numbers from 9 through 96 are represented, with no gap or duplicate disposition. The retained inventory and a fresh live REST query agree on every scoped PR's head, description, title, state and draft flag: **49 merged, 39 open; 47 draft flags**. No closed PR occurs in this interval. All 88 PRs have a usable corresponding added/changed QUEUE row matched by the numeric problem identifier, its source alias and the attempt-folder path. Thus there is **no missing-status case** requiring independent full-claim inference in this interval. PR97 was deliberately excluded from this review.

The historical corresponding statuses are **51 unsolved, 18 already_solved, and 19 claimed_solved**. Of the latter 19, nine are already published and correctly recorded, and ten have explicit later matching canonical non-claimed classifications together with current PR descriptions that withdraw a new full-solution claim. The 79 nonpublication exclusions therefore follow the user's explicit status rule; no exclusion depends solely on a merged/open/draft label.

The canonical QUEUE snapshot is bound to remote main commit `9d7f5632c44fc73a78eeba37bacb2cd34f955cd4`, file SHA and SHA256 in `canonical_queue_receipt.json`. Fresh PR and Sheet capture times are retained in `prs_live.json` and `ledger_fresh.json`. This is snapshot evidence; later irreversible actions still require their normal fresh checks.

## Adversarial attempts to find a false negative

1. **Unrelated row mistaken for own status:** matched every own attempt-folder ID to an added row, then matched the exact canonical source alias. All 88 pass. PR22 has an additional explicit duplicate row, 20002052, but its own 20002011 row and disposition are correctly distinguished.
2. **Generic main queued row suppresses an absent-status claim:** 39 live canonical main rows remain `queued`. None was used as an exclusion. Their PR patches themselves supply matching explicit `unsolved` or `already_solved` statuses. An untouched queued main row could not supply an exclusion for a genuinely missing-status PR; no such case occurs here.
3. **Merged or draft label suppresses a full claim:** all 19 historical full claims were traced separately. Nine have exact existing publication coverage; the other ten have the specific current corrections below. In particular, merged draft PR50/57/80/85 were retained as publication matches, while merged draft PR55/65/66/73 were examined for their scientific disposition.
4. **Title-only publication match:** independently compared original source aliases, the result's objects, hypotheses and quantifiers, PR references, DOI, live abstract/description, and the main theorem in the deposited source. The source archives were read only for identity and scope, not for renewed proof work. All nine matches pass; narrower or neighboring targets remain explicitly qualified.
5. **Known broad target hides a potentially new narrower theorem:** PR36's degree-eleven construction, PR55's exact algorithm and PR73's connected example were specifically considered. They do not override the user's current explicit non-claimed status rule. PR55 explicitly leaves the full-source/bijection gap open; PR73 explicitly retains unresolved novelty/intended-target priority. Alternate-method novelty or a future successful priority audit would be a new basis for eligibility, not evidence that the present scan skipped a current full-resolution claim.
6. **Old approval labels treated as mathematical truth:** I did not transfer an old PASS into any fresh mathematical or priority conclusion. For exclusions I verified what result and status are currently asserted. No theorem is accepted or rejected here merely because a historical audit endorsed it.

## Ten superseded historical full claims

| PR | Exact problem | Current canonical status | Current claim and remaining limitation |
|---:|---|---|---|
| 11 | 30002867 / OWR-13678-008 | already_solved | Same global affine complete-intersection matrix-rank task; current description credits earlier equivalent methods and explicitly disclaims a new resolution. An earlier identical D2 display remains unlocated, which is not a present novelty claim. |
| 12 | 30005897 / OWR-14298367-003 | already_solved | Same full all-p shadowing/density result is presented as a derived corollary of earlier stronger scalar spectral machinery. The description explicitly creates no new paper/DOI and distinguishes other Banach and aggregate-mass questions. |
| 14 | 30005934 / OWR-14298374-003 | already_solved | Same noninteger positive trace-class Wishart obstruction is explicitly credited to an earlier anonymous DOI. Alpha zero and the source's N convention are expressly unresolved/qualified, so no broader novel full result survives. |
| 21 | 30001696 / OWR-4798-013 | already_solved | Same bounded-switch PL sphere–ball product is retained as a classical-priority correction, with no new original-problem resolution claimed. |
| 32 | 6800007 / AMR-067-0007 | already_solved | Same ordered-integrable-flag regular-homotopy classification is explicitly a credited prior-method application. Earlier exact printed coordinates remain unlocated; the current description does not convert that gap into novelty. |
| 36 | 20001424 / AIM-DYNAMICAL_SYSTEMS-0082 | already_solved | Same universal PCF field-of-moduli question is answered by an attributed prior cubic. The separate original degree-eleven graph remains preserved and its narrower priority is unestablished. |
| 55 | 30006309 / OWR-14299288-015 | already_solved | Scoped smooth complete very ample Delzant comparison is attributed to prior machinery; full-source arbitrary/sparse/singular scope, foundation-free claim and distinct bijection are expressly uncertified. The description explicitly says `full_source_solved=false`. |
| 65 | 2305051 / AMR-022-5051 | already_solved | Same normalized pure-Blaschke/Bloch target is credited to AAN1999 and the later problem-list update. The present PR expressly withdraws the new-resolution claim. |
| 66 | 10400033 / AMR-103-0033 | already_solved | Same original Willerton bound and even estimate are described as earlier-ingredient consequences. Alternate tournament-method priority and an earlier exact even formula remain unestablished, with no present new-resolution claim. |
| 73 | 2985 / KP-4.109 | partial | Connected genus-three quotient example is retained as an attributed theorem, but intended connectedness and novelty/target-priority remain unresolved. Canonical `partial` is explicit; no current full novel resolution or paper is claimed. |

These checks establish status and result identity. They do not independently prove the literature implications stated in the current descriptions; doing that would reopen substantively excluded PRs contrary to the requested status filter.

## Nine exact existing-publication matches

A new GWS CLI read found **exactly one matching DOI row** for each record, and the original problem alias and PR reference occur in that same row. Every live public Zenodo API record is `state=done`, `submitted=true`; every DOI GET resolves with HTTP200 to its intended record. All **41** public payload files were freshly downloaded. Their byte counts and MD5 hashes agree with both the live API and the sweep's previous receipts. Every ZIP passes CRC checks and includes manuscript source and verification code. The PDF/source/support file sets are unchanged. Titles, descriptions, creators, keywords, related identifiers, versions, DOIs and dates agree with the prior receipts; public API schema differences for preprint type and license normalize correctly.

| PR | DOI / Sheet row | Result identity and critical boundaries checked |
|---:|---|---|
| 9 | 10.5281/zenodo.23074543 / 11 | Exposed-point complex Zariski closure for every finite sum of ellipsoidal discs of rank at least two, without genericity/full dimensionality; distinct generic equality with the purely nonlinear part. |
| 16 | 10.5281/zenodo.23088066 / 12 | Finite two-dimensional complex with minimum PL dimension3 and original-simplex affine dimension5; first barycentric subdivision in R3. No enumerated enormous facet list is promised. |
| 18 | 10.5281/zenodo.23127955 / 14 | Spatial common-tangent union is outer null for three pairwise disjoint arbitrary convex subsets of R3, including nonclosed/unbounded/lower-dimensional cases. Conjecture4 is distinguished from stronger Conjecture3. |
| 50 | 10.5281/zenodo.23131001 / 18 | Ordinary oriented unframed classical/virtual closures through even-strand states; four/eight reversible algebraic scheme families and arbitrary word blocks. Historical priority remains expressly unresolved. |
| 57 | 10.5281/zenodo.23131374 / 19 | Every fixed finite integer r>=0, plane and sphere, normalized-map C^r-to-C^(r+1) discontinuity with smooth complete strictly positive-curvature metrics, including nonlinear r1 correction. No RP2/noninteger/abstract-homeomorphism extension. |
| 80 | 10.5281/zenodo.23147866 / 23 | Symmetric four-qubit W in the asymptotic local-unitary routing/receiver-LOCC model; per-sender9/8 rates and sum lower bound3/2+h2(1/4). No one-copy or optimal-capacity assertion. |
| 85 | 10.5281/zenodo.23153134 / 25 | Connected compact genus-three two-sheet covering example, zero dynamics, R17 observation, exact complete Gramian curvature-1/T and two-state ambiguity. No globally Euclidean/simply connected strengthening. |
| 91 | 10.5281/zenodo.23171212 / 27 | Closed unit ball of any finite-dimensional complex norm with a matrix contraction; mixed peripheral converse plus full point/operator spectrum classification. Existing special cases and classical decomposition are credited. |
| 95 | 10.5281/zenodo.23174156 / 28 | Ordinary full SU5, WZW5/shifted10; L(5,1), L(5,2) have the same Z/5 group and the exact unequal positive S3-normalized squares. Kuriya priority access gap and qualified historical status remain explicit. |

PR50 and PR95 are existing qualified publications with unresolved priority. They are correctly represented that way in the Sheet, metadata and deposited sources. This review does not promote them as newly verified novel open-problem resolutions; the user's already-published skip rule applies.

## Issues and recommended repairs

**No material false-negative or missing-publication issue found. No PR in9–96 needs to be reopened for a new mathematical audit on present evidence.**

There are three nonmaterial classification bookkeeping discrepancies: `current_classification` in dispositions for **PR15, PR25 and PR34** still says `unsolved`, whereas their present main rows and PR descriptions say `already_solved`. Both old and new statuses mandate exclusion, so this cannot lose an eligible solution. Recommended repair: retain the historical row status separately and update or qualify the field named current. For the 39 main rows still queued, keep the effective status explicitly sourced to the PR's own changed row rather than rewriting it to generic queued.

The initially pending PR9 publication-lead receipt is historically superseded by the completed GWS/disposition evidence and this independent live coverage check; preserve that time distinction rather than altering an old observation.

## Operational scope exception

While following the GWS skill's missing shared-reference prerequisite, I invoked `gws generate-skills --help` intending to inspect usage. The CLI unexpectedly treated this as generation and regenerated 96 Markdown skill/index files under repository-relative `skills/` and `docs/skills.md`. These paths are untracked; the skills directory itself predates this invocation. Their pre-invocation untracked contents were not captured, so I did **not** delete or automatically roll them back. No subsequent edits were made to those generated files. Exact observed paths, timestamps and hashes are retained in `GWS_GENERATION_INCIDENT.json`. This was an exception to the isolated-folder instruction and is reported explicitly. No scientific file, Git index/branch, PR, Zenodo record or Sheet was changed by this review.

## Replayable evidence

Run `python3 check_evidence.py` from any directory to replay the retained local range, binding, status-identity, ledger-uniqueness, metadata, file-digest and ZIP-integrity checks. The successful output is in `check_results.json`. Core evidence is in `classification_checks.json`, `scope_dispositions.json`, `scope_inventory.json`, `prs_live.json`, `canonical_queue.md`, `ledger_coverage_checks.json`, `ledger_fresh.json`, and the 88 copied `eligibility/prNNNN.json` inputs, and the nine `publication_prNNNN/` folders. Every scientific conclusion in this report is limited to classification and publication coverage. Review completion estimate: **100% of this assigned interval**.
