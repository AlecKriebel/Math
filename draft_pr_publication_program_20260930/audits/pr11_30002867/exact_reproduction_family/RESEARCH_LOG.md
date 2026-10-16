# Exact reproduction and adversarial computational family

Scope: frozen PR11 head `810559762f906624e0939191f5aface0ce7ce301`.
Only this family directory and ignored `tmp/reproduction/pr11_exact_family/`
are writable. No external communication or Git mutation is authorized here.

- 2026-10-01 04:59 UTC — Started independent reproduction. Defined success as
  immutable-manifest verification, byte-identical reruns, and materially distinct
  exact quotient computations checked against separately proved local equation
  counts. General theorem proof and literature novelty are separate families.
  Completion estimate: 10% of this computational audit.
- 2026-10-01 05:02 UTC — Verified all 14 manifest files before and after scratch
  reruns. Author suite reproduced 13 examples byte for byte; frozen prior review
  suite reproduced 20 examples byte for byte. Both exit successfully. A proposed
  plane stress ideal `(u²-v³,uv,v⁴)` exposed a redundant equation:
  `v(u²-v³)-u(uv)=-v⁴`; its true count is two. Using this as an adversarial
  expected-count check and adding a genuine nonhomogeneous non-CI alternative.
  Completion estimate: 30% of this computational audit.
- 2026-10-01 05:06 UTC — New ideal-derived checker passed rational cases through
  dimension six and length twenty. Corrected its chain-condition check to
  simplify exact algebraic expressions before equality; raw SymPy structural
  equality had rejected a zero expression after conjugation. This was an audit
  harness issue, not a counterexample. No source snapshot file was changed.
  Completion estimate: 65% of this computational audit.
- 2026-10-01 05:07 UTC — All 14 new ideal-derived cases pass, using five explicit
  exact coefficient fields. Full Koszul Betti vectors agree with independently
  certified resolutions/counts. A four-component length-seventeen example
  filters 36 Cartesian spectral combinations down to four support points. The
  transpose of a non-CI regular module demonstrates a D2-only false positive
  outside the regular-representation hypothesis. A fixed-basis family
  `x²=xy=0, y²=epsilon*x` demonstrates actual discontinuity inside the valid
  quotient class; at epsilon=10^-18 the exact second rank is 2 and NumPy's
  default numerical rank is 1. Embedded SHA256SUMS also matches all 13 entries.
  Completion estimate: 85% of this computational audit; independent certificate
  review and final report remain.
- 2026-10-01 05:17 UTC — Final adversarial reread passed all expected ideal
  data, CRT localization, perturbation ideal equality, nonregular-dual and
  global-N guards. Both ideal-certificate scripts reran from an independent
  ignored scratch copy and matched saved mathematical output. All 14 frozen
  files and 13 embedded checksums reverified unchanged; both frozen JSON
  outputs again reproduced byte-identically. Root independently reviewed the
  new checker. Portable reproduction now pins three dependencies, identifies
  the already-existing audited Python3.9.6 environment, and recommends
  Python3.9–3.12 for the complete pinned NumPy stack. No new environment was
  installed. The second Gorenstein model is linearly equivalent to J over C;
  no rational isomorphism is claimed, and rational Betti transfer is justified
  by flat minimal graded base change. Strongest result: reproducible frozen
  artifacts and 14 independent ideal-derived tests at 24 support points,
  dimensions1–6, lengths4–20, with full Betti agreement. Exact gap beyond this
  family: the general theorem/global efficient-generation and source proofs,
  handled separately. No in-scope counterexample or computational blocker.
  Completion estimate: **100% of this computational audit**. This percentage
  does not measure novelty or discovery of the arbitrary-d,N theorem.
