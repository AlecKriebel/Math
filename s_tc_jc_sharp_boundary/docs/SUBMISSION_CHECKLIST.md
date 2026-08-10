# Submission checklist

This checklist applies only to the sharpness manuscript
`Full-Dimensional Jukes--Cantor Ambiguity in Weakly Tree-Child Level-2
Networks`.  The quarantined positive-classification manuscript is not a
submission candidate.

## Mathematical gate

- [x] The theorem is restricted to `W_TC \ S_TC`; no result inside `S_TC` is
  claimed.
- [x] The four-leaf rooted graphs, narrow standard semi-directed reductions,
  five admissible LSA rootings, weak-but-not-strong classification,
  nonisomorphism, and non-`T`-equivalence were independently checked.
- [x] The common parameter point is exact and every edge multiplier and
  inheritance probability lies strictly in `(0,1)`.
- [x] Two implementations agree on all 256 Fourier coordinates; the
  independent implementation also checks all 256 inverse-Fourier pattern
  probabilities.
- [x] Exact nonzero rank-eight minors and the common irreducible
  eight-dimensional locus establish a regular full-dimensional stochastic
  overlap.
- [x] The cherry-substitution map has a positive real-analytic inverse and
  proves the theorem for every `n >= 4`, with dimension `2n`.
- [x] An adversarial mathematical review attempted convention, boundary,
  topology, dimension, and mutation failures.

## Reproducibility gate

- [x] `reproducibility/verify_primary.py` derives its Fourier maps from the
  rooted arc lists.
- [x] `reproducibility/independent/verify_sharpness.py` uses only the Python
  standard library and shares no implementation modules with the primary
  verifier.
- [x] The independent source, primitive instance, and canonical certificate
  are SHA-256 locked by the release driver.
- [x] The supplementary-code archive was extracted and replayed successfully.
- [x] The source archive was extracted and reproduced the distributed PDF
  byte for byte.
- [x] The archive builders are deterministic.
- [ ] Run `python3 reproducibility/verify_release.py` from the final committed
  tree and preserve its terminal result.

## Manuscript and public-material gate

- [x] One canonical LaTeX source builds one 10-page submission PDF.
- [x] Two consecutive Tectonic builds are byte-identical.
- [x] Every PDF page was rendered and visually inspected; all fonts are
  embedded.
- [x] Title, abstract, theorem, metadata, README, citation file, repository
  page, and supplementary package have the same scope.
- [x] The earlier positive manuscript, cover letters, referee guide, and
  verifiers are isolated under `quarantine/withdrawn_positive_v1.1.1/`.
- [x] The public paper page contains no hidden copy of the withdrawn theorem
  and no longer serves the withdrawn referee guide.
- [ ] Incorporate the final independent manuscript referee report.
- [ ] Generate and verify the final repository manifest after the last edit.
- [ ] Replay the complete gate in a clean Git worktree.

## Human submission fields

- [ ] Select a journal and adapt its formatting and disclosure requirements.
- [ ] Add any affiliation, correspondence email, ORCID, funding, conflict, and
  data-availability fields required by that journal.
- [ ] Confirm the exact author name and preferred citation metadata.
- [ ] Prepare a journal-specific cover letter only after those choices are
  made.
