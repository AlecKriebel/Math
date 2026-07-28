# Research log: dynamic gluing at \(Y_3\)

## 2026-07-28 PDT

- Read C-059, C-067 through C-072, C-079, C-117, C-118, and C-119,
  together with the accepted mixed-\(P_4\) hostile reviews.
- Distinguished the relevant C-117 static response lists from the earlier
  family-response mixed-\(P_4\) analysis.
- Proved that an exact static \(Y_3\) forces the exact family \(Y_3\):
  endpoint attacks first force the middle color in both internal lists;
  two further forced attacks show that either missing end color violates
  restoration.
- Observed that C-070 makes the omitted middle-color swaps at both path
  ends genuine domination failures.  Their missed vertices form two
  singleton-middle-color ridge cliques.
- Tested the only possible witness collision, where one vertex witnesses
  both failed swaps.  A greatest restoration-compatible kernel deletes the
  reference state in all 16 remaining core adjacency completions.
- Converted that computation into a coverage lemma that is insensitive to
  any number of external vertices: all attacks and successors used by the
  local kernel remain inside the eight displayed vertices.
- Combined the new disjoint defect vertices with the five mutually
  separated witness systems of C-072 to obtain the conditional analytic
  floor \(n\geq14\) for an exact static \(Y_3\) realization.
- Added the exact `FDzro` gamma-two boundary control.  Its 21-state family
  realizes the family-list \(Y_3\), while its static lists are larger.
- Incorporated the concurrently proved, still-hostile-review-pending
  anchor-component lemma as a nondependent interpretation: the two
  \(Y_3\) exact-two endpoints and both unit-bearing components are free, so
  the obstruction is a genuine two-unit/one-clause certificate.
- Independently checked the graph-specific negative control
  `IzM]XTR`W`: its complement is \(K_4\)-free with bipartite links and a
  common neighbor for every pair, but all 77 dominating triples are
  deleted in four one-guard rounds; its full parameter tuple is
  \((3,3,4,4)\).  No claim is made about the coverage of the larger
  exploratory scan that found it.

## Scope

The literal seven-vertex \(Y_3\) is impossible when \(\gamma=3\), and any
embedded exact static realization has order at least 14.  Arbitrary-order
realizability remains open.  This does not prove \(\mathsf{GL}(3)\), the
complete parameter-three theorem, or the universal conjecture.
