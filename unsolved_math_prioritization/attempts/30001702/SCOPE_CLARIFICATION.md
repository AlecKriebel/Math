# Mandatory scope clarification

Problem 30001702 remains **unsolved, 5/5**. This publication preserves both frozen packets byte-for-byte. The independent audit required no mathematical correction patch.

## Target tetrahedron types in the parity argument

In the author's Section 3, “a triangle missing i,j lies in exactly two tetrahedron types” refers to a **target triangle in the boundary of the 4-simplex** and the two possible **target** tetrahedra containing it. The two incident **source** tetrahedra may have the same vertex-set type. There is no assertion that their missing-vertex types differ.

The global vertex-label map sends the mod-2 source fundamental cycle to a target top cycle. At the target triangle missing i,j its boundary coefficient is a_i+a_j, giving equal parity of all five type multiplicities. See audit/EXPANDED_LEMMAS.md, Section 5.

## Accepted bounds and remaining gap

The accepted results are the general central-binomial lower bound and vertex refinement; sharp factorial minima in dimensions one and two; and the factorial bound with equality for the explicitly regular unimodular lattice-quotient subclass. They do not prove the universal factorial target.

A dimension-three counterexample would need five vertices, underlying simple graph K_5, and f-vector (5,27,44,22) or (5,28,46,23), together with the stated parity conditions. These are **necessary conditions only**. Neither vector is certified realizable, excluded, or a counterexample.

The colored 1-dipole reduction applies to properly four-colorable decompositions. It does not color arbitrary simplicial posets. The lattice-volume argument requires its stated geometric hypotheses. Finite computations supplement the written arguments; they do not prove torus homeomorphism or general minimality. No novelty, human peer review, or universal resolution is claimed.
