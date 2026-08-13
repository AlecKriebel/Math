# Search contract

## Locked topology convention

The search uses the literal narrow reduction `sd_0` from
`../../docs/DEFINITIONS_LOCK.md`.  A standard semi-directed candidate is a
simple labelled mixed graph in which every unlabelled internal vertex has
degree three, every taxon has degree one, and each declared reticulation has
exactly two incident arrowheads.  A root site is compatible at a
reticulation endpoint only when the removed mixed edge carries an arrowhead
at that endpoint.  All remaining ordinary edges are oriented afresh and the
result is retained exactly when it is a binary acyclic LSA-valid rooted
network whose `sd_0` image is the input mixed graph.

`W_TC` means at least one such rooting is tree-child; `S_TC` means every such
rooting is tree-child.  A graph with no admissible rooting is discarded.

## Bounded census

The first exact census covers simple binary mixed graphs with three through
five labelled leaves and zero, one, or two reticulations.  It is generated
from every connected simple internal graph with the forced degree sequence,
every labelled leaf allocation, every reticulation set, and every choice of
two incoming incidences at each reticulation.  Canonicalization preserves
taxon labels and arrowheads.  Ordinary triangle redirection is quotienting
only after exact mixed-graph isomorphism.

This is a bounded falsification test.  Even when exhaustive at the stated
sizes, a negative census is not promoted to a theorem for arbitrary port
subdivision.

## Model screen

For each retained topology, displayed rooted switchings are derived directly
from one admissible rooting.  JC Fourier coordinates are computed from the
displayed-tree split masks.  Numerical or modular rank/ideal screens only
nominate possible collisions.  A positive counterexample requires exact
open-domain parameter equality or containment and exact generic-rank
certificates.

