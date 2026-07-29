# Equality geometry on the qutrit pair-sector boundary

## Status

This note proves three exact results about
\[
 {\cal G}(C):=\frac23\|C\|_2^2-\|\Pi _2C\|_2^2 .
 \tag{1}
\]

1. Equality on the established one-site-support boundary has the rigid
   sector distribution
   \[
   (w_0,w_1,w_2,w_3)=(0,0,2/3,1/3).
   \tag{2}
   \]
2. There are at least two geometrically inequivalent exact equality
   mechanisms: a factor--Hodge family and a trace-zero three-qubit
   spin-flip family.  Thus equality is not one local-unitary orbit of
   the displayed matrix-unit example.
3. At their canonical intersection
   \[
   C_0=|000\rangle\langle110|+|001\rangle\langle111|,
   \tag{3}
   \]
   the complete constrained Hessian of \({\cal G}\) is positive
   semidefinite, with rank \(165\) and nullity \(39\).  Every
   Hessian-flat first-order leakage out of the deficient third-site
   support is induced by moving that same two-dimensional support.
   Hence no genuinely support-opening branch with
   \(\|\Pi _2C\|^2/\|C\|^2>2/3\) can bifurcate from (3) at quadratic
   order.

These results do **not** classify every boundary equality point, and
they do not exclude a distant full-support equality point.  The
converse assertion that all equality points belong to the two families
below remains unproved.

The independent exact Hessian checker is
`verification/verify_n3_pair_boundary_hessian.py`.

## 1. Sector rigidity

Let
\[
 w_k=\frac{\|\Pi_kC\|_2^2}{\|C\|_2^2},\qquad
 \sum_{k=0}^3w_k=1.
 \tag{4}
\]
The endpoint form has eigenvalues
\[
 -\frac18,\quad\frac14,\quad-\frac12,\quad1
 \tag{5}
\]
on degrees \(0,1,2,3\), respectively.  Therefore
\[
 \frac{Q_3(C)}{\|C\|_2^2}
 =
 1-\frac98w_0-\frac34w_1-\frac32w_2.
 \tag{6}
\]

Suppose that one left or right singular plane of \(C\) has deficient
one-site qutrit support.  The established local-support theorem gives
\(Q_3(C)\geq0\).  Equation (6) then gives the sharper boundary estimate
\[
 \boxed{\qquad
 w_2\leq\frac23-\frac34w_0-\frac12w_1.
 \qquad}
 \tag{7}
\]
Consequently \(w_2=2/3\) is possible only if
\[
 w_0=w_1=0,\qquad Q_3(C)=0.
 \tag{8}
\]
Normalization then forces \(w_3=1/3\), proving (2).

Equivalently, every boundary equality matrix obeys
\[
 \operatorname{Tr}C=0,\qquad
 \operatorname{Tr}_{\widehat i}C=0\quad(i=1,2,3),
 \tag{9}
\]
and has only exact degrees two and three.  This is a useful intrinsic
canonical sector form, but by itself it is not yet an orbit
classification.

The identity behind (7), valid without a support assumption, is
\[
 \boxed{\qquad
 {\cal G}(C)
 =\frac23Q_3(C)
  +\frac34\|\Pi_0C\|_2^2
  +\frac12\|\Pi_1C\|_2^2.
 \qquad}
 \tag{10}
\]

There is also a global equality dichotomy which does not assume the
pair-sector theorem.  If an arbitrary normalized rank-two matrix has
\(w_2=2/3\), then (6) and
\(w_3=1/3-w_0-w_1\) give
\[
 \boxed{\qquad
 \frac{Q_3(C)}{\|C\|_2^2}
 =-\frac98w_0-\frac34w_1.
 \qquad}
 \tag{10a}
\]
Thus a full-support \(f=2/3\) code with either low sector nonzero is
already an exact negative three-copy witness.  A harmless full-support
equality would have to satisfy the strictly smaller algebraic system
\[
 \Pi_0C=\Pi_1C=0,\qquad
 \|\Pi_2C\|_2^2=\frac23\|C\|_2^2,
 \tag{10b}
\]
and would be an endpoint zero.  No such full-support code is presently
known.

