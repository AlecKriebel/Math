# 30001696: ball-product structure of B(i,d)

**Complete candidate; independent adversarial AI review passed. AI-assisted and unrefereed.**
Historical priority has not been established.

The exact proposed conclusion is a PL homeomorphism
`|B(i,d)| ≅ S^i × D^(d-i-1)` for every `d ≥ 2`, `0 ≤ i ≤ d-2`,
with the whole-sphere endpoint handled separately. This is the full
ball-product question in Oberwolfach Report 08/2011, Question 4, p. 372.

## Artifacts

- [PROOF.md](PROOF.md): complete argument with zero-sensitive sign variation,
  a totally positive spectral flow, a continuous hitting graph, an identity
  cutoff near the attracting sphere, and a semialgebraic-to-PL upgrade
- [SOURCE_AUDIT.md](SOURCE_AUDIT.md): original scope, prior work, duplicate gate,
  and limits of the historical-priority search
- [RESEARCH_LOG.md](RESEARCH_LOG.md): timestamped progress and proof-attempt count
- [attempt.json](attempt.json): machine-readable scope and model metadata
- [source_provenance.json](source_provenance.json): primary URLs and downloaded
  PDF hashes; copyrighted source PDFs are not redistributed
- [verify.py](verify.py), [verification.json](verification.json): bounded exact
  algebraic/combinatorial diagnostics, not a formal proof certificate

## Reproduce the diagnostics

Run `python3 verify.py` from this directory. No third-party package is needed.
The program uses integer and rational arithmetic, checks small-dimensional
spectral identities and positive minors, all tested zero-sensitive sign
patterns, compound graphs, ratio inequalities, and cutoff inverses. These
finite tests supplement, and do not replace, the general proof.

The initial and final proof hashes and the independent adversarial review
are recorded in `review/`. The separate reviewer also passed 20,326 exact
assertions. No required mathematical corrections were identified.
