# Coherent Hodge leakage can vanish in every parity sector

## Status

The determinant-critical Hessian gives, for every paired motion of the
left and right singular planes,
\[
 \frac{|p|+|q|}{\sqrt{AB}}\leq 1.
\tag{1}
\]
A proposed physical bridge was to build the motions canonically from
the one-, two-, and three-skew Hodge components of the two code
planes.  The previously known full-support example only showed that
the triple-skew vector can vanish.

This note gives a stronger exact obstruction.  There is a
two-dimensional qutrit code with full local support for which **every
coherent local-parity component of every logical matrix has zero mixed
block**.  Consequently all coherent one-, two-, and three-skew plane
leakages vanish simultaneously.  Adding the parity sectors after first
performing their Pluecker-coherent sum therefore cannot prove (1).

The exterior information has not disappeared.  Each parity component
has a nonzero normal--normal block.  Moreover, if the individual
Fierz labels are retained before summing, the even and odd label
families separately give the universal tight leakage frame
\[
 \sum_T J_T^\dagger J_T=\frac{25}{2}I_2.
\tag{2}
\]
This yields a lossless replacement for the failed coherent
construction: a signed, individual-label Fierz colligation.  At a
critical point its normal residual has the exact formula (24) below.
Thus the remaining bridge is a signed fourth-moment inequality for
two linked tight frames, not an inequality between the four
parity-summed Hodge vectors.

This is an obstruction to an intermediate proof mechanism, not a
negative Werner witness.  The exact checker is
`verification/verify_n3_coherent_hodge_leakage_obstruction.py`.

## 1. Local-transpose parity

Put
\[
 {\cal H}=(\mathbb C^3)^{\otimes3}.
\]
For a coefficient matrix \(D\in M_{27}\), let \(\tau_iD\) be the
partial transpose of its \(i\)-th qutrit tensor factor.  The three
\(\tau_i\)'s are commuting Hilbert--Schmidt orthogonal involutions.
For \(R\subseteq[3]\), define their joint spectral projection
\[
 \Pi_R
 =
 2^{-3}
 \prod_{i\in R}(I-\tau_i)
 \prod_{i\notin R}(I+\tau_i).
\tag{3}
\]
Thus
\[
 \tau_i\Pi_R=(-1)^{1_{i\in R}}\Pi_R,\qquad
 (\Pi_R D)^{\mathsf T}=(-1)^{|R|}\Pi_R D.
\tag{4}
\]
The sectors with respectively one, two, and three elements of \(R\)
are precisely the one-, two-, and three-skew tensor-matrix sectors.

Let \(U:\mathbb C^2\to{\cal H}\) be an isometry and
\(P=UU^\dagger\).  The coherent parity leakage of a logical matrix
\(M\in M_2\) is
\[
 {\mathscr X}_{R,U}(M)
 =(I-P)\Pi_R(UMU^\dagger)U.
\tag{5}
\]
For odd \(R\), (5) is the mixed block of the Hodge/Pluecker component
of the logical bivector.  Formula (5) also includes the even
two-skew components which can be obtained by polarizing the three
logical symmetric tensors.

## 2. A full-support simultaneous zero

Define the orthonormal codewords
\[
\begin{aligned}
 u_0&=\frac{|000\rangle+|111\rangle+|222\rangle}{\sqrt3},\\
 u_1&=\frac{|012\rangle+|120\rangle+|201\rangle}{\sqrt3},
\end{aligned}
\tag{6}
\]
and put \(U=(u_0,u_1)\).

### Theorem 2.1

The code (6) has the following properties.

1. Its code projection has full local support at all three sites:
   \[
   \operatorname{Tr}_{\widehat i}P=\frac23I_3
   \qquad(i=1,2,3).
   \tag{7}
   \]
2. For every \(R\subseteq[3]\) and every \(M\in M_2\),
   \[
   \boxed{\qquad
   (I-P)\Pi_R(UMU^\dagger)U=0.
   \qquad}
   \tag{8}
   \]
   By (4), the adjoint mixed block vanishes as well.  Hence \(U\) is a
   reducing subspace of every parity component of its full logical
   matrix algebra.
3. The parity components in (8) are not zero.  Their normal--normal
   blocks have the positive squared norms listed in (13)--(14).

### Proof

Both strings in each codeword contain every qutrit label exactly once
at each physical site.  Their supports are disjoint.  Each codeword
therefore has one-site density \(I_3/3\), which proves (7).

