# Hostile audit: paired-repair implication obstruction

Date: 2026-07-28 (PDT)

## Verdict

**UNCONDITIONAL PASS on the reviewed bytes.**

The logical path-replacement statement, the distinction between
resolution-derived units and physical response terminals, and the exact
19-vertex gamma-two control all survive independent reconstruction.  The
control proves the claimed limitation of a one-witness/local-closure
descent.  It does not prove or disprove the gamma--theta conjecture and does
not refute a future argument that uses the no-dominating-pair hypothesis
globally.

Reviewed source SHA-256 values:

```text
NOTE.md     4508baf996fd69e93d435b7a5da390e847a28c0f3b2c2593b9f1eb45f734456e
verify.py   770c131140863e7acbc57669541fafe56ec4172d558a0569ec2827f0794a6d85
result.json 8d3c313af95d17897c33c4fc0dbf14a82609679f2018f204883f7b76ce3dd438
```

## 1. Logical audit

### 1.1 Oriented substitution and strict descent

For

\[
 A=\neg X\lor Q,\qquad B=Y\lor\neg Q,
\]

the implication graph contains exactly the two oriented two-arc routes

\[
 X\to Q\to Y,\qquad
 \neg Y\to\neg Q\to\neg X.
\]

If a marked \(X\)-to-\(Y\) segment of a simple implication path has \(d\)
arcs and \(Q\) is new, substituting the first route deletes \(d\) arcs and
adds two.  The resulting marked path has length

\[
 |P|-d+2.
\]

The reverse contradiction path is untouched.  Thus the displayed marked
bicycle strictly shortens exactly when \(d>2\), is unchanged when \(d=2\),
and lengthens when \(d=1\).  There is no hidden appeal to shortestness:
shortest contradiction paths do not imply \(d>2\).

The contraposed route gives the same numerical substitution in the
contraposed copy.  It supplies no second decrease.

### 1.2 Derived units are not response-formula units

The arm resolvent is

\[
 C=\neg X\lor Y.
\]

Resolving \(C\) with the two inequality consequences

\[
 \neg X\lor\neg Y,\qquad X\lor Y
\]

gives \(\neg X\) and \(Y\), respectively.  These are resolution
consequences.  They are not thereby unit clauses in the selected response
formula, singleton response lists, or a single physical terminal port.

The control makes the distinction exact.  Its arm-containing
inclusion-minimal core has ten clauses, all binary.  The independently
rebuilt opposite route implies both inequality clauses, and the arm
resolvent derives the two endpoint units, while the formula still has zero
syntactic units.  It is therefore in the unit-free case of the accepted
minimal-2-CNF trichotomy.

The source also respects the hypotheses of the cited physical theorems:

- C-079 needs an actual positive-response port, an odd physical
  omitted-color path, and one physical complement neighbor incident with
  that port and both path ends.
- C-094 identifies a same-sign Boolean event but does not move the
  complement edges supporting a clause.
- C-095 is an exact countercontrol to such edge transport.
- C-098 can replace a failed incidence by another virtual gate; it does
  not create a singleton response vertex.
- C-086 does not claim to exclude every arbitrarily long two-unit chain.

Accordingly, the note does not smuggle a resolution derivation into a
one-guard attack argument.

## 2. Independent graph and game reconstruction

`independent_check.py` starts from the graph6 record

```text
RBn]r]vj]lnZ~^~n~z~^z|~nz~^j~w
```

and decodes it directly.  It does not import the source verifier or any
campaign evaluator.  The decoded graph has 19 vertices and 139 edges; its
32-edge complement is exactly the edge set displayed in the note.

The clean-room bit-mask checks give

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

More explicitly:

- no singleton dominates;
- exactly 93 pairs dominate, the first lexicographically being
  \(\{0,11\}\);
- 20 of those pairs are independent, so \(i=2\);
- \(\{0,1,2\}\) is independent and no independent four-set exists;
- the greatest two-guard fixed point is empty, with simultaneous deletion
  rounds \(91,2\);
- the anchor is a triangle in the complement, and the 3-coloring frozen in
  `result.json` is proper on all 32 complement edges.

