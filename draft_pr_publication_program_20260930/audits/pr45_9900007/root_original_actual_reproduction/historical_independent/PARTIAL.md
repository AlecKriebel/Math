# A finite-state obstruction to synchronous weak-shift coupling

**Partial result only.** The illustrative synchronous coupling condition in Thorisson's Problem 3.3 is false, even with convergence in probability replacing almost-sure convergence. The broader request for a two-process coupling characterization is not resolved here. Historical novelty is unestablished.

## 1. Source scope and the precise claim

The [original preprint](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf), Section 3, uses one-sided processes \(X=(X_k)_{k\ge0}\) on a common state space. At Problem 3.3 the state space is separable metric, the sigma-field is Borel, and the path metric is a product metric. The question first seeks a characterization of weak convergence of shifted laws using only a joint construction of X and X'. It then proposes, as an example, a coupling with

\[
d(\theta_n X,\theta_n X')\longrightarrow0.
\tag{1}
\]

The displayed example does not explicitly specify the convergence mode. We show that (1) can fail for **every** coupling even in probability, hence also almost surely. This rejects that example, not every possible two-process characterization. No time-homogeneity, ergodicity of the limit, adaptedness or Markovian-coupling requirement appears in this general source formulation. Our limit is stationary but not ergodic.

The finite random times in the preceding distributional shift-coupling theorem are a separate condition. They are not silently inserted into (1). A bounded-in-probability finite-offset extension of the obstruction is proved in Section 5; arbitrary growing time changes are outside the claim.

## 2. Explicit process and weak convergence

Let \(E=\{-1,+1\}\) with its discrete metric. Its one-sided path space
\(S=E^{\mathbb N_0}\) is compact metrizable. Use

\[
d(x,y)=\sum_{j=0}^{\infty}2^{-j-1}\mathbf1_{\{x_j\ne y_j\}}.
\tag{2}
\]

Let \(X_0\) be a fair sign, and independently take mutually independent signs \(\xi_k\), \(k\ge0\), with

\[
\mathbb P(\xi_k=-1)=\frac1{k+2},\qquad
X_{k+1}=X_k\xi_k.
\tag{3}
\]

Every \(X_k\) is fair. Let \(\nu\) be the distribution of the constant path
\(X'=(B,B,\ldots)\), where B is a fair sign. This law is stationary.

For a window of \(r+1\) coordinates starting at n, the probability of no flip is exactly

\[
\prod_{k=n}^{n+r-1}\left(1-\frac1{k+2}\right)
=\frac{n+1}{n+r+1}.
\tag{4}
\]

The law of this window gives mass \((n+1)/(2(n+r+1))\) to each of the two constant words. All remaining words are nonconstant and have total mass \(r/(n+r+1)\). Consequently, with total variation defined as the supremum over events,

\[
\left\|\mathcal L(X_n,\ldots,X_{n+r})
-\tfrac12\delta_{(+1,\ldots,+1)}
-\tfrac12\delta_{(-1,\ldots,-1)}\right\|_{\rm TV}
=\frac r{n+r+1}\longrightarrow0.
\tag{5}
\]

This proves convergence of every finite-window law. It proves weak convergence on S as well: continuous functions on compact S are uniformly continuous and can be uniformly approximated by functions depending on finitely many coordinates, by replacing the remaining coordinates with a fixed tail. Hence

\[
\boxed{\quad\theta_nX\Rightarrow X'.\quad}
\tag{6}
\]

Only the marginal law of X' has been specified so far. The impossibility argument below permits every joint construction with X.

## 3. Why every coupling has asymptotic mismatch one half

First work with the marginal process X. Write
\(\mathcal F_m=\sigma(X_0,\ldots,X_m)\). For \(n>m\), independence of the future flips gives

\[
\mathbb E[X_n\mid\mathcal F_m]
=X_m\prod_{k=m}^{n-1}\left(1-\frac2{k+2}\right)
=X_m\frac{m(m+1)}{n(n+1)}.
\tag{7}
\]

The formula includes m=0: the product then has a zero factor.

We claim that for every bounded random variable g measurable with respect to the entire path X,

\[
\mathbb E[X_ng]\longrightarrow0.
\tag{8}
\]

Indeed, set \(g_m=\mathbb E[g\mid\mathcal F_m]\). Since the increasing sigma-fields \(\mathcal F_m\) generate \(\sigma(X)\), the conditional-expectation approximation theorem gives \(g_m\to g\) in \(L^1\). For fixed m and n>m, (7) yields

\[
\begin{aligned}
|\mathbb E[X_ng]|
&\le \mathbb E|g-g_m|
+\frac{m(m+1)}{n(n+1)}\mathbb E|g_m|.
\end{aligned}
\tag{9}
\]

First send n to infinity and then m to infinity. This proves (8). The use of finite-history approximation is essential: we do not condition the future flips on B and assume that they stay independent.

Now fix an **arbitrary coupling** of X with a process of law \(\nu\). The latter is almost surely a constant path, so it equals \((B,B,\ldots)\) for a fair sign B on this joint space. B may depend on the complete past and future of X and on extra randomness; no causality constraint is imposed. Put

\[
g=\mathbb E[B\mid\sigma(X)].
\]

This is a bounded function of the full path. Applying (8),

\[
\mathbb E[X_nB]=\mathbb E[X_ng]\longrightarrow0.
\]

For signs, \(\mathbf1_{\{X_n\ne B\}}=(1-X_nB)/2\). Thus every coupling satisfies

\[
\boxed{\quad\mathbb P(X_n\ne B)\longrightarrow\frac12.\quad}
\tag{10}
\]

Since (2) gives
\(d(\theta_nX,\theta_nX')\ge\frac12\mathbf1_{\{X_n\ne B\}}\), no coupling can make this distance converge to zero in probability. In particular, almost-sure convergence is impossible.

An elementary weaker obstruction, not needing (8), is already visible from

\[
\mathbb P(X_n\ne X_m)
=\frac12\left(1-\frac{n(n+1)}{m(m+1)}\right),\quad m>n.
\tag{11}
\]

The right side tends to 3/8 when m=2n, whereas convergence of both coordinates in probability to the same B would force it to zero. Equation (10) strengthens this to the exact limiting mismatch under every coupling.

## 4. The entire metric error has a nonzero limiting law

For an arbitrary fixed coupling, let

\[
D_n=d(\theta_nX,\theta_nX'),\qquad
I_n=\mathbf1_{\{X_n\ne B\}}.
\]

From (2), the triangle inequality for indicator differences, and the probability of at least one flip in a window,

\[
\begin{aligned}
\mathbb E|D_n-I_n|
&\le\sum_{j\ge0}2^{-j-1}\mathbb P(X_{n+j}\ne X_n)\\
&\le\sum_{j\ge0}2^{-j-1}\frac{j}{n+j+1}
\le\frac1{n+1}\sum_{j\ge0}j2^{-j-1}
=\frac1{n+1}.
\end{aligned}
\tag{12}
\]

Equations (10) and (12) prove

\[
D_n\Rightarrow\tfrac12\delta_0+\tfrac12\delta_1,
\qquad \mathbb E D_n\longrightarrow\tfrac12,
\tag{13}
\]

for every coupling. The obstruction is therefore independent of choosing almost-sure versus in-probability versus distributional convergence to the constant zero.

Changing to another metric compatible with the product topology cannot rescue convergence to zero in probability. On compact S any two compatible metrics are uniformly equivalent. Alternatively, the disjoint compact sets of pairs with different zeroth coordinates are separated from the diagonal by a positive distance for any such metric.

## 5. Finite random offsets do not remove this obstruction

Let T and T' be arbitrary almost surely finite nonnegative integer random variables on the joint space; they may depend on both processes. The shifted constant path is unchanged by T'. For any fixed M and any \(\varepsilon>0\),

\[
\begin{aligned}
&\mathbb P\{d(\theta_{n+T}X,\theta_nX)>\varepsilon\}\\
&\quad\le\mathbb P(T>M)
+\varepsilon^{-1}\sum_{s=0}^{M}\mathbb E\,d(\theta_{n+s}X,\theta_nX)\\
&\quad\le\mathbb P(T>M)
+\frac{M(M+1)}{2\varepsilon(n+1)}.
\end{aligned}
\tag{14}
\]

The last step uses the same flip bound coordinatewise: each expectation is at most \(s/(n+1)\). Send n and then M to infinity. Thus this distance tends to zero in probability, so replacing n by n+T in the first process and n+T' in the second leaves the limiting law (13) unchanged. The same estimate works for a uniformly tight family of nonnegative offsets \(T_n\), but is not a claim about arbitrary growing random time changes.

This does not conflate sample-path asymptotic closeness with the distributional equality at random times in the earlier source theorem.

## 6. What remains and what is not being claimed

This is a concrete negative answer to the **illustrative synchronous condition**. It leaves open the source's broader request for another two-process condition equivalent to weak shift convergence. A characterization using a different probabilistic relation or permitted unbounded time rearrangements has neither been proved nor ruled out here.

Ordinary Skorohod/Dudley constructions and Thorisson's finite-window density theorem couple a whole sequence of copies. Their joint law need not preserve the shift-consistency relations of a single original path X. Applying those theorems and then renaming all copies as shifts of one X would be the missing, generally false step illustrated above.

This example is not a counterexample to setwise-implies-total-variation convergence in the distinct Problem 3.1 / ID9900005. The independent flips occur infinitely often almost surely, since their probabilities have divergent sum. Thus every shifted law assigns probability zero to the invariant event of eventually constant paths, whereas \(\nu\) assigns it probability one. Setwise convergence fails. No previous result for 9900005 is revised by this artifact.

The finite checks validate equations (4), (5), (7) and (11) in modest exact cases and check the elementary mismatch inequality. They do not replace the all-couplings conditional-expectation argument or the infinite limiting arguments. One substantive construction family was used. The full target's status remains **unsolved**, with a proved partial obstruction pending separate adversarial review.
