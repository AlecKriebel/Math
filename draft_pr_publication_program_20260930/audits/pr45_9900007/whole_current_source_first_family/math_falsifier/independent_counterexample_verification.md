# Independent verification of the repeated-block counterexample

Date: 2026-10-03 UTC. Reviewer role: independent mathematical falsifier.

This note was derived from the proposed construction alone. No earlier PR45 reports, code, source files, or ROOT files were read or executed. No Git, remote, or external communication operations were performed. The scope of completion below is this independent mathematical verification, not the wider research program.

## Exact statement and assumptions

Let the time index set be the nonnegative integers. On the binary sequence space, let

\[
 h_r=2^r,\qquad a_r=s_r=2^{r+1}-2,\qquad b_r=a_r+h_r,
\]

and let all variables \(U_{r,j}\), for \(r\geq0\) and \(0\leq j<h_r\), be independent Bernoulli\((1/2)\) variables. Define

\[
 X_{a_r+j}=X_{b_r+j}=U_{r,j}.
\]

The blocks \([a_r,a_r+2h_r-1]\) partition the nonnegative integers: the next block starts at \(a_{r+1}=a_r+2h_r\). Let \(Y\) have the full law of an iid Bernoulli\((1/2)\) sequence.

Write \((\theta_n x)_k=x_{n+k}\), and use the compatible product metric

\[
 d(x,y)=\sum_{k=0}^{\infty}2^{-k-1}|x_k-y_k|.
\]

The claims verified here are:

1. \(\mathcal L(\theta_n X)\Rightarrow\mathcal L(Y)\) as \(n\to\infty\).
2. No coupling of the entire processes with these marginal laws has \(d(\theta_n X,\theta_n Y)\to0\) in probability.
3. More generally, no such coupling, augmented by any extra randomness, has \(d(\theta_{n+S}X,\theta_{n+T}Y)\to0\) in probability for fixed, almost surely finite, nonnegative integer-valued random offsets \(S,T\). The offsets may be arbitrary functions of both full paths and of the extra randomness.

Here “fixed” means that \(S,T\) do not change with \(n\). The integer-valued assumption is required for the discrete-time shifts to be defined. Almost sure convergence is also excluded by each negative convergence-in-probability result.

## Claim 1: every fixed finite window is eventually exactly iid

Fix a window length \(L\geq1\). Choose \(R\) with \(2^R\geq L\). For every \(n\geq a_R\), all coordinates of \([n,n+L-1]\) lie in blocks with labels \(r\geq R\).

Two distinct coordinates share an underlying \(U\) variable only if they are the paired positions \(a_r+j,b_r+j\) of the same block. Their separation is \(h_r\geq2^R\geq L\), which exceeds the window span \(L-1\). Thus all underlying variables appearing in the window are distinct, including when the window crosses a block boundary. Consequently

\[
 (X_n,\ldots,X_{n+L-1})\sim\operatorname{Bernoulli}(1/2)^{\otimes L}
 \quad\text{for every }n\geq a_R.
\]

This implies weak convergence on the binary product space. For completeness, given any bounded continuous \(f\), compactness of this space gives uniform continuity. Replace the coordinates after the first \(L\) by zeros to obtain \(f_L\). The replacement has distance at most \(2^{-L}\), so \(\|f-f_L\|_\infty\to0\). The expectations of \(f_L(\theta_n X)\) and \(f_L(Y)\) are exactly equal for all sufficiently large \(n\); the uniform approximation then proves the claimed weak convergence.

## Claim 2: the synchronous coupling obstruction

In every coupling with the prescribed full marginal laws, the countably many equalities \(X_{a_r+j}=X_{b_r+j}\) hold simultaneously almost surely. For a fixed pair, if \(Y_{a_r+j}\ne Y_{b_r+j}\), at least one of its endpoints disagrees with the corresponding \(X\) endpoint. Therefore

\[
 \frac12
 =\Pr(Y_{a_r+j}\ne Y_{b_r+j})
 \leq \Pr(X_{a_r+j}\ne Y_{a_r+j})
     +\Pr(X_{b_r+j}\ne Y_{b_r+j}).
\]

Taking \(j=0\), both endpoint indices tend to infinity with \(r\). Hence coordinate mismatch probabilities cannot tend to zero. In fact

\[
 \limsup_{n\to\infty}\Pr(X_n\ne Y_n)\geq\frac14.
\]

Because \(d(\theta_n X,\theta_n Y)\geq\tfrac12\mathbf1_{\{X_n\ne Y_n\}}\), product-metric convergence in probability is impossible. This argument uses no nonanticipation or independence between the coupled processes.

## Claim 3: fixed, path-dependent random offsets

Assume for contradiction that such a coupling and offsets exist. Define the unconditional mismatch probabilities

\[
 q_n=\Pr(X_{n+S}\ne Y_{n+T}).
\]

Metric convergence in probability implies \(q_n\to0\), again by the first metric coordinate. This implication is enough for the contradiction. In fact the two convergences are equivalent for fixed offsets: if \(q_n\to0\), then for any \(L\),

