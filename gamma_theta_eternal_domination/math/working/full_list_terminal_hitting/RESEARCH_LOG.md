# Research log

## 2026-07-27 PDT

- Read the accepted full-list deletion, safe-kernel, separated-port,
  minimal-2-SAT, odd-connector, dynamic-cap, and cap-and-escape notes, plus
  claims C072--C084.
- Fixed one inclusion-minimal augmented core for each failed color and
  observed that its one or two augmented units hit every satisfying
  assignment of the base formula.  This gives at most six fixed link
  terminals for all three colors.
- Combined the fixed hitting sets with a compatible deletion coloring to
  obtain a rainbow terminal transversal.  The three direct terminal states
  are retained, while the all-link state fails to dominate the full
  vertex, localizing the first cross-label response to cube level two or
  three.
- Proved directly that three link vertices with respective singleton lists
  \(\{a\},\{b\},\{c\}\) cannot coexist.  Therefore three failed
  augmentations cannot all be immediate false constants.
- Refined the accepted Kempe-linkage lemma: a shortest bichromatic
  link-to-link path yields either a link edge of that color pair or a
  hub-free induced odd hole through the full vertex.
- Generalized the exact cap-and-escape placement to a location trichotomy
  for every all-dynamic omitted-color edge: \(R\)--\(R\),
  \(R\)--\(Z\), or \(Z\)--\(Z\).
- Audited the known \(\gamma=2\) controls.  They delimit, rather than
  refute, the new \(\gamma=3\)-dependent cap conclusions and show that
  safe kernels, ridge covariance, false constants, and Boolean port
  recurrence do not separately finish the proof.
- Stop gate: no theorem currently aligns a terminal-cube move edge in
  \(G\) with a marked implication connector or Kempe ear in \(H\).
  Base-unsatisfiable formulas, singleton or \(A_\ast\) terminals,
  separated/multi-port lollipops, longer two-unit chains, and finite
  cap-escape recurrence remain open.
