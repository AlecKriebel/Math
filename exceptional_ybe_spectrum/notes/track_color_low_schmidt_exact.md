# Exact no-go in the cyclic low-Schmidt color/face ansatz

**Date:** 2026-07-28
**Status:** proved ansatz theorem; not an unrestricted \(d=6\)
nonexistence theorem

## 1. Result and scope

The exact \(d=4\) color/face family from (10) of
`track_color_face_search.md` suggests extending two colors to three while
retaining its two-term operator-Schmidt form.  The natural cyclic extension
does **not** work, even if the mixing angle in every block is allowed to
vary.

More precisely, let \(F_c\) be the \(c\times c\) Fourier matrix and let
\[
 A,\ B_j,\ C_b\in M_2(\mathbb C)
\]
be traceless Hermitian reflections, with
\[
 AB_j=-B_jA.
\]
Let \(x_j,y_j\in\mathbb R\) satisfy
\[
 x_j^2+y_j^2=1,
\]
and put, with all color indices read modulo \(c\),
\[
 \boxed{
 K_{ab}
 =x_{a+b}A\otimes I_2
 +y_{a+b}B_{a+b}\otimes C_b .
 }
 \tag{1}
\]
Use \(U=F_c\) in the mixed color construction (3)--(5) of
`track_color_face_search.md`.

**Theorem.**  For \(c=3\), no exceptional Yang--Baxter solution of the
form (1) exists.

This is a genuine variable-angle theorem.  It does not assume
\(\lvert x_j\rvert=1/\sqrt3\), does not assume Pauli signs in advance, and
does not come from a numerical search.  Its proof includes the degenerate
pure-product boundary \(x_0=x_1=x_2=0\).

The proof first treats the genuinely two-term branch
\[
(x_0,x_1,x_2)\ne(0,0,0),
\tag{2}
\]
and then closes its pure-product boundary.

The theorem is only about the cyclic, mutually-unbiased color ansatz (1).
It does not cover arbitrary blocks \(K_{ab}\), arbitrary \(U\in U(3)\), or
arbitrary \(d=6\) exceptional matrices.

## 2. Why this ansatz contains the entire exact \(d=4\) calibration family

For \(c=2\), take
\[
 F_2=\frac1{\sqrt2}
 \begin{pmatrix}1&1\\1&-1\end{pmatrix},
\qquad
 x_0=\frac1{\sqrt3},\quad x_1=-\frac1{\sqrt3},
\qquad
 y_0=y_1=\sqrt{\frac23},
\]
\[
 A=Z,\qquad B_0=X,\qquad B_1=-Y,
\]
and
\[
 C_0=-tX-tY-sZ,\qquad
 C_1=-tX-tY+sZ,
\qquad s^2+2t^2=1.
\]
Then (1) is exactly
\[
 K_{ab}
 =\frac{(-1)^{a+b}}{\sqrt3}Z\otimes I_2
 +\sqrt{\frac23}\,
 B_{a+b}\otimes C_b,
\]
which is the full one-parameter family (9)--(10) in the preceding note.
Thus the failed \(c=3\) extension contains the complete exact calibration
family that motivated it.

## 3. Gauge reductions

The following reductions do not narrow the stated ansatz.

1. A simultaneous unitary on the first internal qubit sends the common
   reflection \(A\) to \(Z\).  The relations \(AB_j=-B_jA\) then put every
   \(B_j\) in the real Pauli plane
   \(\operatorname{span}_{\mathbb R}\{X,Y\}\).
2. A rotation about \(Z\) can send one chosen \(B_j\) to \(X\).  The proof
   below is coordinate-free in that plane and does not use this last
   normalization.
3. Simultaneous unitary conjugacy on the second internal qubit rotates all
   \(C_b\).  Individual signs may be moved between \(y_j\), \(B_j\), and a
   common sign of all \(C_b\); the proof retains signed \(y_j\) and therefore
   does not hide a sign branch.
4. Column phases of a complex Hadamard matrix do not change its rank-one
   column projections.  Row phases and row/column permutations are local
   color gauges and relabelings.  Every complex Hadamard matrix of order
   \(2\) or \(3\) is equivalent under these operations to \(F_2\) or
   \(F_3\).  Hence \(U=F_c\) is a gauge choice **within the
   mutually-unbiased mixing subansatz**.  We do not claim that an arbitrary
   solution must have mutually-unbiased color decompositions.

The condition \(AB_j=-B_jA\) is also exactly what involutivity of a
nondegenerate block requires:
\[
 (xA\otimes I+yB\otimes C)^2
 =(x^2+y^2)I+xy(AB+BA)\otimes C.
\]

