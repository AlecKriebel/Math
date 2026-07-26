# Bounded structural lane for the order-13, parameter-five slice

## Status and claim boundary

This is a bounded working note, not an accepted campaign claim.  It records
two serious analytic mechanisms and stops where each requires an unavailable
classification.  One complete reduction is proved:

> Any minimum order-13 counterexample with common parameter five has a
> degree-two vertex, and deletion of its closed neighborhood leaves a
> ten-vertex equality kernel with common parameter and clique-cover number
> four.

Several exact attachment constraints are then derived.  They do not yet
exclude the slice.

All eternal-domination statements use the one-guard-moves model.  The
external results used here concern only the ordinary static domination
number, so there is no import from an all-guards eternal variant.

## 1. Inputs and source audit

Assume that \(G\) is a counterexample of order \(13\) with

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=5<\theta(G).
\tag{1.1}
\]

Relative to C-050, it is a minimum-order counterexample.  The accepted
campaign inputs give:

1. \(G\) is connected;
2. C-048: \(G\) has no simplicial vertex, \(\delta(G)\geq2\), and the two
   neighbors of every degree-two vertex are nonadjacent;
3. C-049: the McCuaig--Shepherd bound is applicable, but at \(n=13\) it
   yields only
   \[
   \gamma(G)\leq 2n/5=26/5,
   \]
   hence the integral bound \(\gamma(G)\leq5\), not a contradiction; and
4. C-051: deleting the closed neighborhood of any independent \(t\)-set
   projects the common parameter from \(5\) to \(5-t\); minimum-order
   minimality also makes the projected clique-cover number \(5-t\).

The exact ordinary-domination sources checked in this bounded lane are:

- W. McCuaig and B. Shepherd, *Domination in Graphs with Minimum Degree
  Two*, Journal of Graph Theory **13**(6) (1989), 749--762,
  DOI `10.1002/jgt.3190130610`.  Its theorem applies to connected graphs of
  minimum degree at least two outside seven exceptions: \(C_4\) and six
  order-seven graphs.  Those exceptions are irrelevant at order 13.
- M. A. Henning, I. Schiermeyer, and A. Yeo, *A New Bound on the Domination
  Number of Graphs with Minimum Degree Two*, Electronic Journal of
  Combinatorics **18**(1) (2011), P12, DOI `10.37236/499`.  Theorem 1 is the
  official open-access restatement used to verify the exact
  McCuaig--Shepherd hypotheses and exception inventory.
- B. Reed, *Paths, Stars and the Number Three*, Combinatorics, Probability
  and Computing **5** (1996), 277--295.  Reed proves that every graph of
  minimum degree at least three has
  \[
  \gamma(G)\leq 3|V(G)|/8.
  \tag{1.2}
  \]
- A. V. Kostochka and C. Stocker, *A New Bound on the Domination Number of
  Connected Cubic Graphs*, Siberian Electronic Mathematical Reports
  **6** (2009), 465--504, Math-Net identifier `semr77`.  Its stronger
  connected-cubic bound has a cubic hypothesis and therefore cannot be
  applied to an arbitrary graph with minimum degree three.

No equality or stability refinement of the McCuaig--Shepherd theorem
sufficient to classify the order-13 value \(\gamma=5\) was found in the
bounded primary-source audit.  This is recorded as a missing tool, not as a
claim that no such theorem exists.

## 2. Route A: domination bounds

### Lemma 1 (a degree-two vertex is forced)

Under (1.1),

\[
 \delta(G)=2.
\tag{2.1}
\]

#### Proof

C-048 gives \(\delta(G)\geq2\).  If \(\delta(G)\geq3\), Reed's bound (1.2)
would give

\[
 \gamma(G)\leq\frac{3\cdot13}{8}=\frac{39}{8}<5.
\]

Since \(\gamma(G)\) is integral, this says \(\gamma(G)\leq4\), contrary to
(1.1).  Hence \(\delta(G)=2\). \(\square\)

Choose a degree-two vertex \(v\) and write

\[
 N_G(v)=\{a,b\}.
\tag{2.2}
\]

C-048 gives

\[
 ab\notin E(G).
\tag{2.3}
\]

