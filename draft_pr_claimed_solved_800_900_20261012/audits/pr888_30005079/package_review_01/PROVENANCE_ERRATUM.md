# Dated provenance erratum

2026-10-16 06:18:31 UTC; review completion estimate 97%.

The original source freeze says "06:05 UTC" and the original substantive math
freeze says "06:06 UTC". These were manually entered minute-resolution labels,
not independently sampled exact clock readings at their save instants. The
source label rounded forward. Both original full bodies are now restored
byte-for-byte to the original hashes recorded before any timestamp edit:

- source: 4605 bytes, d1fd0f54da2cd68357a1d1db1be2f9721343ba8b7d782a5cb4608b03e251eaea;
- math: 6417 bytes, dfb1a642e8b6658f837ee35e57599a8e52e164ac7c9e870e80f6d6c7e773805f.

At 06:15:16 UTC I recorded later-observed filesystem birthtime/mtime metadata:
source creation/save 06:04:36.783162 / 06:04:36.783308, math creation/save
06:06:28.582532 / 06:06:28.582669. These are **mutable filesystem metadata
observed later**, not immutable audit timestamps or direct clock observations
of the original save. FREEZE_TIMESTAMPS.json preserves exactly that evidence.
The original tool sequence and parent's earlier observations independently
support the ordering: source freeze before candidate proof, math freeze before
old verdict bodies. No greater timestamp certainty is claimed.

I briefly replaced those two prose labels with metadata-derived exact times
and added explanatory lines. No mathematical or substantive assessment text
changed. That was poor provenance handling: the freezes should stay frozen.
The original full bodies have been restored; this separate erratum supplies
the clock qualification instead. Their current post-restoration mtimes must
not be mistaken for original save metadata. The early research-log first two
entries also retain their original minute labels. A separately named early-log
reconstruction preserves the exact available first-two-entry text; it is
explicitly a reconstruction from retained text, not a previously saved original
file with an independently captured old hash. The parent also observed the
early freeze/log text before these changes.

The initial CLI collector ran eight cases and passed their guarded return-code
expectations, then failed on my final malformed expected archive-hash literal.
The first recovery path constructed CompletedProcess with the expected status.
Although reaching the later failure supports those statuses by control flow,
the recovered fields were not individually persisted direct process-status
records. They must be described as **guard-inferred**, not fresh/direct values.
The exact initial failed code, raw outputs and first recovered receipt are
preserved privately by pins. The collector is being repaired to run eight new
actual cases and immediately persist actual start/end/returncode before any
later validation assertion. Fresh and historical cases will be counted
separately. This concerns reviewer evidence only; no candidate defect or change
is implied.

Final evidence-repair checkpoint 2026-10-16T06:23:04.547748+00:00: all eight fresh actual cases passed. FRESH_PROCESS_RECORDS.json preserves their immediately persisted direct status records. Historical initial cases and qualified recovery remain separate and are not counted as fresh/direct evidence. The original freeze hashes are rechecked at finalization.
