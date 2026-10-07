# Continuation C4: a BK–Poisson block proof candidate

Date: 2026-10-07. Problem 9700042 / AMR-096-0042.

## Status

This is the fifth supported substantive author attempt: the historical approach plus C1–C4. It is a complete proof candidate submitted for fresh independent review. **It is not yet an accepted solution.** No claim of novelty, human peer review, or formal verification is made. C1's accepted partial-result audit does not validate the new argument below. The earlier C1–C3 files are preserved unchanged.

The proposed conclusion is the full canonical asymptotic

\[
\lim_{q\downarrow0}\frac{1-v(1-q)}{\sqrt{2q}}=1.
\tag{T}
\]

The mechanism differs from the unsuccessful local-density rule in C3: rectangles may overlap and long strip excursions are allowed. Disjoint *closed-edge witnesses* for path segments permit a BK product bound, while a coarse endpoint skeleton has entropy independent of the microscopic lattice spacing.

## External inputs and exact model

The model is precisely the finite north/east Bernoulli-capacity square in Aldous's primary problem page. C1 established its finite directed planar-dual identity; a fresh independent audit accepted that identity and the C1 partial bound. We use the following notation, suppressing the two harmless boundary edges:

- Q_N={0,...,N}^2 is the reflected dual square.
- Each east/north edge is independently marked with probability q.
- Traversing a forward edge gives reward 1 if marked, 0 otherwise; traversing a west/south edge gives reward -1 regardless of its mark.
- D_N is the maximum reward of a corner-to-corner path confined to Q_N.
- Cycles have nonpositive reward, so a maximizer can be simple.
- The original flow normalization is

\[
g(q):=1-v(1-q)=\lim_{N\to\infty}\frac{\mathbb E D_N}{2N}.
\tag{22}
\]

Equation (22) uses the source-stated L1 flow-density limit and C1's exact boundary identity. It is an explicit dependency, not a new existence proof.

Only two further external probability inputs are used:

**P. Poisson increasing chains.** If Lambda_s is the longest increasing chain of a rate-one Poisson process in a square of side s, then Lambda_s/s -> 2 in probability and mean. For every a>0, its upper tail beyond (2+a)s is at most exp(-c_a s) for sufficiently large s. These are standard consequences of the fixed-sample results stated in the introduction and Theorem 2 of J.-D. Deuschel and O. Zeitouni, *On increasing subsequences of i.i.d. samples*, https://www.wisdom.weizmann.ac.il/~zeitouni/pdf/ccp.pdf, arXiv:math/9803035. The elementary Poissonization and moment consequence needed here are detailed below.

**BK. Disjoint occurrence.** For finitely many increasing events in a finite Bernoulli product space, the probability of their disjoint occurrence is at most the product of their probabilities. The original result is J. van den Berg and H. Kesten, *Inequalities with applications to percolation and reliability*, J. Appl. Probab. 22 (1985), 556–569, https://doi.org/10.2307/3213860. A primary-author restatement, including the precise witness definition and product-measure theorem, is Theorem 1.1 and the preceding definitions in J. van den Berg and J. Jonasson, https://arxiv.org/pdf/1105.3862, PDF pages 2–3. The finite-many version follows by iteration; increasing disjoint-occurrence events are increasing, and mutually disjoint witnesses certify the iterated event.

Everything else, including the required order of limits, is proved below.

## 1. A stronger consequence of the C1 count

Let K_N^+ be the largest number k(P) of marked forward edges on a simple corner-to-corner path satisfying b(P)<=k(P), where b counts backward steps. Define it as zero if necessary. This controls k and b, rather than only their difference D_N.

The marked-list enumeration in C1 bounds the probability of a path with exactly k marks and b<=k by

\[
A_{N,k}(q):=(2q)^k\binom{N+2k}{k}^2
\left(1+\sqrt{\frac{k}{N+2k}}\right)^{4k+2}.
\tag{23}
\]

The argument counts ordered distinct marked edges, with each coordinate's total negative variation at most k. It does not require k-b to exceed a separate threshold. Thus it applies to K_N^+ directly.

For q<=10^{-6} and integers k>=32 sqrt(q) N,

\[
A_{N,k}(q)\leq4\,4^{-k}. \tag{24}
\]

Indeed, if k<=N/4, the C1 binomial estimate gives

\[
A_{N,k}\leq\frac94
\left[2e^2(3/2)^6 q(N/k)^2\right]^k,
\]

