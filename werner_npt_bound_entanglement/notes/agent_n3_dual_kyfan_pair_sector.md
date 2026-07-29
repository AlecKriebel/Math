# The unrestricted three-copy dual and its degree-two sector frontier

## Status

This note independently derives the exact Ky--Fan dual formulation of
the unrestricted qutrit three-copy endpoint.  It also isolates the
pair-only inequality as a sharp rank-two projection theorem.  The
equivalences and constants below are exact.  The pair-only inequality
itself remains unproved.

## 1. Orthogonal local-sector decomposition

Give \(M_3^{\otimes3}\) its Hilbert--Schmidt inner product.  On local
site \(i\), define the orthogonal projectors
\[
 {\cal P}_i(C)=\frac13 I_i\otimes\operatorname{Tr}_iC,
 \qquad
 {\cal Q}_i=I-{\cal P}_i.                                \tag{1}
\]
Thus \({\cal P}_i\) selects the identity direction and
\({\cal Q}_i\) selects the traceless subspace.  For
\(S\subseteq\{1,2,3\}\), let
\[
 \Pi_S=\prod_{i\in S}{\cal Q}_i
       \prod_{i\notin S}{\cal P}_i.                      \tag{2}
\]
The eight \(\Pi_S\) are mutually orthogonal projections summing to the
identity.

The endpoint superoperator
\[
 {\cal L}(X)=X-\frac12\operatorname{Tr}(X)I_3             \tag{3}
\]
has eigenvalue \(1\) on traceless matrices and \(-1/2\) on
the identity direction.  Hence
\[
 Q_3(C)=\langle C,{\cal L}^{\otimes3}C\rangle             \tag{4}
\]
has sector eigenvalues
\[
\begin{array}{c|cccc}
 |S|&0&1&2&3\\ \hline
 {\cal L}^{\otimes3}&-1/8&1/4&-1/2&1 .
\end{array}                                               \tag{5}
\]

Define the positive semidefinite sector multiplier
\[
 {\cal T}=\sqrt{2(I-{\cal L}^{\otimes3})}.                \tag{6}
\]
Its squared eigenvalues on sectors of traceless degree \(0,1,2,3\)
are respectively
\[
 \frac94,\qquad\frac32,\qquad3,\qquad0.                  \tag{7}
\]
Therefore
\[
 \boxed{\qquad
 Q_3(C)=\|C\|_2^2-\frac12\|{\cal T}C\|_2^2 .
 \qquad}                                                  \tag{8}
\]

## 2. Exact Ky--Fan dual

Every operator in \(\operatorname{ran}{\cal T}\) has the unique
orthogonal form
\[
 D=cI_{27}
  +\sum_{i=1}^3 A_i^{(i)}
  +\sum_{1\le i<j\le3}B_{ij}^{(ij)},                     \tag{9}
\]
where
\[
 \operatorname{Tr}A_i=0,\qquad
 \operatorname{Tr}_iB_{ij}
 =\operatorname{Tr}_jB_{ij}=0.                           \tag{10}
\]
Unshown sites in (9) carry the unnormalized identity \(I_3\).
The embedded sector norms are
\[
\begin{aligned}
\|cI_{27}\|_2^2&=27|c|^2,\\
\|A_i^{(i)}\|_2^2&=9\|A_i\|_2^2,\\
\|B_{ij}^{(ij)}\|_2^2&=3\|B_{ij}\|_2^2.
\end{aligned}                                             \tag{11}
\]
Using (7), the minimum squared norm of a preimage
\({\cal T}Y=D\) is
\[
 \min_{{\cal T}Y=D}\|Y\|_2^2
 =
 12|c|^2+6\sum_i\|A_i\|_2^2
 +\sum_{i<j}\|B_{ij}\|_2^2.                              \tag{12}
\]

For an arbitrary matrix \(D\),
\[
 \sup_{\substack{\operatorname{rank}C\le2\\\|C\|_2=1}}
 |\langle D,C\rangle|^2
 =s_1(D)^2+s_2(D)^2.                                     \tag{13}
\]
Indeed, von Neumann's singular-value inequality gives the upper bound,
and the rank-two truncation of a singular-value decomposition attains
it.

Combining (8), Hilbert-space duality, (12), and (13) proves the exact
equivalence:
\[
\boxed{
\begin{aligned}
&Q_3(C)\ge0
\quad\text{for every }\operatorname{rank}C\le2\\
&\quad\Longleftrightarrow\\
&s_1(D)^2+s_2(D)^2
\le
24|c|^2
+12\sum_i\|A_i\|_2^2
+2\sum_{i<j}\|B_{ij}\|_2^2
\quad\text{for every }D\text{ in (9).}
\end{aligned}}                                            \tag{14}
\]
This confirms all constants in the proposed dual statement.

## 3. The pair-only frontier

Set \(c=0\) and \(A_i=0\).  The first unresolved dual subproblem is
\[
\boxed{\qquad
s_1(D)^2+s_2(D)^2
\le2\sum_{i<j}\|B_{ij}\|_2^2,
\qquad
D=\sum_{i<j}B_{ij}^{(ij)} .
\qquad}                                                    \tag{15}
\]

