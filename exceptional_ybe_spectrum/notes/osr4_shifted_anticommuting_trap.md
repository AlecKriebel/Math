# An exact rank-four shifted-anticommuting optimizer trap in dimension six

**Date:** 2026-07-29

**Status:** PROVED optimizer limitation model

**Scope:** this note constructs a fully standard Hermitian involution of
operator-Schmidt rank four in local dimension six.  Its shifted copies
anticommute, so it is an exact stationary point of the normalized cubic
residual on the fixed-Schmidt-rank search manifold, but it is **not** an
exceptional Yang--Baxter solution.  Nothing here excludes other rank-four
solutions.

## 1. Construction

Write
\[
V=\mathbb C^2\otimes\mathbb C^3.
\]
Let \(X,Y,Z\) be the Hermitian Pauli matrices on \(\mathbb C^2\).  On
\(\mathbb C^3\), put
\[
P_0=|0\rangle\langle0|,\qquad P_1=I-P_0,
\]
\[
X_{12}=|1\rangle\langle2|+|2\rangle\langle1|,
\qquad
Z_{12}=|1\rangle\langle1|-|2\rangle\langle2|,
\]
and \(c=1/\sqrt2\).  Define
\[
\begin{array}{ll}
C_0=P_0+cP_1, & S_0=cX_{12},\\
C_1=cP_1,     & S_1=P_0+cZ_{12}.
\end{array}
\tag{1}
\]
The four matrices \(C_0,C_1,S_0,S_1\) are linearly independent.  Indeed,
\[
C_0-C_1=P_0,\quad C_1=cP_1,\quad S_0=cX_{12},
\quad S_1-P_0=cZ_{12}.
\tag{2}
\]

On \(V\otimes V\), define
\[
\begin{aligned}
H={}&(X\otimes P_0)\otimes(Z\otimes C_0)
    +(X\otimes P_1)\otimes(Z\otimes C_1)\\
 & +(Y\otimes P_0)\otimes(Z\otimes S_0)
    +(Y\otimes P_1)\otimes(Z\otimes S_1).
\end{aligned}
\tag{3}
\]

> **Proposition 1.**  The matrix \(H\) is a Hermitian involution with
> \[
> \operatorname{Tr}H=0,\qquad
> \operatorname{Tr}_1H=\operatorname{Tr}_2H=0,
> \qquad \operatorname{OSR}(H)=4.
> \tag{4}
> \]
> Its shifted copies \(S=H_{12}\) and \(T=H_{23}\) satisfy
> \[
> \boxed{ST=-TS.}
> \tag{5}
> \]

### Proof

After grouping the two qubit coordinates and the two qutrit coordinates,
write
\[
H=(X\otimes Z)\otimes K_X+(Y\otimes Z)\otimes K_Y,
\tag{6}
\]
where
\[
K_X=P_0\otimes C_0+P_1\otimes C_1,\qquad
K_Y=P_0\otimes S_0+P_1\otimes S_1.
\tag{7}
\]
The definitions give
\[
[C_a,S_a]=0,\qquad C_a^2+S_a^2=I_3
\quad(a=0,1).
\tag{8}
\]
Therefore \([K_X,K_Y]=0\) and \(K_X^2+K_Y^2=I_9\).  The two qubit
factors in (6) anticommute and square to the identity, so \(H^2=I_{36}\).
Hermiticity is immediate.

Every summand in (3) contains a traceless Pauli factor on each six-
dimensional site.  This proves the trace and both partial-trace identities
in (4).  The four left factors in (3) are nonzero and mutually
Hilbert--Schmidt orthogonal.  The four right factors are independent by
(2).  Hence the realigned matrix has rank four, proving
\(\operatorname{OSR}(H)=4\).

For every left factor \(A_j\in\{X\otimes P_a,Y\otimes P_a\}\) and every
right factor \(B_i\in\{Z\otimes C_a,Z\otimes S_a\}\), the qutrit factors
commute while \(X\) and \(Y\) anticommute with \(Z\).  Thus
\[
\{B_i,A_j\}=0\qquad(i,j=1,\ldots,4).
\tag{9}
\]
Expanding the two shifted copies gives
\[
ST+TS=\sum_{i,j}A_i\otimes\{B_i,A_j\}\otimes B_j=0,
\]
which is (5). \(\square\)

## 2. Exact exceptional residual

Let
\[
\mathcal C(H)=STS-TST-\frac13(S-T).
\tag{10}
\]
From \(ST=-TS\) and \(S^2=T^2=I\),
\[
STS=-T,\qquad TST=-S.
\]
Consequently
\[
\boxed{\mathcal C(H)=\frac23(S-T).}
\tag{11}
\]
Also \(\operatorname{Tr}(ST)=0\), either by cyclicity and anticommutation
or from the zero marginals.  In local dimension \(d\),
\[
\|S-T\|_{\mathrm{HS}}^2=2d^3.
\]
For the displayed \(d=6\) model,
\[
\boxed{\|\mathcal C(H)\|_{\mathrm{HS}}^2
=\frac89d^3=192,}
\qquad
\boxed{d^{-3}\|\mathcal C(H)\|_{\mathrm{HS}}^2=\frac89.}
\tag{12}
\]
Thus this is not an exceptional solution: its cubic coefficient is \(1\),
not \(1/3\).