and 2e^2(3/2)^6/32^2 < 1/4. If k>N/4, it gives

\[
A_{N,k}\leq4[32e^2q(4+2)^2]^k\leq4\,4^{-k}.
\]

Consequently, for integers r>=ceil(32 sqrt(q) N),

\[
\Pr(K_N^+\geq r)\leq6\,4^{-r}. \tag{25}
\]

In particular, with probability tending to one exponentially in sqrt(q) N, an optimal nonnegative-reward simple path has

\[
b(P)\leq k(P)\leq B_N:=\lceil32\sqrt q\,N\rceil.
\tag{26}
\]

Nonnegative reward is available from a monotone path. Thus (26) is not inferred from an upper bound on D_N alone.

For every fixed 0<theta<log 4, (25), D_N<=K_N^+, and tail summation also give a constant C_theta>=1 such that

\[
\mathbb E e^{\theta D_N}\leq C_\theta e^{32\theta\sqrt q\,N},
\qquad q\leq10^{-6},\ N\geq1.
\tag{27}
\]

For example, split at ceil(32 sqrt(q)N) and sum the resulting geometric tail; a constant no larger than

\[
e^\theta\left(1+\frac{6e^\theta}{1-e^\theta/4}\right)
\]

suffices. Enlarging a rectangle of side lengths W,H to a square of side max(W,H), adding independent marks outside it, and padding paths monotonically yields

\[
\mathbb E e^{\theta D_{W,H}}
\leq C_\theta e^{32\theta\sqrt q(W+H)}.
\tag{28}
\]

Here D_{W,H} is the analogous corner-to-corner reward confined to the rectangle. Equation (28) is deliberately nonsharp and will only be used for the exceptional rectangles.

## 2. Fixed-scale sparse convergence, with exponential moments

Let W_q,H_q be positive integer side lengths such that

\[
\sqrt q\,W_q\to w>0,\qquad\sqrt q\,H_q\to h>0.
\]

The marked-edge starting positions, scaled by sqrt(q) and forgetting their two orientations, converge to a rate-two Poisson point process on [0,w] x [0,h]. This follows directly from the independent Bernoulli Laplace functional: each interior lattice vertex supplies two independent possible marks, and boundary contributions vanish.

The unrestricted reward D_{W_q,H_q} has the same limit as the increasing-chain length of that process. Here is the needed deterministic stability argument.

Fix an integer M. On the event that the total number Z of marks is at most M and every two marked starting positions differ by more than M in *each* coordinate, any nonnegative-reward simple path has b<=k<=M. Its ordered marked starting positions cannot decrease in either coordinate: such a decrease would cost more than M backward steps. The marked positions therefore form a strict increasing chain. Conversely, any such chain can be visited monotonically, including each marked edge, because the coordinate gaps exceed M>=1. Hence the unrestricted reward equals the monotone chain length on this event.

For each fixed M, the chance of a pair within M in either coordinate tends to zero as q decreases to zero. For example, a union bound gives order O_M(q^{1/2}) in a rectangle of bounded rescaled size. The variable Z is binomial with uniformly bounded mean and converges to Poisson(2wh), so its tail above M can then be made arbitrarily small. Strict increasing-chain length is locally constant under perturbations of a finite point configuration with no coordinate ties, an almost-sure property of the limiting Poisson process. These observations prove convergence in distribution.

Moreover 0<=D_{W_q,H_q}<=Z, and, for every fixed a>0,

\[
\mathbb E e^{aZ}
=(1-q+qe^a)^{2W_qH_q+W_q+H_q}
\leq\exp[(2W_qH_q+W_q+H_q)q(e^a-1)].
\]

The right side stays bounded. Taking a larger exponent establishes uniform integrability of every fixed exponential moment. We have therefore proved

\[
\mathbb E e^{\theta D_{W_q,H_q}}
\longrightarrow\mathbb E e^{\theta\Lambda_{\sqrt{2wh}}}
\quad\text{for every fixed }\theta>0.
\tag{29}
\]

The Poisson rectangle has the same chain-length law as the rate-one square of side sqrt(2wh), by a separate positive rescaling of the two coordinates. No large-volume limit is interchanged in (29); w and h are fixed first.

## 3. The sharp Poisson exponential-moment estimate

We need the following consequence of input P: for every epsilon>0 there are theta in (0,log 4) and s_0 such that

\[
\mathbb E e^{\theta\Lambda_s}
\leq e^{\theta(2+\epsilon)s},\qquad s\geq s_0.
\tag{30}
\]

