# Logical spin-flip completion of the three-component deficit

## Status

This note does **not** prove the three-component determinant
\[
 \det M\geq0.
\]
It gives two exact common-origin identities and rules out the most
direct residual-Gram construction.

For the three physical pair components, the scalar deficit matrix is
the logical partial trace of a natural \(6\times6\) Hermitian matrix.
The latter matrix need not be positive, even for an exact qutrit code
and three identical nonzero pair components.  Its logical spin flip is
therefore not optional: it is exactly the term which repairs the
negative direction in the example below.

The dependency-free checker is
`verification/verify_n3_pair_sector_logical_spinflip_obstruction.py`.

## 1. Logical block notation

Keep the notation of the three-component determinant reduction.  Thus
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
is an isometry,
\[
 D_{\widehat i}=I_i\otimes B_{\widehat i},\qquad
 X_i=D_{\widehat i}V,
\]
and
\[
 b_i=\|B_{\widehat i}\|_2^2,\qquad
 A_{ij}=X_i^\dagger X_j\in M_2.
\]
Then
\[
 c_{ij}=\operatorname{Tr}A_{ij},\qquad
 d_i=2b_i-\operatorname{Tr}A_{ii}.
\]

Define a \(3\times3\) block matrix with \(2\times2\) logical blocks by
\[
 {\mathbb N}_{ij}=\delta_{ij}b_iI_2-A_{ij}.               \tag{1}
\]
It is the tempting matrix-valued residual: if
\({\mathbb N}\succeq0\), its logical partial trace would immediately
give the desired scalar deficit matrix.

Let
\[
 \epsilon=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
 {\mathfrak s}(A)=\epsilon A^{\mathsf T}\epsilon^\dagger.
                                                               \tag{2}
\]
For a \(2\times2\) matrix,
\[
 {\mathfrak s}(A)=(\operatorname{Tr}A)I_2-A.              \tag{3}
\]
Apply \({\mathfrak s}\) blockwise to \({\mathbb N}\).

### Proposition 1 (exact logical spin-flip completion)

\[
 \boxed{\qquad
 M\otimes I_2={\mathbb N}+{\mathfrak s}_K({\mathbb N}).
 \qquad}                                                  \tag{4}
\]

#### Proof

If \(i=j\), equations (1)--(3) give
\[
 {\mathbb N}_{ii}+{\mathfrak s}({\mathbb N}_{ii})
 =
 \left(2b_i-\operatorname{Tr}A_{ii}\right)I_2
 =d_iI_2.
\]
If \(i\ne j\), they give
\[
 {\mathbb N}_{ij}+{\mathfrak s}({\mathbb N}_{ij})
 =
 -\left(A_{ij}+{\mathfrak s}(A_{ij})\right)
 =-\operatorname{Tr}(A_{ij})I_2
 =-c_{ij}I_2.
\]
These are precisely the blocks of \(M\otimes I_2\). \(\square\)

Equation (4) is a lossless common-logical-qubit reformulation.  It
also shows why a proof by discarding the logical cofactor channel is
not legitimate.

## 2. The spin-flipped Gram is not positive

The blockwise spin-flipped Gram
\[
 {\mathfrak s}_K(A),\qquad A_{ij}=X_i^\dagger X_j,
\]
is not positive in general.  This already fails with two nonzero
physical pair components.

Let
\[
 V|0\rangle=|020\rangle,\qquad V|1\rangle=|120\rangle,
\]
put \(Z=\operatorname{diag}(1,0,-1)\), and take
\[
\begin{aligned}
 D_{\widehat1}&=I\otimes E_{02}\otimes Z,\\
 D_{\widehat2}&=0,\\
 D_{\widehat3}&=-E_{01}\otimes E_{02}\otimes I.
\end{aligned}                                             \tag{5}
\]
The two nonzero pair coefficients are doubly traceless.  Direct action
on the code columns gives
\[
 X_1=(|000\rangle,|100\rangle),\qquad
 X_2=0,\qquad
 X_3=(0,-|000\rangle).                                   \tag{6}
\]
Although \(A=[X_i^\dagger X_j]\succeq0\), the principal submatrix of
\({\mathfrak s}_K(A)\) on
\[
 (\,\text{site label }1,\text{ logical }0\,),\qquad
 (\,\text{site label }3,\text{ logical }1\,)
\]
is
\[
 \begin{pmatrix}1&1\\1&0\end{pmatrix}.                   \tag{7}
\]
Its determinant is \(-1\), so
\[
 \boxed{\qquad {\mathfrak s}_K(A)\not\succeq0. \qquad}   \tag{8}
\]

Thus neither the direct residual below nor the spin-flipped Gram can
be made into a separate positive channel.  They must be combined
before positivity is asserted.

## 3. Exact physical obstruction to the naive residual Gram

Put
\[
 T=\operatorname{diag}\left(\frac23,-\frac13,-\frac13\right)
\]
and choose the code
\[
 V|0\rangle=|000\rangle,\qquad
 V|1\rangle=|111\rangle.                                 \tag{9}
\]
For all three sites take
\[
 B_{\widehat i}=\frac13T\otimes T.                        \tag{10}
\]
Every \(B_{\widehat i}\) is doubly traceless and nonzero.  Moreover,
\[
 b_i=\frac4{81}.                                         \tag{11}
\]
All three \(X_i\)'s coincide.  In the logical basis of (9),
\[
 A_{ij}=X_i^\dagger X_j
 =\operatorname{diag}\left(\frac{16}{729},
                            \frac1{729}\right)
 \quad\text{for every }i,j.                              \tag{12}
\]

