# Research log: distributed gate holonomy

## 2026-07-28 PDT

- Read the accepted literal-physicalization theorem C-094, original-edge
  incidence theorem C-098, and third-color odd-return theorem C-100 with
  its hostile review.
- Encoded the smallest pair of separated parallel tight gates with two
  projection connectors.  Exact one-guard probes were UNSAT whenever the
  connector parities differed, without using \(\gamma(G)=3\).
- Replaced the gate hypotheses by their two dead boundary states.  The
  exact probes then became SAT for equal parity and UNSAT for opposite
  parity, isolating the correct theorem.
- Proved the boundary parity synchronization theorem by:
  1. launching two retained corner states from the direct endpoint
     responses;
  2. converting each across one complement edge into a retained
     \(b\)-corner state; and
  3. propagating that state by two steps at a time using the accepted
     same-side path dead-state lemma.
- Derived the separated parallel-gate odd-bigon exclusion.  The theorem
  permits four distinct physical ports and arbitrary subdivisions in both
  connector components.
- Independently rebuilt four accepted equality controls and checked 436
  qualifying vertex-disjoint path pairs.  Every pair had equal parity,
  and same-parity examples occur, confirming the stated boundary is sharp
  against the naive stronger prohibition.
- Remaining gap: a minimal odd signed cycle through at least three tight
  gates, where the alternate route between two gates changes omitted
  color and is not contained in one frozen projection.

No universal \(k=3\) theorem or conjecture resolution is claimed.
