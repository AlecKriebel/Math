# Exact local-excess root cover for order 43

Date: 2026-07-24 (America/Los_Angeles)

## Result and claim boundary

An exact complement-and-relabel cover has been constructed for any
hypothetical order-43 Ramsey(5,5) graph. It has four basic root-degree
branches \(d=18,19,20,21\). An optional refinement has nine branches indexed
by the exact complement-invariant parameter

\[
\mu=\min(\delta(G),42-\Delta(G)).
\]

This is a checked decomposition and deterministic CNF design only. No branch
has been solved, no UNSAT certificate is claimed, and no Ramsey bound changes.

## Zero-sum local excess

For \(A_v=N(v)\), \(B_v=V\setminus(A_v\cup\{v\})\), define

\[
c(v)=e(G[B_v])-e(G[A_v])-\frac{d(v)(43-2d(v))}{2}.
\]

For an edge \(xy\), the number of vertices that count it in an induced
nonneighbourhood minus the number that count it in an induced neighbourhood
is \(43-d(x)-d(y)\). Consequently

\[
\sum_v(e(G[B_v])-e(G[A_v]))
 =43|E|-\sum_v d(v)^2
 =\sum_v\frac{d(v)(43-2d(v))}{2},
\]

so \(\sum_v c(v)=0\). Some vertex therefore has \(c(v)\le0\).

Complementation preserves \(c(v)\). Using the established degree interval
\([18,24]\), complement when the chosen vertex has degree above 21 and then
relabel it to vertex 0. Its degree is one of \(18,19,20,21\).

Let \(A=N(0)\), \(B=V\setminus(A\cup\{0\})\), and
\(H=\overline{G[B]}\). The condition \(c(0)\le0\) is equivalent to the
following integer cardinality bounds:

| \(d(0)\) | \(|A|\) | \(|B|\) | required \(e(G[A])+e(H)\) |
|---:|---:|---:|---:|
| 18 | 18 | 24 | at least 213 |
| 19 | 19 | 23 | at least 206 |
| 20 | 20 | 22 | at least 201 |
| 21 | 21 | 21 | at least 200 |

Each basic CNF branch fixes the root star and places one deterministic forward
sequential counter on the complementary “bad” literals: nonedges inside
\(A\) and edges inside \(B\). The complete appended-clause streams and their
variable layouts are frozen in the plan.

## Exact \(\mu\) refinement

The interval \([\mu,42-\mu]\) alone does not enforce that a branch's value of
\(\mu\) is exact. The refinement therefore adds 86 selectors, ordered as a
low/high pair for each of the 43 vertices, and one positive selector-cover
clause.

Under the global interval:

- a selected low witness forces its vertex to have degree at most \(\mu\),
  hence exactly \(\mu\);
- a selected high witness forces its vertex to have nondegree at most
  \(\mu\), hence degree exactly \(42-\mu\).

The implications use the already present forward degree-threshold variables.
Thus a satisfying refined branch has
\(\delta=\mu\) or \(\Delta=42-\mu\), so its invariant really is \(\mu\).
The case \(\mu=21\) is impossible because it would force a 21-regular graph
on 43 vertices and hence an odd degree sum.

The nine exact pairs are

\[
(18,18),(18,19),(18,20),(18,21),
(19,19),(19,20),(19,21),(20,20),(20,21),
\]

where each pair is \((\mu,d(0))\).

## Frozen artifacts

The exact plan is:

```text
results/benchmark_plans/global_croot_cover_v1.json
SHA-256 3d462687328fa9096a2be42b6fd16e0f0916a622533e3b18d4351bf8680d6847
```

The independent checker reconstructs the edge-variable map, base degree
counter endpoints, c-root counters, global interval units, extremum selectors,
and every appended-clause hash without importing the generator. It reports
four basic branches, nine exact-\(\mu\) branches, and zero errors:

```text
results/verification/global_croot_cover_v1.check.json
SHA-256 bf1ad9b6c2cd797697db30fe845fe9a152438c6cfd6f5bae67275cff3e90a907
valid true
```

Five focused tests also check the zero-sum identity and complement invariance
on deterministic random graphs, all four thresholds, independent clause
reconstruction, exact selector layout, and a 20-regular circulant boundary
example.

## Reproduction

```bash
PYTHONPATH=src:verify /opt/homebrew/opt/python@3.11/bin/python3.11 \
  tests/global_croot_cover_tests.py -v

PYTHONPATH=src:verify /opt/homebrew/opt/python@3.11/bin/python3.11 \
  verify/global_croot_cover_check.py \
  --plan results/benchmark_plans/global_croot_cover_v1.json \
  --output results/verification/global_croot_cover_v1.check.json
```
