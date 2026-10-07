# Turn 3: finite spectral-factor reduction in every odd order

Problem 4700011, Gasull Problem 11. Authored 2026-10-07.

## Result and scope

This is a structural reduction for **every odd order**, without rationality assumptions on the original coefficients. It replaces the continuous coefficient search by an explicit finite set, up to positive rescaling. It also gives a finite bound on possible global periods and an exact decision procedure for each fixed odd order.

The reduction does **not** prove a uniform classification for all odd orders. Arbitrary even orders also remain outside its scope. As concrete exact applications, the accompanying arithmetic certificates completely classify orders 13 and 15. No claim of novelty relative to the literature is made.

Turns 1 and 2 remain frozen. This turn uses the independently audited Turn 1 structural and two-cycle lemmas. It does not change or weaken the order-six theorem of Turn 2.

## 1. The remaining odd-order form

Let \(k=2m+1\geq3\). By Turn 1, apart from the identity dilation and constant-numerator reciprocal dilation, a globally periodic candidate has the form

\[
\tag{1}
x_{n+k}=\frac{a_0+\sum_{j=1}^{k-1}a_jx_{n+j}}{x_n},
\quad a_j\geq0,\quad a_j=a_{k-j},\quad a_0>0,
\]

with \(S=\sum_{j=1}^{k-1}a_j>0\). The strict positivity of \(a_0\) follows from Turn 1's homogeneous odd-order obstruction, and does not assume rational coefficient ratios.

Set \(h=S/2>0\) and

\[
E(t)=\sum_{r=1}^{m}a_{2r}t^r,\qquad
O(t)=\sum_{r=0}^{m-1}a_{2r+1}t^r.
\]

Symmetry implies \(E(1)=O(1)=h\). The proved two-cycle condition from Turn 1 is

\[
\tag{2}
h\big(E(t)^2-tO(t)^2\big)
=a_0\big(t^{m+1}O(t)-E(t)\big).
\]

## 2. A polynomial identity with only finitely many factors

**Theorem 1 (spectral-factor identity).** Define

\[
\tag{3}
A(z)=1+z^k+\frac{2h}{a_0}\sum_{j=1}^{k-1}a_jz^j.
\]

Then

\[
\tag{4}A(z)A(-z)=1-z^{2k}.
\]

In particular, \(A\) is monic and reciprocal, all its coefficients are nonnegative, its constant coefficient is 1, and every root is a simple \(2k\)-th root of unity.

*Proof.* Put \(r=2h/a_0\). The even part of \(A\) is \(1+rE(z^2)\); its odd part is \(z^k+r zO(z^2)\). Their difference of squares gives

\[
\begin{aligned}
A(z)A(-z)
={}&1-z^{2k}
+2r\big(E(z^2)-z^{k+1}O(z^2)\big)\\
&+r^2\big(E(z^2)^2-z^2O(z^2)^2\big).
\end{aligned}
\]

By (2), the last two terms cancel. Nonnegativity and reciprocity follow from (3) and the coefficient symmetry. The roots of \(1-z^{2k}\) are simple, so (4) gives the root assertion. \(\square\)

**Corollary 2 (explicit finite list).** Every such \(A\) belongs to the following list of \(2^m\) polynomials:

\[
\tag{5}
A_{\boldsymbol\varepsilon}(z)
=(z+1)\prod_{j=1}^{m}
\left(z^2+2\varepsilon_j\cos\frac{\pi j}{k}\,z+1\right),
\qquad \varepsilon_j\in\{-1,1\}.
\]

*Proof.* Since \(A(1)>0\), (4) forces \(-1\), rather than \(+1\), to be a root of \(A\). Among the remaining \(2k\)-th roots, organize each set

\[
\{\zeta,\overline\zeta,-\zeta,-\overline\zeta\}
\]

as a four-element group. There are exactly \(m\) such groups: because \(k\) is odd, none contains a root equal to its negative conjugate. Reality of \(A\), and the fact that \(A(z)\) and \(A(-z)\) cannot share a root, force exactly one conjugate pair from each group. The two choices produce the two signs in (5). The monic normalization fixes the remaining multiplicative constant. \(\square\)

Some factors in (5) have negative coefficients and are discarded. The factor \(1+z^k\) has no active interior coefficient and belongs to the separately handled constant-numerator case. No admissible nonconstant family has been lost by including other inadmissible factors in this preliminary finite list.