The domination-bound route now stops.  The McCuaig--Shepherd inequality is
attained only after rounding at this order and supplies no further local
structure.  Ordinary domination data alone cannot make the desired
exclusion: the cycle \(C_{13}\) is connected, has minimum degree two, has no
simplicial vertex, and satisfies

\[
 \gamma(C_{13})=\left\lceil\frac{13}{3}\right\rceil=5.
\]

It fails other counterexample requirements, but it is an explicit witness
that the order, minimum-degree, nonsimplicial, and domination-number facts do
not contradict one another.  Continuing Route A would require a genuine
near-extremal classification that also incorporates
\(\alpha=5\), well-coveredness, or the eternal transition structure.  Such a
classification was not available in the checked sources.

## 3. Route B: the degree-two projection

Put

\[
 Q=G-N_G[v].
\tag{3.1}
\]

Since \(N[v]=\{v,a,b\}\), the graph \(Q\) has exactly ten vertices.
Define the two attachment masks by

\[
 A=N_G(a)\cap V(Q),\qquad B=N_G(b)\cap V(Q).
\tag{3.1a}
\]

### Lemma 2 (the ten-vertex equality kernel)

The graph \(Q\) is well-covered and

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=\theta(Q)=4.
\tag{3.2}
\]

#### Proof

Apply C-051 to the independent one-set \(\{v\}\).  Its projection theorem
gives well-coveredness and

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=5-1=4.
\]

Because \(G\) is minimum-order, the minimum-counterexample consequence of
C-051 gives \(\theta(Q)=4\). \(\square\)

The projection has two further exact consequences.

### Lemma 3 (the global clique-cover number is exactly six)

\[
 \theta(G)=6.
\tag{3.3}
\]

Moreover, for every partition

\[
 V(Q)=C_1\mathbin{\dot\cup}C_2\mathbin{\dot\cup}
 C_3\mathbin{\dot\cup}C_4
\tag{3.4}
\]

into four cliques, neither \(a\) nor \(b\) is complete to any part \(C_i\).

#### Proof

A four-clique partition of \(Q\), together with the two cliques
\(\{v,a\}\) and \(\{b\}\), gives

\[
 \theta(G)\leq6.
\]

The counterexample inequality in (1.1) gives \(\theta(G)\geq6\), proving
(3.3).

Suppose, for example, that \(a\) were complete to some part \(C_i\) of a
four-clique partition of \(Q\).  Replace \(C_i\) by the clique
\(C_i\cup\{a\}\) and add the clique \(\{v,b\}\).  This would partition
\(G\) into five cliques, contradicting (3.3).  The argument for \(b\) is
symmetric. \(\square\)

Thus every minimum four-clique partition of \(Q\) obeys

\[
 \forall i,\quad
 C_i-A\ne\varnothing
 \quad\text{and}\quad
 C_i-B\ne\varnothing.
\tag{3.5}
\]

### Lemma 4 (a parameter-three common nonneighbor kernel)

Let

\[
 R=Q-(A\cup B),
\tag{3.6}
\]

the vertices of \(Q\) adjacent to neither \(a\) nor \(b\) in \(G\).  Then
\(R\) is nonempty, well-covered, and

\[
 \gamma(R)=\alpha(R)=\gamma^\infty(R)=\theta(R)=3.
\tag{3.7}
\]

#### Proof

The set \(\{a,b\}\) is independent by (2.3).  Its closed neighborhood in
\(G\) contains \(a,b,v\) and exactly the vertices of \(Q\) adjacent to at
least one of \(a,b\).  Hence

\[
 G-N_G[\{a,b\}]=R.
\]

Apply C-051 with \(t=2\).  Its projection and minimum-counterexample
consequence give nonemptiness, well-coveredness, and every equality in
(3.7). \(\square\)

In particular,

\[
 |R|\geq3.
\tag{3.8}
\]

There is also an internal local hierarchy.  For every \(q\in V(Q)\), the
set \(\{v,q\}\) is independent, and C-051 gives

\[
 Q-N_Q[q]
\quad\text{well-covered with}\quad
 \gamma=\alpha=\gamma^\infty=\theta=3.
\tag{3.9}
\]

### Exact point where the projection route blocks

The simplicial reduction cannot be applied to \(v\): its two neighbors are
nonadjacent, so \(N[v]\) is not a clique.  Accordingly there is no identity

