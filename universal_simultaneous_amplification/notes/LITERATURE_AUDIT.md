# Narrow literature audit

**Audit date:** 2026-08-01
**Timing:** performed only after the strong-selection theorem had been derived,
independently recomputed, symbolically verified, and subjected to hostile
review.

## Scope and finding

The audit searched primary papers for universal dB amplification, strong
selection on weighted graphs, complete-support weightings, and simultaneous
Bd/dB amplification.  It found the following closest results.

1. Tkadlec, Pavlogiannis, Chatterjee, and Nowak (2020),
   [*Limits on amplifiers of natural selection under death-Birth updating*](https://doi.org/10.1371/journal.pcbi.1007494),
   prove that every **noncomplete** graph is eventually dB-suppressing.  Their
   theorem allows directed and/or weighted edges and gives an explicit
   threshold bound.  Crucially, the paper states that the only remaining
   possible universal amplifier is a weighted version of `K_n`, and its
   further-directions section asks whether such a universal amplifier exists.

2. Allen et al. (2020),
   [*Transient amplifiers of selection and reducers of fixation for death-Birth updating on graphs*](https://doi.org/10.1371/journal.pcbi.1007529),
   derive the dB weak-selection coefficient using coalescing random walks and
   exhibit transient weighted amplifiers.  This agrees with the independently
   derived weak-selection formulas in this repository and does not resolve the
   weighted-complete strong-selection case.

3. Svoboda, Joshi, Tkadlec, and Chatterjee (2024),
   [*Amplifiers of selection for the Moran process with both Birth-death and death-Birth updating*](https://doi.org/10.1371/journal.pcbi.1012008),
   construct weighted simultaneous amplifiers for the fixed interval
   `1 < r < 1.2`.  This establishes that simultaneous amplification is possible
   on bounded fitness intervals, while leaving the all-`r` question distinct.

Targeted searches through 2026-08-01 did not locate a primary source closing
the residual nonuniform weighted-complete case for finite undirected symmetric
loopless graphs.  The present theorem closes exactly that case:

\[
 \rho_{\rm dB}(K_n,r)-\rho_{\rm dB}(G,r)
 =\frac{1}{n^2(n-2)r}
 \sum_i\sum_{\substack{j<k\\j,k\ne i}}
 \frac{(w_{ij}-w_{ik})^2}{w_{ij}w_{ik}}+O(r^{-2}).
\]

Thus it strengthens the 2020 transience theorem within the undirected model
from “all noncomplete supports” to “all graphs other than a uniformly weighted
complete graph,” with a sharp equality certificate.

## Novelty caution

This was a narrow, query-driven audit rather than a systematic review of every
database, thesis, or unpublished manuscript.  The mathematical theorem is
independent of the audit; any novelty claim should retain the qualified phrase
“to the best of this audit.”

## Directed-hypothesis audit after the extension proof

This second audit was performed only after the directed complete-support
coefficient had been derived twice and checked by an independent exact
directed-state verifier.

The model and Theorem 1 of Tkadlec--Pavlogiannis--Chatterjee--Nowak use the
same source-to-target convention `w_uv`, exclude self-loops, allow directed
nonsymmetric nonnegative weights, initialize the single mutant uniformly, and
assume the support is strongly connected. Their theorem states eventual
strict dB suppression for every strongly connected noncomplete support and
even supplies the threshold `r* <= 2n^2`. Their normalization `w_uv in [0,1]`
does not restrict the present finite-weight model, since a global positive
rescaling leaves both update rules unchanged.

Thus the published theorem exactly supplies the strongly connected,
noncomplete branch. It does not cover supports that are not strongly
connected; `phase1_directed/non_strong_support_closure.md` gives a separate
first-principles proof for that branch. Complete directed support is
automatically strongly connected and is handled by the new incoming-column
sum-of-squares theorem.

Primary source checked: J. Tkadlec, A. Pavlogiannis, K. Chatterjee, and
M. A. Nowak, *Limits on amplifiers of natural selection under death--Birth
updating*, PLOS Computational Biology 16 (2020), e1007494,
doi:10.1371/journal.pcbi.1007494; arXiv:1906.02785.
