# Root-killing phase blocks for the fitness-two product target

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note gives a **PROVED exact finite-matrix identity** for the decisive
cross-rule product target

\[
                         m_Lm_D\le b_nd_n.                    \tag{1}
\]

It combines the weighted adjoint `L^T=C+V` and the target-locked geometric
resolvent before taking a determinant.  Both endpoint means become
root-killing derivatives of two phase blocks with the same off-diagonal
coupling.  Consequently `(1)` is one coefficient inequality between two
block determinants.

The first canonical Hermitian Schur/Hadamard--Fischer route is then
**EXACTLY OBSTRUCTED**.  The two upper-left blocks differ by the selective
Laplacian `(I-S)/2`, whose symmetric part is indefinite in every positive
diagonal metric.  This failure occurs already on the complete graph.  The
lower adjoint potential has both signs on the weighted three-path and on a
four-vertex orientation witness.  These facts do not refute a genuinely
nonsymmetric `M`-matrix or arborescence inequality, and `(1)` remains open.

No literature search or external communication was used.

## 1. Root-killing derivatives

Let `Q` be an irreducible row generator on a finite state space and put
`R=-Q`.  If `tau(x)` is its rooted in-tree cofactor and
`W=diag(w_x)`, multilinearity in the diagonal gives

\[
 \left.{d\over ds}\det(R+sW)\right|_{s=0}
       =\sum_x\tau(x)w_x.                                  \tag{2}
\]

In particular, if `K=diag(|A|)` on the nonempty subsets,

\[
 m_L=
 {\partial_s\det(-Q_L+sK)|_{0}\over
  \partial_s\det(-Q_L+sI)|_{0}}.                            \tag{3}
\]

For dB, use its target-event kernel `K_D` on all nonempty subsets.  The full
set is transient and the proper nonempty sets form the unique closed class.
Put `R_D=I-K_D`.  Its full-set cofactor is zero, and the other cofactors are
the event-Palm tree weights `theta_D`.  Hence

\[
 {1\over m_D}=
 {\partial_s\det(R_D+sK^{-1})|_{0}\over
  \partial_s\det(R_D+sI)|_{0}}.                             \tag{4}
\]

Equations `(3)--(4)` already express the product target as a cross-product
of four root-killing determinant derivatives.  The next section puts the
two matrices over the same original arrows.

## 2. Marked arrow matrices

Let

\[
 \Omega=2^V\setminus\{\varnothing\},\qquad
 \mathcal Y=\{(A,v):A\in\Omega, v\in A\}.
\]

All matrices below act on row distributions.  Define:

- `J : Omega -> Y`, which chooses `v` uniformly from `A`;
- `F : Y -> Omega`, which forgets the target;
- `S : Y -> Y`, one selective row-`P_v` sample retaining `v`; and
- `N : Y -> Omega`, one neutral row-`P_v` replacement followed by target
  forgetting.

Thus

\[
 JF=I_\Omega.                                               \tag{5}
\]

Put

\[
 \mathcal C=SF+N-2F,qquad
 \mathcal A=I_\mathcal Y-{S\over2}.                         \tag{6}
\]

The unbatched reversed-arrow generator and the locked-target event kernel
are exactly

\[
 Q_C=KJ\mathcal C,                                         \tag{7}
\]

\[
 \begin{aligned}
 K_D-I
 &=\frac12J\mathcal A^{-1}\mathcal C,\\
 K_D&=\frac12J\mathcal A^{-1}N.                             \tag{8}
 \end{aligned}
\]

The equivalence of the two lines in `(8)` is the finite marked version of

\[
 (I-S_v/2)(G_v-I)=C_v/2.                                   \tag{9}
\]

At fitness two the ordinary transpose is the weighted adjoint, so

\[
                         Q_L^T=Q_C+V,                        \tag{10}
\]

where `V` is diagonal.

## 3. Two common-coupling phase blocks

For a diagonal killing matrix `W` on `Omega`, define

\[
 \boxed{
 \mathbb B_D(s;W)=
 \begin{pmatrix}
  \mathcal A&-\mathcal C/2\\
  -J&sW
 \end{pmatrix},}                                           \tag{11}
\]

and

