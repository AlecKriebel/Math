# Source and scope audit

Checked 2026-09-30, starting 03:29 UTC. This is a bounded research audit;
absence of a search hit is not evidence of first priority.

## Required first source and pinned record

The requested first source was attempted before mathematical research:
https://www.unsolvedmath.com/problems/30005897. The web reader could not open
it, and an ordinary HTTP request returned Vercel 403. No challenge or access
restriction was bypassed. The record was instead read from the authorized
repository's pinned upstream dataset, revision
`37e53eabe540fb458758e198be61634bd02ee008`.

The two full dataset files were supplied in a shared source cache and were
verified by the coordinating task against the repository manifest. This
attempt extracted the unique numeric record, checked that its problem code
has exactly one matching numeric ID, and found no research-results entry
for `OWR-14298367-003`. The complete selected record is preserved with
provenance metadata.

## Exact primary statement

Oberwolfach Report 19/2024, DOI
https://doi.org/10.4171/owr/2024/19, Martina Maiuriello's contribution
*Preserved dynamics: visualizing the connection between composition
operators and weighted shifts*, pp. 1078--1081, has two questions in Open
Problem (1), printed on p. 1080:

1. Whether the earlier shadowing characterization survives without bounded
   distortion
2. Whether generalized hyperbolicity remains equivalent to shadowing

The clean dataset statement isolates the second question. The proof package
does not silently conflate the two. The first is already answered negatively
in the July 2026 paper below; the proposed theorem addresses the second.

The report's full relevant contribution was read, including definitions and
standing hypotheses on pp. 1078--1080. In particular, the target is a bounded
invertible composition operator on Lp, `1 <= p < infinity`, over a sigma-finite
measure space, with a finite-positive-measure wandering generator. Generalized
hyperbolicity uses spectral radii of the restricted operators. Dissipativity
is not a claim that all arbitrary Banach-space operators are covered.

Readable original report PDF:
https://oa.tib.eu/renate/server/api/core/bitstreams/e2c61b25-148e-4b67-94db-93802821f4e1/content.

## Primary literature examined

### D'Aniello--Darji--Maiuriello, 2021

https://doi.org/10.1016/j.jde.2021.06.038;
https://arxiv.org/abs/2009.11526.

Read Definitions 2.3.1--2.3.2, Lemma 2.3.3, the generalized-hyperbolicity
definitions, the composition and dissipativity hypotheses in Sections
2.5--2.6, Definition 3.1.1, Theorems SS/SN, Corollaries SC/GH, the related
Radon--Nikodym criterion, and Problem 5.0.1. The full preprint PDF was
retrieved and retained outside the submission folder as a research source.
This paper proves the target with bounded distortion; it does not establish
the no-distortion theorem. Its aggregate conditions are not substituted for
pointwise densities in the candidate.

### Carvalho--Darji--Varandas, 2024

https://arxiv.org/abs/2407.20890;
https://www.cmup.pt/sites/default/files/2024-09/CDV-arxiv-2024.pdf.

Read Theorem 2.4, its full proof in Section 4.2, Corollary 2.16, and Question
5.1. The density-weighted representation of arbitrary dissipative composition
operators as shifts is known. The finite-dimensional-fiber result does not
visibly cover the arbitrary measure-space fibers used here. The candidate
credits the representation and claims no novelty for it.

### Bernardes--D'Aniello--Maiuriello, July 2026

https://arxiv.org/abs/2607.15831v1, submitted 17 July 2026.

Read the introduction and Section 6's Theorem 6.1 and Example 6.2 in full.
Example 6.2 refutes the extension of the old aggregate-mass criterion: HC
holds but shadowing fails. Its explicit pseudotrajectory argument was
checked. This is prior art, not this attempt's new counterexample.

### Pituk, August 2026

https://arxiv.org/abs/2608.19499v1, submitted 19 August 2026.

Read the full statements of Theorems A--C, the definitions, the right-resolvent
construction, and the nature of the Banach-space counterexample. Theorem B
already gives the equivalence on separable complex Hilbert spaces; that
covers the corresponding p=2 slice. The general Banach counterexample is
built using an uncomplemented-subspace/quotient mechanism and is not shown to
be a dissipative composition operator. It does not settle the remaining
target negatively.

