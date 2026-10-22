# Independent audit of the Baernstein counterexample verification

**Verdict: PASS.** The frozen packet gives a complete verification of an existing negative answer to Problem 5.57, catalogue 2305057 / AMR-022-5057. The construction is credited to **Oleg Ivrii, arXiv:2609.18785v1, 16 September 2026**. No blocking mathematical error was found. This verdict is a mathematical audit of the stated counterexample, not a claim of a new discovery, journal acceptance, or external peer review.

The review was completed on 3 October 2026. The five author files were read in full and left unchanged. In particular, the reviewed `COUNTEREXAMPLE_VERIFICATION.md` has SHA-256 `7b024162d4926a411d8dc5a7fddf08eee94148c4e1b10d45f99a067970e818f4`. The accompanying `independent_results.json` records the complete file-integrity check and supplementary deterministic controls.

## Source and target match

The primary-source record matches the intended problem:

- Anderson, Barth, and Brannan, *Research problems in complex analysis*, Bulletin of the London Mathematical Society 9 (1977), 129–162, Problem 5.57, printed p.138. The cached text of the [original scan](https://citeseerx.ist.psu.edu/document?doi=ea1cdeb32c106ad049da5f856f5bb77162129243&repid=rep1&type=pdf) contains the exact relevant passage and Baernstein attribution. Direct fetching of that scan was unavailable during this audit; the passage itself was available from the indexed primary source.
- Hayman and Lingham, *Research Problems in Function Theory*, [2018 arXiv edition](https://arxiv.org/pdf/1809.07200), printed pp.106–107, Problem 5.57. The relevant pages and local text were checked. The quantifiers concern a holomorphic function on the disc, almost every boundary point, angular limits, and the actual image of every Stolz angle, with a logarithmic-capacity-zero omitted set. This is not a claim about image closure or multiplicity.
- Ivrii's [versioned full text](https://arxiv.org/html/2609.18785v1) and [PDF](https://arxiv.org/pdf/2609.18785) agree on the construction and the needed conclusions. Theorem 1.1(i),(iii), Sections 2–5, and Section 7 were inspected beyond the abstract. The [submission record](https://arxiv.org/abs/2609.18785) gives 16 September 2026 and version 1; no journal acceptance is inferred.
- Gardiner and Manolaki's [Theorem 1](https://arxiv.org/pdf/2011.05874), printed pp.1–2, gives a multiplicity-weighted length conclusion. Its distinction from omitted area/capacity is correctly represented in the packet.

The audit certifies the capacity-zero dichotomy's failure. The broader request for possible improvements of Plessner's theorem is not an exhaustively classified research programme. Ivrii's separate exact-range and Hausdorff-dimension results are outside this verdict.

## The precise certified assertion

Put

\[
f_\omega(z)=\sum_{k\ge1}\frac{\xi_k(\omega)}{\sqrt{k}}z^{2^k},
\]

with independent circular complex Gaussian variables of density \(\pi^{-1}e^{-|z|^2}\). There is a probability-one set of coefficient sequences on which the following holds: there is one measurable full arc-length-measure boundary set \(E_\omega\) such that, for every \(\zeta\in E_\omega\),

\[
\liminf_{r\uparrow1}|f_\omega(r\zeta)|=0,
\qquad
\limsup_{r\uparrow1}|f_\omega(r\zeta)|=\infty,
\]

and, simultaneously for every finite \(A>1\),

\[
\frac{m\bigl(f_\omega(\Gamma_A(\zeta))\cap B(0,R)\bigr)}{\pi R^2}
\longrightarrow0,
\qquad
\Gamma_A(\zeta)=\{z\in\mathbb D:|z-\zeta|<A(1-|z|)\}.
\]

Thus one may fix a single deterministic coefficient sequence with these properties. For each good boundary point and each such cone, its complement contains a compact set of positive logarithmic capacity. The compact omitted set may depend on both the boundary point and the cone. No common omitted compact set for the entire disc or for almost every boundary point is asserted or needed.

## Coefficient bounds and cone shadowing

The coefficient event is valid because

\[
\sum_{k\ge1}\mathbb P(|\xi_k|>k^{1/4})
=\sum_{k\ge1}e^{-\sqrt{k}}<\infty.
\]

Borel–Cantelli gives a finite random constant \(M\) with \(|\xi_k|/\sqrt{k}\le M k^{-1/4}\) for all \(k\), after absorbing the finitely many initial coefficients. For each \(\rho<1\), the majorant \(M\sum_k\rho^{2^k}\) is finite, giving compact absolute and uniform convergence and holomorphy.

Let \(\zeta=e^{i\theta}\) and \(S_n(\theta)=\sum_{k\le n}(\xi_k/\sqrt{k})e^{i2^k\theta}\). For
\(2^{-n-1}<1-|z|\le2^{-n}\) and \(z\in\Gamma_A(\zeta)\), the factorization of a difference of powers gives

\[
|z^{2^k}-\zeta^{2^k}|\le2^k|z-\zeta|\le A2^{k-n}
\quad(k\le n),
\]

and \((1-u)^q\le e^{-qu}\) gives

\[
|z|^{2^k}\le e^{-2^{k-n-1}}\quad(k>n).
\]

There is no missing angular error: the first inequality directly handles both modulus and argument. The sums obey

\[
\sum_{k\le n}k^{-1/4}2^{k-n}
\le 2\,2^{-n/2}+2(n/2)^{-1/4}=O(n^{-1/4}),
\]

and

\[
\sum_{k>n}k^{-1/4}e^{-2^{k-n-1}}
\le n^{-1/4}\sum_{j\ge1}e^{-2^{j-1}}=O(n^{-1/4}).
\]

Consequently the stated shadowing estimate is uniform in \(\theta\) and in the point of each annular cone piece. The constant depends only on \(M\) and \(A\). The central portion and any finite number of annular pieces lie in a closed subdisc of radius less than one, so their image is bounded. This deals with the omitted \(n=0\) piece as well as all later finite initial pieces.

**Result: PASS.** The error decay is sufficient, and there is no unjustified uniformity in the coefficient or cone parameters.

## Independent verification of the occupation bound

Normalize planar Brownian motion by \(\mathbb E|B_t|^2=t\), so its transition density is
\(p_t(x)=(\pi t)^{-1}e^{-|x|^2/t}\). Fix \(0<\varepsilon<1\), and write

\[
K_\varepsilon=\{x:\min_{0\le t\le1}|B_t-x|\le\varepsilon\}.
\]

For each fixed \(x\), define the closed-disc hitting time
\(\tau_x=\inf\{t\ge0:|B_t-x|\le\varepsilon\}\). Continuity and adaptedness make this a stopping time. The event \(\{\tau_x\le1\}\) belongs to \(\mathcal F_{\tau_x}\). On that event the stopping location lies within distance \(\varepsilon\) of \(x\), including when \(\tau_x=0\).

For any such location \(y\), \(\varepsilon^2\le s\le1\), and \(u\in B(x,\varepsilon)\),
\(|u-y|\le2\varepsilon\) and therefore

\[
\mathbb P_y(B_s\in B(x,\varepsilon))
\ge \pi\varepsilon^2(\pi s)^{-1}e^{-4}
=e^{-4}\varepsilon^2/s.
\]

For complete stopping-time bookkeeping, introduce
\(T_x=\int_0^2\mathbf1_{\{|B_t-x|<\varepsilon\}}\,dt\). Pathwise on \(\{\tau_x\le1\}\), its defining interval contains all \(\tau_x+s\) with \(\varepsilon^2\le s\le1\). Thus the strong Markov property and nonnegative integration give

\[
\mathbb E T_x
\ge \mathbb E\left[\mathbf1_{\{\tau_x\le1\}}
\int_{\varepsilon^2}^1
\mathbb P_{B_{\tau_x}}(B_s\in B(x,\varepsilon))\,ds\right]
\ge 2e^{-4}\varepsilon^2\log(1/\varepsilon)
\mathbb P(\tau_x\le1).
\]

This is an unconditional inequality; it does not improperly condition Brownian increments on the hitting event. The random interval lies in \([0,2]\) precisely because hitting was required by time 1.

Tonelli applies without an integrability assumption because all integrands are nonnegative. For each path and time, integration over disc centres gives exactly \(\pi\varepsilon^2\). Hence

\[
\int_{\mathbb C}\mathbb E T_x\,dm(x)=2\pi\varepsilon^2.
\]

Also \(x\in K_\varepsilon\) if and only if \(\tau_x\le1\), so
\(\int\mathbb P(\tau_x\le1)dm(x)=\mathbb E m(K_\varepsilon)\). The event is jointly measurable in path and \(x\): the minimum-distance functional on the continuous path over a compact interval is continuous. Division now yields exactly

\[
\boxed{\mathbb E m(K_\varepsilon)\le
\frac{\pi e^4}{\log(1/\varepsilon)}}.
\]

Using an open occupation disc with a closed hitting disc causes no issue: the heat-kernel lower bound is valid even for a starting point on the circle. This proof requires neither point-hitting recurrence nor a sharp Wiener-sausage asymptotic. Its nonsharp constant is harmless.

**Result: PASS.** The replacement estimate is rigorous with the displayed normalization and constant.

## Shrinking neighbourhoods and almost sure density

For fixed \(\gamma>0\), the unit-time slice of
\(W_\gamma=\bigcup_{t\ge0}B(B_t,e^{-\gamma t})\) is contained in \(B_n+K_n\), where \(K_n\) is the closed \(e^{-\gamma n}\)-neighbourhood of the increment path on \([n,n+1]\). Independence of the future increment process from \(\mathcal F_n\) makes \(K_n\) independent of \(B_n\). No independence between distinct sausages is needed.

The occupation bound gives \(\mathbb E m(K_n)\le C_\gamma/n\) for \(n\ge1\). Conditioning on \(K_n\), or applying Tonelli to its membership indicator, gives

\[
\mathbb E m((B_n+K_n)\cap B(0,R))
=\int\mathbb P(u\in K_n)\,
\mathbb P(B_n\in B(0,R)-u)\,dm(u).
\]

Since \(p_n\le1/(\pi n)\), the second factor is bounded by \(\min(1,R^2/n)\). Summation yields

\[
\mathbb E m(W_\gamma\cap B(0,R))
\le C_\gamma'\bigl(1+\log(R+1)\bigr),\qquad R\ge1.
\]

For the omitted initial slice, \(K_0\) lies in a disc of radius \(1+\sup_{t\le1}|B_t|\); the reflection-principle tail bound makes the expected square of this radius finite. For the remaining terms, split at \(N=\lfloor R^2\rfloor\): the first sum is harmonic, while \(R^2\sum_{n>N}n^{-2}\) is uniformly bounded because \(R^2/N<2\).

Let \(X_j=m(W_\gamma\cap B(0,2^j))/(\pi4^j)\). Then
\(\sum_j\mathbb E X_j<\infty\), as \(\sum_{j\ge0}(j+1)/4^j=16/9\). Tonelli gives a finite nonnegative sum \(\sum_jX_j\) almost surely, and hence \(X_j\to0\). It is not merely convergence in expectation. For \(2^j\le R<2^{j+1}\), the normalized area at \(R\) is at most \(4X_{j+1}\). Thus the limit holds for all real radii.

The uncountable union defining \(W_\gamma\) is measurable without an extra assumption: continuity of the path and strict membership in its open discs allow the union to be restricted to nonnegative rational times. Closed neighbourhoods used for the upper bound are likewise measurable.

**Result: PASS.** All conditioning, infinite summation, and almost-sure limiting steps are justified.

## Brownian sampling and the common boundary set

For any fixed \(\theta\), multiplying each Gaussian coefficient by \(e^{i2^k\theta}\) preserves its distribution and independence. Thus the entire sequence \((S_n(\theta))\), not just its one-dimensional marginals, has the same law as \((B_{H_n})\), where \(H_n=\sum_{k\le n}1/k\). This is all the proof needs; it never constructs simultaneously independent Brownian motions for uncountably many angles.

One can take the absolute lower index in the packet to be \(N_0=3\). Indeed

\[
H_n\le1+\log n\le2\log n\quad(n\ge3),
\qquad
n^{-1/8}\le e^{-H_n/16}.
\]

For each fixed angle the union
\(U_\theta=\bigcup_{n\ge3}B(S_n(\theta),n^{-1/8})\) therefore has density zero almost surely by sequence-law equality and its Brownian realization inside \(W_{1/16}\).

The needed Fubini event is measurable in \((\theta,\omega)\). Explicitly,

\[
\mathbf1_{\{w\in U_\theta(\omega)\}}
=\mathbf1_{\{\exists n\ge3:|w-S_n(\theta,\omega)|<n^{-1/8}\}}
\]

is measurable in \((\theta,\omega,w)\), since each partial sum is a finite jointly measurable function. Integrating this indicator over a fixed dyadic disc gives a measurable area functional. The condition that these normalized areas tend to zero is a countable limit condition. Fubini now gives one probability-one coefficient event on which almost every angle is good.

For coefficients in that event and the coefficient-bound event, fix any good angle. For any \(A>1\), choose an integer \(N\) exceeding \(3\) and \(C_A^8\). Then
\(C_A n^{-1/4}<n^{-1/8}\) for \(n\ge N\). The cone tail image is contained in the same \(U_\theta\), and the initial image is bounded. The angle was chosen before \(A\); the good-angle event and \(U_\theta\) have no aperture dependence. This proves the simultaneous every-cone assertion without intersecting uncountably many probability-one events.

**Result: PASS.** The quantifiers have the strength needed by the original question.

## Radial oscillation and the angular-limit alternative

Planar Brownian recurrence and unboundedness give arbitrarily late approaches to the origin and arbitrarily large moduli. The sampling argument is essential, because recurrence of a continuous process alone does not automatically imply recurrence on a prescribed time sequence.

Here the gaps are \(H_{n+1}-H_n=1/(n+1)\). For the normalized Brownian motion, the reflection principle in each coordinate and a union bound yield

\[
\mathbb P\left(\sup_{0\le s\le t}|B_s|>r\right)
\le4e^{-r^2/(2t)}.
\]

Hence the probability that the oscillation on \([H_n,H_{n+1}]\) exceeds \(n^{-1/3}\) is at most
\(4\exp[-(n+1)/(2n^{2/3})]\). Its sum is finite, so Borel–Cantelli shows that the between-sample errors tend to zero. Both Brownian modulus conclusions survive sampling. Independence between these oscillation events is not required.

Sequence-law equality and a second Fubini argument transfer the two measurable sequence-limit properties to almost every angle for almost every coefficient sequence. At \(r_n=1-2^{-n}\), radial points belong to any fixed \(\Gamma_A\) with \(A>1\); shadowing gives
\(|f(r_ne^{i\theta})-S_n(\theta)|\to0\). The lower limit for the full radial parameter is zero because the modulus is nonnegative and has a subsequence tending to zero. Its upper limit is infinite because another subsequence is unbounded.

These two limits exclude both finite and infinite angular limits. Intersecting the coefficient events and the corresponding full-measure angle sets is legitimate. After fixing the function, classical Plessner gives a further full-measure boundary set of Plessner points. The negative answer itself already follows from the failure of the angular-limit alternative and the omitted-capacity alternative, so no new strengthening of classical Plessner is presupposed.

**Result: PASS.** The radial and angular assertions follow with a single deterministic function.

## Omitted values and logarithmic capacity

Fix a good point and a cone, and write \(V=f(\Gamma_A(\zeta))\). The function is nonconstant by its radial oscillation, and the cone is open, so the open mapping theorem makes \(V\) open. For sufficiently large \(R\), density zero gives

\[
K=\overline{B(0,R)}\setminus V,
\qquad 0<m(K)<\infty.
\]

The set is compact. With \(a=m(K)\) and \(d\mu=a^{-1}\mathbf1_K\,dm\), the positive part of logarithmic energy satisfies

\[
\iint\log^+\!\frac1{|x-y|}\,d\mu(x)d\mu(y)
\le \frac1a\int_{|u|<1}\log\frac1{|u|}\,dm(u)
=\frac{\pi}{2a}.
\]

The negative part is bounded by \(\log^+(2R)\). In particular the diagonal singularity causes no infinite energy: the area measure has no atoms and the displayed local kernel is integrable. Thus \(I(\mu)\) is finite. The energy definition gives
\(\operatorname{cap}(K)=\exp[-\inf_\nu I(\nu)]>0\). For bounded \(K\), the energy is also bounded below, so there is no hidden indeterminate expression. Monotonicity transfers positivity to \(\mathbb C\setminus V\), regardless of which standard extension of capacity to unbounded sets is used.

An ordinary open Stolz triangle lies in some \(\Gamma_A\) near its vertex; its remainder has closure compactly contained in the disc. The image of the first part is sparse at infinity, and the second image is bounded. Its image therefore has density zero as well. Alternatively, a fixed small symmetric triangle inside one cone already suffices to refute the claimed every-Stolz-angle conclusion. Truncation only makes the image smaller and its complement larger.

This argument concerns actual omitted values. Dense image is fully compatible with density zero and a positive-area closed complement with empty interior. Infinite area counted with multiplicity also presents no contradiction.

**Result: PASS.** The capacity conclusion has the correct direction, compactness, and quantifiers.

## Adversarial checks and final disposition

The following potential failure points were explicitly tested:

1. The coefficient bound holds on one coefficient event, uniformly in angle.
2. Brownian normalization is consistent between Gaussian increments, the heat kernel, and the reflection bound.
3. The stopping-time event is measurable at the stopping time, and the whole post-hit integration interval stays within the occupation window.
4. Nonnegative Tonelli justifies both centre integration and the infinite expected-area sum.
5. The translated random increment neighbourhood is independent of its starting point; different slices need not be independent.
6. Almost-sure density follows from summability on dyadic radii, not from expectation convergence alone.
7. A countable union of random discs gives a measurable angle/coefficient event.
8. One good-angle set works for every cone aperture; no uncountable intersection is hidden.
9. Sampling Brownian recurrence is justified by a summable maximal-displacement estimate.
10. Bounded initial images do not affect density at infinity.
11. Positive area yields finite logarithmic energy and positive capacity for a compact subset of each omitted set.
12. The negative result is attributed to the September 2026 preprint, with no new-resolution or journal-status claim.

The supplied deterministic script verifies the frozen file set and hashes and checks the radius comparison and low-frequency sum through index 100,000. These finite controls are regression checks only; the analytic arguments above establish the infinite statements. No random numerical sample is used as an existence certificate.

There are **no required mathematical amendments** to the frozen author packet. It is suitable to identify this target as an **existing, attributed negative resolution verified from the preprint**. The same construction also refutes the weaker area-zero proposal, but this audit does not authorize changes to another catalogue record. No publication or remote modification was performed by this review.