\[
 \Pr\bigl(d(\theta_{n+S}X,\theta_{n+T}Y)>2^{-L}\bigr)
 \leq\sum_{k=0}^{L-1}q_{n+k}\to0.
\]

Fix an arbitrary integer \(B\geq0\), and let

\[
 E_B=\{S\leq B,\ T\leq B\}.
\]

Fix an arbitrary integer \(M\geq1\). Choose

\[
 j_\ell=\ell(2B+1),\qquad 0\leq\ell<M.
\]

For all sufficiently large \(r\), these indices satisfy \(0\leq j_\ell<h_r\), and \(a_r\geq B\). Define the event \(D_r\) that at least one of the following \(2M(B+1)\) shifted-coordinate errors occurs:

\[
 \left\{X_{a_r+j_\ell-s+S}\ne Y_{a_r+j_\ell-s+T}\right\},
 \qquad
 \left\{X_{b_r+j_\ell-s+S}\ne Y_{b_r+j_\ell-s+T}\right\},
\]

where \(0\leq\ell<M\) and \(0\leq s\leq B\). Each displayed index before \(+S\) or \(+T\) is a deterministic nonnegative integer. A union bound gives

\[
 \Pr(D_r)\leq
 \sum_{\ell=0}^{M-1}\sum_{s=0}^{B}
 \left(q_{a_r+j_\ell-s}+q_{b_r+j_\ell-s}\right)\longrightarrow0
 \quad(r\to\infty),
\]

because \(B,M\) are fixed and every index in this finite sum tends to infinity.

On \(E_B\setminus D_r\), use the actual value \(s=S\) among the finitely many tested values. With \(K=T-S\in\{-B,\ldots,B\}\), absence of the errors and the repeated-block identities force

\[
 Y_{a_r+j_\ell+K}=X_{a_r+j_\ell}
 =X_{b_r+j_\ell}=Y_{b_r+j_\ell+K}
 \qquad(0\leq\ell<M).
\]

For each deterministic \(k\in\{-B,\ldots,B\}\), let \(A_{r,k}\) denote all \(M\) displayed equalities with \(K\) replaced by \(k\). For this fixed \(k\), all \(2M\) coordinates are distinct: the first endpoints lie in \([a_r+k,b_r+k-1]\), the second in \([b_r+k,a_r+2h_r+k-1]\), and the \(j_\ell\)'s are distinct. They are also nonnegative for the large \(r\) under consideration. The iid marginal law of \(Y\) therefore gives the exact unconditional probability

\[
 \Pr(A_{r,k})=2^{-M}.
\]

There is no need to condition on the random offsets. Their possible path dependence is handled by the event inclusion

\[
 E_B\setminus D_r\subseteq\bigcup_{k=-B}^{B}A_{r,k}.
\]

Consequently

\[
 \Pr(E_B)\leq\Pr(D_r)+(2B+1)2^{-M}.
\]

First let \(r\to\infty\), keeping \(B,M\) fixed. Then let \(M\to\infty\), keeping \(B\) fixed. This proves \(\Pr(E_B)=0\) for every \(B\). Finally \(E_B\uparrow\{S,T\text{ are finite}\}\) as \(B\to\infty\), whereas the latter event has probability one. This is the contradiction.

The spacing requirement \(j_{\ell+1}-j_\ell>2B\) is valid but stronger than necessary. Distinct \(j_\ell\)'s within the first half of the block suffice: no independence between different \(A_{r,k}\)'s is used in the union bound.

## Adversarial findings and precise scope

No mathematical defect was found in the three stated claims. The essential quantifier order is: fix \(B\), fix \(M\), let \(r\to\infty\); then let \(M\to\infty\); finally let \(B\to\infty\). The number of tested mismatch events depends on \(B,M\), but stays finite during the \(r\) limit. All mismatch probabilities used are unconditional. Conditioning on path-dependent offsets would not preserve iid laws and is unnecessary.

The marginal of \(Y\) must be fully iid, not merely coordinatewise fair. The offsets must be fixed in \(n\) and almost surely finite. The argument makes no claim for time-varying offsets or for arbitrary separately represented copies having only the individual shifted laws. Weak convergence of shifted laws is fully compatible with failure of a single coherent full-path coupling. Whether a particular external theorem asserts the excluded full-path coupling is outside this independent note's scope.

Verified conclusion: the proposed construction is a rigorous binary counterexample to the assertion that weak convergence of successive shifted full-path laws necessarily admits a full-path coupling with synchronous, or fixed finite randomly offset, convergence in probability in the product metric.

Completion estimate for the assigned mathematical falsification and verification task: **100%**. No unsupported mathematical gap remains in these stated claims.

Supplementary reproducible checks are preserved in `verify_indices.py`: 4,098 finite window index configurations and 1,210 offset equality index configurations passed. These are checks of indexing and boundary cases; the proofs above establish the unrestricted statements.
