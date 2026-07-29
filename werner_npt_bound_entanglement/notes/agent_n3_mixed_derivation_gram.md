# Mixed local derivations of one degree-two operator

## Status

This note computes the complete mixed double-commutator frame attached
to
\[
 D=\Pi _2C.
\]
The main structural fact is that a derivation on two distinct sites
isolates exactly one of the three pair-sector components of \(D\).
This gives:

1. an exact operator-valued double-frame identity;
2. an exact Casimir reconstruction of every pair component from the
   mixed derivations;
3. an exact cross-site Gram identity for the three first-derivation
   maps.

The identities retain the common operator \(D\), rather than only its
sector masses.

There is also a sharp obstruction.  An explicit qutrit degree-two
operator of squared norm \(2/3\) has:

- full-rank first-derivation maps on every local traceless space;
- identically zero cross-site first-derivation Gram blocks;
- nonzero commuting mixed double derivations;
- the exact pair-sector Casimir norms.

Consequently, Gram positivity, mixed-derivation commutation, and all
their scalar Casimir traces supply no new scalar inequality at the
\(f=2/3\) frontier.  Any successful use of the mixed identities must
couple their operator-valued frames to the common rank-two matrix
\(C\), for example through the critical normal-space equations.  The
example is not asserted to be \(\Pi _2C\) for a critical rank-two
\(C\).

The exact checker is
`verification/verify_n3_mixed_derivation_gram.py`.

## 1. Sector isolation

Let
\[
 {\cal E}_i(X)=I_i\otimes\operatorname{Tr}_iX
 \tag{1}
\]
be unnormalized trace replacement at site \(i\).  Write an exact
degree-two operator as
\[
 D=D_{\widehat1}+D_{\widehat2}+D_{\widehat3},
 \qquad
 p_k=\|D_{\widehat k}\|_2^2,\qquad
 f=p_1+p_2+p_3.
 \tag{2}
\]
Thus \(D_{\widehat k}\) is scalar at \(k\) and traceless at the other
two sites.

For a local matrix \(A\), put
\[
 \delta_i(A)X=[A_i,X].
 \tag{3}
\]
If \(i,j,k\) are distinct, then
\[
\boxed{\qquad
 \delta_i(A)\delta_j(B)D
 =
 \delta_i(A)\delta_j(B)D_{\widehat k}.
 \qquad}
 \tag{4}
\]
Indeed, \(\delta_i\) kills the component scalar at \(i\), and
\(\delta_j\) kills the component scalar at \(j\).  Only the component
scalar at the third site survives.

In particular,
\[
 [A_i,[B_j,D]]=[B_j,[A_i,D]]
 \tag{5}
\]
is not merely a formal Jacobi relation: the common value is a
derivation of one definite two-site component.

## 2. The operator-valued double frame

Choose a Hermitian Hilbert--Schmidt orthonormal basis
\((F_\mu)_{\mu=0}^8\) of \(M_3\).  It obeys
\[
 \sum_\mu F_\mu YF_\mu=\operatorname{Tr}(Y)I_3,
 \qquad
 \sum_\mu F_\mu^2=3I_3.
 \tag{6}
\]
For an operator \(X\) which is traceless at site \(i\), direct
expansion gives
\[
\boxed{\quad
 \sum_\mu
 \delta_i(F_\mu)X\,\delta_i(F_\mu)X^\dagger
 =
 3XX^\dagger+{\cal E}_i(XX^\dagger).
 \quad}
 \tag{7}
\]
Without the tracelessness assumption the right side of (7) has the
two additional terms
\[
 -{\cal E}_i(X)X^\dagger-X{\cal E}_i(X^\dagger).
 \tag{8}
\]

