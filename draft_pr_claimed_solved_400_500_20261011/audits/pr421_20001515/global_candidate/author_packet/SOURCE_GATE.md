# Source and prior-attempt gate

Checked 2026-10-03 UTC. Rank 455; ID 20001515;
AIM-GEOMETRIC_GROUP_THEORY-0024.

**Post-audit update:** archived primary-source identity has now been verified
in two independently retrieved AIM captures, and the complete mathematical
audit returns PASS. See [VERIFICATION_ADDENDUM.md](VERIFICATION_ADDENDUM.md)
for both exact archive URLs, byte hashes, record identity and review scope.
The failed live-page checks below remain failed; the earlier provisional
source statements record the initial gate and are superseded only as to
archived source identity. Historical priority remains unverified.

## Exact scope

The catalogue title, *Fast monodromy and the cocompact cubulation bottleneck*,
describes a prior partial result. The target is the original AIM 5.2 question:
whether the mapping torus of the free-group automorphism
a -> a, b -> ab, c -> bcb acts properly and cocompactly on a CAT(0) cube
complex. The final b in bcb is positive.

## Provenance and live limitations

- The live GitHub QUEUE.md row was read as `queued`, `0/5`. Its file blob was
  `6367ebc85729ad0cd61af37aa0124554e4969a08`.
- The exact catalogue URL https://www.unsolvedmath.com/problems/20001515
  was attempted through web retrieval and then visited in the cloud browser.
  The latter returned `403 FORBIDDEN` and `This request was blocked`.
  No live catalogue statement is certified.
- The canonical http://aimpl.org/freebycyclic/5/ was attempted through web
  retrieval and visited in the cloud browser. It redirected to HTTPS and
  returned `502 Bad Gateway`, with a TLS certificate hostname mismatch.
  No certificate warning was bypassed. No current live AIM statement is
  certified.
- The exact formulation is therefore provisionally grounded in the supplied
  public UnsolvedMath snapshot, revision
  `37e53eabe540fb458758e198be61634bd02ee008`.
  The complete cached files' SHA-256 hashes were recomputed and matched:
  - problems.json:
    `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`
  - research_results.json:
    `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`
- The record identifies AIM Problem 5.2, attributed to Rylee Lyman, in
  *Rigidity properties of free-by-cyclic groups*. That attribution is
  snapshot evidence, not a successful live-page observation today.
- The official workshop report was successfully read at
  https://aimath.org/pastworkshops/freebycyclicrep.pdf . Its cubulation
  working-group paragraph on printed page 2 discusses b -> aba, c -> bcb,
  and a three-dimensional candidate. This is a genuine formula discrepancy.
  The current proof treats ab,bcb exactly, not the workshop's aba,bcb map.

## Genuine prior-attempt gate

The complete pinned research report for this precise slug was read, including
its proofs and limitations. It explicitly leaves geometric cubulation open.
It contains the sharp quadratic growth formula, fastness and the free cubical
action consequence, the two-stage cyclic HNN hierarchy, and a conditional
matched-convex-axis gluing criterion. Those are credited earlier work, not
new contributions of the present attempt.

This is not an already-resolved certificate and does not justify a zero-turn
completion. The new construction in ATTEMPT_1.md supplies actual finite local
isometries and a finite flag-link cube complex rather than assuming the
axis-matching condition. It is recorded as one substantive proof attempt.

Repository duplicate/history checks were also made:

- The main attempts directory was listed (45 directories); it contained no
  20001515 directory.
- The path-specific commits endpoint for
  unsolved_math_prioritization/attempts/20001515 returned an empty array.
- All-state issue/PR searches for 20001515, the exact slug, `cubulation`, and
  `monodromy` returned no matches.
- Branch searches for 20001515 and cubulation returned no matches.
- Default-branch code searches for 20001515 and bcb returned no matches.
- review_v2/related_target_groups.json was read (blob
  `b5cfa231ed6079c0f5021e1368c3b30a43100a10`); no 20001515 occurrence was found.

These are bounded repository checks, not a claim that every historical
private discussion or unpublished result has been searched.

Rank 454 / ID 20001506 was explicitly coordinated: it asks whether two
different exponentially growing free-by-cyclic groups are not quasi-isometric
(AIM 3.4). Its lamination-depth work and this cubulation target share workshop
context only. It is not counted as a duplicate proof attempt or discovery.

## Current primary-literature check

1. Hagen--Wise, *Cubulating mapping tori of some polynomial growth free group
   automorphisms*, https://arxiv.org/abs/1605.07879 and
   https://arxiv.org/html/1605.07879v3 . The latest version shown in the arXiv
   submission history is v3, 13 August 2025. The authors explicitly record a
   gap in the old version. Corollary 7.2 supplies free cubulation for fast
   automorphisms. The introduction defines this without metric properness,
   finite dimension or local finiteness. Questions 1.2--1.3 and Remark 6.10
   still discuss the cocompactness upgrade as a question/strategy. Our proof
   does not cite the superseded unrestricted theorem or assume that strategy.
2. Bongiovanni--Ghosh--Gültepe--Hagen, *Characterizing hierarchically hyperbolic
   free by cyclic groups*, https://arxiv.org/abs/2508.15738 and
   https://arxiv.org/html/2508.15738v3 . The latest arXiv version observed was
   v3, 15 May 2026. The unbranched/HHG/quasi-isometry characterization does not
   by itself produce the requested equivariant geometric cubulation.
3. Wu--Ye, *Some questions related to free-by-cyclic groups and tubular
   groups*, https://arxiv.org/abs/2504.14192 and
   https://arxiv.org/html/2504.14192v1 . The observed arXiv history contains
   v1, 19 April 2025. Its counterexamples concern the linear tubular family
   with both b and c modified by powers of a. That is not the present
   quadratic automorphism, in which c is modified by b.
4. The official AIM workshop report cited above acknowledges the nearby
   three-dimensional candidate. This is a reason to refrain from a
   historical-priority claim, even if the exact finite proof is accepted.

Focused searches by the exact words, AIM section, Lyman and cubulation did not
locate a published exact-target solution. Negative search results do not prove
novelty. No first-resolution claim is authorized by this ledger.

## Publication boundary

Only the original construction, the exact verification program/results, and
this short source ledger belong in the public packet. Downloaded papers,
raw corpus extracts, browser evidence, and unrelated repository/user context
remain excluded. The unavailable live source pages are disclosed rather than
treated as successfully verified. The fresh independent audit has subsequently
passed without mathematical repair; the final publication gate has authorized
a draft PR at claimed_solved, 1/5. These updates are detailed in the dated
addendum; they do not assert external peer review or historical priority.