### Messaoudi--Tofanin Neto--Saavedra--Tsokanos, August 2026

https://arxiv.org/abs/2608.17021v1, submitted 17 August 2026.

Inspected the introduction, definitions, principal statements, and general
Banach-space counterexample scope. Pseudo-hyperbolicity is explicitly not
treated as identical to generalized hyperbolicity. No claimed realization
of the counterexamples as the dissipative Lp composition operators in the
target was found.

### Additional current work and access limit

The 2026 paper *On the Dynamics of Weighted Composition Operators II*,
https://link.springer.com/article/10.1007/s00009-026-03136-w, Theorem 21,
was checked for its bounded-distortion hypothesis; its stated shadowing
transfer retains that hypothesis.

Dragičević--Pituk, *Duality between shadowing and uniform expansivity in
linear dynamics*, DOI https://doi.org/10.1090/tran/9879, is cited by Pituk
(2026). The publisher PDF request returned 403. The candidate independently
proves the necessary dual-expansion implication it needs, so this inaccessible
proof is not an unverified mathematical premise.

## Duplicate and previous-attempt gate

- Repository root AGENTS.md, queue AGENTS.md, README, policy.json, QUEUE.md,
  and the selected shortlist/individual desk review were read
- At the initial check the queue recorded 0/5 substantive turns and queued
  status for this numeric ID
- GitHub searches across all PR states for `30005897` and `Shadowing` found
  no matching previous research PR
- A branch search for `30005897` found none; CLI checks before branch
  creation repeated the PR and branch gate
- Repository source search found the selected desk note, but no previous
  mathematical attempt on this target; unrelated uses of the programming
  word shadowing were excluded
- The dataset was searched for shadowing/composition and exact-code matches;
  no duplicate of this numeric target was found
- `review_v2/related_target_groups.json` does not group this target with
  another one

These checks include closed/invalidated PR visibility, rather than inspecting
only currently open work. They cannot exclude unpublished or unindexed work.

## Result of the audit

The old scalar characterization is already refuted; the separable complex
p=2 equivalence is already in the literature. The broader dissipative
composition-operator equivalence for all `1 <= p < infinity` was not found
in the checked sources. The present complete proof candidate is therefore
eligible for independent verification, with historical priority explicitly
unresolved. No outside individual was contacted.

## 2026-10-01T13:42:24.142403+00:00 — current priority reconciliation supersedes original conclusion

The earlier paragraphs are the dated September 30 search. The subsequent
primary-scope audit confirms the exact second question at OWR p.1080 and the
finite positive wandering set assumptions. Two new priority families were
kept independent through their initial conclusions. The exact-question family
has bounded fulltext gaps. The equivalent-method family supplies a positive
full-scope derived corollary of Kitover--Orhon 2020v2 Theorem 2.26 (attributed
to Kitover 2011 Theorem 3.29), with independently checked transfer, clopen
uniform splitting, and primal norm identities. See PRIORITY_AUDIT.md for the
full certificate and the broader old equation (33) issue it avoids. The exact
older composition statement was not located; that does not create a novelty
clearance. Proposed current status is already_solved, known-method corollary,
with final acceptance review pending and no new preprint. No outreach occurred.
The uninspected 2011 proof and inaccessible current fulltexts remain explicit.

**Source-proof precision update:** the plain-shift cocycle countercheck in the historical falsifier report alone distinguishes operators, not their global norms. A broader allowed weighted-module example does falsify the printed norm identity, and a corrected operator relation can repair the growth estimate; the old spectral theorem is not refuted. See [the exact correction](https://github.com/AlecKriebel/Math/blob/main/draft_pr_publication_program_20260930/audits/pr12_30005897/ROOT_EQ33_PRECISION.md). The sufficient priority route remains independent of that identity.

## 2026-10-01T14:06:53.753458+00:00 — final acceptance

The fresh complete adversary passed the current proof and the qualified older stronger-result subsumption, including all endpoints and density condition. Earlier pending/proposed passages above are historical. Current QUEUE status is already_solved, credited derived corollary, with no earlier literal statement or first priority claimed. No paper, deposit or tracker row. See ACCEPTANCE.md.