## 2. A factor--Hodge equality family

Let \(a,b\in\mathbb C^3\otimes\mathbb C^3\), and let \(A,B\in M_3\)
be their coefficient matrices.  Assume
\[
 AB^\dagger=0,\qquad B^\dagger A=0.
 \tag{11}
\]
These are exactly the two conditions
\[
 \operatorname{Tr}_2|a\rangle\langle b|=0,\qquad
 \operatorname{Tr}_1|a\rangle\langle b|=0.
 \tag{12}
\]
Thus the rank-one operator \(|a\rangle\langle b|\) lies entirely in
the two-site fully traceless sector.

Let \(W\subset\mathbb C^3\) be a two-plane and \(P_W\) its orthogonal
projection.  Then
\[
 C_{\rm fac}=|a\rangle\langle b|\otimes P_W
 \tag{13}
\]
has rank two.  Since
\[
 \left\|\frac{\operatorname{Tr}P_W}{3}I_3\right\|_2^2
 =\frac43,\qquad
 \left\|P_W-\frac23I_3\right\|_2^2=\frac23,
 \tag{14}
\]
while \(\|P_W\|_2^2=2\), tensor-sector orthogonality gives
\[
 (w_0,w_1,w_2,w_3)=(0,0,2/3,1/3).
 \tag{15}
\]
Hence \({\cal G}(C_{\rm fac})=Q_3(C_{\rm fac})=0\).

This family is already larger than the simple product-matrix orbit.
For example,
\[
 \left(
 |00\rangle\langle11|+|00\rangle\langle22|
 \right)\otimes P_{\operatorname{span}\{|0\rangle,|1\rangle\}}
 \tag{16}
\]
is an exact equality matrix.  Its left one-site support ranks are
\((1,1,2)\), while its right ranks are \((2,2,2)\).  The canonical
matrix (3) has ranks \((1,1,2)\) on both sides, so (16) is not related
to (3) by local unitaries, site permutations, phase, or adjunction.

## 3. The trace-zero spin-flip equality family

Choose local two-planes \(W_i\subset\mathbb C^3\), with isometries
\(T_i:\mathbb C^2\to W_i\), and put \(T=T_1\otimes T_2\otimes T_3\).
On a qubit set
\[
 \epsilon=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
 \qquad J=\epsilon^{\otimes3}.
 \tag{17}
\]
For an isometry
\[
 U:\mathbb C^2\longrightarrow(\mathbb C^2)^{\otimes3},
 \tag{18}
\]
define
\[
 V=-J\overline U\,\epsilon,\qquad
 C_{\rm sf}=TUV^\dagger T^\dagger.
 \tag{19}
\]
Both \(U\) and \(V\) are isometries, so \(C_{\rm sf}\) is a rank-two
partial isometry and \(\|C_{\rm sf}\|_2^2=2\).

The established spin-flip identity gives
\[
 Q_3(C_{\rm sf})=0.
 \tag{20}
\]
There is a sharper marginal identity.  Put
\(\tau=\operatorname{Tr}C_{\rm sf}\).  Then
\[
 \boxed{\qquad
 \operatorname{Tr}_{\widehat i}C_{\rm sf}
 =\frac{\tau}{2}P_{W_i}\quad(i=1,2,3).
 \qquad}
 \tag{21}
\]

Here is a direct proof.  Work first in the qubit frames and write
\[
 \Omega=U\epsilon U^{\mathsf T},\qquad C_{\rm sf}=-\Omega J.
 \]
Across the cut \(i:\widehat i\), contract the two complementary
indices of \(\Omega\) against
\(J_{\widehat i}=\epsilon\otimes\epsilon\).  The latter is symmetric,
whereas \(\Omega\) is skew-symmetric.  The resulting \(2\times2\)
matrix \(M_i\) is skew-symmetric, hence \(M_i=m_i\epsilon\).
Multiplication by the remaining local \(\epsilon\) turns the partial
trace into \(m_iI_2\).  Its trace is \(\tau\), so
\(m_i=\tau/2\).  Embedding by \(T_i\) proves (21).

