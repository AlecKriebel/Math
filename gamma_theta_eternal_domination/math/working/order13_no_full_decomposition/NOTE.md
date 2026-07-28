# The order-13 no-full branch: a sound response-type decomposition

## Status and exact scope

Date: 2026-07-27 (PDT)

Let \(G\) satisfy

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]

let \(\mathcal F\) be an eternal family of triples, and let
\(S=\{a,b,c\}\in\mathcal F\) be independent.  Put \(H=\overline G\).
For \(x\notin S\), write

\[
L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\tag{0.1}
\]

This note treats the **no-full branch**

\[
1\leq |L(x)|\leq2\qquad(x\notin S).
\tag{0.2}
\]

The human results proved here are:

1. if at most one two-list type occurs, then \(H\) is 3-colorable;
2. every occurring two-list type forces two distinct vertices with the
   corresponding pure anchor signature, joined by an edge of \(H\);
3. if a neutral vertex exists, the nonneutral anchor signatures cover all
   three anchors; and
4. on 13 vertices, a no-full counterexample must have at least five
   nonneutral vertices and at most five neutral vertices.  If all three
   two-list types occur, the bounds improve to six and four.

The tight five-nonneutral case has an explicit signature normal form
recorded in Corollary 4.3.

These are structural reductions, not an exclusion of the complete
order-13 no-full branch and not a resolution of the gamma--theta
conjecture.

An earlier draft incorrectly asserted that \(\gamma\geq3\) forces three
outside vertices having double anchor signatures.  That is false: for a
pair of anchors, the third anchor already witnesses failure of domination.
The incorrect claim and its derived bounds
\(|A|\geq7,\ |Q|\leq3\) are explicitly retracted and are not used below.

## 1. Definitions and accepted inputs

For \(x\notin S\), define its anchor signature

\[
\sigma(x)=N_H(x)\cap S.
\tag{1.1}
\]

Since \(S\) dominates \(G\), \(\sigma(x)\ne S\).  Partition the ten
outside vertices at order 13 as

\[
Q=\{x\notin S:\sigma(x)=\varnothing\},
\qquad
A=\{x\notin S:\sigma(x)\ne\varnothing\}.
\tag{1.2}
\]

Thus \(Q\) is the set of vertices that are \(G\)-complete to \(S\).
Membership \(u\in L(x)\) forces \(ux\in E(G)\), because the retained
state \(S-u+x\) must dominate the omitted anchor \(u\).  Consequently

\[
L(x)\subseteq S-\sigma(x).
\tag{1.3}
\]

For \(i\in S\), say that **type \(i\)** occurs if some outside vertex has

\[
L(x)=S-\{i\}.
\tag{1.4}
\]

Let \(T\subseteq S\) be the set of occurring omitted colors and put
\(t=|T|\).

We use three previously proved family statements.

1. **Frozen projection.**  For
   \[
   W_i=\{x\notin S:i\notin L(x)\},
   \]
   the induced graph
   \[
   H[(S-\{i\})\cup W_i]
   \tag{1.5}
   \]
   is bipartite.
2. **Singleton safety.**  If
   \(L(x)=L(y)=\{i\}\), then \(xy\in E(G)\).
3. **Physical representative.**  If type \(i\) occurs, then there is a
   vertex \(z_i\notin S\) such that
   \[
   L(z_i)=S-\{i\},
   \qquad
   \sigma(z_i)=\{i\}.
   \tag{1.6}
   \]

The frozen-projection statement is Corollary 5 of
`math/working/k3_cross_state_attack.md`; singleton safety is Corollary 9 of
`math/working/universal_complement_local_balance_attack.md`; and the third
statement is Corollary 2.3 of
`math/working/separated_core_n14_attack/NOTE.md`.  None interprets a
missing family response as a graph nonedge.

## 2. At least two two-list types

### Theorem 2.1 (one type gives an ordinary 3-coloring) — PROVED

If \(t\leq1\), then

\[
\chi(H)\leq3.
\tag{2.1}
\]

#### Proof

Choose \(c\in S\) so that, if a two-list type occurs, it is type \(c\).
If no type occurs, choose \(c\) arbitrarily.

Every outside vertex not in \(W_c\) has \(c\in L(x)\).  Under the
no-full hypothesis, any such vertex either has singleton list \(\{c\}\)
or has a two-list containing \(c\).  The latter would be a two-list type
different from type \(c\), contrary to the choice of \(c\).  Hence

\[
V(H)=
\bigl((S-\{c\})\cup W_c\bigr)
\ \dot\cup\
\bigl(\{c\}\cup\{x:L(x)=\{c\}\}\bigr).
\tag{2.2}
\]

