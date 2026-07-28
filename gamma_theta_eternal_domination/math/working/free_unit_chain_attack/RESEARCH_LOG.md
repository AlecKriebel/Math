# Research log: free singleton unit-chain attack

- 2026-07-28 PDT: Opened the lane after reading the accepted C-069,
  C-075, C-079, C-094, C-098, C-103, C-119, and C-120 notes.  The first
  analytic observation is that a free singleton marker propagates retained
  anchor--vertex pairs through its entire frozen bipartite component, not
  merely a Boolean orientation.  Began a direct arbitrary-family SAT
  synthesis for the exact mixed family-list \(P_4\) under
  \(\gamma(G)=3\), to determine whether full equality itself forbids the
  smallest two-unit chain or merely forces a larger control.

- 2026-07-28 PDT: Proved the length-independent component-polarization
  theorem.  A free singleton marker forces one retained anchor--vertex
  pair on each side of its whole projection component.  Attacking across
  an arbitrary component edge then proves that every complement edge in
  the component lifts to a retained frozen family state.  All singleton
  pins in one component are consequently coherent.  This eliminates the
  zero-binary-clause two-unit terminal but not a chain that crosses a
  genuine clause.

- 2026-07-28 PDT: Found the seven-vertex equality control `FCZbg`.
  Its greatest family has eighteen states.  At reference `345`, vertices
  `0` and `6` are singleton markers of opposite colors in the same free
  frozen-`4` component, and the complement edge `06` lifts to retained
  state `046`.  A standalone verifier recomputes all five parameters,
  all seventy-two obligations, lists, projections, polarization, and edge
  saturation.

- 2026-07-28 PDT: Discovery-only same-marker two-arm probes through path
  length six showed UNSAT whenever at least one arm was even and SAT for
  odd/odd arms.  Discovery-only exact mixed-\(P_4\) synthesis returned
  UNSAT at orders 12, 13, 14, 15, 16, 18, and 20.  No proof logs or
  unbounded coverage proof were produced, so none is a mathematical
  claim.  One order-twenty CEGAR leaf was terminated at the ten-minute cap
  and is TIMEOUT/OBSERVED.  No further long solver was launched.