\[
 \boxed{
 \mathbb B_L(s;W)=
 \begin{pmatrix}
  I_\mathcal Y/2&-\mathcal C/2\\
  -J&K^{-1}(sW-V)
 \end{pmatrix}.}                                           \tag{12}
\]

The off-diagonal blocks are now literally identical.  Schur complementation
of the upper-left blocks, using `(7)--(10)`, gives

\[
 \boxed{
 \det\mathbb B_D(s;W)
   =\det(\mathcal A)\det(R_D+sW),}                           \tag{13}
\]

\[
 \boxed{
 \det\mathbb B_L(s;W)
   ={\det(-Q_L+sW)\over2^{|\mathcal Y|}\det K}.}             \tag{14}
\]

For `(13)`, one may start from the standard phase-type `M`-matrix

\[
 \begin{pmatrix}
  \mathcal A&-N/2\\
  -J&I+sW
 \end{pmatrix}                                             \tag{15}
\]

and multiply on the right by the determinant-one triangular matrix

\[
 \begin{pmatrix}I_\mathcal Y&F\\0&I_\Omega\end{pmatrix}.
\]

This produces `(11)` because `JF=I` and
`mathcal A F-N/2=-mathcal C/2`.  Thus the common coupling is not an
invented ansatz; it is the exact phase elimination of the locked burst.

Write

\[
 \dot B_U(W)=left.\partial_s\det\mathbb B_U(s;W)\right|_{s=0}.
\]

The positive prefactors in `(13)--(14)` cancel in ratios, so

\[
 \boxed{
 m_L={\dot B_L(K)\over\dot B_L(I)},\qquad
 {1\over m_D}={\dot B_D(K^{-1})\over\dot B_D(I)}.}           \tag{16}
\]

This is the requested exact adjoint--resolvent determinant coupling.

## 4. One block coefficient exactly equivalent to `PAPT_n`

Define the two block-diagonal pencils

\[
 \begin{aligned}
 \mathbb P_+(s)&=\mathbb B_L(s;I)\oplus
                  \mathbb B_D(s;b_nd_nK^{-1}),\\
 \mathbb P_-(s)&=\mathbb B_L(s;K)\oplus
                  \mathbb B_D(s;I).
 \end{aligned}                                             \tag{17}
\]

Every determinant in `(17)` vanishes to first order at zero.  Therefore

\[
\begin{aligned}
 [s^2]\{\det\mathbb P_+(s)-\det\mathbb P_-(s)\}
 ={}&b_nd_n\dot B_L(I)\dot B_D(K^{-1})\\
    &-\dot B_L(K)\dot B_D(I).                               \tag{18}
\end{aligned}
\]

Using `(13)--(16)`, the right side is the positive factor

\[
 {\det(\mathcal A)\over2^{|\mathcal Y|}\det K}
\]

times the event-tree numerator

\[
 b_nd_nZ_L\Phi_D-Y_L\Theta_D.                               \tag{19}
\]

Consequently

\[
 \boxed{
 PAPT_n\quad\Longleftrightarrow\quad
 [s^2]\{\det\mathbb P_+(s)-\det\mathbb P_-(s)\}\ge0.}     \tag{20}
\]

This is one finite block-determinant sign, not a sufficient scalar
envelope.

## 5. Sharp obstruction to the canonical PSD/Hadamard--Fischer step

The common upper-left blocks in `(11)--(12)` differ by

\[
 \mathcal A-{I\over2}={I-S\over2}.                          \tag{21}
\]

A standard Hermitian Schur proof would try to regard `(21)` as positive in
a diagonal arrow metric.  This is impossible.  Choose an edge with
`P_vi=p>0`, and let

\[
 x=(V\setminus\{i\},v),\qquad y=(V,v).
\]

On these two marked states, the relevant principal block of `I-S` is

\[
 \begin{pmatrix}p&-p\\0&0\end{pmatrix}.                     \tag{22}
\]

For every positive diagonal metric `D=diag(d_x,d_y)`, the symmetric part of
`D(I-S)/2` has determinant

\[
                         -{d_x^2p^2\over16}<0.               \tag{23}
\]

Thus `(21)` is indefinite in every positive diagonal inner product.  On
`K_4`, one may take `p=1/3`, giving the exact minor determinant `-1/144` in
the Euclidean metric.  The failure is present even at the equality kernel,
so it is not a perturbative artifact of orientation.

