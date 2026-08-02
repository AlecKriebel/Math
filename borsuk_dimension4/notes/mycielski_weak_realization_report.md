# The third Mycielski tower is not a diameter subgraph in four dimensions

**Checkpoint:** 2026-08-01 17:43 PDT
**Scope:** exact first-principles closure of the weak-realization caveat in
`mycielski_tower_report.md`; no literature search or external catalogue was
used.

## Status

The caveat is closed globally.

> **Theorem.** Let
> \[
> T_0=C_5,\qquad T_{r+1}=M(T_r).
> \]
> There is no finite set of points in \(\mathbb R^4\) whose diameter graph
> contains \(T_3=M^3(C_5)\) as a subgraph.

Thus accidental additional diameter edges cannot repair the exact-graph
obstruction. This theorem eliminates the 47-vertex Mycielski candidate, but
does **not** resolve the four-dimensional Borsuk conjecture.

The main proof combines the rank-four center-vector theorem in
[`diameter_vector_five_coloring.md`](diameter_vector_five_coloring.md) with an
explicit equivariant suspension for the Mycielski construction. A separate
slack-matrix enumeration is retained in Section 8 as independent finite
corroboration.

## 1. The geometric input

The center-vector theorem says that every diameter subgraph \(G\) of a
finite set in \(\mathbb R^4\) has unit vectors

\[
 n_v\in S^3
\]

such that

\[
 \langle n_u,n_v\rangle\le -\frac14
 \qquad(uv\in E(G)).                                  \tag{1}
\]

The theorem is expressly valid for a non-induced diameter subgraph, so it
already allows accidental diameter edges. Only the strict negativity in
(1), not the sharp value \(-1/4\), will be needed below.

We prove that \(T_3\) admits no assignment of unit vectors in \(\mathbb R^4\)
whose products are negative on its edges. This is stronger than what (1)
requires.

## 2. The probability-pair complex

For a finite loopless graph \(G\), let

\[
 \Delta(V(G))=
 \left\{\alpha\in\mathbb R_{\ge0}^{V(G)}:
                 \sum_v\alpha_v=1\right\}.
\]

Write \(\operatorname{supp}\alpha=\{v:\alpha_v>0\}\), and define

\[
 \mathcal H(G)=
 \left\{(\alpha,\beta)\in\Delta(V(G))^2:
   ab\in E(G)\text{ for every }
   a\in\operatorname{supp}\alpha,
   b\in\operatorname{supp}\beta
 \right\}.                                             \tag{2}
\]

This is a finite polyhedral cell complex: for every nonempty completely
cross-joined pair \((A,B)\), it contains the product cell
\(\Delta(A)\times\Delta(B)\). It is the probability-coordinate model of
\(\operatorname{Hom}(K_2,G)\).

There is an involution

\[
 \tau(\alpha,\beta)=(\beta,\alpha).                    \tag{3}
\]

It is free. Indeed, a fixed point would have equal, nonempty supports on the
two shores, so (2) would require a loop at every vertex of that support.

### 2.1 An obtuse representation gives an equivariant sphere map

Suppose unit vectors \(n_v\in S^{r-1}\) satisfy

\[
 \langle n_a,n_b\rangle<0\qquad(ab\in E(G)).           \tag{4}
\]

For \((\alpha,\beta)\in\mathcal H(G)\), put

\[
 x_\alpha=\sum_a\alpha_a n_a,
 \qquad
 y_\beta=\sum_b\beta_b n_b.                           \tag{5}
\]

The difference \(x_\alpha-y_\beta\) cannot vanish. If it did, with common
value \(z\), then

\[
 \|z\|^2
 =x_\alpha\mathbin{\cdot}y_\beta
 =\sum_{a,b}\alpha_a\beta_b
        \langle n_a,n_b\rangle<0,                      \tag{6}
\]

because every support pair is an edge and the weights sum to one. This is
impossible. Therefore

\[
 F_G(\alpha,\beta)=
 \frac{x_\alpha-y_\beta}{\|x_\alpha-y_\beta\|}         \tag{7}
\]

is a continuous map \(\mathcal H(G)\to S^{r-1}\). It is equivariant:

\[
 F_G\circ\tau=-F_G.                                    \tag{8}
\]

In particular, a rank-four obtuse representation of \(G\) gives an
equivariant map

\[
 \mathcal H(G)\longrightarrow S^3.                    \tag{9}
\]

## 3. The antipodal decagon in \(\mathcal H(C_5)\)

