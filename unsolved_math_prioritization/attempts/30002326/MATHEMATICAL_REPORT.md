# An all-order flower bound for disjoint homometric sets

Problem 30002326 / OWR-12481-016. Research note, 10 October 2026.

Project author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

## Review status of this edition

This is an AI-assisted research note accompanied by an independent internal AI mathematical audit. The note, reconstruction and audit are unrefereed. No external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification is claimed. Acceptance means acceptance within the explicit partial-result scope of the accompanying audit. Published theorems used below retain their original authors' credit and remain external dependencies; in particular, the Bollobás–Kittipassorn–Narayanan–Scott theorem is not independently reproved here.

## Status and exact question

**Partial result; the sublinearity question is not resolved.** We give an explicit graph of every sufficiently large order, with its homometric parameter calculated exactly. We also prove that the entire flower family used in this construction cannot establish sublinearity. The construction extends the odd-clique flower mechanism of Axenovich–Özkahya; no independent novelty claim is made.

Throughout, graphs are finite, simple, connected and unweighted, except that an auxiliary flower core may be disconnected. For a vertex set $A$, let $D_G(A)$ be the multiset of distances in the ambient graph $G$ between unordered distinct pairs of vertices of $A$. Define

\[
h(G)=\max\{k: A\cap B=\varnothing,
 |A|=|B|=k,\ D_G(A)=D_G(B)\},\qquad
h(n)=\min_{|V(G)|=n}h(G).
\]

The question is whether $h(n)/n\to0$. An affirmative answer requires suitable graphs for **every sufficiently large integer $n$** and a vanishing upper ratio. Neither an upper bound along an unspecified subsequence nor the linear bound proved below establishes that limit.

This is the operational min–max convention explicitly stated by Axenovich–Özkahya, with the connected restriction in Pach's question. The isolated Oberwolfach sentence omits its size clause. We do not assume that the alternative literal quantity

\[
\max\{k:\text{every connected n-vertex graph has a pair of exactly size k}\}
\]

is equivalent to this min–max parameter. The noninheritance example in §6 explains one reason that such an equivalence needs justification. Ordered-pair distance lists including the diagonal encode exactly the same information when the equal sizes are retained.

## 1. The all-order partial theorem

**Theorem 1.** For every integer $n\ge12^4=20736$, put

\[
k=k(n)=\left\lfloor\log_2(\log_{12}n)\right\rfloor.
\]

There is an explicitly defined connected $n$-vertex graph $G_n$ such that

\[
\boxed{h(G_n)=\left\lfloor\frac{n-k(n)+3}{4}\right\rfloor.}
\]

Consequently, with natural logarithms,

\[
h(n)\le \frac n4-\frac{\log\log n}{4\log2}+O(1)
\quad\text{for all sufficiently large (n)}.
\]

This proves an all-order version of the logarithmic-in-logarithm saving arising from odd-clique flowers. Its leading term is still $n/4$.

### Construction

Let $b_0=1$, and recursively set

\[
b_j=4\left(1+\sum_{i=0}^{j-1}b_i(b_i+1)\right)+1
\qquad (j\ge1).
\]

Every $b_j$ is odd. The first values after $b_0$ are $b_1=13$ and $b_2=741$. Define

\[
s=\left\lfloor\frac{n-k+1}{4}\right\rfloor,
\qquad q=k+2s,\qquad m=n-q.
\]

Take $a_i=b_i$ for $1\le i<k$ and

\[
a_k=q-\sum_{i=1}^{k-1}b_i.
\]

Let $H$ be the disjoint union of cliques of orders $a_1,\ldots,a_k$. Take a disjoint path $P=p_0p_1\cdots p_{m-1}$, and join $p_0$ to every vertex of $H$. There are no other edges between $P$ and $H$. This graph is $G_n$. In particular, $P$ has $m$ vertices, not $m$ edges, and $G_n$ has exactly $q+m=n$ vertices.

