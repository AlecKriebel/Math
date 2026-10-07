# Turn 5: a uniform mixed-lag exclusion and the remaining arithmetic gap

Problem 4700011, Gasull Problem 11. Authored 2026-10-07.

## Outcome of the fifth substantive attempt

The full arbitrary-order classification is **not resolved**, and no new globally periodic example has been constructed.

The principal new theorem excludes an infinite family of even-order supports with arbitrarily many active terms, for arbitrary real coefficients. A second line of argument gives all-order bounds and parameter restrictions for rational-ratio coefficients, including a finite exact decision procedure for the rationally scaled subclass. These results strengthen the partial classification without substituting a finite search for a uniform proof.

Turns 1–4 remain unchanged. No claim of novelty relative to prior literature is made.

## 1. Uniform exclusion of an odd midpoint with even neighbors

**Theorem 1.** Let \(k=4L+2\), with \(L\geq1\), and \(m=k/2=2L+1\). Consider

\[
\tag{1}
x_{n+k}=\frac{a_0+d x_{n+m}+\sum_{j\in E}a_jx_{n+j}}{x_n},
\]

where \(d>0\), \(a_0\geq0\), and \(E\) is a nonempty subset of the even lags \(\{2,4,\ldots,k-2\}\), closed under \(j\mapsto k-j\). Every displayed \(a_j\) is positive. Then (1) is not globally periodic.

No rationality assumption is made. Coefficient magnitudes do not enter the obstruction. In particular, a globally periodic map cannot have the midpoint as its only active odd lag and also have an active even lag when the order is congruent to 2 modulo 4.

*Proof.* By Turn 2's proved tropicalization lemma, finite order of the rational map would imply finite order of

\[
T(z_0,\ldots,z_{k-1})=
\left(z_1,\ldots,z_{k-1},
\max(\{z_m\}\cup\{z_j:j\in E\}\cup\{0:a_0>0\})-z_0\right).
\]

Let the base sequence be 4-periodic, with

\[
\tag{2}(z_0,z_1,z_2,z_3)=(0,0,1,1).
\]

Every reflected even pair consists of one lag divisible by 4 and one lag congruent to 2 modulo 4. Hence every base maximum equals 1, and

\[
z_{n+k}=1-z_n.
\]

The first \(k\) entries of (2) therefore give a fixed point of \(T^4\). The zero constant is always strictly below the base maximum, so its presence is immaterial to the tangent calculation.

Define

\[
A=\max\{j/4:j\in E,\ j\equiv0\pmod4\}.
\]

Then \(1\leq A\leq L\), and the smallest even lag congruent to 2 modulo 4 is \(4(L-A)+2\).

We construct a nonzero tangent sequence \(w_n\) satisfying \(w_{n+4}=\lambda w_n\), with \(\lambda>0\) and \(\lambda\ne1\). Set

\[
\tag{3}
w_{4t}=w_{4t+2}=0,\qquad
w_{4t+1}=U\lambda^t,\qquad
w_{4t+3}=-\lambda^t.
\]

The choices of \(\lambda\) and \(U\) depend only on the parity of \(L\).

### Case I: \(L\) odd

Let \(\lambda>1\) be the unique solution of

\[
\tag{4}\lambda^{2L+1}-\lambda^{2L-A+1}-1=0,
\]

and put

\[
U=\lambda^L-\lambda^{L-A}>0.
\]

Existence and uniqueness follow by writing (4) as

\[
\lambda^{2L-A+1}(\lambda^A-1)=1:
\]

the left side is zero at 1 and strictly increasing to infinity on \((1,\infty)\).

At each even time \(n\), the tied base winners are even-indexed coordinates with tangent value zero, and possibly the midpoint coordinate with a negative tangent value. The tangent maximum is therefore zero, as required by (3).

At time \(n=1\), the winning even lags are those congruent to 2 modulo 4. Since \(\lambda>1\), the largest of their negative tangent values is \(-\lambda^{L-A}\). The midpoint is not a base winner because \(m\equiv3\pmod4\). The tangent equation becomes

\[
-\lambda^L=-\lambda^{L-A}-U.
\]

At time \(n=3\), the midpoint is a base winner with tangent value zero. It dominates all negative tangent values from the even lags. The tangent equation becomes

\[
U\lambda^{L+1}=1,
\]

which is exactly (4). Thus the four-step tangent return multiplies the vector by \(\lambda>1\).

### Case II: \(L\) even

Let \(0<\lambda<1\) be the unique solution of

\[
\tag{5}\lambda^{2L+1}+\lambda^A-1=0,
\]

and put \(U=\lambda^L>0\). The polynomial in (5) is strictly increasing on \((0,\infty)\), negative at zero and positive at one.

The even-time tangent equations remain zero. At \(n=1\), the midpoint is now a base winner with tangent value zero, so