Let \(X=D_{\widehat k}\), where \(\{i,j,k\}=\{1,2,3\}\), and set
\[
 Y_{\mu\nu}^{ij}
 =
 \delta_i(F_\mu)\delta_j(F_\nu)D.
 \tag{9}
\]
Applying (7) successively at the two sites proves the exact
operator-valued identity
\[
\boxed{
\begin{aligned}
 \sum_{\mu,\nu}Y_{\mu\nu}^{ij}Y_{\mu\nu}^{ij\dagger}
 ={}&
 9XX^\dagger
 +3{\cal E}_i(XX^\dagger)
 +3{\cal E}_j(XX^\dagger)\\
 &+{\cal E}_i{\cal E}_j(XX^\dagger).
\end{aligned}}
 \tag{10}
\]
The right-oriented companion is
\[
\boxed{
\begin{aligned}
 \sum_{\mu,\nu}Y_{\mu\nu}^{ij\dagger}Y_{\mu\nu}^{ij}
 ={}&
 9X^\dagger X
 +3{\cal E}_i(X^\dagger X)
 +3{\cal E}_j(X^\dagger X)\\
 &+{\cal E}_i{\cal E}_j(X^\dagger X).
\end{aligned}}
 \tag{11}
\]
Taking the trace gives
\[
\boxed{\qquad
 \sum_{\mu,\nu}\|Y_{\mu\nu}^{ij}\|_2^2=36p_k.
 \qquad}
 \tag{12}
\]
Hence
\[
 \sum_{i<j}\sum_{\mu,\nu}
 \|[F_\mu^{(i)},[F_\nu^{(j)},D]]\|_2^2
 =36f.
 \tag{13}
\]
This total is an identity, not an inequality, so its scalar trace
cannot improve a bound on \(f\).

## 3. Exact reconstruction

The same completeness relations give the local Casimir identity
\[
 \sum_\mu\delta_i(F_\mu)^2X
 =6X-2{\cal E}_i(X).
 \tag{14}
\]
Since \(D_{\widehat k}\) is traceless at \(i,j\), equations
(4) and (14) give
\[
\boxed{\quad
 D_{\widehat k}
 =
 \frac1{36}
 \sum_{\mu,\nu}
 \delta_i(F_\mu)^2\delta_j(F_\nu)^2D.
 \quad}
 \tag{15}
\]
Thus the three mixed-derivation tensors reconstruct the complete
operator \(D\).  A formal six-map model which does not admit (15)
cannot be promoted to commuting physical derivations.

## 4. The cross-site first-derivation Gram

Define
\[
 {\mathfrak d}_i^D(A)=\delta_i(A)D.
 \tag{16}
\]
For distinct \(i,j,k\), sector orthogonality and (4) give
\[
\boxed{
\begin{aligned}
 \left\langle{\mathfrak d}_i^D(A),
 {\mathfrak d}_j^D(B)\right\rangle
 &=
 \left\langle\delta_i(A)D_{\widehat k},
 \delta_j(B)D_{\widehat k}\right\rangle\\
 &=
 \left\langle D,
 \delta_i(A^\dagger)\delta_j(B)D\right\rangle .
\end{aligned}}
 \tag{17}
\]
This is the operator-valued mixed moment missing from norm-only
covariance arguments.

If \(X=D_{\widehat k}\), the \(9\times9\) cross-Gram block is
represented by the map
\[
\boxed{
\begin{aligned}
 {\cal G}_{ij}^X(B)
 =
 \operatorname{Tr}_{\widehat i}\bigl(
 &B_jXX^\dagger-XB_jX^\dagger\\
 &-X^\dagger B_jX+X^\dagger XB_j
 \bigr),
\end{aligned}}
 \tag{18}
\]
in the sense that
\[
 \langle\delta_i(A)X,\delta_j(B)X\rangle
 =\operatorname{Tr}\bigl(A^\dagger{\cal G}_{ij}^X(B)\bigr).
 \tag{19}
\]

The block need not carry a positive amount of mass.  If
\[
 X=R_i\otimes S_j\otimes T
 \tag{20}
\]
and \(R,S\) are normal, then
\[
 {\cal G}_{ij}^X=0.
 \tag{21}
\]
Indeed, the left side of (19) factorizes into
\[
 \langle[A,R],R\rangle\,
 \langle S,[B,S]\rangle\,\|T\|_2^2,
 \tag{22}
\]
and both displayed commutator expectations vanish for normal
matrices.

## 5. Exact full-rank obstruction