Let \(t=|\tau|^2\).  Equations (21), scalar/traceless orthogonality,
and \(\|C_{\rm sf}\|_2^2=2\) give
\[
 \boxed{
 \begin{aligned}
 w_0&=\frac{t}{54},&
 w_1&=\frac{t}{36},\\
 w_2&=\frac23-\frac{t}{36},&
 w_3&=\frac13-\frac{t}{54}.
 \end{aligned}}
 \tag{22}
\]
Indeed the unnormalized scalar mass is \(t/27\).  For each site,
\[
 \left\|
 \frac{\tau}{2}\left(P_{W_i}-\frac23I_3\right)
 \right\|_2^2=\frac t6,
 \]
and restoring the two identity factors divides this by \(9\), so the
total unnormalized degree-one mass is \(t/18\).  The last two lines of
(22) then follow from normalization and (20).

Consequently
\[
 \boxed{\qquad
 {\cal G}(C_{\rm sf})=0
 \quad\Longleftrightarrow\quad
 \operatorname{Tr}C_{\rm sf}=0.
 \qquad}
 \tag{23}
\]
This trace-zero spin-flip family has deficient support on both sides
at every site and contains generic-looking, nonfactor equality
matrices.

## 4. Exact outward Hessian at the canonical intersection

Parameterize rank-two partial isometries near (3) as
\[
 C(t)=U(t)V(t)^\dagger
 \tag{24}
\]
using independent polar Stiefel charts and one relative logical
\(\mathfrak u(2)\) coordinate.  The real chart dimension is \(204\).

### Theorem

The Hessian of \({\cal G}\) at \(C_0\) is positive semidefinite and has
\[
 \boxed{\qquad
 \operatorname{rank}\operatorname{Hess}_{C_0}{\cal G}=165,
 \qquad
 \operatorname{nullity}\operatorname{Hess}_{C_0}{\cal G}=39.
 \qquad}
 \tag{25}
\]
Its exact connected-block profile is
\[
\begin{array}{c|c|c|c}
\text{block size}&\text{rank}&\text{diagonal value}&\text{multiplicity}\\
\hline
1&1&1/3&48\\
1&1&2/3&48\\
1&1&2/9&8\\
1&1&4/3&2\\
2&1&1/3&21\\
2&1&2/3&4\\
2&1&2/9&4\\
2&2&2/9&8\\
4&2&2/9&4\\
4&3&2/9&2.
\end{array}
\tag{26}
\]

Fix the deficient left support at site three:
\[
 \operatorname{span}\{|0\rangle,|1\rangle\}.
 \]
There are \(36\) real first-order left-frame coordinates whose row
index has third digit \(2\).  The projection of the \(39\)-dimensional
Hessian kernel onto these coordinates is exactly the four-dimensional
space
\[
 \begin{aligned}
 \delta u_0&=\alpha\,|002\rangle,\\
 \delta u_1&=\beta\,|002\rangle,
 \end{aligned}
 \qquad \alpha,\beta\in\mathbb C.
 \tag{27}
\]
These are precisely the variations induced by moving the common local
two-plane itself.  The matching right-frame variations are
\[
 \delta v_0=\alpha\,|112\rangle,\qquad
 \delta v_1=\beta\,|112\rangle.
 \tag{28}
\]

