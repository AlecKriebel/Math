# Turn 1: structural reduction and rational-ratio subfamilies

Problem: 4700011, Gasull Problem 11. Date: 2026-10-07.

## Status and scope

This is an authored partial result, not a solution of the full classification problem. In particular, it does not exclude inhomogeneous even-order examples with several active numerator coefficients, or the remaining irrational-ratio cases. None of the arguments below is asserted to be new to the literature.

The primary formulation uses a least **common global period**: the shift map on the positive orthant has finite order. Individual initial conditions can have smaller least periods. For example, every displayed classical family has positive fixed initial conditions. Reading the catalog as requiring the same least period for every initial condition would change the problem.

Primary source: Armengol Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, equations (12)–(13), Problem 11, https://arxiv.org/abs/2012.02524 and https://arxiv.org/html/2012.02524v1 . The paper records classification for orders 1, 2, 3, 4, 5, 7, 9, and 11 and cites Cima–Gasull–Mañosas, *On periodic rational difference equations of order k*, J. Difference Equations Appl. 10 (2004), 549–559, https://doi.org/10.1080/10236190410001667977 . The latter bibliographic record and abstract were checked at https://portalrecerca.uab.cat/en/publications/on-periodic-rational-difference-equations-of-order-k/ ; its full proof has not been inspected here.

## 1. Setup

Write the original recurrence as

\[
x_{n+k}=f(x_n,\ldots,x_{n+k-1}),\qquad
f(x_0,\ldots,x_{k-1})=
\frac{A_0+\sum_{i=1}^k A_i x_{i-1}}
 {B_0+\sum_{i=1}^k B_i x_{i-1}},
\]

with all coefficients nonnegative, both coefficient sums positive, and \(A_1+B_1>0\). Its shift map is

\[
F(x_0,\ldots,x_{k-1})=(x_1,\ldots,x_{k-1},f(x_0,\ldots,x_{k-1})).
\]

Assume throughout that \(F^p=\mathrm{id}\) on \((0,\infty)^k\) for some positive integer \(p\). In particular, \(F\) is bijective and its derivative at a fixed point has finite order.

## 2. Surjectivity removes mixed numerator–denominator candidates

**Lemma 1.** The recurrence is in exactly one of the following two forms:

\[
\tag{I}x_{n+k}=\frac{c x_n}{b_0+\sum_{j=1}^{k-1} b_j x_{n+j}},
\quad c>0,
\]

or

\[
\tag{II}x_{n+k}=\frac{a_0+\sum_{j=1}^{k-1}a_jx_{n+j}}{x_n},
\quad a_j\geq0,\quad \sum_{j=0}^{k-1}a_j>0.
\]

In (I), the denominator coefficients are nonnegative and not all zero.

*Proof.* Fix arbitrary positive \(y=(x_1,\ldots,x_{k-1})\). Surjectivity of \(F\) implies that

\[
t\longmapsto\frac{A_1t+N(y)}{B_1t+D(y)}
\]

maps \((0,\infty)\) onto \((0,\infty)\). Here \(N,D\) are affine forms with nonnegative coefficients. A constant fractional-linear function is not onto. A nonconstant such function is strictly monotone, so its endpoint limits must be 0 and \(+\infty\), in some order.

For increasing orientation, the limit at zero is 0 and the limit at infinity is infinite. This forces \(N(y)=0\), \(B_1=0\), \(A_1>0\), and \(D(y)>0\). An affine form with nonnegative coefficients vanishing at a positive point vanishes identically. Therefore the numerator is precisely \(A_1t\), giving (I).

For decreasing orientation, the limit at zero is infinite and that at infinity is 0. This forces \(D(y)=0\), \(A_1=0\), \(B_1>0\), and \(N(y)>0\). Hence all coefficients of \(D\) vanish. Divide numerator and denominator by \(B_1\) to obtain (II). These cases exhaust all possibilities. \(\square\)

This argument also excludes apparent order reduction caused by proportional numerator and denominator.

## 3. Complete exclusion of the increasing branch

