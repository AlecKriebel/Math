# Audit of Ho's lacunary partial sum counterexample

## Conclusion and scope

**Accept the source-scoped conclusion of Theorem 1.6 in Boon Suan Ho, _Counterexamples for lacunary dilates via dyadic spike blocks_, arXiv:2604.18535v2, 21 April 2026.** The dependency chain needed for this theorem is mathematically sound. No obstruction remains in that chain after checking the block estimates, digit-window independence, common exceptional set, shielding of all other blocks, and the recursive choice of parameters.

For each fixed real $p$ with $2\le p<\infty$, the construction gives a deterministic increasing integer sequence $n_j=2^{m_j}$, with $n_{j+1}/n_j\ge2$, and a real mean-zero $f\in L^p(\mathbb T)$, such that on one set of full Lebesgue measure,

$$
\limsup_{N\to\infty}
\frac{\sum_{j\le N}f(n_jx)}{N(\log N)^{1/p-\varepsilon}}
=+\infty\qquad\text{for every }\varepsilon>0.
$$

In particular, for $p=2$, the proposed general $o(N\sqrt{\log\log N})$ bound fails. The function and sequence can depend on $p$; they do not depend on $x$ or on the subsequent choice of $\varepsilon$.

This is verification of Ho's existing construction, not a novelty claim, a journal-refereeing claim, or an acceptance of every theorem in the manuscript. The exact logarithmic endpoint and optimal secondary logarithmic factors remain outside this conclusion. Sections 5, 6, and 8 are not dependencies of Theorem 1.6 and are not granted independent acceptance by this report.

## Sources and exact pins

