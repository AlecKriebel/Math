# Random projections of the cube: already solved in published work

**Both parts of OWR-17469-011 were resolved by Johnston, Kabluchko and Prochno, published online in 2021 and in Studia Mathematica in 2022. This is a source-status correction, not our discovery.** Separate adversarial AI review of this identification passed; see [the report](review/REVIEW.md).

## Exact question and normalization

The complete [original report](https://publications.mfo.de/bitstream/handle/mfo/3713/OWR_2020_06.pdf?isAllowed=y&sequence=4), pp.411–413, concerns a **one-dimensional** projection of the uniform law on the growing cube \([-1,1]^N\). Write
\[
\mu_\theta=\operatorname{Law}\left(\sum_{i=1}^N\theta_iU_i\right),
\qquad \theta\in S^{N-1},\quad U_i\stackrel{\mathrm{iid}}\sim\operatorname{Unif}[-1,1].
\]
For a Haar-uniform direction \(\Theta^{(N)}\), the object undergoing deviations is the **random probability measure** \(\nu_N=\mu_{\Theta^{(N)}}\). For \(\alpha\in\ell_2\), \(\|\alpha\|_2\le1\), define
\[
\kappa_\alpha=\operatorname{Law}\left(
\sum_{i\ge1}\alpha_iU_i+
\sqrt{\frac{1-\|\alpha\|_2^2}{3}}\,Z\right),
\tag{1}
\]
where \(Z\sim N(0,1)\) is independent of the uniforms. The series converges in \(L^2\) and almost surely. Its total variance is **1/3**.

## Published resolution of the large-deviation claim

S. G. G. Johnston, Z. Kabluchko and J. Prochno, *Projections of the uniform distribution on the cube: a large deviation perspective*, **Studia Mathematica 264 (2022), 103–119**, DOI [10.4064/sm210413-16-9](https://doi.org/10.4064/sm210413-16-9). The [publisher record](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/online/114493/projections-of-the-uniform-distribution-on-the-cube-a-large-deviation-perspective) gives the online date as 17 December 2021. A complete [author manuscript, arXiv v2](https://arxiv.org/abs/2103.16430v2), is openly available.

**Theorem A** states the full LDP for \((\nu_N)\) on \(\mathcal P(\mathbb R)\) with its weak topology, at speed \(N\), with good rate
\[
I(\nu)=
\begin{cases}
-\frac12\log(1-\|\alpha\|_2^2),&\nu=\kappa_\alpha,\ \|\alpha\|_2<1,\\
+\infty,&\text{otherwise}.
\end{cases}
\tag{2}
\]
This is exactly the report's Conjecture 1. There is no extra tail assumption or growing projection-dimension hypothesis.

The paper uses nonnegative decreasing coefficients. This does not restrict (1): independent symmetric uniforms allow arbitrary signs to be removed and coefficients to be reordered without changing the law or squared norm. Square summability makes these rearrangements legitimate in \(L^2\).

## The intermediate limit set is also covered

Put
\[
W=\{a_1\ge a_2\ge\cdots\ge0:\ \sum_i a_i^2\le1\}.
\]
**Proposition 3.1** of the same paper proves that \(a\mapsto\kappa_a\) is a homeomorphism from \(W\), with coordinatewise convergence, to its image \(K\subset\mathcal P(\mathbb R)\). In particular, \(K\) is compact. The following explains explicitly how that proposition yields the report's Lemma 1, including attainability of every proposed limit.

Every law in \(E_N\) belongs to \(K\): sort the absolute values of its unit-vector coefficients and pad by zeros. Hence any weak limit of a sequence chosen from the \(E_N\) lies in the closed set \(K\).

Conversely fix \(a\in W\). For \(N\ge2\), take \(m_N=\lfloor\sqrt N\rfloor<N\), retain \(a_1,\ldots,a_{m_N}\), and fill the remaining \(N-m_N\) positions with
\[
c_N=\sqrt{\frac{1-\sum_{i=1}^{m_N}a_i^2}{N-m_N}}.
\tag{3}
\]
The resulting vector has squared norm one, so its projection law belongs to \(E_N\). Moreover \(c_N\to0\). After decreasing rearrangement and zero padding, the vector converges coordinatewise to \(a\): any fixed positive coordinate eventually exceeds every filler; when a fixed target coordinate is zero, only finitely many target entries are positive and the fillers tend to zero. Proposition 3.1 now gives convergence of the laws to \(\kappa_a\). The first, irrelevant, term \(N=1\) can be chosen arbitrarily in \(E_1\).

Weak convergence of probabilities on \(\mathbb R\) is equivalent to convergence in the Prohorov metric. Thus the requested set of all possible Prohorov limits is exactly \(K\), including coefficients of norm one. Those boundary laws have infinite rate in (2); they must not be deleted from the limit set.

## Scope and technical checks

- Probability in the LDP is over the random **direction**. This is not a quenched scalar-projection LDP or an LDP for the direction-averaged scalar law.
- The projection dimension is fixed at one; the ambient dimension is \(N\). No coupling or independence between directions of different dimensions is needed for the marginal LDP.
- At \(a=0\), the law is \(N(0,1/3)\) and the rate is zero. Norm-one coefficient vectors give infinite rate, and measures outside \(K\) do as well.
- The manuscript's isolated sentence after equation (2) says variance one. Its formula, Theorem A, and the publisher abstract all give variance **1/3**. Our normalization uses the formula and verifies it directly; no theorem is altered.
- Coordinatewise convergence is essential: the vectors with \(N\) entries \(1/\sqrt N\) have norm one and converge coordinatewise to zero. The limiting missing coefficient mass is represented by the Gaussian term in (1).

The existence and exact statement of the published theorem settle the original target. The coefficient construction above only makes the intermediate implication explicit; it is not claimed as new research. The appropriate status is **already_solved**, subject to the separate source-match review required for this workflow.
