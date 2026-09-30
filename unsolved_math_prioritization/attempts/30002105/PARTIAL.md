# kNN observation scope and componentwise nonidentifiability

**Target:** 30002105 / OWR-11793-003.  
**Status:** **unsolved; two approaches.** Source-qualified partial results, not a solution of connected-support undirected recovery. Separate adversarial review is pending.  
**Attribution:** the directed density/metric and ordinal-embedding literature is credited below. Componentwise similarity ambiguity is a standard identifiability obstruction, already reflected in the per-component qualification of Hashimoto–Sun–Jaakkola. No novelty claim is made.

## 1. What the primary question observes

The original contribution is Ulrike von Luxburg's *Can we estimate the density from an unweighted, random k-nearest neighbor graph?*, in Oberwolfach Report **31/2012**, printed pp. 1914–1915 [O]. The imported report title's year 2013 is inaccurate for the actual report.

The source samples independent points \(X_1,\ldots,X_n\) from a density on \(\mathbb R^d\), and explicitly observes an **undirected, unweighted** graph. An edge is present if either endpoint is among the other's \(k\) nearest neighbors. Thus, with \(B\) the directed kNN adjacency matrix, the observed matrix is
\[
 A_{ij}=\max\{B_{ij},B_{ji}\},\qquad A_{ii}=0. \tag{1}
\]
It asks for density values at the sampled vertices up to multiplicative constants, and for approximate point recovery up to translation, rotation and scale. It gives no distances, coordinates, ordering of neighbors or edge directions. Its phrase “nice density” is not a formal hypothesis list; the contribution does not specify connectedness, a density lower bound, a regime \(k=k_n\), a loss or a mode of convergence.

We retain these ambiguities rather than declare a theorem about another observation model to be a full answer. In particular:

- directed kNN observations contain more information than (1);
- one global scale is different from a separate scale on each disconnected component;
- finite-sample nonuniqueness does not by itself disprove asymptotic statistical recovery;
- a counterexample for disconnected support does not settle the connected-support question that the later literature studies.

## 2. The exact scope of the credited literature

The full papers, rather than their abstracts alone, were checked.

1. **von Luxburg–Alamgir (2013) [L].** Section 2 uses directed edges, a compact support with a connected nonempty interior core, and a positive C¹ density bounded above and below. Section 4 analyzes a geometric, hypothetical gradient estimate. Crucially, §5 describes the graph-only multidimensional estimator as a conjecture and explicitly says that a formal proof is missing; its weaker proved variant uses quantities unavailable from the graph alone. The undirected-to-directed common-neighbor procedure in §7 is a sketch. These limitations cannot be removed by citing the abstract's affirmative language.
2. **Terada–von Luxburg (2014) [T].** Theorem 3 and Proposition 4 concern the directed-neighbor observation model, with compact connected convex full-dimensional support, a smooth boundary, positive C¹ density and a dense growing-neighbor regime. They are credited as directed ordinal-embedding results, not transferred to (1). This package does not undertake an independent all-details audit of those published proofs.
3. **Hashimoto–Sun–Jaakkola (2015) [H].** Its Theorem 2.1 and Corollary 2.3 give the directed-graph stationary-distribution recovery theorem under the full condition (⋆): path-connected compact domain, density/log-gradient regularity, a uniformly convergent radius scale, and almost-sure uniform equicontinuity of the rescaled stationary masses. The paper states the last condition as an additional assumption and conjectures its automatic validity. For kNN graphs, the regime is \(k/n\to0\) with \(k=\omega(n^{2/(d+2)}(\log n)^{d/(d+2)})\). Its §2.1 explicitly qualifies disconnected recovery as componentwise. We do not suppress that qualification or the equicontinuity assumption.
4. **Cucuringu–Woodworth (2015) [W].** The synchronization construction takes ordinal constraints from directed neighbor information; its use of a symmetrized graph for an intermediate clustering step does not mean that all directions were absent from the input. Its empirical embedding and density demonstrations are not a universal theorem for the original undirected model.

A bounded current-literature search did not establish a full theorem for the original unspecified undirected model. This is an access-and-scope finding, not a proof that no such theorem exists.

## 3. An exact finite obstruction to recovering directions

Set \(d=1\), \(n=4\), \(k=2\), keeping vertex labels in the displayed order. Consider
\[
 X=(0,1,19/10,41/10),\qquad
 Y=(0,1,21/10,38/10).
\]
There are no tied distances from any vertex. Their outgoing-neighbor sets are
\[
\begin{array}{c|c|c}
 i&N_B^X(i)&N_B^Y(i)\\ \hline
 1&\{2,3\}&\{2,3\}\\
 2&\{1,3\}&\{1,3\}\\
 3&\{1,2\}&\{2,4\}\\
 4&\{2,3\}&\{2,3\}.
\end{array}
\]
Nevertheless their undirected graph is the same: \(K_4\) with only edge \(\{1,4\}\) deleted. Consequently no deterministic procedure can recover the exact directed kNN graph from every finite undirected kNN graph, even when \(d,n,k\) are supplied.