## 3. Each factor determines exactly one normalized recurrence

Write

\[
A(z)=1+z^k+\sum_{j=1}^{k-1}\ell_jz^j,
\qquad L=A(1)-2=\sum_{j=1}^{k-1}\ell_j.
\]

For an admissible nonconstant factor, all \(\ell_j\geq0\) and \(L>0\). Define

\[
\tag{6}
\lambda=\frac{\sqrt{1+4/L}-1}{2}>0,
\qquad c_j=\lambda\ell_j,
\qquad c_0=1-\sum_{j=1}^{k-1}c_j.
\]

Since \(L\lambda(\lambda+1)=1\),

\[
\sum c_j=\lambda L=\frac1{\lambda+1}<1,
\qquad c_0=\frac{\lambda}{\lambda+1}>0.
\]

**Theorem 3 (finite coefficient rigidity).** Up to positive rescaling of all scalar variables, every globally periodic nonconstant odd-order candidate is exactly one of the finitely many maps

\[
\tag{7}
y_{n+k}=\frac{c_0+\sum_{j=1}^{k-1}c_jy_{n+j}}{y_n}
\]

obtained from (5)–(6), retaining only factors with nonnegative coefficients and \(L>0\). Thus there are at most \(2^{(k-1)/2}-1\) nonconstant coefficient patterns up to rescaling.

*Proof.* The positive diagonal fixed point of (1) is the unique \(q>0\) satisfying

\[
q^2=a_0+2h q.
\]

After \(x_n=q y_n\), the normalized coefficients are \(c_j=a_j/q\) and \(c_0=a_0/q^2\), with \(c_0+\sum c_j=1\). Equation (3) gives

\[
\ell_j=\frac{2h}{a_0}a_j,\qquad
L=\frac{4h^2}{a_0},\qquad
\lambda=\frac{a_0}{2h q}.
\]

These satisfy \(c_j=\lambda\ell_j\) and \(\lambda(\lambda+1)=1/L\). The positive root is unique, giving (6). Conversely, (6) gives a well-defined positive map for every retained factor. That converse constructs candidates only; it does not assert that they are periodic. \(\square\)

This result removes any continuous real parameter other than the already permitted scalar rescaling. It applies to irrational coefficient ratios as well as rational ones.

## 4. Two exact arithmetic filters

Let

\[
K=\mathbb Q\left(2\cos\frac\pi k\right).
\]

Every coefficient \(\ell_j\) of (5) is an algebraic integer in the totally real cyclotomic field \(K\). Its degree is \(\varphi(k)/2\), where \(\varphi\) is Euler's totient.

At the normalized fixed point \((1,\ldots,1)\), the derivative has characteristic polynomial

\[
\tag{8}P(z)=z^k-\sum_{j=1}^{k-1}c_jz^j+1.
\]

Global periodicity makes every root of \(P\) a root of unity. Consequently every \(c_j\), being an elementary symmetric function of roots of unity, is an algebraic integer. Since the coefficients are real and belong to a cyclotomic field, they are also totally real: every algebraic conjugate is real.

### 4.1 Total-realness filter

**Theorem 4.** Every embedding \(\sigma:K\to\mathbb R\) must satisfy

\[
\tag{9}\sigma(A(1))>2.
\]

*Proof.* Formula (5) evaluated at 1 is

\[
A(1)=2\prod_{j=1}^{m}\left(2+2\varepsilon_j\cos\frac{\pi j}{k}\right).
\]

Under every embedding of \(K\), the cosine values become conjugate cosine values strictly between \(-1\) and 1. Thus every \(\sigma(A(1))\) is strictly positive.

Choose any nonzero \(\ell_j\). Since \(\lambda=c_j/\ell_j\), the total-realness of \(c_j\) and of \(K\) makes \(\lambda\) totally real. The embedding \(\sigma\) extends to the compositum containing \(\lambda\), and the image of \(\lambda\) must be a real root of

\[
X^2+X-\frac1{\sigma(A(1))-2}=0.
\]

If \(0<\sigma(A(1))<2\), its discriminant

\[
1+\frac4{\sigma(A(1))-2}
\]

is negative. Equality \(\sigma(A(1))=2\) is impossible because the nonzero algebraic number \(L=A(1)-2\) cannot map to zero under an embedding. Hence (9). \(\square\)

### 4.2 Algebraic-integrality filter

**Theorem 5.** For every \(j\), a necessary condition for periodicity is