It remains to check (8).  By linearity it suffices to use the four
matrix units
\[
 E_{ab}=u_au_b^\dagger,\qquad a,b\in\{0,1\}.
\tag{9}
\]
Write
\[
 X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
\tag{10}
\]
Direct application of the eight signs in (3) gives the following
complete table.  An entry displays
\[
 \left(U^\dagger\Pi_R(E_{ab})U,\,
       \|\Pi_R(E_{ab})\|_2^2\right);
\tag{11}
\]
every unlisted entry is zero:
\[
\begin{array}{c|c|c}
E_{ab}&R&\text{entry in (11)}\\ \hline
E_{00}&\varnothing&(\frac12E_{00},\frac12)\\
E_{00}&|R|=2&(\frac16E_{00},\frac16)\\
E_{11}&\varnothing&(\frac12E_{11},\frac12)\\
E_{11}&|R|=2&(\frac16E_{11},\frac16)\\
E_{01}&\varnothing&(\frac14X,\frac14)\\
E_{01}&|R|=1&(\frac16J,\frac16)\\
E_{01}&|R|=2&(\frac1{12}X,\frac1{12})\\
E_{10}&\varnothing&(\frac14X,\frac14)\\
E_{10}&|R|=1&(-\frac16J,\frac16)\\
E_{10}&|R|=2&(\frac1{12}X,\frac1{12}).
\end{array}
\tag{12}
\]
The three choices of a subset having the indicated cardinality give
the same displayed entry.

The coefficient of a basis string in
\(\Pi_R(E_{ab})u_c\) is an eight-term signed sum.  Substituting the
three support strings from (6) shows that the result is exactly the
corresponding column of the \(2\times2\) matrix in (12).  Therefore
\(\Pi_R(E_{ab})U=U[U^\dagger\Pi_R(E_{ab})U]\), which is (8).
This calculation uses only the integer incidence table of the two
three-string supports; the factors \(1/3\) and \(1/8\) are the
normalization of (6) and (3).

Because the mixed blocks vanish, Pythagoras and (12) give the
normal--normal squared norms.  For the two diagonal matrix units they
are
\[
\begin{array}{c|cc}
 &R=\varnothing&|R|=2\\ \hline
\|(I-P)\Pi_R(E_{aa})(I-P)\|_2^2
 &\frac14&\frac5{36},
\end{array}
\tag{13}
\]
and for either off-diagonal matrix unit they are
\[
\begin{array}{c|ccc}
 &R=\varnothing&|R|=1&|R|=2\\ \hline
\|(I-P)\Pi_R(E_{ab})(I-P)\|_2^2
 &\frac18&\frac19&\frac5{72}.
\end{array}
\tag{14}
\]
These numbers are strictly positive.  This proves all three claims.
\(\square\)

### Consequence

The triple-Hodge vector of (6) vanishes because
\(\Pi_{\{1,2,3\}}(u_0u_1^\dagger-u_1u_0^\dagger)=0\).
Theorem 2.1 is strictly stronger:
\[
 {\mathscr X}_{R,U}(M)=0
 \quad\text{simultaneously for every }R,M.
\tag{15}
\]
Thus adding the three one-skew channels and the three two-skew
channels to the triple-skew channel does not repair the canonical
coherent leakage.  The nonzero quantities in (13)--(14) live wholly
in the normal--normal block and are discarded by (5).

## 3. The individual-label leakage frame does not vanish

The cancellation in (15) occurs only after coherently summing the
individual matrix labels inside a parity sector.  Retaining those
labels gives an exact tight frame.

Let \(N\geq2\), let \(U:\mathbb C^2\to\mathbb C^N\) be any isometry,
and put \(P=UU^\dagger\).  Let \({\cal B}_-\) and \({\cal B}_+\) be
Hilbert--Schmidt orthonormal bases of the transpose-skew and
transpose-symmetric matrices, respectively.  Define
\[
 J_T=(I-P)T\overline U.
\tag{16}
\]

### Theorem 3.1 (two tight leakage frames)

For either choice of sign,
\[
 \boxed{\qquad
 \sum_{T\in{\cal B}_\pm}J_T^\dagger J_T
 =\frac{N-2}{2}I_2.
 \qquad}
\tag{17}
\]
For \(N=27\), this is (2).  If the bases are tensor products of local
qutrit symmetric/skew bases, then the union over even subsets \(R\)
is \({\cal B}_+\), and the union over odd subsets is \({\cal B}_-\).
Thus (17) is exactly a coherent statement combining all local
parities without mixing their individual Fierz labels.

### Proof

For a transpose-skew orthonormal basis,
\[
 \sum_{T\in{\cal B}_-}T^\dagger T=\frac{N-1}{2}I_N.
\tag{18}
\]
Moreover \(U^\dagger T\overline U\) is a \(2\times2\)
skew-symmetric matrix.  Parseval on
\(\bigwedge^2\mathbb C^2\), which has dimension one, gives
\[
 \sum_{T\in{\cal B}_-}
 (U^\dagger T\overline U)^\dagger
 (U^\dagger T\overline U)
 =\frac12I_2.
\tag{19}
\]
Subtracting the squared projection onto \(U\) from (18) proves (17)
for the minus sign.

For a symmetric basis,
\[
 \sum_{T\in{\cal B}_+}T^\dagger T=\frac{N+1}{2}I_N.
\tag{20}
\]
Now \(U^\dagger T\overline U\) is symmetric.  Parseval on
\(\operatorname{Sym}^2\mathbb C^2\) gives
\[
 \sum_{T\in{\cal B}_+}
 (U^\dagger T\overline U)^\dagger
 (U^\dagger T\overline U)
 =\frac32I_2.
\tag{21}
\]
Subtracting (21) from (20) again gives (17). \(\square\)