## 3. Why gradient searches stop here

Consider the normalized objective
\[
\Phi(H)=d^{-3}\|\mathcal C(H)\|_{\mathrm{HS}}^2
\tag{13}
\]
on the rank-four Hermitian Schmidt parameter manifold
\[
H=\sum_{j=1}^4s_jA_j\otimes B_j,
\tag{14}
\]
where each family is Hilbert--Schmidt orthonormal in the real space of
traceless Hermitian matrices, all \(s_j\ne0\), and
\[
\sum_js_j^2=d^2.
\tag{15}
\]
The tangent conditions are
\[
\langle A_i,\dot A_j\rangle+\langle\dot A_i,A_j\rangle=0,
\quad
\langle B_i,\dot B_j\rangle+\langle\dot B_i,B_j\rangle=0,
\quad
\sum_js_j\dot s_j=0.
\tag{16}
\]

> **Proposition 2.**  If a zero-marginal Hermitian involution satisfies
> \(ST=-TS\), then
> \[
> \boxed{\nabla_H\Phi=\frac{64}{9d^2}H.}
> \tag{17}
> \]
> Hence every rank-four point of this type is stationary on the manifold
> (14)--(16).

### Proof

For an arbitrary Hermitian variation, put \(C=\mathcal C(H)\).  The
adjoint derivatives with respect to the two shifted variables are
\[
\begin{aligned}
G_S&=\frac2{d^3}
\left(TSC+CST-TCT-\frac13C\right),\\
G_T&=\frac2{d^3}
\left(SCS-STC-CTS+\frac13C\right).
\end{aligned}
\tag{18}
\]
At a shifted-anticommuting involution, \(C=\frac23(S-T)\).  Reduction with
\(S^2=T^2=I\) and \(ST=-TS\) gives
\[
\begin{aligned}
G_S&=\frac4{3d^3}
\left(\frac83S+\frac{10}3T\right),\\
G_T&=\frac4{3d^3}
\left(\frac{10}3S+\frac83T\right).
\end{aligned}
\tag{19}
\]
The gradient with respect to the common two-site matrix is
\[
\nabla_H\Phi=\operatorname{Tr}_3G_S+\operatorname{Tr}_1G_T.
\tag{20}
\]
Zero marginals kill the \(T\)-term in the first partial trace and the
\(S\)-term in the second.  The two surviving terms each contribute
\(32H/(9d^2)\), proving (17).

For a tangent variation of (14), orthonormality and (16) give
\[
\langle H,\dot H\rangle
=\sum_js_j\dot s_j
+\sum_js_j^2\langle A_j,\dot A_j\rangle
+\sum_js_j^2\langle B_j,\dot B_j\rangle=0.
\tag{21}
\]
The radial gradient (17) therefore has zero pairing with every tangent
direction. \(\square\)

This explains an exact false basin observed by the general rank-four
search: continuation drove the involution residual below \(10^{-8}\) while
the shifted product spectrum converged to \(+i\) and \(-i\), each with
multiplicity \(108\), and the normalized cubic residual converged to
\(8/9\).  Those numbers diagnose (5); they are not evidence for or against
an exceptional \(d=6\) witness.

## 4. Stacked sandwich-kernel calibration

The model also calibrates the two stacked support maps used in the
rank-four Schmidt-support audit.  Absorb all coefficients into the
displayed independent families and write
\[
H=\sum_{i=1}^4L_i\otimes R_i.
\tag{22}
\]
Define
\[
\mathcal K_{R|L}=
\left\{
C\in M_4(\mathbb C):
\sum_{i,k}C_{ik}R_i xR_k=0
\text{ for every }
x\in\operatorname{span}_{\mathbb C}\{I,L_1,\ldots,L_4\}
\right\},
\tag{23}
\]
and define \(\mathcal K_{L|R}\) by interchanging \(L\) and \(R\).
Stacking the five \(6\times6\) outputs produces a
\(180\times16\) matrix in each orientation.  Exact reduction gives
\[
\begin{array}{c|cc}
&\text{stack rank}&\text{complex kernel dimension}\\ \hline
\mathcal K_{R|L}&5&11\\
\mathcal K_{L|R}&4&12.
\end{array}
\tag{24}
\]

Both kernels are closed under adjoint.  The verifier deterministically
splits a complex nullspace basis into Hermitian and skew-Hermitian parts
and extracts real bases of the Hermitian kernels.  In the \(R|L\)
orientation, ten selected generators have
\[
(\operatorname{rank},n_+,n_-,n_0)=(2,1,1,2)
\]
and one has \((3,2,1,1)\).  In the \(L|R\) orientation, all twelve selected
generators have \((2,1,1,2)\).  These signature counts concern one explicit
deterministic Hermitian basis, while the kernel dimensions in (24) are
basis invariant.

Thus this optimizer trap lies deep in both residual sandwich-kernel
branches; it is a calibration model, not a counterexample to any
exceptional-solution implication.

## 5. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_osr4_shifted_anticommuting_trap.py
```

The verifier uses exact arithmetic over \(\mathbb Q(\sqrt2,i)\) and checks
all assertions above, including the full \(216\times216\) shifted
anticommutator, residual norm, radial gradient, and both stacked
sandwich kernels.
