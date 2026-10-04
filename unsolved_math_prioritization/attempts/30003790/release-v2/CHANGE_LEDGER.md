# Exact correction and status-supersession ledger

Version: corrected release v2, 4 October 2026. This file records corrections to an
author-created copy. It does not modify or replace the historical files.

## Immutable inputs

1. Original author manifest: `history/public/MANIFEST.json`, SHA256
   `a18df1c214a6ea7ed7aa14d8a038827f463a7c9ff4f069228e0eb68b247367d2`.
2. Original author result: `history/public/RESULT.md`, SHA256
   `0c63e1801d50434d217a8a66d16ea8bad27cac4867919f7532abc4819eb9dc16`.
3. First audit: `history/independent-audit/AUDIT.md`, SHA256
   `546d0d709f61a2f8e25e653a29606b7e7e6512ddabaeb811195057adc31e890b`.
4. Exact auxiliary theorem/proof: `history/independent-audit/AUXILIARY_CANDIDATE.md`
   and its identical copy `public/AUXILIARY_THEOREM.md`, SHA256
   `072aba944c908baf44bb86d6c9a3d1c87444b5f779c53a14b4a9648d9595351c`.
5. Fresh auxiliary audit: `history/auxiliary-independent-audit/AUDIT.md`, SHA256
   `954dedd9ec67d2819b211aa6cbb6f33cd578977175fb1478ede820aa3f4aab6f`.

Both audit packets and the original author packet retain their original manifests.
Only their manifest-listed distributable files and manifests are copied. No source
documents, page images, caches or private read inventories are included.

## Required corrections from the first audit

### C1: literal consistency versus a separately stronger rate objective

Corrected `public/RESULT.md` title, opening, Sections 1 and 7, plus its README,
readiness and manifest, now foreground conditional literal consistency. The source
question is not redefined to require a dimension-efficient rate. Conservative
`unsolved`, 5/5, now means unverified coverage of the underspecified source model.
`FINDINGS.md` states the affirmative bounded-model result explicitly.

The original five author turn entries are not rewritten. `public/turns.json` appends
a dated post-review assessment and explains that no additional author search turn
is being counted. The original log is retained below a clearly marked supersession
notice in its corrected copy; the exact original remains in history.

### C2: coordinate moments and normalized deconvolution estimates

Corrected `public/RESULT.md`, Section 3, requires `E||X||²<∞` for simultaneous
coordinate/second-moment identification. Its quantitative extension requires bounded
X or `E||X||⁴<∞`, and an L² density for each weighted measure. It states fixed-slice
positive-mass normalization using a positive denominator floor, convergence in
probability, and no automatic expectation bound for the ratio.

### C3: tangent nullspace is an interior, almost-everywhere assertion

The same section requires a unique interior closest-point projection, injective link,
finite conditional covariance and a rank-(D−1) spectral gap, interpreted for almost
every applicable clean level. Endpoint caps are explicitly excluded from that claim.

### C4: measurable, response-independent ranking

Corrected `public/RESULT.md`, Section 5B, requires a jointly measurable training-data/
covariate field, deterministic sample-index ties, all-candidate ranking and no use of
regression responses in field assignment or neighbor selection. It explicitly makes
the test point independent of the joint observed data. These clarifications do not
alter the original quantitative inequalities or proof mechanism.

### C5: auxiliary theorem review boundary

The first auditor's new candidate was not treated as independently reviewed at birth.
The separate fresh auxiliary audit subsequently accepted exactly the SHA256-bound
candidate above. That exact file is incorporated unchanged. Section 5A and FINDINGS
state the accepted complete model, all-n ranking, response-independent assignment,
common conditional second-moment bound and joint-test-independence interpretation.
No new theorem variation, stronger risk mode or new rate is claimed.

## Precise supersession of stale status language

- `history/public/RESULT.md` opening and Sections 1/7, and the corresponding original
  README/readiness/log, remain evidence of the author's earlier disposition. Their
  use of dimension-efficiency as the deciding source criterion is superseded by C1.
- Original `history/public/readiness.json` and `history/public/MANIFEST.json` retain
  `independent_review` / `independent_audit` pending language from their freeze. The
  original packet has now received the first audit, with scoped corrections. This
  does not mean the original uncorrected packet was accepted without qualifications.
- `history/independent-audit/AUDIT.md` opening, its README, manifest scope,
  `VERDICT.json` auxiliary status and C5, and the auxiliary candidate's own opening
  describe its then-current not-independently-audited status. That status, and only
  that chronology-dependent status, is superseded by the fresh auxiliary acceptance.
- `public/AUXILIARY_THEOREM.md` retains that same old banner because its entire
  accepted content is preserved byte-for-byte. Read its current review status via
  this ledger and the fresh auxiliary audit, not by silently editing the original.
- The fresh auxiliary audit accepts the exact theorem under its explicit standard
  joint-independence interpretation. It does not certify this corrected assembly,
  all source-model interpretations, originality, or dimension-efficient geometry.
- Current corrected-release binding status is **pending**. Mathematical auxiliary
  acceptance is established; publication authorization is not. No remote write is
  represented as having occurred.

## Exact edit evidence

`AUTHOR_V1_TO_CORRECTED_V2.diff` is the deterministic unified diff between
`history/public/` and `public/`, sorted by relative path, including added files and
the corrected manifest. `CHANGES.json` binds old/new bytes and hashes for each path
and maps these corrections to their affected files. `RELEASE_MANIFEST.json` binds
every distributed file in this version. `VERIFY_RELEASE.py` verifies all bindings,
reconstructs the exact diff, and replays both audits against the preserved inputs.

These changes supersede conclusions transparently; no historical statement, audit
result or frozen hash is silently rewritten.