\[
-\lambda^L=-U.
\]

At \(n=3\), the midpoint is not a base winner. Since \(0<\lambda<1\), the largest negative tangent value among lags divisible by 4 is \(-\lambda^A\). The remaining equation is

\[
U\lambda^{L+1}=1-\lambda^A,
\]

which is (5). Therefore the four-step tangent return multiplies the vector by a strictly contracting positive number.

In both cases the tangent vector is nonzero, because \(w_3=-1\). The tangent return is positively homogeneous, so its \(p\)-th iterate sends this vector to \(\lambda^p w\), never to itself for \(p>0\). A finite-order piecewise-linear map fixing the base point would induce a finite-order tangent return, as proved in Turn 2. This contradiction establishes the theorem. \(\square\)

**Index-dilation corollary.** Any recurrence obtained by index-dilating a support in Theorem 1 is likewise excluded, because its residue-class subsystems can be initialized independently.

The order-six support \(\{2,3,4\}\) is the case \(L=A=1\), with expanding multiplier satisfying \(\lambda^3-\lambda^2-1=0\). In orders 10, 18, and so on, the obstruction instead uses a contracting tangent ray. This distinction is essential; an expanding-ray ansatz alone would miss half the family.

## 2. The normalized constant is totally positive

Continue with the normalized recurrence from Turn 4:

\[
y_{n+k}=\frac{c_0+\sum_jc_jy_{n+j}}{y_n},\qquad
c_0+\sum_jc_j=1,\qquad c_0>0.
\]

**Lemma 2.** Under global periodicity, \(c_0\) is a totally positive algebraic unit: every algebraic conjugate is strictly positive.

*Proof.* Turn 4 proves that \(c_0\) and its inverse are algebraic integers. It also gives the two fixed-point characteristic polynomials

\[
P_+(z)=z^k-\sum_jc_jz^j+1,
\qquad
P_-(z)=z^k+\sum_j(c_j/c_0)z^j+1.
\]

Every conjugate of each polynomial has roots of unity and real coefficients. Its value at 1 is strictly positive: nonreal roots pair to give positive squared absolute values; any root \(-1\) contributes 2; a root \(+1\) is impossible because the original value is nonzero and embeddings preserve nonzero algebraic numbers.

For any embedding \(\sigma\), these two values are

\[
1+\sigma(c_0)>0,
\qquad
1+1/\sigma(c_0)>0.
\]

A negative value \(\sigma(c_0)\) would have to be both greater than \(-1\) and less than \(-1\), which is impossible. Hence all conjugates are positive. \(\square\)

## 3. Rational-ratio coefficients: an algebraic parameter and a gap bound

Assume the positive variable coefficients of the reduced recurrence have rational ratios. Write them uniquely up to the positive scale \(b\) as

\[
a_j=b m_j,
\]

where the nonnegative integers \(m_j=m_{k-j}\) have greatest common divisor 1 among their positive entries. Put

\[
N=\sum_jm_j>0,\qquad
A=a_0/b^2>0.
\]

Rescaling \(x_n=b u_n\) gives

\[
\tag{6}
u_{n+k}=\frac{A+\sum_jm_j u_{n+j}}{u_n}.
\]

Let \(\rho>0\) be its diagonal fixed point and set

\[
\tau=1/\rho,\qquad
c_0=1-N\tau,\qquad
d=\tau/c_0,\qquad
M=1/A=\tau d.
\]

The fixed-point equation gives

\[
\tag{7}d-\tau=N\tau d=NM.
\]

**Theorem 3.** If (6) is globally periodic, then:

1. \(M\) is a totally positive algebraic integer.
2. If \(r=\min\{j:m_j>0\}\), every conjugate satisfies
   \[
   \tag{8}0<\sigma(M)<B:=\frac{k}{r m_r N}.
   \]
3. Consequently
   \[
   \tag{9}r m_r N\leq k-1.
   \]
4. If \(B\leq2\), then \(M=1\), equivalently \(A=1\).

*Proof.* The fixed-point coefficients are \(m_j\tau\) and \(-m_jd\). Bézout's identity and the primitive integer weights show that both \(\tau\) and \(d\) are totally real algebraic integers. By Lemma 2, \(\sigma(c_0)>0\), so \(\sigma(\tau)\) and \(\sigma(d)=\sigma(\tau)/\sigma(c_0)\) have the same sign and are nonzero. Thus

\[
\sigma(M)=\sigma(\tau)^2/\sigma(c_0)>0,
\]

and \(M=\tau d\) is an algebraic integer.

By coefficient symmetry, the first nonzero coefficient below the leading term of each fixed-point polynomial occurs at distance \(r\). Newton's identity gives the \(r\)-th power sums of the two spectra as

\[
r m_r\tau\quad\text{and}\quad-r m_r d,
\]