Number the vertices of \(C_5\) modulo five. The following ten oriented
edges, in cyclic order, are vertices of \(\mathcal H(C_5)\):

\[
\begin{split}
 e_0,\ldots,e_9={}&
 (0,1),(0,4),(3,4),(3,2),(1,2),\\
 & (1,0),(4,0),(4,3),(2,3),(2,1).
\end{split}                                             \tag{10}
\]

Every consecutive pair lies on an edge of the probability-pair complex.
For example, \((0,1)\) and \((0,4)\) lie in

\[
 \Delta(\{0\})\times\Delta(\{1,4\}),
\]

while \((0,4)\) and \((3,4)\) lie in

\[
 \Delta(\{0,3\})\times\Delta(\{4\}).
\]

The same alternating pattern continues around the list. Moreover,

\[
 \tau(e_k)=e_{k+5}\qquad(k\bmod 10).                  \tag{11}
\]

Mapping a regular decagon in \(S^1\) linearly around these ten complex
edges gives an equivariant map

\[
 S^1\longrightarrow\mathcal H(C_5).                   \tag{12}
\]

This base certificate is completely explicit; the companion program checks
all ten cells and all ten antipode identities.

## 4. Mycielski suspension, with every interpolation checked

Let \(M(G)\) have original vertices \(Oa\), shadow vertices \(Sa\), and
apex \(w\). Its edges are

\[
 Oa\,Ob,\quad Oa\,Sb,
 \quad Sa\,Ob\qquad(ab\in E(G)),                       \tag{13}
\]

together with

\[
 w\,Sa\qquad(a\in V(G)).                              \tag{14}
\]

Fix once and for all a probability distribution \(q\) supported on the
shadows; the uniform distribution will do. If
\(z=(\alpha,\beta)\in\mathcal H(G)\), use \(O\alpha\) and \(S\alpha\) for
the transported distributions on originals and shadows.

We define a path \(P(z,s)\in\mathcal H(M(G))\), \(0\le s\le1\), through
the following four nodes:

\[
 (O\alpha,O\beta)
 \longrightarrow
 (O\alpha,S\beta)
 \longrightarrow
 (\delta_w,S\beta)
 \longrightarrow
 (\delta_w,q).                                         \tag{15}
\]

Precisely, for \(0\le s\le1/3\), with \(\lambda=3s\), set

\[
 P(z,s)=
 \bigl(O\alpha,(1-\lambda)O\beta+\lambda S\beta\bigr).
                                                               \tag{16}
\]

For \(1/3\le s\le2/3\), with \(\lambda=3s-1\), set

\[
 P(z,s)=
 \bigl((1-\lambda)O\alpha+\lambda\delta_w,S\beta\bigr).
                                                               \tag{17}
\]

For \(2/3\le s\le1\), with \(\lambda=3s-2\), set

\[
 P(z,s)=
 \bigl(\delta_w,(1-\lambda)S\beta+\lambda q\bigr).
                                                               \tag{18}
\]

Every interpolation remains in the required complex:

1. In (16), every \(Oa\) on the left is adjacent to both \(Ob\) and
   \(Sb\) on the right because \(ab\in E(G)\).
2. In (17), both \(Oa\) and \(w\) on the left are adjacent to every
   \(Sb\) on the right.
3. In (18), \(w\) is adjacent to every shadow, including the whole support
   of \(q\).

Thus no interpolation relies on convexity across a missing edge. The first
endpoint is

\[
 I(z)=(O\alpha,O\beta),                                \tag{19}
\]

and the last endpoint

\[
 p_+=(\delta_w,q)                                      \tag{20}
\]

is independent of \(z\).

Let

\[
 \Sigma\mathcal H(G)=
 \bigl(\mathcal H(G)\times[-1,1]\bigr)/
 \bigl(\mathcal H(G)\times\{-1\},
       \mathcal H(G)\times\{1\}\bigr)                \tag{21}
\]

be the suspension, with involution

\[
 [z,t]\longmapsto[\tau z,-t].                         \tag{22}
\]

Define

\[
 \Phi_G([z,t])=
 \begin{cases}
   P(z,t),&0\le t\le1,\\
   \tau P(\tau z,-t),&-1\le t\le0.
 \end{cases}                                           \tag{23}
\]

At \(t=0\), the two definitions agree because

\[
 \tau I(\tau z)=I(z).                                  \tag{24}
\]