\[
 \theta(G)=\theta(Q)+1.
\]

The actual identity is (3.3), two larger than \(\theta(Q)\).

Likewise, a four-clique partition of \(Q\) cannot automatically be extended
to a five-clique partition of \(G\).  Such an extension would work if \(a\)
or \(b\) were complete to one of its parts, but Lemma 3 shows that precisely
this incidence is forbidden.  C-051 controls the induced projections but
does not control the two attachment neighborhoods

\[
 A=N_G(a)\cap V(Q),\qquad B=N_G(b)\cap V(Q).
\tag{3.10}
\]

The eternal-family projection also does not lift conversely.  If \(I\) is a
maximum independent set of \(Q\), then
\[
 \{v\}\cup I
\]
is an independent five-set and is forced into every eternal five-family of
\(G\).  An attack at \(a\) may be answered either by the guard at \(v\) or
by a guard of \(I\cap A\).  If \(v\) moves to \(a\), the successor can
dominate \(b\) only if
\[
 I\cap B\ne\varnothing.
\tag{3.11}
\]
Other responses depend on private neighborhoods inside \(Q\).  The
symmetric condition holds for an attack at \(b\).  These are useful finite
filters, but they do not force a contradiction without classifying
\((Q,A,B)\).

Route B therefore stops at a strictly smaller finite attachment problem.  It
does not reduce to the original universal conjecture, but an analytic finish
would require a classification of ten-vertex kernels satisfying (3.2),
(3.7), and (3.9), together with their admissible attachment masks.  No such
classification was available in the bounded lane.

## 4. Strongest current conclusion

### Proposition 5 (exact structural normal form)

Relative to C-050, any order-13 counterexample with common parameter five
has the following form.

1. \(V(G)=V(Q)\mathbin{\dot\cup}\{a,b,v\}\), where \(|V(Q)|=10\).
2. \(N(v)=\{a,b\}\) and \(ab\notin E(G)\).
3. \(Q\) satisfies (3.2) and the local hierarchy (3.9).
4. The common nonneighbor subgraph \(R\) in (3.6) satisfies (3.7).
5. \(\theta(G)=6\), and the attachment masks \(A,B\) satisfy the
   four-clique-partition obstruction (3.5).
6. \(G\) has no simplicial vertex, has \(\gamma=\alpha=5\), and must admit
   an eternal family of five-sets.

Every item has been proved above or is an accepted input.  Proposition 5 is
a reduction, not an exclusion.

## 5. Single best next finite template

The highest-value next step is **canonical attachment enumeration over the
ten-vertex kernel**, not a monolithic 59,280-variable parameter-five solve.

The finite cases are triples

\[
 (Q,A,B),
\]

where:

1. \(Q\) is an unlabeled ten-vertex graph satisfying (3.2) and (3.9);
2. \(A,B\subseteq V(Q)\) are the neighborhoods of \(a,b\);
3. cases are quotiented by \(\operatorname{Aut}(Q)\) and by swapping
   \(a,b\);
4. \(R=Q-(A\cup B)\) satisfies (3.7);
5. every four-clique partition of \(Q\) satisfies (3.5);
6. adjoining nonadjacent \(a,b\) and a vertex \(v\) adjacent exactly to
   \(a,b\) produces a nonsimplicial graph with
   \(\gamma=\alpha=5\) and \(\theta=6\); and
7. only survivors reach two independent exact one-guard evaluators at
   \(k=5\).

Coverage requires a canonical-generation proof and a manifest of every
kernel and attachment orbit.  Failure to find a survivor without those
artifacts would not exclude the slice.

## 6. Route registry

| route | status | exact obstruction |
|---|---|---|
| minimum-degree domination bounds | **exhausted for this lane** | Reed forces \(\delta=2\); McCuaig--Shepherd then permits \(\gamma=5\), and \(C_{13}\) witnesses feasibility of the remaining static profile |
| degree-two projection and clique cover | **blocked on a finite classification** | C-051 fixes \(Q\), \(R\), and \(\theta(G)=6\), but supplies no control of the attachment masks \(A,B\) sufficient to extend a four-clique partition or lift an eternal family |

No analytic contradiction was obtained.  The precise finite template in
Section 5 is the bounded lane's recommended continuation.
