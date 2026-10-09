# A same-ground-set matroid-rank obstruction

## Accepted result and exact scope

There is no dimension-independent factor for two-sided approximation of every normalized, nonnegative, monotone submodular function by one ordinary matroid rank on the same finite ground set. This edition addresses problem 30004909 / OWR-8415356-020, from László Végh's contribution in Oberwolfach Report 53/2021, printed p. 2946 (PDF page 54).

For f(S)=sqrt(|S|) on n elements, every such factor obeys alpha >= n^(1/6). The optimal factor among all matroids is the minimum over integer ranks R of max(sqrt(R), sqrt(n)/R); uniform matroids attain it. In particular, the n^(1/6) bound is sharp when n is a cube. A rational-valued family on n=m² elements gives alpha²+alpha >= m and hence alpha >= n^(1/4)/sqrt(2).

Both families use one method: compare a proposed matroid rank on a basis and on the whole ground set. The result was reached on substantive approach 1 of a maximum of 5. Editorial preparation adds no mathematical approach.

## Source correction and interpretation

The source's actual comparison is r(S)/alpha <= f(S) <= alpha r(S). The denominator alpha on the left was dropped in the corpus transcription. The proof treats the original, weaker comparison, so it does not rely on that transcription error. The source says “constant” but does not separately quantify over finite ground sets; this edition explicitly uses the dimension-independent interpretation. The approximant is a single ordinary rank on the same ground set.

The result does not concern sums of ranks, weighted ranks, ranks on expanded ground sets, a scalar-rescaled output class, or an unspecified alternative intended question. No novelty, historical-priority or exhaustive-current-literature claim is made.

## Reading order

1. [The complete proof](REPORT.md), preserved byte-for-byte, includes all input hypotheses, a direct all-pairs submodularity proof, the lower bounds, and the exact uniform-rank sharpness argument.
2. [The full mathematical and source audit](SOURCE_AUDIT.md) retains every mathematical check, original-source observation, bounded literature assessment and disposition. Only private repository/corpus-history details were removed, with an explicit edition-selection notice.
3. [Edition acceptance](ACCEPTANCE.md) states the accepted scope and limits. [Provenance](PROVENANCE.md) explains preservation and the proof-only boundary. [Public source metadata](SOURCE_PROVENANCE.json) records the scholarly references and inspection history.
4. [Status](STATUS.json) records the scoped result. [The selected artifact inventory](ARTIFACT_MANIFEST.json) binds the proof, audit and status. [The edition manifest](MANIFEST.json) enumerates all members and hashes every member except itself.

The written proof is self-contained; no computational output or checksum is a mathematical premise. These are AI-assisted research audits, not external human peer review, journal acceptance or formal proof-assistant verification. This is an additive proof-only edition with no QUEUE.md or unrelated repository change.
