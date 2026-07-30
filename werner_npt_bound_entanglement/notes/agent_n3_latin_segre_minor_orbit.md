# A complete Latin--Segre third-minor orbit

## Status

The diagonal symmetric-cube minors are insufficient because they see
only \(\mathrm{Sym}^3(\mathbb C^3)\).  Allowing independent local
frames changes the answer completely.

For three independent local unitaries \(U_1,U_2,U_3\), define the
orthonormal product triple
\[
 p_r(U)=U_1|r\rangle\otimes U_2|r\rangle
              \otimes U_3|r\rangle,\qquad r=0,1,2.
\tag{1}
\]
Use another independent triple \(V_1,V_2,V_3\) on the right and put
\[
 \Delta_{U,V}(C)
 =
 \det\left(
 \langle p_r(U),C\,p_s(V)\rangle
 \right)_{r,s=0}^2.
\tag{2}
\]

This one local-unitary orbit type is complete:
\[
\boxed{
 {\mathbb E}_{U,V}|\Delta_{U,V}(C)|^2=0
 \quad\Longleftrightarrow\quad
 \operatorname{rank}C\leq2.
 }
\tag{3}
\]
More quantitatively,
\[
\boxed{
 \frac1{5760^2}\|\wedge^3C\|_2^2
 \leq
 {\mathbb E}_{U,V}|\Delta_{U,V}(C)|^2
 \leq
 \frac1{36^2}\|\wedge^3C\|_2^2.
 }
\tag{4}
\]

Thus independently polarized Latin triples supply a genuine finite
rank-two realizability mechanism.  A finite subfamily exists because
their exterior vectors span the 2925-dimensional third exterior
power.

However, the averaged minor is not a function of the five existing
quadratic invariants \(q,c,G,a,\Xi\).  An exact rank-two zero boundary
and an exact high-rank operator below have identical values of all
five, while their Latin-minor averages are respectively zero and
strictly positive.  Therefore a useful fusion with the current
quadratic inequalities must retain additional sixth-order
common-code data; scalar sector arithmetic cannot reconstruct the
average.

The dependency-free checker is
`verification/verify_n3_latin_segre_minor_orbit.py`.

## 1. Exterior form of the determinant

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3}
\]
and use the normalized exterior product.  Put
\[
 \eta
 =
 |000\rangle\wedge|111\rangle\wedge|222\rangle
 \in\wedge^3{\cal H}.
\tag{5}
\]
For \(U=(U_1,U_2,U_3)\), let
\[
 \eta_U
 =p_0(U)\wedge p_1(U)\wedge p_2(U).
\tag{6}
\]
Then the determinant identity is exactly
\[
\boxed{
 \Delta_{U,V}(C)
 =
 \langle\eta_U,(\wedge^3C)\eta_V\rangle.
 }
\tag{7}
\]

Define the left frame operator
\[
 K={\mathbb E}_U|\eta_U\rangle\langle\eta_U|.
\tag{8}
\]
Independence of the left and right frames gives
\[
\boxed{
 {\mathbb E}_{U,V}|\Delta_{U,V}(C)|^2
 =
 \operatorname{Tr}\left[
 (\wedge^3C)^\dagger K(\wedge^3C)K
 \right].
 }
\tag{9}
\]
It remains to prove that \(K\) is positive definite and to compute
its extreme eigenvalues.

## 2. Complete decomposition from the three-replica permutation algebra

On one physical qutrit, three replicas carry the three permutation
types
\[
 S=[3],\qquad M=[2,1],\qquad A=[1,1,1].
\tag{10}
\]
Their permutation-representation dimensions and qutrit
multiplicity-space dimensions are
\[
\begin{array}{c|ccc}
\lambda&S&M&A\\ \hline
d_\lambda&1&2&1\\
D_\lambda&10&8&1.
\end{array}
\tag{11}
\]
These numbers follow directly from the permutation projectors.  The
fully symmetric subspace has the ten symmetrized multisets of size
three, the fully antisymmetric subspace has dimension one, and the
remaining dimension is
\[
 27-10-1=16=2\cdot8.
\]

The character table needed below is
\[
\begin{array}{c|rrr}
 &e&(12)&(123)\\ \hline
 S&1&1&1\\
 A&1&-1&1\\
 M&2&0&-1.
\end{array}
\tag{12}
\]
The third exterior power is the sign sector of the simultaneous
permutation of the three replicas.  Multiplying the three rows of
(12) shows that the sign representation occurs, with multiplicity
one, exactly for

* triples of \(S,A\) containing an odd number of \(A\)'s;
* triples containing exactly two \(M\)'s and one \(S\) or \(A\);
* the triple \(MMM\).

The total physical dimension of these components is
\[
 3(10^2)+1
 +3(8^2\cdot10)+3(8^2)
 +8^3
 =2925
 =\binom{27}{3},
\tag{13}
\]
so the list is complete.

## 3. The seed has nonzero mass in every component

Inside the six-dimensional distinct-index orbit of one local replica
triple, identify basis vectors with the six permutations \(g\in S_3\).
The exterior seed (5) is
\[
 \eta=\frac1{\sqrt6}
 \sum_{g\in S_3}\operatorname{sgn}(g)
 |g\rangle\otimes|g\rangle\otimes|g\rangle.
\tag{14}
\]

