# Explicit correction record

The corrected `REPORT.md` and `PARAMETRIC_EXTENSION.md` are the controlling mathematical texts. `CORRECTIONS.patch` shows all seven recorded changes from the initial authored report to the corrected report.

The pre-edit report was reconstructed by reversing those recorded editing operations; it was not captured as an immutable live snapshot before the edits. This limitation is explicit rather than presenting a retrospective reconstruction as a contemporaneous snapshot. The reconstructed full baseline is preserved locally and is omitted from this public slice because it contains rejected, superseded statements. The patch is an authored correction record: removed lines are rejected text, not accepted claims. Historically it was checked against that reconstruction and produced the corrected report exactly; full-baseline patch replay is NOT_RUN in the public-only protocol.

## Corrections and changes

1. Restrict Alexander shrinking to 0<t≤1, with t=0 separately defined. The earlier phrase “for t>0” was too broad. For example, an increasing interval homeomorphism with h(1/2)=3/4 gives A_2(h)(1)=3/2, which is not in the unit interval.
2. Specify that the fragmentation subgroups have their subspace topologies, ensuring continuity of the product map used in the proof.
3. Use D=max(forward distance, inverse distance), consistently with the parametric note. With this convention the radial bound is π/(2N). The sum convention would require π/N; topology and completeness are unaffected.
4. Incorporate the proved radial-amplification obstruction into the route summary, rather than leaving that particular interpolation's dimension-free bound merely unproved.
5. Update the route's exact-gap paragraph accordingly. A different interpolation or another extension construction remains possible.
6. Restrict the fragmentation statement's target group to the separable metrizable category matching the inspected Hanner theorem. The compact-manifold homeomorphism groups under discussion satisfy this restriction.
7. Narrow the Haver-source inspection statement: the original full proof was not obtained, and no positive ANR conclusion depends on it.

The review found the priority mathematical arguments sound as partial results after the parameter-range and topology clarifications. The maximum-metric convention makes the numerical normalization explicit. No correction turns these statements into a solution or refutation of the compact-manifold ANR problem.

## Pinned hashes

- Reconstructed baseline SHA-256: c88e169dbdca92b29a5508d04bb4939cd418c04b2bfa6e38e6aff8be03a72f5c
- Corrected REPORT.md SHA-256: d57de7c98d615a70fea2bfd3e6b5a338ac83e497adede77034b85e78a3de610f
- Original CORRECTIONS.patch SHA-256 (before the publication preamble): 61004cf5771891c876c811a4d0227db2f9469b87c0669d9a6d43d2f4131a0f29
