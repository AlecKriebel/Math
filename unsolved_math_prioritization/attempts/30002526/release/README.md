# Corrected partial-results packet: Whitney umbrellas

Problem 30002526 / OWR-12869-003. **Unsolved after five approaches.** No full resolution, counterexample group, verified prior resolution, or novelty claim is made.

The independent audit accepted the elementary partial results subject to two wording corrections, now applied exactly as supplied:

1. The local birational obstruction requires a **proper birational modification** preserving the normal-crossing locus. It is not an assertion about unrestricted birational morphisms.
2. A covering **need not preserve** the fundamental group. Nontrivial covers do not always change its abstract isomorphism type.

The corrected content is in `current/`. Only `PROOF.md` and `SOURCES.md` changed, together with their regenerated checksum file. The original author code and all mathematical control outputs are unchanged. The five-approach count and unresolved construction gap remain unchanged.

## Contents and provenance

- `current/`: corrected author packet
- `original-author/`: every frozen author file, preserved byte-for-byte
- `audit/`: complete independent audit, preserved byte-for-byte, including its originally unapplied correction patch
- `CORRECTION.diff`: the reviewer's exact patch, now applied to `current/`
- `CORRECTION_LEDGER.json`: before/after hashes and correction scope
- `author_replay.json`, `independent_replay.json`: deterministic control replays
- `verify_release.py`, `verification_results.json`: preservation, exact-diff and replay checks
- `MANIFEST.json`, `SHA256SUMS`: binding of the complete safe packet

The preserved author log and audit describe their original preparation stages. They are historical records, not updated claims that the corrections remain unapplied. At preparation of this packet, the original reviewer's binding of this exact corrected release is pending.

## Reproduce

Python 3 standard library only, with no network calls:

    python3 verify_release.py

This verifies package and nested checksums; reconstructs the exact two-file diff; checks that all other author files are unchanged; reruns the original and corrected author controls (506 assertions each); and reruns the independent audit (93 assertions, plus its original-author binding). The printed JSON should match `verification_results.json`. An optional `--output /tmp/whitney-release-rerun.json` writes a separate copy.

The principal mathematical gap is an arbitrary-group, projective NC self-gluing construction on a connected normalization with verified local rings, ample descent, and a complete fundamental-group calculation. The controls do not fill that gap.

The literature caveat is unchanged: two official 2016 seminar announcements claim a stronger theorem, but a full proof was not verified; the author's dated 2019 statement retains Whitney umbrellas. This packet neither certifies `already_solved` nor asserts categorical current-literature openness.

No source PDFs, full source text, imported corpora, or private coordination inventories are included. No remote write, merge, release, DOI creation or outreach was performed in preparing this packet.