For completeness, the two ingredients and the conversion are recorded explicitly.

First, the fixed-sample upper-tail theorem implies the stated Poisson tail. If Z_s is Poisson(s^2), compare it with n=ceil((1+delta)s^2). The probability Z_s>n is exponentially small in s^2. On Z_s<=n, add independent uniform points up to n; the chain length increases. Choose delta sufficiently small that (2+a)s>(2+a/2)sqrt(n) eventually. The fixed-sample upper tail gives exp(-c_a s).

Second, direct counting of k-point increasing chains gives

\[
\Pr(\Lambda_s\geq k)\leq\frac{s^{2k}}{(k!)^2}
\leq\left(\frac{es}{k}\right)^{2k}. \tag{31}
\]

To deduce (30), choose a much smaller positive a than epsilon and a fixed M>10e. Below (2+a)s, bound the exponential by e^{theta(2+a)s}. Between (2+a)s and Ms, the first tail estimate contributes at most a polynomial factor in s times e^{theta Ms-c_a s}. Choose theta>0 small enough that this is exponentially smaller than e^{theta(2+2a)s}. Above Ms, (31) gives a convergent geometric bound, uniformly for this theta. Absorb the finitely many constant/polynomial factors by the remaining gap between 2+2a and 2+epsilon, taking s sufficiently large. This proves (30).

Since 2sqrt(2wh)<=sqrt(2)(w+h), (30) implies, with epsilon changed harmlessly, that for any fixed finite collection of rectangle aspect ratios and all sufficiently large common scale R,

\[
\log\mathbb E e^{\theta\Lambda_{\sqrt{2wh}}}
\leq\theta(1+\epsilon)\sqrt2(w+h).
\tag{32}
\]

All of these are ordinary finite-scale Poisson estimates.

## 4. Parameters and good rectangle moments

Fix a desired final excess zeta>0. Choose epsilon>0 small and an integer m large enough that

\[
\Delta:=(1+\zeta)-(1+\epsilon)(1+6/m)>0.
\tag{33}
\]

Choose theta from (30), using a slightly smaller epsilon if needed. Next choose a large fixed R; it will be enlarged once more below. For q sufficiently small define integer scales

\[
h=\left\lfloor\frac{R}{m\sqrt q}\right\rfloor\geq1,
\qquad L=mh.
\tag{34}
\]

Thus sqrt(q)L -> R as q decreases to zero. Crucially, L/h=m is a fixed integer: skeleton entropy will not contain log(1/q).

The good rectangles below have side lengths

\[
W=(z+3)h,\qquad H=(m-z+3)h,
\quad z\in\{-2,-1,...,m+2\}. \tag{35}
\]

There are only m+5 possible shapes, both sides are at least h, and W+H=L+6h. Use (29), (32), and the finite number of shapes to obtain, for fixed sufficiently large R and all sufficiently small q,

\[
\mathbb E e^{\theta D_{W,H}}
\leq2\exp\{\theta(1+\epsilon)\sqrt{2q}(L+6h)\}.
\tag{36}
\]

The factor 2 absorbs finite-q convergence and integer rounding. The threshold on q is uniform over these finitely many shapes and is independent of N.

## 5. First-passage slicing and deterministic rectangles

Work on the high-probability event in (26), and choose a simple optimal path P. Slice it at its first hitting times of successive levels x+y=L,2L,... below 2N, with the final endpoint included. There are

\[
J=\lceil2N/L\rceil
\]

segments. Let the endpoints be (x_j,y_j), j=0,...,J, with t_j=x_j+y_j. For j<J the level increments are L, and the last increment tau_j=t_{j+1}-t_j is in (0,L].

Let b_j be the number of backward steps in segment j. Record the integers

\[
i_j=\lfloor x_j/h\rfloor,
\qquad s_j=\lfloor b_j/h\rfloor,
\qquad a_j=(s_j+1)h>b_j.
\tag{37}
\]

The record (i_0,...,i_J;s_0,...,s_{J-1}) is the skeleton. Since i_0=0 and sum b_j=b(P)<=B_N,

\[
\sum_j s_j\leq K:=\lfloor B_N/h\rfloor. \tag{38}
\]

For this skeleton define the axis-aligned rectangle with lower corner

\[
(i_jh-a_j,\ t_j-(i_j+1)h-a_j)
\]

and upper corner

