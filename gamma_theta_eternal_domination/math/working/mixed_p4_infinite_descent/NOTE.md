# One endpoint defect excludes the exact static mixed \(P_4\)

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, one adjacent guard moves to
the attacked vertex, and the successor remains in the specified eternal
family.

Let \(G\) satisfy

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]

let \(\mathcal F\) be an arbitrary eternal family of dominating triples,
let

\[
 S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).

The new conclusion is:

> **THEOREM — PROVED BY A COMPLETE 32-COMPLETION LOCAL KERNEL.**
> There is no induced path
> \[
> x_0x_1x_2x_3
> \]
> in \(H\) whose four static dominating-swap lists at \(S\) are
> \[
> \{a\},\qquad \{a,c\},\qquad \{b,c\},\qquad \{b\}.
> \]

Equivalently, the exact static \(Y_3=P_4\) gluing obstruction isolated in
C-118 and bounded below by C-121 cannot occur at any order.  C-121's
conditional order floor \(n\geq14\) is therefore superseded for this exact
pattern by a universal exclusion.

The proof is local.  C-121 produces one endpoint defect \(d\).  On the
eight vertices

\[
 \{a,b,c,x_0,x_1,x_2,x_3,d\}
\]

exactly five graph adjacencies remain undecided.  For all \(2^5=32\)
completions, the greatest core-dominating,
restoration-compatible one-guard kernel is empty.  External vertices
cannot repair this: a one-guard response to an attack at a displayed
vertex from a displayed triple is another displayed triple.

This theorem excludes one exact static minimal obstruction.  It does
**not** exclude:

- the exact *family*-list mixed \(P_4\) when some static lists are larger;
- arbitrary longer two-unit chains or one-unit lollipops;
- unit-free bicycles;
- the full-response-list branch;
- all of \(k=3\); or
- the universal gamma--theta conjecture.

No literature-priority claim is made.

## 1. Accepted input and the single forced defect

Assume for contradiction that the displayed exact static lists exist.
Accepted C-121 proves static-to-family rigidity, so the family-response
lists are exactly

\[
\begin{array}{c|ccccc}
v&x_0&x_1&x_2&x_3\\ \hline
L_S^{\mathcal F}(v)&
\{a\}&\{a,c\}&\{b,c\}&\{b\}.
\end{array}
\tag{1.1}
\]

Accepted C-070 then gives endpoint saturation

\[
 cx_0,cx_3\in E(G).
\tag{1.2}
\]

Because \(c\) is absent from the **static** list at \(x_0\), the graph
edge \(cx_0\) cannot produce a dominating direct swap.  Thus

\[
 S-c+x_0=\{a,b,x_0\}
\]

misses some vertex \(d\).  Consequently

\[
 da,db,dx_0\in E(H).
\tag{1.3}
\]

The vertex \(d\) is distinct from all seven original vertices.  It is
not in the failed state; it is not \(c\), because \(cx_0\in E(G)\); it is
not \(x_1\), since \(ax_1\in E(G)\); it is not \(x_2\), since
\(bx_2\in E(G)\); and it is not \(x_3\), since \(bx_3\in E(G)\).

The independent reference state \(S\) dominates \(d\).  Equations (1.3)
leave only \(c\), so

\[
 cd\in E(G).
\tag{1.4}
\]

The triple \(\{a,b,d\}\) is independent.  Since \(\alpha(G)=3\), it is a
maximum independent set and therefore belongs to every eternal
triple-family.  Relative to \(S\), this is the direct \(c\)-replacement.
The graph nonedges in (1.3) exclude the other two roles, hence

\[
 L_S^{\mathcal F}(d)=\{c\}.
\tag{1.5}
\]

Finally, (1.1) puts both

\[
 \{a,b,x_1\},\qquad \{a,b,x_2\}
\]

in \(\mathcal F\).  Each state must dominate \(d\), while \(a\) and \(b\)
both miss \(d\).  Therefore

\[
 dx_1,dx_2\in E(G).
\tag{1.6}
\]

No second endpoint defect, witness clique, infinite recurrence, or
greatest-family assumption is needed.

## 2. The eight-vertex incidence ledger

Label

\[
(a,b,c,x_0,x_1,x_2,x_3,d)=(0,1,2,3,4,5,6,7).
\]

The fixed graph edges are

