# Exterior/swap-sector attack on positive and normal rank two

## Research log

### 2026-07-28 09:24 PDT — checkpoint 1

Goal: prove, or exactly refute, the all-copy inequality
\[
Q_n(H)\ge 2^{-n}\bigl(2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2\bigr)
\tag{E1}
\]
for \(H\succeq0\), \(\operatorname{rank}H\le2\), and investigate whether the
corresponding statement extends to normal rank-two matrices.

The swap-sector reformulation has been checked from first principles below.
A tempting stronger statement is false: the operator \(W_n\) in (E5) is not
block-positive on arbitrary \(u\otimes v\), even when \(u\perp v\).  Thus an
all-copy proof must use the combined spectral sum in \(H\otimes H\), not a
termwise estimate on its \(u\otimes v\) summands.

Best-guess completion toward this restricted research goal: **15%**.

## 1. Exact swap-sector reformulation

Let the physical space be
\[
\mathcal V=V_1\otimes\cdots\otimes V_n,
\]
and let \(F_i\) swap the two replicas of \(V_i\).  Write
\[
F_T=\prod_{i\in T}F_i,\qquad F_{\rm all}=F_{[n]}.
\]
For Hermitian \(H\),
\[
\|\operatorname{Tr}_S H\|_2^2
=\operatorname{Tr}\bigl[(H\otimes H)F_{\bar S}\bigr].
\tag{E2}
\]
Indeed, expanding both sides in product indices leaves exactly the same
contractions: indices in \(\bar S\) are crossed between replicas and indices
in \(S\) are contracted inside each copy.

Consequently,
\[
\begin{aligned}
2^nQ_n(H)
&=\sum_{S\subseteq[n]}(-1)^{|S|}2^{n-|S|}
  \operatorname{Tr}\bigl[(H\otimes H)F_{\bar S}\bigr]\\
&=\operatorname{Tr}\left[(H\otimes H)
  \prod_{i=1}^n(2F_i-I)\right].
\end{aligned}
\tag{E3}
\]
Also
\[
2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2
=\operatorname{Tr}\bigl[(H\otimes H)(2F_{\rm all}-I)\bigr].
\tag{E4}
\]
Thus (E1) is equivalent to
\[
\operatorname{Tr}[(H\otimes H)W_n]\ge0,\qquad
W_n:=\prod_{i=1}^n(2F_i-I)+I-2F_{\rm all}.
\tag{E5}
\]

Put \(\Pi_i^\pm=(I\pm F_i)/2\) and
\(\Pi_R=\prod_{i\in R}\Pi_i^-\prod_{i\notin R}\Pi_i^+\).
On the sector \(\Pi_R\), with \(k=|R|\), the eigenvalue of \(W_n\) is
\[
w_k=(-3)^k+1-2(-1)^k
=\begin{cases}
3^k-1,&k\text{ even},\\
3-3^k,&k\text{ odd}.
\end{cases}
\tag{E6}
\]
It is zero for \(k=0,1\), positive for even \(k\ge2\), and negative for odd
\(k\ge3\).

## 2. Exactly where rank two enters

Factor \(H=AA^\dagger\) with
\(A:K\to\mathcal V\) and \(\dim K\le2\).  Then
\[
p_R(H):=\operatorname{Tr}[(H\otimes H)\Pi_R]
=\|\Pi_R(A\otimes A)\|_F^2.
\tag{E7}
\]
The map \(\Pi_R(A\otimes A)\) has domain
\(S^2K\) for even \(|R|\), and domain \(\Lambda^2K\) for odd \(|R|\).
For \(\dim K=2\), the latter domain is one-dimensional.  Equivalently, if
\(A\) has columns \(a,b\), all odd-sector mass is carried by the single
decomposable bivector \(a\wedge b\):
\[
p_R(H)=\|\Pi_R(a\wedge b)\|^2\qquad(|R|\ {\rm odd}),
\tag{E8}
\]
where \(a\wedge b=(a\otimes b-b\otimes a)/\sqrt2\).

