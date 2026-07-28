# Bipartite inactivity does not solve the deletion-coloring gluing problem

## Status and scope

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** eternal-domination model.
It is a theorem-boundary result, not a counterexample to the
\(\gamma\)--\(\theta\) conjecture and not a proof of the \(k=3\) case.

The result is:

> **Theorem 1 (PROVED — sharp static boundary).** There is a
> three-colorable graph \(H'\), together with a partition
> \(V(H')=A\mathbin{\dot\cup}R\), such that:
>
> 1. every pair of vertices of \(H'\) has a common neighbor;
> 2. every maximal clique of \(H'\) is a triangle;
> 3. the marking \(A/R\) satisfies the C-108 ridge-covariance rule;
> 4. \(A\) contains a full active triangle;
> 5. \(H'[R]\) is bipartite; but
> 6. every proper three-coloring of \(H'\) uses all three colors on \(R\).
>
> Consequently, static equality of the deletion graph, pure triangle
> geometry, ridge covariance, a full active root, and bipartiteness of the
> inactive graph do **not** force a deletion coloring that omits one color
> on \(R\).

The explicit target extension has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,4,4).
\]

It is therefore a low-domination control only.  The condition
\(\gamma=3\) already excludes this particular extension.  Moreover, its
full active root survives every one-step domination test but is defeated
by a literal adaptive two-attack sequence.  Thus the control does not
refute an equality-specific or genuinely dynamic gluing theorem.

The exhaustive search observation that this is the smallest order, and
the separate absence of a \(\gamma=3\) extension through deletion order
ten, are labeled **OBSERVED**, not certified finite theorems.

## 1. The graph and marking

Let \(H'\) have vertex set \(\{0,\ldots,8\}\), canonical graph6 string

```text
HEhbtjK
```

and edge set

```text
03 04 07 08 13 15 16 18 24 25 26 27
36 37 46 48 57 58
```

Put

\[
 A=\{1,2,5,7,8\},
 \qquad
 R=\{0,3,4,6\}.
\tag{1.1}
\]

The six maximal cliques are

\[
\begin{array}{lll}
 136,&246,&037,\\
 257,&048,&158.
\end{array}
\tag{1.2}
\]

In particular,

\[
 S=\{1,5,8\}\subseteq A
\tag{1.3}
\]

is a full active root facet.

There is a useful human-readable identification.  The graph \(H'\) is
the line graph of \(K_{3,3}\).  One incidence labeling is

\[
\begin{array}{c|ccccccccc}
\text{line vertex}&0&1&2&3&4&5&6&7&8\\ \hline
K_{3,3}\text{ edge}
&a_2b_1&a_0b_2&a_1b_0&a_0b_1&a_2b_0
&a_1b_2&a_0b_0&a_1b_1&a_2b_2.
\end{array}
\tag{1.4}
\]

The six triangles in (1.2) are the six degree-three stars of \(K_{3,3}\).

## 2. Direct proof of the static assertions

### 2.1 Common neighbors and pure triangles — PROVED

View vertices of \(H'\) as edges of \(K_{3,3}\).  If two underlying edges
share an endpoint, the third edge at that endpoint is adjacent in the
line graph to both.  If they are disjoint, say \(a_i b_j\) and
\(a_k b_\ell\), then \(a_i b_\ell\) is adjacent to both.  Thus every pair
of vertices of \(H'\) has a common neighbor.

Because \(K_{3,3}\) is triangle-free and cubic, every maximal clique of
its line graph is one of its degree-three stars.  Hence (1.2) is the
complete maximal-clique list and every maximal clique is a triangle.

For \(G'=\overline{H'}\), these facts imply

\[
 \gamma(G')=\alpha(G')=3.
\tag{2.1}
\]

Indeed, the common-neighbor property says no pair dominates \(G'\);
each maximal \(H'\)-clique is a maximal independent triple of \(G'\).
A three-edge-coloring of \(K_{3,3}\) partitions \(V(H')\) into three
independent sets, equivalently partitions \(G'\) into three cliques.
The clique-product guard strategy therefore gives

\[
 \boxed{
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G')
 =(3,3,3,3,3).
 }
\tag{2.2}
\]

The standalone verifier checks all five parameters directly from their
definitions and finds 48 states in the greatest eternal triple-family.

### 2.2 Ridge covariance — PROVED, but vacuous in this control

Two distinct star triangles of \(L(K_{3,3})\) meet in at most one line
vertex.  Thus no two facets share a ridge.  The C-108 requirement that
opposite vertices across a shared ridge have equal active/inactive status
is satisfied vacuously.

This is an intentional scope warning: the example refutes the stated
static implication, but it does not exhibit nontrivial ridge transport.
A strengthened theorem may legitimately use connected ridge propagation.

### 2.3 Bipartite inactive graph and full root — PROVED

Under (1.4), \(R\) is the four-edge \(K_{2,2}\) on
\(\{a_0,a_2\}\) and \(\{b_0,b_1\}\).  Hence its line graph is

\[
 H'[R]=0\,3\,6\,4\,0\cong C_4,
\tag{2.3}
\]

which is bipartite.  Equation (1.2) directly shows that \(158\) is an
all-active triangle.

### 2.4 Exact coloring obstruction — PROVED

Up to permuting color names, \(H'\) has exactly two proper
three-colorings:

\[
\begin{split}
 \{0,1,2\}\mid\{3,4,5\}\mid\{6,7,8\},\\
 \{0,5,6\}\mid\{1,4,7\}\mid\{2,3,8\}.
\end{split}
\tag{2.4}
\]

The set \(R=\{0,3,4,6\}\) meets all three parts in both lines of (2.4).
Therefore every proper three-coloring uses all three colors on \(R\),
despite \(H'[R]\) itself being bipartite.  The verifier exhausts the
colorings rather than assuming the displayed list.

This proves Theorem 1.

## 3. Adding the target: exact failure boundary

Adjoin a vertex \(x=9\) to \(H'\), adjacent in \(H\) precisely to the
vertices of \(R\), and let

\[
 G=\overline H.
\tag{3.1}
\]

The labeled graph6 strings are

```text
H = IEhbtjKe_
G = IxU[ISrXW
```

Because every coloring in (2.4) uses all three colors on \(R=N_H(x)\),
\(H\) is not three-colorable.  Coloring \(x\) with a fourth color proves
\(\chi(H)=4\).

Every vertex marked active is physically adjacent to \(x\) in \(G\), and
every inactive vertex is not.  For every deletion facet \(T\) and every
\(v\in T\cap A\), the successor

\[
 T-v+x
\tag{3.2}
\]

dominates \(G\).  Thus the example passes all prescribed one-step target
response checks, including all three responses from the full root \(158\).

Nevertheless,

\[
 N_H(x)\cap N_H(5)=R\cap\{1,2,7,8\}=\varnothing.
\tag{3.3}
\]

Equivalently, \(\{x,5\}\) dominates \(G\).  Direct evaluation gives

\[
 \boxed{
 (\gamma,i,\alpha,\gamma^\infty,\theta)(G)
 =(2,3,3,4,4).
 }
\tag{3.4}
\]

This is the precise equality boundary: the target extension fails
\(\gamma=3\), so it is not a conjecture counterexample.

## 4. Literal two-attack failure

The greatest-family deletion process begins with all 58 dominating
triples.  It deletes 36 states in round one and the remaining 22 in round
two.  Every deletion facet has rank two.  In particular, the full root
\(S=158\) passes every first-round obligation.

There is a shorter direct certificate.  Attack \(x=9\) from \(158\).
All three guards may legally answer and all three successors dominate.
The attacker then chooses:

\[
\begin{array}{c|c|c}
\text{first move}&\text{state}&\text{second attack}\\ \hline
1\to9&589&0\\
5\to9&189&0\\
8\to9&159&3.
\end{array}
\tag{4.1}
\]

In each row, every guard adjacent to the second attacked vertex produces
a non-dominating successor.  Hence no eternal triple-family can contain
the full root.  The verifier checks every legal second move, not just one
selected move.

Thus:

- one-step target domination does **not** kill the static control;
- one full round of the global kernel does **not** kill its deletion
  facets;
- the exact two-attack one-guard condition does kill it; and
- independently, the global equality condition already kills it through
  the dominating pair \(\{5,9\}\).

## 5. Bounded searches — OBSERVED only

`search_static.py` streams canonical unlabeled graphs from nauty `geng`,
then enumerates every union of the exact ridge-covariance equivalence
classes.  It uses the following sound discovery filters: connected,
\(K_4\)-free, minimum degree at least two, and at most
\(\lfloor n^2/3\rfloor\) edges.  These are necessary under the static
hypotheses and three-colorability.

The run found no static obstruction through order eight and found
`HEhbtjK` at order nine.  The bounded minimality statement is
**OBSERVED**, because no independent generator reconstruction or formal
coverage certificate was produced.

`search_layers.py` then required that the target extension retain the
every-pair-common-neighbor condition.  This is equivalent here to
\(\gamma(G)=\alpha(G)=3\).  It exhaustively streamed the same canonical
search through deletion order ten:

\[
\begin{array}{c|r|r|r}
n&\text{canonical candidates}&
\text{static equality graphs}&
\gamma=3\text{ gluing obstructions}\\ \hline
6&40&11&0\\
7&283&45&0\\
8&3,328&220&0\\
9&64,851&1,673&0\\
10&2,108,079&18,777&0.
\end{array}
\tag{5.1}
\]

This is a useful **OBSERVED bounded absence**, not a finite theorem.
In particular, it supplies no justification for claiming that
\(\gamma=3\) universally forces the desired coloring.

## 6. The surviving proof target

Conditionally assuming the all-length inactive-cycle theorem, the
equality-critical full-target branch has \(H'[R]\) bipartite.  The present
control shows that bipartiteness alone cannot finish the proof.

The smallest accurate next statement is:

> **OPEN gluing target.** Under the hypotheses of Theorem 1, add the
> equality-specific condition that the target extension has
> \(\gamma(G)=3\), and add the literal multi-step response constraints of
> the optimal eternal family.  Prove that \(H'\) has a proper
> three-coloring using at most two colors on \(R\).

The computation through order ten supports this target but is not
evidence of a universal proof.  A proof must use either:

1. the missing common-neighbor witness for every pair \(\{x,a\}\) with
   \(a\in A\), together with ridge/triangle propagation; or
2. an adaptive one-guard attack that eliminates every global
   precoloring obstruction.

The control pinpoints both mechanisms: its only dominating pair is
\(\{x,5\}\), and its full root is defeated in exactly two attacks.

## 7. Reproduction

From the campaign root:

```text
python3 -I -B -W error \
  math/working/inactive_bipartite_gluing/verify_countermodel.py
```

The exact output is `countermodel_verification.json`.

The discovery searches are:

```text
python3 -I -B -W error \
  math/working/inactive_bipartite_gluing/search_static.py \
  --min-order 6 --max-order 9 \
  --output math/working/inactive_bipartite_gluing/search_6_9.json

python3 -I -B -W error \
  math/working/inactive_bipartite_gluing/search_layers.py \
  --layer gamma3 --min-order 6 --max-order 10 \
  --output math/working/inactive_bipartite_gluing/gamma3_result.json
```

The search files and bounded absences remain `OBSERVED`.  Only the explicit
countermodel properties and the displayed attack certificate are claimed
as `PROVED`.
