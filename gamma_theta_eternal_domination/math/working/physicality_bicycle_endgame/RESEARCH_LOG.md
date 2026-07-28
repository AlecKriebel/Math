# Research log: physicality bicycle endgame

## 2026-07-28 PDT

- Read the accepted minimal-2-SAT classification and C-079,
  C-094--C-105, and C-107 in their exact stated scopes.
- Began under the then-provisional physicality theorem and rechecked the
  argument after C-111 was accepted at commit `73cf94ff`.
- Derived the same-type-mate lemma from the common-neighbor condition for
  the pair consisting of a port and its omitted anchor.
- Combined that mate with C-079 to upgrade conditional projection
  side-purity to universal side-purity.
- Proved that an endpoint-type common neighbor of a cross edge violates
  universal side-purity.  Hence every cross edge has only third-type
  common neighbors and belongs to a literal transversal triangle.
- Observed that this removes the C-095/C-099 transport issue without
  contradicting C-105/C-107: no representative is substituted and no
  almost-cap arms are promoted to an equality.
- Replaced the response 2-CNF by the exact signed edge system in which
  same-type edges flip chirality and cross-type edges preserve it.
- Used the outside diameter-two consequence of \(\gamma=3\) to prove
  that any shortest unbalanced signed cycle has length at most five.
- Exhausted type words through length five.  Bipartiteness and universal
  side-purity leave exactly the five residual words recorded in
  `NOTE.md`.
- Constructed the 12-vertex gamma-two eternal boundary
  `KBjB\z[^||Z[`.  Its 163 dominating triples form the greatest eternal
  family, every list is exact and physical, and its shortest unbalanced
  cycle has length six.
- Added the three complement mate edges `3-9,4-7,8-11`, obtaining the
  gamma-three static boundary `KBjB\j[Z||ZW`.  It shortens the odd
  holonomy to a five-cycle but deletes all 136 dominating triples in
  rounds `34,56,46`.
- Wrote a standalone ordinary-set verifier.  It passed warning-fatal
  execution and independently checks all 1,467 obligations of the
  eternal control, both parameter tuples, the type geometry, coloring
  gap, common-neighbor boundary, signed cycles, and word classification.

The complete arbitrary-bicycle proof is not finished.  Its exact current
target is a one-guard exclusion of the five chordless signed type
skeletons

```text
0012
00011
00101
00102
00121
```

with literal third-type triangle witnesses on every cross edge.