The desired inequality is therefore the precise weighted comparison
\[
\sum_{\substack{R\\|R|\ {\rm even},\,|R|\ge2}}
(3^{|R|}-1)p_R(H)
\ \ge\
\sum_{\substack{R\\|R|\ {\rm odd},\,|R|\ge3}}
(3^{|R|}-3)p_R(H).
\tag{E9}
\]

## 3. A termwise route that fails

It would be enough, but is false, to prove
\[
\langle u\otimes v|W_n|u\otimes v\rangle\ge0
\tag{E10}
\]
for all orthogonal \(u,v\).  Direct floating-point contraction (used only
to locate the obstruction) gives negative values already for \(n=3\) and
two-dimensional local factors.  This does not refute (E1): if
\(H=\lambda|u\rangle\langle u|+\mu|v\rangle\langle v|\), then (E5)
contains the two additional nonnegative rank-one diagonal contributions
\(\lambda^2\langle u,u|W_n|u,u\rangle\) and
\(\mu^2\langle v,v|W_n|v,v\rangle\).

For later use, define
\[
D_n(x,y):=\langle x\otimes y|W_n|x\otimes y\rangle.
\tag{E11}
\]
If \(u\perp v\), then
\[
\operatorname{Tr}[(H\otimes H)W_n]
=\lambda^2D_n(u,u)+\mu^2D_n(v,v)+2\lambda\mu D_n(u,v).
\tag{E12}
\]
The rank-one endpoint bound proves \(D_n(x,x)\ge0\), but \(D_n(u,v)\)
can be negative.  The exact remaining scalar condition is copositivity of
the \(2\times2\) matrix in (E12):
\[
D_n(u,v)\ge-\sqrt{D_n(u,u)D_n(v,v)}.
\tag{E13}
\]
This is the form an exterior-algebra proof must establish.

### 2026-07-28 10:18 PDT — checkpoint 2

The failure of termwise positivity now has an exact sparse certificate, not
just a numerical example.  The full PSD quantitative conjecture survived
dedicated projected-gradient searches for \(d=3,n=3,4\), but that is discovery
data only.

An exact all-copy theorem was obtained for a substantial restricted class:
if the row and column support lies in a tensor product of common local
subspaces of dimension at most two, then \(Q_n\ge0\) for matrices of arbitrary
rank.  Thus any negative witness must use all three local directions on at
least one copy; after deletion of every copy using all three directions, the
remaining form is manifestly positive.

Best-guess completion toward the restricted research goal: **30%**.

## 4. Exact sparse obstruction to termwise \(W_n\)-positivity

Work on three copies and use the two local basis vectors \(0,1\) (the example
therefore embeds into local dimension three).  Define the unnormalized,
orthogonal vectors
\[
\begin{aligned}
u_0&=-|000\rangle+|010\rangle+|101\rangle+|111\rangle,\\
v_0&=\phantom{-}|000\rangle-|010\rangle+|101\rangle+|111\rangle.
\end{aligned}
\tag{E14}
\]
They satisfy
\[
\langle u_0,v_0\rangle=0,\qquad
\|u_0\|^2=\|v_0\|^2=4.
\]
A direct permutation of the eight basis coordinates gives, for every proper
\(T\subsetneq[3]\),
\[
\langle u_0\otimes v_0|F_T|u_0\otimes v_0\rangle
=\begin{cases}
16,&T=\varnothing,\\
8,&T\ne\varnothing,
\end{cases}
\qquad
\langle u_0\otimes v_0|F_{[3]}|u_0\otimes v_0\rangle=0.
\tag{E15}
\]
Substitution in
\[
\langle x,y|W_3|x,y\rangle
=\sum_{T\subseteq[3]}2^{|T|}(-1)^{3-|T|}
 \langle x,y|F_T|x,y\rangle
 \|x\|^2\|y\|^2-2|\langle x,y\rangle|^2
\tag{E16}
\]
gives
\[
\langle u_0,v_0|W_3|u_0,v_0\rangle=-48.
\]
For \(u=u_0/2,\ v=v_0/2\),
\[
D_3(u,v)=-3.
\tag{E17}
\]
The same exact contraction gives
\[
D_3(u,u)=D_3(v,v)=3.
\tag{E18}
\]
Thus (E13) is saturated.  This example is a rotated basis of a simple
two-dimensional product code.  Put
\[
a=|010\rangle-|000\rangle,\qquad
b=|101\rangle+|111\rangle.
\]
Then \(u_0=a+b,\ v_0=-a+b\), while \(a/\sqrt2,b/\sqrt2\) are orthogonal
product vectors differing in all three local factors.  The support projection
is unchanged by this rotation.  This explains structurally why a proof based
on the individual spectral cross term cannot work: the cross term can move
all the way to the negative Cauchy--Schwarz boundary under a harmless change
of basis inside an equality support.