For vertex 3, the common-neighbor counts with vertices 1 and 4 are both one, while the count with vertex 2 is two. Thus the simple common-neighbor ranking cannot distinguish the two displayed outgoing sets; any fixed tie rule fails on one of them.

This is a **finite exact-recovery diagnostic only**. The two configurations have open neighborhoods preserving the indicated strict inequalities, but this fact does not by itself rule out an asymptotic estimator under a fixed connected sampling density. It also does not refute an approximate or distribution-specific version of the §7 sketch in [L].

## 4. Smooth disconnected densities with asymptotically identical graph laws

Here is a fully probabilistic obstruction to omitting connectedness. It applies even when the more informative directed graph is observed.

Fix \(d\geq1\), \(s>1\), and \(L=10s\). Let \(e_1\) be the first coordinate vector. Choose the smooth radial probability density
\[
 f(u)=C_d\exp\!\left(-\frac1{1-\|u\|^2}\right)
       \mathbf 1_{\{\|u\|<1\}},
\]
where \(C_d>0\) normalizes its integral. This is C∞ on all of \(\mathbb R^d\), positive on the open unit ball, and zero outside its closure. Define two fixed densities
\[
 p(x)=\tfrac12 f(x)+\tfrac12f(x-Le_1),
\qquad
 q(x)=\tfrac12 f(x)+\frac1{2s^d}
                  f\!\left(\frac{x-Le_1}{s}\right). \tag{2}
\]
Both are globally smooth, compactly supported, and have exactly two disjoint ball components. Their component masses are equal. The first component has radius one in both models; the second has radius one under \(p\) and radius \(s\) under \(q\). No single similarity takes one support to the other, because the unordered ratio of component radii is a similarity invariant.

