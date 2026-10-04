# Acceptance of the corrected Whitney umbrella packet

Problem 30002526 / OWR-12869-003, rank 625. Binding continuation of the original independent audit, checked 4 October 2026.

**Accept the corrected partial-results release identified below. Both audit corrections are closed.** This acceptance is confined to the elementary partial results and the exact corrected packet. The universal irreducible NC projective surface realization target remains unsolved in this investigation after five approaches. No new proof search, full solution, counterexample group, verified prior resolution, or novelty claim is certified.

## Exact release binding

- MANIFEST.json SHA-256: `66e5c688379a999bb99edef5c1b48e14484a47c3f8d5893ef8776eb747013b98`
- SHA256SUMS SHA-256: `0fa0e7e0a6798edd82986626ddad5a3ade3c0617d33f04166ea3e7da7c208e76`
- CORRECTION.diff SHA-256: `04e69a8ad6206071e2e4226c19950c2eb60d57dfa941fe26a97426ca14e7297d`

The release contains exactly 36 ordinary files, with no symlinks, special files, source PDFs/full text, imported corpora, or private coordination inventories. All manifest sizes and hashes and all outer and nested checksums pass. Its eight original-author files and eleven audit files are byte-identical to the independently reviewed originals.

## Correction closure

C1 is closed. PROOF.md and SOURCES.md now explicitly restrict the Bierstone–Milman obstruction to a proper birational modification preserving the NC locus, with Question 1.2 and Example 1.7 identified.

C2 is closed. PROOF.md now says that a covering need not preserve the fundamental group and requires a separate preservation argument. It no longer asserts that every covering changes the abstract group.

The two content changes reproduce the reviewer's proposed patch byte-for-byte. Only current/PROOF.md, current/SOURCES.md, and the regenerated current/SHA256SUMS differ from the author freeze. The correction ledger correctly records all before/after hashes and unchanged files.

## Status and controls

The original and corrected author programs each replay the same 506 assertions. The independent audit replays the same 93 assertions with its original-author binding. Both saved outputs are byte-identical to fresh runs. The release verifier's output also exactly matches its saved verification result.

The five-approach count, unresolved construction gap, and 2016/2019 literature caveat are unchanged. The stronger official seminar announcements have not been promoted into a verified prior proof, and no categorical assertion of current-literature openness is certified.

The release's retained audit and author preparation statements are historical. In particular, its pending-binding fields describe the state before this separate supplement was issued. This supplement supplies the original reviewer's acceptance for the exact hashes above without altering those frozen records. Any later release modification requires a new binding or an explicit additional review.

## Reproduction and preservation

Place this supplement beside the bound release directory and run `python3 verify_binding.py`, or pass `--release-dir` explicitly. The JSON output should match verification_results.json. The script checks the bound files, correction closure, status, ledger and replays, and confirms that the release inventory and bytes remain unchanged during verification.

This continuation made no edits to the release, no remote writes, no external communications, and used no additional agents. It is a correction-binding check, not another substantive mathematical approach.