At the two suspension poles the values are the fixed points \(p_+\) and
\(p_-=\tau p_+\), so (23) descends continuously through the quotient. Its
definition also gives

\[
 \Phi_G([\tau z,-t])=\tau\Phi_G([z,t]).                \tag{25}
\]

We have proved the exact recursive lemma

\[
 \boxed{
 \Phi_G:\Sigma\mathcal H(G)\longrightarrow
                 \mathcal H(M(G))
 \text{ is equivariant}.}                              \tag{26}
\]

## 5. Three suspensions

Suspending an equivariant map \(S^k\to X\) gives an equivariant map
\(S^{k+1}\to\Sigma X\), where all spheres carry the antipodal involution.
Starting from (12) and applying (26) three times gives

\[
\begin{aligned}
 S^1&\longrightarrow\mathcal H(T_0),\\
 S^2&\longrightarrow\mathcal H(T_1),\\
 S^3&\longrightarrow\mathcal H(T_2),\\
 S^4&\longrightarrow\mathcal H(T_3),                  \tag{27}
\end{aligned}
\]

and every map in (27) is equivariant.

## 6. There is no equivariant map \(S^4\to S^3\)

For completeness, here is the standard short proof specialized to the
dimensions needed here.

Suppose \(f:S^4\to S^3\) were antipodal-equivariant. It would descend to

\[
 \bar f:\mathbb{RP}^4\longrightarrow\mathbb{RP}^3.    \tag{28}
\]

Let \(a\) and \(b\) be the degree-one generators of the mod-two cohomology
rings of \(\mathbb{RP}^3\) and \(\mathbb{RP}^4\), respectively. The lift
is equivariant, so a path from \(x\) to \(-x\) maps to a path from
\(f(x)\) to \(-f(x)\). Consequently \(\bar f\) sends the nontrivial loop
to the nontrivial loop, and

\[
 \bar f^*(a)=b.                                        \tag{29}
\]

The cellular calculation of real-projective-space cohomology gives

\[
 H^*(\mathbb{RP}^m;\mathbb F_2)
 \cong\mathbb F_2[t]/(t^{m+1}).                        \tag{30}
\]

But then

\[
 0=\bar f^*(a^4)=b^4\ne0,                              \tag{31}
\]

since \(a^4=0\) in \(\mathbb{RP}^3\), whereas \(b^4\) is the nonzero top
class of \(\mathbb{RP}^4\). This contradiction is the required
Borsuk--Ulam case.

## 7. Global conclusion

Assume that a diameter graph in \(\mathbb R^4\) contains \(T_3\). Apply the
center-vector theorem only to the prescribed \(T_3\) edges. Equation (1)
gives a rank-four obtuse representation and hence, by (7), an equivariant
map

\[
 \mathcal H(T_3)\longrightarrow S^3.                  \tag{32}
\]

Composing (27) and (32) produces an equivariant map

\[
 S^4\longrightarrow S^3,                              \tag{33}
\]

contradicting Section 6. Therefore \(T_3\) cannot be a diameter subgraph.

No assumption was made about the nonedges of \(T_3\). This is why the
argument rules out every possible accidental-edge augmentation at once.

## 8. Independent exact slack and supergraph census

Before the topological obstruction was found, the companion program also
performed an exact finite audit of the smallest augmentations. It is useful
as an independent check on the original slack argument.

Write the top Mycielski level as originals \(x_i\), shadows \(y_j\), and
apex zero, with \(i,j\in V(T_2)\). The nonnegative matrix

\[
 B_{ij}=1-\|x_i-y_j\|^2
       =-\|x_i\|^2+2\langle x_i,y_j\rangle             \tag{34}
\]

has rank at most five. Its zeros are precisely the top original--shadow
diameter edges, and its other entries are strictly positive when the full
diameter graph is fixed.

The tower \(T_3\) has 845 nonedges and is maximal triangle-free: every
nonedge has a common neighbor. Thus every proper supergraph starts by
creating at least one triangle.

There are 458 one-edge additions outside the top original--shadow block.
They do not change (34), so the exact rank-five/polytope contradiction from
`mycielski_tower_report.md` survives unchanged.

The remaining 387 additions are directed nonedges \((i,j)\) of \(T_2\),
identified with \(x_i y_j\). Their exact census is:

| terminal certificate | additions |
|---|---:|
| forced triangular \(6\times6\) support minor, contradicting \(\operatorname{rank}B\le5\) | 232 |
| local facet Euler contradiction | 33 |
| a forced ridge vertex has polygonal degree greater than two | 65 |
| a forced ridge contains a closed proper boundary cycle | 11 |
| the same ridge is forced into three displayed facets | 5 |
| current face certificate stops at an incomplete ridge | 30 |
| current face certificate stops at an edge needing unlisted ridges | 11 |
| **total** | **387** |

Hence 346 of the 387 cross additions, and 804 of all 845 one-edge
supergraphs, are independently excluded. The remaining 41 choices form
seven orbits under the order-ten dihedral action inherited from \(C_5\):

| row label in \(T_2\) | column label in \(T_2\) | representative | orbit | old common neighbors | stopping stage |
|---|---|---:|---:|---:|---|
| `O2(O1(c0))` | `S2(S1(c0))` | `(0,16)` | 5 | 2 | ridge |
| `O2(S1(c0))` | `O2(S1(c2))` | `(5,7)` | 10 | 4 | ridge |
| `O2(S1(c0))` | `S2(S1(c2))` | `(5,18)` | 10 | 2 | ridge |
| `S2(O1(c0))` | `O2(O1(c0))` | `(11,0)` | 5 | 4 | local completion |
| `S2(O1(c0))` | `S2(S1(c0))` | `(11,16)` | 5 | 3 | ridge |
| `S2(S1(c0))` | `O2(S1(c0))` | `(16,5)` | 5 | 3 | local completion |
| `S2(w1)` | `O2(w1)` | `(21,10)` | 1 | 5 | local completion |

These are only survivors of the auxiliary slack certificate; the global
topological proof excludes all of them and every larger augmentation.

The four monotone graph screens requested in the weak-realization audit were
also run exactly:

1. \(K_6-e\);
2. \(K_5\), which would force a five-part simplex partition despite the
   inherited six-chromatic subgraph;
3. a non-three-colorable common neighborhood of a diameter edge;
4. two completely cross-joined blocks, each containing two diameter edges.

All 845 one-edge supergraphs pass these four graph-only screens. This is a
useful negative result: none of the standard local obstructions sees the
first accidental edge. The rank and face-lattice conditions do the actual
finite pruning.

As a symmetry check, among the 60 augmentations obtained by adding one whole
dihedral orbit of cross edges, only six survived the auxiliary slack and
graph screens. Every one of the 127 nonempty unions of the seven diagonal
dihedral orbits is excluded by the local Euler certificate. Again, these
counts are corroboration rather than ingredients of the global proof.

## 9. Reproduction

The standard-library checker is

```text
borsuk_dimension4/search/mycielski_weak_realization.py
```

The topological construction has a finite combinatorial skeleton check:

```text
python3 borsuk_dimension4/search/mycielski_weak_realization.py --topological
```

It verifies:

1. all ten edges of the base probability-pair decagon;
2. the five-step antipode relation;
3. every original/original, original/shadow, and apex/shadow adjacency used
   in all three suspension maps;
4. the exact tower sizes and maximal triangle-freeness.

The analytic nonvanishing calculation (6), the suspension quotient gluing,
and the projective-space cohomology contradiction are proved above rather
than delegated to floating-point computation.

The independent one-edge census is reproduced by

```text
python3 borsuk_dimension4/search/mycielski_weak_realization.py \
  --single --skip-graph
python3 borsuk_dimension4/search/mycielski_weak_realization.py \
  --all-single-graph
python3 borsuk_dimension4/search/mycielski_weak_realization.py \
  --symmetric-orbits
python3 borsuk_dimension4/search/mycielski_weak_realization.py \
  --diagonal-unions
```

No numerical feasibility output is used anywhere in the theorem.

## 10. Research log

- **2026-08-01 16:40--17:32 PDT.** Re-expressed every weak realization by
  its top cross-layer zero pattern. Proved that a first accidental edge must
  lie in that block, found forced rank-six minors, and audited the augmented
  four-polytope face complexes. Final one-edge census: 804 excluded, 41
  auxiliary survivors.
- **2026-08-01 17:32--17:43 PDT.** Combined the new center-vector theorem
  with the explicit probability-pair decagon and a three-stage Mycielski
  contraction. Three equivariant suspensions force
  \(S^4\to\mathcal H(T_3)\); the obtuse rank-four vectors would force
  \(\mathcal H(T_3)\to S^3\), contradicting the projective-space form of
  Borsuk--Ulam. This closes the weak-realization caveat globally.