The first induced part is bipartite by the frozen-projection theorem.
The second part is independent in \(H\): response membership makes
\(cx\in E(G)\), and singleton safety makes every two outside vertices
with list \(\{c\}\) adjacent in \(G\).  Color the first part with two
colors and the second part with a third color.  This is an ordinary
proper coloring of \(H\).

Crucially, this proof does **not** try to respect the singleton response
colors inside the bipartite part.  Conflicting 2-SAT units therefore do
not affect the argument. \(\square\)

### Corollary 2.2

If \(\theta(G)>3\), equivalently \(\chi(H)>3\), then

\[
t\geq2.
\tag{2.3}
\]

## 3. Two pure vertices per type

### Theorem 3.1 (pure-signature doubling) — PROVED

For every \(i\in T\), there are distinct vertices \(z_i,w_i\in A\) such
that

\[
\sigma(z_i)=\sigma(w_i)=\{i\},
\qquad
z_iw_i\in E(H),
\qquad
L(z_i)=S-\{i\}.
\tag{3.1}
\]

Consequently,

\[
|A|\geq2t.
\tag{3.2}
\]

#### Proof

Take the physical representative \(z_i\) from (1.6).  Since
\(\gamma(G)\geq3\), the pair \(\{i,z_i\}\) does not dominate.  Choose

\[
w_i\in N_H(i)\cap N_H(z_i).
\tag{3.3}
\]

The vertex \(w_i\) is not in \(S\).  Indeed, it is neither \(i\) nor
\(z_i\), and every other anchor \(r\in S-\{i\}\) is adjacent to \(z_i\)
in \(G\) because \(r\in L(z_i)\).

Thus \(w_i\notin S\) and \(i\in\sigma(w_i)\).  Suppose another anchor
\(r\ne i\) also belongs to \(\sigma(w_i)\), and let \(h\) be the third
anchor.  Since \(h\in L(z_i)\), the state

\[
S-h+z_i=\{i,r,z_i\}
\tag{3.4}
\]

belongs to \(\mathcal F\) and must dominate.  But (3.3) and
\(r\in\sigma(w_i)\) say that all three members of (3.4) miss \(w_i\) in
\(G\), a contradiction.  Therefore

\[
\sigma(w_i)=\{i\}.
\]

The vertices are distinct and (3.3) gives their \(H\)-edge.  Pure
signature classes belonging to distinct anchors are disjoint, proving
(3.2). \(\square\)

### Remark 3.2

The new vertex \(w_i\) need not itself have the two-list
\(S-\{i\}\).  Its list is merely a nonempty subset of \(S-\{i\}\).
Thus Theorem 3.1 does not automatically iterate to force a third pure
vertex.

## 4. Neutral coverage and the order-13 count

### Lemma 4.1 (every neutral vertex sees all signature colors) — PROVED

For every \(q\in Q\) and every \(i\in S\), there is a vertex
\(x_{q,i}\in A\) such that

\[
i\in\sigma(x_{q,i}),
\qquad
qx_{q,i}\in E(H).
\tag{4.1}
\]

In particular, if \(Q\ne\varnothing\), then

\[
\bigcup_{x\in A}\sigma(x)=S.
\tag{4.2}
\]

#### Proof

The pair \(\{q,i\}\) does not dominate, so take

\[
x_{q,i}\in N_H(q)\cap N_H(i).
\]

It is not in \(S\), since \(q\) is \(G\)-complete to \(S\).  It is not
in \(Q\), since every member of \(Q\) is \(G\)-adjacent to \(i\).
Therefore it lies in \(A\), and the two required incidences are exactly
the definition of the common complement neighborhood. \(\square\)

### Theorem 4.2 (sound order-13 count) — PROVED

Assume \(|V(G)|=13\) and \(\theta(G)>3\).  In the no-full branch,

\[
\boxed{|A|\geq5,\qquad |Q|\leq5.}
\tag{4.3}
\]

If \(t=3\), then

\[
\boxed{|A|\geq6,\qquad |Q|\leq4.}
\tag{4.4}
\]

#### Proof

There are ten vertices outside \(S\), so \(|A|+|Q|=10\).
Corollary 2.2 gives \(t\geq2\), and Theorem 3.1 gives
\(|A|\geq2t\).

If \(t=3\), this immediately gives \(|A|\geq6\).

Suppose \(t=2\), with omitted colors \(i,j\), and let \(h\) be the third
anchor.  Theorem 3.1 supplies four vertices: two have pure signature
\(\{i\}\) and two have pure signature \(\{j\}\).  If \(|A|=4\), then
\(|Q|=6>0\), but the union of the four signatures is only
\(\{i,j\}\), contradicting Lemma 4.1 for color \(h\).  Hence
\(|A|\geq5\).  Subtracting from ten gives the stated bounds on \(Q\).
\(\square\)