The lower-right base blocks also have no order away from the complete
kernel.  At `s=0` they are `0` for dB and `-K^{-1}V` for `L`.  On the
weighted three-path with edge weights `w01=1,w02=2,w12=0`,

\[
 \min_A V(A)=-2,qquad \max_A V(A)=2.                        \tag{24}
\]

On the four-vertex orientation witness

\[
 w_{02}=1000, w_{03}=2, w_{12}=1, w_{13}=1000,
  w_{23}=10, w_{01}=0,                                   \tag{25}
\]

\[
 \min_A V(A)=-{10115\over255783},\qquad
 \max_A V(A)={10115\over255783}.                            \tag{26}
\]

Hence neither the upper nor lower common block admits the Loewner ordering
needed by the literal PSD Schur/Hadamard--Fischer argument.

Nor can one apply the standard nonsymmetric `M`-matrix
Hadamard--Fischer theorem directly to the common blocks `(11)--(12)`.  They
are not `Z`-matrices, and no diagonal sign change repairs this.  Indeed, for
`y=(A,v)`, looplessness gives

\[
 \mathcal C_{y,A}=P_v(A)-2<0.                               \tag{26a}
\]

Thus the common top-right entry `(-mathcal C/2)_(y,A)` is positive, whereas
the reverse bottom-left entry `(-J)_(A,y)=-1/|A|` is negative.  Any signature
similarity that keeps the latter nonpositive assigns the same sign to `y`
and `A`, and therefore leaves the former positive.  Positive diagonal
scalings do not change either sign.

The untransformed dB phase matrix `(15)` is an `M`-matrix, as is the
analogous untransformed `L` phase matrix, but their arrow blocks are no
longer identical.  Hence a nonsymmetric Hadamard--Fischer proof would need a
strictly larger master `M`-matrix and a nontrivial principal-minor
identification; it cannot be applied directly to the exact common-coupling
pencils.

There is one canonical attempt at such a master.  Duplicate the endpoint of
the selective arrow according to whether it returns to the locked target or
forgets the target:

\[
 \mathbb M(B)=
 \begin{pmatrix}
 I&-S/2&-S/2&-N/2\\
 -I&I&0&0\\
 0&0&I&-F\\
 -J&0&0&B
 \end{pmatrix}.                                             \tag{26b}
\]

The principal block on the first, second, and fourth sectors Schur-reduces
to the untransformed dB phase matrix.  The principal block on the first,
third, and fourth sectors Schur-reduces to the untransformed `L/C` phase
matrix with the same bottom block `B`.  Thus `(26b)` is the literal smallest
principal-minor master suggested by Hadamard--Fischer.

It is not an `M`-matrix.  Although it is a `Z`-matrix, on the unweighted
complete triangle at `B=I` its determinant is exactly

\[
                         \det\mathbb M(I)=-{27\over2048}<0.  \tag{26c}
\]

The duplicated selective channel overcounts the common arrow in the union
principal block.  Consequently the obvious larger-master repair also fails
at the equality kernel.  Any successful `M`-matrix embedding must identify
the shared selective arrow without duplicating its mass.

There is a second, independent warning.  The killed matrices are not
diagonally symmetrizable in general.  On the weighted three-path the `L`
cycle through masks `001,010,011` has forward and reverse rate products

\[
                         {1\over9}\ne {1\over3}.              \tag{27}
\]

The locked dB event graph has one-way transitions even on `K_4`.  Therefore
the determinant problem cannot be converted directly into two Hermitian
graph Laplacians.

Equations `(23)--(27)` refute the canonical Hermitian ordering, the direct
common-block `M`-matrix shortcut, and the smallest duplicated-phase master.
They do not refute a different nonsymmetric master block, a directed forest
exchange, or `(20)` itself.  Any successful determinant proof must use that
genuinely directed structure rather than a hidden reversible congruence.

## 6. Exact audit

`verify_root_killing_phase_block.py` constructs every matrix over `QQ`.  It
checks `(5)--(20)` on the weighted three-path, `K_4`, and the four-vertex
orientation witness; verifies equality on `K_4`; and freezes the exact
obstructions `(23)--(27)`.  The surviving sign `(20)` remains open in
arbitrary order.