respectively. Their conjugates are sums of \(k\) numbers of modulus one, so

\[
|\sigma(\tau)|\leq\frac{k}{r m_r},\qquad
|\sigma(d)|\leq\frac{k}{r m_r}.
\]

Equation (7) and total positivity give \(\sigma(d)>\sigma(\tau)\). Because those numbers have the same nonzero sign,

\[
N\sigma(M)=\sigma(d)-\sigma(\tau)
<\max\{|\sigma(d)|,|\sigma(\tau)|\}
\leq\frac{k}{r m_r}.
\]

This proves (8). If \(B\leq1\), every conjugate of the nonzero algebraic integer \(M\) would lie strictly between zero and one, making its norm a positive integer strictly less than one. Hence \(B>1\), which is (9).

If \(B\leq2\), every conjugate of \(M-1\) lies strictly between \(-1\) and 1. Unless \(M-1=0\), the absolute value of its nonzero integer norm would again be less than one. Therefore \(M=1\). \(\square\)

**Corollary 4 (central-third supports).** In the rational-ratio class, every globally periodic recurrence whose active variable lags all lie in \([k/3,2k/3]\) is one of the classical families.

*Proof.* If at least three variable terms were active, then \(N\geq3\), \(m_r\geq1\), and \(r\geq k/3\), giving \(r m_r N\geq k\), contrary to (9). At most two active terms remain, and Turn 4 classifies all such supports without any rationality restriction. The homogeneous case was already classified in the rational-ratio class by Turn 1. \(\square\)

## 4. A finite algebraic parameter list in the large-gap regime

**Corollary 5.** For a fixed primitive integer support pattern, if \(B<4\), the parameter \(M=1/A\) belongs to a finite explicit list:

\[
\tag{10}M=2+\zeta+\zeta^{-1},
\]

where \(\zeta\) is a root of unity of order \(n\geq3\), and

\[
\tag{11}2+2\cos(2\pi/n)<B.
\]

In particular,

\[
\tag{12}n^2<\frac{4\pi^2}{4-B}
\]

is a finite upper bound for the orders needing inspection.

*Proof.* By (8), every conjugate of the algebraic integer \(M-2\) lies in \((-2,B-2)\subset(-2,2)\). Turn 4's proved Kronecker lemma gives (10). Orders 1 and 2 would give 4 and 0, incompatible with (8). The largest conjugate of (10) is \(2+2\cos(2\pi/n)\), which proves (11). Finally, \(\cos t\geq1-t^2/2\) gives

\[
2+2\cos(2\pi/n)\geq4-4\pi^2/n^2,
\]

and (11) yields (12). \(\square\)

This is a genuine all-order parameter restriction. It does not assert that the listed parameters are periodic; the full fixed-point spectra and nonlinear map identity still have to be checked.

## 5. Rationally scaled constants: finite arithmetic data in every order

Now add the hypothesis that \(A=a_0/b^2\) is rational. This includes recurrences whose reduced coefficients are all rational, and is invariant under a positive rescaling of the scalar variable.

**Theorem 6.** Under global periodicity with \(A>0\):

\[
\tag{13}A=1/M\quad\text{for an integer }M\geq1,
\]

and

\[
\tag{14}r m_r N M\leq k-1.
\]

Define \(R(z)=\sum_jm_jz^j\) and \(B_0(z)=z^k+1\). Then the integer polynomial

\[
\tag{15}Q(z)=B_0(z)^2+NM B_0(z)R(z)-M R(z)^2
\]

is a product of cyclotomic polynomials.

*Proof.* A rational algebraic integer is an integer, so Theorem 3 gives (13). The positive normalized fixed-point parameter satisfies

\[
\tag{16}\tau^2+NM\tau-M=0.
\]

