# Exact prefix geometry for independently signed unrestricted partitions

## Scope

Let
\[
P(q)=\prod_{m\ge1}\left(1+\sum_{j\ge1}\epsilon_{m,j}q^{mj}\right),
\qquad \epsilon_{m,j}\in\{-1,1\}.
\]
Every sign is independent and every constant is 1. The desired condition is
\(|[q^n]P|\le1\) for all \(n\). This note proves exact finite-prefix reductions and a sharp obstruction to a *universal prefix-extension strategy*. It does not prove that the unrestricted problem has, or lacks, an infinite solution. No novelty claim is made.

## 1. Exact one-step continuation test

A degree-\(N\) sign prefix specifies exactly those signs with \(mj\le N\). Define its truncated factors
\[
F_m^{[N]}(q)=1+\sum_{1\le j\le N/m}\epsilon_{m,j}q^{mj},
\qquad B_N(q)=\prod_{m=1}^{N}F_m^{[N]}(q).
\]
It is feasible when all coefficients of \(B_N\) through degree \(N\) have absolute value at most 1. Let \(d(n)\) be the number of positive divisors of \(n\), and let \(p(n)\) be the ordinary partition number. Put
\[
A_n=[q^n]B_{n-1},\qquad \rho_n=p(n)\bmod2\in\{0,1\}.
\]
There are exactly \(d(n)\) fresh signs at degree \(n\), namely \(\epsilon_{m,n/m}\) for \(m\mid n\). Each contributes additively to degree \(n\), because it can only multiply constant terms there. Therefore the new coefficient is
\[
a_n=A_n+\sum_{m\mid n}\epsilon_{m,n/m}. \tag{1}
\]
Each coefficient is a sum of \(p(n)\) signed partition contributions. Consequently
\[
a_n\equiv p(n)\pmod2,\qquad A_n\equiv p(n)-d(n)\pmod2. \tag{2}
\]
In particular, the allowed coefficient is exactly 0 if \(\rho_n=0\), and either \(-1\) or 1 if \(\rho_n=1\).

**Proposition 1.** A feasible degree-\(n-1\) prefix has a feasible degree-\(n\) extension if and only if
\[
|A_n|\le d(n)+\rho_n. \tag{3}
\]
The exact number of extensions is
\[
\sum_{t\in T_n}
\binom{d(n)}{(d(n)+t-A_n)/2},\qquad
T_n=\begin{cases}\{0\},&\rho_n=0,\\\{-1,1\},&\rho_n=1,\end{cases} \tag{4}
\]
where a binomial coefficient is zero if its lower argument is nonintegral or outside \([0,d(n)]\).

Indeed the fresh sum takes all values \(-d(n),-d(n)+2,\ldots,d(n)\). Its parity is fixed, and (2) makes the parity condition in (3) automatic. Choosing the positions of the positive fresh signs gives (4). This proves both necessity and sufficiency, with no heuristic pruning.

## 2. Universal extension first fails at degree 7

It is false that every feasible prefix of the unrestricted problem can be extended. The following example is already terminal at degree 6:
\[
F_1^{[6]}=1-q-q^2-q^3-q^4+q^5+q^6,
\]
with all assigned signs in factors \(m\ge2\) positive. Exact multiplication gives
\[
([q^n]B_6)_{n=0}^{7}=(1,-1,0,-1,-1,-1,-1,-5).
\]
Thus the prefix is feasible through 6, but at degree 7 its only fresh signs are \(\epsilon_{1,7}\) and \(\epsilon_{7,1}\). The possible new coefficients are \(-7,-5,-3\), none allowed.

For a short direct check, the coefficients through degree 7 of
\(\prod_{m\ge2}(1-q^m)^{-1}\) are
\(1,0,1,1,2,2,4,4\). Multiplication by the displayed first-factor prefix gives precisely the stated numbers; truncating the other factors at degree 6 does not affect the result before 7, and removes only the still-unassigned pure term \(q^7\) from factor 7 at degree 7. Equivalently the degree-7 residual is
\(4-4-2-2-1+1+0-1=-5\), where the final subtraction removes that pure term. Direct multiplication of the truncated factors is the unambiguous definition.

