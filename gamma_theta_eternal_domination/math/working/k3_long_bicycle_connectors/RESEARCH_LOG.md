# Research log: long bicycle connectors

## 2026-07-27 (PDT)

- Re-read the accepted 2-SAT terminal trichotomy, connector parity law,
  canonical lollipop exclusion, `GFznc{` control, and mixed-\(P_4\)
  counterboundary.
- Rejected the naive contraction inference: a missing successor is a
  dynamic family statement and does not imply the corresponding graph
  nonedge.
- Isolated the maximal safe replacement: prove that every off-chain
  successor is absent directly, rather than infer its move edge is absent.
- Proved Lemma 2.1: one anchor plus any two outside vertices whose lists
  omit the same reference anchor is not a family state.
- Proved Lemma 2.2: any three such outside vertices are not a family state.
- Proved Theorem 3.1: the canonical one-unit tail-triangle remains
  impossible after an arbitrary odd path subdivision.  The theorem needs
  only \(a\in L(p)\) and \(a\notin L(v_i)\), not exact singleton/two-list
  equalities, and permits all additional complement edges.
- Found the exact attack chain
  \[
    P_{0,1}\longrightarrow P_{1,m}\longrightarrow
    P_{1,m-2}\longrightarrow\cdots\longrightarrow P_{1,3},
  \]
  where the last state is killed by attacking the intervening path vertex.
- Identified a sharp parity barrier for this mechanism.  For even path
  length, all opposite-parity token pairs form a closed abstract family
  avoiding the endpoint trap.  This is a transition countermodel, not a
  graph counterexample.
- Replayed the exact `GFznc{` 35-state family and the exact `FDzro`
  21-state mixed-\(P_4\) family.  Exhaustive tuple scans found zero
  embeddings of Theorem 3.1 in either control, as required.
- Current exact boundary: odd physical fan-path lollipops are eliminated;
  arbitrary implication bicycles are not.  The next useful target is to
  derive the fan-path geometry from a broader class of one-unit implication
  walks, or find new domination information that kills the even-parity
  token family.