\[
((i_{j+1}+1)h+a_j,\ t_{j+1}-i_{j+1}h+a_j).
\tag{39}
\]

Every vertex of segment j lies in this rectangle. In a coordinate, the path cannot go below its starting coordinate by more than b_j; it cannot exceed its ending coordinate by more than b_j, since it would need that many negative steps to get back. The endpoint quantization in (39) enlarges these bounds.

Writing W_j,H_j for the side lengths gives the exact identity

\[
W_j+H_j=\tau_j+2h+4a_j. \tag{40}
\]

Also -s_j-2<=i_{j+1}-i_j<=m+s_j+2. These bounds imply positive side lengths, at least h.

Call a segment good if s_j=0 and it is not the last segment. Its rectangle is one of (35). The remaining segments are bad. There are at most K+1 bad segments. Since each nonlast bad segment has s_j>=1 and a_j< b_j+h<=2b_j,

\[
\sum_{\mathrm{bad}}(W_j+H_j)
\leq(m+10)B_N+(L+6h). \tag{41}
\]

One way to check (41) directly is to use (40): the number of nonlast bad segments is at most sum b_j/h, their tau_j contributions are at most m sum b_j, their 2h contributions at most 2 sum b_j, and their 4a_j contributions at most 8 sum b_j. The last segment adds at most L+6h+4b_last, which is covered by the same (m+10)B_N budget if it was not counted among the nonlast segments.

Rectangles are allowed to extend outside Q_N. Extend the mark field independently to the needed finite union of rectangles. This changes neither D_N nor the disjoint witnesses below.

## 6. Skeleton counting

For fixed s_j, the number of possible next coarse x-coordinates is at most

\[
m+2s_j+5\leq(m+5)(s_j+1).
\]

Since s+1<=e^s, the number of endpoint records for a given s-vector is at most (m+5)^J e^K. The number of nonnegative integer s-vectors with sum at most K is binom(J+K,K). Hence the total skeleton count is bounded by

\[
(m+5)^J e^K\binom{J+K}{K}. \tag{42}
\]

As N tends to infinity at fixed q,m,R,

\[
\frac KJ\longrightarrow\kappa(q):=16m\sqrt q.
\tag{43}
\]

The entropy per segment beyond log(m+5) is therefore vanishing as q decreases to zero. With

\[
F(u)=(1+u)\log(1+u)-u\log u,\quad F(0)=0,
\]

we have log binom(J+K,K) <= J F(K/J). No microscopic endpoint enumeration is used.

## 7. Why BK applies despite overlapping rectangles

For a fixed skeleton let X_j be the unrestricted corner reward D_{W_j,H_j} in its rectangle, computed from the extended common field. Let r_j be the positive part of the actual reward of segment j. These are nonnegative integers and

\[
\sum_j r_j\geq D_N.
\]

For each j, the set of marked forward edges actually traversed by the segment is a witness for the increasing event {X_j>=r_j}. To see this, keep those edges marked and allow all other edge states to vary. The segment's reward does not decrease: its originally unmarked forward edges contribute at least zero, and its backward steps always cost one. Pad the segment from the rectangle's lower corner to its start and from its end to the upper corner by monotone paths. Padding has nonnegative reward, even when every added edge is unmarked. The resulting walk has reward at least r_j. Removing cycles cannot decrease reward, so a simple corner path certifies X_j>=r_j. If r_j=0 the empty witness is sufficient.

Because the global path P is simple, these original marked-edge witness sets are pairwise disjoint. They remain disjoint even when the enlarged rectangles overlap. Thus the relevant local events occur disjointly, and BK gives

\[
\Pr\bigl(\text{a realization of this skeleton has }D_N\geq d\bigr)
\leq\sum_{\substack{r_j\geq0\\\sum r_j\geq d}}
\prod_j\Pr(X_j\geq r_j).
\tag{44}
\]

Define S_theta=(1-e^{-theta})^{-1}. For any nonnegative integer X,

\[
\sum_{r\geq0}e^{\theta r}\Pr(X\geq r)
=\mathbb E\frac{e^{\theta(X+1)}-1}{e^\theta-1}
\leq S_\theta\mathbb E e^{\theta X}.
\]

Applying this to (44),

\[
\Pr(\text{this skeleton contributes at least }d)
\leq e^{-\theta d}S_\theta^J
\prod_j\mathbb E e^{\theta X_j}. \tag{45}
\]

This is a product of marginal moments obtained through BK, not an assertion that overlapping rectangles are independent.

