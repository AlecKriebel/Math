# Adversarial review of the structural sidecar

Status: **VERIFIED AFTER SCOPE CORRECTION**

This pass attempts to falsify the proposed obstruction rather than the
landmark theorem.

## 1. Does the triangle really meet the remainder in two states?

**VERIFIED.**  In a theta, the three internally disjoint paths share exactly
the two poles.  A triangle is the union of two of those paths, while the
remaining path has both poles as endpoints.  No choice of edge orientation
changes this undirected separator.  The blob is biconnected, so it cannot be
recast as a bridge gluing without changing the topology.

## 2. Does reticulation mixing spoil the factorization?

**VERIFIED.**  In each triangle-bearing core the reticulation whose two parent
edges lie in the triangle is assigned to the triangle factor; the other
reticulation and its choice are assigned to the complementary path.  Their
inheritance choices are independent.  Conditional on the pole states, every
edge transition and every choice weight belongs to exactly one factor, so
summing internal states gives the displayed contraction.  A root/incoming
message can be absorbed into either incident factor.

## 3. Is the gauge merely the already-audited bridge incidence gauge?

**FALSE.**  Separate pole factors produce a rank-one matrix in `(u,v)`.  The
translation-invariant exact witness `c(u,v)=2` on the diagonal and `1`
off-diagonal has a `2 x 2` minor of determinant `3`.  It therefore cannot be
written as separate incidence factors.  Scalar port-arm gauges are still
smaller.

## 4. Does the gauge prove nonidentifiability?

**FALSE; corrected before promotion.**  The transformed factors need not be
JC network tensors.  The first draft idea “the decomposition is nonunique,
therefore the topologies overlap” would have been invalid.  The report now
claims only that ambient contraction does not identify the factors and that a
model-specific gauge-rigidity lemma is missing.

## 5. Could generic tensor decomposition remove the gauge?

**NOT FROM THE AVAILABLE VIEWS.**  In every triangle-bearing strong word, any
extra port on either short path would destroy the triangle.  The triangle
sector therefore has exactly one observed four-state variable.  Its flattening
against the sixteen pole-state pairs has rank at most four.  Standard
three-view/Kruskal reasoning does not apply.  This does not rule out a special
JC rigidity theorem, which remains the stated open lemma.

## 6. Are all triangle-bearing cores included?

**VERIFIED against the locked inert core encoding.**  Direct path-length
arithmetic gives `theta-0`, `theta-1`, and `theta-3`; `theta-2` has all three
paths of length at least two.  The verifier independently reconstructs the
minimum-repair path lengths and triangle roles.  The arbitrary-word
conditions are proved symbolically in `STRUCTURAL_ANALYSIS.md`, not inferred
from a bounded enumeration.

## 7. Can marginalization or a virtual leaf repair the proof?

**NO WITHOUT AN EXTRA LEMMA.**  Marginalization is one-way and can erase the
triangle under the declared cleanup.  Adding a virtual leaf is an extension,
not an operation determined by the observed tensor.  Source-relative
containment does not furnish a compatible target extension or a continuous
target parameter section.

## 8. Could the published triangle-free theorem apply to the remainder?

**NO UNDER ITS STATED HYPOTHESES.**  The remainder has two hidden state
boundaries at the theta poles and is not a complete leaf-labelled
semi-directed network.  The theorem does not state identifiability in this
two-terminal tensor category.

## Final adversarial verdict

The obstruction is rigorous and correctly scoped.  It neither proves nor
refutes the desired JC identifiability theorem.  It rules out one proposed
shortcut and isolates a strictly narrower, honest load-bearing lemma.  Any
future proof claiming to combine level-1 and triangle-free identifiability
must either prove that two-terminal JC rigidity lemma or use a different
observable reconstruction which bypasses the hidden-pair factorization.

