# Reduced length and Mahler measure: a published resolution

Problem 30000750 / OWR-1537-002. Verification date: 2026-10-04.

## Conclusion and attribution

The answer is **yes**. The complete assertion follows from Edward Dobrowolski's 2012 theorem. The appropriate classification is **already_solved**, not a new solution. This note gives the complete deduction for the exact real-coefficient reduced-length question, including arbitrary multiplier degree and the endpoints of the parameter interval.

## Exact assertion and conventions

For a polynomial $F(x)=\sum_{j=0}^d a_jx^j$, put

\[
L(F)=\sum_{j=0}^d|a_j|.
\]

For nonzero $F=a_d\prod_{j=1}^d(x-\alpha_j)$, define the multiplicative Mahler measure

\[
M(F)=|a_d|\prod_{j=1}^d\max\{1,|\alpha_j|\}.
\]

Empty products have value 1. Thus $M(c)=|c|$ for constants $c\ne0$. Extend the convention by $M(0)=0$. The real reduced length is

\[
\ell_{\mathbb R}(F)=\inf\{L(FQ):Q\in\mathbb R[x]\text{ is monic}\}.
\]

The degree-zero monic polynomial $Q=1$ is allowed. We prove that, for every real $t\in[-2,2]$ and every $P\in\mathbb R[x]$,

\[
\ell_{\mathbb R}((x^2+tx+1)P)\ge 2M(P).
\tag{T}
\]

Schinzel posed (T) on printed page 1136 of Oberwolfach Report 21/2007, in “The reduced length of a polynomial, revisited.” [Original report](https://ems.press/content/serial-article-files/46108), [DOI](https://doi.org/10.4171/owr/2007/21).

## Published input

Dobrowolski's Theorem 2.1 states that a nonzero complex polynomial $F$ with a zero of modulus 1 satisfies

\[
L(F)\ge 2M(F).\tag{D}
\]

Reference: E. Dobrowolski, “On a question of Schinzel about the length and Mahler's measure of polynomials that have a zero on the unit circle,” *Acta Arithmetica* **155** (2012), no. 4, 453–463, Theorem 2.1 on p. 454. [DOI](https://doi.org/10.4064/aa155-4-8); [publisher PDF](https://www.impan.pl/shop/en/publication/transaction/download/product/82795).

We use (D) as an established external theorem. We do not claim a new proof of that theorem. Its field is $\mathbb C$, which includes every real polynomial used below.

## Complete deduction

Write $A_t(x)=x^2+tx+1$. If $-2<t<2$, its two zeros are

\[
\alpha_\pm=\frac{-t\pm i\sqrt{4-t^2}}{2},\qquad
|\alpha_\pm|^2=\frac{t^2+(4-t^2)}4=1.
\]

At $t=-2$, $A_t=(x-1)^2$; at $t=2$, $A_t=(x+1)^2$. Thus in every case $A_t$ is monic and both zeros have modulus 1, counting multiplicity. In particular,

\[
M(A_t)=1.\tag{1}
\]

Mahler measure is multiplicative: $M(UV)=M(U)M(V)$ for nonzero polynomials $U,V$. Indeed, their leading coefficients multiply and the multiset of zeros of their product is the union of their zero multisets. Also, if $Q$ is monic, the defining root product gives

\[
M(Q)=\prod_\beta\max\{1,|\beta|\}\ge1,\tag{2}
\]

including $Q=1$.

Now fix $P\ne0$ and an arbitrary monic $Q\in\mathbb R[x]$. The nonzero product $F=A_tPQ$ retains the unit-circle zeros of $A_t$; multiplying polynomials cannot cancel those zeros. Applying (D), multiplicativity, (1), and (2) yields

\[
L(A_tPQ)\ge2M(A_tPQ)
=2M(A_t)M(P)M(Q)
=2M(P)M(Q)\ge2M(P).
\]

The right-hand side does not depend on $Q$. Every member of the nonempty set over which the reduced length is defined has this lower bound, so its infimum has the same lower bound. This proves (T). No minimizing multiplier or bound on its degree is assumed. If $P=0$, then $L(A_tPQ)=0$ for all $Q$, so both sides of (T) are zero. ∎

## Sharpness and exact scope

The universal constant 2 cannot be increased: take $t=0$, $P=cx^m$, where $m\ge0$ and $c\ne0$. The choice $Q=1$ gives $L((x^2+1)cx^m)=2|c|=2M(P)$, while (T) gives the matching lower bound. Hence the reduced length equals $2M(P)$ in this family.

This settles the inequality only. It does not assert a formula for reduced length of every cubic, and it does not solve the separate computation question discussed immediately before Schinzel's problem.