Thus the claimed value \(\gamma^\infty=3\) is independently established
both by the empty two-guard kernel and by the nonempty eternal triple
family below.  It does not rely solely on reusing the source evaluator.

### 2.1 Restricted eternal family

There are 900 dominating triples.  From these, the checker excludes the 16
forbidden direct anchor swaps and independently performs simultaneous
greatest-fixed-point deletion.  The deletion rounds are

```text
51, 37, 63, 29, 10
```

and the fixed point has 703 states with canonical family hash

```text
c116c4a60299fea35d30bf09bda9b1faa31b39533caac8eb265818cd1347874d
```

Every retained state dominates.  For each of its 16 unoccupied attacked
vertices, the checker requires a successor obtained by moving exactly one
guard along a graph edge to the attacked vertex.  All

\[
703\cdot16=11{,}248
\]

obligations pass.  Occupied vertices are never treated as attacks.

Reconstructing direct responses from the fixed point gives exactly the 16
two-lists in the note.  No singleton or full outside list occurs.

The audit agrees with the source's important boundary: this is the greatest
closed family subject to the displayed direct-state restriction, not a
claim that it is the unrestricted greatest triple-family.

## 3. Response formula, cores, and marked paths

The checker independently bipartitions all same-type complement
components, verifies their bipartiteness, and derives cross clauses from
proper-coloring semantics.  It obtains the same seven variables and eleven
edge-supported clauses as the note.  A separate truth-table comparison
checks, for all \(2^7\) component orientations, that the CNF is true exactly
when every cross-type complement edge is properly colored.

Exhausting all clause subsets gives:

- the unique minimum-cardinality unsatisfiable core
  \[
  I_0=(0,1,3,4,5,7,8,9,10),\qquad |I_0|=9;
  \]
- the unique smallest inclusion-minimal unsatisfiable core containing both
  arm clauses
  \[
  I_q=(0,1,2,3,4,5,6,7,8,9),\qquad |I_q|=10.
  \]

Both are inclusion-minimal and every selected clause is binary.  Clauses 2
and 6 resolve on variable 3 to

\[
\neg4\lor6,
\]

which is exactly clause 10.

Independent breadth-first implication searches give the marked shortest
lengths

\[
\begin{array}{c|cc}
&4\leadsto\neg4&\neg4\leadsto4\\ \hline
I_0&4&5\\
I_q&5&5.
\end{array}
\]

The displayed subdivided forward path in the note is legal.  There is also
another forward shortest path of length five in \(I_q\), which does not
affect the claim.  The reverse five-arc path is literally retained in both
cores.

## 4. Tight gates and the dynamic almost-cap

All three rows of the claimed gate table pass the complete physical edge
check, including:

- both cap arms;
- the original cross edge;
- the length-two same-type physicalization path;
- the anchor-to-cap complement edge;
- the failed-pair graph edge.

Truth-table elimination of each three-clause gate leaves exactly equality
of its two local cyclic chirality coordinates.  Each of

\[
3\,7,\qquad4\,8,\qquad5\,6
\]

joins opposite sides of one same-type projection component and therefore
reverses local chirality.  Three preserving gates and three reversing
connectors give the claimed odd holonomy and reproduce the nine-clause
unsatisfiable core \(I_0\).

For the selected pair \(\{4,6\}\), vertex 18 is the unique common
complement neighbor.  It has exact list \(\{1,2\}\), both edges
\(4\,18,6\,18\) lie in the complement, and \(0\,18\) lies in the original
graph.  It is therefore exactly the claimed third-type dynamic almost-cap.
Its two clauses are indices 2 and 6.

This control sharply realizes the obstruction: replacing essential clause
10 by its two arm clauses changes the shortest marked forward path from
four to five and yields another inclusion-minimal binary bicycle.  Because
the graph has 93 dominating pairs and \(\gamma=2\), it does not refute a
descent theorem that uses \(\gamma=3\) at further pairs.

## 5. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/paired_repair_implication/verify.py \
  --check math/working/paired_repair_implication/result.json

python3 -I -B -W error \
  reviews/paired_repair_implication_hostile/independent_check.py
```

Both commands return `PASS`.  The second command rewrites
`evidence.json` from the current source bytes, so a later source edit
invalidates the reviewed hashes until the independent audit is rerun.
