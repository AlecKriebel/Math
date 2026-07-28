# Research log

- **2026-07-27 PDT.** Read the odd fan-path theorem and its independent
  hostile PASS review in full.
- Expanded a general augmented unit as an orientation constraint on a
  frozen component.  Identified the unsupported inference: the first and
  last implication clauses need not use the unit marker, or even the same
  physical port.
- Built the smallest separated-port Boolean pattern: an even
  three-vertex starting connector and an odd two-vertex repeated
  connector.
- Used a direct graph/family SAT encoding to find a realization, then
  replaced the solver witness by a deterministic definition: the greatest
  safe kernel after banning the unwanted direct swaps.
- The resulting graph has labeled graph6 `HFzvvn{`, canonical graph6
  `Hvzax|~`, a 65-state proper eternal family, and all 390 literal
  one-guard obligations.
- Exact lists are
  \(S,\{a,b\},\{a,b\},\{a,b\},\{b,c\},\{b,c\}\).  The base formula has
  two assignments; coloring the full target \(a\) adds the sole unit and
  produces a minimal one-unit lollipop.  Exhaustive embedding finds zero
  odd fan paths.
- **Verdict:** automatic fan lift refuted locally.  Under
  minimum-counterexample \(\gamma=3\), port identification remains open.
  The sufficient extra hypothesis is a common terminal port in \(R_x\)
  plus one vertex-distinct odd connector contained in \(W_a\).
