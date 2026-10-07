# High-genus triangulations: five scoped approaches to the remaining diameter constant

Problem 30005926 / OWR-14298373-004. Author research record, 2026-10-07.

**Outcome: unresolved.** The typical-distance assertion is credited to Tanguy Lions. No proof of the diameter limit or the factor three is given here. The results below are elementary deductions, obstruction examples, a fixed-pattern counting calculation, and a conditional reduction. They are not asserted to be novel. None establishes new sharp constants for the uniform triangulation model.

## 0. Exact target and imported inputs

Let \(T_{n,g}\) be uniform among rooted, connected, orientable **type-I** triangulations with \(2n\) triangular faces; loops and parallel edges are allowed. The root is an oriented edge. There are \(3n\) edges and \(N=n+2-2g\) vertices. Fix \(g_n/n\to\theta\in(0,1/2)\). All logarithms below are natural. Neither endpoint regime, the dual metric, nor simple triangulations is included.

The source target is Budzinski's contribution to the 2024 Oberwolfach report, printed p.1399, with the size convention on p.1398 [O]. It asks for typical distance \(D_\theta\log n\) and diameter \(3D_\theta\log n\).

Imported facts, not re-proved here:

* [L, Theorem 1.1, p.2; model p.6] proves \(d(U,V)/\log n\to D_\theta\) in probability both for independent uniform vertices and for the initial vertices of independent uniform oriented edges. This is a 25 June 2026 preprint, v1.
* [B, Theorem 1] supplies upper and lower logarithmic diameter bounds. [B, Proposition 17] gives a constant \(t_\theta>0\) with \(\operatorname{diam}T-d(X,Y)\ge t_\theta\log n\) with high probability for the edge-rooted sampling.
* [B, Lemma 2, crediting Budzinski--Louf] supplies \(\tau(n-1,g_n)/\tau(n,g_n)\to\lambda(\theta)\), where \(\tau\) counts the rooted maps. The statement applies along every admissible sequence with the specified genus ratio.

The parameter definitions used in [L] and [B] are
\[
\lambda=\frac{h}{(1+8h)^{3/2}},\qquad
\frac{1-2\theta}{6}=\frac{h}{(1+8h)\sqrt{1-4h}}
 \log\frac{1+\sqrt{1-4h}}{1-\sqrt{1-4h}},
\quad
m=\frac{1-2h-\sqrt{1-4h}}{2h},\quad D_\theta=\frac1{\log(1/m)},
\]
with \(0<h<1/4\). The following work starts from these explicit inputs.

## 1. Approach 1: eliminate parameters and test candidate depth constants

### Proposition 1 (one-variable form and endpoint asymptotics)
Put \(t=1/D_\theta>0\). Then
\[
 m=e^{-t},\quad h=\frac{m}{(1+m)^2},\quad
 \lambda=\frac{m(1+m)}{(m^2+10m+1)^{3/2}},\qquad
 1-2\theta=\frac{3t\coth(t/2)}{\cosh t+5}.                 \tag{1}
\]
In particular
\[
 D_\theta\sim(240\theta)^{-1/4}\quad(\theta\downarrow0).
                                                               \tag{2}
\]
Writing \(\delta=1-2\theta\) and \(L=\log(1/\delta)\),
\[
 D_\theta^{-1}=L+\log L+\log6+o(1)\quad(\theta\uparrow1/2).
                                                               \tag{3}
\]
These are asymptotics of the known typical-distance constant, not uniform-in-\(\theta\) extensions of the random-map theorem.

**Proof.** Set \(s=\sqrt{1-4h}\). Direct cancellation gives \(m=(1-s)/(1+s)\); hence \(s=(1-m)/(1+m)\) and \(h=m/(1+m)^2\). Substitution yields the first three formulas and
\[
 1-2\theta=\frac{6m(1+m)\log(1/m)}{(1-m)(m^2+10m+1)}.
\]
Use \((1+m)/(1-m)=\coth(t/2)\) and \(m^2+10m+1=2m(\cosh t+5)\) to obtain (1). The original monotonic parameter correspondence ensures \(t\downarrow0\) as \(\theta\downarrow0\) and \(t\to\infty\) as \(\theta\uparrow1/2\). Taylor division gives
\[
 \theta=\frac{t^4}{240}-\frac{t^6}{4032}-\frac{t^8}{172800}+O(t^{10}),
\]
which proves (2). For large \(t\), (1) gives \(\delta=6te^{-t}(1+O(e^{-t}))\). Thus \(t-\log t=L+\log6+o(1)\). First this implies \(t/L\to1\), and substitution in \(\log t\) gives (3). \(\square\)