The proof is supplied in the next two sections, including the integer rounding and domination conditions.

## 2. A localization calculation for flowers

For a graph $X$, let $t(X)$ be the largest common order of two disjoint vertex sets inducing the same number of edges in $X$. No connectedness is required for $X$.

Let $G=F(H,m)$ be the flower just described, with $H\ne\varnothing$ and $m\ge2$. Write

\[
C=G[V(H)\cup\{p_0,p_1\}],\qquad
L=\max\left\{t(C),\left\lfloor\frac{m+1}{2}\right\rfloor\right\}.
\]

**Lemma 2.** Every such flower satisfies

\[
L\le h(G)\le\max\{3,L\}.
\]

In particular, $h(G)=L$ whenever $L\ge3$, and therefore whenever $m\ge5$.

**Proof.** The induced graph $C$ has diameter at most two and is isometric in $G$: adjacent vertices remain at distance one, and any other pair in $C$ has a two-edge path through $p_0$. Equal-order sets in $C$ are therefore homometric in $G$ exactly when they induce equal numbers of edges in $C$. This gives $h(G)\ge t(C)$. Also, for any $u\in V(H)$, the vertices $u,p_0,\ldots,p_{m-1}$ form an isometric path. Its two consecutive blocks of order $\lfloor(m+1)/2\rfloor$ are disjoint and homometric.

For the upper bound, take disjoint homometric $A,B$ of common order at least four. If no used path vertex lies beyond $p_1$, their union is in $C$. Otherwise, let $p_j$, $j\ge2$, be the used path vertex of largest index, and exchange the names of $A,B$ so that $p_j\in A$.

If $A$ also contained $u\in H$, then distance $j+1$ would occur in $D_G(A)$. Every path vertex of $B$ has index at most $j-1$; its distances to $H$ are at most $j$, distances within $H$ are at most two, and distances within the path are smaller still. Thus distance $j+1$ could not occur in $D_G(B)$. Hence $A\subseteq P$.

The greatest distance within $A$ is at least three and is realized once, by its two extreme path vertices. If $B\cap H\ne\varnothing$, then $B\cap P\ne\varnothing$, since distances inside $H$ are at most two. Let $p_i$ be the largest-index path vertex of $B$. The greatest distance in $B$ is $i+1\ge3$, realized exactly $|B\cap H|$ times. Thus $|B\cap H|=1$. Consequently $A\cup B\subseteq P\cup\{u\}$ for some $u\in H$. If $B\cap H=\varnothing$, the same containment holds with any $u\in H$.

Every pair of common order at least four is therefore either supported on $C$, where its order is at most $t(C)$, or on $P\cup\{u\}$, where disjointness gives order at most $\lfloor(m+1)/2\rfloor$. Smaller pairs have order at most three. ∎

This is the localization mechanism of Axenovich–Özkahya, reproduced here to make the calculation self-contained. The revised author version states the needed threshold four in Lemma 12. The earlier arXiv version states a threshold two, which is too small. For example, take $H=P_3$ and $m=3$. The whole core $H$ and whole tail $P$ form homometric triples with profile $\{1,1,2\}$, but their union has neither of the two claimed localizations. In this example $L=2$ and $h(G)=3$, so the small exception in Lemma 2 is real. This is a source-version caution, not a newly claimed correction to the revised paper.

## 3. Exact calculation for the rapidly growing clique core

**Lemma 3.** Let $k\ge2$, $a_0=1$, and let $a_1,\ldots,a_k$ be positive odd integers satisfying

\[
a_j>4\left(1+\sum_{i<j}a_i(a_i+1)\right)
\qquad(1\le j\le k).
\tag{1}
\]

Let $C$ consist of a universal vertex $r$ joined to a disjoint union of cliques $Q_0,\ldots,Q_k$ of these orders. Set $q=\sum_{i=1}^k a_i$. Then

\[
\boxed{t(C)=\frac{q-k}{2}.}
\tag{2}
\]

