# Exact bounded synthesis for the mixed-\(P_4\) witness

## Status

Date: 2026-07-26 (PDT)

**OBSERVED — exhaustive labeled orders 8 and 9.**

There is no 8- or 9-vertex realization of the exact mixed family-list
pattern in a full one-guard eternal family with
\(\gamma=\alpha=3\).  The search includes arbitrary proper eternal
subfamilies, not only greatest families.

This is exact finite evidence for the stated labeled mask spaces.  It is
not a universal theorem, an order-\(10+\) exclusion, or a
literature-priority claim.

## 1. Literal model

Use labels

\[
a=0,\ b=1,\ c=2,\quad
x_0=3,\ x_1=4,\ x_2=5,\ x_3=6,\quad
w=7
\]

and, at order nine, one arbitrary further vertex \(y=8\).

The reference state \(S=\{a,b,c\}\) is independent.  The graph induced by
\(x_0,x_1,x_2,x_3\) is the complement of the path
\(x_0x_1x_2x_3\).  The witness satisfies

\[
wx_1,wx_2\notin E(G),
\]

so \(T=\{w,x_1,x_2\}\) is independent.

The six positive list memberships are imposed as graph edges and required
family states:

\[
L_S(x_0)\supseteq\{a\},\quad
L_S(x_1)\supseteq\{a,c\},\quad
L_S(x_2)\supseteq\{b,c\},\quad
L_S(x_3)\supseteq\{b\}.
\]

The other six direct swaps are forbidden in the family.  Thus the desired
lists are exact.

Every retained family state must dominate the **entire** 8- or 9-vertex
graph.  For every retained state and every unoccupied attacked vertex,
exactly one adjacent guard must be able to move along one edge to a state
retained in the same family.

## 2. Why the proper-family search is exact

For a fixed graph, let \(\mathcal U\) be all dominating triples except the
six forbidden direct swaps.  Define

\[
\Psi(\mathcal A)=
\{D\in\mathcal A:
  \text{every unoccupied attack at }D
  \text{ has a legal successor in }\mathcal A\}.
\]

Iterate

\[
\mathcal U\supseteq\Psi(\mathcal U)
\supseteq\Psi^2(\mathcal U)\supseteq\cdots
\]

to its finite fixed point \(\mathcal K\).

If \(\mathcal F\subseteq\mathcal U\) is any eternal family, induction gives
\(\mathcal F\subseteq\Psi^i(\mathcal U)\) for every \(i\), hence
\(\mathcal F\subseteq\mathcal K\).  Conversely, a nonempty
\(\mathcal K\) is itself an eternal family.  Therefore an exact-list family
containing all required states exists if and only if every required state
survives in \(\mathcal K\).

This greatest-safe-fixed-point test covers proper families exactly.  It
does not make the scope error identified in the earlier greatest-family
census.

## 3. Exhaustive counts

The fixed adjacencies leave 11 unknown edges at order eight and 19 at order
nine.  The program checks every mask in
\([0,2^{11})\) and \([0,2^{19})\), respectively.

| condition | order 8 | order 9 |
|---|---:|---:|
| all labeled edge masks | 2,048 | 524,288 |
| \(S\) and all six positive swaps dominate | 576 | 87,552 |
| preceding row and \(\alpha=3\) | 552 | 68,688 |
| \(\gamma=\alpha=3\) | 62 | 8,985 |
| \(\gamma=\alpha=3\) and all required states dominate | 0 | 96 |
| unrestricted eternal-equality graphs in the structural pool | 9 | 1,150 |
| unrestricted greatest family contains all six positive swaps | 0 | 0 |
| nonempty safe family after all six negative swaps are banned | 0 | 0 |
| exact mixed-list realizations | **0** | **0** |

At order eight the static requirements already contradict \(\gamma=3\):
none of the 62 \(\gamma=\alpha=3\) graphs makes all required states
dominating.

At order nine, 96 graphs pass every static requirement.  Of those, only 42
have any eternal three-family.  In their unrestricted greatest families at
most four of the six required positive swaps survive closure.  The four
closest masks are

\[
89928,\quad106372,\quad352072,\quad368516.
\]

After the six negative swaps are banned, the safe fixed point becomes empty
for every one of the 96 masks in two or three simultaneous deletion waves.

The independently developed projection-gluing enumerator reported the same
stage counts \(576,552,62,0\) and
\(87\,552,68\,688,96,0\).  The two implementations use different
prefilters and result layouts.  This agreement is a cross-check, not a
universal proof.

## 4. Forced-edge diagnostics

Because the exact survivor sets are empty, there are no nonvacuous edges
forced across exact realizations.

The weaker frontiers show why a single graph-edge lemma did not emerge:

- among all 62 order-eight \(\gamma=\alpha=3\) masks, every one of the 11
  unknown adjacencies occurs both as an edge and as a nonedge;
- among all 8,985 order-nine \(\gamma=\alpha=3\) masks, every one of the 19
  unknown adjacencies occurs both ways;
- the same is true across the 96 order-nine masks where all required states
  dominate.

For context only:

- the nine unrestricted eternal-equality graphs at order eight all have
  \(wx_0,wx_3\notin E(G)\);
- among the 14 unrestricted order-nine graphs attaining the global maximum
  of five positive swaps, \(cy\) is always an edge, while
  \(ax_3,bx_0,cw,x_0y,x_3y\) are always nonedges.

These latter intersections are finite cohort observations, not analytic
lemmas.

## 5. Hostile strengthening searches

### 5.1 No bounded base-ordering counterexample

The independent states \(S=\{a,b,c\}\) and
\(T=\{w,x_1,x_2\}\) are disjoint.  For every unrestricted
eternal-equality graph in the pool, a CEGAR search considered arbitrary
proper eternal subfamilies containing \(S,T\).

