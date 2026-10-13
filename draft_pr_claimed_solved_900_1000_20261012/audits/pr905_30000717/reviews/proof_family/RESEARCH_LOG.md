# PR 905 proof-family research log

All timestamps are UTC. Completion estimates concern the independent mathematical audit, not a claim of historical novelty or formal certification. Work is confined to this directory. The supplied original snapshot is read-only for this review; no Git operations or external communication are authorized here.

## 2026-10-13T04:25:50Z — first reconstruction checkpoint — 40%

- Read the author theorem, its complete proof and source assessment, and the historical Audit A, epsilon supplement, frozen acceptance, Audit B and correction record. Historical acceptance is treated as evidence to test, not a premise.
- Exact target: every fixed real epsilon >= 0; arbitrary finite real polynomial SOS; ordinary radical or the larger real vanishing ideal; both explicitly defined tangency-minor and off-diagonal-product ideals.
- Reconstructed the zero-line boundedness argument, homogeneous decomposition, cubic injectivity and coordinate-axis growth contradiction. No circular dependency identified.
- Adversarial issues still to finish: exact independent arithmetic, determinant ordering, lower-degree injection, possible surviving degree-four components, representative-only versus whole-line distinction, boundary cases in sphere minimization, and the nonattaining literal-product diagnostic.
- The default Python lacks SymPy. Decision: use a dependency-free exact rational polynomial checker instead of modifying the environment or importing the author's scripts.

## 2026-10-13T04:29:15Z — exact arithmetic checkpoint — 75%

- Independently constructed the Robinson polynomial, derivative and both ideals; recovered the ten directions by filtering the 13 normalized nonzero cube directions. All line identities hold symbolically, not only at sampled parameters.
- The first exact run passed 111 controls: Schur identity and symmetries, derivatives and Euler identity, line and axis restrictions, ranks 1/3/6/10/10 in degrees 0 through 4, the author's ordered determinant -128, cubic-kernel identification, and the complete Q diagnostic arithmetic.
- Sharp boundary control: (x^2-y^2)(x^2+y^2-z^2) vanishes on all ten zero lines but equals t^4 on the extra axis. The final degree restriction cannot be omitted or extended uncritically to degree four.
- Representative-only control: (x-1)(y-1) vanishes at all ten normalized points but restricts to (t-1)^2 on one whole line. This blocks an unjustified separation of homogeneous parts based only on point evaluations.
- Independently derived an axis interpolation stencil using only the eight directions with x=1. It gives another exact route to the contradiction and is being added to the checker.
- No mathematical correction identified. The remaining work is the full adversarial report, replay/output consistency, and snapshot-preservation manifest.

## 2026-10-13T04:32:45Z — portability checkpoint — 90%

- At the parent reviewer's packaging request, the exact checker now recognizes a standalone root/original_packet layout before falling back to the supplied frozen layout. It checks explicit file existence and the fixed frozen PROOF.md hash before computing controls.
- The full checker now passes 133 controls: two input guards and 131 finite algebraic/interpolation checks. No original file was modified.
- The new interpolation proof uses only eight zero lines and the extra axis. The full ten-zero cubic argument remains valid; the independent stencil avoids relying on determinant acceptance.
- Adversarial report drafted with exact claim, complete universal argument, constants, high degrees, ordinary/real radicals, scope boundaries, sphere minimization, and Q nonattainment. No mathematical blocker found.

## 2026-10-13T04:35:08Z — final verification checkpoint — 100%

- Mathematical verdict: PASS for all frozen v2 claims under the explicitly defined J and K ideals. No requested correction or unresolved mathematical gap remains.
- Exact results reproduced byte-for-byte in normal Python, optimized Python and the requested standalone original_packet layout. The checker rejected altered-hash and missing-proof test inputs.
- The snapshot file set and all 30 hashes agree exactly with ORIGINAL_SNAPSHOT.json. Temporary test data was confined to this review directory and removed. No Git operation, external communication, source retrieval or publication occurred.
- Final artifacts: AUDIT.md, dependency-free check_exact.py, RESULTS.json, REPRODUCIBILITY.json, local verification/sealing utilities, this log and MANIFEST.json.
- Source-formula intended meaning and exhaustive historical priority are outside this family's conclusion. No novelty or formal-certification claim is promoted.

## 2026-10-13T04:38:07Z — packaging utility follow-up opened — 50% of follow-up; mathematical audit 100%

- Parent requested archive portability for the optional verify_review.py and seal_manifest.py utilities, preserving the prior seal as history. The requested archive has root/ORIGINAL_SNAPSHOT.json unchanged and root/original_packet.
- Preserved MANIFEST.json exactly as MANIFEST.before_portable_utilities.json (SHA256 86696eab579a25067e4e10fb8206dd7de5481093c4c4ad949af49043f26ee6dc).
- Adapted utility input comparison to strip the fixed candidate-path prefix from the snapshot table and select original_packet when present. Retained fixed anchors for the snapshot record, author proof, author manifest and public manifest.
- No mathematical change, original mutation or change to check_exact.py was made. Remaining follow-up: test both utilities on a disposable full-payload standalone archive and reseal current artifacts.

## 2026-10-13T04:39:38Z — packaging utility follow-up complete — 100%

- Both optional utilities passed in a disposable archive with all 30 original files under original_packet, the unchanged ORIGINAL_SNAPSHOT.json and no original workspace directory. Normalized input tables and all sealed artifact hashes matched.
- The updated workspace verification again checked all 30 original hashes, fixed proof/manifest/snapshot anchors, ordinary and optimized Python replay, and the portable checker layout. All 133 checker controls and RESULTS.json bytes remain unchanged.
- UTILITY_PORTABILITY.json records the full-archive test. Disposable test material was confined to this review folder and removed.
- Updated the report's utility portability instructions and resealed the current review, retaining the old seal as historical evidence. Mathematical verdict remains PASS with no unresolved gap.
