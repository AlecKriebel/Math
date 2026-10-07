# Bounded readiness and source verification

Observed 7 October 2026 before writing the mathematical proof.

## Identity

Rank 953; problem 30005737; source code OWR-14298013-001; title “Post-Lie Structures with Semisimple Target.” The inspected queue row was queued, 0/5. It was not edited.

The exact intended scope is finite-dimensional complex Lie algebras on one vector space, with source g perfect nonsemisimple and target n semisimple. The primary OWR conjecture is at printed p.2689; the full paper's Sections 2–3 supply explicit dimensional and field conventions. The desired conclusion is nonexistence of a post-Lie structure, not the adjacent nilpotent-target question, nor the semisimple-source theorem, nor a claim in positive characteristic.

## Corpus identity and prior-attempt search

Both complete source files were read and their hashes freshly recomputed against the supplied provenance:

- problems.json: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf.
- research_results.json: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b.
- Provenance revision: 37e53eabe540fb458758e198be61634bd02ee008.

Exact ID/code lookup finds the problem record and no corresponding research report. Across the full problem corpus, normalized post-Lie spelling searches and the broader combination perfect + semisimple + Lie algebra identify only this problem. All 6,701 research-report entries were checked for post-Lie spellings and identifiers; none matched. Two broad perfect/semisimple/Lie-algebra report hits concern unrelated Shimura intersection and hyperkahler-confluence problems.

## Repository and draft-PR checks

Read-only checks on AlecKriebel/Math included:

- Default-branch code queries for post-Lie and 30005737: no returned matches.
- All-state PR queries for post-Lie, post Lie, perfect Lie, exact problem ID, and exact OWR code: no matching inherited attempt. A broader semisimple query returned unrelated group-spectrum, cohomology, TF-equivalence and classical-group records, which were not conflated with this target.
- Branch-name searches for 30005737 and post: no matches, with no continuation cursor.
- All 76 entries returned by the default-branch attempts directory, all 18 entries in the problems directory, and the default-branch root listing: no target or semantic-name match.
- A later read of main resolved to 6d575ea47761d5a3fda2cb0a63a9e6022d060496. The target queue row still read queued, 0/5.

This is a bounded readiness result. Two attempts to fetch the entire recursive repository tree returned a transport-closed error; no exhaustive all-branch/all-commit contents claim is made. Successful targeted searches and directory checks found no substantive inherited attempt. No branch, commit, PR, or queue write was performed.

## Current literature disposition

The 2024 primary paper presents the general perfect-source/semisimple-target case as conjectural and proves specified subclasses, recorded in SOURCES.md. Current bounded primary-source searches found no later general resolution. The candidate argument in PROOF.md is an authored proof attempt and has no historical novelty claim. Its independent mathematical acceptance is outside this readiness check.
