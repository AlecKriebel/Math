# Source, prior-work and scope audit

Checked 4 October 2026. Mathematical claims are in PROOF.md; a source's own
claim of successful AI audits is not an independent proof certificate.

## Original problem

- Numeric upstream ID 2305055; problem code AMR-022-5055; queue rank 576.
- Requested [numeric catalogue page](https://www.unsolvedmath.com/problems/2305055)
  was inaccessible via the browsing tool. The corresponding code-form URL
  returned 403. Neither response was treated as mathematical evidence.
- The full statement was checked in Hayman–Lingham,
  [arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), printed p. 106
  (PDF page 107). The rendered page confirms both the ordering (f,alpha) and
  the general-domain addendum. The adjacent no-progress update in this draft
  is printed as **Update 5.56**, an editorial numbering mismatch; it is not
  silently cited as a correctly labeled Update 5.55.
- Historical source: Anderson, Barth and Brannan, *Research Problems in
  Complex Analysis*, Bulletin LMS 9 (1977), 129–162,
  [doi:10.1112/blms/9.2.129](https://doi.org/10.1112/blms/9.2.129).
  Publisher metadata and an indexed scan identify Rubel's Problem 5.55.
- The imported prior research report merely reports an unsuccessful literature
  search and leaves the conjecture open. It contains no proof to adopt.

## Prior public proposed resolution

DannyExperiments, *Rubel's L-atoms on the disk and a several-variable
counterexample*, Version 2.1, release 1.0.0 (5 August 2026).

The checked repository commit is
`65b6668e63e7fa3aec7ff28e36396f0a59af2aa9`.
The [immutable manuscript](https://github.com/DannyExperiments/rubel-l-atoms/blob/65b6668e63e7fa3aec7ff28e36396f0a59af2aa9/paper/manuscript.tex)
has Git blob `9d41191691739f3c0fba1a877c26c5732ad281d0` and SHA-256
`d76a606d85f3de1a34990b13ded7587c2e4f72d393c3d442aad958d29578af87`.
The exact source bytes were checked, and §§2–5 were reconstructed directly.

Its source states that the manuscript is AI-assisted and has not received
human specialist review. Its partial Lean artifact covers abstract logic,
not the analytic existence theorem. Those limitations are retained here.
The source records DOI 10.5281/zenodo.21803853; direct DOI retrieval failed in
this check, so the DOI deposit itself is not independently verified here.
The immutable GitHub manuscript is the actually inspected proof source.

The prior manuscript's arbitrary-perturbation construction is valid for the
plane-domain specialization needed here. PROOF.md supplies its topology,
infinite tail and Rouché details explicitly. The disk theorem therefore has
verified prior mathematical content, even though neither journal acceptance
nor human peer review is claimed.

## Classical approximation background

Kalmes and Nieß, *Composition and differentiation operators and fast
approximation*, J. Approx. Theory 164 (2012), 57–76,
[doi:10.1016/j.jat.2011.09.007](https://doi.org/10.1016/j.jat.2011.09.007).
Lemma 2 on p. 4 of the [author manuscript](https://www.tu-chemnitz.de/mathematik/analysis/kalmes/Preprints/Composition_and_differentiation_operators_and_fast_approximation_manuscript.pdf)
was read directly. It gives approximation on disjoint compact islands with
connected complements that escape compact subsets of a plane domain. This
confirms established approximation background credited by the prior source.
Our full construction only invokes ordinary Runge approximation and Rouché,
with the necessary compact-set geometry proved explicitly.

## Planar-domain consequence and novelty limits

The prior manuscript explicitly asserts the result for bounded plane domains
and gives a general moderate-algebra criterion, while declining a geometric
classification for all unbounded domains. The separator in PROOF §5 gives
that classification for plane domains under compact-source escape. This is
an elementary consequence of the prior surjectivization mechanism, separately
identified here. Dated searches using L-atom, Rubel, univalence, plane domain
and unbounded-domain variants did not locate a competing explicit statement.
Negative search evidence does not establish originality; none is claimed.

The same original collection's Problem 2.56 concerns several variables and
credits Rubel with the one-variable entire-source result. This supplies prior
credit for the special case U=C. The present packet neither republishes nor
changes the disposition of the distinct several-variable problem.

## Repository duplication and queue scope

Read-only checks against AlecKriebel/Math main at
`bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b` found:

- own queue row: queued, 0/5;
- no own entry in state.json or in the main attempts directory listing;
- no hit for 2305055 in code search, PR search or branch-name search;
- no own target in the related-target groups file;
- title/number searches and a Rubel search produced no duplicate of this
  problem. Other Rubel problems have separate attempts and were not reused.

These are bounded search observations, not a guarantee about all inaccessible
or unindexed work. Any later publication must recheck the live repository.
Only the target row's Status and Turns are proposed to change, with a narrowly
scoped prior-credit Findings sentence only if separately approved. All other
queue cells and rows are outside this packet's scope.

Downloaded scholarly papers, full imported corpora, copied source manuscript
bytes and operational records are excluded from the public packet. Source
links, hashes, fresh mathematical exposition and reproducible controls remain.
