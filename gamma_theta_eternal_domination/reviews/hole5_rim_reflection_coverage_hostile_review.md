# Hostile review: residual rim reflection and combined hole-5 coverage

**Verdict:** `ACCEPT_RIM_REFLECTION_AND_COMBINED_COVERAGE`

**Boundary:** This verdict certifies a symmetry/covariance argument and an exact
CNF byte construction for the frozen complete-bank `hole5` formula. It does
not assert that the formula, any cube, or the underlying graph problem is SAT
or UNSAT. No SAT solver was run.

## Frozen input

Let \(F\) be the complete `hole5` formula with:

- 6,886 variables, 23,653 clauses, and 188,959 literals;
- CNF SHA-256
  `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7`;
- coloring-bank SHA-256
  `b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00`;
- manifest SHA-256
  `99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402`.

The audit independently rebuilt every one of the 3,645 bank clauses and found
the rebuilt stream equal, clause-for-clause and in order, to the suffix of
\(F\).

## Complete semantic action of the reflection

The probe did not import the production encoding or symmetry-breaker modules.
It independently reconstructed the allocation:

| Role | Variables | Interval |
|---|---:|---:|
| edge | 66 | 1–66 |
| common-neighbor witness | 660 | 67–726 |
| eternal-family state | 220 | 727–946 |
| legal-move witness | 5,940 | 947–6,886 |

For the vertex reflection
\[
\rho=(0\ 1)(2\ 4),
\]
fixing \(3,5,6,\ldots,11\), it then constructed the semantic image of every
variable:

- \(e_{\{u,v\}}\mapsto e_{\{\rho u,\rho v\}}\);
- \(w_{\{u,v\},x}\mapsto w_{\{\rho u,\rho v\},\rho x}\);
- \(f_D\mapsto f_{\rho(D)}\);
- \(m_{D,r,u}\mapsto m_{\rho(D),\rho(r),\rho(u)}\).

Pairs and triples were renormalized after relabeling. The resulting map is a
role-preserving involutive permutation of all 6,886 variables. Its full
`old-variable image-variable` stream has SHA-256
`0676813af83a90bb9193cd79e149cd6e0693b7581b9a19ff75fafc9d96a66471`.
It moves 36 edge, 476 witness, 148 family, and 4,988 move variables.

This full action matters: relabeling only graph-edge variables would not
establish covariance of the auxiliary witness and eternal-family clauses.

## Exact covariance result

After applying the full signed-literal action, the following clause multisets,
including multiplicities, were unchanged:

| Portion | Clauses | Literals | Canonical multiset SHA-256 |
|---|---:|---:|---|
| base | 20,008 | 114,601 | `81ed857162f778f0fbebdc6be753fb53aec32ed756b8d31e06589ed323ce62cd` |
| coloring bank | 3,645 | 74,358 | `44f752a8d551a58e1a8750f9b4922a561177268ba027803fdbfadf0bbf15b841` |
| full \(F\) | 23,653 | 188,959 | `201496666b255837ff7692ce13ef058f867a11ea7404d571429b7bf0589b1b78` |

All 3,645 coloring-bank rows map back into the bank, the row action is
bijective, and the induced action on each same-color clause agrees with the
full variable action.

There is also a direct structural explanation. The generic clique,
common-neighbor, connectivity, domination, family-transition, and redundant
triangle clauses are vertex-natural once all auxiliary variables are
relabelled. The reflection preserves the labeled induced \(C_5\), fixes the
distinguished external vertex 5 and the rim edge \(\{0,1\}\), swaps the two
units \(e_{05}\) and \(e_{15}\), and permutes each no-hub clause internally.
The complete coloring bank is closed under the same relabeling. The exact
multiset audit checks that this reasoning matches the frozen bytes.

## Combined \(S_6\) and reflection coverage