## 5. A manifestly positive all-copy local-qubit-support class

**Theorem.**  Let \(W_i\subseteq\mathbb C^d\) have
\(\dim W_i\le2\), put \(W=\bigotimes_{i=1}^nW_i\), and suppose
\[
C=P_WCP_W.
\tag{E19}
\]
Then
\[
Q_{d,n}(C)\ge0
\tag{E20}
\]
for every matrix \(C\), with no rank or normality assumption.

**Proof.**  On one local matrix space define the Hilbert--Schmidt
self-adjoint superoperator
\[
\mathcal K(Z)=Z-\frac12\operatorname{Tr}(Z)I.
\]
For matrices \(A,B\) supported on a common \(r\)-dimensional subspace,
\[
\langle A,\mathcal K_d(B)\rangle
=\operatorname{Tr}(A^\dagger B)
-\frac12\overline{\operatorname{Tr}A}\operatorname{Tr}B,
\tag{E21}
\]
which depends on \(r\) but not on the ambient \(d\).  If \(r=2\), the
right-hand side is the quadratic form of the orthogonal projection
\[
\mathcal P_0(B)=B-\frac12\operatorname{Tr}(B)I_2
\tag{E22}
\]
onto the traceless \(2\times2\) matrices.  If \(r=1\), it is one half of
the ordinary scalar inner product.  Hence the compression of every local
\(\mathcal K_d\) to \(\operatorname{End}(W_i)\) is a positive semidefinite
superoperator.  Their tensor product is positive semidefinite, and therefore
\[
Q_{d,n}(C)
=\langle C,(\mathcal K_d^{\otimes n})(C)\rangle
=\left\|
\left(\bigotimes_{\dim W_i=2}\mathcal P_{0,i}\right)
\left(\bigotimes_{\dim W_i=1}2^{-1/2}I_i\right)C
\right\|_2^2\ge0.
\tag{E23}
\]
This proves the assertion. \(\square\)

When every \(\dim W_i=2\), equality holds exactly when the component of
\(C\) that is traceless on every local factor vanishes.  This provides a
large all-copy zero manifold, much larger than the copywise-product spectral
ansatz.

### The two-copy quantitative PSD identity

For completeness, the quantitative conjecture has a particularly short SOS
for two copies, with no rank assumption on \(H\succeq0\):
\[
\begin{aligned}
Q_2(H)-\frac12\left(
\operatorname{Tr}H^2-\frac12(\operatorname{Tr}H)^2\right)
&=\frac12\left(
\operatorname{Tr}H^2-\|\operatorname{Tr}_1H\|_2^2
-\|\operatorname{Tr}_2H\|_2^2+(\operatorname{Tr}H)^2\right)\\
&=2\operatorname{Tr}\left[(H\otimes H)
\Pi_1^-\Pi_2^-\right]\ge0.
\end{aligned}
\tag{E23a}
\]
The last inequality follows because both factors inside the trace are
positive.  If \(\operatorname{rank}H\le2\), the grouped one-copy identity is
\[
\operatorname{Tr}H^2-\frac12(\operatorname{Tr}H)^2
=\frac12(\lambda_1-\lambda_2)^2,
\]
so (E23a) gives
\[
Q_2(H)\ge\frac14(\lambda_1-\lambda_2)^2
\]
with the conjectured sharp constant.

## 6. The \(d=3\) skew-matrix representation and its obstruction

