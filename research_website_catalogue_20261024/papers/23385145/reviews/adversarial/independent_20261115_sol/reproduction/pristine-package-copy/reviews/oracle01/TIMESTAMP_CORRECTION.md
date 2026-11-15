# Preserved timestamp correction

The source-first checkpoint and its first log entry used a manually estimated 04:15 UTC timestamp. This was erroneous. A tool clock immediately preceding the first candidate read returned 2026-10-15 04:10:08 UTC. The original checkpoint and its SHA256 were created in the preceding tool call, and thus predate 04:10:08 UTC. The file's filesystem birth/modification time is recorded below. The future-looking timestamp was not evidence of later source reconstruction, and no content of that sealed checkpoint has been rewritten. This correction is saved after candidate access.
Filesystem checkpoint birth: 2026-10-14T21:10:05Z; modification: 2026-10-14T21:10:05Z
Filesystem checkpoint birth (UTC): 2026-10-15T04:10:05Z; modification (UTC): 2026-10-15T04:10:05Z

The first filesystem line above was produced under America/Los_Angeles while its format mistakenly appended Z. It denotes 21:10:05 PDT on October 14, hence 04:10:05 UTC on October 15; the explicit TZ=UTC line is authoritative. This formatting correction is preserved rather than erasing the record.
