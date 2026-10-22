# Independent finite ZIP format review plan

Frozen at 2026-10-15 12:18:44 UTC, before reading any prior review report or verdict and before loading or executing candidate code.

Scope: only the repaired verification-package format routines for PR883, under the parent-provided review root. This is a tools-only review, not either later whole-paper or whole-package reviewer. No candidate edits, source-input writes, corpus copies, Git mutations, network, publication, credentials, or communication with outside individuals.

## Exact target and success criteria

The target is that the pinned routines preserve exact input source bytes, accept their documented finite valid ZIP format, reject tested malformed ZIP members whose declared raw DEFLATE bytes are not exactly one fully consumed stream, construct deterministic ZIP output, and give the same validation decisions with ordinary Python and optimized Python. A CLEAR decision is limited to the tested code, source pins, and finite cases. It does not assert complete ZIP parser correctness or the mathematical validity of the paper.

Acceptance requires:

1. Fully read every candidate script and any imported project script before executing a review-local copy; verify the final parent-provided pins before and after checks.
2. Perform all Python execution with `-I -S -B`, and repeat meaningful diagnostics with `-O` added. Use only the standard library and inert local fixtures in review-owned directories.
3. Independently build ZIP byte fixtures rather than using candidate output as the validity oracle. A stored member and a raw-DEFLATE member must expose the exact expected bytes when valid. Empty raw-DEFLATE members must also be accepted where their surrounding format satisfies the documented contract.
4. Reject extra nonstream bytes inside a member's declared compressed size; reject an appended second raw-DEFLATE stream; reject truncations that preserve superficial header consistency; check both nonempty and empty member payloads. Include corruption of relevant declared lengths and checksums as the final source contract warrants.
5. Check that valid source extraction or archiving preserves byte identity, including binary bytes and line endings. Exercise a minimal publication-style fixture if the routines require one.
6. Rebuild the same finite input package independently at least twice and compare complete archive hashes and meaningful metadata against deterministic-construction claims.
7. Check the pinned original archives by the available read-only verification entry points as appropriate, record every actual command/result, and distinguish a source-format restriction from a member-consumption result.

## Independent mechanism

The fixture oracle will use explicit little-endian ZIP local headers, central directory records, and EOCD records, plus standard-library `zlib.compressobj(wbits=-15)`. It will record the raw compressed byte sequence and construct declared-size variants directly. For a valid raw stream `c` and expected plaintext `p`, independent consumption means one inflater reaches EOF, yields exactly `p`, and leaves no unused or unconsumed bytes. A verifier that checks only extracted `p` has not met this criterion.

The fixture suite will keep all data small. It will include an independently readable expected-byte table, mutation names, and actual ordinary/optimized results. The standard library's ZIP reader may be used for comparison of valid cases but will not decide malformed raw-stream validity.

## Adversarial checks and possible falsifiers

- A valid member is rejected solely because its output is empty.
- A byte suffix or second complete stream is silently ignored within the declared compressed size.
- A truncated stream yields the expected prefix and is accepted without EOF.
- A malformed member changes verdict under `-O`, indicating validation dependent on assertions.
- The final source hash differs from the announced pins or changes during review.
- Exact source bytes change during build, or the same build input produces different archive bytes.
- A finite expected rejection is merely caused by an unrelated metadata or policy violation, leaving stream consumption untested.

Each failing case will identify the first failed invariant and avoid overclaiming about an untested layer. Reproducible ISSUES blocks CLEAR until repaired and freshly pinned.

## Required review artifacts

`REPORT.md`, `DECISION.json` (CLEAR or ISSUES), a concise self-contained standard-library fixture, source and output SHA-256 pins, actual run transcripts or JSON, a research log with UTC timestamps and completion estimates, and `PUBLIC_MANIFEST.json` containing an explicit safe allowlist. Review-local copies and temporary fixtures will not be in the public allowlist unless needed and intentionally documented. No prior review report or verdict will be read before this plan and independent mechanism are frozen.

Checkpoint estimate: 10% of this finite format-review goal complete. Waiting for final repaired source pins is the sole dependency for execution.