Here is also a purely algebraic proof that no earlier feasible prefix is terminal. Write \(x_j=\epsilon_{1,j}\), \(y_j=\epsilon_{2,j}\), and \(z_1=\epsilon_{3,1}\). Feasibility at degree 2 gives
\(x_2+y_1=0\). The residuals at degrees 2 and 3 are 0 and \(x_1y_1\), respectively, and these pass (3). At degree 4,
\[
A_4=x_2y_1+x_1z_1=-1+x_1z_1\in\{-2,0\},
\]
which passes (3), since \(d(4)=3\) and \(p(4)=5\). At degree 5 the terms \(x_2z_1+y_1z_1\) cancel, leaving
\[
A_5=x_3y_1+x_1y_2+x_1\epsilon_{4,1},
\]
so \(|A_5|\le3=d(5)+\rho_5\). At degree 6 the two terms involving \(\epsilon_{4,1}\) cancel, leaving
\[
A_6=x_1\epsilon_{5,1}
 +z_1(x_3+x_1y_1)
 +x_2y_2+x_4y_1.
\]
The feasible degree-3 coefficient is \(a_3=x_3+z_1+x_1y_1\in\{-1,1\}\), whence
\[
z_1(x_3+x_1y_1)=z_1a_3-1\in\{-2,0\}.
\]
The other three summands are signs, so \(-5\le A_6\le3\). This passes (3), since \(d(6)=4\) and \(p(6)=11\). Degree 1 is immediate. Therefore attempted degree 7 is exactly the first place a feasible unrestricted prefix can fail to extend.

A separate exact computation enumerated the full unrestricted tree through degree 9 by direct polynomial multiplication. Its program and raw states are not distributed in this appendix. Its feasible frontier sizes at degrees 0 through 9 are
\[
1,2,4,12,60,160,1268,2848,10784,21354.
\]
There are 80 terminal degree-6 parents, 120 terminal degree-7 parents, and 1446 terminal degree-8 parents. These finite counts are diagnostics, not evidence of eventual global impossibility.

## 3. An exact linear system for the next half-prefix

Fix a feasible degree-\(M\) prefix and an integer \(N\) with
\(M<N\le2M+1\). Put \(B=B_M\). For \(1\le m\le N\), define
\[
H_m(q)=\prod_{\substack{1\le r\le M\\r\ne m}}F_r^{[M]}(q).
\]
This equals the formal quotient \(B/F_m^{[M]}\) for \(m\le M\), and equals \(B\) for \(m>M\). The quotient exists since every factor has constant 1.

The fresh index set is
\[
\mathcal I=\{(m,j):M<mj\le N\}.
\]
For signs \(u_{m,j}\in\{-1,1\}\), an expansion by the number of fresh terms gives
\[
P(q)\equiv B(q)+
\sum_{(m,j)\in\mathcal I}u_{m,j}q^{mj}H_m(q)
\pmod{q^{N+1}}. \tag{5}
\]
There is no term containing two fresh coefficients, because its degree would be at least \(2(M+1)>N\). This proves (5) even if two fresh coefficients belong to different factors; coefficients from the same factor are never multiplied in the original product anyway.

For \(M<n\le N\), set
\[
b_n=[q^n]B,\qquad
C_{n,(m,j)}=[q^{n-mj}]H_m,
\]
with negative-index coefficients understood to be zero. Then the entire block can be completed if and only if the following finite **integer** linear system has a solution:
\[
b_n+\sum_{(m,j)\in\mathcal I}C_{n,(m,j)}u_{m,j}
=\begin{cases}0,&p(n)\text{ even},\\v_n,&p(n)\text{ odd},\end{cases}
\quad u_{m,j}\in\{-1,1\},\quad v_n\in\{-1,1\}. \tag{6}
\]
Thus all nonlinearity is confined to the already-fixed lower half. There is no relaxation or sufficiency gap in (6), and no claim that a solution always exists.