Consequently \({\mathbb N}\) splits into its two logical diagonal
sectors.  On logical \(|0\rangle\), it is
\[
 \frac{36}{729}I_3-\frac{16}{729}J_3,
\]
where \(J_3\) is the all-ones matrix.  Hence
\[
 \boxed{\qquad
 \lambda_{\min}({\mathbb N})=-\frac4{243}<0.
 \qquad}                                                  \tag{13}
\]
Thus the most direct common residual vectors, whose Gram would be
\({\mathbb N}\), do not exist.

This is not a counterexample to the scalar determinant.  Here
\[
 M_{ii}=\frac{55}{729},\qquad
 M_{ij}=-\frac{17}{729}\quad(i\ne j),
\]
and therefore
\[
 \operatorname{spec}M
 =
 \left\{\frac7{243},\frac8{81},\frac8{81}\right\}.         \tag{14}
\]
The blockwise spin flip in (4) moves the negative logical-\(|0\rangle\)
channel to the complementary logical channel before the two are
added, and the scalar deficit is strictly positive.

## 4. A fully three-component equality

At a sharp equality with all three pair components nonzero, both
logical residual channels can be positive and share the correct
kernel.  Take
\[
\begin{aligned}
 V|0\rangle&=|000\rangle,\\
 V|1\rangle&=\frac{|110\rangle+|012\rangle}{\sqrt2},
\end{aligned}                                             \tag{15}
\]
and put
\[
\begin{aligned}
 Z&=\operatorname{diag}(1,-1,0),&
 S&=\operatorname{diag}(1,0,-1),\\
 E&=E_{20},&
 F&=E_{10},
\end{aligned}
\]
\[
\begin{aligned}
 D_{\widehat1}&=I\otimes Z\otimes E,\\
 D_{\widehat2}&=Z\otimes I\otimes E+F\otimes I\otimes S,\\
 D_{\widehat3}&=F\otimes Z\otimes I.
\end{aligned}                                             \tag{16}
\]
Direct contraction gives
\[
 (b_1,b_2,b_3)=(2,4,2)
\]
and
\[
\begin{array}{c|ccc}
 A_{ij}&1&2&3\\ \hline
1&\operatorname{diag}(1,\tfrac12)&
  \operatorname{diag}(1,1)&
  \operatorname{diag}(0,\tfrac12)\\
2&\operatorname{diag}(1,1)&
  \operatorname{diag}(2,2)&
  \operatorname{diag}(1,1)\\
3&\operatorname{diag}(0,\tfrac12)&
  \operatorname{diag}(1,1)&
  \operatorname{diag}(1,\tfrac12).
\end{array}                                               \tag{17}
\]
Consequently
\[
 (d_1,d_2,d_3)=\left(\frac52,4,\frac52\right),\qquad
 (c_{12},c_{23},c_{13})=\left(2,2,\frac12\right),
\]
and
\[
 \operatorname{spec}M=\{0,3,6\},\qquad
 \ker M=\mathbb C(1,1,1).
\]

Before taking the logical trace, the logical-\(|0\rangle\) block of
\({\mathbb N}\) is the path Laplacian
\[
 \begin{pmatrix}1&-1&0\\-1&2&-1\\0&-1&1\end{pmatrix},
\]
and its logical-\(|1\rangle\) block is the weighted-triangle
Laplacian
\[
 \begin{pmatrix}
 3/2&-1&-1/2\\
 -1&2&-1\\
 -1/2&-1&3/2
 \end{pmatrix}.                                          \tag{18}
\]
Thus
\[
 \operatorname{spec}{\mathbb N}=\{0,0,1,2,3,3\}.
\]
The blockwise spin flip interchanges the two Laplacians.  Both
channels are positive and have common kernel
\[
 \operatorname{span}\{(1,1,1)\otimes|0\rangle,\,
                       (1,1,1)\otimes|1\rangle\}.         \tag{19}
\]
This equality displays the desired residual geometry: two correlated
logical frames, not one.

## 5. The exact logical three-cycle identity

The common logical dimension also gives a lossless replacement of the
problematic scalar cycle.  For arbitrary \(2\times2\) matrices
\(K_1,K_2,K_3\),
\[
\boxed{
\begin{aligned}
 \operatorname{Tr}K_1\operatorname{Tr}K_2\operatorname{Tr}K_3
={}&
 \operatorname{Tr}(K_1K_2)\operatorname{Tr}K_3\\
&+\operatorname{Tr}(K_1K_3)\operatorname{Tr}K_2\\
&+\operatorname{Tr}(K_2K_3)\operatorname{Tr}K_1\\
&-\operatorname{Tr}(K_1K_2K_3)
 -\operatorname{Tr}(K_1K_3K_2).
\end{aligned}}                                           \tag{20}
\]
This is the complete polarization of the degree-three
Cayley--Hamilton identity in dimension two.  It can also be obtained
by contracting \(\bigwedge^3\mathbb C^2=0\).

Taking
\[
 K_1=A_{12},\qquad K_2=A_{23},\qquad K_3=A_{31}
\]
turns the left side into
\[
 c_{12}c_{23}\overline{c_{13}}.                          \tag{21}
\]
Thus the phase-sensitive term in \(\det M\) is not an independent
scalar: it is exactly a sum of five coherent trace contractions of
the same three logical transition matrices.

Identity (20) has not yet been converted into a positive bound by the
diagonal budgets \(d_i\).  Equations (4), (13), and (20) sharply locate
the remaining task: a successful residual Gram must combine the two
logical spin-flip channels before taking positivity, and a successful
cycle estimate must retain the five terms in (20) coherently.
