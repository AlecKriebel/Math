# Publication edition: infinite real-complement modulus

Status: accepted_full_stated_target. No mathematical correction is required.

This is an AI-assisted, unrefereed mathematical edition. Acceptance means an independent internal AI audit of the full theorem under its explicit curve and density conventions. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

The full authored proof and complete mathematical audit are retained in PROOF.md and AUDIT.md. Copied source documents, source text and images, executable code, raw datasets, raw search responses, independent preparatory material and private coordination material are not distributed. This is a written proof-and-audit edition, not a computational reproduction package.

Source retrieval and inspection statements describe the candidate and independent audit of October 11, 2026 UTC. Editorial preparation authenticated their sealed bytes and checked repository publication scope, but performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Hashes authenticate bytes; mathematical acceptance comes from reading the written arguments.

The candidate-status sentence in the frozen manuscript below records its status before the independent audit. The manuscript is now accepted in the precise sense above; its original text is retained in full, unchanged. The theorem does not assert a result for other interpretations of unspecified source terminology.

# Infinite modulus between a compact real set and its real complement

Authored mathematical candidate, 11 October 2026. Independent mathematical audit pending. No claim of priority or of exhaustive literature coverage is made.

## The exact claim

Identify the real line with the horizontal axis in the plane. For sets $A,B\subset\mathbb R^2$, let $\Gamma(A,B)$ denote all connecting curves with one endpoint in each set. Curves are continuous and locally rectifiable away from their endpoints; their nonnegative line integrals are the increasing limits of line integrals over compact interior subcurves. Globally rectifiable connecting curves are included. Constant portions contribute zero length. The same proof applies if only globally rectifiable connecting curves are used throughout.

For a curve family $\Gamma$, its $2$-modulus is

$$M_2(\Gamma)=\inf_{\rho\in\operatorname{Adm}(\Gamma)}\int_{\mathbb R^2}\rho^2\,dA,$$

where an admissible density is a Borel function $\rho:\mathbb R^2\to[0,\infty]$ satisfying $\int_\gamma\rho\,ds\ge1$ for every $\gamma\in\Gamma$. The infimum of an empty set is infinity. Densities may be infinite on sets of area zero. Write $S_2=\{z:|z|=2\}$.

**Theorem.** If $E\subset[0,1]$ is compact and

$$M_2(\Gamma(E,S_2))>0,$$

then, for $F=\mathbb R\setminus E$,

$$M_2(\Gamma(E,F))=\infty.$$

Here $F$ is the complement in the real line, not the planar complement. No positive-length assumption on $E$ is made. This is the formulation of Gonchar's question communicated by Vuorinen in Hayman and Lingham, Problem 7.58 [HL].

We prove the contrapositive: the existence of one finite-energy admissible density for $\Gamma(E,F)$ implies $M_2(\Gamma(E,S_2))=0$. First it forces $E$ to have length zero, by an explicitly constructed Sobolev potential and a trace calculation. A separate curve argument then handles every length-zero compact set, including sets of positive conformal capacity. We use no equivalence between condenser capacity and Sobolev capacity, and no assertion about quasicontinuous representatives.

## 1 Pointwise lower semicontinuous majorants

**Lemma 1.** Let $Q\subset\mathbb R^2$ be a compact rectangle and let $r:Q\to[0,\infty]$ be Borel with $\int_Q r^2\,dA<\infty$. There is a lower semicontinuous function $g:Q\to[1,\infty]$, in the relative topology of $Q$, such that $g\ge r$ at every point and $\int_Qg^2\,dA<\infty$.

**Proof.** Put $h=r^2$ and $A_k=\{h>2^k\}$ for $k\ge0$. By outer regularity of area restricted to $Q$, choose relatively open $O_k\supset A_k$ such that

$$|O_k|\le |A_k|+2^{-2k-4}.$$

Define

$$H=1+\sum_{k=0}^{\infty}2^{k+1}\mathbf1_{O_k},\qquad g=\sqrt H.$$

