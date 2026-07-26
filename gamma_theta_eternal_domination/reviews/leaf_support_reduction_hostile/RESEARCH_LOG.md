# Research log: leaf--support reduction hostile audit

## 2026-07-26

- **05:28 PDT:** Began clean-room reconstruction in the exact one-guard,
  unoccupied-attack family model.  Derived the \(x\)-fixed projected family
  and identified the need to exclude states containing both \(x\) and \(y\).
- **05:34 PDT:** Reported the missing co-occupation justification in the first
  draft.  The author patched it by observing that deleting \(x\) from a
  dominating \(k\)-state containing \(x,y\) would contradict
  \(\gamma(G)=k\).
- **05:39 PDT:** Tightened the order-\(12\), \(k=5\) implication: the
  hypothesized graph itself is minimum-order under the published
  through-order-\(11\) premise, so its own parameter \(k=5\) enters the
  \(5k/2\) bound.
- **05:43 PDT:** Requested and verified an explicit citation and scope
  statement for the MacGillivray--Mynhardt--Virgile computation.
- **05:46 PDT:** Recorded the \(Q=\varnothing\) boundary.  It is exactly
  \(G=K_2\) and requires an empty-graph eternal-domination convention; it is
  irrelevant to counterexamples.
- **05:48 PDT:** Completed a clean-room bitmask probe through order \(8\):
  13,598 nonempty unlabeled graphs, 694 equality graphs, and 467 eligible
  leaf--support choices.  All assertions passed.
- **05:51 PDT:** Visually inspected pages 3 and 5 of the official Henning--
  Schiermeyer--Yeo PDF and page 620 of the official MMV PDF.  Confirmed the
  exact McCuaig--Shepherd restatement, the one-plus-six exception inventory,
  and MMV Observation 5.6.
- **05:54 PDT:** Assessed a possible removal of the MMV premise.  Deferred:
  three order-\(7\) exceptions still require packaged one-guard failure
  certificates or analytic proofs, beyond the supporting fixed-point output.
- **05:59 PDT:** Finalized the hostile review against target SHA-256
  `802907a01c27043dfa1348a1c8e97e142769238cb62c9064e946573dfba93517`.
  Verdict: `ACCEPT_PROVED_WITH_EXPLICIT_PUBLISHED_COMPUTATION_DEPENDENCY`.