**Proposition 2.** A globally periodic recurrence of form (I) is exactly

\[
x_{n+k}=x_n.
\]

*Proof.* Put \(b=\sum_{j=1}^{k-1}b_j\). If \(b=0\), the recurrence is \(x_{n+k}=r x_n\) for \(r=c/b_0>0\). Since every sequence is \(p\)-periodic, iterating \(p\) times in steps of \(k\) gives \(x_{n+pk}=r^p x_n=x_n\), so \(r=1\).

Suppose \(b>0\). If \(c\leq b_0\), every positive solution satisfies \(x_{n+k}<x_n\). Iterating this strict inequality \(p\) times contradicts \(x_{n+pk}=x_n\). Thus \(c>b_0\), and

\[
q=\frac{c-b_0}{b}>0
\]

produces a diagonal fixed point \((q,\ldots,q)\). At this fixed point, the last row of the derivative is

\[
(1,-c_1,\ldots,-c_{k-1}),\qquad c_j=\frac{q b_j}{c}\geq0.
\]

The characteristic polynomial is

\[
P(t)=t^k+\sum_{j=1}^{k-1}c_jt^j-1.
\]

It satisfies \(P(0)=-1\) and \(P(1)=\sum c_j>0\), so it has a real root in \((0,1)\). But \((DF(q,\ldots,q))^p=I\), and every eigenvalue of a finite-order matrix has modulus one. This contradiction proves \(b=0\). \(\square\)

Thus the sole increasing family is an index dilation of the identity.

## 4. Coefficient symmetry in the decreasing branch

For (II), set \(S=\sum_{j=1}^{k-1}a_j\). There is a unique positive solution

\[
q=\frac{S+\sqrt{S^2+4a_0}}2
\]

to \(q^2=a_0+Sq\); the excluded zero-numerator case is the only case where this formula could be zero. The diagonal point \((q,\ldots,q)\) is fixed.

**Lemma 3.** Every globally periodic recurrence of form (II) satisfies

\[
\tag{1}a_j=a_{k-j}\quad (1\leq j\leq k-1).
\]

*Proof.* At the diagonal fixed point, the companion derivative has characteristic polynomial

\[
\tag{2}P(t)=t^k-\sum_{j=1}^{k-1}\frac{a_j}{q}t^j+1.
\]

Its roots are roots of unity. Because \(P\) is real, its roots are closed under complex conjugation. On the unit circle, conjugation equals inversion. Consequently the monic reciprocal polynomial \(t^kP(1/t)\) has the same multiset of roots as \(P\). Both are monic, so they agree. Comparing coefficients proves (1). \(\square\)

**Corollary 4.** If \(S=0\), the recurrence is a rescaled index dilation of \(x_{n+1}=1/x_n\). If \(a_0=0\) and precisely one \(a_j\) is positive, then \(k=2\ell\), that index is \(j=\ell\), and the recurrence is a rescaled index dilation of \(x_{n+2}=x_{n+1}/x_n\).

*Proof.* The first statement follows by scaling by \(\sqrt{a_0}\). For the second, symmetry forces the sole support index to equal \(k/2\). Scaling by its positive coefficient gives the stated recurrence. \(\square\)

## 5. All homogeneous rational-ratio cases

The phrase **rational coefficient ratios** means that the ratios among the nonzero variable coefficients \(a_j\), \(j\geq1\), are rational. Their common scale need not be rational. The constant \(a_0\) is not included in this assumption.

**Theorem 5.** If \(a_0=0\) and the positive variable coefficients have rational ratios, global periodicity forces the six-period family in Corollary 4.

*Proof.* Now \(S>0\), \(q=S\), and all \(c_j=a_j/S\) are rational, nonnegative, and sum to 1. The polynomial (2) is monic with roots of unity. Its coefficients are algebraic integers, being elementary symmetric functions of algebraic integers. A rational algebraic integer is an integer. Therefore every \(c_j\) is an integer. Nonnegativity and \(\sum c_j=1\) imply that exactly one is 1 and the rest are 0. Apply Corollary 4. \(\square\)

