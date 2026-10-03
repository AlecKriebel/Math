# Affirmative solution by a published weighted-coefficient theorem

## Exact target

Let D be the open unit disk and let

\[
f(z)=z+\sum_{n\ge1}c_{2n+1}z^{2n+1}
\]

be analytic, odd, and one-to-one in D. Put c_1=1 and

\[
d_n=|c_{2n+1}|-|c_{2n-1}|,\qquad
\beta_0=(\sqrt2-1)^2=3-2\sqrt2>0.
\]

Problem 6.38 asks whether \(\sum_{n\ge1}n^{-\beta_0}d_n^2\) is finite. This is a question about squared differences of coefficient moduli, not complex coefficient differences. No maximal-growth hypothesis occurs in the question.

## Published input and deduction

V. I. Milin, *Adjacent coefficients of odd univalent functions*, Siberian Mathematical Journal 22 (1981), 283–290, [DOI 10.1007/BF00968424](https://doi.org/10.1007/BF00968424), proves the following. In the Russian original, this is Theorem 2, equation (30), pp. 153–154; [Math-Net record](https://www.mathnet.ru/eng/smj6431).

For a normalized odd univalent function \(f_2(z)=\sum_{k\ge0}b_kz^{2k+1}\), with \(b_0=1\), there is an absolute constant A<50 such that every nonnegative, nonincreasing summable sequence \((\alpha_k)_{k\ge1}\) satisfies

\[
\sum_{k\ge1}\alpha_k k(|b_k|-|b_{k-1}|)^2
\le A\sum_{k\ge1}\alpha_k. \tag{M}
\]

Apply (M) with \(b_k=c_{2k+1}\) and \(\alpha_k=k^{-1-\beta_0}\). The index k=0 gives precisely b_0=c_1=1. Since \(\beta_0>0\), the sequence is nonnegative and decreasing, and

\[
\sum_{k\ge1}\alpha_k
\le 1+\int_1^\infty x^{-1-\beta_0}\,dx
=1+\frac1{\beta_0}<\infty.
\]

Thus

\[
\boxed{\quad
\sum_{k\ge1} k^{-\beta_0}d_k^2
\le A\sum_{k\ge1}k^{-1-\beta_0}<\infty.
\quad}
\]

Indeed the same argument works for every exponent \(\varepsilon>0\). Milin states this directly in Corollary 1, equation (34), p. 155. The use of \(\beta\) in the 2018 update involves a factor of two: set its parameter to \(\beta_0/2\), not \(\beta_0\), to recover the exact requested weight.

This is a complete deduction from an established theorem, with its hypotheses checked. It is not a new proof of Milin's theorem. The reading and dependencies of that theorem are recorded separately.

## Endpoint check: the positivity restriction matters

The following classical example occurs in Milin's discussion. Here its admissibility and divergence are checked directly. Let

\[
f_0(z)=\frac{z}{\sqrt{1-z^4}},
\]

where the analytic square root is chosen to be 1 at zero. It exists in D since 1-z^4 has no zeros there. The function is odd and normalized. To prove univalence, write

\[
f_0(z)^2=H(z^2),\qquad H(w)=\frac{w}{1-w^2}.
\]

If H(u)=H(v), cross multiplication gives \((u-v)(1+uv)=0\). For u,v in D the second factor cannot vanish, so H is injective. If f_0(z)=f_0(w), it follows that z^2=w^2. The alternative w=-z, combined with oddness, forces f_0(z)=0 and hence z=w=0. Therefore f_0 is univalent.

Set \(a_m=4^{-m}\binom{2m}{m}\). The binomial expansion gives

\[
b_{2m}=a_m,\qquad b_{2m+1}=0.
\]

Consequently \(d_1=-1\), \(d_{2m}=a_m\), and \(d_{2m+1}=-a_m\) for m>=1. For every m>=1,

\[
a_m^2\ge\frac1{4m}.
\]

The case m=1 is equality. For the induction step use
\(a_{m+1}/a_m=(2m+1)/(2m+2)\) and
\((2m+1)^2-4m(m+1)=1\). Hence

\[
\sum_{n\ge1}d_n^2=1+2\sum_{m\ge1}a_m^2=\infty.
\]

This confirms that the universal conclusion cannot be extended to exponent zero. It is an elementary check of a known example, not a novelty claim.