**Exact column grouping.** Fix a fresh degree \(k\), and put \(L=N-k\). For every divisor \(m\mid k\) with \(m>L\),
\[
H_m\equiv B\pmod{q^{L+1}},
\]
since \(F_m^{[M]}\equiv1\pmod{q^{L+1}}\). All fresh signs at that degree with \(m>L\) therefore have identical columns in (6). If there are \(r\) such signs, they can be replaced for feasibility by a single variable with domain
\(\{-r,-r+2,\ldots,r\}\). If counting labeled assignments, a value \(s\) has multiplicity \(\binom r{(r+s)/2}\). This is an exact finite-horizon quotient. It does not identify those assignments beyond degree \(N\), where their effects can differ.

A useful but only necessary relaxation is obtained by multiplying (6) by arbitrary real weights \(w_n\), summing, and applying the triangle inequality:
\[
\left|\sum_{n=M+1}^{N}w_nb_n\right|
\le \sum_{(m,j)\in\mathcal I}
\left|\sum_{n=M+1}^{N}w_nC_{n,(m,j)}\right|
+\sum_{\substack{M<n\le N\\p(n)\text{ odd}}}|w_n|. \tag{7}
\]
A violated inequality is a valid certificate that the fixed prefix cannot extend across the block. Passing all such inequalities characterizes a real box relaxation, not generally the sign-constrained integer problem. No real relaxation is substituted for (6).

## 4. A constant-size exact two-step test

For a fixed feasible degree-\(n-1\) prefix with \(n\ge2\), put
\[
A=[q^n]B_{n-1},\qquad D=[q^{n+1}]B_{n-1},\qquad x=\epsilon_{1,1}.
\]
At degree \(n\), separate the fresh sign \(e=\epsilon_{1,n}\) from the sum
\(s=\sum_{m\mid n,\ m>1}\epsilon_{m,n/m}\). Then
\[
s\in\{-(d(n)-1),-(d(n)-1)+2,\ldots,d(n)-1\}.
\]
The degree-\(n\) coefficient is \(A+e+s\). At degree \(n+1\), a fresh term of degree \(n\) can only multiply a degree-1 term in another factor. For \(m=1\), there is no such term outside its own factor, so its contribution is zero. For every \(m>1\), that degree-1 term is \(xq\) in factor 1. Two fresh terms have degree at least \(2n>n+1\). Thus the degree-\(n+1\) residual, before its own fresh signs, is exactly
\[
D+xs.
\]
Consequently the prefix has a feasible continuation through \(n+1\) if and only if there exist \(e\in\{-1,1\}\) and a legal sum \(s\) such that
\[
|A+e+s|\le1,\qquad
|D+xs|\le d(n+1)+\rho_{n+1}. \tag{8}
\]
For each permitted degree-\(n\) coefficient \(t\in T_n\), one need only test
\(s=t-A-e\). There are at most four candidate pairs \((t,e)\), regardless of the number of divisors of \(n\). Every legal sum has a realizing sign assignment, and all its realizations have the same effect on the next coefficient, so (8) is both necessary and sufficient. This compression is only for two steps; the individual factor labels can matter again at higher degrees.

## 5. Precisely what compactness would require

The full feasible-prefix tree is finitely branching: degree \(n-1\) has at most \(2^{d(n)}\) extensions. An infinite sign array exists if and only if this tree has a nonempty level at every degree. For completeness, if every level is nonempty, the root has arbitrarily deep descendants; at least one of its finitely many children does too. Inductively choose such a child at every level. The resulting nested prefixes specify each sign once and yield an infinite feasible array.

This equivalence requires feasible prefixes of *arbitrarily large* degree, not a witness at any fixed finite bound. Proposition 1 does not prove that every level is nonempty. Section 2 explicitly disproves the stronger claim that every current feasible prefix extends. The exact block formulation (6) isolates a possible route to a coherent-prefix invariant, but no such invariant is established here.

## Source context

The original problem and its fixed coefficient-parity observation are stated by [David Newman, Open Problem Garden](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions). The exact reductions and algebraic prefix example above are proved within this note; no unproved external lower bound or asymptotic result is used.