1. Boon Suan Ho, _Counterexamples for lacunary dilates via dyadic spike blocks_, [arXiv:2604.18535v2](https://arxiv.org/abs/2604.18535v2), [versioned PDF](https://arxiv.org/pdf/2604.18535v2), 21 April 2026, 27 PDF pages. Inspected PDF: 609251 bytes; SHA-256 `f88b36a072d66476c5948061b7f2fc4d61dc536bbc5df5aa5bd3cdd2a84a82d0`. The primary abstract page was checked on 11 October 2026 and identifies v2, the author, title, date, and 27-page length. It did not supply a journal reference. Absence of a journal field is not proof of absence of any later publication.
2. Paul Erdős, _Problems and results on diophantine approximations_, Compositio Mathematica 16 (1964), 52–65, [author-archive PDF](https://users.renyi.hu/~p_erdos/1964-24.pdf). Inspected PDF: 1568391 bytes; SHA-256 `31727bb7ef68a536ee7fc68ef3a793e8b6a78f66af6f6fc5aab9c733731e78cd`. The relevant pages are printed 57–58, PDF pages 6–7.

All page numbers below for Ho are both PDF and printed page numbers. The audit used the retained PDF bytes and text extraction. The mathematical dependency pages 9–16, the theorem on page 4, and the parameter proof on pages 21–23 were additionally checked against rendered PDF pages. Erdős's printed page 58 was visually checked to resolve the exponents. No source-author code was executed.

## Original normalization and attribution

Erdős's printed page 57 assumes $n_{k+1}>(1+c)n_k$ for a fixed $c>0$, evaluates the periodic function at fractional parts, and discusses $L^2(0,1)$. Ho's ratio bound $n_{j+1}/n_j\ge2$ meets this strict condition, for example with $c=1/2$.

On printed page 58, equation (15) has denominator

$$
N(\log\log N)^{1/2-\varepsilon},
$$

and equation (16) has denominator

$$
N(\log N)^{1/2+\varepsilon}.
$$

The first describes lower examples with infinite limsup; the second is a general upper limit zero. These exponents were read from the scan, not inferred from damaged OCR. The surrounding 1964 prose discusses the gap between those scales. It does **not** literally display the modern $o(N\sqrt{\log\log N})$ question. That precise formulation appears in Ho's introduction on page 3 and in the modern problem being audited. The present report distinguishes those formulations rather than attributing an unprinted formula to the 1964 page.

The original superlinear question does not require a mean-zero assumption: subtracting an integral changes a partial sum by $O(N)$. Ho provides mean zero anyway. Fractional-part evaluation and evaluation of a periodic representative on $\mathbb T$ are the same convention.

## Dependency chain

Theorem 1.6, page 4, is proved in Section 7, pages 21–23. Its dependencies are:

- Lemma 2.1, page 8: binary-digit distribution and independence, and dyadic Fourier valuation support.
- Lemma 3.1, pages 9–10: zero mean, squared $L^2$ cost, and a deterministic lower floor. Its Fourier-tail estimates are correct but are not needed for Theorem 1.6.
- Lemma 3.2, page 10: the $L^p$ cost of a block.
- Lemma 3.3, pages 10–11: independent-series $L^p$ convergence under summable second and $p$-th moments.
- Definition 3.4 and Lemma 3.5, pages 11–12: one successful trial and its amplification.
- Stage definitions (4.1)–(4.14), pages 12–14, and Lemmas 4.1–4.2, pages 14–15: deterministic placement, term counts, and event independence.
- Proposition 4.3, pages 15–16: convergence, a common almost-everywhere representative, and the full partial-sum lower bound.
- Section 7: the budget and signal choices, summable stage failures, and the simultaneous $\varepsilon$ conclusion.

The following sections verify this chain. They also give an elementary alternative for the $L^p$ step using the paper's explicit geometric budget, so that the acceptance of Theorem 1.6 does not depend on re-auditing the original proof of Rosenthal's inequality.

## Dyadic spikes and one block

Write $\theta=2^{-d}$, $h_d=\sqrt{2^d-1}$, and $g_d=1/\sqrt{2^d-1}$. The spike is the centered and variance-normalized indicator of a dyadic interval of measure $\theta$. It has values $h_d$ and $-g_d$, mean zero, and variance one. After dilation by $2^v$, it depends exactly on binary coordinates $v+1,\ldots,v+d$. Disjoint finite collections of binary coordinates are independent under Lebesgue measure. Binary-expansion ambiguity is confined to a null set and can alternatively be avoided by retaining the half-open interval definition throughout.

For the block, put

$$
F(x)=\sqrt{\lambda/L}\sum_{q=1}^{L}\phi_d(2^{U+qD}x),
\quad
64B^2L/\lambda\le2^d<128B^2L/\lambda,
$$

where $0<\lambda\le1$, $B\ge100$, $D\ge d+2$, and the indexing and shift parameters are integers. The block's coordinate windows are disjoint, so its mean is zero and $\|F\|_2^2=\lambda$.

The pointwise lower floor follows directly, with ample constant slack:

$$
F\ge-\sqrt{\lambda L}\,g_d,
\qquad
\sqrt{\lambda L}\,g_d
\le\sqrt{2\lambda L/2^d}
\le\frac{\lambda}{4\sqrt2 B}.
$$

Thus the unspecified absolute constant $C_3$ can safely be taken to be 1. This lower floor is uniform in $L,d,D,U$. Its independence from the size of the stage is essential and is correctly obtained.

For completeness, the Fourier-support argument is also valid. The nonzero coefficient of the interval indicator is proportional to $(1-e^{-2\pi i r2^{-d}})/r$, so it vanishes if $2^d\mid r$. Dilating by $2^v$ confines nonzero coefficients to valuations $v,\ldots,v+d-1$. The disjoint bands yield orthogonality even after a symmetric Fourier projection. The bounded-variation estimate gives squared tail $O(\min(1,2^d/R))$; summing the geometric dilation scales gives Lemma 3.1's bounds (3.6)–(3.8). No Fourier-tail fact is used later to infer Theorem 1.6.

### The block moment estimate

The manuscript applies Rosenthal's inequality to the independent centered summands. Its two terms are respectively $\lambda^{p/2}$ and $O_p(\lambda B^{p-2})$. Since $\lambda\le1$ and $B\ge1$, the first is also at most $\lambda B^{p-2}$. The exponents and normalization in Lemma 3.2 are correct for every real $2\le p<\infty$.

Here is a separate elementary verification. Let $Y$ count the spikes in the block. Then $Y$ has binomial distribution with parameters $L,\theta$, and

$$
F=A(Y-t),\qquad
t=L\theta,\qquad
A=\sqrt{\lambda/L}/\sqrt{\theta(1-\theta)}.
$$

The parameter condition gives

$$
0<t\le\lambda/(64B^2)\le1,
\qquad A^2<256B^2.
$$

For an integer $r\ge1$, $\Pr(Y=r)\le t^r/r!$. Consequently, for every fixed finite real $p\ge2$,

$$
\mathbb E Y^p\le\sum_{r\ge1}\frac{r^pt^r}{r!}
\le t\sum_{r\ge1}\frac{r^p}{r!}=C_p t.
$$

The last series converges by the ratio test. Since $t^p\le t$, the elementary inequality $ |a-b|^p\le2^{p-1}(|a|^p+|b|^p)$ now yields

$$
\mathbb E|F|^p
\le C_p B^p t
\le C_p\lambda B^{p-2}.
$$

This verifies the claimed uniform estimate without an unexamined cancellation assumption or an integer-$p$ restriction.

## Lemma 3.3 and convergence of the function

Lemma 3.3 is a correct application of the standard finite-sum Rosenthal inequality for independent centered real random variables:

$$
\left\|\sum_{k=m}^{n}G_k\right\|_p^p
\le C_p\left[
\left(\sum_{k=m}^{n}\|G_k\|_2^2\right)^{p/2}
+\sum_{k=m}^{n}\|G_k\|_p^p\right].
$$

Both sums on the right have uniformly vanishing tails under the stated hypotheses; hence the partial sums are Cauchy in $L^p$. For $p=2$, independence and zero means imply orthogonality, so the Hilbert-space argument applies. Summability of $p$-th moments alone, without independence or some other condition, would not justify the lemma, but no such inference is made.

The required independence across blocks really holds. The last digit used by $F_{k-1}$ is $V_{k-1}^{\max}+1$. The first digit used by $F_k$ is

$$
U_k+D_k+1=V_{k-1}^{\max}+D_k+2,
$$

strictly later. Earlier blocks end no later than $F_{k-1}$. Thus the collections of digits for the blocks are disjoint. Orthogonality, or the direct digit independence, gives $L^2$ convergence when $\sum\lambda_k<\infty$. The independent mean-zero summable-variance convergence theorem used for almost-everywhere convergence is applicable.

Two elementary redundant checks remove possible dependence on those convergence citations for the particular theorem:

1. The source explicitly permits $a_k=2^{-k-2}$. With $\lambda_kB_k^{p-2}=a_k$, the block bound gives
   $$
   \sum_k\|F_k\|_p\le C_p^{1/p}\sum_k2^{-(k+2)/p}<\infty.
   $$
   Minkowski and completeness give $L^p$ convergence directly. This uses the explicit geometric choice, not an incorrect claim that every summable $a_k$ has summable $p$-th roots.
2. Put $\delta_k=C_3\lambda_k/B_k$. Since $F_k\ge-\delta_k$ and $\int F_k=0$,
   $$
   \int|F_k|=2\int F_k^-\le2\delta_k.
   $$
   The summable floors therefore imply $\sum_k\int|F_k|<\infty$. Tonelli gives $\sum_k|F_k(x)|<\infty$ for almost every $x$. In fact this gives absolute almost-everywhere and $L^1$ convergence independently of the block-independence argument.

The $L^p$, $L^2$, and pointwise limits agree: norm convergence implies convergence in measure, and a pointwise limit of the same partial sums is the same limit almost everywhere. The integral of the limit is zero by $L^1$ convergence. All blocks and hence the limit are real-valued.

Rosenthal's original 1970 paper, cited by Ho as reference [14], was not itself re-proved in this audit. The displayed standard inequality is used correctly, and the independent elementary route above is sufficient for the accepted theorem.

## Local amplification and its probability

A trial selects the exponents $M+rD$, $1\le r\le\ell$, where $1\le\ell\le L/8$ and $M+D\ge0$. Regrouping the finite double sum by $h=q+r$ is exact:

$$
\sum_{r=1}^{\ell}F(2^{M+rD}x)
=\sqrt{\lambda/L}\sum_{h=2}^{L+\ell}w_h
\phi_d(2^{U+M+hD}x).
$$

The weight counts pairs $q+r=h$. Therefore $\sum_hw_h=L\ell$, $0\le w_h\le\ell$, and $w_h=\ell$ on the inclusive range $\ell+1\le h\le L+1$. There are exactly $L-\ell+1$ central variables. The endpoint indices have no off-by-one defect.

Their digit windows are disjoint because the shifts differ by $D\ge d+2$, and all shifts are nonnegative: the smallest possible shift $U+M+2D$ is at least $D$. With $n_c=L-\ell+1$,

$$
\Pr(E)=1-(1-\theta)^{n_c},\quad
n_c\ge7L/8,\quad
\frac{\lambda}{128B^2L}<\theta\le\frac{\lambda}{64B^2L}.
$$

Since $n_c\theta\le1/64$, the elementary union lower bound yields

$$
\Pr(E)\ge\tfrac12n_c\theta
>\frac{7\lambda}{2048B^2}
\ge c_0\frac{\lambda}{B^2}
$$

with, for example, $c_0=1/1024$.

If at least one central variable takes its positive value, all other terms can be bounded below by their negative floors. Discarding an additional positive term only weakens the estimate:

$$
\sum_{r=1}^{\ell}F(2^{M+rD}x)
\ge\ell\left(\sqrt{\lambda/L}\,h_d-\sqrt{\lambda L}\,g_d\right).
$$

The first parenthesized term is at least $4\sqrt2B$; the subtracted term is at most $\lambda/(4\sqrt2B)\le B$. Thus the sum is at least $2B\ell$, as claimed. Multiple positive spikes only help. There is no assumption that noncentral terms vanish or are independent of the good event.

## Stage geometry and independent trials

All parameters are fixed deterministically before testing events at $x$. The schedule does not select a new sequence adaptively according to successes.

For $\eta=1/20$, the ceiling in the source's length recursion is redundant because $P_{k,t}$ is an integer. In one stage, starting from $P=P_{k,1}$, the exact formulas are

$$
\ell_{k,t}=20(P+1)21^{t-1},\qquad
P_{k,t}+1=(P+1)21^{t-1},
$$

$$
N_k^*+1=(P+1)21^{T_k},\qquad
L_k=160(P+1)21^{T_k-1}.
$$

These imply every needed bound in Lemma 4.1, with $C_\eta=21$, and ensure every trial has $\ell_{k,t}\le L_k/8$. The trial term count $N_{k,t}=P_{k,t}+\ell_{k,t}$ satisfies $N_{k,t}\le(1+\eta)\ell_{k,t}$.

The first trial of a stage is placed after all previously selected exponents and after all previously used event-digit coordinates, by (4.10). The starts are possible because only finitely many lower bounds have been imposed at each stage. For successive trials the source chooses

$$
M_{k,t+1}=M_{k,t}+(L_k+\ell_{k,t})D_k+d_k+2.
$$

The current trial's good-event coordinates are no later than

$$
U_k+M_{k,t}+(L_k+1)D_k+d_k.
$$

Every coordinate of the next good event is beyond this bound. Even the larger range containing all variables in the current trial ends by $U_k+M_{k,t}+(L_k+\ell_{k,t})D_k+d_k$; the recursion leaves a gap beyond that range. The source's $\Omega_k$ is an upper bound for the full range of the last trial and hence for all prior good events. Thus all good events $E_{k,t}$ across all stages and trials depend on disjoint digit sets.

Within each trial the exponents increase by $D_k$. Between adjacent trials the first exponent of the next trial exceeds the last of the current one by

$$
(L_k+1)D_k+d_k+2>0.
$$

Since $D_k=d_k+2$, this gap is exactly $(L_k+2)D_k$. Across stages the first inequality in (4.10) gives strict ordering. The resulting integer exponents are all distinct, so the associated integers $n_j=2^{m_j}$ satisfy the required ratio bound.

The independence has two separate uses: block independence supports the original moment/convergence proof; event independence supports the trial probabilities. Independence of the collection of all blocks from the collection of all good events is neither true in general nor required. In particular, future blocks can interact with digits from old events without damaging any estimate below.

For $S_k=\bigcup_{t=1}^{T_k}E_{k,t}$, independence within a stage gives

$$
\Pr(S_k^c)\le\exp(-c_0T_k\lambda_k/B_k^2).
$$

Independence across stages also holds and justifies the second Borel–Cantelli statement in Proposition 4.3(i). Theorem 1.6 only needs the first Borel–Cantelli lemma and summable failure probabilities.

## Shielding the complete partial sum

Let $\mu=\sum_k\delta_k<\infty$. On the set where the block series converges, termwise lower floors imply

$$
f(y)\ge-\mu,\qquad f(y)-F_k(y)\ge-\mu\quad\text{for all }k.
$$

There is one full-measure set on which these inequalities and convergence hold for every $k$: only countably many omissions are involved, and absolute convergence also gives this directly. Intersect its inverse images under every selected measure-preserving dyadic map $x\mapsto2^{m_j}x$. The resulting set still has measure one. Fix a representative of $f$, assigning any finite value on the original exceptional set. On this inverse-image intersection its values at all selected dilations agree with the convergent series. No uncountable intersection or unchecked pointwise evaluation of an $L^p$ equivalence class occurs.

At a successful trial endpoint $N=P+\ell$, split the finite partial sum into: the current block over the new trial; the entire function over the $P$ earlier selected terms; and the remaining blocks over the $\ell$ new terms. The lower bound is

$$
\sum_{j\le N}f(n_jx)\ge2B_k\ell-\mu P-\mu\ell
=2B_k\ell-\mu N.
$$

Since $N\le(1+\eta)\ell$,

$$
\frac1N\sum_{j\le N}f(n_jx)
\ge\frac{2B_k}{1+\eta}-\mu
\ge B_k-\mu.
$$

This checks Proposition 4.3's decisive estimate. The negative error is $\mu N$, not a quantity multiplying the spike height or the number of future stages. No conditioning on the rest of the series, independence from the good event, or cancellation estimate is silently used.

## Section 7 parameters and absence of circularity

Fix $p\in[2,\infty)$ and choose $a_k=2^{-k-2}$. The sum of this sequence is $1/4$. At stage $k$, the previous stages and $P=P_{k,1}$ are already fixed. For a proposed $B\ge100$, set

$$
\lambda=a_kB^{-(p-2)},\qquad
T=\left\lceil\Gamma B^p a_k^{-1}\log(k+1)\right\rceil,
\quad\Gamma\ge8/c_0.
$$

These are valid for every finite proposed $B$: $0<\lambda\le a_k\le1$, $T$ is a positive finite integer, and the exact length formulas give finite integer $L$. A depth $d$ always exists because every interval $[X,2X)$ with $X>0$ contains a power of two. The remaining digit and exponent shifts have only finite lower constraints. None of those shifts changes the number of selected terms.

The exact count formula gives a constant $K_k>0$, independent of proposed $B$, such that

$$
\log N_k^*(B)\le K_k B^p\qquad(B\ge100).
$$

For example, use $T\le\Gamma B^p a_k^{-1}\log(k+1)+1$, the fixed $\log(P+1)$, and $B^p\ge1$ to absorb the fixed additive terms into $K_k$. Consequently, with

$$
\varepsilon_k=\frac1{2p(k+2)},\qquad
\alpha_k=1/p-\varepsilon_k>0,
$$

$$
\frac{B}{(\log N_k^*(B))^{\alpha_k}}
\ge K_k^{-\alpha_k}B^{p\varepsilon_k}\longrightarrow\infty.
$$

This holds even though the stage endpoint changes with $B$. Ceiling discontinuities do not affect the bound, and continuity is not invoked. The constants can be arbitrarily large as functions of past stages; each is fixed before the current $B$ is chosen.

The manuscript's upper bound $\bar\mu_k(B)$ in (7.4) correctly separates known past floors, the current floor, and a deterministic upper bound on all future floors. It is bounded as $B\to\infty$. There is also the simpler uniform estimate, valid for every stage choice,

$$
\mu=C_3\sum_i\frac{a_i}{B_i^{p-1}}
\le\frac{C_3}{4\cdot100^{p-1}}=:M_p.
$$

Thus the eventual unknown constant creates no circularity. Choose $B\ge\max(100,2M_p)$ sufficiently large that

$$
\frac{B-M_p}{(\log N_k^*(B))^{\alpha_k}}\ge k.
$$

An explicit sufficient inequality is $B^{p\varepsilon_k}\ge2kK_k^{\alpha_k}$. The choice can be made among integer $B$, although integrality of $B$ is not required. This also verifies the source's condition (7.5), using its bounded $\bar\mu_k(B)$ instead if desired. Later choices cannot invalidate the floor bound.

For $p=2$, $\lambda=a_k$ does not shrink as $B$ increases. This is harmless: $T$ grows as $B^2$, and the same positive exponent $p\varepsilon_k$ still makes the displayed ratio diverge. There is no lost $p=2$ endpoint in the parameter argument.

## Almost sure success and simultaneous exponents

The chosen number of trials yields

$$
\Pr(S_k^c)
\le\exp(-c_0\Gamma\log(k+1))
\le(k+1)^{-8}.
$$

Their sum is finite. The measure of the union of failures from stage $K$ onward is at most the tail of that convergent series, which tends to zero. Therefore almost every $x$ has a successful trial in every sufficiently large stage. This conclusion does not need independence between different stages.

Intersect this set with the common full-measure evaluation set already obtained. For any $x$ in the intersection and every sufficiently large $k$, select one successful trial endpoint $N_{k,t}\le N_k^*$. This selection is only a subsequence of the already fixed global sequence; it does not change the constructed $n_j$.

The stage choice ensures $B_k-\mu>0$. Since $\alpha_k>0$, replacing $N_{k,t}$ by $N_k^*$ in the logarithmic denominator weakens the lower bound. Hence

$$
\frac{\sum_{j\le N_{k,t}}f(n_jx)}{N_{k,t}(\log N_{k,t})^{1/p-\varepsilon_k}}
\ge\frac{B_k-\mu}{(\log N_k^*)^{\alpha_k}}
\ge k.
$$

All these endpoints exceed 1, and they tend to infinity because successive stages append positive numbers of terms. Given any $\varepsilon>0$, eventually $\varepsilon_k<\varepsilon$. Since $\log N_{k,t}>1$ and the numerator just bounded is positive, changing the denominator exponent from $1/p-\varepsilon_k$ to $1/p-\varepsilon$ only increases the quotient. The same endpoints therefore give lower bounds $k$ for the requested exponent.

The full-measure set was chosen before fixing $\varepsilon$, so the conclusion is genuinely simultaneous for all positive real $\varepsilon$. This is stronger than merely saying “for each $\varepsilon$, almost everywhere,” and the source's quantifier order is justified without an uncountable intersection.

## Compatibility with geometric ergodic averages

For the doubling transformation $Tx=2x\pmod1$, the ordinary ergodic averages $N^{-1}\sum_{j=1}^N f(T^jx)$ converge to the integral for $f\in L^1$. Ho does not use consecutive iterates. The constructed samples are $f(T^{m_j}x)$, where the $m_j$ form long arithmetic progressions with stage-dependent step $D_k$, separated by still larger gaps. For example, the within-stage gap between trials is exactly $(L_k+2)D_k$.

Neither convergence along all consecutive times nor convergence along the powers of one fixed iterate $T^D$ supplies uniform control for this changing collection of finite, far-shifted trial segments. The important denominator $N$ counts selected samples, not $m_N$ and not $n_N$. The size of the exponent gaps has no penalty in the Section 7 term-count estimate. There is therefore no inference from geometric ergodicity that contradicts the construction, and no erroneous replacement of these sparse samples by consecutive dyadic powers in the proof.

The common event construction is deliberately arranged to find rare exceptional finite segments for the current block. Every fixed block can still obey its own appropriate ordinary ergodic theorem; the signal-producing block changes with the stage.

## Consequence and remaining boundary

Take $p=2$ and any fixed $0<\varepsilon<1/2$, for example $\varepsilon=1/4$. Then

$$
\frac{(\log N)^{1/2-\varepsilon}}{\sqrt{\log\log N}}\longrightarrow\infty.
$$

The positive infinite limsup established by Theorem 1.6 therefore contradicts $o(N\sqrt{\log\log N})$. Indeed the same positive subsequence yields infinite limsup when divided by $N\sqrt{\log\log N}$. Thus the precise proposed universal bound in the audited problem has a negative answer, credited to Ho's preprint.

The manuscript's elementary comparison in Remark 7.1, pages 23–24, is also consistent: for any increasing sequence of positive integers, the $L^p$ norm of the maximal partial sum on a dyadic range is bounded by the sum of the $L^p$ norms of its summands. Chebyshev at height $2^m m^{1/p+\varepsilon}$ gives a summable $O(m^{-1-p\varepsilon})$ exceptional bound. This supplies the upper exponent $1/p+\varepsilon$, without even requiring lacunarity. It does not supply the exact endpoint exponent $1/p$ or optimal secondary logarithms.

There is no remaining proof obstruction to the stated Theorem 1.6 conclusion. The remaining restrictions are scope restrictions: no optimal epsilon-free endpoint is established here; no bounded-gap or exact-geometric version is claimed; and this audit does not change the manuscript's publicly verified preprint status or make an independent claim about the Fourier-tail theorems for Erdős 996.
