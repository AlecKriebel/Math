# Global reverse colors at a full target

## Status and exact scope

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** eternal-domination model:
attacks are made only at unoccupied vertices, exactly one guard moves along
one graph edge, and every retained successor dominates.

The main positive result is that the reverse role of the guard at a full
target is global over the entire physical complement link, not merely over
one link component, and that at least one such global reverse color always
exists.  The proof combines C-108 with the accepted family-response Hall
condition.

The hoped-for coloring conclusion is false in its color-by-color form.
Even with

\[
 \gamma=i=\alpha=\gamma^\infty=\theta=3
\]

and the literal greatest eternal family, a reverse color need not be a
feasible color for the target.  An exact order-12 equality control has all
three reverse colors but only one feasible target color.  The same control
shows that a reverse color need not survive the natural color-restricted
coinductive kernel.

This note does **not** close the full-list branch, prove the complete
parameter-three case, or resolve the universal gamma--theta conjecture.  No
literature-priority claim is made.

## 1. Setup

Let

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
 \qquad H=\overline G,
\tag{1.1}
\]

and let \(\mathcal F\) be an optimal eternal family of dominating triples.
Fix an independent state

\[
 S=\{s_0,s_1,s_2\}\in\mathcal F
\tag{1.2}
\]

and a target \(x\notin S\) having a full family response:

\[
 D_i=S-\{s_i\}+\{x\}\in\mathcal F
 \qquad(0\le i\le2).
\tag{1.3}
\]

Membership in (1.3) includes the move edge

\[
 xs_i\in E(G)
 \qquad(0\le i\le2).
\tag{1.4}
\]

Put

\[
 B=N_H(x).
\tag{1.5}
\]

Equation (1.4) gives \(S\cap B=\varnothing\).
The set \(B\) is nonempty, since otherwise \(x\) would dominate \(G\).
Moreover \(H[B]\) has no isolated vertex.  Indeed, for \(b\in B\), the
pair \(\{x,b\}\) cannot dominate \(G\), so some vertex \(c\) is adjacent
in \(H\) to both \(x\) and \(b\).  Thus \(c\in B\) and \(bc\in E(H)\).

Every edge \(bc\in E(H[B])\) gives an independent triple

\[
 T_{bc}=\{x,b,c\}.
\tag{1.6}
\]

Equality \(\alpha=\gamma^\infty=3\) puts every maximum independent triple
in every optimal eternal family, hence

\[
 T_{bc}\in\mathcal F.
\tag{1.7}
\]

For \(b\in B\), retain the C-132 palette notation

\[
 P(b)=\{i:\{x,s_i,b\}\in\mathcal F\}.
\tag{1.8}
\]

## 2. The global reverse-color theorem

For an edge \(bc\in E(H[B])\), define

\[
 R_{bc}=
 \{i:\{s_i,b,c\}\in\mathcal F\}.
\tag{2.1}
\]

Equivalently, \(i\in R_{bc}\) when the guard at \(x\) can answer the
attack at \(s_i\) from \(T_{bc}\).

### Theorem 2.1 (globality and nonemptiness) — PROVED

There is one nonempty set

\[
 \varnothing\ne R\subseteq\{0,1,2\}
\tag{2.2}
\]

such that

\[
 R_{bc}=R
 \qquad\text{for every }bc\in E(H[B]).
\tag{2.3}
\]

Thus

\[
 \boxed{
 i\in R
 \quad\Longleftrightarrow\quad
 \{s_i,b,c\}\in\mathcal F
 \text{ for one, equivalently every, link edge }bc.
 }
\tag{2.4}
\]

#### Proof

Fix \(i\).  Any two states \(T_{bc}\) and \(T_{de}\) are retained
independent triples avoiding \(s_i\), and they share the vertex \(x\).
C-108, applied with target \(s_i\) and shared responder \(x\), gives

\[
 x\text{ answers at }s_i\text{ from }T_{bc}
 \quad\Longleftrightarrow\quad
 x\text{ answers at }s_i\text{ from }T_{de}.
\tag{2.5}
\]

Equation (1.4) supplies the move edge, so (2.5) is exactly

\[
 \{s_i,b,c\}\in\mathcal F
 \quad\Longleftrightarrow\quad
 \{s_i,d,e\}\in\mathcal F.
\]

This proves globality across all link components, not just within one
component.

It remains to prove nonemptiness.  Fix one link edge \(bc\) and use
\(T=T_{bc}\) as the independent reference state.  The root \(S\) is an
independent three-set outside \(T\).  The family-response Hall theorem
applied to this outside independent set gives

\[
 \left|
 \bigcup_{i=0}^2 L_T^{\mathcal F}(s_i)
 \right|\ge3.
\tag{2.6}
\]

Every list in (2.6) is a subset of the three guard positions
\(\{x,b,c\}\).  Consequently their union is all of \(T\), and in
particular the guard position \(x\) occurs in at least one list.  For that
index \(i\), the state \(T-x+s_i=\{s_i,b,c\}\) belongs to
\(\mathcal F\).  Hence \(i\in R\). \(\square\)

