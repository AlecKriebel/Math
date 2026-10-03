# Random-graph coloring growth rates: the expectation/root distinction

**Problem:** 30002320 / OWR-12481-005. **Disposition:** partial; the source conjecture is not resolved. No new theorem of general random-graph coloring is claimed.

## 1. Exact source question and conventions

In Amin Coja-Oghlan's contribution, “Random graph coloring,” the defining formula is on printed page 1098 and Conjecture 4 is on page 1099 of [Oberwolfach Report 18/2013](https://publications.mfo.de/handle/mfo/3349). The nth root is **inside** the expectation. This was checked against the rendered original page, not only text extraction. The report is in volume 10 (2013); its publication date is March 17, 2014.

Fix an integer k≥3 and a real d>0. We use labeled simple undirected graphs, m=m_n=⌊dn/2⌋, and G(n,m) uniform over the binomial(N,m) subsets of edges, where N=binomial(n,2). Put

\[
 Z_k(G)=\#\{\sigma:[n]\to[k]:\sigma(u)\ne\sigma(v)\text{ for every edge }uv\},\qquad
 F_{n,k}(d)=\mathbb E[Z_k(G(n,m_n))^{1/n}].
\]

We set 0^(1/n)=0 and use labeled colors. The source conjecture asks whether lim_n F_{n,k}(d) exists for every such k,d. The floor convention is our explicit implementation of fixed average degree; the arguments below also handle m_n/n→d/2 where stated. They do not establish invariance under arbitrary rounding at an unresolved critical point.

The accessible catalog snapshot displays instead

\[
 A_{n,k}(d)=(\mathbb E Z_k(G(n,m_n)))^{1/n}.
\]

That is a different, annealed first-moment problem. Its own plain-language “original statement” says expected nth root, in agreement with the OWR. Consequently a proof about A alone must not be reported as a solution of the OWR conjecture.

## 2. The literal annealed question has a complete elementary answer

**Proposition 1.** For fixed k≥2, d≥0 and m_n/n→d/2,

\[
 \lim_{n\to\infty}(\mathbb E Z_k(G(n,m_n)))^{1/n}
 = a_k(d):=k(1-1/k)^{d/2}.
\]

**Proof.** Write q=1−1/k. A coloring assignment with class sizes n_1,…,n_k has

\[
 T(\boldsymbol n)=\frac{n^2-\sum_i n_i^2}{2}
\]

allowed edges. Its probability of being proper is binomial(T,m)/binomial(N,m), with a zero numerator if T<m. The maximum T_n occurs when the class sizes differ by at most one. Thus T_n=q n²/2+O_k(1). A fixed balanced type has multinomial coefficient C_n at least k^n/(n+1)^k: balanced types maximize that coefficient, the sum over all types is k^n, and there are at most (n+1)^k types. Therefore, for all sufficiently large n,

\[
 \frac{k^n}{(n+1)^k}\frac{\binom{T_n}{m}}{\binom{N}{m}}
 \le\mathbb E Z_k(G(n,m))
 \le k^n\frac{\binom{T_n}{m}}{\binom{N}{m}}.
\]

Because m=O(n), T_n,N=Θ(n²),

\[
 \log\frac{\binom{T_n}{m}}{\binom{N}{m}}
 =\sum_{j=0}^{m-1}\log\frac{T_n-j}{N-j}
 =m\log q+O_{k,d}(1).
\]

Indeed T_n/N=q+O(1/n), and the accumulated without-replacement correction is O(m²/n²)=O(1). Dividing the logarithmic bounds by n proves the result. ∎

The same reasoning in the binomial graph model gives a different annealed limit:

\[
 \lim_n(\mathbb E Z_k(G(n,d/n)))^{1/n}=k\exp(-d/(2k)).
\]