## 4. Two exact contractions of the face equation

Write
\[
 K=xA_1+yB_1C_2,\qquad
 K'=x'A_1+y'B'_1C'_2,
\]
\[
 L=uA_2+vD_2E_3,
\qquad
 g=\frac12\operatorname{Tr}(BB').
\]
Using only tracelessness and \(AB=-BA\), \(AB'=-B'A\), one gets
\[
 \operatorname{Tr}_1(KLK')
 =2\bigl(xx'L+yy'g\,CLC'\bigr),
\tag{3}
\]
\[
 \operatorname{Tr}_{1,3}(KLK')
 =4u\bigl(xx'A+yy'g\,CAC'\bigr).
\tag{4}
\]
In the second cubic word \(LKL'\), the trace over the first internal
qubit is zero.  Applying (3)--(4) to the \((b,b')\) entry of the exact face
equation (5) therefore gives the two necessary identities
\[
 \sum_e\overline{U_{eb}}U_{eb'}x_{e+d}
 \left[
 \left(x_{a+b}x_{a+b'}+\frac13\right)A
 +y_{a+b}y_{a+b'}g_{a+b,a+b'}C_bAC_{b'}
 \right]=0,
\tag{5}
\]
and
\[
\begin{split}
\sum_e\overline{U_{eb}}U_{eb'}\bigg[
 &\left(x_{a+b}x_{a+b'}+\frac13\right)K_{e+d}\\
 &+y_{a+b}y_{a+b'}g_{a+b,a+b'}C_bK_{e+d}C_{b'}
\bigg]=0,
\end{split}
\tag{6}
\]
where
\[
 K_\ell=x_\ell A+y_\ell B_\ell C_d
\]
acts on the last two internal qubits.  The harmless fixed second factor
\(C_d\) is suppressed when no ambiguity can result.

These contractions are independently checked by
`verifiers/verify_color_low_schmidt_no_go.py`.

## 5. Standardness and the Fourier coefficient

Every exceptional solution is automatically standard.  In this block
form, its right partial trace is
\[
 \operatorname{Tr}_2H
 =2\sum_a |a\rangle\langle a|\otimes
 \left(\sum_jx_j\right)A.
\]
Consequently,
\[
 x_0+x_1+x_2=0.
\tag{7}
\]

Let \(\omega=e^{2\pi i/3}\).  For a real vector satisfying (7),
\[
\left|x_0+\omega x_1+\omega^2x_2\right|^2
=\frac32(x_0^2+x_1^2+x_2^2).
\tag{8}
\]
If \((x_0,x_1,x_2)\ne0\), both nontrivial Fourier coefficients are
therefore nonzero.
For \(U=F_3\), equation (5) with \(b\ne b'\) reduces to
\[
 \left(x_jx_k+\frac13\right)A
 y_jy_k g_{jk}C_bAC_{b'}=0
\qquad(j\ne k).
\tag{9}
\]

The three numbers \(x_jx_k+1/3\) cannot all vanish: multiplying those
three equations would make the nonnegative square
\((x_0x_1x_2)^2\) equal to \(-1/27\).  Varying the outer color in (9)
therefore shows, for every pair \(b\ne b'\), that
\[
 C_bAC_{b'}=\rho_{bb'}A,\qquad \rho_{bb'}\in\{+1,-1\}.
\tag{10}
\]

Compatibility around the three color pairs implies that there are signs
\(\delta_b\) and a single reflection \(C\) such that
\[
 C_b=\delta_bC,\qquad ACA=\kappa C,\qquad
 \kappa\in\{+1,-1\}.
\tag{11}
\]
Using the same nonzero pair in the three cyclic placements in (9) gives
\(\delta_0\delta_1=\delta_1\delta_2=\delta_2\delta_0\), so all
\(\delta_b\) agree.  Absorbing their common sign into \(C\), equations
(9) become
\[
 y_jy_kg_{jk}=-\kappa\left(x_jx_k+\frac13\right)
\qquad(j\ne k).
\tag{12}
\]

Thus the equations themselves force all three second-qubit reflections to
collapse to one axis, which either commutes or anticommutes with \(A\).

## 6. The nonzero common-axis branch

Put
\[
 L_j=K_j-\kappa CK_jC.
\]
For every nonzero coefficient \(x_jx_k+1/3\), equation (6) says that a
nontrivial Fourier coefficient of the cyclic sequence \(L_0,L_1,L_2\)
vanishes.  At least one coefficient is nonzero for each of the two
orientations.  Hence both nontrivial Fourier coefficients vanish and
\[
 L_0=L_1=L_2.
\tag{13}
\]

### 6.1 The commuting branch

If \(\kappa=+1\), then \(C=\pm A\), and conjugation by \(C\) negates every
\(B_j\).  Equation (13) says
\[
 y_0B_0=y_1B_1=y_2B_2=:V.
\tag{14}
\]
It follows from \(x_j^2+y_j^2=1\) that all \(\lvert x_j\rvert\) are equal.
Three real numbers of equal absolute value cannot have zero sum unless
they all vanish.  That would give \(\lVert V\rVert^2=1\), while (12) gives
\(\lVert V\rVert^2=-1/3\).  This branch is impossible.

### 6.2 The anticommuting branch

If \(\kappa=-1\), choose the orthonormal Pauli axes \(C,N\) in the plane
anticommuting with \(A\), and write
\[
 y_jB_j=h_jC+z_jN.
\tag{15}
\]
Equation (13) gives \(h_0=h_1=h_2=:h\).

Now use the diagonal case \(b=b'\) of (6).  Since (7) kills its \(A\)
component, its \(C\)- and \(N\)-components are exactly
\[
 4h=0,
\qquad
 2\left(x_j^2-\frac13\right)(z_0+z_1+z_2)=0
\quad(j=0,1,2).
\tag{16}
\]
The alternative \(x_0^2=x_1^2=x_2^2=1/3\) is incompatible with (7).
Therefore
\[
 h=0,\qquad z_0+z_1+z_2=0.
\tag{17}
\]

The vectors
\[
 w_j=(x_j,z_j)\in\mathbb R^2
\]
are unit vectors, by block involutivity, and sum to zero by (7) and (17).
Hence every pair has inner product \(-1/2\).  On the other hand, (12) gives
\[
 z_jz_k=x_jx_k+\frac13,
\]
so
\[
 -\frac12=w_j\mathbin{\cdot}w_k
 =2x_jx_k+\frac13.
\]
Thus
\[
 x_0x_1=x_1x_2=x_2x_0=-\frac5{12}.
\tag{18}
\]
Multiplying (18) again makes the nonnegative real square
\((x_0x_1x_2)^2\) negative.  This is the final contradiction.

## 7. The pure-product boundary

It remains to treat
\[
x_0=x_1=x_2=0.
\tag{19}
\]
Absorb each sign \(y_j=\pm1\) into \(B_j\), so
\[
K_{ab}=B_{a+b}\otimes C_b.
\]
The diagonal case \(b=b'\) of (6) becomes
\[
\frac13 S+C_bSC_b=0,
\qquad
S=B_0+B_1+B_2.
\tag{20}
\]
Conjugation by \(C_b\) preserves the Frobenius norm, whereas (20) would
shrink it by \(1/3\).  Therefore
\[
B_0+B_1+B_2=0.
\tag{21}
\]
The three \(B_j\)'s are unit Bloch vectors, so (21) makes their pairwise
inner products equal to \(-1/2\).

For \(b\ne b'\), let
\[
\widehat B_\Delta
=\sum_{e=0}^2\omega^{e\Delta}B_e,
\qquad \Delta=b'-b\in\{1,2\}.
\]
Equation (6), using \(g_{jk}=-1/2\), now reads
\[
C_b\widehat B_\Delta C_{b'}
=\frac23\widehat B_\Delta.
\tag{22}
\]
At least one nontrivial Fourier mode is nonzero, and Hermiticity makes the
two modes have equal Frobenius norm, so both are nonzero.  But the left
side of (22) has exactly the same Frobenius norm as
\(\widehat B_\Delta\), while the right side has only \(2/3\) of that norm.
This contradiction closes the boundary (19).

## 8. Consequences

1. The exact \(d=4\) color family is intrinsically even-color in this
   cyclic low-Schmidt mechanism.  Replacing the Hadamard pair by three
   Fourier-mixed colors cannot produce \(d=6\), even after freeing all
   three block angles.
2. The naive fixed-angle extension is excluded even earlier:
   \(x_j\in\{\pm1/\sqrt3\}\) cannot satisfy the standardness equation
   \(x_0+x_1+x_2=0\).
3. The obstruction is stronger than a request for a fourth Pauli axis.
   The exact face equations first collapse the \(C_b\)'s to one axis and
   then force the impossible real products (18).
4. This does not establish \(4\mid d\) for arbitrary solutions.  A viable
   \(d=6\) color construction must break at least one of: cyclic dependence
   on \(a+b\), mutually-unbiased Fourier mixing, a common first Pauli axis,
   or the rank-two block form (1).

The exact replay command is

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_color_low_schmidt_no_go.py
```

Its retained output is
`results/color_low_schmidt_exact_no_go.txt`.
