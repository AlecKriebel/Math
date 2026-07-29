# The physical logical residual can have two negative directions

## Status

This note gives an exact physical obstruction to an exterior-power route
for the remaining qutrit three-copy pair-sector determinant.  In the
standard notation
\[
 {\mathbb N}_{ij}=\delta_{ij}b_iI_2-X_i^\dagger X_j,
 \qquad X_i=D_{\widehat i}V,
\]
the scalar deficit satisfies
\[
 M\otimes I_2={\mathbb N}+{\mathfrak s}_K({\mathbb N}),
\]
where \({\mathfrak s}_K\) is the logical spin flip.

It was natural to hope that physical common-frame geometry forced
\({\mathbb N}\) to have negative index at most one.  Such an inertia
bound, combined with a suitable compound-matrix argument, would sharply
restrict the possible negative directions before the spin-flip
completion.

The construction below proves instead that
\[
 \boxed{\operatorname{inertia}({\mathbb N})=(4,2,0)}
\]
for exact doubly-traceless qutrit pair coefficients.  At the same time,
the genuine scalar matrix \(M\) is strictly positive.  Thus this is not
a counterexample to the pair-sector theorem.  It is a counterexample
only to the proposed residual-inertia lemma and to any proof which
requires \(\bigwedge^2{\mathbb N}\succeq0\).

The dependency-free exact checker is
`verification/verify_n3_pair_sector_residual_inertia_two.py`.

## 1. Code and pair coefficients

Let
\[
 V|0\rangle=|000\rangle,\qquad V|1\rangle=|111\rangle.
 \tag{1}
\]
Use
\[
 E=|0\rangle\langle1|,\qquad
 F=|1\rangle\langle0|,
 \tag{2}
\]
and the two traceless diagonal matrices
\[
 Z_0=\operatorname{diag}(1,-\tfrac12,-\tfrac12),
 \qquad
 Z_1=\operatorname{diag}(-\tfrac12,1,-\tfrac12).
 \tag{3}
\]
Define
\[
\begin{aligned}
 B_{\widehat1}
 &=E\otimes E+F\otimes F,\\
 B_{\widehat2}
 &=\frac23\left(F\otimes Z_0+E\otimes Z_1\right),\\
 B_{\widehat3}
 &=\frac23\left(F\otimes Z_0+E\otimes Z_1\right),
\end{aligned}
\tag{4}
\]
where the tensor factors of \(B_{\widehat i}\) are the two physical
sites other than \(i\), in increasing order.  Insert the spectator
identity to obtain \(D_{\widehat i}\).

Every simple tensor in (4) has two traceless factors, so all three
pair coefficients are doubly traceless.  Orthogonality of the displayed
summands gives
\[
 (b_1,b_2,b_3)
 =
 \left(\|B_{\widehat1}\|_2^2,
       \|B_{\widehat2}\|_2^2,
       \|B_{\widehat3}\|_2^2\right)
 =
 \left(2,\frac43,\frac43\right).
 \tag{5}
\]

Put
\[
 r=|100\rangle,\qquad s=|011\rangle.
 \tag{6}
\]
Direct action on the two code columns gives
\[
\begin{array}{c|cc}
 &V|0\rangle&V|1\rangle\\ \hline
 X_1&s&r\\
 X_2&\frac23r&\frac23s\\
 X_3&\frac23r&\frac23s .
\end{array}
\tag{7}
\]
Thus the six logical inputs split into two orthogonal, perfectly
aligned triples: one ending at \(r\), and one ending at \(s\).

## 2. Exact residual inertia

Order the six input labels as
\[
 (1,0),(1,1),(2,0),(2,1),(3,0),(3,1).
\]
After the permutation
\[
 \bigl((1,0),(2,1),(3,1)\bigr)
 \oplus
 \bigl((1,1),(2,0),(3,0)\bigr),
\]
equation (7) gives
\[
 {\mathbb N}\simeq H\oplus H,
 \qquad
 H=
 \begin{pmatrix}
 1&-\frac23&-\frac23\\
 -\frac23&\frac89&-\frac49\\
 -\frac23&-\frac49&\frac89
 \end{pmatrix}.
 \tag{8}
\]
The leading principal minors of \(H\) are
\[
 \Delta_1=1,\qquad
 \Delta_2=\frac49,\qquad
 \Delta_3=-\frac{16}{27}.
 \tag{9}
\]
Hence the exact \(LDL^\dagger\) pivots are
\[
 1,\qquad \frac49,\qquad-\frac43.
 \tag{10}
\]
Sylvester inertia therefore gives
\[
 \operatorname{inertia}(H)=(2,1,0),
 \qquad
 \boxed{\operatorname{inertia}({\mathbb N})=(4,2,0)}.
 \tag{11}
\]

There is also a transparent normalized form.  With
\[
 {\cal B}=\operatorname{diag}
 \left(2,\frac43,\frac43\right),
 \qquad
 z=\left(\frac1{\sqrt2},
          \frac1{\sqrt3},
          \frac1{\sqrt3}\right)^{\mathsf T},
 \]
one has
\[
 {\cal B}^{-1/2}H{\cal B}^{-1/2}=I_3-zz^\dagger,
 \qquad
 \|z\|^2=\frac76.
 \tag{12}
\]
Thus each aligned output triple contributes exactly one negative
direction.

The second compound is genuinely indefinite.  For example, with
\[
 q=(1,1,1)^{\mathsf T},\qquad p=(0,1,-1)^{\mathsf T},
 \]
one has \(q^\dagger Hp=-0\) and
\[
 (q^\dagger Hq)(p^\dagger Hp)-|q^\dagger Hp|^2
 =
 -\frac{56}{27}<0.
 \tag{13}
\]
This is precisely the quadratic form of
\(\bigwedge^2H\) on \(q\wedge p\).

## 3. The scalar determinant remains strictly positive

Taking the logical traces gives
\[
 (d_1,d_2,d_3)
 =
 \left(2,\frac{16}{9},\frac{16}{9}\right),
 \tag{14}
\]
and
\[
 c_{12}=c_{13}=0,\qquad c_{23}=\frac89.
 \tag{15}
\]
Consequently
\[
 M=
 \begin{pmatrix}
 2&0&0\\
 0&\frac{16}{9}&-\frac89\\
 0&-\frac89&\frac{16}{9}
 \end{pmatrix},
 \tag{16}
\]
with
\[
 \operatorname{spec}M
 =
 \left\{2,\frac89,\frac83\right\},
 \qquad
 \det M=\frac{128}{27}>0.
 \tag{17}
\]

The example therefore shows that the logical spin-flip completion
does more than repair a single exceptional direction.  It can cancel
a two-dimensional negative residual sector while leaving a strictly
positive scalar deficit.  A successful Cayley--Hamilton or
exterior-algebra proof must combine both logical channels before
asserting positivity; negative-index-one control of
\({\mathbb N}\) is false.
