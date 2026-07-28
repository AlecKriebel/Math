# Research log

## 2026-07-27 PDT

- Froze the target at SHA-256
  `f51bd5e1b032b739478822c6212c16734ec590806e34e39e46f4fc7f70786f4c`.
- Rebuilt the graph and restricted eternal family with an independent
  bit-mask implementation.
- Verified 65 states, deletion rounds \(8,1,4\), all 390 literal
  one-guard obligations, exact lists and parameters.
- Independently reconstructed the base orientation formula, augmentation
  lollipop, semantic list colorings, and exhaustive odd-fan embedding test.
- Found one scope overstatement in the minimality paragraph: coincident
  terminal ports do not force a fan unless the common port also lies in
  \(R_x\).
- Verdict: **qualified pass; exact control accepted, one textual scope
  correction required.**

## Revised bytes

- Re-read the corrected target at SHA-256
  `6ee66aec144b41a1256e7c9503d46fb7a0fde5d948cd76bda1e86128766d9563`.
- Confirmed that the minimality paragraph now has the required
  outgoing-port subclass restriction and explicitly recognizes a shared
  port outside \(R_x\).
- Rebound and reran the independent replay; every mathematical payload is
  unchanged.
- One downstream scope issue remains: Section 4's “remaining exact branch”
  must include the shared-port-\(q\notin R_x\) alternative.
- Rechecked the subsequent opening-language revision at SHA-256
  `e9c66ed9bd7bbe883226fffd61928675ffd50cc4e135633436a1a538fa60766b`;
  “one explicit obstruction” now avoids any uniqueness claim.

## Final revised bytes

- Re-read target SHA-256
  `31c72da963cedf7e90a095fa565c1d7690b4acacc2bb54d833be65311278e286`.
- Confirmed Section 4 now includes the shared-port-\(q\notin R_x\)
  alternative, making the stated remaining branch complete.
- Rebound and reran the replay with result SHA-256
  `8cc75c25da867d718544feb1931d6e8726e6796a02b511e05b3a8471492e950d`.
- Final verdict: **PASS; no issue remains.**