The indicator of an open set is lower semicontinuous. Finite sums and increasing limits preserve lower semicontinuity, so $H$ and $g$ are lower semicontinuous. If $h\le1$, then $H\ge h$. If $1<h<\infty$, the sum of the terms for which $2^k<h$ is at least $h-1$, so again $H\ge h$. If $h=\infty$, the point belongs to every $A_k$ and hence every $O_k$, and $H=\infty$. Thus the domination is pointwise, including all infinite values of $r$.

For every finite $h\ge0$,

$$\sum_{k\ge0}2^{k+1}\mathbf1_{\{h>2^k\}}\le4h.$$

Tonelli therefore gives

$$\int_Q H\,dA\le |Q|+4\int_Qh\,dA+\sum_{k\ge0}2^{-k-3}
=|Q|+4\int_Qh\,dA+\tfrac14<\infty.$$

In particular $g$ is finite almost everywhere, although infinite values on an area-zero set have been preserved. This proves the lemma. $\square$

## 2 A measurable path-distance potential with exact plate values

Fix the compact rectangle $Q=[-2,3]\times[-2,2]$, whose interior contains $E$. Suppose $E$ is nonempty, $g\ge1$ is lower semicontinuous on $Q$, and $g\in L^2(Q)$. For $z\in Q$, set

$$d(z)=\inf_\alpha\int_\alpha g\,ds,\qquad u(z)=\min\{1,d(z)\},$$

where the infimum is over all globally rectifiable curves in $Q$ from a point of $E$ to $z$. Set the infimum to infinity when all such integrals are infinite. Constant curves at points of $E$ are allowed, so $d=0$ on $E$.

**Lemma 2.** The functions $d$ and $u$ are lower semicontinuous and hence Borel. Every rectifiable curve $\beta\subset Q$ from $x$ to $y$ satisfies

$$|u(x)-u(y)|\le\int_\beta g\,ds. \tag{1}$$

Moreover, $u\in W^{1,2}(\operatorname{int}Q)$ and $0\le u\le1$.

**Proof of measurability.** We give the weighted-length compactness detail. For a nonnegative continuous function $a$ on $Q$, weighted length is lower semicontinuous under uniform convergence of curves with a common Lipschitz bound. One direct proof uses, for every finite partition $P=(t_i)$ of $[0,1]$, the lower sums

$$S_P(\alpha)=\sum_i\left(\min_{t\in[t_{i-1},t_i]}a(\alpha(t))\right)
|\alpha(t_i)-\alpha(t_{i-1})|.$$

Each $S_P$ is continuous for uniform convergence. Its supremum over partitions is $\int_\alpha a\,ds$: refinement approximates the variation of the rectifiable curve, while uniform continuity of $a\circ\alpha$ makes the difference between the upper and lower weights arbitrarily small. Thus weighted length is a supremum of continuous functions.

A nonnegative lower semicontinuous $g$ on compact $Q$ is an increasing limit of continuous nonnegative functions. For example, the functions

$$a_m(x)=\min\left\{m,\inf_{y\in Q}\big(g(y)+m|x-y|\big)\right\},\qquad m\ge1,$$

are continuous, increase to $g$, and are nonnegative. To check the pointwise limit, any sequence of near-minimizers that could keep $a_m(x)$ below $g(x)$ must tend to $x$; lower semicontinuity then rules this out. This also covers $g(x)=\infty$. Monotone convergence of the line integrals shows that $\alpha\mapsto\int_\alpha g\,ds$ is lower semicontinuous under the same uniform convergence.

Now let $z_j\to z$ with $L=\liminf_jd(z_j)<\infty$. Pass to a subsequence with $d(z_j)\to L$ and choose curves $\alpha_j$ with $g$-length at most $d(z_j)+1/j$. Since $g\ge1$, their Euclidean lengths are bounded. Parameterize them on $[0,1]$ with a common Lipschitz bound. They remain in the fixed compact set $Q$, so Arzela-Ascoli gives a uniformly convergent subsequence with a rectifiable limit $\alpha$. The starting points lie in compact $E$, hence $\alpha(0)\in E$, and $\alpha(1)=z$. Lower semicontinuity of weighted length gives

