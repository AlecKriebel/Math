# Independent order-13, parameter-three constructor audit

**Audit date:** 2026-07-26  
**Scope:** the four `hole5`, `hole7`, `hole9`, and `hole11` formulas proposed
for the order-13, \(k=3\) frontier, plus a separate check of the discovered
`hole11` two-outside-vertex reduction.  
**Solver use:** none.

## Verdict

**`ACCEPT_EXACT_CLEAN_ROOM_RECONSTRUCTION`**

The standard-library-only reconstructor in `reconstruct.py` imports no
production search, synthesis, coloring, transition, or verifier code.  It
independently allocates all variables, derives every semantic clause family,
enumerates the complete first-use-canonical coloring bank, serializes and
strictly reparses DIMACS, and compares the result with the frozen exploratory
census and hashes.

All four complete formulas agree byte for byte:

| template | variables | base clauses | color rows | full clauses | bytes | SHA-256 |
|---|---:|---:|---:|---:|---:|---|
| `hole5` | 9,802 | 29,791 | 10,935 | 40,726 | 1,805,539 | `8df56270...d2fb5` |
| `hole7` | 9,802 | 29,800 | 5,103 | 34,903 | 1,372,338 | `3e1c86cc...6c340` |
| `hole9` | 9,802 | 29,813 | 2,295 | 32,108 | 1,168,197 | `3fff100c...e95e9ea` |
| `hole11` | 9,802 | 29,830 | 1,023 | 30,853 | 1,076,723 | `1ab880e6...e901` |

There is no disagreement in variable count, clause count, literal count,
byte size, or SHA-256.  There is no implementation blocker to freezing a
dedicated order-13 constructor.  This audit does not establish that any
formula is unsatisfiable.

## Independent derivation

The variable universe is the disjoint contiguous union of:

- 78 variables \(e_{uv}\) for edges of \(H=\overline G\);
- 858 variables \(w_{ab,c}\) certifying an external common neighbor \(c\)
  for each pair \(a,b\);
- 286 variables \(f_T\) selecting three-vertex eternal-family states; and
- 8,580 variables \(m_{T,r,u}\), defined only for \(r\notin T\) and
  \(u\in T\).

The checker has a clause-specification path separate from the generation
path.  It independently reconstructs and compares the tagged clause
multisets for:

1. no \(K_4\) in \(H\);
2. an external common H-neighbor for every pair;
3. the induced odd-hole rim, named common neighbor, and hub-free clauses;
4. all 4,095 connectedness cuts for \(G\);
5. domination by every selected state;
6. nonemptiness of the selected family;
7. exactly one moved guard, an \(H\)-nonedge for its traversed \(G\)-edge,
   and the selected successor \(T-u+r\);
8. forced selection of every H-triangle; and
9. one same-color H-edge clause for every canonical proper coloring of the
   forced-positive template graph.

For coloring-bank completeness, the audit separately enumerates all
\(3^{13}\) named color rows, counts those proper on the forced-positive
template edges, verifies the free color-permutation action supplied by the
fixed triangle, and checks that the restricted-growth bank has exactly one
row from every orbit.  No forced-negative edge is incorrectly treated as a
coloring constraint.

The only graph-label restriction is the proved hole-plus-named-common-
neighbor template.  The only coloring quotient is color-name
canonicalization.  There is no unrelated anchor, DoubleLex, signature,
reflection, or other symmetry breaker.

## Deliberate model-error suite

Each of the following eight mutations was introduced separately in every
template and rejected by the independent semantic check and/or exact frozen
bytes:

| mutation | detected in all four |
|---|---|
| attacks allowed at occupied vertices | yes |
| multi-guard successor substituted for \(T-u+r\) | yes |
| successor domination requirement omitted | yes |
| \(G/H\) move-edge sign reversed | yes |
| one coloring obstruction omitted | yes |
| no-\(K_4\), hence \(\alpha\leq3\), omitted | yes |
| pair-common-neighbor, hence \(\gamma\geq3\), omitted | yes |
| unrelated fixed anchor added | yes |

This suite is evidence that the byte agreement is sensitive to the model
errors most likely to invalidate the finite target.  It is not a substitute
for a proof checker after a solver run.

## Independent `hole11` reduction check

**`AGREE_NO_INDEXING_FLAW_FOUND`**

Let \(x,y\) be the two vertices outside the induced \(C_{11}\) in \(H\), and
let \(X,Y\) be their respective rim nonneighbor sets in \(H\).
Hub-freeness makes both nonempty.  Rim-edge common-neighbor forcing gives
\(X\cap Y=\varnothing\).  If \(a\in X\) and \(b\in Y\), neither outside
vertex can be a common H-neighbor of the distinct rim pair \(a,b\); in an
induced \(C_{11}\), a rim common neighbor exists exactly when the cyclic
distance is two.  Thus every member of \(X\) is at cyclic distance two from
every member of \(Y\).

Independent enumeration gives 44 ordered nonempty set pairs before
quotienting and exactly two orbits under \(D_{22}\times S_2\):

\[
 (X,Y)=(\{0\},\{2\}),\qquad
 (X,Y)=(\{0\},\{2,9\}).
\]

In every case a rim edge is disjoint from \(X\cup Y\).  If \(xy\) were an
H-edge, that rim edge together with \(x,y\) would induce a \(K_4\), so
\(xy\notin E(H)\).

For both representatives, the direct \(G\)-adjacency checker confirms the
same attack tree from the maximum independent state
\(\{4,5,11\}\):

- attack 0 has exactly the dominating successors
  \(\{0,5,11\}\) and \(\{0,4,11\}\);
- \(\{0,4,11\}\) has no dominating response to attack 2;
- \(\{0,5,11\}\) has the unique dominating response
  \(\{0,7,11\}\) to attack 7; and
- \(\{0,7,11\}\) has no dominating response to attack 9.

Thus the reported indexing and both representatives agree.  Promoting this
finite check to a written theorem still requires explicitly citing the
accepted pair-common-neighbor and maximum-independent-state lemmas at the
two implication points.

## Reproduction

From the campaign directory:

```text
python3 reviews/order13_k3_constructor_independent/reconstruct.py evidence |
  cmp - reviews/order13_k3_constructor_independent/evidence.json

python3 reviews/order13_k3_constructor_independent/hole11_reduction_check.py |
  cmp - reviews/order13_k3_constructor_independent/hole11_reduction_evidence.json
```

The first replay takes about ten seconds on the campaign MacBook and invokes
no solver.  It enumerates the labeled coloring rows afresh rather than
trusting the retained bank counts.

## Claim boundary

- **Established by this audit:** exact clean-room reconstruction and strict
  parsing of all four proposed formulas; complete template-coloring banks;
  detection of all named semantic mutations; finite confirmation of the
  stated `hole11` orbit classification and attack tree.
- **Not established:** formula UNSAT, a checked SAT proof, exclusion of all
  order-13 \(k=3\) targets, or the full conjecture.
- **Next gate:** bind a dedicated production constructor to these exact
  bytes, then retain and independently replay a proof-producing result.