## 8. The uniform large-volume upper bound

Put

\[
A_q=(1+\epsilon)\sqrt{2q}(L+6h).
\]

Use (36) on good rectangles, (28) and (41) on bad ones, and harmlessly assign the good baseline A_q to every segment. Combining (42) and (45) yields

\[
\begin{split}
\Pr\{D_N\geq d,\ (26)\text{ holds}\}
\leq{}&e^{-\theta d+\theta A_qJ}
\exp\{32\theta\sqrt q[(m+10)B_N+L+6h]\}\\
&\times[2(m+5)S_\theta]^J
 C_\theta^{K+1}e^K\binom{J+K}{K}.
\end{split}
\tag{46}
\]

Take d=ceil(2(1+zeta)sqrt(2q)N). Let N tend to infinity while q,m,R are fixed. Divide the logarithm of the right side by 2 sqrt(q)N. Its limsup is at most

\[
\begin{split}
&-\theta\sqrt2\,\Delta
+\frac{\log[2(m+5)S_\theta]}{\sqrt q L}\\
&\quad+\frac{\kappa(q)(1+\log C_\theta)+F(\kappa(q))}{\sqrt q L}
+512\theta(m+10)\sqrt q.
\end{split}
\tag{47}
\]

Now recall the actual parameter order. Epsilon and m were fixed first to make Delta>0; theta was then fixed. Enlarge R so that (36) is valid and

\[
\frac{\log[2(m+5)S_\theta]}R
<\frac12\theta\sqrt2\,\Delta. \tag{48}
\]

Finally let q be sufficiently small. Since sqrt(q)L -> R, kappa(q)->0 and F(kappa(q))->0, expression (47) is strictly negative. For every such fixed q, (46) tends to zero exponentially as N tends to infinity. The complement of (26) tends to zero by (25). We conclude

\[
\Pr\{D_N\geq2(1+\zeta)\sqrt{2q}\,N\}\longrightarrow0
\quad(N\to\infty). \tag{49}
\]

Since 0<=D_N<=2N, (22) and boundedness give

\[
g(q)\leq(1+\zeta)\sqrt{2q}
\]

for all sufficiently small q. Zeta was arbitrary, proving the proposed matching upper bound

\[
\limsup_{q\downarrow0}\frac{g(q)}{\sqrt{2q}}\leq1. \tag{50}
\]

## 9. A fresh lower bound, independent of the missing historical proof

Concatenating optimal paths in consecutive diagonal squares of side ell gives D_{k ell}>=sum_{j=1}^k D_ell^{(j)}. Taking expectations and using (22),

\[
g(q)\geq\frac{\mathbb E D_\ell}{2\ell}. \tag{51}
\]

For fixed R>0 set ell=floor(R/sqrt(q)). The fixed-scale convergence in Section 2, including convergence of expectations, implies

\[
\liminf_{q\downarrow0}\frac{g(q)}{\sqrt{2q}}
\geq\frac{\mathbb E\Lambda_{\sqrt2R}}{2\sqrt2R}.
\]

Let R tend to infinity and use the mean part of input P. The right side tends to 1. This supplies the lower bound anew, without relying on inaccessible historical author or audit bytes. Combined with (50), it gives candidate conclusion (T).

## 10. Review boundaries and required adversarial checks

The author regards the argument above as complete, but independent acceptance is pending. The following are the decisive review targets, not omitted assumptions:

1. The strengthened K_N^+ bound must count all nonnegative-reward simple paths, not just D_N itself.
2. The sparse finite-volume convergence must include orientation, coordinate separation, and exponential uniform integrability.
3. The external Poisson upper-tail input and its moment consequence must be verified at the stated normalization (rate two after lattice scaling).
4. The first-passage skeleton rectangles, (40)–(43), including the last segment, must have no missing entropy factor depending on q.
5. The local witnesses in Section 7 must be genuinely disjoint even with padding and overlapping rectangles. Their construction uses only original segment marks.
6. The parameter order is epsilon,m,theta,R; then sufficiently small fixed q; then N -> infinity. The final q -> 0 uses the resulting uniform-in-N inequality.

No finite computation can establish these infinite-volume arguments. The accompanying checks target deterministic slicing, the sparse stability lemma, and numerical constants only. All sources and historical limitations are separately listed in the package manifest. Until the fresh audit accepts this proof, the strongest independently accepted new theorem remains the C1 normalized limsup bound e/2.