### Proposition 2 (a strict comparison relevant to rigid tubes)
For every interior \(\theta\), \(0<\lambda<m<1\). Consequently
\[
 a_\theta:=\frac1{3\log(1/\lambda)}<\frac{D_\theta}{3}.       \tag{4}
\]
**Proof.** Since \(m^2+10m+1>(1+m)^2\), the formula for \(\lambda\) yields
\(\lambda/m<(1+m)^{-2}<1\). Taking logarithms proves (4). \(\square\)

This comparison matters in Approach 4: a specified constant-width triangular tube has a much more expensive height tail than the conjectured generic trap. Replacing the growth parameter \(m\) by a face-count Boltzmann factor \(\lambda\) silently changes the proposed constant.

### Corollary 3 (credited strict gap)
For each \(\varepsilon>0\),
\[
 \mathbb P\{\operatorname{diam}T_{n,g_n}\ge
 (D_\theta+t_\theta-\varepsilon)\log n\}\longrightarrow1.
                                                               \tag{5}
\]
Indeed, intersect [B, Proposition 17] with the edge-rooted version of [L, Theorem 1.1], using its lower-tail convergence. The intersection has probability tending to one by the union bound. This is an immediate combination of published/preprint inputs, not an authored solution or a new strict-gap mechanism.

**Why this approach stops.** Parameter elimination does not identify extremal depths. The gap constant in (5) is not proved to be \(2D_\theta\), and the argument gives no matching upper bound.

## 2. Approach 2: quantify the passage from typical to extreme pairs

Let \(G\) be a random connected graph with deterministic vertex count \(N\), and let \(U,V\) be conditionally independent uniform vertices. Parallel edges and loops do not affect these statements. Write \(p(r)=\mathbb P(d(U,V)>r)\).

### Proposition 4 (geodesic witness bound)
For every real \(r\ge0\) and integer \(s\ge0\),
\[
 \mathbb P\{\operatorname{diam}G>r+2s\}
 \le \frac{N^2p(r)}{2(s+1)^2}.                              \tag{6}
\]
**Proof.** Let \(Z_r\) count ordered pairs at distance greater than \(r\). Then \(\mathbb E Z_r=N^2p(r)\). On the event in (6), choose a geodesic \(v_0,\ldots,v_\ell\) with \(\ell>r+2s\). Its first \(s+1\) and last \(s+1\) vertices are disjoint. Each pair \((v_i,v_{\ell-j})\), \(0\le i,j\le s\), has distance \(\ell-i-j>r\), since every subpath of a geodesic is geodesic. Counting both orders gives \(Z_r\ge2(s+1)^2\). Taking expectations proves the claim. \(\square\)

The case \(s=0\) is the exact unordered-pair union bound. Taking \(s\) proportional to \(\log n\) saves a squared logarithm but still asks for a polynomially small typical-pair tail. The assertion \(p((D_\theta+\varepsilon)\log n)=o(1)\) alone is far weaker.

### Proposition 5 (a large, bounded-diameter metric subset)
If \(p(r_n)\to0\), then with probability tending to one there is a vertex set \(S_n\) with \(|S_n|=(1-o(1))N\) and ambient metric diameter at most \(2r_n\). More explicitly, when \(0<p(r_n)\le1\), with probability at least \(1-\sqrt{p(r_n)}\) one may choose
\[
 |S_n|\ge(1-\sqrt{p(r_n)})N,\qquad
 \max_{x,y\in S_n}d_G(x,y)\le2r_n.                         \tag{7}
\]
**Proof.** Given \(G\), put \(Q=Z_{r_n}/N^2\). Markov gives \(Q\le\sqrt{p(r_n)}\) except with probability at most \(\sqrt{p(r_n)}\). Some row of the distance matrix has at most \(QN\) entries exceeding \(r_n\), because its average row count is \(QN\). Its center \(v\) has a ball \(S_n=B(v,r_n)\) of the claimed size. The triangle inequality bounds distances inside this ball by \(2r_n\). If \(p=0\), all pairs satisfy the bound almost surely. \(\square\)