**Proof.** Splitting $a_i-1$ vertices of every $Q_i$, $i\ge1$, equally between two sets and using neither $r$ nor $Q_0$ gives equal edge counts. This proves the lower bound in (2).

For the upper bound take any disjoint equal-order sets $A,B$ with equal induced edge counts. Put

\[
x_i=|A\cap Q_i|,\quad y_i=|B\cap Q_i|,\quad
z_i=x_i+y_i,\quad d_i=x_i-y_i,\quad u_i=a_i-z_i.
\]

Let $U=|V(C)\setminus(A\cup B)|$. We prove $U\ge k+2$. Since $|V(C)|=q+2$, this gives (2).

First suppose $r\notin A\cup B$. Equality of orders gives $\sum_i d_i=0$; equality of edge counts gives

\[
0=2(e_C(A)-e_C(B))=\sum_i d_i(z_i-1),
\quad\text{hence}\quad\sum_i d_i z_i=0.
\tag{3}
\]

If all $d_i=0$, each $z_i$ is even while $a_i$ is odd. Thus $u_i\ge1$ for every $i$, and the unused root gives $U\ge(k+1)+1$.

Otherwise let $j$ be the largest index with $d_j\ne0$, and write

\[
T=\sum_{i<j}a_i(a_i+1),\qquad S=\sum_{i<j}a_i.
\]

Equation (3) and $|d_i|\le a_i$ give $z_j\le T$. We cannot have $j=0$, since then $d_0z_0=0$ and $d_0\ne0$ would imply $z_0=0$, hence $d_0=0$. Thus $j\ge1$. By (1),

\[
u_j=a_j-z_j\ge a_j-T>3T+4.
\tag{4}
\]

There are $j$ positive $a_i$ preceding $a_j$, so $T\ge2j$; in particular $u_j\ge j+1$. For each $i>j$, equality $d_i=0$ forces $u_i\ge1$. Adding these $k-j$ omissions and the unused root gives $U\ge(j+1)+(k-j)+1=k+2$.

Now suppose the root is used; interchange $A,B$ so that $r\in A$. If their common order is $h$, then

\[
\sum_i d_i=-1,\qquad \sum_i z_i=2h-1.
\]

The root contributes $h-1$ edges to $A$, so equality of edge counts becomes

\[
0=\sum_i d_i(z_i-1)+2(h-1)
 =\sum_i(d_i+1)z_i.
\tag{5}
\]

Put $e_i=d_i+1$. Then $\sum_i e_i=k$. Let $j$ be the largest index with $e_j\ne0$, which exists since $k\ge2$. From (5), $|e_i|\le a_i+1$, and $|e_j|\ge1$, we again obtain $z_j\le T$. If $j=0$, (5) forces $z_0=0$, hence $e_0=1$, and then $\sum_i e_i=1$, contrary to $k\ge2$. Thus $j\ge1$, and (4) holds.

Since $e_i\le z_i+1$, $z_i\le a_i$, and $e_i=0$ for $i>j$,

\[
k=\sum_{i\le j}e_i
 \le S+T+j+1
 \le 2T+1.
\tag{6}
\]

The last inequality uses $j\le S$ and $2S\le T$. Equations (4) and (6) give

\[
u_j>3T+4>2T+3\ge k+2.
\]

Thus $U\ge k+2$ also when the root is used. ∎

### Completing the proof of Theorem 1

Let $S_j=\sum_{i=0}^j b_i$. The defining recurrence gives

\[
S_j+1\le 4S_{j-1}^2+5S_{j-1}+6
 \le 6(S_{j-1}+1)^2.
\]

Since $S_0+1=2$, induction yields

\[
S_j+1\le \frac{12^{2^j}}6.
\tag{7}
\]

The definition of $k$ gives $12^{2^k}\le n$, so

\[
\sum_{i=1}^k b_i=S_k-1\le n/6-2.
\]