\[
\tag{10}\frac{\ell_j^2}{A(1)-2}\ \text{is an algebraic integer}.
\]

In fact, for a fixed spectral factor, (10) is equivalent to algebraic integrality of the coefficient \(c_j=\lambda\ell_j\).

*Proof.* The relation \(\lambda^2+\lambda=1/L\) gives

\[
\tag{11}c_j(c_j+\ell_j)=\frac{\ell_j^2}{L}.
\]

If \(c_j\) is an algebraic integer, the right side is one as well. Conversely, if the right side is an algebraic integer, \(c_j\) solves the monic polynomial

\[
X^2+\ell_jX-\ell_j^2/L=0
\]

with algebraic-integer coefficients, so it is integral over the ring of algebraic integers and hence an algebraic integer. \(\square\)

These are necessary arithmetic conditions, not sufficient conditions for nonlinear global periodicity.

## 5. A finite period bound in each odd order

**Lemma 6.** A finite-order rational map fixing an interior point has the same order as its derivative there.

*Proof.* Translate the fixed point to zero and let \(F^p=\mathrm{id}\), \(D=DF(0)\). Define locally

\[
h(x)=\frac1p\sum_{j=0}^{p-1}D^{-j}F^j(x).
\]

Then \(Dh(0)=I\), so \(h\) is a local diffeomorphism. Reindexing the sum, using \(D^p=I\) and \(F^p=\mathrm{id}\), gives \(h\circ F=D\circ h\). If \(D^q=I\), then \(F^q\) is the identity on a neighborhood. A rational map equal to the identity on a nonempty open set is identically that rational map; in particular the equality holds throughout the positive domain where all iterates are defined. The derivative's order always divides the map's order, so the orders agree. \(\square\)

**Theorem 7 (explicit finite bound).** For an odd order \(k\geq3\), set

\[
D_k=k\varphi(k),\qquad B_k=2D_k^2,
\qquad N_k=\operatorname{lcm}\{1,2,\ldots,B_k\}.
\]

Every globally periodic nonconstant candidate in Theorem 3 satisfies \(F^{N_k}=\mathrm{id}\).

*Proof.* All coefficients of the normalized map lie in \(K(\lambda)\), whose degree over \(\mathbb Q\) is at most \(\varphi(k)\). Any eigenvalue of the degree-\(k\) characteristic polynomial (8) has algebraic degree at most \(k\varphi(k)=D_k\). If it is a root of unity of order \(n\), its degree is \(\varphi(n)\), hence \(\varphi(n)\leq D_k\).

The elementary bound

\[
\varphi(n)\geq\sqrt{n/2}
\]

implies \(n\leq2D_k^2=B_k\). For completeness, for \(n=\prod p^{e_p}\),

\[
\frac{\varphi(n)^2}{n}=\prod_{p\mid n}p^{e_p-2}(p-1)^2\geq\frac12:
\]

the factor for \(p=2\), if present, is at least \(1/2\), and every factor for an odd prime is at least 1. Therefore the derivative order divides \(N_k\). Apply Lemma 6. \(\square\)

**Corollary 8 (exact decision procedure for each fixed odd order).** Enumerate (5), retain the nonnegative factors with \(L>0\), construct their maps using (6), and test the rational-function identity \(F^{N_k}=\mathrm{id}\) over their algebraic coefficient fields. This finite procedure determines all globally periodic maps of that order, after separately adding the identity and reciprocal families.

The bound is deliberately crude. Directly computing such an iterate is generally impractical. The arithmetic filters and an exact derivative-root test are useful ways to reject candidates much earlier. The corollary is a finite decision theorem for each supplied odd \(k\), not a uniform proof that only the classical families survive as \(k\) varies.

## 6. Exact applications: orders 13 and 15

The accompanying verifier implements arithmetic in

\[
\mathbb Q[z]/(\Phi_{2k}(z)),
\]

using rational coefficients and the cyclotomic polynomial \(\Phi_{2k}\). It represents \(2\cos(\pi j/k)\) by \(z^j+z^{-j}\). This slightly larger complex cyclotomic field contains the real field \(K\); it does not change any integrality or conjugate-value test.

For each of the \(2^{(k-1)/2}\) sign patterns, the verifier:

1. Multiplies the factors (5) exactly.
2. Rejects \(L=0\), incompatible with a nonconstant nonnegative coefficient pattern. Such a factor need not itself be the constant-numerator factor if it has negative coefficients.
3. Forms the rational multiplication matrix for the field element \(A(1)\). Its characteristic polynomial lists all algebraic conjugates, with their field multiplicities. Exact real-root counting rejects any conjugate in \((0,2)\), by Theorem 4.
4. For each \(\ell_j^2/L\), forms its rational multiplication matrix. An element of a number field is an algebraic integer if and only if this characteristic polynomial has integer coefficients. Failure invokes Theorem 5.
5. Examines the surviving coefficients exactly for nonnegativity. In these two cases all remaining coefficients are rational integers, so no numerical sign decision occurs.

No floating-point approximations, sampled eigenangles, or assumed period caps are used in these classifications.

### Order 13

There are 64 sign patterns:

- 1 has zero interior sum;
- 62 fail the total-realness filter;
- 1 fails the algebraic-integrality filter;
- no nonconstant candidate remains.

The last rejected factor is

\[
A(z)=1+2z+2z^2+\cdots+2z^{12}+z^{13}.
\]

Here \(L=24\) and \(\ell_1^2/L=1/6\), which is not an algebraic integer. Therefore the only order-13 recurrences are identity and reciprocal dilations, with least common global periods 13 and 26.

### Order 15

There are 128 sign patterns:

- 2 have zero interior sum;
- 114 fail total-realness;
- 10 fail algebraic integrality;
- 2 pass those arithmetic filters.

One of the last two has coefficient list, from constant to leading term,

\[
(1,2,2,0,-2,-2,0,2,2,0,-2,-2,0,2,2,1),
\]

so it is inadmissible. The sole nonnegative survivor is

\[
\tag{12}A(z)=1+2z^5+2z^{10}+z^{15}.
\]

Now \(L=4\), so \(c_5=c_{10}=\sqrt2-1\) and

\[
c_0=3-2\sqrt2=(\sqrt2-1)^2.
\]

This is precisely the normalized eight-period order-three Lyness map, dilated by 5. It is globally periodic by the classical identity already verified in Turn 1. Thus order 15 contains only identity, reciprocal, and that Lyness dilation, with global periods 15, 30, and 40.

The full sign patterns, exact rejection polynomials, and surviving coefficient lists are preserved in `turn03_verification.json`. The deterministic verifier is `verify_turn03.py`.

## 7. Why weaker routes do not settle the general problem

- **Integrality alone is insufficient.** For \(k=5\), the positive factor with interior coefficients
  \[
  1+\sqrt5,\quad3+\sqrt5,\quad3+\sqrt5,\quad1+\sqrt5
  \]
  passes (10): the nonzero quotients are \((\sqrt5-1)/2\) and \((\sqrt5+1)/2\). But \(A(1)=10+4\sqrt5\) has conjugate \(10-4\sqrt5\in(0,2)\), so total-realness rejects it.
- **Total-realness alone is insufficient.** The all-2 interior factor in order 13 has \(A(1)=26\) and passes (9), but fails the exact integrality test above.
- **Arithmetic filters alone do not enforce the original sign hypothesis.** The explicitly displayed order-15 negative-coefficient factor passes both arithmetic filters and must still be removed.
- **These filters have not been proved sufficient for periodicity.** A remaining admissible factor must still pass the derivative root-of-unity test and the nonlinear identity. The finite decision theorem provides a terminating exact test, but not a practical or uniform classification proof.
- Exploratory numerical enumeration suggested strong patterns in additional odd orders. Those numerical observations are not used in any theorem or certificate here.

## 8. Exact remaining target

The continuous irrational-ratio difficulty in odd order is now reduced to the finite, explicit cyclotomic factors (5). A route to the full odd-order classification would be a uniform theorem showing that every admissible factor capable of global periodicity is

\[
1+2z^\ell+2z^{2\ell}+z^{3\ell},\qquad k=3\ell,
\]

besides the separate constant-numerator and identity cases. No such theorem has been proved here. The total-realness and integrality conditions suggest a precise arithmetic subproblem, but asserting their uniform sufficiency would exceed the evidence.

The full original problem also requires an arbitrary even-order argument. Turn 2's complete order-six support analysis does not automatically extend to all even orders.

## Source context

The original scope and the historical list of classified orders are recorded in Armengol Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, Problem 11, https://arxiv.org/abs/2012.02524 . This turn's spectral-factor argument and exact certificates are independently authored. No later-literature completeness or novelty claim is made.