Let \(S\) be the accepted outer-signature sorting breaker. Its independently
rebuilt clause stream again has 315 clauses, 3,210 literals, 11,424 bytes, and
SHA-256
`ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`.
All five adjacent comparators were checked on all \(2^{12}=4,096\) assignments;
each accepts exactly the 2,080 nondecreasing ordered pairs.

Let
\[
T:\quad e_{25}\le e_{45},
\]
whose CNF clause is exactly
\[
(-24\ \ 39).
\]

The equisatisfiability claim is valid:
\[
F\text{ is satisfiable}\quad\Longleftrightarrow\quad
F\land S\land T\text{ is satisfiable}.
\]

Proof. The reverse implication is immediate. For the forward implication,
take any assignment satisfying \(F\).

1. If it violates \(T\), then \(e_{25}=1\) and \(e_{45}=0\). Apply \(\rho\).
   Exact covariance preserves \(F\), while
   \(\rho(e_{25})=e_{45}\) and \(\rho(e_{45})=e_{25}\). Thus the image has
   \(e_{25}=0,e_{45}=1\) and satisfies \(T\). If the original assignment
   already satisfies \(T\), leave it unchanged.
2. Stable-sort the six outer vertices \(6,\ldots,11\) by their six-bit
   signatures into the fixed core \(0,\ldots,5\), and apply the corresponding
   \(S_6\) relabeling to all variables. The five adjacent transpositions
   generate this \(S_6\); the audit independently confirmed full-\(F\)
   covariance for each generator. The image signatures are nondecreasing, so
   the comparator truth tables imply \(S\).
3. Every outer permutation fixes vertices \(0,\ldots,5\), hence fixes both
   \(e_{25}\) and \(e_{45}\) literal-by-literal. Therefore the sorting step
   cannot destroy \(T\).

This proves the claimed orbit coverage. The order of the operations is
important: reflect first when necessary, then re-sort the outer vertices.

## Three-edge cube reduction

In coordinate order
\[
(e_{25},e_{35},e_{45})=(x,y,z),
\]
the variable IDs are \((24,32,39)\). The frozen base formula contains exactly
one copy of each unit \(e_{05}\) and \(e_{15}\), with IDs 5 and 15, and exactly
one vertex-5 no-hub clause
\[
(-5,-15,-24,-32,-39).
\]
After the two units, that clause excludes \(xyz=111\).

The new condition \(T:x\le z\) excludes precisely `100` and `110`. Reflection
swaps \(x\) and \(z\) and fixes \(y\), pairing those two excluded assignments
with `001` and `011`, respectively. The five exhaustive representatives are
therefore exactly:

`000`, `001`, `010`, `011`, `101`.

The sixth \(T\)-satisfying pattern `111` is already impossible from the source
units and no-hub clause.

## Exact \(F\land S\land T\) bytes

Appending the independently reconstructed \(S\) stream and then the exact
9-byte line `-24 39 0\n` gives:

- 6,886 variables;
- 23,969 clauses;
- 192,171 literals;
- 754,332 bytes;
- SHA-256
  `441e54c28fdf6005f0f17fb951bf37c7ff46e222f3e605b7e715fabeec8f64d4`.

The source body is the exact prefix, the 11,424-byte signature stream is the
exact middle segment, and \(T\) is the exact suffix. A second byte
recomposition from the retained \(F\land S\) package independently reproduced
the same size and hash.

## Reproduction and limitations

- Probe:
  `reviews/hole5_rim_reflection_coverage_hostile_probe.py`,
  SHA-256
  `5a411574eef04354f38e4f048f7f1e9a08b2b376de8dea834407690722984b3c`.
- Deterministic log:
  `reviews/hole5_rim_reflection_coverage_hostile_probe_log.json`,
  SHA-256
  `a5808f2f8485fe462b308e7f1fa9c023fb6d8ab3d5c7aad871fa6516f4569dbc`.

This audit validates the reduction and exact formula construction only. Any
later SAT/UNSAT result for the five cubes still requires its own complete,
independently checked solver certificates and coverage manifest.