Meanwhile $q=k+2\lfloor(n-k+1)/4\rfloor>n/2+k/2-3/2$. Therefore $q\ge\sum_{i=1}^k b_i$, and the enlarged last clique satisfies $a_k\ge b_k$. It is odd because $q\equiv k\pmod2$. All inequalities (1) remain true, including the one for the enlarged final clique.

Also $k\ge2$. Since $n\ge12^{2^k}\ge4k$,

\[
m=n-q\ge (n-k-1)/2\ge3n/8-1/2\ge5.
\]

The graph $C=G_n[V(H)\cup\{p_0,p_1\}]$ is precisely the cone in Lemma 3, with $Q_0=\{p_1\}$ and root $p_0$. Thus $t(C)=(q-k)/2=s$. Lemma 2 now gives

\[
h(G_n)=\max\left\{s,\left\lfloor\frac{n-k-2s+1}{2}\right\rfloor\right\}
 =\left\lfloor\frac{n-k+3}{4}\right\rfloor.
\]

The final identity follows by writing $n-k=4t+r$, $r\in\{0,1,2,3\}$: both sides are $t$ when $r=0$, and $t+1$ otherwise. Finally,

\[
k(n)=\frac{\log\log n}{\log2}+O(1),
\]

which proves the asymptotic bound. ∎

## 4. Why this mechanism cannot settle sublinearity

The following theorem uses the published result of Bollobás, Kittipassorn, Narayanan and Scott: uniformly over all $r$-vertex graphs $X$,

\[
t(X)\ge r/2-o(r).
\tag{8}
\]

**Theorem 4.** Uniformly over all flowers $F(H,m)$ with $H\ne\varnothing$, $m\ge2$, $q=|V(H)|$, and $n=q+m\to\infty$,

\[
h(F(H,m))=\frac12\max\{q,m\}+o(n).
\tag{9}
\]

In particular, the minimum of $h(G)/n$ over these flowers tends to $1/4$. Arbitrary changes to the core graph or to the relative tail size cannot produce a sublinear family within this construction class.

**Proof.** Lemma 2 and the trivial inequality $t(C)\le(q+2)/2$ bound $h(G)$ above by $\max\{q,m\}/2+3$. For the lower bound, fix $\varepsilon>0$. From (8) there is $R=R(\varepsilon)$ such that for all finite graphs $X$,

\[
t(X)\ge |V(X)|/2-\varepsilon|V(X)|-R/2.
\]

This is also valid below the threshold, by enlarging $R$ if necessary. Apply it to $C$, of order $q+2$, and combine it with the isometric-path lower bound from Lemma 2. We obtain

\[
h(G)\ge\tfrac12\max\{q,m\}-\varepsilon(n+2)-R/2-1.
\]

Dividing by $n$, letting $n\to\infty$, and then $\varepsilon\to0$ proves (9) uniformly. Since $\max\{q,m\}\ge n/2$, this gives the $1/4$ lower limit within flowers. Theorem 1 supplies flowers attaining that limit for every large order. ∎

This is a lower bound **inside the flower class**, not a lower bound $h(n)\ge(1/4-o(1))n$ for all connected graphs.

## 5. Other verified restrictions on a potential sublinear construction

If $S\subseteq V(G)$ has at most two distinct ambient pairwise distances, form an auxiliary graph on $S$ by making one of the distance values its edges. For equal-order subsets of $S$, equality of edge counts is exactly equality of their distance multisets. Therefore

\[
h(G)\ge t(X_S)\ge |S|/2-o(|S|).
\]

Consequently, a sequence $G_n$ with $h(G_n)=o(n)$ must have no linearly large two-distance subset. In particular its maximum degree must be $o(n)$, since the closed neighborhood of any vertex has ambient diameter at most two. Its diameter must also be $o(n)$, since a geodesic of $D$ edges yields homometric sets of order $\lfloor(D+1)/2\rfloor$. These restrictions do not prove that such a sequence exists or cannot exist.