There is a sharp quantitative version of this support-opening
statement.  Put
\[
 \rho_3^U(t)=\operatorname{Tr}_{12}P_{U(t)},\qquad
 \rho_3^V(t)=\operatorname{Tr}_{12}P_{V(t)}.
 \tag{28a}
\]
Both base reductions are
\(\operatorname{diag}(1,1,0)\).  If \(X=\dot U(0)\) and
\(Y=\dot V(0)\), the Schur-complement expansion of the determinant
gives
\[
\begin{aligned}
 \det\rho_3^U(t)
 &=t^2\Delta_U(X)+O(t^3),&
 \Delta_U(X)
 &=\sum_{\substack{a,b,r\\(a,b)\ne(0,0)}}
   |X_{(a,b,2),r}|^2,\\
 \det\rho_3^V(t)
 &=t^2\Delta_V(Y)+O(t^3),&
 \Delta_V(Y)
 &=\sum_{\substack{a,b,r\\(a,b)\ne(1,1)}}
   |Y_{(a,b,2),r}|^2.
\end{aligned}
\tag{28b}
\]
Indeed, the omitted terms are exactly the projections of the new
local-\(2\) environment vector onto the two old environment vectors;
they are common-plane motions and do not increase local support.

All \(64\) real coordinates occurring in
\(\Delta_U+\Delta_V\) are isolated one-dimensional blocks of the
pair-deficit Hessian.  Their diagonal coefficients belong to
\[
 \left\{\frac29,\frac13,\frac23\right\}.
 \tag{28c}
\]
The remaining Hessian blocks are positive semidefinite.  Consequently
every polar-chart curve obeys the sharp second-order estimate
\[
 \boxed{\qquad
 {\cal G}(C(t))
 \geq
 \frac29t^2\bigl(\Delta_U(X)+\Delta_V(Y)\bigr)+O(t^3).
 \qquad}
 \tag{28d}
\]
The coefficient \(2/9\) is attained, for example, by a single
left-frame direction with row \((1,1,2)\), or the corresponding
right-frame direction with row \((0,0,2)\).  Thus (28d) is an exact
local determinant gap, not merely strictness of the outward Hessian.

There is also an exact first-order classification of the entire flat
space.  The tangent to the unrestricted factorized \(Q_3\)-zero family
at \(C_0\) has dimension \(37\); its intersection with the Hessian
kernel of \({\cal G}\) has dimension \(21\).  The tangent to the
spin-flip \(Q_3\)-zero family also has dimension \(37\); imposing the
linearized trace-zero condition leaves dimension \(35\).  Exact row
reduction gives
\[
 \boxed{\qquad
 \ker\operatorname{Hess}_{C_0}{\cal G}
 =
 T_{\rm fac}^{\,\rm flat}+T_{\rm sf}^{\,\rm flat},
 \qquad
 \dim(21+35)=39.
 \qquad}
 \tag{29}
\]
Thus there is no third unexplained first-order flat mechanism at the
canonical intersection.  A sum of vectors tangent to the two different
families need not itself integrate into either family, so (29) is a
first-order statement, not a full local equality classification.

Thus if a first-order variation genuinely opens the one-site support
rather than merely moving the deficient plane, its quadratic
coefficient in \({\cal G}\) is strictly positive.  Equivalently, no
interior branch with value above \(2/3\) leaves \(C_0\) with a
support-opening first derivative.

The proof of (25)--(29) is the finite exact calculation in the
verifier.  It starts from the matrix-unit kernel of \(\Pi_2\),
constructs every polar-chart coefficient over \(\mathbb Q\), checks
all \(204^2\) Hessian entries, performs exact symmetric elimination on
every block, reconstructs the \(39\)-dimensional kernel, and compares
its leakage projection with (27)--(28).

## 5. What remains

The exact information obtained here narrows, but does not finish, the
global equality problem:

* every equality point on the proved support boundary has (2);
* the known factor and spin-flip mechanisms are intrinsically
  different and must both occur in any classification;
* a genuinely full-support equality, if it exists, is not a quadratic
  bifurcation from the canonical intersection (3), and its
  second-order support opening is penalized by the sharp determinant
  constant \(2/9\).

A complete boundary classification still requires equality conditions
for the separable compressed one-site form together with the exact
two-copy theorem.  A global statement that every \(f=2/3\) code has
deficient one-site support would be stronger still and is not proved
by this Hessian calculation.
