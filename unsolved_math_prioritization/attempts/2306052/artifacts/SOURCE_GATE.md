# Source and prior-work gate

Checked 2026-10-03 UTC. This is a partial-results packet, not a solution announcement.

## Primary problem

- Catalogue locator: [2306052 / AMR-022-6052](https://www.unsolvedmath.com/problems/2306052).
- The web-reader request could not access the page. A direct HTTPS request returned HTTP 403. A previously pinned catalogue record was used only to identify the primary source; its generated conclusions were not treated as evidence.
- Primary source: W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, [arXiv:1809.07200v2](https://arxiv.org/abs/1809.07200v2), printed p. 137 / PDF leaf 138, Problem 6.52 and Update 6.52.
- The full problem and full accompanying update were read from extracted PDF text and checked against the rendered PDF page. The source has the unit disk D, a holomorphic function with range C, and an existential bounded univalent perturbation whose sum must also have range C. It attributes the question to L. A. Rubel.
- The 2018 update reports no progress received by the authors. It supplies no resolving proof. That historical statement does not certify present-day openness.

## Relevant theorem investigated and rejected as inapplicable

A. Eremenko, *Exceptional values in holomorphic families of entire functions*, [arXiv:math/0503750](https://arxiv.org/abs/math/0503750), 2005 preprint.

The complete proofs of Propositions 2 and 3 and Theorem 2, including the final meromorphic-extension lemma, were read. Proposition 2 concerns entire functions in the source variable; Theorem 2 additionally exploits the uniqueness of an omitted finite value supplied by Picard's theorem. The full supplied theorem proof runs through pluripolarity, continuity on bounded subsets, the graph theorem, and the meromorphic-extension argument. These hypotheses do not hold for an arbitrary function on the disk. No result from that paper is imported into the proof packet. Its deeper external dependencies were therefore not independently re-proved or represented as verified dependencies of this note.

The packet's positive lemmas and example are proved directly using the argument principle/Rouché theorem, elementary polynomial algebra, and elementary one-variable holomorphic facts. The script verifies auxiliary algebra only.

## Literature search scope

Exact-phrase and topic searches included Rubel with bounded univalent perturbations, the whole-plane range formulation, Problem 6.52, and holomorphic families with exceptional values. They located the historical problem list and the entire-source theorem above, but no directly applicable general resolution. This is a bounded search, not a comprehensive review or a novelty certificate.

## Actual prior repository checks

Read-only checks were made in [AlecKriebel/Math](https://github.com/AlecKriebel/Math) before drafting:

- All-state PR searches for `2306052`, `AMR-022-6052`, and `6.52` returned no matches.
- A broader `Rubel` PR search returned #369, #493, and #495. Their returned titles and full bodies concern Problems 2.55, 2.54, and 5.28 respectively, rather than this problem.
- Exact-ID branch and commit searches returned no matches.
- Default-branch code search for the exact ID returned no matches. Index searches alone are not assumed exhaustive.
- The actual root directory listing had no matching target directory. The `problems` directory listing and the 49-entry `unsolved_math_prioritization/attempts` directory listing contained no matching target ID.
- Full recursive tree requests for the repository and the prioritization subtree failed with a transport-closed error. No complete-tree coverage is claimed.
- The target queue row was separately read: rank 528, ID 2306052, status `queued`, turns `0/5`. That row was not used as proof of absence of earlier mathematical work.
- The repository's AGENTS.md was read. No remote write, merge, release, or external outreach was performed during this investigation.

These checks support “no matching prior attempt found in the inspected material,” not an exhaustive repository-history claim.

## Decision

Proposed disposition: `unsolved`, `5/5` substantive analytical attempts. The useful deliverable is an exact special-family classification, quantified bounded-perturbation stability, and precise failures of attempted general routes. The universal original claim remains neither proved nor disproved. Independent mathematical review is still required before publication.