Applied to [L], this gives a subset containing almost all vertices and with diameter at most \(2(D_\theta+\varepsilon)\log n\). It does not control distances from the omitted vertices, and its subset need not have intrinsic diameter bounded by the same number.

**Why this approach stops.** A vanishing fraction of exceptional vertices can carry the diameter. Neither (6) nor (7) creates the rate or covering-radius bound needed for \(3D_\theta\).

## 3. Approach 3: a surface-preserving obstruction to the naive implication

### Construction
Let \(P_\ell\) be a triangulated disk with boundary a triangle \(C_0\). Add triangular cycles \(C_1,\ldots,C_\ell\). For each \(j=1,\ldots,\ell\) and \(i\in\mathbb Z/3\mathbb Z\), triangulate the strip by the faces
\[
 (v_{j-1,i},v_{j-1,i+1},v_{j,i+1}),\qquad
 (v_{j-1,i},v_{j,i+1},v_{j,i}).
\]
Cap \(C_\ell\) with one triangle. The patch has \(6\ell+1\) triangular faces, \(3\ell\) interior vertices, and \(9\ell\) nonboundary edges. Its height function is the layer index, changing by at most one along an edge.

### Proposition 6 (tube surgery)
Replace any face of a type-I triangulation \(T\) of size \(2n\) and genus \(g\) by \(P_\ell\), respecting the three boundary corners, to obtain \(\widetilde T\). Then:

1. \(\widetilde T\) is a type-I triangulation of the same genus, with \(2(n+3\ell)\) faces and \(N+3\ell\) vertices.
2. Every distance between original vertices is unchanged.
3. Every vertex of \(C_\ell\) has distance exactly \(\ell\) from the original vertex set. In particular \(\operatorname{diam}\widetilde T\ge\ell\).

The operation also makes sense when the original face has repeated boundary vertices or edges: use its three abstract corners before applying its boundary identifications.

**Proof.** Replace the characteristic disk of the face by another disk. Its boundary identifications are unaltered, so the underlying surface and its genus are unchanged. Counting the replaced faces and new vertices gives (1); the edge increment is \(9\ell\), also confirming Euler's formula. For (2), an excursion through the patch enters and leaves at old boundary vertices. These are either equal or adjacent in the original face, so replacing the excursion by a length-zero or length-one old path cannot increase length. Original paths remain available, proving equality of distances. For (3), extend the layer index by zero outside the patch. Every path from level \(\ell\) to an old vertex has at least \(\ell\) edges. Vertical edges exhibit a path of exactly that length. \(\square\)

