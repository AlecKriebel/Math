# Audit corrections and supplements

## C1. Exact-file-set guard, required correction

The original author's `manifest_controls` gathers only entries for which `Path.is_file()` is true, then separately rejects directories. An unlisted dangling symlink satisfies neither test, so it is missed. A copied packet with such an additional entry returns PASS. This contradicts the blanket claim that every extra symbolic link is rejected. Similar special entries must also be considered.

No unexpected entry was found in the frozen author ZIP or in the original public directory. The mathematical arguments and the recorded byte hashes are unaffected. The author files have deliberately not been edited.

The independent `verify_audit.py` is the authoritative packaging guard for this combined delivery. It enumerates every entry, uses `lstat`, rejects links and special entries before reading, checks the exact recursively declared file and directory sets, and verifies byte counts and hashes against an externally trusted manifest digest. Nine regression cases cover changed and missing files, extra files/directories, dangling/file/directory symlinks, a FIFO and a wrong trusted digest. Its author-replay mode reproduces the original defect and verifies that the new guard rejects it.

This correction supersedes the original README and VALIDATION prose wherever they claim the original verifier rejects every extra symbolic link or guarantees the exact set of all filesystem entries. Use the stricter guard rather than treating the old integrity claim as unconditional.

## S1. Review-hash provenance completed

The original source metadata accurately said its catalog review hash was retained rather than recomputed. This audit recomputes it using the complete selected problem record and the absent-research default `{}`, with Python's `json.dumps([problem, research], sort_keys=True)` and the default separators and ASCII handling. It matches the catalog. This is a new verification supplement, not evidence that the earlier claim was false.

## S2. Bibliographic precision

The OWR volume/report year is 2024 and the publisher's publication date is 14 February 2025. In the inspected Batanin-Markl arXiv v1, item 104 is labeled a corollary, although the source's following text itself calls it a theorem. Neither detail changes the mathematical assessment.

No correction to the five scoped mathematical propositions is required. No E3 solution or target counterexample is accepted.
