# The nonvertical triple-root companion is impossible

**Status:** exact standalone working lemma.  It has not yet received an
independent hostile audit and is not peer reviewed.

**Recorded:** 2026-07-25T11:39:23Z.

Together with `NONVERTICAL_NONTRIPLE_LEMMA.md`, this closes every
nonvertical companion \(G_3=q\) on the triple-vertical leading-pencil
frontier.

## 1. Statement

Let
\[
H_4=(z^4,zq,0)^T,\qquad (H_3)_3=q,                     \tag{1}
\]
where \((z^3,q)\) is a coprime minimal cubic pencil.  Assume
\[
q|_{z=0}=L^3.                                          \tag{2}
\]
Then no total-degree-four Keller map has (1).

## 2. Complete stabilizer normal forms

Take \(L=x\) and scale \(q\) so that its \(x^3\)-coefficient is one:
\[
q=x^3+z(Ax^2+Bxy+Cy^2)+z^2(Dx+Ey)+Fz^3.               \tag{3}
\]
The full parabolic preserving the marked line \(z=0\) and its triple root
has
\[
x\mapsto ax+uz,\qquad
y\mapsto by+cx+vz,\qquad
z\mapsto dz.                                           \tag{4}
\]
Using only (4), scaling \(q\), and retaining every parameter, the minimal
locus has exactly the following three normal-form families:
\[
\begin{array}{c|c|c}
\text{condition in (3)}&\text{normal form}&\text{retained moduli}\\ \hline
C\ne0&
x^3+y^2z+\alpha xz^2+\beta z^3&(\alpha,\beta)\\
C=0,\ B\ne0&
x^3+xyz+\beta z^3&\beta\\
C=B=0,\ E\ne0&
x^3+yz^2&\text{none}.
\end{array}                                             \tag{5}
\]
If \(C=B=E=0\), then \(q\) is binary in \(x,z\), and
\((z^3,q)\) is nonminimal; it reclassifies into the \((a,b)=(1,3)\) row.

For completeness:

- if \(C\ne0\), completing the square in \(y\) kills \(B,E\), translating
  \(x\) depresses the remaining binary cubic, and scaling gives the first
  row of (5);
- if \(C=0,B\ne0\), an \(x\)-translation kills \(E\), then the \(x\)- and
  \(z\)-parts of a \(y\)-shear kill \(A,D\);
- if \(C=B=0,E\ne0\), a \(y\)-shear and an \(x\)-translation kill
  \(A,D,F\).

Thus (5) is exhaustive and the two displayed moduli in the first row are
not silently specialized.

## 3. Constant-minor obstruction

Write
\[
H_3=(U,V,q)^T,\qquad H_2=(A_2,B_2,W)^T.
\]
The complete legal \(E_7\) gauge is
\[
U=dz^3,\qquad V=zW+fz^3.                               \tag{6}
\]
For each family in (5), keep all six coefficients of \(W\), both
scalars \(d,f\), all twelve coefficients of \(A_2,B_2\), all nine entries
of the linear matrix, and all displayed moduli symbolic.

The combined full \(E_6,E_5\) coefficient matrix has rank fourteen.  It
has the following literal \(14\times14\) pivot minors:
\[
\begin{array}{c|c}
q&\text{pivot minor}\\ \hline
x^3+y^2z+\alpha xz^2+\beta z^3&
-110075314176=-2^{24}3^8\\
x^3+xyz+\beta z^3&
-191102976=-2^{18}3^6\\
x^3+yz^2&
-2293235712=-2^{20}3^7.
\end{array}                                             \tag{7}
\]
Solving those pivot equations gives identically, in all three families,
\[
\begin{aligned}
A_2&=\alpha_0z^2,\\
B_2&=z(\ell_{31}x+\ell_{32}y+\beta_0z),\\
\bar L_1&=\bar L_2=0,\qquad
\bar L_3=(\ell_{31},\ell_{32}).
\end{aligned}                                          \tag{8}
\]
Every nonpivot coefficient equation vanishes after (8); no compatibility
condition or parameter divisor is omitted.

The first two rows of \(L\) in (8) are multiples of \(dz\), so
\(\det L=0\).  This contradicts the invertible linear part and proves the
lemma.

## 4. Verification and disclosure

`verify_nonvertical_triple_root_sympy.py` reconstructs the three full
systems, checks every constant minor in (7), solves the pivot systems over
the full symbolic coefficient rings, checks every residual equation, and
checks singularity of \(L\).

Exact computer algebra is evidence about the encoded identities, not peer
review.  AI systems materially assisted the classification, derivation,
computation, and exposition.
