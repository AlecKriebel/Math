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
