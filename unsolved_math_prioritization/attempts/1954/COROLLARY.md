# Harmonic sparsity for the integer dilation separation condition

**Review scope.** This AI-assisted authored application and its independent internal AI audit are unrefereed. “Accepted” means only that the stated harmonic corollary follows from the explicitly imported theorem of Koukoulopoulos, Lamzouri and Lichtman. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, or current worldwide open-status certification is claimed. The imported research theorem is not independently reproved. Scholarly-source retrieval and inspection statements describe the recorded audit; edition preparation performed no new scholarly-source retrieval or inspection.

## Result and attribution

Let \(A\subset(1,\infty)\) satisfy
\[
 |kx-y|\geq 1\qquad
 (x,y\in A,\ x\ne y,\ k\in\mathbb Z_{\geq1}). \tag{S}
\]
Then
\[
 H_A(X):=\sum_{x\in A,\ x\leq X}\frac1x=o(\log X)
 \qquad(X\longrightarrow\infty). \tag{C}
\]
Consequently, \(\sum_{x\in A,\ x<n}1/x=o(\log n)\) as integer \(n\to\infty\).

This is a prior corollary of Koukoulopoulos, Lamzouri and Lichtman (2025), not a new result. It supplies the harmonic alternative in Erdős Problem 143. The argument below proves every elementary step of that application. Its one non-elementary input is stated explicitly and imported; the GCD-graph theorem is not reproved here.

## The imported theorem

Write \(H_B(X)=\sum_{b\in B\cap[1,X]}1/b\). Theorem 1 of [KLL25], p. 2, states the following implication for a discrete set \(B\subset\mathbb R_{>0}\):
\[
 \limsup_{X\to\infty}\frac{H_B(X)}{\log X}>0
 \quad\Longrightarrow\quad
 \text{for each }\varepsilon>0\text{ there are }u\ne v\in B,
 \ k\in\mathbb Z_{\geq1},\ |ku-v|<\varepsilon.
 \tag{KLL}
\]
Here the authors use “discrete” in the strong sense of having no accumulation point in \(\mathbb R\), as specified on p. 1. We use precisely that formulation. No assumption about rationality, irrational ratios or integer-valued elements occurs in (KLL).

## Proof of the corollary

1. **Separation and local finiteness.** Taking \(k=1\) in (S) gives \(|x-y|\geq1\) for distinct elements. Each interval \([m,m+1)\), \(m\in\mathbb Z_{\geq1}\), therefore contains at most one element of \(A\). Since these intervals cover \((1,\infty)\), the set is at most countable. Every bounded interval meets only finitely many of them and hence contains finitely many elements of \(A\). More directly, the interval \((z-1/3,z+1/3)\) contains at most one element of \(A\) for every \(z\in\mathbb R\). Thus no real number can be an accumulation point. This verifies the exact discreteness assumption in (KLL), including possible accumulation at the endpoint 1.

2. **The sum and its normalization.** For \(X>1\), local finiteness makes \(H_A(X)\) a finite nonnegative sum. Since \(A\subset(1,\infty)\), the indexing sets \(A\cap[1,X]\) and \(\{x\in A:x\leq X\}\) agree exactly. The half-open unit intervals also give
   \[
    0\leq H_A(X)\leq\sum_{m=1}^{\lfloor X\rfloor}\frac1m
    \leq1+\log X.
   \]
   In particular \(q(X):=H_A(X)/\log X\) is nonnegative, and its limit superior at infinity is finite. We use the natural logarithm. Changing to any fixed logarithm base greater than 1 only multiplies this ratio by a positive constant, so it changes neither positivity nor a zero limit.

3. **Contradiction at the exact threshold.** If (C) failed, nonnegativity would give \(\limsup_{X\to\infty}q(X)>0\): indeed, failure of convergence to zero means that some \(\delta>0\) is attained as a lower bound for \(q(X)\) along an unbounded sequence of \(X\)'s. Apply (KLL) to \(B=A\) and \(\varepsilon=1\). Step 1 verifies discreteness, the domain is positive real numbers, and the contradiction assumption is exactly the theorem's density hypothesis. We obtain distinct \(u,v\in A\) and a positive integer \(k\) satisfying \(|ku-v|<1\). Condition (S), applied to that ordered pair and that same \(k\), instead gives \(|ku-v|\geq1\). This contradiction proves (C). Equality at distance 1 is allowed by (S) and causes no difficulty because the theorem yields a strict inequality.

4. **The endpoint in the recorded alternative.** For every integer \(n>1\),
   \[
    0\leq H_A(n)-\sum_{x\in A,\ x<n}\frac1x
      =\frac{\mathbf 1_{\{n\in A\}}}{n}\leq\frac1n.
   \]
   Dividing by \(\log n\) proves the asserted strict-cutoff version. The limit in (C) was proved for all real \(X\to\infty\), so restricting to integer \(n\) is legitimate. This completes the proof, with (KLL) as the named external input.

## Exact boundary of the conclusion

The proof does not establish
\[
 \sum_{x\in A}\frac1{x\log x}<\infty. \tag{W}
\]
There is no issue of infinitely many terms accumulating near 1: (S) allows at most one element in \((1,2)\), and its contribution to (W), if present, is a finite real number.

For clarity about the logical gap, set \(F(t)=\sum_{x\in A,\ 2\leq x\leq t}1/x\). Finite-sum summation by parts yields, for \(X\geq2\),
\[
 \sum_{x\in A,\ 2\leq x\leq X}\frac1{x\log x}
   =\frac{F(X)}{\log X}
     +\int_2^X\frac{F(t)}{t(\log t)^2}\,dt. \tag{P}
\]
One may verify (P) term by term: the contribution of a fixed \(x\leq X\) on the right is
\(1/(x\log X)+(1/x)\int_x^Xdt/(t(\log t)^2)=1/(x\log x)\).
The proved estimate gives \(F(t)=o(\log t)\). It does not bound the integral in (P) as \(X\to\infty\); in general a nonnegative integrand that is \(o(1/(t\log t))\) need not be integrable. This identifies an inference that is unavailable, rather than proposing a counterexample satisfying (S) or a method for the remaining question. No weighted-convergence attempt is made here.

## Reference

[KLL25] Dimitris Koukoulopoulos, Youness Lamzouri and Jared Duker Lichtman, *Erdős's integer dilation approximation problem and GCD graphs*, arXiv:2502.09539v1, submitted 13 February 2025. [Versioned record](https://arxiv.org/abs/2502.09539v1), [complete PDF](https://arxiv.org/pdf/2502.09539v1). Theorem 1 is on printed/PDF p. 2; the discreteness convention is on p. 1. These are the sources of the imported theorem, not a claim of its independent reproof.
