# Reviewed partial MTW research packet: start here

2026-10-03. Problem **30000997 / OWR-2042-006**, “Degenerate Versus Full Ma–Trudinger–Wang Conditions.” The original global question remains **unsolved, 5/5 author turns exhausted**. This draft records partial results with an independent AI-assisted mathematical audit; it is not external peer review or a novelty certification.

## Current reading order and review status

1. Read [CURRENT_READING_NOTE.md](CURRENT_READING_NOTE.md) first. Its normalization, off-cut-domain, uniqueness, numerical and prior-credit qualifications govern every historical mathematical file.
2. Read [CURRENT.md](CURRENT.md) for the corrected mathematical summary. Its “narrow re-review pending” wording records its frozen, pre-review state. That pending review has now been resolved by the version-bound [narrow PASS](audit/narrow/NARROW_REREVIEW.md) and [receipt](audit/narrow/NARROW_REREVIEW_RECEIPT.json).
3. Read [the full independent audit](audit/initial/INDEPENDENT_REVIEW.md) and [required corrections](audit/initial/CORRECTIONS.md), then TURN_1.md through TURN_5.md and the original summary as historical files governed by the current reading note.
4. [PUBLICATION_STATE.json](PUBLICATION_STATE.json) is the current administrative state. Earlier CURRENT_STATE.json and TURN_STATE.json remain frozen historical snapshots. The [publication manifest](PUBLICATION_MANIFEST.json) binds the complete public packet.

The narrow PASS is specifically bound to corrected commit `a9aca689e54f069b6618aeebef2e26c78fb36bbf`, corrected-manifest SHA-256 `725926f41e7fe58fb0a6607b3f1816a1fc35a07e0d2cb6a30822d9416eb6fe11`. All 38 files of that reviewed remote packet remain byte-for-byte unchanged. This publication adds only packaging and the exact six-file narrow-review packet; it adds no mathematical research turn.

## Scope of the retained result

For the smooth complete sphere with warp f(x)=cos x+(1/10)cos³x sin⁴x, the retained calculation proves positive Gaussian curvature, failure of full nonnegative cross-curvature at a specific equatorial pair, and strict null positivity on all non-antipodal equatorial pairs and on a sufficiently small product neighborhood of the displayed pair. It has **not** proved A3w throughout the whole off-cut-locus domain. It therefore supplies no global counterexample to the original implication.

For c=d_g²/2, the exact finite witness is S_packet=7/10−8/π²<0; Kim–McCann's convention gives cross_KM=2S_packet=7/5−16/π². Endpoint directions are obtained using Dexp. The source-Hessian identities for the actual squared distance require v inside the tangent injectivity domain, with the endpoint uniquely minimizing and nonconjugate. A selected geodesic branch alone is insufficient. The reading note proves equatorial uniqueness separately from nonconjugacy and qualifies every numerical flag.

The source question does not itself explicitly state completeness and the full off-cut-locus domain. Those hypotheses are explicit in the cited Kim–McCann formulation and are retained for the global interpretation; the restricted-domain interpretation and its local separation remain separately labeled. See [the source gate](PUBLIC_SOURCE_GATE.md) and the reading note. No CTIL, compactness, or small-neighborhood restriction has been silently inserted into the global target.

Credit for the Jacobi, angular MTW and surface-of-revolution machinery is due to Figalli–Rifford–Villani, *On the Ma–Trudinger–Wang curvature on surfaces*, §§2 and 6.1; the flat-product obstruction is due to Kim–McCann. Priority for these particular partial statements has not been established.

## Public packaging and reproducibility

This is an explicitly selected public packet, not a copy of the entire working directory. It includes public mathematical notes, diagnostic code and outputs, both mathematical audits, corrections, and public GitHub provenance. It excludes private search and coordination records, screenshots, third-party source PDFs and unrelated scratch files. The public source gate is a sanitized source/prior-gate summary; it is not represented as an exact copy of the private gate. No review report or frozen mathematical file has been redacted or rewritten in this packaging.

The original local TURN_STATE.json had 266 bytes and the remote version had 226 bytes. Both exact historical variants are retained under provenance/ and described in STATE_PROVENANCE.json; the public root TURN_STATE.json preserves the remote variant. Whole-directory local/remote identity is not claimed.

Run `python verify_publication.py` for read-only integrity/status validation. The exact algebra and independent controls remain supplied with their frozen receipts; these checks do not establish global A3w. Diagnostic shooting and finite differences have no minimization or interval certificate.

The queue change is limited to this pre-existing row's Status and Turns cells: `queued | 0/5` becomes `unsolved | 5/5`. Ranking, title, scores and link cells, other rows, generated state and historical review files remain unchanged. A draft PR is the publication vehicle; no merge or release is part of this packet.