### Proposition 2.2 (exact response rows) — PROVED

For every edge \(bc\in E(H[B])\) and every \(i\in\{0,1,2\}\),

\[
 L_{T_{bc}}^{\mathcal F}(s_i)
 =
 \bigl(\{x\}:i\in R\bigr)
 \ \cup\
 \bigl(\{b\}:i\in P(c)\bigr)
 \ \cup\
 \bigl(\{c\}:i\in P(b)\bigr).
\tag{2.7}
\]

Here \((X:\mathcal P)\) means \(X\) if \(\mathcal P\) holds and the empty
set otherwise.

#### Proof

The \(x\)-role is the definition of \(R\).  A move \(b\to s_i\) has
successor

\[
 T_{bc}-b+s_i=\{x,s_i,c\},
\]

so a legal retained \(b\)-response implies \(i\in P(c)\).  Conversely,
if \(i\in P(c)\), the retained state \(\{x,s_i,c\}\) must dominate \(b\).
The vertices \(x\) and \(c\) both miss \(b\) in \(G\), because
\(b\in B\) and \(bc\in E(H)\).  Therefore \(s_i b\in E(G)\), and
\(b\to s_i\) is a legal retained response.  This proves the \(b\)-role.
Interchanging \(b,c\) proves the \(c\)-role. \(\square\)

Equation (2.7) packages the C-139 component palettes and the new global
reverse set into one exact three-by-three response table.  Hall forces
\(R\ne\varnothing\), but it does not select a color inside \(R\).

## 3. What a reverse color would have to prove

For a proper three-coloring of \(H-x\), fix the root colors by

\[
 \kappa(s_i)=i.
\tag{3.1}
\]

Call \(r\in\{0,1,2\}\) **feasible at \(x\)** if there is a proper
three-coloring \(\kappa\) of \(H-x\) satisfying (3.1) and

\[
 r\notin\kappa(B).
\tag{3.2}
\]

Since \(B=N_H(x)\), condition (3.2) is exactly what permits extending the
coloring by

\[
 \kappa(x)=r.
\tag{3.3}
\]

Let \(C_x\) denote the set of feasible target colors.  Then

\[
 C_x\ne\varnothing
 \quad\Longleftrightarrow\quad
 \chi(H)=3
 \quad\Longleftrightarrow\quad
 \theta(G)=3.
\tag{3.4}
\]

Indeed, one direction is extension by (3.3).  In the other direction,
every proper three-coloring of \(H\) gives all three colors to the triangle
\(S\); after renaming them to satisfy (3.1), the color of \(x\) is absent
from \(B\).

### Proposition 3.1 (feasible colors are reverse colors) — PROVED

Let \(\mathcal F^\star\) be the literal greatest eternal triple-family.
Then

\[
 \boxed{C_x\subseteq R.}
\tag{3.5}
\]

#### Proof

Take \(r\in C_x\) and extend the deletion coloring by (3.3).  Its three
color classes are cliques of \(G\).  The family of all triples containing
one vertex from each color class is an eternal triple-family: every such
triple dominates, and an attack is answered by the guard in the attacked
vertex's clique.  Hence this clique-fiber family lies in
\(\mathcal F^\star\).

For a link edge \(bc\), condition (3.2) makes both endpoint colors
different from \(r\), and properness makes the two endpoint colors
different from one another.  Thus \(b,c\) use the other two colors, while
\(s_r\) uses color \(r\).  The transversal

\[
 \{s_r,b,c\}
\]

belongs to the clique-fiber family and therefore to
\(\mathcal F^\star\).  Hence \(r\in R\). \(\square\)

The greatest-family qualification is essential to this short proof.  An
arbitrary optimal eternal subfamily need not contain the clique-fiber
family.

## 4. The coinductive color gate

For \(r\in\{0,1,2\}\), ban the states

\[
 \mathcal B_r=
 \{S-\{s_r\}+\{y\}:y\in B\},
\tag{4.1}
\]

and let \(\mathcal K_r\) be the greatest eternal family among the
dominating triples outside \(\mathcal B_r\).  Call \(r\) **safe** when

\[
 S\in\mathcal K_r
 \quad\text{and}\quad
 S-\{s_r\}+\{x\}\in\mathcal K_r.
\tag{4.2}
\]

This is the color-restricted greatest-kernel construction already tested
in the full-list safe-kernel lane.

### Proposition 4.1 (feasibility passes the coinductive gate) — PROVED

Every feasible color is safe.  Consequently, for the greatest family,

\[
 C_x\subseteq R\cap K_x,
\tag{4.3}
\]

where \(K_x\) is the set of safe colors.

#### Proof

