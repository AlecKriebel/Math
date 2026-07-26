# Research log: hostile order-13 strategy audit

## 2026-07-26

- **07:35 PDT:** Froze the requested historical targets:
  `math/lemmas/order13_strategy.md` at
  `eca21b547641f5f205bf9f5325d49f6c8edb6e6c778ff9fefacc7d1449e6b5c8`
  and `results/logs/order13_strategy_k3_template_pilot.json` at
  `331630a55b5d35d27f92e4104172811ab9e8ccac6aa14bb84de538dbc2b7148c`.
- **07:39 PDT:** Reproved Proposition 1 from C-003, C-006, C-036,
  C-049, and C-050.  Found the opening dependency-ledger omission of C-003
  and the unused inclusion of C-051; no defect in the proposition.
- **07:43 PDT:** Checked the exact C-051 complement identity, all
  \(k-t\) table entries, clique-extension consequence, local
  bipartiteness, and the \(k=3\) hub-free implication.
- **07:47 PDT:** Independently checked the SPGT cases.  The \(k=3\)
  four-template cover is complete, including the exclusion of a spanning
  induced \(C_{13}\).  The \(k=4\) cover
  \(C_5,C_7,C_9,\overline{C_7}\) is also complete relative to the accepted
  large-hole theorem and cycle obstruction.
- **07:51 PDT:** Wrote a standard-library-only clean-room constructor.
  It reconstructed all four exploratory order-13 \(k=3\) DIMACS streams
  byte for byte and matched every reported size, hash, variable count,
  clause count, literal count, and coloring-bank count.
- **07:53 PDT:** Independently recomputed the generic anchored
  \(k=3,4,5\) formula censuses and all proposed signature-comparator
  censuses.  Every reported number matched.
- **07:55 PDT:** Strictly parsed the pilot JSON, verified its source,
  formula, solver, hardware, seed, resource, result, and repository
  bindings, and queried the exact bound solver binary as CaDiCaL 3.0.1.
  Confirmed that the record remains `OBSERVED` / `UNSAT_UNCERTIFIED`.
- **07:57 PDT:** Recorded two prose corrections: the inaccurate
  dependency ledger and the `0.021`-second rounding mismatch.  Also recorded
  the exploratory-protocol gap: exact argv, CPU time, explicit version
  field, and transcript hashes were not retained and must not be invented.
- **08:04 PDT:** Completed the historical hostile review, deterministic
  evidence JSON, and byte-replay check.  No SAT solver was run on any
  formula.
