# Version 1.2.3 editorial-feedback audit

**Audit date:** 17 August 2026 (America/Los_Angeles)

**Scope:** adjudication of the final frontier-model review; primary-source
checks; proof-order and exposition review; release and rendering validation.

## Accepted changes

- Defined the exact Anderson--Cappelletti--Kim entropy-like function before
  quoting its Example 4.1 drift, eliminating ambiguity with the paper's own
  marked log-factorial potential. The definition and drift were checked
  against <https://arxiv.org/html/1904.08967>.
- Reordered the embedded-chain-to-CTMC proof so recurrent holding times first
  establish nonexplosion, after which Tonelli's theorem gives finite expected
  physical return time. This changes no hypothesis or conclusion.
- Added a qualified tier-lineage paragraph. It calls the normalized-log
  compactification a coarse tier-style encoding, does not attribute S-tiers
  to the 2011 deterministic papers, and identifies the carried-target identity
  and scalar envelope as the present proof's new ingredients. Primary records:
  <https://doi.org/10.1137/11082631X>,
  <https://doi.org/10.1137/17M1161427>, and
  <https://arxiv.org/abs/1808.05328>.
- Made the properness step literal by selecting states with potential above
  the sequence index.
- Updated release, literature-access, and material AI-use dates through 17
  August 2026. The live ConStRAINeD page still describes the two-dimensional
  proof as complete while listing the five-author manuscript as in preparation:
  <https://constrained.polito.it/publications/>.
- Corrected the Xu arXiv entry to its canonical 2024 publication year while
  retaining the official Version 2 title and 9 May 2026 revision note:
  <https://arxiv.org/abs/2409.05340>.
- Added the public recording of Daniele Cappelletti's 22 June 2022 Cornell
  talk as a second contemporaneous record of the four-person announcement,
  without calling it the earliest record. The Geneva program cited alongside
  it is dated 10 June 2022:
  <https://vod.video.cornell.edu/media/t/1_hn76x7n9/261126952>.
- Corrected the arXiv page-count metadata and current AI-use date, and refreshed
  the human-only bioRxiv and Zenodo operational checklists against their live
  official guidance.

## Suggestions not applied

- The invariant branches of the top-complex lemma were not removed or expanded.
  They remain mathematically useful, and the finite-set proof already states
  why they are impossible within one communicating class.
- No additional verifier-version warning was added: the README and reproduction
  record already state that outer release Version 1.2.3 carries the unchanged
  standalone verifier Version 1.2.0.

## Mathematical verdict

The theorem, hypotheses, marked-target identity, path recursion, scalar
envelope, top-complex trichotomy, Foster argument, trace conversion,
nonexplosion argument, and regenerative stationary law remain unchanged in
substance. No theorem-breaking defect was found in this review.

## Release validation

Local validation, deterministic artifact hashes, and the visual-PDF verdict
are recorded in the release manifest and reproduction record. Hosted main- and
tag-workflow validation is supplied by the release workflows after publication.