Use the clique-fiber eternal family from Proposition 3.1.  It contains
\(S\) and \(S-s_r+x\).  If \(y\in B\), then \(y\) cannot have color
\(r\), because \(xy\in E(H)\) and \(x\) has color \(r\).  Therefore
\(S-s_r+y\) is not a transversal of the three color classes.  The
clique-fiber family avoids every state in \(\mathcal B_r\), so it is
contained in \(\mathcal K_r\).  This proves (4.2).  Combine with (3.5).
\(\square\)

The containment direction in (4.3) is deliberately one-way.  Neither
reverse membership nor safe-kernel survival has been proved sufficient
for a coloring under equality.

## 5. Exact equality refutation of reverse-color sufficiency

Consider the labeled graph

```text
Ksv`f\knJVis
```

with

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{5.1}
\]

Its greatest eternal triple-family has 127 states.  Take

\[
 S=\{1,2,3\},\qquad x=0,
\tag{5.2}
\]

with anchor colors \(0,1,2\) assigned respectively to vertices \(1,2,3\).
The target is full, and

\[
 B=\{6,8,10,11\},\qquad
 E(H[B])=\{68,10\,11\}.
\tag{5.3}
\]

For both link edges, all three reverse states survive:

\[
\begin{array}{c|cc}
r&68&10\,11\\ \hline
0&\{1,6,8\}&\{1,10,11\}\\
1&\{2,6,8\}&\{2,10,11\}\\
2&\{3,6,8\}&\{3,10,11\}.
\end{array}
\tag{5.4}
\]

Thus

\[
 R=\{0,1,2\}.
\tag{5.5}
\]

There are exactly two proper colorings of \(H-x\) with \(S\) fixed,
written as color vectors on vertices \(0,\ldots,11\), with `-` at \(x\):

```text
(-,0,1,2,2,0,1,1,0,2,1,0)
(-,0,1,2,0,1,2,0,1,1,0,2)
```

The first uses colors \(1,0,1,0\) on \(B=(6,8,10,11)\), so it avoids
color 2.  The second uses colors \(2,1,0,2\) on \(B\), so it avoids no
color.  Therefore

\[
 C_x=\{2\}\subsetneq R.
\tag{5.6}
\]

This is an equality graph, not a gamma-two boundary example.  Equations
(5.5)--(5.6) refute both of the proposed implications

\[
 r\in R\Longrightarrow r\in C_x,
\qquad
 R\ne\varnothing\Longrightarrow
 \text{an arbitrary chosen reverse color extends}.
\tag{5.7}
\]

The coinductive replay identifies the missing information exactly.  For
colors 0 and 1, the restricted kernel is empty, with deletion-round sizes

\[
 16,40,56,12.
\tag{5.8}
\]

For color 2, the restricted kernel has 64 states after deletion rounds

\[
 16,32,13,
\tag{5.9}
\]

and contains both states required by (4.2).  Hence

\[
 K_x=C_x=\{2\},
\qquad R=\{0,1,2\}.
\tag{5.10}
\]

In particular, reverse survival is only a first-response fact.  It does not
guarantee a strategy that preserves the global color prohibition through
all future attacks.

## 6. Bounded probes

The deterministic candidate replay scanned the complete `geng -cq`
streams of connected unlabeled graphs through order nine.  It found

\[
\begin{array}{c|r|r|r}
n&\text{connected graphs}&
\gamma=\alpha=\gamma^\infty=3&
\text{full incidences}\\ \hline
1&1&0&0\\
2&1&0&0\\
3&2&0&0\\
4&6&0&0\\
5&21&0&0\\
6&112&2&0\\
7&853&16&0\\
8&11{,}117&140&0\\
9&261{,}080&1{,}380&0.
\end{array}
\tag{6.1}
\]

Thus the reverse-color test is vacuous through order nine.  This census is
labelled **OBSERVED**: it shares verifier A, has no independent coverage
audit in this package, and is not a new finite-exclusion certificate.

A separate radius-two labeled edge-toggle probe around the order-12
control tested 2,212 graphs.  Of 232 equality graphs, only the unmodified
control retained the specified full incidence.  This is exploratory
evidence only and has no universal implication.

## 7. Corrected proof frontier

The full-response branch now has a clean hierarchy:

\[
\boxed{
\begin{array}{c}
\text{C-132/C-139: componentwise physical-link palettes;}\\
\text{Theorem 2.1: a nonempty global reverse-color set }R;\\
\text{Proposition 4.1: every actually feasible color lies in }
R\cap K_x;\\
\text{the equality control: }R\text{ alone has strict false positives.}
\end{array}}
\tag{7.1}
\]

The next noncircular coinductive target is therefore not
“prove \(R\ne\varnothing\),” which is now done.  It is:

> In the equality-critical full-target branch, prove that at least one
> color in \(R\) survives its color-restricted kernel, and then prove that
> one such surviving color yields a compatible anchored coloring.

The first clause asks for genuinely future-stable selection; the second is
the remaining global gluing step.  The order-12 control shows why the
selection cannot be made from one-step reverse incidence alone.
