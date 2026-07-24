# A transversal-capacity obstruction for a regular \(R(5,5)\) endpoint

July 2026

## Abstract

We give an elementary capacity inequality for hypergraph transversals indexed
by the vertices of a graph. Applied to the cross-neighborhoods at a vertex of
a hypothetical 18-regular \((5,5;43)\)-graph, it excludes the endpoint

\[
e(G[N(v)])=85.
\]

On byte-pinned published \(R(4,5;18)\) and \(R(4,5;24)\) catalogs, the
inequality directly excludes 61,939 of 62,382 fixed-side pairs. The remaining
443 attain equality; uniqueness of a minimizing transversal forces two
adjacent cross-neighborhoods to coincide, contradicting the required
two-column covering condition. Conditional on the published catalog
completeness and extremal-edge statements, every vertex of an 18-regular
\((5,5;43)\)-graph therefore lies in at most 84 triangles.

This excludes one endpoint of one global branch. It does not determine
\(R(5,5)\).

## 1. Transversal capacity

Let \(U\) be finite, let \(\mathcal F,\mathcal Q\subseteq2^U\), and let \(J\)
be a graph with \(\alpha(J)\le a\). Assign a set \(X_b\subseteq U\) to every
\(b\in V(J)\), subject to:

1. \(X_b\) meets every member of \(\mathcal F\);
2. \(X_b\cup X_c\) meets every member of \(\mathcal Q\) whenever
   \(bc\in E(J)\).

For an integer \(s\), define

\[
q_s(U;\mathcal F,\mathcal Q)=
\min_{\substack{X\subseteq U,\ |X|=s\\
                 X\cap F\ne\varnothing\ \forall F\in\mathcal F}}
\left|\{Q\in\mathcal Q:X\cap Q=\varnothing\}\right|,
\]

with \(q_s=+\infty\) if no size-\(s\) transversal of \(\mathcal F\) exists.

**Transversal-capacity lemma.** Every such assignment satisfies

\[
\sum_{b\in V(J)}q_{|X_b|}(U;\mathcal F,\mathcal Q)
\le a|\mathcal Q|.
\]

**Proof.** For \(Q\in\mathcal Q\), put

\[
Z_Q=\{b\in V(J):X_b\cap Q=\varnothing\}.
\]

The second hypothesis makes \(Z_Q\) independent in \(J\), so
\(|Z_Q|\le a\). Double counting the incidences \((b,Q)\) for which
\(X_b\cap Q=\varnothing\) gives

\[
\sum_b q_{|X_b|}
\le \sum_b|\{Q:X_b\cap Q=\varnothing\}|
=\sum_Q|Z_Q|
\le a|\mathcal Q|.
\qquad\square
\]

The same proof permits fixed nonnegative weights \(w_Q\):

\[
q_s^w=\min_X\sum_{\substack{Q\in\mathcal Q\\X\cap Q=\varnothing}}w_Q
\quad\Longrightarrow\quad
\sum_bq_{|X_b|}^w\le a\sum_Qw_Q.
\]

This weighted form is an immediate template, not a tested claim about the
remaining Ramsey layers.

## 2. Ramsey specialization

Let \(G\) be a hypothetical 18-regular graph on 43 vertices with neither a
\(K_5\) nor an independent five-set. Fix \(v\in V(G)\), and write

\[
A=G[N_G(v)],\qquad
B=V(G)\setminus(N_G(v)\cup\{v\}),\qquad
H=\overline{G[B]}.
\]

Then \(|A|=18\), \(|H|=24\), and both \(A\) and \(H\) are \(R(4,5)\)-graphs.
In particular, \(\alpha(H)\le4\).

For \(b\in V(H)=B\), define

\[
X_b=N_G(b)\cap V(A).
\]

The absence of independent five-sets in \(G\) implies:

- \(X_b\) meets every independent four-set of \(A\);
- if \(bc\in E(H)\), then \(X_b\cup X_c\) meets every independent
  three-set of \(A\).

Indeed, a missed independent four-set together with \(b\), or a missed
independent triple together with the \(G\)-nonedge \(bc\), would be an
independent five-set.

Regularity determines the column sizes:

\[
18=|X_b|+\deg_{G[B]}(b)=|X_b|+23-d_H(b),
\]

so

\[
|X_b|=d_H(b)-5.
\]

