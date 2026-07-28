# Research log: exact \(Y_k\) equality gates

## 2026-07-28 PDT

- Audited C-125 and C-126 without assuming functoriality of either static
  or family response lists.
- Observed and proved the mandatory-contamination fact: because every
  \(x_i\) can replace every \(d\in D\), while \(z_dx_i\) is a graph
  nonedge, each \(z_d\) must have a graph neighbor in \(S-\{d\}\).
- Proved that a base-clean exact \(Y_4\) is impossible.
- In the base-clean branch for \(k\geq5\), formed the directed
  singleton-to-\(D\) contamination graph.  Positive outdegree forces a
  directed cycle.  Each cycle arc forces a closed-private buffer; the
  retained installed state forces every such buffer to see another
  singleton.  A simple cycle therefore supplies at least two distinct
  vertices outside the clean equality-three projection.
- Re-audited the endpoint static-defect count.  An original defect either
  survives as a thirteenth vertex in the C-072 projection or is repaired
  by, and therefore lies outside through an edge to, \(Z\).  It is
  disjoint from the cycle buffers because their closed-private anchors
  differ.
- Combined the counts to prove the unconditional clean-pattern floor
  \(n\geq2k+9\) for \(k\geq5\).  No projected static-defect-survival
  hypothesis is required.
- Isolated the only collision preventing \(2k+10\): one common endpoint
  defect outside the projection and adjacent to \(Z\).
- Initially claimed that the dirty-base private-buffer carrier always
  has exact shifted family \(Y_3\) lists.  Hostile review found that this
  repeated C-121 at a potentially nonindependent state: restoration
  relative to the original \(S\) does not force direct successor
  membership at that carrier.
- Retracted and corrected that overclaim.  The retained shifted carrier
  has nonempty response sets inside the \(Y_3\) caps, exact endpoint
  caps, and every intended role is a graph incidence.  Full exactness
  follows when the carrier is independent from \(Z\).
- Recorded the hostile review's nine-vertex \(Z\)-fixed symbolic control:
  its 34-state one-guard kernel satisfies all 136 attacks and all assigned
  restoration inclusions but omits one shifted middle role.  This refutes
  the proof-method inference, not a stronger theorem under the complete
  original \(Y_k\) hypotheses.
- No solver search, candidate counterexample, or experimental claim is
  included in the frozen result.