### Corollary 7 (same typical asymptotic, arbitrarily larger diameter)
Suppose random base triangulations satisfy \(g_n/n\to\theta<1/2\) and \(d(U_n,V_n)/\log n\to D\) in probability. For any deterministic \(\ell_n=o(n)\), apply the surgery and set \(n'=n+3\ell_n\). The resulting, generally **nonuniform**, random triangulations satisfy
\[
 \frac{g_n}{n'}\to\theta,\qquad
 \frac{d(\widetilde U_n,\widetilde V_n)}{\log n'}\to D
 \quad\hbox{in probability}.                              \tag{8}
\]
Choosing \(\ell_n=\lceil(\log n)^2\rceil\) makes their diameter divided by \(\log n'\) tend to infinity. Choosing \(\ell_n=\lceil A\log n\rceil\) gives any prescribed lower bound \(A\) on its asymptotic normalized diameter.

**Proof.** Since \(N\sim(1-2\theta)n\), two uniform vertices of the modified map are both old with probability \((N/(N+3\ell_n))^2\to1\). Conditional on that event they are independent uniform old vertices, whose distances are preserved by Proposition 6. Also \(\log n'/\log n\to1\). The asserted genus ratio and diameter bounds follow directly. \(\square\)

**Scope.** This is not a counterexample to the problem, because the modified maps are not uniform in their size/genus class. It proves that uniform sampling information and control of rare decorations are indispensable; the topology and typical-distance asymptotic by themselves do not suffice.

## 4. Approach 4: count a specified tube and locate the missing precision

Let \(Y_\ell(T)\) count **oriented removal certificates** for \(P_\ell\). A certificate records a copy of its interior disk, its boundary corner identification, and one of the three oriented boundary sides. Removal and replacement by a single triangular face must produce a valid map. Interior vertices and nonboundary edges are distinct; the three outer boundary corners may be identified. Certificates, not unlabelled disk subsets, are counted.

### Proposition 8 (exact first moment and logarithmic upper cutoff)
For \(n-3\ell\ge2g-1\) and \(n>3\ell\),
\[
 \mathbb E Y_\ell(T_{n,g})
   =6n\frac{\tau(n-3\ell,g)}{\tau(n,g)}.                   \tag{9}
\]
Along \(g_n/n\to\theta\in(0,1/2)\), for \(\ell_n\sim c\log n\),
\[
 \mathbb E Y_{\ell_n}=n^{1-3c\log(1/\lambda(\theta))+o(1)}. \tag{10}
\]
Therefore, for each \(\varepsilon>0\), with high probability no removable tube \(P_\ell\) of height
\[
 \ell\ge (a_\theta+\varepsilon)\log n,
 \qquad a_\theta=1/(3\log(1/\lambda(\theta))),               \tag{11}
\]
occurs. This is a statement about the explicitly specified patch only.

**Proof of (9).** First count certificates for which the root edge is not one of the \(9\ell\) nonboundary patch edges. Deletion gives a rooted map with \(2(n-3\ell)\) faces and a marked oriented face side. There are \(6(n-3\ell)\tau(n-3\ell,g)\) such pairs. Insertion is its inverse, including for non-simple face boundaries.

To remove the root restriction, double-count rerootings while keeping the certificate. A map has \(6n\) root darts and the patch has \(18\ell\) internal darts. The fraction of permitted root darts is \((n-3\ell)/n\). This identity holds in sums over rooted maps even when the unrooted map has automorphisms: a rooted connected oriented map has no nonidentity root-fixing automorphism, and counting a second root dart gives the same multiplicity in the two directions. Thus the unrestricted expectation is \(n/(n-3\ell)\) times the restricted one, proving (9).

**Proof of (10).** For \(k_n=3\ell_n=O(\log n)\), telescope the imported ratio:
\[
 \log\frac{\tau(n-k_n,g_n)}{\tau(n,g_n)}
 =\sum_{j=0}^{k_n-1}\log\frac{\tau(n-j-1,g_n)}{\tau(n-j,g_n)}
 = k_n\log\lambda(\theta)+o(k_n).                          \tag{12}
\]
The error is uniform over this window. Otherwise there would be a subsequence and a choice of \(j\le k_n\) violating the sequential ratio limit, while \(g_n/(n-j)\to\theta\), a contradiction. Since \(\lambda(\theta)>0\), taking logarithms is harmless. Equations (9) and (12) imply (10).

Choose \(\ell_n=\lceil(a_\theta+\varepsilon)\log n\rceil\). Its expectation tends to zero, so Markov excludes it. Any longer \(P_\ell\) contains its innermost \(\ell_n\) annuli and cap, which form a removable \(P_{\ell_n}\); hence the same exclusion covers all larger heights. \(\square\)

By (4), the cutoff is strictly below \(D_\theta/3\). Consequently this particular rigid-tube family cannot supply two depth-\(D_\theta\log n\) extremal witnesses. Counting the much richer set of possible planar decorations is essential.

### Proposition 9 (one-step asymptotics alone do not give relative second-moment precision)
Fix \(0<q<1\). There exists a positive sequence \(b_n\) with \(b_{n-1}/b_n\to q\), but along integers \(n_j\to\infty\) and \(k_j\asymp\log n_j\),
\[
 \frac{b_{n_j-2k_j}b_{n_j}}{b_{n_j-k_j}^2}\to\infty.        \tag{13}
\]
**Proof.** For sufficiently large integers \(j\), put \(M_j=\lceil e^j\rceil\). These blocks \([M_j,M_j+2j]\) are disjoint. Define \(f_n=0\) off the blocks, and on each block let it decrease linearly from zero to \(-\sqrt j\) over \(j\) steps and then increase linearly back to zero over the next \(j\) steps. Adjacent differences tend to zero. Set \(b_n=q^{-n}e^{f_n}\). Then \(b_{n-1}/b_n=q e^{f_{n-1}-f_n}\to q\). At \(n_j=M_j+2j\), \(k_j=j\), the ratio in (13) equals \(e^{2\sqrt j}\). \(\square\)

This does not assert that actual triangulation counts behave this way. It identifies a genuine inference gap: (12), whose multiplicative error is \(n^{o(1)}\), cannot by itself justify a relative \(1+o(1)\) second-moment estimate at logarithmic scales. Diverging expectations alone do not prove that a tube exists with high probability.

**Why this approach stops.** It gives an upper cutoff for one narrow pattern family and diagnoses the missing precision for a matching lower bound. It neither enumerates all deep traps nor controls their joint locations.

## 5. Approach 5: a precise extreme-decoration criterion for the factor three

Here is an abstract sufficient-condition theorem. Its hypotheses are deliberately explicit and are **not established for uniform high-genus triangulations in this packet**.

### Lemma 10 (two high values under a second-moment hypothesis)
For a deterministic integer sequence \(M_n\asymp n\), let \(H_{n,1},\ldots,H_{n,M_n}\ge0\) be exchangeable random variables. Suppose \(\alpha>0\), and for every fixed \(0<\varepsilon<1/\alpha\), with
\(r_\pm=(1/\alpha\pm\varepsilon)\log n\), one has
\[
 \mathbb P(H_{n,1}>r_+)=n^{-1-\alpha\varepsilon+o(1)},\qquad
 p_-:=\mathbb P(H_{n,1}>r_-)=n^{-1+\alpha\varepsilon+o(1)},  \tag{14}
\]
\[
 \mathbb P(H_{n,1}>r_-,H_{n,2}>r_-)
       \le (1+o(1))p_-^2.                                 \tag{15}
\]
Then the largest and second-largest heights, each divided by \(\log n\), converge in probability to \(1/\alpha\).

**Proof.** The union bound and the first part of (14) exclude a height exceeding \(r_+\). Set \(Z=\sum_i1_{\{H_{n,i}>r_-\}}\); then \(\mu=\mathbb E Z=n^{\alpha\varepsilon+o(1)}\to\infty\). By exchangeability and (15),
\[
 \operatorname{Var}Z\le\mu+o(\mu^2),
\]
where an upper error can be replaced by its nonnegative part. Chebyshev implies \(Z/\mu\to1\) in probability, hence \(Z\ge2\) with high probability. These two bounds prove the lemma. Independence is sufficient but not necessary for (15). \(\square\)

### Lemma 11 (bounded-boundary metric decomposition)
Let a finite connected graph \(G\) consist of an isometric connected core \(C\) and decorations with disjoint interiors. Each decoration \(i\) meets the core precisely in a nonempty set \(A_i\) of ambient/core diameter at most \(b\), and there are no edges between distinct decoration interiors. Every path from an interior vertex to the rest of the graph meets \(A_i\). Choose an anchor \(a_i\in A_i\), let \(h(x)=d_G(x,A_i)\) for an interior vertex, and let \(H_i\) be its maximum over the decoration (zero for an empty interior). Put \(H=\max_iH_i\).

For vertices \(x,y\) in distinct decoration interiors,
\[
 h(x)+h(y)+d_C(a_i,a_j)-2b
 \le d_G(x,y)
 \le h(x)+h(y)+d_C(a_i,a_j)+2b.                            \tag{16}
\]
Moreover
\[
 \operatorname{diam}G\le2H+\operatorname{diam}C+2b.         \tag{17}
\]
**Proof.** For the upper bound connect each vertex by a shortest path to its boundary, move within the core to its anchor at cost at most \(b\), and join the anchors in the core. For the lower bound take a shortest \(x\)-to-\(y\) path and its first encounter \(p\in A_i\) and last encounter \(q\in A_j\). The prefix and suffix cost at least \(h(x),h(y)\). The intervening path has length at least \(d_G(p,q)=d_C(p,q)\), which is at least \(d_C(a_i,a_j)-2b\). Distinct interiors ensure that the first and last encounters occur in this order. If \(x,y\) are in the same decoration, connecting through its boundary costs at most \(h(x)+h(y)+b\). If a vertex is in the core use zero depth. These cases prove (17). \(\square\)

An attachment along a clique guarantees core isometry: replace every excursion through a decoration by a core edge or a constant path. The isometry assumption in the lemma is essential for arbitrary, non-clique boundaries.

### Theorem 12 (conditional diameter constant)
Suppose random decorated graphs have the preceding structure with \(b=o(\log n)\), a deterministic number \(M_n\asymp n\) of decorations, and satisfy:

1. The height hypotheses (14)--(15) for a constant \(\alpha>0\).
2. \(\operatorname{diam}C_n/\log n\to\beta\) in probability, for \(\beta>0\).
3. The anchors of a uniformly selected ordered pair of distinct attachment slots have distance divided by \(\log n\) converging in probability to \(\beta\).
4. Conditional on the core, its attachment slots, and the multiset of decorations, assigning decorations to slots is a uniform random permutation, independent of the auxiliary choice of two high decorations.

Then
\[
 \frac{\operatorname{diam}G_n}{\log n}
          \longrightarrow \beta+\frac2\alpha
 \quad\hbox{in probability}.                              \tag{18}
\]
In particular \(\beta=D_\theta\) and \(\alpha=1/D_\theta\) would yield the requested factor three.

**Proof.** Lemma 10 and (17) give the upper bound \(\beta+2/\alpha+o_{\mathbb P}(1)\). For a fixed small \(\varepsilon>0\), with high probability at least two decorations have height greater than \(r_-\). Select two by a rule depending only on the decorations and extra independent randomness, not their assigned slots. Hypothesis 4 makes their slots a uniform distinct pair, conditional on all these data. The bad-distance event from hypothesis 3 still has unconditional probability tending to zero when intersected with the high-decoration event: condition on the core and sum its nonnegative conditional bad probability over an event of probability at most one. Thus their anchors are at least \((\beta-\varepsilon)\log n\) apart with high probability. Choose maximum-depth vertices in these two decorations and apply the lower bound in (16). This gives
\(\operatorname{diam}G_n\ge(\beta+2/\alpha-3\varepsilon)\log n-2b\)
with probability tending to one. Let \(\varepsilon\downarrow0\). \(\square\)

**What remains for the actual problem.** One needs an appropriate decomposition with negligible metric error, the sharp logarithmic-scale depth rate \(\alpha=\log(1/m_\theta)\), sufficient joint-tail control under the fixed total size/genus conditioning, uniform core-diameter control at constant \(D_\theta\), and the stated attachment exchangeability. Typical-pair convergence alone supplies none of these full hypotheses. This theorem makes the proposed mechanism testable but does not verify it.

## 6. Verification and claim boundaries

`verify.py` uses only Python's standard library. It checks rational parameter identities, exact Taylor coefficients, finite graph inequalities, explicit triangulated-tube face/edge counts and old-distance preservation, bounded-boundary metric inequalities, and finite negative controls. Decimal numerical values are diagnostics, not interval certificates. The exact finite checks support the encoded constructions; they are not proofs of the asymptotic statements or of any imported theorem.

No simulated distribution is presented as the uniform high-genus model. No finite computation proves the diameter limit. The five approaches are the mathematical sections 1--5. Source collection, duplicate checking, verification, packaging, and independent review do not add author turns.

## References

[O] Thomas Budzinski, “Random triangulations in high genus,” contribution to *Statistical Physics and Random Surfaces*, Oberwolfach Reports 21 (2024), pp.1398--1400; target p.1399. DOI: https://doi.org/10.4171/OWR/2024/25 . Public report: https://publications.mfo.de/bitstream/handle/mfo/4220/OWR_2024_25.pdf?sequence=1 .

[L] Tanguy Lions, *Typical distances in high-genus triangulations*, arXiv:2606.27357v1, 25 June 2026. https://arxiv.org/abs/2606.27357v1 . Full theorem: https://arxiv.org/html/2606.27357v1#S1.Thmtheorem1 .

[B] Thomas Budzinski, Guillaume Chapuy and Baptiste Louf, *Distances and isoperimetric inequalities in random triangulations of high genus*, Annals of Probability 53 (2025), 1645--1667, DOI https://doi.org/10.1214/24-AOP1746 . The theorem numbering and pages inspected here refer to the author's November 8, 2023 preprint, https://perso.ens-lyon.fr/thomas.budzinski/papers/diameter_high_genus.pdf ; arXiv record https://arxiv.org/abs/2311.04005 .