This theorem covers every order, but does not cover arbitrary irrational ratios in even order.

## 6. A two-cycle obstruction in every odd order

Suppose \(k=2m+1\geq3\), \(S>0\), and (1) holds. Define

\[
h=\sum_{r=1}^{m}a_{2r}=\sum_{r=0}^{m-1}a_{2r+1}=S/2>0,
\]

where equality follows because reflection \(j\mapsto k-j\) interchanges parity. Define polynomials

\[
E(t)=\sum_{r=1}^{m}a_{2r}t^r,\qquad
O(t)=\sum_{r=0}^{m-1}a_{2r+1}t^r,
\]

and

\[
H(t)=t^{m+1}O(t)-E(t),\qquad C(t)=E(t)^2-tO(t)^2.
\]

**Theorem 6.** Global periodicity implies both

\[
\tag{3}h C(t)=a_0 H(t)
\]

and that every root of the monic polynomial

\[
\tag{4}Q(t)=t^k-1-\frac{H(t)}h
\]

is a root of unity.

*Proof.* An alternating sequence \(u,v,u,v,\ldots\) solves (II) precisely when

\[
\tag{5}uv=a_0+h(u+v).
\]

There is a continuous positive family: choose \(u>h\) and set

\[
v=h+\frac{a_0+h^2}{u-h}>h.
\]

These are fixed points of \(F^2\). Write \(s=u+v\), which ranges through a nondegenerate interval and is unbounded.

The linearized scalar recurrence along such a two-cycle is

\[
u_n\delta_{n+k}=-u_{n+k}\delta_n+
\sum_{j=1}^{k-1}a_j\delta_{n+j},
\]

where \(u_{2r}=u\) and \(u_{2r+1}=v\). A Floquet mode with multiplier \(t\ne0\) has

\[
\delta_{2r}=U t^r,\qquad \delta_{2r+1}=Vt^r.
\]

The two parity equations become

\[
\begin{pmatrix}
v-E(t)&ut^m-O(t)\\
vt^{m+1}-tO(t)&u-E(t)
\end{pmatrix}
\begin{pmatrix}U\\V\end{pmatrix}=0.
\]

The determinant equals

\[
uv(1-t^k)+sH(t)+C(t).
\]

Hence the monic degree-\(k\) polynomial

\[
\tag{6}Q_s(t)=t^k-1-\frac{sH(t)+C(t)}{a_0+hs}
\]

has all its roots among the eigenvalues of \(D(F^2)\) at the alternating point: a nonzero null vector \((U,V)\) gives a nonzero initial perturbation and its shift by two places multiplies it by \(t\). The constant term is \(-1\), so zero is not a root. This argument does not require the roots to be simple.

Since \((F^2)^p=\mathrm{id}\), all those eigenvalues belong to the finite set of \(p\)-th roots of unity. A monic degree-\(k\) polynomial whose roots lie in a fixed finite set has only finitely many possibilities, even allowing repeated roots. The coefficients of \(Q_s\) vary continuously with \(s\); consequently \(Q_s\) is constant on the interval of attainable \(s\).

Differentiating its variable rational part gives

\[
0=\frac{a_0H(t)-hC(t)}{(a_0+hs)^2},
\]

which is (3). Substitution of (3) into (6) yields exactly (4), whose roots remain roots of unity. \(\square\)

**Corollary 7.** In every odd order, a homogeneous recurrence of form (II) with \(S>0\) cannot be globally periodic, without any rationality assumption.

*Proof.* If \(a_0=0\), (3) gives \(E(t)^2=tO(t)^2\). Both \(E\) and \(O\) are nonzero because \(E(1)=O(1)=h>0\). The order of vanishing at zero of the left side is even, whereas that of the right side is odd. This is impossible. \(\square\)

## 7. Complete odd-order classification with rational variable-coefficient ratios

**Theorem 8.** Suppose the original recurrence is globally periodic, \(k\) is odd, and, after the reduction of Lemma 1, its positive variable numerator coefficients have rational ratios. Then it is equivalent to one of:

- \(x_{n+k}=x_n\);
- \(x_{n+k}=a_0/x_n\), with \(a_0>0\);
- for \(k=3\ell\),
  \[
  x_{n+3\ell}=\frac{b^2+b x_{n+\ell}+b x_{n+2\ell}}{x_n},\quad b>0.
  \]

The last family is precisely a rescaled index dilation of the classical order-three eight-period recurrence. In this case \(\ell\) is odd.

*Proof.* The increasing case is Proposition 2. In the decreasing case, \(S=0\) gives the reciprocal family. Assume \(S>0\). The coefficients \(a_j/h\) are rational. Theorem 6 gives a monic rational polynomial \(Q\) with roots of unity; therefore \(Q\in\mathbb Z[t]\).

The terms of \(E\) occupy degrees 1 through \(m\), and those of \(t^{m+1}O\) occupy degrees \(m+1\) through \(2m\). They do not overlap. Thus each \(a_j/h\) is an integer. The even-indexed coefficients sum to \(h\), and so do the odd-indexed coefficients. Consequently exactly one even-indexed coefficient and exactly one odd-indexed coefficient are nonzero; both equal \(h\).

Let the even support index be \(e=2r\), and write the odd support index as \(o=2s+1\). Symmetry implies \(e+o=k\), hence \(r+s=m\). Then

\[
E=h t^r,\qquad O=h t^s.
\]

By Corollary 7, \(a_0>0\). Equation (3), after cancelling \(h\), becomes

\[
\tag{7}h^2(t^{2r}-t^{k-2r})=a_0(t^{k-r}-t^r).
\]

The two exponents on either side are distinct because \(k\) is odd. Comparing the unique positive-coefficient monomials gives \(2r=k-r\), so \(k=3r\). Comparing their coefficients gives \(a_0=h^2\). The negative-coefficient terms then agree automatically. Thus the support indices are \(r\) and \(2r\), as claimed. Scaling \(x_n=h y_n\) yields the normalized classical recurrence. \(\square\)

For \(k=3\), the rational-ratio assumption is automatic after symmetry; the above therefore independently classifies all order-three cases.

## 8. Periods and verification

For each base recurrence, direct rational substitution gives global map periods 1, 2, 6, 5, and 8. The accompanying exact symbolic verifier checks the identity iterate and checks nonidentity for every proper divisor of the displayed period.

Rescaling by a positive constant conjugates maps and preserves their order. Index dilation by \(\ell\) interlaces \(\ell\) independent base sequences and has global period multiplied by \(\ell\). To see minimality, a shift not divisible by \(\ell\) would identify quantities belonging to independent residue classes; arbitrary positive initial data preclude that. For a shift divisible by \(\ell\), minimality reduces to the base map's order.

Computational checks are consistency tests only. The proofs of Lemmas 1 and 3, Propositions 2, Theorems 5, 6, and 8, and Corollary 7 are the mathematical arguments above, not consequences of a finite search.

## 9. Exact remaining gap and next direction

The full problem permits arbitrary nonnegative real coefficients. The reduction leaves

\[
x_{n+k}=\frac{a_0+\sum_{j=1}^{k-1}a_jx_{n+j}}{x_n},\qquad a_j=a_{k-j},
\]

subject to root-of-unity spectra and nonlinear periodicity identities. We have not proved that the ratios \(a_i/a_j\) must be rational. Nor have we classified all even-order inhomogeneous candidates, even under rational-ratio hypotheses.

A concrete next author turn should examine even order 6, the first order not settled in the cited source, with normalized palindromic numerator

\[
a_0+b(x_{n+1}+x_{n+5})+c(x_{n+2}+x_{n+4})+d x_{n+3}.
\]

It should derive finite-order constraints from its higher-period positive points or nonlinear jets, rather than treat unit-circle eigenvalues alone as sufficient. In parallel, the odd-order identity (3) can be analyzed without the rational-ratio shortcut; irrational solutions of that necessary identity must still pass the root-of-unity test (4) and the full nonlinear identity. No claim of a new example, exhaustive real-coefficient classification, or final campaign failure is made here.