Let \(\mathcal I_k(A)\) be the independent \(k\)-sets of \(A\), put
\(i_3(A)=|\mathcal I_3(A)|\), and define

\[
q_s(A)=
\min_{\substack{X\subseteq V(A),\ |X|=s\\
X\cap I\ne\varnothing\ \forall I\in\mathcal I_4(A)}}
|\{Q\in\mathcal I_3(A):X\cap Q=\varnothing\}|.
\]

The lemma, with
\(\mathcal F=\mathcal I_4(A)\), \(\mathcal Q=\mathcal I_3(A)\),
\(J=H\), and \(a=4\), gives the necessary condition

\[
\boxed{\displaystyle
\sum_{b\in V(H)}q_{d_H(b)-5}(A)\le4i_3(A).}
\]

## 3. Endpoint theorem

Counting cross edges from both sides gives

\[
e(H)=213-e(A).
\]

Thus \(e(A)=85\) is exactly the endpoint \(e(H)=128\).

We use two published-catalog inputs:

- the edge-85 \(R(4,5;18)\) cases are represented by 74 records;
- exactly 843 records in the complete published \(R(4,5;24)\) catalog have
  128 edges.

The exact catalog bytes are pinned by

\[
\begin{aligned}
\operatorname{SHA256}(\texttt{r4518.85.g6})
&=\texttt{46abaee2572d06bba1e594554809d784be60f8f60b9b0d3345b8bf3dd800810a},\\
\operatorname{SHA256}(\texttt{r45\_24.g6})
&=\texttt{83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0}.
\end{aligned}
\]

**Endpoint theorem.** Conditional on those catalog-completeness inputs, no
18-regular \((5,5;43)\)-graph has a vertex \(v\) with

\[
e(G[N_G(v)])=85.
\]

Together with the published extremal bound \(e(G[N_G(v)])\le85\), every
vertex of such a graph lies in at most 84 triangles.

**Proof.** There are

\[
74\cdot843=62,382
\]

fixed-side catalog pairs \((A,H)\). Exact computation of the transversal
minima excludes 61,939 pairs by a strict violation of the boxed inequality.

All 443 equality pairs use the same order-18 record, zero-based catalog index
50, and every associated \(H\) has degree sequence

\[
10^8\,11^{16}.
\]

For this exceptional \(A\),

\[
i_3(A)=74,\qquad q_5(A)=17,\qquad q_6(A)=10,
\]

and the size-six minimizer \(X^\ast\) is unique. The capacity inequality is
tight:

\[
8q_5(A)+16q_6(A)=8\cdot17+16\cdot10=296=4i_3(A).
\]

The two inequalities in the double count must therefore both be equalities,
and every column must attain its individual minimum. In particular, all
sixteen degree-11 vertices of \(H\) have cross-neighborhood \(X^\ast\).

Let \(D\) be those sixteen vertices. Every \(b\in D\) has at most eight
neighbors outside \(D\), hence at least three neighbors inside \(D\).
Therefore \(H[D]\) contains an edge \(bc\). But

\[
X_b\cup X_c=X^\ast,
\]

and \(X^\ast\) misses ten independent triples of \(A\), contradicting the
two-column condition. Thus none of the 443 equality pairs admits a
completion. \(\square\)

## 4. Verification and limitations

The classification is deterministic and solver-free. The certificate
producer and an independently written checker reconstruct:

- the 74 and 843 selected catalog records;
- every transversal minimum;
- all 61,939 strict exclusions;
- all 443 terminal equality contradictions;
- every line of the 62,382-record classification stream.

The saved check reports `valid=true`, and 17 focused semantic tests pass.

Local verification establishes byte identity, graph validity, edge filters,
counts, and the stated finite calculations. It does not independently
re-enumerate the complete \(R(4,5)\) catalogs; completeness and
nonisomorphism remain publisher inputs.

The theorem excludes only

\[
(e(A),e(H))=(85,128)
\]

inside the regular degree-18 branch. It does not exclude the layers with
\(e(A)=81,82,83,84\), the other five global branches, or all order-43
graphs. Consequently it does not change

\[
43\le R(5,5)\le46.
\]

The reusable contribution is the capacity view of the established
two-column gluing constraints. A genuinely stronger continuation would need
optimized weights or correlated missed-triple profiles that operate across
an entire remaining layer.
