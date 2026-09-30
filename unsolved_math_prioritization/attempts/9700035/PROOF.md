# SIRSN spanning length: the interior law and a sufficient excursion-tail condition

**Status: scoped partial result; the asymptotic under the original axioms alone remains unresolved. Independent review pending.**
AI-assisted and unrefereed. No historical-priority claim is made.

Target: 9700035 / AMR-096-0035, Aldous's Open Problem 35 in the 2012 version and Open Problem 9 in the published 2014 paper.

## 1. Correct functional and conclusions

A spanning subnetwork is the **union of all prescribed pairwise routes**,

\[
 \operatorname{span}(z_1,\ldots,z_m)=\bigcup_{i<j}R(z_i,z_j).
\]

It is not a minimal Steiner network. The routes may leave the sampling square; their full length, including these excursions, is the target functional.

Use the planar SIRSN axioms in Aldous [1, Section 2.2]. Write

\[
 D=\operatorname{len}R(0,(1,0)),\qquad \Delta=\mathbb E D<\infty.
\]

For an independent planar Poisson process \(\Xi_\lambda\) of intensity \(\lambda\), let \(S(\lambda)\) be the union of routes between all its points. The constant in the question is

\[
 \ell=\operatorname{intensity}(S(1)),\qquad
 \mathbb E\operatorname{len}(S(\lambda)\cap A)
 =\ell\sqrt\lambda\,|A|.
 \tag{1}
\]

For \(r>0\), the subnetwork \(E(\lambda,r)\) is the union of portions of these routes at Euclidean distance at least \(r\) from **both** endpoints. The major-road axiom and scale invariance give

\[
 p(\lambda,r)=\operatorname{intensity}E(\lambda,r)
 \le\frac{p}{r},\qquad p=p(1)<\infty.
 \tag{2}
\]

These are [1, equations (2.16)–(2.22), (6.1)–(6.2)]. The auxiliary quantity \(p\) is not \(\ell\). Also \(\ell>0\): otherwise (1) would force the sampled network to have zero length in every bounded square, contradicting a route between distinct Poisson points.

Let \(Q_n=[-n/2,n/2]^2\) and let \(Z_1,\ldots,Z_k\) be independent uniform points in \(Q_{\sqrt k}\), independent of the route process. Put \(B_k=\operatorname{span}(Z_1,\ldots,Z_k)\).

**Theorem.**

1. Under the usual SIRSN axioms,
   \[
    \mathbb E\operatorname{len}(B_k\cap Q_{\sqrt k})\sim\ell k,
    \qquad
    \liminf_{k\to\infty}\frac{\mathbb E\operatorname{len}(B_k)}k\ge\ell.
    \tag{3}
   \]
2. If, in addition,
   \[
    t^4\mathbb P(D>t)\longrightarrow0,
    \tag{4}
   \]
   then the full, untruncated conclusion holds:
   \[
    \mathbb E\operatorname{len}(B_k)\sim\ell k.
    \tag{5}
   \]
   In particular, \(\mathbb E D^4<\infty\) is sufficient.

The additional condition (4) is not asserted to follow from the SIRSN axioms. Statement (3) concerns only the part inside the sampling square and is not a resolution of the full question.

## 2. Poisson interior approximation

Fix \(\lambda>0\), and write

\[
 T_{\lambda,n}=\operatorname{span}(\Xi_\lambda\cap Q_n),\qquad
 I_{\lambda,n}=\operatorname{len}(T_{\lambda,n}\cap Q_n).
\]

The span of zero or one point has length zero. Coupling all finite subsets with the full sampled network gives \(T_{\lambda,n}\subset S(\lambda)\). Hence

\[
 \mathbb E I_{\lambda,n}\le\ell\sqrt\lambda\,n^2.
 \tag{6}
\]

For the converse, let \(C=[-1/2,1/2]^2\), and for \(r\ge1\) set

\[
 a_\lambda(r)=\mathbb E\operatorname{len}
 \bigl(\operatorname{span}(\Xi_\lambda\cap Q_r)\cap C\bigr).
\]

As \(r\uparrow\infty\), these networks increase to \(S(\lambda)\) inside \(C\): every pair of Poisson endpoints is eventually included. Monotone convergence and (1) give

\[
 a_\lambda(r)\uparrow\ell\sqrt\lambda.
 \tag{7}
\]