Let \(P_\lambda\) be the local projector onto permutation type
\(\lambda\):
\[
 P_\lambda
 =\frac{d_\lambda}{6}
 \sum_{h\in S_3}\chi_\lambda(h)R_h.
\tag{15}
\]
Directly from (14),
\[
 \langle\eta|
 R_h\otimes R_k\otimes R_\ell
 |\eta\rangle
 =
 \begin{cases}
 \operatorname{sgn}(h),&h=k=\ell,\\
 0,&\text{otherwise}.
 \end{cases}
\tag{16}
\]
Therefore
\[
\begin{aligned}
 w_{\lambda\mu\nu}
 &:=
 \|(P_\lambda\otimes P_\mu\otimes P_\nu)\eta\|^2\\
 &=
 \frac{d_\lambda d_\mu d_\nu}{6^3}
 \sum_{h\in S_3}
 \operatorname{sgn}(h)
 \chi_\lambda(h)\chi_\mu(h)\chi_\nu(h).
\end{aligned}
\tag{17}
\]
The last sum is six on every allowed triple and zero otherwise.
Hence
\[
\boxed{
 w_{\lambda\mu\nu}
 =\frac{d_\lambda d_\mu d_\nu}{36}>0
 }
\tag{18}
\]
on every component of \(\wedge^3{\cal H}\).

## 4. Exact spectrum of the Haar frame

Haar averaging in (8) commutes with all three independent local
unitary actions.  On each component in Section 2 it is therefore a
scalar; the scalar is its trace (18) divided by the component
dimension.  Thus
\[
\boxed{
 K|_{\lambda\mu\nu}
 =
 \frac1{36}
 \frac{d_\lambda d_\mu d_\nu}
      {D_\lambda D_\mu D_\nu}\,I.
 }
\tag{19}
\]
All eigenvalues are positive.  Using
\[
 \frac{d_S}{D_S}=\frac1{10},\qquad
 \frac{d_M}{D_M}=\frac14,\qquad
 \frac{d_A}{D_A}=1,
\]
the least eigenvalue occurs on an \(MMS\) component and the greatest
on \(AAA\):
\[
\boxed{
 \frac1{5760}I\preceq K\preceq\frac1{36}I.
 }
\tag{20}
\]
Substitution in (9) proves (4), and hence (3).

Since the orbit of \(\eta\) spans the whole exterior power, ordinary
finite-dimensional linear algebra permits selection of 2925 orbit
vectors forming a basis.  The determinants between the corresponding
left and right finite frame lists already vanish simultaneously if
and only if \(\wedge^3C=0\).

## 5. Calibration on the cyclic obstruction

For the operator \(C_\star\) in
`agent_n3_symmetric_cube_minor_obstruction.md`, choose the three row
product vectors
\[
 |010\rangle,\quad|121\rangle,\quad|202\rangle
\tag{21}
\]
and the three column product vectors
\[
 |022\rangle,\quad|100\rangle,\quad|211\rangle.
\tag{22}
\]
Each local coordinate runs through an orthonormal qutrit basis, so
both triples belong to the orbit (1).  Direct permutation
contraction gives
\[
 \left(
 \langle p_r,C_\star q_s\rangle
 \right)_{r,s}
 =
 \left(1+\sqrt{\frac35}\right)
 \begin{pmatrix}
 0&1&0\\
 0&0&1\\
 1&0&0
 \end{pmatrix}.
\tag{23}
\]
Consequently
\[
\boxed{
 \Delta(C_\star)
 =
 \left(1+\sqrt{\frac35}\right)^3\ne0.
 }
\tag{24}
\]
The independent Latin orbit detects exactly the high-rank direction
which every symmetric-cube minor missed.

## 6. The average is not determined by \(q,c,G,a,\Xi\)

Let
\[
 P_2=|0\rangle\langle0|+|1\rangle\langle1|,
\qquad E_{01}=|0\rangle\langle1|,
\]
and define the rank-two boundary matrix
\[
 C_{\rm bd}=P_2\otimes E_{01}\otimes E_{01}.
\tag{25}
\]
Its only sector masses are
\[
 c=\frac43,\qquad d=\frac23,
\tag{26}
\]
so
\[
\boxed{
 (q,c,G,a,\Xi)
 =
 \left(0,\frac43,\frac23,0,\frac12\right).
 }
\tag{27}
\]
Since \(\operatorname{rank}C_{\rm bd}=2\), equation (3) gives
\[
 {\mathbb E}|\Delta(C_{\rm bd})|^2=0.
\tag{28}
\]

Now use the invariant pure-sector operators \(D_0,E_0\) from
`agent_n3_cyclic_stationary_high_rank_obstruction.md` and put
\[
 C_{\rm hi}
 =\frac1{\sqrt{54}}D_0+\frac1{\sqrt{40}}E_0.
\tag{29}
\]
Because
\[
 \|D_0\|^2=72,\qquad\|E_0\|^2=\frac{80}{3},
\]
\(C_{\rm hi}\) has exactly the same masses (26), and hence exactly
the same five invariants (27).  But on the symmetric subspace its
eigenvalue is
\[
 \frac2{\sqrt{54}}+\frac4{9\sqrt{40}}>0.
\tag{30}
\]
Thus \(\wedge^3C_{\rm hi}\ne0\), and (3) gives
\[
 {\mathbb E}|\Delta(C_{\rm hi})|^2>0.
\tag{31}
\]

Equations (28)--(31) prove that the complete Latin-minor average
cannot be expressed as a function of \(q,c,G,a,\Xi\) alone.  This
calibrates the orbit both on the exact rank-two \(q=0\) boundary and
on a sector-indistinguishable high-rank operator.

The next fusion problem is therefore genuinely sixth order: retain
selected components of \(\wedge^3C\), or their polarized Gram matrix,
inside the critical Hessian argument before reducing to the five
quadratic scalars.
