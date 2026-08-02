# No universal death–birth amplifier, v1.0.0

This release publishes the fixed-graph obstruction and its exact verification
materials.

## Main results

- Every fixed finite loopless directed weighting with positive incoming degree
  is eventually death–birth suppressing, or its full death–birth chain exactly
  ties the complete graph.
- For complete directed support, the first strong-selection deficit is an
  explicit sum of squares over incoming weight columns.
- Every nonuniform positive weighted triangle suppresses death–birth fixation
  for every beneficial fitness.
- The same all-beneficial-fitness classification holds for the full symmetric
  `1+3` and `2+2` complete-support families on four vertices.
- Eventual amplification at every fixed fitness requires support degree to
  diverge in probability; a separate theorem excludes unequal-degree dense
  finite-type blow-ups under its stated hypotheses.

## Scope

The release rules out one population threshold that works uniformly for every
beneficial fitness.  It does **not** settle the reversed quantifier order in
which the population threshold may depend on fitness.  The unrestricted
six-edge weighted `K_4`, the diffuse asymptotically regular regimes, and the
optimal simultaneous-amplification interval remain open.

## Reproducibility

`make paper1` rebuilds all exact checks and the manuscript.  The released run
used Python 3.14.6, SymPy 1.14.0, and Tectonic 0.16.9.  Release assets include
the typeset paper, editable manuscript source, the complete reproduction tree,
and a SHA-256 manifest.

The manuscript and internal hostile audits are AI-assisted and have not
undergone external specialist peer review.

## Archival identifiers

- Version DOI: <https://doi.org/10.5281/zenodo.21753405>
- Concept DOI: <https://doi.org/10.5281/zenodo.21753404>
- GitHub release:
  <https://github.com/AlecKriebel/Math/releases/tag/universal-db-obstruction-v1.0.0>