For completeness, the number of monochromatic candidate edges is minimized at a balanced type, where it is n²/(2k)−n/2+O_k(1). The preceding multinomial bounds, with proper-coloring probability (1−d/n) to that power, give the displayed limit. Thus even these elementary annealed quantities cannot be interchanged between graph ensembles.

**Corollary 2 (a rigorous zero region).** Set

\[
 d_{\mathrm{FM}}(k)=\frac{-2\log k}{\log(1-1/k)}.
\]

For d>d_FM(k), the source quantity F_{n,k}(d) tends to zero. For every d,

\[
 \mathbb P(Z_k>0)\le F_{n,k}(d)\le k\mathbb P(Z_k>0),\qquad
 F_{n,k}(d)\le (\mathbb E Z_k)^{1/n}.
\]

The first pair follows from 1≤Z_k^(1/n)≤k on {Z_k>0}; the last inequality is Jensen's inequality. If d>d_FM(k), Proposition 1 has a_k(d)<1, so E Z_k decays exponentially. Markov's inequality and F≤k P(Z_k>0) prove the claim. No claim is made at equality d=d_FM(k).

For a concrete distinction, k=3 and d=6 give

\[
 A_{n,3}(6)\longrightarrow8/9,
 \qquad F_{n,3}(6)\longrightarrow0.
\]

Both statements concern exactly the same uniform simple G(n,3n) ensemble for sufficiently large n.

## 3. A self-contained low-density proof

**Proposition 3.** For every k≥3 and 0<d<1,

\[
 Z_k(G(n,\lfloor dn/2\rfloor))^{1/n}\xrightarrow{\mathbb P}a_k(d),
 \qquad F_{n,k}(d)\longrightarrow a_k(d).
\]

**Proof.** Choose d′ with d<d′<1. For all large n, the probability that any specified set of h distinct edges occurs is (m)_h/(N)_h≤(m/N)^h≤(d′/n)^h (and zero if h>m).

Let R be the number of vertices whose connected component contains a cycle. Such a vertex has a witness consisting of a simple cycle of length ℓ≥3 and a simple path of length r≥0 from a cycle vertex to that vertex, with all off-cycle path vertices distinct and outside the cycle. The number of such witnesses is at most n^(ℓ+r)/2: count a cyclic ordering, choose the attachment vertex, and then the ordered off-cycle vertices. Consequently