It is irrational: otherwise the positive algebraic integer \(\tau\), lying strictly between zero and \(1/N\), would be an integer. Thus (16) is its quadratic minimal polynomial, and its other root is \(\tau'=-NM-\tau=-d\).

The negative fixed-point spectrum has power sum \(-r m_r d\). Since \(d=NM+\tau>NM\), its modulus bound gives

\[
r m_r NM<r m_r d\leq k.
\]

The left side is an integer, yielding (14).

The product of the conjugate characteristic polynomials is

\[
(B_0-\tau R)(B_0-\tau'R)
=B_0^2+NM B_0R-MR^2.
\]

All their roots are roots of unity, and the resulting monic polynomial has integer coefficients. Its irreducible factors are consequently cyclotomic polynomials. \(\square\)

**Finite per-order procedure.** Bound (14) implies \(N\leq k-1\), so there are only finitely many primitive palindromic nonnegative integer weight vectors to inspect. For each, it also bounds the positive integer \(M\). Equation (15) provides an exact cyclotomic rejection test.

If that test passes, also check that \(P_+(z)=B_0(z)-\tau R(z)\) is squarefree. If it is, let \(p\) be the least common multiple of the orders of the cyclotomic factors of \(Q\). The two conjugate spectra have the same sets of root orders, so \(p\) is the order of the positive fixed-point derivative. Global periodicity is then equivalent to the exact rational identity \(F^p=\mathrm{id}\), by the local linearization/order argument proved earlier.

Every cyclotomic factor of \(Q\) has degree at most \(2k\), so its order \(n\) satisfies \(\varphi(n)\leq2k\), hence \(n\leq8k^2\). This gives another explicit finite bound if needed. The homogeneous, identity, and constant-numerator cases are handled separately by the earlier theorems.

This procedure is finite for each fixed order. It has **not** been executed for all orders, and its existence is not a proof that its only surviving maps are the five classical families.

## 6. Why the combined restrictions still do not close the problem

### Bounds are not sufficient

For example, take order 8, weights

\[
m_1=m_7=1,\qquad m_4=2,
\]

and \(A=M=1\). Then \(N=4\), the parity weights are equal, and \(r m_r N M=4\leq7\). The normalized parameter is \(\tau=\sqrt5-2\), with positive algebraic-unit constant \(c_0=9-4\sqrt5\). These coarse arithmetic conditions all pass.

Nevertheless the negative fixed-point parameter is \(d=2+\sqrt5\). Its characteristic polynomial has first two lower leading coefficients \(d\) and zero, so Newton's identity gives second power sum

\[
d^2=9+4\sqrt5>8.
\]

Eight unit-modulus eigenvalues cannot have such a power sum. Thus this candidate is not periodic. It is included as a control against mistaking the coefficient bounds for a solution.

### Small-gap arithmetic can still have infinitely many candidates

The all-order gap bound leaves \(B\geq4\) possible. For instance, the primitive symmetric pattern

\[
k=16,\qquad R(z)=z+z^4+z^{12}+z^{15}
\]

has \(N=4\), equal parity weights, and \(B=4\). The infinitely many totally positive algebraic integers

\[
M_n=2+2\cos(2\pi/n),\qquad n\geq3,
\]

and all their conjugates lie strictly between 0 and 4. Thus the parameter-bound and positivity tests alone do not produce a finite list in this region.

This does **not** supply periodic recurrences or counterexamples. The corresponding candidates can fail the actual fixed-point root-of-unity spectra, cubic conditions, or full nonlinear identity. It shows exactly why a uniform conclusion cannot be drawn from the present arithmetic bounds alone.

### Other attempted transfers

The finite-order quiver/T-system classification was considered as a possible route. No verified identification of the general linear-sum numerator family with the hypotheses of such a theorem was established, so no quiver classification is invoked. Likewise, finite numerical or support searches were used only to suggest obstructions, never as proof in arbitrary order.

The remaining obstacles include mixed supports outside Theorem 1, unrestricted irrational variable-coefficient ratios in even order, and uniform elimination of the odd-order cyclotomic factors from Turn 3. None has been silently assumed away.

## 7. Exact verification and final retained conclusion

The exact verifier checks the tangent formulas over 247 different symmetric support patterns in orders 6 through 30, using polynomial remainders rather than numerical approximations to the multipliers. It verifies both constant statuses, the quadratic norm identity (15), the classical controls, and the order-eight failure control. These checks supplement the uniform proofs above; the theorems do not rest on extrapolation from those examples.

After five substantive author attempts, the retained result is a collection of rigorously proved partial classifications and necessary conditions:

- Complete arbitrary-real-coefficient classifications in orders 6, 13, and 15.
- Complete arbitrary-order classification with at most two active variable numerator terms.
- Odd-order finite spectral-factor and period reductions.
- Uniform mixed-lag, parity-weight, algebraic-unit, gap, and cubic obstructions.
- Finite exact per-order reductions in the stated rational-ratio/rationally scaled subclasses.

The complete arbitrary-order classification, or a new example outside the five known equivalence classes, remains unproved in this work.

## Source and method credit

The problem and its historical low-order context are in Armengol Gasull, *Some open problems in low dimensional dynamical systems*, Section 2.8, Problem 11: https://arxiv.org/abs/2012.02524 . The associated earlier classification reference is Cima–Gasull–Mañosas, *On periodic rational difference equations of order k*, J. Difference Equations Appl. 10 (2004), 549–559, https://doi.org/10.1080/10236190410001667977 . Its bibliographic record and abstract were checked; its full proof was not inspected in this work.

The local averaging linearization and fixed-point root-of-unity method are standard tools, also presented in Gasull's ICDEA 2012 slides, *Different approaches to the global periodicity problem*: https://www.gsd.uab.cat/icdea2012/Slides/Gasull.pdf . The preceding proofs include the arguments they use; presenting an independent derivation is not a claim to have originated those tools.
