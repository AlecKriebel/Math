# Coincidence sets of normalized univalent functions: partial results for Problem 6.83

## 1. Scope and conventions

Write \(\mathbb D=\{z:|z|<1\}\), and let \(S\) consist of injective holomorphic maps on \(\mathbb D\) with \(f(0)=0\) and \(f'(0)=1\). The question is to characterize sets \(Z\subset\mathbb D\) on which two different members of \(S\) agree. This note does **not** give a characterization for arbitrary \(Z\). It proves a useful sufficient condition, reconstructs an established necessary condition, and identifies two failed converse arguments.

Coincidence conditions depend only on the distinct points, not their enumeration or repetitions. All sums below are over distinct nonzero points of \(Z\). The point 0 is automatic. This qualification is essential: endlessly repeating 0 must not be used to infer a divergent-sum uniqueness theorem. A set with an interior accumulation point is a uniqueness set by the identity theorem.

Hayman and Lingham's Update 6.83 refers to the partial result of Overholt (2000). The necessary Dirichlet-space reduction in Section 2 is his result, reconstructed here with the area calculation included. No novelty is claimed for the sufficient conditions below; they are elementary constructions related to the older work of Lappan. His complete paper was not available for a theorem-by-theorem comparison.

## 2. Attempt 1: reciprocal differences and a necessary Dirichlet condition

Define the Dirichlet space by
\[
\mathcal D=\left\{h(z)=\sum_{n\ge0}d_nz^n:
\sum_{n\ge1}n|d_n|^2<\infty\right\}.
\]
Its seminorm equals \(\pi^{-1}\int_{\mathbb D}|h'|^2\,dA\).

**Proposition 1 (Overholt).** If distinct \(f,g\in S\) coincide on \(Z\), then a nonzero function in \(\mathcal D\) vanishes on \(Z\). More precisely,
\[
h=1/f-1/g\in\mathcal D,
\qquad \sum_{n\ge1}n|[z^n]h|^2\le4.
\]
The function \(h\) vanishes at all nonzero coincidence points; \(zh\) also vanishes at 0.

**Proof.** Since the only zero of either normalized injective function is 0, the simple poles in \(1/f-1/g\) cancel there. Define
\[
F(\zeta)=1/f(1/\zeta)=\zeta+b_0+\sum_{n\ge1}b_n\zeta^{-n},
\qquad |\zeta|>1.
\]
This map is injective. For \(r>1\), its image of \(|\zeta|=r\) is a smooth Jordan curve. The map takes the exterior to the unbounded component, so the bounded component has nonnegative area. The usual boundary area integral, with the Laurent series integrated term by term on this circle, is
\[
A_r=\frac1{2i}\int_{|\zeta|=r}\overline{F(\zeta)}F'(\zeta)\,d\zeta
=\pi\left(r^2-\sum_{n\ge1}n|b_n|^2r^{-2n}\right)\ge0.
\]
Letting \(r\downarrow1\) gives \(\sum n|b_n|^2\le1\). The analogous coefficients \(c_n\) for \(g\) have the same bound. Thus
\[
\sum_{n\ge1}n|b_n-c_n|^2
\le2\sum_{n\ge1}n(|b_n|^2+|c_n|^2)\le4.
\]
The reciprocal difference is not identically zero, since otherwise \(f=g\). Finally, multiplication by \(z\) preserves \(\mathcal D\): its seminorm becomes
\(\sum_{n\ge0}(n+1)|d_n|^2\), which is finite because \(d_0\) is finite and \(n+1\le2n\) for \(n\ge1\). This proves the proposition. □

In particular, every uniqueness set for \(\mathcal D\) is a uniqueness set for \(S\). Since \(\mathcal D\subset H^2\), Jensen's formula yields
\[
\sum_{a\in Z\setminus\{0\}}(1-|a|)<\infty
\tag{1}
\]
for a non-uniqueness set. For completeness, remove the finite-order zero at 0 from a nonzero Dirichlet function. Its Hardy square means remain bounded; Jensen and the arithmetic-geometric mean inequality bound the sums \(\sum_{|a|<r}\log(r/|a|)\) uniformly as \(r\uparrow1\). Monotone convergence and \(-\log|a|\ge1-|a|\) give (1).

**Outcome.** This is a necessary condition through a smaller zero-set class than Hardy spaces. Nothing here proves its converse. Overholt also reports, using earlier Dirichlet-space zero-set theorems, Blaschke sequences that are uniqueness sets for \(S\). That reported conclusion explains why (1) alone cannot be promoted to a general characterization; those earlier existence proofs are not reconstructed or used as inputs to the constructive results below.

## 3. Attempt 2: bounded-derivative perturbations and every finite set

**Lemma 2.** Let \(H\not\equiv0\) be holomorphic in \(\mathbb D\), with \(H(0)=H'(0)=0\) and \(\|H'\|_\infty\le M<\infty\). For \(0<|\epsilon|M<1\),
\[
f(z)=z,\qquad g(z)=z+\epsilon H(z)
\]
are distinct bounded members of \(S\). Their coincidence set is exactly the zero set of \(H\).

**Proof.** The normalization is immediate. For distinct \(z,w\in\mathbb D\), integrate along their line segment, contained in the convex disk, to get
\[
|H(z)-H(w)|\le M|z-w|,
\quad |g(z)-g(w)|\ge(1-|\epsilon|M)|z-w|>0.
\]
Also \(|H(z)|\le M|z|\), so \(g\) is bounded. □

For finitely many prescribed nonzero points \(a_1,\ldots,a_N\), put
\(P(z)=z^2\prod_{j=1}^N(z-a_j)\). If \(P=\sum c_jz^j\), the explicit bound \(M=\sum j|c_j|>0\) works. Taking \(\epsilon=1/(2M)\) proves finite interpolation by a distinct pair, with no additional coincidence points other than 0.

**Outcome.** Finite point sets impose no obstruction. For infinite sets the missing object is a nonzero vanishing function with bounded derivative; arbitrary bounded Blaschke products need not have that derivative bound.

## 4. Attempt 3: a quantitative infinite-set construction

**Theorem 3.** Let \(\zeta\in\partial\mathbb D\) and let \(Z\setminus\{0\}=\{a_n\}\) be a distinct finite or infinite sequence of nonzero points satisfying
\[
E_\zeta(Z):=\sum_n(1-|a_n|^2)
\left(1+\frac{|\zeta-a_n|}{1-|a_n|}\right)^2<\infty.
\tag{2}
\]
There exist distinct bounded \(f,g\in S\) whose coincidence set is exactly \(Z\cup\{0\}\). One can take \(f(z)=z\), and \(g=z+\epsilon H\) with
\[
H(z)=z^2(1-\bar\zeta z)^2B(z),\qquad
\epsilon=\frac1{2(12+E_\zeta(Z))},
\tag{3}
\]
where \(B\) is the Blaschke product with simple zeros \(a_n\).

**Proof.** Condition (2) implies the Blaschke condition because its summand is at least \(1-|a_n|\). For clarity, the normalized factors are
\[
b_a(z)=\frac{|a|}{a}\frac{a-z}{1-\bar a z}.
\]
Writing \(a=re^{i\phi}\) shows
\[
|1-b_a(z)|\le(1-r)\frac{1+R}{1-R},\qquad |z|\le R<1.
\]
Consequently the finite products converge locally uniformly to a nonzero holomorphic product \(B\), with precisely the stated zeros and \(|B|\le1\). Differentiation of finite products gives
\[
|B_N'(z)|\le\sum_{n\le N}\frac{1-|a_n|^2}{|1-\bar a_nz|^2}.
\tag{4}
\]
Products and their derivatives converge on compact subsets.

For any \(a,z\in\mathbb D\),
\[
|1-\bar\zeta z|
\le |1-\bar a z|+|\zeta-a||z|,
\qquad |1-\bar a z|\ge1-|a|.
\]
Thus
\[
\frac{|1-\bar\zeta z|}{|1-\bar a z|}
\le1+\frac{|\zeta-a|}{1-|a|}.
\]
Multiply (4) by \(|1-\bar\zeta z|^2\), and pass to the limit, to obtain
\[
|(1-\bar\zeta z)^2B'(z)|\le E_\zeta(Z).
\]
For \(P(z)=z^2(1-\bar\zeta z)^2\), direct differentiation gives
\(|P'|\le2|z||1-\bar\zeta z|^2+2|z|^2|1-\bar\zeta z|\le12\).
Therefore \(|H'|\le12+E_\zeta(Z)\). Lemma 2 applies. Neither \(1-\bar\zeta z\) nor the nonzero part of the Blaschke product has any other zeros inside the disk. □

**Corollary 4 (one Stolz region).** Suppose
\(|\zeta-a_n|\le C(1-|a_n|)\) for some fixed finite \(C\). Then (1) is necessary and sufficient for non-uniqueness in \(S\). Indeed,
\(E_\zeta(Z)\le2(1+C)^2\sum_n(1-|a_n|)\).
This includes every radial Blaschke sequence tending to \(\zeta\).

**Finite union extension.** Assign each point \(a\) one of finitely many boundary points \(\zeta_1,\ldots,\zeta_m\), and assume the sum in (2), using the assigned point in each summand, is finite and equals \(E\). Set
\[
P(z)=z^2\prod_{j=1}^m(1-\bar\zeta_jz)^2,\qquad H=PB.
\]
For \(m\ge1\), the same computation yields
\[
\|H'\|_\infty\le(m+2)4^m+4^{m-1}E.
\]
The factors not assigned to a given zero contribute at most \(4^{m-1}\), and differentiating \(P\) gives the first term. Hence the same characterization by (1) holds within a finite union of fixed Stolz regions. Finite exceptional points can be included because they add only finitely many finite summands.

**Explicit infinite example.** Take \(a_n=1-2^{-n}\), \(n\ge1\), and \(\zeta=1\). Here the ratio in (2) equals 1 and
\[
\sum_n(1-a_n^2)=2\sum_n2^{-n}-\sum_n4^{-n}=\frac53,
\qquad E_1=\frac{20}3.
\]
Thus \(\|H'\|_\infty\le56/3\) and the concrete choice \(\epsilon=3/112\) works in (3). The infinite product construction, not a finite numerical sample, establishes all coincidence points and injectivity.

**Outcome.** This is a complete characterization only under the stated geometric restrictions. The series in (2) may diverge for general Blaschke sequences. Failure of (2) does not prove uniqueness.

## 5. Attempt 4: why a small Dirichlet perturbation is not enough

A proposed converse to Proposition 1 might start with a small \(h\in\mathcal D\) and set \(g=z/(1+zh)\), so that \(1/g-1/z=h\). Small Dirichlet norm does not preserve univalence in this construction.

For any integer \(N>1\), put
\[
h_N(z)=N^{-3/4}z^N,\qquad
q_N(z)=\frac{z}{1+N^{-3/4}z^{N+1}}.
\]
These rational functions have no pole in the disk and are normalized. Nevertheless,
\[
\|h_N\|_\infty=N^{-3/4}\longrightarrow0,
\quad \frac1\pi\int_{\mathbb D}|h_N'|^2\,dA=N^{-1/2}\longrightarrow0,
\]
while
\[
q_N'(z)=\frac{1-N^{1/4}z^{N+1}}
{(1+N^{-3/4}z^{N+1})^2}
\]
vanishes at the positive point \(r_N=N^{-1/(4(N+1))}<1\). Thus \(q_N\) is not univalent. This disproves a uniform small-norm reconstruction principle. It does **not** disprove that every suitable Dirichlet zero set might admit some other univalent pair.

**Outcome.** A converse must control injectivity, not just the area seminorm. Scaling and the area theorem alone do not supply that control.

## 6. Attempt 5: finite interpolation and compactness

Finite interpolation cannot simply be passed to a distinct limiting pair. Here is an explicit failure of that inference. For any sequence of distinct nonzero points, let \(P_N\) and \(M_N\) be the finite-set polynomial and coefficient bound in Section 3, and set
\[
g_N(z)=z+\frac{P_N(z)}{2^NM_N}.
\]
Each \(g_N\in S\) is different from the identity and agrees with it at the first \(N\) points. But \(|P_N(z)|\le M_N|z|\), so
\(\|g_N-\mathrm{id}\|_\infty\le2^{-N}\). The pairs collapse to the same function. Taking \(a_n=1/(n+2)\) makes this especially clear: every finite subset is realizable, whereas the infinite set is a uniqueness set by the identity theorem.

One can state precisely what a compactness proof would have to add. Let \(K_r=\{|z|\le r\}\). Using the classical compactness of normalized univalent functions, non-uniqueness is equivalent to the existence of \(0<r<1\) and \(\eta>0\) such that for every \(N\) there are \(f_N,g_N\in S\) agreeing at the first \(N\) points and satisfying
\[
\max_{K_r}|f_N-g_N|\ge\eta.
\tag{5}
\]
Necessity follows by using a fixed distinct pair. For sufficiency, extract a locally uniformly convergent subsequence of both families. The limits remain in \(S\), agree at every prescribed point, and retain (5) by uniform convergence on \(K_r\). The classical compactness input follows from Koebe's bound \(|f(z)|\le|z|/(1-|z|)^2\), Montel's theorem, and the injective-or-constant limit theorem; the derivative normalization excludes a constant limit.

This exact reformulation still quantifies over \(S\) and supplies no independent test on the sequence. It is not offered as the requested characterization.

## 7. Precise remaining gap

The full question remains unresolved here. A non-uniqueness set must be contained in the zeros of a nonzero Dirichlet function. The construction above realizes sets satisfying a quantitative boundary-damping condition and hence all Blaschke sets in finitely many fixed Stolz regions. For arbitrary Dirichlet zero sets, no argument here constructs a distinct normalized univalent pair, and no argument here characterizes which ones admit such a pair. Neither failure of the weighted series, the small-norm counterexample, nor finite interpolation settles that gap.

## References

- W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory*, Problem and Update 6.83, printed p. 146, [arXiv:1809.07200](https://arxiv.org/abs/1809.07200).
- M. Overholt, *Sets of Uniqueness for Univalent Functions*, Canadian Mathematical Bulletin **43** (2000), 105–107, [DOI:10.4153/CMB-2000-016-x](https://doi.org/10.4153/CMB-2000-016-x). Section 2 credits its core reduction; the other constructions are given with complete proofs.
- P. Lappan, *Points where univalent functions may coincide*, Complex Variables **5** (1985), 17–20, [DOI:10.1080/17476938508814124](https://doi.org/10.1080/17476938508814124). Related prior work, not an invoked theorem dependency.