Tile the plane by integer translates of \(C\). For every tile \(a+C\) whose concentric translated square \(a+Q_r\) lies in \(Q_n\), the length of \(T_{\lambda,n}\) in that tile is at least the corresponding locally generated length. There are \(n^2+O_r(n)\) such tiles. Translation invariance thus gives

\[
 \liminf_{n\to\infty}n^{-2}\mathbb E I_{\lambda,n}\ge a_\lambda(r).
\]

Fixed tile boundaries have expected length measure zero by (1), so summing over them causes no double-counting issue. Let \(r\to\infty\), then combine with (6):

\[
 \frac{\mathbb E I_{\lambda,n}}{n^2}\longrightarrow\ell\sqrt\lambda.
 \tag{8}
\]

No mixing, ergodicity, finite-range dependence, or confinement of routes to \(Q_n\) was used.

## 3. Binomial de-Poissonization of the interior law

For fixed \(n\), couple independent uniform points \(U_1,U_2,\ldots\) in \(Q_n\) and define

\[
 F_m(n)=\operatorname{len}(\operatorname{span}(U_1,\ldots,U_m)\cap Q_n).
\]

This is nondecreasing in \(m\). Translation, rotation and scaling invariance imply, for deterministic endpoints \(x,y\),

\[
 \mathbb E\operatorname{len}R(x,y)=\Delta|x-y|.
\]

The union bound on length consequently gives the uniform polynomial estimate

\[
 \mathbb E F_m(n)\le\mathbb E\operatorname{len}
 \operatorname{span}(U_1,\ldots,U_m)
 \le \sqrt2\,n\Delta {m\choose2}.
 \tag{9}
\]

Put \(n=\sqrt k\). For fixed \(\varepsilon\in(0,1)\), let \(N_\pm\) be independent of the points and routes, with Poisson means \((1\pm\varepsilon)k\). Conditional uniformity of Poisson points identifies \(F_{N_\pm}(n)\) with \(I_{1\pm\varepsilon,n}\) in distribution.

Monotonicity and independence of \(N_+\) from \(F_k(n)\) imply

\[
 \mathbb E F_k(n)\le
 \frac{\mathbb E F_{N_+}(n)}{\mathbb P(N_+\ge k)}.
 \tag{10}
\]

For the other direction,

\[
 \mathbb E F_{N_-}(n)
 \le\mathbb E F_k(n)
 +\frac{\sqrt2\,n\Delta}{2}
   \mathbb E[N_-(N_--1)\mathbf1_{\{N_->k\}}].
 \tag{11}
\]

For fixed \(\varepsilon\), the last expectation is a polynomial in \(k\) times an exponentially small bound. For example, with \(\mu=(1-\varepsilon)k\), the Poisson identity

\[
 \mathbb E[N_-(N_--1)\mathbf1_{\{N_->k\}}]
 =\mu^2\mathbb P\{\operatorname{Pois}(\mu)>k-2\}
 \tag{12}
\]

and the exponential Markov inequality give this immediately. Also \(\mathbb P(N_+\ge k)\to1\). Equations (8)–(11), followed by \(\varepsilon\downarrow0\), prove the interior assertion in (3). The full-length lower bound follows by inclusion.

## 4. The exterior estimate: nearby and very long excursions

For \(r\ge0\), let

\[
 Q_n^r=[-n/2-r,n/2+r]^2,
 \qquad h(t)=\mathbb E[D\mathbf1_{\{D\ge t\}}].
\]

Fix \(R\ge1\). The first exterior strip has expected length at most

\[
 \mathbb E\operatorname{len}(T_{\lambda,n}\cap(Q_n^1\setminus Q_n))
 \le\ell\sqrt\lambda(4n+4).
 \tag{13}
\]

For a dyadic \(r=2^j\), a route element in \(Q_n^{2r}\setminus Q_n^r\), with both endpoints in \(Q_n\), is at Euclidean distance at least \(r\) from each endpoint. It therefore lies in \(E(\lambda,r)\). The annular area is

\[
 |Q_n^{2r}\setminus Q_n^r|=(n+4r)^2-(n+2r)^2=4nr+12r^2.
\]

By (2), its expected length is at most \(p(4n+12r)\). For \(J=\lfloor\log_2 R\rfloor\), the first strip and the annuli with \(0\le j\le J\) cover \(Q_n^R\setminus Q_n\). Since \(\sum_{j=0}^J2^j\le2R\),

\[
 \mathbb E\operatorname{len}(T_{\lambda,n}\cap(Q_n^R\setminus Q_n))
 \le \ell\sqrt\lambda(4n+4)
    +4pn(1+\log_2 R)+24pR.
 \tag{14}
\]

