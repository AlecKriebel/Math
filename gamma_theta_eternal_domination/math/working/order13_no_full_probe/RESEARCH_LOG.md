# Research log: order-13 no-full-list probe

## 2026-07-27 PDT

- After independent certification of the complementary full-response branch,
  built an exact discovery formula for the case in which every response list
  at the fixed maximum independent triple \(S=\{0,1,2\}\) has size at most
  two.
- The formula retains the exact order-13 equality, one-guard closure, and
  complement non-3-colorability clauses.  It removes the distinguished full
  target and adds ten no-full-list clauses.
- The discovery formula has 9,802 variables and 85,413 clauses.  Its
  retained DIMACS SHA-256 is
  `5d6d9bccb80c3ccab222a095819d50b58bb9f1fc22652b2d0bad8013681fd007`.
- CaDiCaL 3.0.1 reached the 120-second wall limit without returning SAT or
  UNSAT.  This timeout is a nonclaim.
- The interrupted run produced a 389 MiB partial DRAT stream.  It cannot
  certify UNSAT and was deleted to preserve laptop disk capacity.  The
  generator, exact DIMACS instance, empty solver log, and command are
  retained, so the exploration is resumable.
- No full-list or no-full-list order-13 conclusion is inferred from this
  timeout.  The independently certified full-response exclusion remains a
  separate result.

Exact command, from the campaign directory:

```text
python3 -I -B -W error \
  math/working/order13_no_full_probe/search.py \
  --solver tools/cadical_3_0_1/build/cadical \
  --timeout 120 \
  --instance math/working/order13_no_full_probe/instance.cnf \
  --proof math/working/order13_no_full_probe/proof.drat \
  --solver-log math/working/order13_no_full_probe/solver.out
```