$$d(z)\le\int_\alpha g\,ds\le\liminf_j\int_{\alpha_j}g\,ds\le L.$$

This proves lower semicontinuity of $d$, including the case $d(z)=\infty$. There is no escape-to-infinity issue because all these auxiliary paths are confined to $Q$. Truncation at $1$ preserves lower semicontinuity.

**Proof of (1) and Sobolev regularity.** Concatenating a near-minimizing path to $x$ with $\beta$ gives $d(y)\le d(x)+\int_\beta g\,ds$ whenever the right side is finite. Reverse $x,y$ and then truncate at $1$. If a distance is infinite, a finite-length connection from a point at finite distance would make it finite, so the same truncated inequality still holds. This proves (1).

For almost every horizontal or vertical line, $g$ is integrable on its intersection with $Q$, by Fubini and Cauchy-Schwarz. Apply (1) to every subsegment of each such line. It proves absolute continuity of the actual pointwise function $u$ on that line, with the corresponding one-dimensional derivative bounded in absolute value by $g$ almost everywhere. In particular the two partial derivatives belong to $L^2(Q)$. Integrating the one-dimensional integration-by-parts identities against test functions and applying Fubini identifies them as weak derivatives. Since $u$ is bounded and Borel, $u\in W^{1,2}(\operatorname{int}Q)$. In particular $|\nabla u|^2\le2g^2$ almost everywhere is sufficient for finite energy. $\square$

Suppose now that $\rho\in L^2(\mathbb R^2)$ is admissible for $\Gamma(E,F)$ and choose $g\ge\rho$ on $Q$ by Lemma 1. Every auxiliary path from $E$ to $x\in F\cap Q$ belongs to $\Gamma(E,F)$, so its $g$-length is at least $1$. Consequently this pointwise construction has the exact values

$$u=0\text{ on }E,\qquad u=1\text{ on }F\cap Q. \tag{2}$$

These identities come from admissibility for every connecting curve. They are not obtained by choosing values of an almost-everywhere Sobolev representative on the real line.

Choose $\eta\in C_c^\infty(\operatorname{int}Q)$ with $\eta=1$ in a neighborhood of $[0,1]\times\{0\}$. Extend

$$w=\eta(1-u)$$

by zero to the plane. Then $w\in W^{1,2}(\mathbb R^2)$ has compact support. On almost every vertical line it is absolutely continuous, and its value at height zero is, by (2),

$$f(x):=w(x,0)=\mathbf1_E(x)\quad\text{for almost every }x\in\mathbb R. \tag{3}$$

The exceptional vertical lines have one-dimensional measure zero by Fubini. No conclusion about values at their endpoints, and no capacity statement about them, is used in this trace identification.

## 3 The trace calculation and characteristic-function rigidity

**Lemma 3.** If $w\in W^{1,2}(\mathbb R^2)$ has compact support and $f(x)=w(x,0)$ is its almost-everywhere vertical absolute-continuity trace, then

$$\int_{\mathbb R}\frac{\|f(\cdot+h)-f\|_{L^2(\mathbb R)}^2}{h^2}\,dh<\infty. \tag{4}$$

**Proof.** First let $w$ be smooth and compactly supported, and use the unitary Fourier transform in the horizontal variable, with frequency convention $e^{-ix\xi}$. Write $W(\xi,y)=\widehat{w(\cdot,y)}(\xi)$. For each $\xi$,

$$|\xi|\,|W(\xi,0)|^2
\le2|\xi|\int_0^\infty |W(\xi,y)|\,|\partial_yW(\xi,y)|\,dy
\le\int_0^\infty\big(\xi^2|W(\xi,y)|^2+|\partial_yW(\xi,y)|^2\big)\,dy.$$

The first inequality follows by integrating the derivative of $|W|^2$ from $0$ to infinity; the second is $2ab\le a^2+b^2$. Plancherel gives

$$\int_{\mathbb R}|\xi|\,|\widehat f(\xi)|^2\,d\xi
\le\int_{y>0}|\nabla w|^2\,dA. \tag{5}$$