Let
\[
\begin{aligned}
 Z&=\frac1{\sqrt2}\operatorname{diag}(1,0,-1),\\
 X&=\frac12(E_{01}+E_{10}+E_{12}+E_{21}),\\
 S&=\frac1{\sqrt3}I_3,\qquad
 a=\frac{\sqrt2}{3}.
\end{aligned}
 \tag{23}
\]
These are Hilbert--Schmidt unit vectors; \(Z,X\) are traceless
Hermitian matrices.  Define
\[
\boxed{\quad
 D_*=
 a\bigl(
 Z\otimes Z\otimes S
 +X\otimes S\otimes Z
 +S\otimes X\otimes X
 \bigr).
 \quad}
 \tag{24}
\]
The three summands occupy mutually orthogonal exact degree-two
sectors.  Therefore
\[
 p_1=p_2=p_3=\frac29,\qquad
 \|D_*\|_2^2=f=\frac23.
 \tag{25}
\]

At each site the first derivation contains the two orthogonal
components generated by \(Z\) and \(X\).  The common commutant of
\(Z\) and \(X\) is \(\mathbb CI_3\): commuting with the
simple-spectrum diagonal \(Z\) makes a matrix diagonal, and commuting
also with the connected path matrix \(X\) makes its three diagonal
entries equal.  Hence
\[
\boxed{\qquad
 \ker{\mathfrak d}_i^{D_*}=\mathbb CI_3,
 \qquad
 \operatorname{rank}
 \left({\mathfrak d}_i^{D_*}|_{M_3^0}\right)=8
 \quad(i=1,2,3).
 \qquad}
 \tag{26}
\]

Every pair component in (24) is a product of normal local matrices.
Equation (21) consequently gives the much stronger identity
\[
\boxed{\qquad
 ({\mathfrak d}_i^{D_*})^\dagger
 {\mathfrak d}_j^{D_*}=0
 \quad(i\ne j).
 \qquad}
 \tag{27}
\]
Thus the entire \(27\times27\) Gram matrix of the three local
derivation maps is block diagonal, even though every traceless block
has full rank eight.

The mixed maps are nevertheless nonzero and exactly physical:
\[
\begin{aligned}
 \delta_1(A)\delta_2(B)D_*
 &=a[A,Z]\otimes[B,Z]\otimes S,\\
 \delta_1(A)\delta_3(B)D_*
 &=a[A,X]\otimes S\otimes[B,Z],\\
 \delta_2(A)\delta_3(B)D_*
 &=aS\otimes[A,X]\otimes[B,X].
\end{aligned}
 \tag{28}
\]
They commute across distinct sites and reconstruct the three
summands through (15).  Their exact norms are
\[
\boxed{
\begin{aligned}
 \sum_\mu\|[F_\mu^{(i)},D_*]\|_2^2&=\frac83
 &&(i=1,2,3),\\
 \sum_{\mu,\nu}
 \|[F_\mu^{(i)},[F_\nu^{(j)},D_*]]\|_2^2&=8
 &&(i<j).
\end{aligned}}
\tag{29}
\]

The example is not a dual pair-sector witness.  Its characteristic
polynomial is
\[
\begin{aligned}
 \chi_{D_*}(t)
 ={}&t^7
 \left(t^2-\frac1{18}\right)
 \left(t^2-\frac1{27}\right)^3\\
 &\times
 \left(t^2-\frac{\sqrt6}{18}t-\frac1{54}\right)^3
 \left(t^2+\frac{\sqrt6}{18}t-\frac1{54}\right)^3.
\end{aligned}
\tag{30}
\]
Hence its largest singular value is \(\sqrt2/6\), with multiplicity
two, and
\[
 s_1(D_*)^2+s_2(D_*)^2=\frac19
 <\frac23\|D_*\|_2^2=\frac49.
\tag{31}
\]
Thus \(D_*\) is an obstruction to a proposed proof mechanism, not a
counterexample to the normalized transition contraction.

## 6. Consequence for the pair-sector program

Equations (10), (11), (15), and (17) are the exact common-\(D\)
information supplied by mixed local derivations.  They are stronger
than the previously recorded six-map norm identities.

The operator \(D_*\) proves a precise no-go, however.  The following
data can coexist at the sharp numerical value \(f=2/3\):

1. full-rank local derivation maps;
2. exact cross-site Gram orthogonality;
3. commuting, nonzero double derivations;
4. exact component reconstruction;
5. all first- and second-Casimir norm identities.

