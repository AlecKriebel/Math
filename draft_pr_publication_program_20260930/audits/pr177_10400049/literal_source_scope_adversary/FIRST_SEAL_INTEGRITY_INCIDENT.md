# First-seal integrity incident: transparent qualification

Recorded 2026-10-12 15:54:37 UTC after ROOT's independent authentication reported a mismatch. This is an additive fresh record. Neither `FIRST_ASSESSMENT.md` nor `FIRST_INVENTORY.json` has been amended, replaced, or resealed. The scientific verdict is unchanged.

## Incident and responsibility

I updated `RESEARCH_LOG.md` after the true first inventory had pinned its bytes/hash/mode. That was my provenance error. The complete first payload cannot be described as continuously immutable or currently matching its first inventory. The update added post-seal checkpoints and changed the concluding paragraph; it did not change the mathematical/source-scope first assessment. I did not silently restore the original log in place.

At the first seal, `RESEARCH_LOG.md` had 2,343 bytes, SHA256 `45b27e87c99cf12ec7cf09774d4c2faf404b90b724c5e759771350d39b48eba1`, mode0644. After the update, it had 4,265 bytes, SHA256 `5f7366c5aacca39ca20f322e46a46615aedc86087eae697b20fe0ac645a5b072`, still mode0644. The changed body is preserved unchanged in `RESEARCH_LOG_POST_SEAL_CHANGED.md`, separately mode0444. The original changed-path body is retained too. No later body modification of any first-payload file is being performed.

## Exact recovery without a continuous-immutability claim

The initial log was recoverable from the recorded first writing operation and the unchanged original prefix. A separately named recovery, `RESEARCH_LOG_FIRST_SEAL_RECONSTRUCTED_AUTHENTICATED.md`, has exactly 2,343 bytes and SHA256 `45b27e87c99cf12ec7cf09774d4c2faf404b90b724c5e759771350d39b48eba1`, matching the original log entry in the immutable first inventory. It is mode0444. This authenticates its content as the pinned original; it does not pretend that the original path stayed immutable continuously.

An earlier manual recovery attempt, `RESEARCH_LOG_FIRST_SEAL_RECONSTRUCTED.md`, was 2,338 bytes with SHA256 `1d87ca18a13c4a16c715fb080a2b190211ec4fc17d2db8b029a53ce2d25b949e`; it failed the pinned receipt because I miscopied a five-byte-longer phrase. That failed attempt remains retained and is excluded from the final safe-public allowlist. It is not presented as authenticated evidence.

`incident_validation.py` explicitly compared every one of the 23 first-payload files using normalized octal modes before late protection. Only `RESEARCH_LOG.md` differed, and only in bytes/hash; its current mode then still matched the pinned0644. The utility separately authenticated the first scientific note and first inventory against their original externally reported bytes/hash/mode, authenticated the named recovered log against the first inventory, and checked the preserved changed log as an exact copy. Normal and optimized executions both succeeded; their clean receipts are `INCIDENT_VALIDATION_NORMAL.json` and `INCIDENT_VALIDATION_OPTIMIZED.json`. The status deliberately says this is a documented authenticated incident, not an intact continuously immutable first tree.

## Physical-freezing limitation and late protection

The first inventory itself was mode0444, and `FIRST_ASSESSMENT.md` was mode0444. The inventory correctly records that its other 22 payload files were mode0644. Thus it did **not** establish physical read-only protection of the complete first payload. Calling the assessment/envelope sealed was accurate, but describing the entire first payload as physically frozen would be inaccurate.

ROOT separately reported that an initial comparison of string forms such as `0o444` and `0444` had produced spurious mode differences. ROOT will preserve that failed observation and perform a normalized comparison. This note does not use string-format differences as evidence of file mutation; the actual log-byte/hash change remains real.

ROOT's latest instruction requests a fully frozen final snapshot and explicitly permits writable-to-readonly changes if disclosed as **late protection**. The final inventory operation will therefore make every retained file mode0444, including the 22 first-payload files whose pinned original mode is0644. These mode changes occur after the first seal and after this incident; they are not continuous first freezing. Their bodies are preserved exactly as currently retained. The final manifest records final actual bytes/hashes/modes, including the unchanged first scientific note/envelope, the changed original log, exact separately authenticated recovery, failed recovery, and all private sources/renders/headers/code.

The final manifest's own hash is reported as a detached receipt to ROOT, since self-hashing inside a manifest would be circular. Whole-file-tree and byte/hash/mode validation will be run in normal and optimized modes after that late freeze. No file will be added or changed afterward within the frozen folder.

## Effect on the scientific claim

The authentic independent `FIRST_ASSESSMENT.md` remains 16,676 bytes, SHA256 `9a08ebd2cf58b526ed3efb62caf637b3ec9db99b7d24b9cf1c676023f2e5b62a`, mode0444. The true first `FIRST_INVENTORY.json` remains 4,773 bytes, SHA256 `e5a71d680b23efe02d3a1a9a7edc3059067f63fa4e4c6ba755595e68f11f601c`, mode0444. Independent source reading and source-scope reasoning remain first-seal evidence. This incident concerns audit provenance and must accompany any package that uses the first records. It does not identify a mathematical gap or authorize promotion.

At discovery, narrow deliverable completion estimate decreased from98% to90% for incident handling. After documented recovery and before final late freezing it is98%; successful final verification marks this narrow family100%. Case completion remains15%, with no mathematical/priority/publication clearance. No historical search, external-person contact, Git/index/ref/checkout/PR/publishing/tracker action occurred.