For a general compactly supported $W^{1,2}$ function, convolution supplies smooth compactly supported $w_j\to w$ in $W^{1,2}$. Their traces converge to the actual vertical trace in $L^2$, because for every such function $v$, one-dimensional absolute continuity gives

$$|v(x,0)|^2\le\int_0^\infty\big(|v(x,y)|^2+|\partial_yv(x,y)|^2\big)\,dy$$

for almost every $x$. Apply this to $v=w_j-w$ and integrate. Passing to a subsequence with almost-everywhere Fourier-transform convergence and using Fatou extends (5) to $w$.

Finally Plancherel and Tonelli yield

$$\int_{\mathbb R}\frac{\|f(\cdot+h)-f\|_2^2}{h^2}\,dh
=C\int_{\mathbb R}|\xi|\,|\widehat f(\xi)|^2\,d\xi,$$

where

$$C=\int_{\mathbb R}\frac{|e^{it}-1|^2}{t^2}\,dt\in(0,\infty).$$

The constant is finite since the integrand is bounded near zero and at most $4/t^2$ away from zero; scaling $t=\xi h$ proves the identity. This proves (4). $\square$

**Lemma 4.** For a measurable set $E\subset[0,1]$, if $f=\mathbf1_E$ satisfies (4), then $|E|=0$.

**Proof.** Let $0<h<1$ and $N=\lceil2/h\rceil$. The supports of $f$ and $f(\cdot+Nh)$ are disjoint up to a null set, so

$$2|E|=\|f(\cdot+Nh)-f\|_1
\le N\|f(\cdot+h)-f\|_1.$$

This is the triangle inequality applied to $N$ successive translations. Since $N\le3/h$ and characteristic-function differences have square equal to their absolute value,

$$\|f(\cdot+h)-f\|_2^2=\|f(\cdot+h)-f\|_1\ge\tfrac23|E|h.$$

The part of the integral (4) over $0<h<1$ is therefore at least

$$\tfrac23|E|\int_0^1\frac{dh}{h},$$

which is infinite unless $|E|=0$. $\square$

Applied to (3), Lemmas 3 and 4 prove:

$$\rho\in L^2(\mathbb R^2)\cap\operatorname{Adm}(\Gamma(E,F))\quad\Longrightarrow\quad |E|=0. \tag{6}$$

Length zero is an intermediate conclusion, not the theorem's hypothesis and not a substitute for its positive-capacity hypothesis.

## 4 The length-zero case by small-circle concatenation

**Lemma 5.** Let $E\subset[0,1]$ have length zero. Suppose $\rho\in L^2(\mathbb R^2)$ is Borel and admissible for $\Gamma(E,\mathbb R\setminus E)$. Put $q=\rho+\mathbf1_{B(0,3)}$. Then every curve $\gamma\in\Gamma(E,S_2)$ satisfies

$$\int_\gamma q\,ds=\infty. \tag{7}$$

**Proof.** The augmented density $q$ is Borel, belongs to $L^2(\mathbb R^2)$, and is still admissible for $\Gamma(E,F)$ because $q\ge\rho$. Suppose one $\gamma\in\Gamma(E,S_2)$ has finite $q$-length. Orient it from $e\in E$ and stop at its first hit of $S_2$. Before that hit its image is in $B(0,2)$, where $q\ge1$, so this initial curve has finite Euclidean length, including its endpoints. Reparameterize it by arclength as $\gamma:[0,L]\to\overline{B(0,2)}$, omitting constant portions. Its other endpoint has distance at least $1$ from $e$. We use circles centered at this particular $e$; no exceptional set of endpoints is discarded.

For almost every $r>0$, put

$$A(r)=\int_{|z-e|=r}q(z)^2\,ds.$$

Polar integration gives $\int_0^\delta A(r)\,dr<\infty$ for every finite $\delta$. Also $e+r\notin E$ for almost every $r>0$, since $E$ has length zero. Hence there is a sequence $r_j\downarrow0$, with $r_j<1$, such that

$$e+r_j\notin E,\qquad r_j A(r_j)\longrightarrow0. \tag{8}$$