The constants in (17) are independent of the code plane.  In
particular the full-support plane of Theorem 2.1, despite (15), has
individual-label leakage mass \(25/2\) in each global transpose
parity.

## 4. Exact Fierz colligation at a critical point

Choose real Hilbert--Schmidt orthonormal symmetric and skew qutrit
matrix bases.  Let \(T_{R\mu}\) run through their tensor products with
local skew set \(R\).  Put
\[
 w_R=2^{-3}3^{|R|},\qquad \eta_R=(-1)^{|R|}.
\tag{22}
\]
The qutrit endpoint superoperator has the exact completely
copositive Fierz expansion
\[
 {\cal L}(D)
 =\sum_{R,\mu}\eta_Rw_R
 T_{R\mu}D^{\mathsf T}T_{R\mu}^\dagger.
\tag{23}
\]

Let
\[
 C=U\Sigma V^\dagger,\qquad
 \Sigma=\operatorname{diag}(r,r^{-1}),
\]
be a determinant-critical candidate, and write
\[
\begin{aligned}
 A_T&=U^\dagger T\overline V,\\
 X_T&=(I-P_U)T\overline V,\\
 Z_T&=(I-P_V)T\overline U.
\end{aligned}
\]
Since \(T^{\mathsf T}=\eta_RT\),
\[
 V^\dagger T\overline U=\eta_RA_T^{\mathsf T}.
\]
Substitution in (23) gives the following exact block colligation:
\[
\boxed{
\begin{aligned}
 U^\dagger{\cal L}(C)V
 &=\sum_{R,\mu}w_R A_T\Sigma\overline{A_T},\\
 (I-P_U){\cal L}(C)V
 &=\sum_{R,\mu}w_RX_T\Sigma\overline{A_T},\\
 U^\dagger{\cal L}(C)(I-P_V)
 &=\sum_{R,\mu}\eta_Rw_RA_T\Sigma Z_T^\dagger,\\
 R_{\rm n}:=(I-P_U){\cal L}(C)(I-P_V)
 &=\sum_{R,\mu}\eta_Rw_RX_T\Sigma Z_T^\dagger.
\end{aligned}}
\tag{24}
\]
Equivalently one may replace \(Z_T\) by the parity-twisted frame
\(\widehat Z_T=\eta_RZ_T\).  Then the last two lines have positive
weights, with the physical sign stored in the relation between the
two individual-label frames.

At a critical point, the first three lines reduce to
\[
\begin{aligned}
 \sum_Tw_TA_T\Sigma\overline{A_T}&=\lambda\Sigma^{-1},\\
 \sum_Tw_TX_T\Sigma\overline{A_T}&=0,\\
 \sum_T\eta_Tw_TA_T\Sigma Z_T^\dagger&=0.
\end{aligned}
\tag{25}
\]
In particular the normal residual retains the physical relative
parity sign \(\eta_R\) (or, equivalently, the right leakage frame is
parity twisted).  The singular-component scalars are
\[
\boxed{
\begin{aligned}
 a_0&=\sum_Tw_T|(A_T)_{11}|^2,\\
 b_0&=\sum_Tw_T|(A_T)_{22}|^2,\\
 c_0&=\sum_Tw_T(A_T)_{12}\,
                    \overline{(A_T)_{21}}.
\end{aligned}}
\tag{26}
\]
Thus the strict reverse-Cauchy defect is a positive-weighted
correlation inside the common core frame, whereas the normal
curvature in the Hessian comes from the signed fourth line of (24).

Equations (17), (24), and (26) isolate the surviving physical bridge:

> Given two tensor-Fierz colligations arising from the same pair of
> qutrit code planes and satisfying (25), prove that a core defect
> \(|c_0|^2>a_0b_0\) forces the generalized real-linear correlation
> norm of the signed normal block in the last line of (24) to exceed
> one.

This is strictly more specific than the unrestricted leakage search:
all variables are blocks of the same fixed tensor matrices
\(T_{R\mu}\), the two individual-label leakage families obey the
tight identities (17), and the parity twist survives in the right
mixed and normal blocks.
Theorem 2.1 proves that the labels cannot first be collapsed to the
eight parity sums.  Any successful one-/two-/three-skew bridge must
retain at least their individual-label fourth moments or an
equivalent normal--normal invariant.

## Exact status

Established here:

1. a full-local-support physical code on which every coherent
   one-, two-, and three-skew leakage vanishes;
2. exact nonzero normal-block masses showing where the discarded
   information resides;
3. two universal individual-label tight leakage frames;
4. the exact signed Fierz block colligation (24) at a determinant
   critical point.

Not established:

1. the remaining signed fourth-moment inequality after (26);
2. unrestricted three-copy positivity;
3. an exact negative three-copy Werner witness.