Let
\[
 \Pi_2=\sum_{|S|=2}\Pi_S
 ={\cal Q}_1{\cal Q}_2{\cal P}_3
  +{\cal Q}_1{\cal P}_2{\cal Q}_3
  +{\cal P}_1{\cal Q}_2{\cal Q}_3.                       \tag{16}
\]
Since the three embedded pair sectors are orthogonal,
\[
 \|D\|_2^2=3\sum_{i<j}\|B_{ij}\|_2^2.                    \tag{17}
\]
Applying (13) and then dualizing inside the pair-sector subspace shows
that (15) is exactly equivalent to
\[
 \boxed{\qquad
 \|\Pi_2C\|_2^2\le\frac23\|C\|_2^2
 \quad\text{whenever }\operatorname{rank}C\le2.
 \qquad}                                                   \tag{18}
\]
There is no relaxation in passing between (15) and (18).

## 4. Partial-trace form

For a two-site operator \(X\in M_3\otimes M_3\), its doubly traceless
part is
\[
 X_{00}
 =X-\frac13\left(
 I\otimes\operatorname{Tr}_1X
 +\operatorname{Tr}_2X\otimes I\right)
 +\frac{\operatorname{Tr}X}{9}I\otimes I,                \tag{19}
\]
and orthogonality gives
\[
 \|X_{00}\|_2^2
 =\|X\|_2^2
 -\frac13\left(
 \|\operatorname{Tr}_1X\|_2^2
 +\|\operatorname{Tr}_2X\|_2^2\right)
 +\frac19|\operatorname{Tr}X|^2.                         \tag{20}
\]
Moreover,
\[
 \|\Pi_2C\|_2^2
 =\frac13\sum_{k=1}^3
 \|(\operatorname{Tr}_kC)_{00}\|_2^2.                   \tag{21}
\]
Substitution into (18) yields the equivalent marginal inequality
\[
\boxed{
\begin{aligned}
\sum_{k=1}^3\|\operatorname{Tr}_kC\|_2^2
&-\frac23\sum_{i=1}^3
\left\|\operatorname{Tr}_{\{1,2,3\}\setminus\{i\}}C
\right\|_2^2\\
&+\frac13|\operatorname{Tr}C|^2
\le2\|C\|_2^2,
\qquad \operatorname{rank}C\le2 .
\end{aligned}}                                            \tag{22}
\]

## 5. Sharpness

The constant \(2\) in (15) cannot be reduced.  Take
\[
 B_{12}=E_{01}\otimes E_{01},\qquad
 B_{13}=B_{23}=0.                                        \tag{23}
\]
Both marginal traces of \(B_{12}\) vanish and
\(\|B_{12}\|_2=1\).  The operator
\[
 D=B_{12}\otimes I_3
\]
has singular value \(1\) with multiplicity three.  Hence
\[
 s_1(D)^2+s_2(D)^2=2
 =2\|B_{12}\|_2^2.                                       \tag{24}
\]

The corresponding primal equality is also explicit:
\[
 C=E_{01}\otimes E_{01}\otimes
   (|0\rangle\langle0|+|1\rangle\langle1|).              \tag{25}
\]
It has rank two and squared norm \(2\).  Since the first two factors
are already traceless and the identity component of the third factor
is \((2/3)I_3\),
\[
 \|\Pi_2C\|_2^2=\frac43
 =\frac23\|C\|_2^2.                                      \tag{26}
\]

The exact checker
`verification/verify_n3_dual_kyfan_pair_sector.py` verifies the sector
constants, (20)--(22) on a rational rank-two matrix, and both sharp
examples.

## 6. A positive partial-transpose form

The pair-sector witness
\[
 W=\frac23I-\Pi_2                                             \tag{27}
\]
has an unexpectedly simple positive partial transpose.  Let \(F_i\)
swap the row and column qutrits at site \(i\).  Since
\({\cal P}_i^\Gamma=F_i/3\), expansion of (16) gives
\[
 W^\Gamma
 =\frac23I-\frac13\sum_iF_i
   +\frac29\sum_{i<j}F_iF_j-\frac19F_1F_2F_3.                \tag{28}
\]
The three swaps commute.  On their simultaneous eigenspace having
exactly \(r\) eigenvalues equal to \(-1\), (28) has eigenvalue
\[
\begin{array}{c|cccc}
r&0&1&2&3\\ \hline
W^\Gamma&2/9&2/9&2/3&22/9.
\end{array}                                                  \tag{29}
\]
Consequently
\[
\boxed{\qquad
 W^\Gamma=\frac29I+\frac49E_2+\frac{20}{9}E_3\succeq0,
\qquad}                                                       \tag{30}
\]
where \(E_r\) projects onto the joint-swap sector with exactly \(r\)
local antisymmetric signs.