Indeed, if $rA(r)$ were bounded below by a positive constant for almost every sufficiently small good radius, then $\int A(r)\,dr$ would dominate a positive multiple of $\int dr/r$. Equivalently, for every $\varepsilon,\delta>0$ some good $0<r<\delta$ has $rA(r)<\varepsilon$; choose the sequence recursively. Removing the null set of bad radii does not alter the divergent integral of $1/r$.

Let $p_j$ be the first point where $\gamma$ exits the open disk $B(e,r_j)$, and let $\gamma_j$ be its initial portion from $e$ to $p_j$. Then

$$\int_{\gamma_j}q\,ds\longrightarrow0. \tag{9}$$

Indeed, the first-exit arclength parameters $t_j$ tend to zero. For every $t>0$, the arclength-parameterized curve is nonconstant on $[0,t]$, so some point of that initial portion has positive distance from $e$; every smaller disk is exited before $t$. Since $q\circ\gamma$ is integrable on $[0,L]$, absolute continuity of the Lebesgue integral gives $\int_0^{t_j}q(\gamma(s))\,ds\to0$.

Join $p_j$ to the real point $e+r_j\in F$ along either circular arc on $|z-e|=r_j$. By Cauchy-Schwarz the $q$-length of that arc is at most the length integral over the full circle, which satisfies

$$\int_{|z-e|=r_j}q\,ds\le\sqrt{2\pi r_j A(r_j)}\longrightarrow0. \tag{10}$$

Concatenate $\gamma_j$ with this arc. It is a globally rectifiable curve from $E$ to $F$, because both pieces are rectifiable. Equations (9) and (10) make the total $q$-length tend to zero. For large $j$ it is less than $1$, contradicting admissibility. This proves (7). $\square$

## 5 Conclusion

If $E$ is empty, its modulus to $S_2$ is zero. Otherwise suppose

$$M_2(\Gamma(E,F))<\infty.$$

By the definition of the infimum there is an admissible Borel $\rho$ with finite $L^2$ energy. Sections 1 through 3 show $|E|=0$. Set $q=\rho+\mathbf1_{B(0,3)}\in L^2(\mathbb R^2)$. Lemma 5 proves that every curve of $\Gamma(E,S_2)$ has infinite $q$-length. In particular, for each positive integer $n$, $q/n$ is admissible for the entire family $\Gamma(E,S_2)$, with no exceptional curves removed. Curves that have infinite augmented length are included, rather than discarded as exceptions. Therefore

$$0\le M_2(\Gamma(E,S_2))\le\frac{1}{n^2}\int_{\mathbb R^2}q^2\,dA.$$

Letting $n\to\infty$ proves $M_2(\Gamma(E,S_2))=0$. This is the contrapositive of the theorem. $\square$

## Scope and dependencies

- The proof uses the entire stated connecting-curve families. Compactness of the auxiliary path class is used only to make the separating potential measurable; it does not restrict the final modulus family.
- The only potential constructed is confined to a fixed rectangle, and its plate values are pointwise consequences of admissibility. No touching-plate condenser theorem is invoked.
- The trace calculation establishes only the length-zero conclusion. The positive-capacity, length-zero case is handled by Lemma 5 and the definition of modulus itself.
- The analytic ingredients used without a new foundational proof are Lebesgue outer regularity, Fubini and Tonelli, Cauchy-Schwarz, the fundamental theorem for absolutely continuous functions, Arzela-Ascoli, mollification in Euclidean Sobolev spaces, and the Plancherel theorem. All problem-specific implications, the weighted-distance measurability, and the trace seminorm estimate are proved above.
- No numerical experiment, source-author code, machine-generated test outcome, or finite example is used as proof of the theorem.

## Source

[HL] Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, 21 September 2018, Problem 7.58, printed p. 178, PDF p. 179. Public record: <https://arxiv.org/abs/1809.07200>. Public HTML formulation: <https://arxiv.org/html/1809.07200v2>. The source gives the question and its attribution; the proof in this document is authored here. The source's report of no progress is a historical statement, not evidence of present worldwide openness.