Thus dense diameter-two random graphs cannot be witnesses. Replacing all distance counts by their maximum, or by a distance-preserving isomorphism test, changes the problem. A proposed random subdivision or weighted-distance construction would still need to control homometric sets involving **all** the subdivision vertices and to handle every sufficiently large final order. No such argument is proved here. The multicolour generalization of the equal-edge-count theorem cannot simply be assumed; it is posed as a further problem in the cited paper.

## 6. Exact-size formulation caution

An equal-size homometric pair need not contain a smaller homometric pair obtained by choosing the same smaller size from its two members. Here is an unweighted connected example.

Take disjoint four-vertex graphs $G[A]=K_{1,3}$ and $G[B]=K_3\cup K_1$, and join every vertex of $A$ to every vertex of $B$. Distances within either side are one for edges and two for nonedges. The two four-sets each induce three edges and have common profile $\{1,1,1,2,2,2\}$. A triple inside $A$ induces either zero or two edges; a triple inside $B$ induces either one or three edges. Hence no triple from $A$ is homometric to any triple from $B$.

This shows failure of inheritance **within the specified pair**. It does not show that the entire graph lacks other homometric triples, and it does not prove inequivalence of the two extremal conventions. That separate equivalence remains unproved in this note.

## 7. Credit, scope and remaining gap

Albertson–Pach–Young introduced the connected graph question and the kite upper-bound mechanism. Axenovich–Özkahya introduced the flower localization and the use of rapidly growing odd clique cores for a saving of order $log\log n$, stated for infinitely many $n$. Their construction is the starting point here. Lemma 3 gives a self-contained exact calculation under a stronger growth condition; enlarging the final clique and balancing the path then gives the all-order formula. We do not claim this interpolation has not appeared elsewhere.

The flower-family obstruction and two-distance restrictions use the equal-order/equal-edge-count theorem of Bollobás–Kittipassorn–Narayanan–Scott. Alon's source-checked lower bound $c(\log n)^2/(\log\log n)^2$ is compatible with the upper bounds here. The bounded source search did not locate a resolution of the requested limit; that is not an exhaustive literature or novelty certificate.

**Exact remaining gap:** no construction has been established with $h(G_n)/|V(G_n)|\to0$ for all sufficiently large orders, and no positive lower ratio along an unbounded sequence of orders has been established for the extremal function over all connected graphs. The proved flower upper bound still has ratio tending to $1/4$.

### References

1. János Pach, “Homometric sets in graphs,” in *Combinatorics and Probability*, Oberwolfach Reports, printed p. 1119. [Official report DOI](https://doi.org/10.4171/owr/2013/18).
2. Michael O. Albertson, János Pach and Michael E. Young, “Disjoint homometric sets in graphs,” *Ars Mathematica Contemporanea* 4 (2011), 1–4. [Journal article](https://doi.org/10.26493/1855-3974.174.027).
3. Maria Axenovich and Lale Özkahya, “On homometric sets in graphs,” *Australasian Journal of Combinatorics* 55 (2013), 175–187. [arXiv version](https://arxiv.org/abs/1203.1158); [revised author PDF, dated 5 December 2012](https://web.cs.hacettepe.edu.tr/~ozkahya/pub/homsets.pdf), Definition 11, Lemma 12 and Theorem 2.
4. Béla Bollobás, Teeradej Kittipassorn, Bhargav P. Narayanan and Alex Scott, “Disjoint induced subgraphs of the same order and size,” *European Journal of Combinatorics* 49 (2015), 153–166. [Publication DOI](https://doi.org/10.1016/j.ejc.2015.03.005); [arXiv](https://arxiv.org/abs/1312.1680). Theorem 1.1 and §5.
5. Noga Alon, “Problems and results in Extremal Combinatorics – III,” *Journal of Combinatorics* 7 (2016), 233–256. [Author-hosted PDF](https://web.math.princeton.edu/~nalon/PDFS/extremalIII4.pdf), §2, Theorem 2.1.