\[
 \mathbb E R\le\frac12\sum_{\ell\ge3}\sum_{r\ge0}(d')^{\ell+r}<\infty.
\]

Multiple witnesses only increase this upper bound, so R=O_P(1).

For each fixed L, the probability of any connected component with at most L vertices and at least one more edge than vertices is O_L(1/n). To see this, union-bound over its vertex set and the finitely many possible edge sets on ≤L vertices: an s-vertex, t-edge choice with t≥s+1 has expected number O(n^(s−t))=O(1/n). A complex component (one containing at least two independent cycles) either has >L vertices, forcing R>L, or belongs to this finite list. Hence its existence has limsup probability at most C/L. Letting L tend to infinity shows that with probability tending to one every component is a tree or unicyclic.

On that event every component is k-colorable, because k≥3. The union of cyclic components has R vertices and exactly R edges. Removing it leaves a forest with n−R vertices and m−R edges. A forest with v vertices and e edges has k^v q^e colorings. The cyclic union has between 1 and k^R colorings. Multiplication over components gives

\[
 \log Z_k(G)=n\log k+m\log q+O_k(R).
\]

Since R=O_P(1), division by n proves convergence in probability. The root is always between 0 and k, so boundedness upgrades convergence in probability to convergence of expectations. ∎

This is an elementary rederivation of an established regime, also discussed in Section 4.1 of [Bapst et al.](https://arxiv.org/abs/1404.5513). It does not extend the low-density range available in the literature.

## 4. What is already known beyond the elementary regime

[Coja-Oghlan, Krzakala, Perkins and Zdeborová, Theorem 1.2](https://arxiv.org/abs/1611.00814v4) (Advances in Mathematics 333, 2018) identifies a variational condensation threshold d_{k,cond} for every k≥3. Below it, n^(-1)log Z_k(G(n,d/n)) converges in probability to log k+(d/2)log(1−1/k). Above it, their theorem gives a strictly smaller exponential upper bound with high probability. The first assertion implies convergence of the expected root below condensation; the second does not give a limiting value above condensation. The theorem does not assert the boundary case. The transfer argument in Section 7 puts the below-condensation conclusion in G(n,⌊dn/2⌋) as well.

The earlier [Bapst et al. result](https://arxiv.org/abs/1404.5513) treats sufficiently large k. A literature review that mentions only that result misses the all-k 2018 extension, but this extension is not an all-density resolution.

[Bayati, Gamarnik and Tetali, Theorems 1–2 and Remark 3](https://arxiv.org/abs/0912.2444) prove finite-temperature pressure and optimum-value limits. Their coloring objective counts the maximum number of properly colored edges. Their partition-function theorem assumes finite inverse-temperature weight λ; Remark 3 explicitly distinguishes the hard-constraint extension. Zero-temperature optimization does not count exact zero-energy assignments. Their exponential rate for the probability of satisfiability likewise does not determine that probability when the exponential rate is zero.

[Ayre, Coja-Oghlan and Greenhill](https://arxiv.org/abs/1812.09691), Theorem 1.3, establish variational non-colorability upper bounds on the average degree. Those imply additional zero regions for the expected-root quantity wherever non-colorability holds with high probability. They do not establish a positive limiting entropy throughout the colorable region. The sources checked did not supply an all-k, all-d solution; this is a bounded literature check, not a proof that no newer result exists.

## 5. Why the straightforward hard-temperature and logarithmic arguments fail

Define the soft Potts partition function

\[
 Z_{\beta,k}(G)=\sum_{\sigma:[n]\to[k]}e^{-\beta M_G(\sigma)},
\]

where M_G is the number of monochromatic edges. For fixed finite G, Z_{β,k} decreases to Z_k as β→∞. The finite-temperature limit cannot simply be interchanged with n→∞.

**Exact obstruction to that inference.** Let H_n be the empty graph for even n and K_{k+1} together with n−k−1 isolated vertices for odd n (ignore finitely many small n). For every fixed β<∞,

\[
 \frac1n\log Z_{\beta,k}(H_n)\longrightarrow\log k.
\]

On odd n, the difference from n log k is the fixed constant log Z_{β,k}(K_{k+1})−(k+1)log k. But Z_k(H_n)^(1/n) equals k for even n and 0 for odd n, so it has no limit. This is a deterministic counterexample to the proposed implication from finite-temperature convergence, **not** a counterexample in the random-graph model of the conjecture.

Even a one-edge edit can cause an order-one change in the root: K_{k+1} minus one edge, with isolates added, has k! k^(n−k−1) colorings, while adding the missing edge makes the count zero. Thus a generic bounded-difference argument for log Z_k cannot be imported from finite β.

The expression E log Z_k is worse than merely difficult. For every fixed d>0 and all sufficiently large n, m_n≥binomial(k+1,2). A graph containing a prescribed K_{k+1} and m_n edges has positive probability. Therefore P(Z_k=0)>0 and the extended expectation E log Z_k=−∞ for each such n, including in the low-density regime of Proposition 3. A theorem asserting convergence of log Z/n *in probability* remains meaningful despite this fact; it is not a theorem about its unregularized expectation.

Clamping does not automatically fix the inference. log(max{1,Z_k}) is not additive under disjoint union: an uncolorable component annihilates the original product. Explicitly, for an uncolorable graph U and a nonempty edgeless graph V, the clamped logarithm is zero on U∪V but equals |V|log k on V alone.

## 6. A necessary condition: the coloring threshold must converge

**Proposition 4.** If the source expected-root limit exists for every d>0 for a fixed k≥3, then the sharp k-colorability threshold sequence converges.

**Proof.** The [Achlioptas–Friedgut sharp-threshold theorem, Theorem 1.1](https://cgi.di.uoa.gr/~optas/papers/k-col-threshold.pdf), supplies a sequence d_k(n) with an o(1) average-degree transition window. The elementary low- and high-density bounds keep it in a bounded interval away from zero. The graph-process coupling and binomial edge-count concentration transfer the two one-sided threshold assertions to G(n,⌊dn/2⌋).

If a=liminf d_k(n)<limsup d_k(n)=b, choose a<d<b and a fixed positive ε smaller than both gaps. On one subsequence, d_k(n)≤d−ε, so P(Z_k>0)→0 and F_{n,k}(d)→0. On another, d_k(n)≥d+ε, so P(Z_k>0)→1 and liminf F_{n,k}(d)≥1. This contradicts the assumed limit. ∎

This implication was already observed in the coloring literature; the proof is included to exhibit the precise obstruction. Its converse is not established here: convergence of the colorability threshold would not itself determine the positive-root expectation or behavior exactly at the threshold.

## 7. What conditioning and changing ensembles do permit

Write p_n=P(Z_k>0), and on that event S_n=(log Z_k)/n. Whenever p_n>0,

\[
 F_{n,k}(d)=p_n\,\mathbb E[e^{S_n}\mid Z_k>0],\qquad0\le S_n\le\log k.
\]

**Sufficient condition.** If p_n→p and S_n converges in probability under the conditional laws to a constant s, then F_{n,k}(d)→p e^s. This follows from boundedness of e^(S_n). If p=0, convergence of the conditional entropy is unnecessary. If the target is general d, both a probability limit and adequate control of the conditional entropy are missing; proving just one does not silently supply the other.

Here is the exact ensemble comparison. Let B_{n,k}(d)=E[Z_k(G(n,d/n))^(1/n)]. Couple all simple graphs by a uniformly random ordering of their N possible edges. Conditional on a binomial edge count, the initial segment has the binomial model's distribution. For every fixed 0<ε<d, its count lies between ⌊(d−ε)n/2⌋ and ⌊(d+ε)n/2⌋ with probability tending to one. Since the root is decreasing in the edges and bounded by k,

\[
 F_{n,k}(d+\varepsilon)-o(1)
 \le B_{n,k}(d)\le F_{n,k}(d-\varepsilon)+o(1).
\]

Conversely, using binomial graphs of parameters (d±ε)/n gives

\[
 B_{n,k}(d+\varepsilon)-o(1)
 \le F_{n,k}(d)\le B_{n,k}(d-\varepsilon)+o(1).
\]

Thus a limit known on a neighborhood transfers at continuity points of the limiting function. This proves the transfer below condensation, where the formula a_k(d) is continuous, and transfers open non-colorability regions. It does not settle equality at a discontinuity or an unresolved threshold.

Nor can one condition a with-replacement graph on simplicity and assume expectation limits are preserved. An event of probability bounded away from zero is enough to preserve a high-probability deterministic limit, but is insufficient for arbitrary expectation limits. For example, X_n=1_{S_n} and P(S_n)=1/2 have E X_n=1/2 and E[X_n|S_n]=1. In the coloring setting, self-loops are particularly important: any one loop forces Z_k=0. The model in Section 1 excludes them from the start.

## 8. Outcome

The literal outside-root display has the complete elementary answer in Proposition 1. The historically sourced inside-root conjecture is not solved or disproved here. Five substantive routes produced a corrected source statement, exact annealed and low-/high-density proofs, an updated credited condensation range, and explicit reasons why several tempting limit arguments do not close the remaining gap. No universal conditional-entropy limit, threshold-boundary limit, or hard-constraint interpolation theorem has been proved.
