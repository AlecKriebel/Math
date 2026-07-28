# Research log: hostile review of the full-list terminal gate

## 2026-07-28 PDT

- Froze the candidate at commit
  `34c80b36dc03b6fbab846c27a71d90db3301cb45`.
- Read the complete candidate note, C-141/C-142 source and hostile review,
  and C-149 source and hostile review.
- Audited all per-color and per-trace quantifiers, response-palette
  semantics, the two attack-tree branches, the 27 terminal-label triples,
  and the distinction between a retained family state and a graph edge.
- Built an independent seven-vertex fixed-point exhaustion.  All 512
  graph completions reject three simultaneous own-color singleton
  terminals; relaxing either singleton ban for one color yields 35
  mutation controls per relaxed color.
- Independently rebuilt the order-12 equality control from graph6.  The
  five parameters, 127-state greatest family, restricted kernels,
  synchronous deletion rounds, four terminal rows, and four corridor
  diamonds all match.
- Verdict: `PASS_STRICT_SCOPE`.  The theorem proves at least one color has
  no own-color-singleton terminal trace; it does not prove that a safe
  color exists.
- Recorded two nonfatal wording cautions: the control does not establish
  literal sharpness of (3.2), and the proposed all-nonsingleton
  corridor-only lane is not the exhaustive remaining case.