Let \(A_k\in M_3(\mathbb C)\), \(k=0,1,2\), be the real skew matrices
\[
(A_k)_{ij}=\varepsilon_{kij}.
\tag{E24}
\]
The contraction
\[
\sum_k\varepsilon_{kia}\varepsilon_{kjb}
=\delta_{ij}\delta_{ab}-\delta_{ib}\delta_{aj}
\tag{E25}
\]
gives the exact identity
\[
\boxed{\quad
\mathcal R(M):=\operatorname{Tr}(M)I_3-M
=\sum_{k=0}^2 A_kM^TA_k^\dagger .
\quad}
\tag{E26}
\]
Thus \(\mathcal R\) is completely copositive, and the endpoint coefficient
superoperator satisfies
\[
\mathcal K_3=\frac12(I-\mathcal R).
\tag{E27}
\]
Consequently,
\[
Q_{3,n}(H)
=2^{-n}\left\langle H,(I-\mathcal R)^{\otimes n}(H)\right\rangle.
\tag{E28}
\]

Equation (E26) is the natural \(d=3\) exterior-algebra entry point:
\(A_k\) identifies \(\Lambda^2\mathbb C^3\) with \(\mathbb C^3\).  It does
not by itself give a sum of squares.  A partial application of
\(\mathcal R\) contains a partial transpose, and need not preserve
positivity of an entangled rank-two \(H\).  Therefore expanding (E28) and
declaring its individual skew-matrix terms positive is invalid.  A successful
SOS must pair terms of opposite subset parity and use the single Plücker
vector of the two-dimensional support.

## 7. Quantitative all-copy theorem for normal matrices with product eigenvectors

The copywise-factorized class admits the conjectured sharp quantitative
bound, including arbitrary complex eigenvalues.

**Theorem.**  Suppose
\[
C=\lambda|u\rangle\langle u|+\mu|v\rangle\langle v|,
\qquad
u=\bigotimes_{i=1}^n u_i,\quad
v=\bigotimes_{i=1}^n v_i,
\tag{E29}
\]
where all local vectors are unit and \(u\perp v\).  Then
\[
Q_{d,n}(C)\ge2^{-n}(|\lambda|-|\mu|)^2.
\tag{E30}
\]

**Proof.**  Put \(t_i=|\langle u_i,v_i\rangle|^2\).  On one copy, the
endpoint bilinear form on the two local projectors has diagonal entries
\(1/2\) and off-diagonal entry \(t_i-1/2\).  Tensor factorization gives
\[
Q_{d,n}(C)
=2^{-n}(|\lambda|^2+|\mu|^2)
+2\operatorname{Re}(\overline\lambda\mu)
\prod_{i=1}^n(t_i-\tfrac12).
\tag{E31}
\]
Since \(0\le t_i\le1\),
\[
\left|\prod_i(t_i-\tfrac12)\right|\le2^{-n}.
\]
Applying the triangle inequality to the cross term in (E31) proves (E30).
\(\square\)

If \(\lambda\mu\ne0\), equality requires every \(t_i\in\{0,1\}\) and the
relative eigenvalue phase to make the cross term negative.  Because
\(u\perp v\), at least one \(t_i\) is zero.  Hence the equality codes are,
up to local basis changes, pairs of product strings whose local entries are
at every site either identical or orthogonal, with the corresponding parity
absorbed into the relative phase.  The exact obstruction (E14) is a rotation
inside one such equality support.

### 2026-07-28 10:55 PDT — checkpoint 3

No exact negative normal rank-two example was found.  Dedicated real-normal
searches (positive, projection, and signed eigenvalues) for \(d=3\) through
\(n=5\) converged to zero or positive values.  This is not evidence in the
verification layer, but it makes a simple normal counterexample unlikely.

The \(d=3\) skew expansion (E28) was pursued as an SOS.  Its individual
partial-reduction terms cannot be signed because partial transpose destroys
positivity; grouping only by subset parity reproduces (E9) and gains no new
inequality.  The unresolved exact core is now (E13), equivalently a weighted
Plücker inequality between the \(S^2K\) and one-dimensional
\(\Lambda^2K\) images of \(A\otimes A\).

Best-guess completion toward a full all-copy theorem for all normal rank two:
**35%**.  Best-guess completion toward the exact restricted results and
obstruction analysis recorded here: **95%**.