Couple the samples by independent \(Z_i\sim\operatorname{Bernoulli}(1/2)\) and \(U_i\sim f\):
\[
 X_i=Z_iLe_1+U_i,\qquad
 Y_i=Z_iLe_1+s^{Z_i}U_i. \tag{3}
\]
Then \(X_i\) are i.i.d. from \(p\) and \(Y_i\) are i.i.d. from \(q\). Let \(N_j=\#\{i:Z_i=j\}\), and define
\[
 E_n=\{N_0>k_n,\ N_1>k_n\}.
\]
All within-component distances are at most \(2s\) in either model. All cross-component distances are at least \(L-1-s=9s-1>2s\). On \(E_n\), every vertex therefore has at least \(k_n\) closer vertices in its own component, so no directed kNN edge crosses components. Inside each component, (3) is a similarity and preserves every distance ordering. Consequently the entire **labelled directed** adjacency matrices coincide on \(E_n\); so do their union-symmetrizations (1), and their mutual-kNN versions.

For any fixed \(\alpha<1/2\), if \(k_n\leq\alpha n\), the binomial Hoeffding bound gives
\[
 \mathbb P(E_n^c)
 \leq 2\exp\{-2n(1/2-\alpha)^2\}. \tag{4}
\]
In particular, this holds eventually for every regime \(k_n/n\to0\), even if \(k_n\) diverges very quickly. The coupling inequality implies
\[
 d_{\rm TV}(\mathcal L(A_n^p),\mathcal L(A_n^q))
 \leq\mathbb P(E_n^c)\longrightarrow0. \tag{5}
\]
The same conclusion holds for the directed observations. The densities in (2) are fixed, not chosen anew as a function of \(n\).

## 5. Why a single global density scale cannot fix (5)

Density values known up to one common multiplicative normalization determine their ratios. We show that even the ratio at the first two labelled sample vertices cannot be consistently recovered under both models.

Let \(R_p=p(X_1)/p(X_2)\) and \(R_q=q(Y_1)/q(Y_2)\), which are almost surely finite and positive. On the event \(Z_1=0,Z_2=1\),
\[
 R_q=s^dR_p. \tag{6}
\]
Choose any closed ball \(K\) strictly inside the unit ball with positive \(f\)-probability \(\beta\). On \(K\), let \(0<m\leq f\leq M\). On
\[
 F=\{Z_1=0,Z_2=1,U_1,U_2\in K\},
\]
we have \(\mathbb P(F)=\beta^2/4>0\) and
\[
 R_q-R_p\geq (s^d-1)m/M=:\Delta>0.
\]
Suppose a graph-based estimator \(\widehat R_n\) were consistent for the sample ratio under both \(p\) and \(q\). Couple any auxiliary randomization of the estimator identically. On \(E_n\), its two outputs are identical. On \(F\cap E_n\), they cannot both lie within \(\Delta/3\) of their respective targets. Thus
\[
 \mathbb P_p(|\widehat R_n-R_p|>\Delta/3)
 +\mathbb P_q(|\widehat R_n-R_q|>\Delta/3)
 \geq \beta^2/4-\mathbb P(E_n^c).
\]
The right side stays positive. This contradicts the proposed two-model consistency.

This proves an obstruction to globally normalized **consistent relative-density recovery**. The source's informal phrase about constant factors is not silently replaced by a particular fixed multiplicative-error criterion; the theorem specifies exactly which normalization-invariant target fails. Componentwise normalization would remove this particular contradiction, and is accordingly a different target.

## 6. The corresponding geometry obstruction

The ratio
\[
 T(X)=\frac{\|X_1-X_2\|}{\|X_3-X_4\|}
\]
is unchanged by every global translation, orthogonal transformation or nonzero scale. The inclusion of reflections only makes the permitted equivalence more generous.

Take the event \(Z_1=Z_2=0\), \(Z_3=Z_4=1\). Further restrict \(U_1,U_3\) to the ball of radius \(1/8\) centered at \(-e_1/2\), and \(U_2,U_4\) to the ball of radius \(1/8\) centered at \(e_1/2\). Call this event \(F'\). It has a fixed positive probability. Both relevant within-component distances under \(p\) lie in \([3/4,5/4]\), so \(T(X)\geq3/5\). Under the coupling,
\[
 T(Y)=T(X)/s,
 \qquad T(X)-T(Y)\geq(1-s^{-1})3/5>0.
\]
The same coupled-output argument as in §5 rules out a graph-only estimator of this similarity-invariant ratio that is consistent under both models.

In particular, no method can recover the entire labelled cloud under both models with maximal coordinate error tending to zero after one global similarity alignment. Such a recovery would estimate the displayed ratio consistently on \(F'\): pairwise distances change by at most twice the aligned coordinate error, and the denominator is bounded below there. Allowing a separate similarity for each component is again a distinct, weaker goal.

## 7. Exact remaining gap and status

The source's unrestricted phrase “nice density” does not determine whether disconnected densities such as (2) are admissible. Later positive papers impose connectedness and additional assumptions. Also, our coupling covers \(k_n/n\to0\), or more generally \(\limsup k_n/n<1/2\), not every possible choice of \(k_n\). Therefore the obstruction is recorded as a necessary-hypothesis result, **not a full negative answer to every intended version of the original question**.

The unresolved target retained here is recovery from the original **undirected union-kNN observation** under a precise connected-support regularity class and an appropriate specified neighbor regime. A complete positive transfer would require a proven recovery mechanism with sufficient error control; a finite exact-direction ambiguity is not an asymptotic impossibility theorem. This package supplies neither that positive mechanism nor a connected-support statistical counterexample.

The finite checker verifies the exact graph example, componentwise graph coupling on modest rational clouds, the normalization identities and finite binomial controls. The all-n statistical obstruction follows from the proof and (4), not from sampled graphs. No simulation is presented as proof of asymptotic consistency or impossibility.

## Primary references

[O] U. von Luxburg, contribution in *Learning Theory and Approximation*, Oberwolfach Report 31/2012, pp. 1914–1915. [Full report](https://ems.press/doi/pdf/10.4171/OWR/2012/31).

[L] U. von Luxburg and M. Alamgir, *Density estimation from unweighted k-nearest neighbor graphs: a roadmap*, NIPS 2013, especially §§2, 4, 5 and 7. [Published full text](https://proceedings.neurips.cc/paper_files/paper/2013/file/eae27d77ca20db309e056e3d2dcd7d69-Paper.pdf).

[T] Y. Terada and U. von Luxburg, *Local Ordinal Embedding*, ICML 2014, Theorem 3 and Proposition 4. [Published paper](https://proceedings.mlr.press/v32/terada14.html).

[H] T. Hashimoto, Y. Sun and T. Jaakkola, *Metric recovery from directed unweighted graphs*, AISTATS 2015, §2.1, Theorem 2.1 and Corollary 2.3. [Published paper](https://proceedings.mlr.press/v38/hashimoto15.html).

[W] M. Cucuringu and J. Woodworth, *Point Localization and Density Estimation from Ordinal kNN graphs using Synchronization*, arXiv:1504.00722v2 (2015). [Full author version](https://arxiv.org/abs/1504.00722v2).
