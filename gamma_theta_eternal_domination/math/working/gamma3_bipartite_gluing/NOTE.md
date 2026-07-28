# The exact \(\gamma=3\) target condition and a sharp static boundary

## Status and scope

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** eternal-domination model.
It proves the exact complement translation of the missing
\(\gamma(G)\geq3\) condition at a deletion target and gives an explicit
countermodel to the resulting **static** coloring shortcut.

It does **not** refute a theorem using full multi-step eternal closure.  In
fact, the target extension in the countermodel has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4),
\]

so it is not a counterexample to the \(\gamma\)--\(\theta\) conjecture.

The main conclusions are:

1. if \(H'=\overline{G-x}\) already has a common neighbor for every pair
   and \(B=N_{\overline G}(x)\), then
   \[
   \gamma(G)\geq3
   \quad\Longleftrightarrow\quad
   B\text{ totally dominates }H';
   \]
2. for the C-108 family-relative marking, \(B\subseteq R\), so every
   deletion vertex—not only every active vertex—has an \(H'\)-neighbor in
   \(B\subseteq R\);
3. even the stronger special case \(B=R\), together with nonvacuous ridge
   covariance, a full active root, bipartite \(H'[R]\), pure triangle
   geometry, and every marked one-step successor dominating, does not force
   a three-coloring using at most two colors on \(R\).

No literature-priority claim is made.

## 1. Exact common-neighbor translation

Let \(G\) be a finite graph of order at least three, fix \(x\in V(G)\), and
put

\[
 H=\overline G,\qquad H'=H-x,\qquad B=N_H(x).
\tag{1.1}
\]

Recall that a pair \(\{u,v\}\) fails to dominate \(G\) exactly when it has a
common neighbor in \(H\): a vertex \(w\) is missed by the pair in \(G\) if
and only if

\[
 w\in N_H(u)\cap N_H(v).
\tag{1.2}
\]

### Theorem 1.1 (exact target translation) — PROVED

Assume every pair of vertices of \(H'\) has a common neighbor in \(H'\).
Equivalently, \(\gamma(G-x)\geq3\).  Then

\[
 \boxed{
 \gamma(G)\geq3
 \quad\Longleftrightarrow\quad
 N_{H'}(v)\cap B\ne\varnothing
 \text{ for every }v\in V(H').
 }
\tag{1.3}
\]

Thus \(\gamma(G)\geq3\) is equivalent to saying that \(B\) is a **total
dominating set** of \(H'\).

#### Proof

Pairs wholly contained in \(V(H')\) already have common \(H'\)-neighbors
by hypothesis.  The only new pairs to check are therefore
\(\{x,v\}\), with \(v\in V(H')\).  By (1.2), such a pair fails to dominate
\(G\) exactly when

\[
 N_H(x)\cap N_H(v)
 =
 B\cap N_{H'}(v)
\ne\varnothing.
\]

This condition for every \(v\) is precisely total domination of \(H'\) by
\(B\).  The absence of a dominating pair also excludes a dominating
singleton, completing the equivalence. \(\square\)

The distinction between ordinary and total domination matters here:
vertices of \(B\) themselves must have a neighbor in \(B\).

### Corollary 1.2 (C-108 active/inactive form) — PROVED

Suppose

\[
 \alpha(G)=\gamma^\infty(G)=3
\]

and \(A=A_x\), \(R=V(G-x)-A\) are the family-relative active and inactive
sets of C-108 for a fixed eternal triple-family.  Then

\[
 B=N_H(x)\subseteq R.
\tag{1.4}
\]

If the deletion graph satisfies \(\gamma(G-x)\geq3\), then
\(\gamma(G)\geq3\) implies

\[
 \boxed{
 N_{H'}(v)\cap B\ne\varnothing
 \quad\text{for every }v\in V(H').
 }
\tag{1.5}
\]

In particular, every active \(a\in A\) has an \(H'\)-neighbor in
\(B\subseteq R\), and \(R\) itself totally dominates \(H'\).

#### Proof

An active vertex must move along a \(G\)-edge to \(x\), so it cannot lie in
\(N_H(x)\).  Conversely, a vertex of \(B=N_H(x)\) has no \(G\)-edge to
\(x\) and cannot answer the attack at \(x\).  Since \(R\) is the complement
of the active set \(A\) in \(V(G-x)\), this directly gives \(B\subseteq R\).
Theorem 1.1 gives (1.5), and \(B\subseteq R\) gives the final assertion.
\(\square\)

Notice that \(B=R\) is not automatic.  A vertex may be adjacent to \(x\)
in \(G\) but still be inactive because its proposed successor is absent
from the chosen eternal family.

## 2. Stronger consequences at a full root

Let

\[
 S=\{s_0,s_1,s_2\}
\tag{2.1}
\]

be an independent triple of \(G\) avoiding \(x\), equivalently a triangle
of \(H'\).  Suppose all three swaps

\[
 S-s_i+x\qquad(i=0,1,2)
\tag{2.2}
\]

dominate \(G\).  A full family response implies these static hypotheses.

### Proposition 2.1 (three anchor-pure target witnesses) — PROVED

Under Theorem 1.1 and (2.2), every \(b\in B\) has at most one
\(H'\)-neighbor in \(S\).  Moreover, for each \(s_i\) the spoke

\[
 B_i=B\cap N_{H'}(s_i)
\tag{2.3}
\]

is nonempty, and the three spokes are pairwise disjoint.

#### Proof

If \(b\in B\) were adjacent in \(H'\) to two anchors, say
\(s_j,s_k\), then it would be a common \(H\)-neighbor of the three guards
in

\[
 \{x,s_j,s_k\}=S-s_i+x.
\]

That successor would fail to dominate \(b\) in \(G\), contrary to (2.2).
Thus \(b\) sees at most one anchor.

Theorem 1.1 applied to the pair \(\{x,s_i\}\) gives a vertex
\(b_i\in B\cap N_{H'}(s_i)\), so every spoke is nonempty.  The at-most-one
property makes the spokes disjoint. \(\square\)

There are two further immediate consequences.

- Total domination makes \(H'[B]\) isolate-free.
- If \(H'[R]\) is bipartite, then its induced subgraph \(H'[B]\) is
  bipartite and isolate-free.

If, more generally, every active vertex in every deletion triangle has a
dominating swap to \(x\), then for every triangle
\(\{a,p,q\}\) with \(a\in A\),

\[
 B\cap N_{H'}(p)\cap N_{H'}(q)=\varnothing.
\tag{2.4}
\]

Indeed, a vertex in the displayed intersection would be a common
\(H\)-neighbor of the successor \(\{x,p,q\}\).  Equation (2.4) is the
exact static “opposite-ridge” consequence of the marked response.

These conclusions strengthen the missing condition in C-123, but they
still do not solve the global coloring problem.

## 3. An exact static countermodel with \(\gamma=3\)

### Theorem 3.1 (static \(\gamma=3\) gluing shortcut is false) — PROVED

There is an 11-vertex three-colorable graph \(H'\), a partition

\[
 V(H')=A\mathbin{\dot\cup}R,
\tag{3.1}
\]

and a target extension \(H\) obtained by adjoining \(x\) with
\(N_H(x)=R\), such that:

1. every pair of vertices of both \(H'\) and \(H\) has a common neighbor;
2. every maximal clique of \(H'\) is a triangle;
3. the marking satisfies the C-108 ridge-covariance rule nonvacuously;
4. \(A\) contains a full active triangle;
5. \(H'[R]\) is bipartite and \(R\) totally dominates \(H'\);
6. every active marked response from every deletion triangle to \(x\)
   produces a dominating triple of \(G=\overline H\); but
7. every proper three-coloring of \(H'\) uses all three colors on \(R\).

Hence adding the exact \(\gamma(G)=3\) target condition—even in the strong
form \(R=N_H(x)\)—does not make the accepted static hypotheses imply the
desired deletion coloring.

### 3.1 Graph and marking

Let \(V(H')=\{0,\ldots,10\}\), with edge set

```text
03 04 07 08 09
13 15 16 18
24 25 26 27 29 (2,10)
36 37 39 (3,10)
46 48 (4,10)
57 58
(9,10)
```

The labeled graph6 string is

```text
JEhbtjKk@o_
```

and a canonical graph6 string is

```text
J``E@SV^Tx?
```

Put

\[
 A=\{0,4,6,7,8,9,10\},
 \qquad
 R=\{1,2,3,5\}.
\tag{3.2}
\]

Adjoin \(x=11\) with

\[
 N_H(x)=R.
\tag{3.3}
\]

The labeled strings of \(H\) and \(G=\overline H\) are

```text
H = KEhbtjKk@om_
G = KxU[ISrR}NP^
```

and their canonical strings are respectively

```text
H = K_?@h]SRNr^Q
G = Kq]p`SVJw~W^
```

### 3.2 Pure triangles, covariance, and the full root

The maximal cliques of \(H'\) are exactly

\[
\begin{array}{lllll}
037,&048,&039,&136,&246,\\
257,&\{2,4,10\},&158,&\{2,9,10\},&\{3,9,10\}.
\end{array}
\tag{3.4}
\]

Thus every maximal clique is a triangle.  The exact equivalence classes
generated by exchanging opposite vertices across shared triangle ridges
are

\[
\{0,6,10\},\quad
\{1\},\quad
\{2,3\},\quad
\{4,7,9\},\quad
\{5\},\quad
\{8\}.
\tag{3.5}
\]

Every class is wholly active or wholly inactive under (3.2), proving
ridge covariance.  The classes of sizes three and two show that the
condition is genuinely nonvacuous here.  The triangle

\[
 S=\{0,4,8\}\subseteq A
\tag{3.6}
\]

is a full active root.

### 3.3 The exact \(\gamma=3\) condition

The inactive graph is the path

\[
 H'[R]=3-1-5-2,
\tag{3.7}
\]

so it is bipartite.  The following table gives an \(R\)-neighbor for every
deletion vertex:

\[
\begin{array}{c|ccccccccccc}
v&0&1&2&3&4&5&6&7&8&9&10\\ \hline
R\text{-neighbor}&3&3&5&1&2&1&1&2&1&2&2.
\end{array}
\tag{3.8}
\]

Thus \(R=N_H(x)\) totally dominates \(H'\).  By Theorem 1.1,
\(\gamma(G)\geq3\).  The triangle (3.6) is independent and dominating in
\(G\), so \(\gamma(G)=3\).

The standalone verifier supplies an explicit common-neighbor witness for
each of the 55 pairs of \(H'\) and all 66 pairs of \(H\).  It also checks
directly all 18 marked active-response obligations from (3.4); every move
uses one \(G\)-edge to \(x\), and every resulting triple dominates \(G\).

### 3.4 Unique coloring and failure of gluing

Up to permuting color names, \(H'\) has the unique proper
three-coloring

\[
 \{0,5,6,10\}
 \mid
 \{1,4,7,9\}
 \mid
 \{2,3,8\}.
\tag{3.9}
\]

There is also a short forcing proof.  The pairs of triangles sharing
ridges in (3.4) force

\[
 7\sim_{\rm color}9,\qquad
 0\sim_{\rm color}10,\qquad
 2\sim_{\rm color}3,\qquad
 6\sim_{\rm color}10.
\]

Triangles \(246\) and \(037\) then force \(4,7,9\) to share the third
color.  Triangle \(048\) forces \(8\) to share the color of \(2,3\).
Finally, \(136\) and \(158\) force \(1\) into the \(4,7,9\) class and
\(5\) into the \(0,6,10\) class.  This yields exactly (3.9).

The inactive vertices meet its three parts as

\[
 R\cap\{0,5,6,10\}=\{5\},\qquad
 R\cap\{1,4,7,9\}=\{1\},\qquad
 R\cap\{2,3,8\}=\{2,3\}.
\tag{3.10}
\]

Therefore every deletion three-coloring uses all three colors on \(R\).
Since \(x\) is adjacent in \(H\) precisely to \(R\), no color extends
over \(x\), and \(\chi(H)=4\).

This proves Theorem 3.1.

## 4. Exact dynamic boundary

Direct evaluation from the definitions gives

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G-x)
 =(3,3,3,3,3),
\tag{4.1}
\]

with 48 states in the greatest eternal triple-family of \(G-x\), but

\[
 \boxed{
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G)
 =(3,3,3,4,4).
 }
\tag{4.2}
\]

The greatest three-guard deletion process for \(G\) removes

\[
 47,\ 56,\ 3
\tag{4.3}
\]

states in its three rounds and leaves no state.  The full root \(048\)
has deletion rank three.  An explicit adaptive attack tree, including
every legal dominating successor at each branch, is recorded in
`countermodel_verification.json`.

Thus the countermodel sharply separates the remaining mechanisms:

- \(\gamma=3\) and all static one-step response tests are insufficient;
- nonvacuous ridge transport is insufficient;
- exact multi-step one-guard closure is still missing and kills this
  control.

The surviving theorem target must genuinely use the assumption
\(\gamma^\infty(G)=3\), not merely its static consequences presently
encoded in the deletion geometry.

## 5. Bounded discovery observations

All search statements in this section are **OBSERVED**, not certified
finite theorems.

1. A targeted scan of all 8,587 existing edge-toggle database graphs with
   \((\gamma,\alpha,\theta)=(3,3,4)\), and a second scan of 391 existing
   one-vertex-extension candidates with \(\gamma=\alpha=3\), found no
   earlier instance satisfying the full marked target conditions.
2. The accepted C-123 search already observed no static \(\gamma=3\)
   gluing obstruction through deletion order ten.
3. The present graph was found among two-vertex extensions of the
   C-123 graph \(L(K_{3,3})\), after 13,370 labeled extension rows.  This
   early-stop discovery count has no coverage significance.

These observations suggest, but do not certify, that target order 12 may
be the first order of the strengthened static phenomenon.

## 6. Reproduction

From the campaign root:

```text
python3 -I -B -W error \
  math/working/gamma3_bipartite_gluing/verify_countermodel.py
```

The deterministic output is
`math/working/gamma3_bipartite_gluing/countermodel_verification.json`.

The discovery probes are retained separately:

```text
python3 -I -B \
  math/working/gamma3_bipartite_gluing/scan_existing_candidates.py \
  --allow-dynamically-inactive-neighbors \
  --seconds 600

python3 -I -B \
  math/working/gamma3_bipartite_gluing/extend_lk33_all_markings.py \
  --seconds 600
```

Only Theorems 1.1 and 3.1, Proposition 2.1, the explicit graph checks, and
the exact parameter/game evaluations are claimed as proved.  Negative
search outcomes and minimality impressions remain observations.