### Corollary 4.3 (tight five-nonneutral normal form) — PROVED

If equality holds in (4.3), then \(t=2\).  Write the two omitted colors
as \(i,j\), and the remaining anchor as \(h\).  The set \(A\) consists
of:

- two vertices of pure signature \(\{i\}\);
- two vertices of pure signature \(\{j\}\); and
- one vertex \(r\) whose signature is, after possibly interchanging
  \(i,j\),
  \[
  \sigma(r)=\{h,i\}.
  \tag{4.5}
  \]

Moreover,

\[
qr\in E(H)\quad(q\in Q),
\qquad
L(r)=\{j\}.
\tag{4.6}
\]

#### Proof

The first four vertices are forced by Theorem 3.1.  Lemma 4.1 says that
the unique fifth vertex \(r\) must have \(h\in\sigma(r)\), and, because
it is the unique such vertex, every \(q\in Q\) must use \(r\) in (4.1)
for color \(h\).  This proves the first part of (4.6).

If \(\sigma(r)=\{h\}\), then the pair \(\{h,r\}\) has no common neighbor
in \(H\): no anchor works, no member of \(Q\) is adjacent in \(H\) to
\(h\), and none of the four pure \(i/j\)-vertices has \(h\) in its
signature.  This would make \(\{h,r\}\) a dominating pair in \(G\),
contrary to \(\gamma(G)=3\).  Since \(S\) dominates, the only remaining
possibilities are \(\{h,i\}\) and \(\{h,j\}\).  Interchange \(i,j\) if
needed to obtain (4.5).

Finally, (1.3) and nonemptiness of \(L(r)\) give
\[
\varnothing\ne L(r)\subseteq S-\{h,i\}=\{j\},
\]
which proves the second part of (4.6). \(\square\)

## 5. Audit of the existing no-full SAT wrapper

The wrapper

`math/working/order13_no_full_probe/search.py`

was audited before the structural work.

- Edge variables encode \(H\), not \(G\).
- The fixed \(H\)-triangle \(S=\{0,1,2\}\), no \(H\)-\(K_4\), and
  common-\(H\)-neighbor clauses give \(\alpha(G)=\gamma(G)=3\).
- A nonempty family of dominating triples with literal one-guard closure
  gives \(\gamma^\infty(G)=3\).
- Closure at \(S\) makes every response list nonempty.  The ten added
  ternary clauses forbid all three direct successors at one target, so
  they express exactly the no-full condition.  A retained direct
  successor already forces its move edge because it must dominate the
  omitted anchor.
- Connectedness and the redundant requirement that every independent
  triple be retained are omitted.  This is a relaxation and is safe for
  an eventual UNSAT exclusion.
- The pivoted \(S_9\) signature sort is sound: after choosing any outside
  vertex as label 3, the remaining nine vertices are interchangeable and
  can be sorted by their four-bit signatures to
  \(\{0,1,2,3\}\).

The exact formula census is:

\[
\begin{array}{c|r}
\text{variables}&9802\\
\text{clauses}&85413\\
\text{no-full clauses}&10\\
\text{pivoted signature clauses}&960\\
\text{anchored non-3-colorability clauses}&3^{10}=59049.
\end{array}
\]

The retained DIMACS has SHA-256

```text
5d6d9bccb80c3ccab222a095819d50b58bb9f1fc22652b2d0bad8013681fd007
```

and exactly matches a fresh rebuild from the wrapper.  It contains no
duplicate clauses, no tautological clauses, and no unused variables.
CaDiCaL's 120-second timeout remains a **NONCLAIM**.

The auxiliary splitter `decompose.py` replaces the pivoted sorter by a
sound full \(S_{10}\) sort of the three-bit anchor signatures.  Two
order-13 \(|A|=4\) discovery formulas were independently accepted by
`drat-trim`, but Theorem 4.2 already excludes that census by a human
argument.  These runs are therefore only redundant **OBSERVED** controls,
not promoted finite results.

Two earlier overconstrained formulas named `tight-*` and `six-*` used the
retracted, false assumption that three outside double-signature vertices
were mandatory.  Their UNSAT outputs have no coverage meaning and must
not be cited.

## 6. Remaining branch

The complementary order-13 no-full search is now soundly reduced to:

1. the tight normal form of Corollary 4.3, with
   \((|A|,|Q|)=(5,5)\);
2. \(|A|\geq6,\ |Q|\leq4\).

The universal conjecture and the complete order-13 no-full branch remain
open.  A high-value next step is to combine the \(H\)-complete neutral
hub \(r\) in (4.6) with the exact minimal 2-SAT terminal trichotomy, or to
partition the residual branch by \(t=2\) versus \(t=3\).
