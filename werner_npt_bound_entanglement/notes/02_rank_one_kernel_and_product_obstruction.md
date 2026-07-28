# Rank-one kernel formula and a no-go theorem for copywise product codewords

Let
\[
R_{d,n}:=\left(I-\tfrac12F\right)^{\otimes n}
\]
on \(H\otimes H\), where \(H=(\mathbb C^d)^{\otimes n}\).  This operator is
positive definite because each factor has eigenvalues \(\tfrac12\) and
\(\tfrac32\).

## 1. Four-vector formula

Write rank-one coefficient matrices as \(|a\rangle\langle b|\).  For any
\(a,b,c,e\in H\),
\[
\begin{aligned}
\left\langle \operatorname{Tr}_S(|a\rangle\langle b|),
\operatorname{Tr}_S(|c\rangle\langle e|)\right\rangle_{HS}
&=\langle a\otimes e|F_S|c\otimes b\rangle,\\
\mathcal B_n(|a\rangle\langle b|,|c\rangle\langle e|)
&=\langle a\otimes e|R_{d,n}|c\otimes b\rangle,
\tag{1}
\end{aligned}
\]
where \(\mathcal B_n\) is the sesquilinear form whose quadratic form is
\(Q_{d,n}\), and \(F_S\) swaps the two copies of each subsystem in \(S\).

To verify the first identity, expand both sides in coordinates.  The left
side is
\[
\sum_{x_{\bar S},y_{\bar S}}\sum_{z_S,w_S}
\overline{a_{z_Sx_{\bar S}}}\,
b_{z_Sy_{\bar S}}\,
c_{w_Sx_{\bar S}}\,
\overline{e_{w_Sy_{\bar S}}},
\]
which is exactly the matrix element of \(F_S\) on the right.  Summing with
coefficients \((-\tfrac12)^{|S|}\) proves the second identity.

In particular,
\[
Q_{d,n}(|a\rangle\langle b|)
=\langle a\otimes b|R_{d,n}|a\otimes b\rangle>0
\tag{2}
\]
for nonzero \(a,b\).  Thus the endpoint tensor powers are strictly positive
on nonzero Schmidt-rank-one vectors.

For a rank-at-most-two matrix
\[
C=|a\rangle\langle b|+\lambda|c\rangle\langle e|,
\]
formula (1) gives
\[
\begin{aligned}
Q_{d,n}(C)
={}&\langle a\otimes b|R_{d,n}|a\otimes b\rangle\\
&+|\lambda|^2
\langle c\otimes e|R_{d,n}|c\otimes e\rangle\\
&+2\operatorname{Re}\!\left[
\lambda\langle a\otimes e|R_{d,n}|c\otimes b\rangle
\right].
\tag{3}
\end{aligned}
\]
Ordinary Cauchy--Schwarz for the positive operator \(R_{d,n}\) only bounds
the last matrix element by the *crossed* diagonal terms
\(\langle a\otimes e|R|a\otimes e\rangle\) and
\(\langle c\otimes b|R|c\otimes b\rangle\).  These are not the two diagonal
terms in (3); this precisely identifies why positivity of \(R_{d,n}\) alone
does not settle two-block positivity.

## 2. Copywise-product no-go theorem

**Theorem.** Suppose all four vectors in a two-term decomposition factor
across copies:
\[
a=\bigotimes_{i=1}^n a_i,\quad
b=\bigotimes_{i=1}^n b_i,\quad
c=\bigotimes_{i=1}^n c_i,\quad
e=\bigotimes_{i=1}^n e_i.
\]
Then, for every \(\lambda\in\mathbb C\),
\[
Q_{d,n}\!\left(
|a\rangle\langle b|+\lambda|c\rangle\langle e|
\right)\ge0.
\tag{4}
\]

**Proof.** For each copy define
\[
\begin{aligned}
A_i&=\langle a_i\otimes b_i|
(I-\tfrac12F)|a_i\otimes b_i\rangle,\\
D_i&=\langle c_i\otimes e_i|
(I-\tfrac12F)|c_i\otimes e_i\rangle,\\
Z_i&=\langle a_i\otimes e_i|
(I-\tfrac12F)|c_i\otimes b_i\rangle.
\end{aligned}
\]
The one-copy theorem applied to
\(|a_i\rangle\langle b_i|+z|c_i\rangle\langle e_i|\), for every
\(z\in\mathbb C\), says that the scalar quadratic polynomial
\[
A_i+|z|^2D_i+2\operatorname{Re}(zZ_i)
\]
is nonnegative.  Since \(A_i,D_i>0\) unless a rank-one term vanishes, its
discriminant condition is
\[
|Z_i|^2\le A_iD_i.
\tag{5}
\]
(The cases with a zero vector follow directly.)

Tensor factorization in (3) yields
\[
Q_{d,n}(C)
=A+|\lambda|^2D+2\operatorname{Re}(\lambda Z),
\quad
A=\prod_iA_i,\ D=\prod_iD_i,\ Z=\prod_iZ_i.
\]
Multiplying (5) gives \(|Z|^2\le AD\), which is exactly the condition that
this last quadratic polynomial be nonnegative for every \(\lambda\).
\(\square\)

Consequently, any endpoint distillation witness must have entanglement
across the copy index in at least one of the four Schmidt vectors in every
two-term decomposition to which the theorem applies.  In particular,
searching only computational strings, GHZ-like sums of two copywise product
terms, or tensor powers of one-copy Schmidt vectors cannot succeed.