Therefore their scalar Gram traces do not strengthen the existing
sector arithmetic, and no universal positive lower bound on a
cross-site Gram block is possible.  This does not rule out a genuinely
operator-valued use of (10)--(11).  Such a use must exploit that
\(D=\Pi _2C\) for one rank-two critical \(C\).  In particular, it
must combine the double frames with the critical left/right support
equations; replacing those frames by their traces loses all possible
improvement.

## 7. The critical equations exclude the obstruction

The missing rank-two coupling immediately eliminates \(D_*\).  The
reason is a general spectral-support lemma.

### Lemma 7.1 (critical spectral support)

Let \(C\) have rank \(r\), Hilbert--Schmidt norm one, and singular
value decomposition
\[
 C=U\Sigma V^\dagger.
 \tag{32}
\]
Suppose an arbitrary operator \(D\) and a real \(f>0\) obey
\[
 CD^\dagger=fCC^\dagger,\qquad
 D^\dagger C=fC^\dagger C.
 \tag{33}
\]
Then
\[
\boxed{
\begin{aligned}
 DV&=fU\Sigma,&D^\dagger U&=fV\Sigma,\\
 D^\dagger DV&=f^2V\Sigma^2,&
 DD^\dagger U&=f^2U\Sigma^2.
\end{aligned}}
\tag{34}
\]
Consequently
\[
\boxed{\qquad
 s_1(D)^2+\cdots+s_r(D)^2\geq f^2.
 \qquad}
\tag{35}
\]

### Proof

Left-multiply the first equation in (33) by \(U^\dagger\), cancel
the invertible matrix \(\Sigma\) on its \(r\)-dimensional support,
and take the adjoint.  This gives \(DV=fU\Sigma\).  Apply the second
equation to \(V\) and cancel \(\Sigma\) to get
\(D^\dagger U=fV\Sigma\).  Composition proves the second line of
(34).

Taking the trace of \(V^\dagger D^\dagger DV=f^2\Sigma^2\) gives
\[
 \operatorname{Tr}(V^\dagger D^\dagger DV)
 =f^2\operatorname{Tr}\Sigma^2=f^2.
 \]
The rank-\(r\) Ky--Fan variational principle bounds the left side by
the sum of the \(r\) largest eigenvalues of \(D^\dagger D\), proving
(35). \(\square\)

The proof gives the complete solution set for a fixed \(D\).

### Corollary 7.2 (classification for fixed \(D\))

Normalized rank-\(r\) solutions of (33) are in one-to-one
correspondence with \(r\)-dimensional singular subsystems
\[
 DV=U\Lambda,\qquad D^\dagger U=V\Lambda
 \tag{36}
\]
such that
\[
 \operatorname{Tr}\Lambda^2=f^2.
 \tag{37}
\]
The corresponding matrix is
\[
\boxed{\qquad C=\frac1fU\Lambda V^\dagger.\qquad}
\tag{38}
\]
Conversely, (36)--(38) directly imply both equations in (33).  For a
nondegenerate \(D^\dagger D\), this simply selects \(r\) singular
triples of \(D\) whose squared singular values sum to \(f^2\).

If in addition \(\|D\|_2^2=f\), every solution has the orthogonal
singular-block decomposition
\[
\boxed{
 D=fC+D_\perp,\qquad
 D_\perp V=0,\quad D_\perp^\dagger U=0,\quad
 \|D_\perp\|_2^2=f-f^2.
}
\tag{39}
\]
Thus the critical equations fix not just a lower bound on the
top-two mass, but the complete singular block on which \(C\) lives.

For \(D_*\), equations (30)--(31) give
\[
 s_1(D_*)^2+s_2(D_*)^2=\frac19,
 \qquad
 f^2=\left(\frac23\right)^2=\frac49.
 \tag{40}
\]
Thus no normalized rank-at-most-two \(C\) can satisfy (33) with
\(D=D_*\) and \(f=2/3\).  This conclusion does not even require the
additional projection equation \(D_*=\Pi _2C\).

The obstruction therefore separates the two logical layers cleanly:
mixed-derivation compatibility alone admits \(D_*\), while the
rank-two critical support equations reject it by an exact factor
four in squared Ky--Fan mass.
