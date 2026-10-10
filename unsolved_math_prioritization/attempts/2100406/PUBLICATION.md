# Current reviewed disposition: 2100406

**Already solved, 0/5: credited Lazutkin literal negative for unrestricted convex-caustic rotation numbers; rational/resonant variants untouched.**

The full independent audit passes the exact literal target. Lazutkin's classical caustic-existence theorem applies to the explicit analytic nonellipse and supplies a positive-measure rotation set. Elementary compactness produces distinct convex caustics whose rotation numbers accumulate strictly between zero and one half.

## Reading order

1. [CERTIFICATE.md](CERTIFICATE.md): exact source identity, explicit nonellipse, classical theorem application, accumulation argument, and scope limits.
2. [SOURCE_AUDIT.md](SOURCE_AUDIT.md): version numbering, parameter measure, imported-citation corrections, and live-detail-page access limitation.
3. [Independent audit](independent_review_v1/AUDIT_REPORT.md): full literal-scope PASS, no blocking correction.
4. [Exact controls](verify_geometry.py), with [author output](GEOMETRY_CHECK.json) and [independent replay](independent_review_v1/GEOMETRY_RECHECK.json).

## Differentiability precision

In the frozen certificate, the classical input's word “smooth” can and should be read here as **sufficiently differentiable, for example C² convex caustics**. Fixing a finite regularity in Lazutkin's theorem is enough. The explicit table is analytic and satisfies every finite differentiability requirement. No assertion about one C-infinity family is needed or claimed. This is the nonblocking precision note in the independent audit; the mathematical certificate is retained unchanged.

## Credit and limitations

The decisive existence theorem belongs to V. F. Lazutkin (1973). This is a source-derived consequence, with no new-discovery, historical-priority, author-issued-erratum, or human-peer-review claim. The source sentence does not impose rational or resonant caustics. Nothing here settles such a strengthened version or infers what the proposer intended. A prescribed interior limit, an open foliation, the Birkhoff conjecture, and endpoint accumulation at one half are not asserted.

The literal question is Question3.10 in arXiv v1 and Question4.10 in arXiv v2 and the published article. The catalogue's Question4.6 label is incorrect. The exact live UnsolvedMath detail page could not be read successfully; the primary editions were verified.

## Frozen evidence and checks

- Certificate SHA-256: `4e47a382af31327e0d04b70f270000cf9ecd2a9ceedf4e6fc1d7d24b2703a3bf`
- Original author manifest: `1477830577f747618a6e083148c747d1873f0e77ca55d4146c345d59622a6810`
- Independent report: `48dbdb513dbde78e73384a3d7afec67587b2d1f63a2d22d2a44442652d4f5d63`
- Thirteen author exact geometry assertions and thirteen independent replay assertions PASS; these do not replace the classical theorem or infinite-sequence proof.

The original STATUS.json and pending-review prose are preserved historical records of the pre-review stage; this file and PUBLICATION_STATUS.json give the later reviewed disposition. Downloaded source PDFs, full extracted source texts, raw imports and private context are excluded. Only this target's QUEUE status and previously blank Findings cell change; 0/5 and all other rows/cells are preserved. Draft review only; no merge or release.

## Reproduce finite controls

Requires Python3 and SymPy. From this directory run `python3 verify_geometry.py` and compare the JSON with GEOMETRY_CHECK.json. The frozen output was produced with SymPy1.14.0. The complete proof is written in CERTIFICATE.md; computation verifies only the listed finite identities.
