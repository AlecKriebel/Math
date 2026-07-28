# Research log: side-pure ports and the cap-cycle boundary

## 2026-07-27 22:23 PDT

- Read the accepted C-075, C-079, C-081, C-082, and C-083 proof notes,
  including their explicit warnings against converting response omission
  into a graph nonedge or Boolean port identity into physical identity.
- Recast C-079 as a componentwise side-purity theorem: any physical hub
  having an \(a\)-positive complement neighbor can meet only one side of
  each component of \(H[W_a]\).
- Derived the singleton-buffer consequence.  A two-list port that meets
  opposite sides of an \(a\)-omitting component has no \(a\)-positive
  complement neighbor; every outside continuation in its own omitted-color
  projection is therefore forced to be the third-color singleton.
- Located the connected graph6 control `GCXfVG`.  Its greatest eternal
  triple-family has 26 states, exact lists
  \[
    \{a\},\{b,c\},\{b,c\},\{b,c\},\{b,c\},
  \]
  and a single \(a\)-positive cap repeated around the full
  \(a\)-omitting complement \(C_4\).
- Proved directly that the graph has
  \[
    (\gamma,\alpha,\gamma^\infty,\theta)=(3,3,3,3)
  \]
  and that the 26 states are exactly all dominating triples and form an
  eternal family.
- Built an independent ordinary-set verifier.  It checks the 13 graph
  edges, all 26 dominating triples, the greatest safe kernels, all 130
  unoccupied attack obligations, the exact lists and two compatible
  colorings, all four parameters, the repeated cap (including one fully
  dynamic rim edge), and zero C-079 embeddings at all three anchors.
- Froze the exact boundary: the control is colorable and does not refute
  the gamma--theta conjecture or an arbitrary-bicycle theorem.  It refutes
  only a recurrence argument based on cap repetition, equality, and
  finiteness without using cross-clause or terminal-unit data.