This proves ordinary block positivity of \(W\), but not yet the needed
two-block positivity.  For a Schmidt-rank-two vector
\[
 \psi=s_1u_1\otimes\overline v_1+
      s_2u_2\otimes\overline v_2,
\]
the partial transpose of \(|\psi\rangle\langle\psi|\) has only one
negative eigenline, spanned by
\[
 \eta_-=\frac1{\sqrt2}
 \left(u_1\otimes\overline v_2-u_2\otimes\overline v_1\right). \tag{31}
\]
Thus (30) reduces the remaining obstruction to controlling the
weight-two and weight-three local-antisymmetry content of this single
decomposable cross-bivector by the three positive Schmidt lines.  Any
such control must use the common left and right singular planes:
positivity of \(W^\Gamma\) alone is insufficient.

There is also an exact reciprocal two-atom decomposition of (30).
Write
\[
 {\mathsf S}=\frac{I+F}{2},\qquad
 {\mathsf A}=\frac{I-F}{2},\qquad
 t_\pm=2\pm\sqrt3,
\]
and
\[
 p=\frac{\sqrt3-1}{2\sqrt3},\qquad
 q=\frac{\sqrt3+1}{2\sqrt3}.
\]
The four moment identities
\[
 pt_+^r+qt_-^r=1,1,3,11\qquad(r=0,1,2,3)
\]
give
\[
\boxed{\qquad
 W^\Gamma=\frac29\left[
 p({\mathsf S}+t_+{\mathsf A})^{\otimes3}
 +q({\mathsf S}+t_-{\mathsf A})^{\otimes3}\right].
\qquad}                                                     \tag{32}
\]
Here \(t_+t_-=1\).  Both summands are positive, but only the
\(t_-\) local factor has positive partial transpose.  Thus (32) is a
genuine reciprocal pairing rather than a decomposition into terms
which are separately two-block-positive.

A natural termwise exterior estimate is already too weak, sharply.
Expand \(E_2,E_3\) using normalized real symmetric and skew-symmetric
matrix bases, and for a Kraus tensor \(R\) put
\[
 M_R=U^{\mathsf T}RV\in M_2 .
\]
The partial transpose of
\(|\operatorname{vec}M_R\rangle
 \langle\operatorname{vec}M_R|\)
is bounded below by \(-|\det M_R|I_4\).  Hence a termwise proof would
need the weighted estimate
\[
 \frac49\sum_{R\in E_2}|\det M_R|
 +\frac{20}{9}\sum_{R\in E_3}|\det M_R|
 \leq\frac29.                                             \tag{33}
\]
This is false by the exact factor two.  Take
\[
 U=(|000\rangle,|001\rangle),\qquad
 V=(|110\rangle,|111\rangle).
\]
With the standard bases
\((E_{ij}+E_{ji})/\sqrt2\) and
\((E_{ij}-E_{ji})/\sqrt2\), the three nonzero \(E_2\)
determinant contributions are \(1/18\) each and the nonzero \(E_3\)
contribution is \(5/18\).  Their total is \(4/9\), although this is
the exact equality code (25) and its true partially transposed
compression is positive semidefinite with one zero eigenvalue.
Therefore the negative directions of the four Hodge channels must be
combined coherently; their determinant magnitudes cannot be summed.

## 7. A one-plane operator inequality

There is a second exact common-origin reduction which eliminates the
left singular plane entirely.  Fix an isometry
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3},
 \qquad V|r\rangle=v_r,
\]
and introduce the unnormalized maximally entangled code vector
\[
 |\boldsymbol V\rangle=\sum_{r=1}^2v_r\otimes|r\rangle_K,
 \qquad
 R=|\boldsymbol V\rangle\langle\boldsymbol V|,
 \qquad \operatorname{Tr}_{123}R=I_K.                     \tag{34}
\]
On operators carrying the auxiliary qubit, put
\[
 {\cal R}_i(X)=I_i\otimes\operatorname{Tr}_iX-\frac13X.    \tag{35}
\]
Choose Hilbert--Schmidt orthonormal bases of traceless qutrit
operators.  The frame operator of
\[
 (B_{12},B_{13},B_{23})
 \longmapsto
 \left(\sum_{i<j}B_{ij}^{(ij)}v_r\right)_{r=1}^2
\]
is exactly
\[
 {\cal S}_V=\sum_{i<j}{\cal R}_i{\cal R}_j(R).             \tag{36}
\]
It follows that the pair-only inequality (15) is equivalent to
\[
\boxed{\qquad
 {\cal S}_V\preceq2I_{(\mathbb C^3)^{\otimes3}\otimes K}
 \quad\text{for every isometry }V.
\qquad}                                                    \tag{37}
\]
Writing
\(\rho_{TK}=\operatorname{Tr}_{\{1,2,3\}\setminus T}R\),
the defect in (37) has the explicit marginal form
\[
\boxed{
3(2I-{\cal S}_V)
 =
6I
+2\sum_i I_i\otimes\rho_{\widehat i,K}
-3\sum_{\{i,j,k\}=\{1,2,3\}}
 I_i\otimes I_j\otimes\rho_{kK}
-R .
}                                                          \tag{38}
\]
Equations (37)--(38) retain the full nonlinear two-plane condition
solely through the rank-one operator \(R\) and its exact marginal
\(\operatorname{Tr}_{123}R=I_K\).  They are equivalent reformulations,
not a proof of the pair-only inequality.