\[
\begin{split}
&ax_0,ax_1,cx_1,bx_2,cx_2,bx_3,cx_0,cx_3,\\
&x_0x_2,x_0x_3,x_1x_3,\\
&cd,dx_1,dx_2.
\end{split}
\tag{2.1}
\]

The first line consists of the six positive response incidences and the
two endpoint-saturation edges.  The second line is inducedness of the
complement \(P_4\).  The third line is (1.4)--(1.6).

The fixed graph nonedges are

\[
ab,ac,bc,\qquad
x_0x_1,x_1x_2,x_2x_3,\qquad
ad,bd,x_0d.
\tag{2.2}
\]

The only undecided pairs are

\[
\boxed{bx_0,\ bx_1,\ ax_2,\ ax_3,\ x_3d.}
\tag{2.3}
\]

The count is complete:

\[
14\text{ fixed edges}
+9\text{ fixed nonedges}
+5\text{ optional pairs}
=\binom82=28.
\tag{2.4}
\]

The exact response lists used by the local calculation are

\[
\begin{array}{c|ccccc}
v&x_0&x_1&x_2&x_3&d\\ \hline
L_S^{\mathcal F}(v)&
\{a\}&\{a,c\}&\{b,c\}&\{b\}&\{c\}.
\end{array}
\tag{2.5}
\]

## 3. The local-kernel lemma

### Lemma 3.1 (one-defect kernel exclusion)

For every completion of the five optional pairs in (2.3), there is no
eternal triple-family containing \(S\) and satisfying the incidences and
exact lists (2.1)--(2.5).

### Coverage and proof

Fix one completion and let \(\mathcal A_0\) consist of every triple of the
eight displayed vertices which:

1. dominates the displayed induced subgraph; and
2. satisfies arbitrary-state restoration relative to \(S\):
   \[
   S-D\subseteq
   \bigcup_{v\in D-S}L_S^{\mathcal F}(v).
   \tag{3.1}
   \]

Starting from \(\mathcal A_0\), synchronously delete a triple whenever it
has an unoccupied displayed attack with no legal one-edge, one-guard
successor remaining.  Write

\[
 \mathcal A_{r+1}=\Phi(\mathcal A_r).
\tag{3.2}
\]

This descending process reaches the empty set for all \(32\) completions.
The initial sets have sizes \(28\) through \(32\), and the reference
state is deleted in rounds two through five.

This finite deletion proves the global statement.  If an actual eternal
family \(\mathcal F\) existed, its displayed-core portion

\[
 \mathcal F_C=\{D\in\mathcal F:D\subseteq C\},
 \qquad
 C=\{a,b,c,x_0,x_1,x_2,x_3,d\},
\tag{3.3}
\]

would satisfy \(\mathcal F_C\subseteq\mathcal A_0\):

- every family state dominates all of \(G\), hence the induced core; and
- accepted arbitrary-state restoration gives (3.1).

Moreover, for a displayed state and an unoccupied displayed attack,
every one-guard successor is again a displayed triple.  Eternal closure
therefore makes \(\mathcal F_C\) closed under every attack used in
(3.2).  Induction gives

\[
 \mathcal F_C\subseteq\mathcal A_r
\qquad(r\geq0).
\tag{3.4}
\]

But \(S\in\mathcal F_C\), while the terminal set is empty.  This is the
contradiction.

The two checkers use different representations:

- `verify.py` uses adjacency sets and `frozenset` configurations, checks
  the complete pair partition, records every synchronous deletion row,
  and reconstructs both scope controls;
- `verify_bitset.py` independently uses packed integer neighborhoods and
  configurations and reproduces all \(32\) initial sizes, deletion-round
  sizes, and reference deletion ranks.

The first \(16\) rows, where \(x_3d\notin E(G)\), reproduce C-121's
accepted double-defect table: then \(d\) is also an \(x_3\)-defect.  The
new half is \(x_3d\in E(G)\).  With the low four mask bits ordered as

\[
(bx_0,bx_1,ax_2,ax_3),
\]

its complete table is:

| low mask | \(|\mathcal A_0|\) | synchronous deletion sizes | round deleting \(S\) | fatal attack at \(S\) |
|---:|---:|---|---:|---|
| 0 | 29 | 10, 13, 6 | 2 | \(x_1\) |
| 1 | 30 | 8, 15, 7 | 3 | \(x_1\) |
| 2 | 30 | 8, 9, 6, 5, 2 | 2 | \(x_1\) |
| 3 | 31 | 7, 10, 6, 6, 2 | 3 | \(x_1\) |
| 4 | 30 | 8, 8, 10, 4 | 4 | \(x_0\) |
| 5 | 31 | 6, 11, 10, 4 | 4 | \(x_0\) |
| 6 | 31 | 6, 3, 2, 6, 4, 6, 4 | 5 | \(x_1\) |
| 7 | 32 | 5, 5, 2, 6, 4, 6, 4 | 5 | \(x_1\) |
| 8 | 29 | 9, 11, 9 | 3 | \(x_1\) |
| 9 | 30 | 6, 13, 10, 1 | 4 | \(x_0\) |
| 10 | 30 | 7, 8, 5, 6, 4 | 3 | \(x_1\) |
| 11 | 31 | 5, 9, 6, 6, 5 | 4 | \(x_0\) |
| 12 | 30 | 8, 8, 10, 4 | 4 | \(x_0\) |
| 13 | 31 | 5, 12, 10, 4 | 4 | \(x_0\) |
| 14 | 31 | 6, 3, 2, 6, 4, 6, 4 | 5 | \(x_1\) |
| 15 | 32 | 4, 6, 2, 6, 4, 6, 4 | 5 | \(x_1\) |

Every row sums to its initial size, so the terminal local kernel is
literally empty.

## 4. Why the proposed singleton descent does not iterate

C-121's endpoint defects all lie in

\[
 U=N_H(a)\cap N_H(b),
\]

which is a clique in \(G\), and every such defect has singleton list
\(\{c\}\).  This does **not** itself force an external next generation.
For a defect \(d\):

- the pair \(\{a,d\}\) already has \(b\) as a common neighbor in \(H\);
- the pair \(\{b,d\}\) already has \(a\) as a common neighbor in \(H\);
- in the frozen projections, \(d\) lies in an anchor-fixed component,
  not in a fresh free component to which C-124 polarization would apply.

Thus the naive recurrence “a singleton defect forces a fresh singleton
defect” is unsupported.  The equality graph

```text
HCOceRy
```

is an exact boundary control.  It has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3),
\]

and at \(S=\{0,1,2\}\) its greatest eternal family has two adjacent
vertices \(3,6\) with

\[
 L_S(3)=L_S(6)=\{0\},
\qquad
 N_H(3)\cap S=N_H(6)\cap S=\{1,2\}.
\]

So even a same-color pure singleton \(G\)-clique is compatible with full
equality.  The contradiction in Lemma 3.1 uses the complete mixed-\(P_4\)
incidence and response system, not an unproved recurrence.

## 5. Other boundary controls

The graph

```text
FDzro
```

has

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3)
\]

and a checked 21-state proper eternal family with exact family lists

\[
\{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
\]

Its static lists are instead

\[
\{a,c\},\quad
\{a,b,c\},\quad
\{a,b,c\},\quad
\{b,c\}.
\]

It therefore does not contain the endpoint defect used in Section 1 and
does not contradict the theorem.  It also shows why the theorem must not
be restated as an exclusion of the family-list pattern without the static
hypothesis.

The accepted graph-specific control

```text
IzM]XTR`W
```

satisfies the principal static complement conditions used in the gluing
program and has

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,3,4,4).
\]

Its complete triple kernel is empty.  This is consistent with the new
local theorem and shows that the eternal-three-family hypothesis is doing
real work.

## 6. Consequence and exact stopping boundary

The exact static \(Y_3=P_4\) is universally impossible under
\(\gamma=\alpha=\gamma^\infty=3\).  In particular, it cannot be the
uncolorable static response-list obstruction in a parameter-three
counterexample.

This removes the shortest exact static two-unit/one-clause core.  It does
not establish that every uncolorable static response-list instance
contains this core.  The remaining gluing problem still permits longer
unit chains, lollipops, residual bicycles, and full lists.  Therefore no
complete \(k=3\) theorem and no resolution of the gamma--theta conjecture
is claimed here.

## 7. Reproduction

From the campaign root:

```text
python3 -I -B -W error \
  math/working/mixed_p4_infinite_descent/verify.py

python3 -I -B -W error \
  math/working/mixed_p4_infinite_descent/verify_bitset.py
```

Both commands must print JSON with verdict `PASS`.