This estimate deliberately stops at \(R\); summing these annuli to infinity would give a divergent bound.

If a route with both endpoints in \(Q_n\) visits the complement of \(Q_n^R\), its total length is at least \(2R\): each endpoint is at least distance \(R\) from that visited point. Its contribution outside \(Q_n^R\) is therefore bounded by \(L\mathbf1_{\{L\ge2R\}}\), where \(L\) is the route's full length. Given the endpoints, \(L\) has the law \(|x-y|D\), and \(|x-y|\le\sqrt2 n\). Thus its expected contribution is at most

\[
 \sqrt2 n\,h(\sqrt2 R/n).
\]

The expected number of unordered endpoint pairs is \(\lambda^2n^4/2\). Conditioning on this finite Poisson count and then on its uniform locations, or using the elementary Poisson factorial-moment formula, proves

\[
 \mathbb E\operatorname{len}(T_{\lambda,n}\setminus Q_n^R)
 \le\frac{\lambda^2n^5}{\sqrt2}\,h(\sqrt2 R/n).
 \tag{15}
\]

No independence between different routes or between a route and other route geometry is assumed. Only independence of the sampled points from the SIRSN and linearity of expectation are used in the pair bound.

## 5. The tail condition closes the full-length estimate

Condition (4) implies

\[
 h(t)=o(t^{-3}).
 \tag{16}
\]

For completeness, the layer-cake identity gives
\(\mathbb E[D\mathbf1_{\{D>t\}}]=t\mathbb P(D>t)+\int_t^\infty\mathbb P(D>s)\,ds\).
For every \(\eta>0\), condition (4) bounds this by \((4\eta/3)t^{-3}\) for all sufficiently large \(t\). Possible atoms at the cutoff do not change the conclusion: use the strict-tail estimate at \(t/2\) to bound \(h(t)\). Finite fourth moment implies (4), since \(t^4\mathbb P(D>t)\le\mathbb E[D^4\mathbf1_{\{D>t\}}]\to0\).

In (14)–(15), first fix \(\delta>0\) and choose \(R=\delta n^2\). As \(n\to\infty\), the right side of (15), divided by \(n^2\), tends to zero by (16). The normalized limsup of (14) is at most \(24p\delta\). Letting \(\delta\downarrow0\) shows

\[
 \mathbb E\operatorname{len}(T_{\lambda,n}\setminus Q_n)=o(n^2).
 \tag{17}
\]

Together with (8), this establishes the full Poisson law

\[
 \mathbb E\operatorname{len}(T_{\lambda,n})\sim\ell\sqrt\lambda\,n^2.
 \tag{18}
\]

For binomial sampling, use the monotonicity argument (10) with full rather than in-square length, and use (18) at \(\lambda=1+\varepsilon\). It yields

\[
 \limsup_{k\to\infty}k^{-1}\mathbb E\operatorname{len}(B_k)
 \le\ell\sqrt{1+\varepsilon}.
\]

Let \(\varepsilon\downarrow0\), and combine with the unconditional lower bound (3). This proves (5).

## 6. Precise unresolved step

The ordinary axioms supply only \(\mathbb ED<\infty\). They do not, in this argument, supply (16), an equivalent adequate excursion estimate, or uniform integrability of the normalized exterior lengths. Integrating the major-road intensity estimate over all of the unbounded exterior is not legitimate as a finite bound. Replacing binomial points with a Poisson process without the estimates in Section 3 would also omit a step.

For a scalar example, a Pareto tail \(\mathbb P(D>t)=t^{-2}\), \(t\ge1\), has finite first moment but fails (4), and has \(h(t)=2/t\). This only demonstrates that the scalar first-moment assumption does not imply the tail hypothesis. It is **not** a construction of a SIRSN counterexample.

The published original itself asks which extra assumptions, if any, suffice. The theorem above supplies an explicit sufficient tail assumption. It does not settle whether any extra assumption is necessary, and therefore does not justify marking the dataset's unconditional claim solved.

## Reference

[1] D. Aldous, *Scale-invariant random spatial networks*, Electronic Journal of Probability 19 (2014), paper 15, 1–41. DOI: [10.1214/EJP.v19-2920](https://doi.org/10.1214/EJP.v19-2920). [Full published PDF](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf). Definitions: pp. 6–9; major-road scaling: p. 28; Open Problem 9: p. 38. The [2012 version](https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf) labels the target Open Problem 35 and explicitly highlights distant excursions.