Whenever the current greatest safe family contained a subset-compatible
base cube for some bijection \(S\to T\), the search branched on omitting
one of that cube's six interior states and recomputed the greatest safe
family.  Any non-base-orderable target family must lie in one such branch,
so the branching is complete.

The search used 63 fixed points over the nine order-eight graphs and 8,914
fixed points over the 1,150 order-nine graphs.  It found zero
non-base-orderable proper families.  This is bounded evidence for the open
base-orderability question, not a proof.

### 5.2 A disjunctive-response counterexample

At order nine there are 18 unrestricted eternal-equality graphs with the
following property:

1. no eternal family avoids all six negative direct-swap states;
2. for each individual negative state \(q\), some eternal family avoids
   \(q\).

Thus the finite obstruction need not select one family-independent extra
response.  The first exemplar is

\[
G=\texttt{HCxrs`c}
\]

at mask 39588.  Its greatest eternal family has 39 states.  The complete
state records for the distinct safe families are stored in the order-nine
JSON.

This refutes the tempting strengthening “joint closure failure forces one
specific forbidden response in every eternal family.”  It does not refute
any accepted lemma in the source notes.

## 6. Scope comparison with permissive local closure

A separate permissive named-state calculation produced eight local masks
with the additional mandatory edges

\[
cx_0,\ bx_1,\ ax_2,\ cx_3,\ aw,\ bw,\ wx_0,\ wx_3.
\]

Those masks are outside the present equality frontier.  In every one,
\(\{a,x_1\}\) dominates all eight vertices:

- \(a,x_1\) occupy themselves;
- \(x_1\) dominates \(b,c,x_3\);
- \(a\) dominates \(x_0,x_2,w\).

Hence \(\gamma=2\).  If a further vertex \(y\) has
\(L_S(y)\supseteq\{a\}\), then \(ay\in E(G)\), so the same pair also
dominates \(y\).  The corresponding 12 local \(y\)-models likewise cannot
be equality realizations.

The assumption mismatch is therefore:

- the permissive calculation enforces a selected named/local transition
  system;
- the present calculation requires every family state to dominate the full
  graph and enforces \(\gamma=3\) by excluding every dominating pair.

Both calculations are internally useful, but their survivor counts answer
different questions.

## 7. Exact gamma-2 countermodel

After the independent formulation and preliminary exhaustion were fixed,
the graph

\[
G=\texttt{HDzruf]}
\]

was supplied as a stress test.  Independent decoding and recomputation
give:

\[
(\gamma,\alpha,\gamma^\infty)=(2,3,3);
\]

- the greatest safe family after the six negative swaps are banned has 46
  states;
- all \(46(9-3)=276\) literal attack obligations pass; and
- at \(S\),
  \[
  L(x_0)=\{a\},\quad L(x_1)=\{a,c\},\quad
  L(x_2)=\{b,c\},\quad L(x_3)=\{b\},\quad
  L(w)=L(y)=\{a,b\}.
  \]

This is an exact counterexample to any equality-free claim that literal
closure plus the displayed \(W/Y\) witness layers eliminates the mixed
path.  Its decisive defect is the dominating pair \(\{a,x_1\}\), so it is
not an equality realization.

## 8. Reproduction and artifacts

Run:

```text
python3 math/working/mixed_witness_local_synthesis/mixed_witness_local_synthesis.py \
  --order 8 \
  --output results/mixed_witness_local_synthesis/order8.json \
  --checkpoint results/mixed_witness_local_synthesis/order8.checkpoint.json \
  --log results/mixed_witness_local_synthesis/order8.log

python3 math/working/mixed_witness_local_synthesis/mixed_witness_local_synthesis.py \
  --order 9 \
  --output results/mixed_witness_local_synthesis/order9.json \
  --checkpoint results/mixed_witness_local_synthesis/order9.checkpoint.json \
  --log results/mixed_witness_local_synthesis/order9.log
```

The checkpoint files contain the next mask, all counters, and all retained
mask lists.  `--resume` continues a run whose source hash and mask interval
match.  A completed-checkpoint resume was tested and reproduced identical
output bytes.

| artifact | SHA-256 |
|---|---|
| source | `d2e565eeaae4f04cdace53e08657cdaaf84b51bec83e7fe23822aaee77640c4d` |
| order-8 JSON | `ae752b8aaf6b2cad693c1183d22d42ce04160b4ece2a58324f3d57615f7481a5` |
| order-8 log | `a0b16aac03e74af7707cdfd1419fd70ddc2c50644cb8ff3a02a2cb958d8c8636` |
| order-8 checkpoint | `5d134503c84d907046d848e04857adf90f6798dc8c5bb11c112f98b37ad0db4a` |
| order-9 JSON | `45ce01d4ef36b1d90e5bb593506976897edeaa972921407ddd4108dbb10609c1` |
| order-9 log | `38cc12c99a748f30683d2eac39b2b52672d35d582bb5404bfa0472ba27810837` |
| order-9 checkpoint | `5a50aa1939753e0b15089a954519bb25be88dccb18a5272391653af227d052f6` |

## 9. Exact stopping boundary

The bounded result closes the proper-family loophole at orders eight and
nine for this exact mixed-\(P_4\) pattern.  It does not prove that larger
equality graphs cannot realize the pattern.  The first additional vertex
beyond order nine could simultaneously:

1. repair domination of a required positive state;
2. destroy a dominating pair; and
3. supply closure successors absent from the nine-vertex fixed points.

The next analytic step therefore remains a witness-proliferation or
multi-projection compatibility argument.  A larger brute-force search is
not justified by this bounded result.
