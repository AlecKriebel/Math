# A same-\(C\) cyclic stationary obstruction outside rank two

## Status

The isotropic \(a=0\) critical-data obstruction can be strengthened
substantially.  It is not excluded by imposing the cross-site
commutator and Jacobi identities.  In fact, for every
\[
 0<\delta<\frac18
 \tag{1}
\]
there is one explicit Hermitian three-qutrit operator \(C_\delta\)
which simultaneously realizes

* the formal sector data
  \[
    x=a=0,\qquad
    c=\frac{2(1+\delta)}3,\qquad
    d=\frac{1-2\delta}{3};
  \]
* all six complete local endpoint, pair-sector, and negative-depth
  Euler forms and positive Hessians;
* every first-order left/right multiplication identity;
* all same-site and cross-site commutator/Jacobi identities.

The operator has rank at least ten.  Thus it is not a Werner
counterexample.  The theorem isolates the missing information more
sharply:
\[
\boxed{\begin{minipage}{0.87\linewidth}
Neither local stationarity nor cyclic compatibility of the local
multiplication maps can force the proposed one-body lower bound.
The next certificate must use the rank-two determinantal relations
jointly with those maps.
\end{minipage}}
\tag{2}
\]

The dependency-free exact checker is
`verification/verify_n3_cyclic_stationary_high_rank_obstruction.py`.

## 1. Two invariant pure-sector operators

Work on \((\mathbb C^3)^{\otimes3}\).  Let \(F_{ij}\) swap tensor
factors \(i,j\), let \(V\) cyclically permute the three factors, and
put
\[
\begin{aligned}
 D_0&=F_{12}+F_{13}+F_{23}-I,\\
 E_0&=V+V^{-1}
 -\frac23(F_{12}+F_{13}+F_{23})
 +\frac49I.
\end{aligned}
\tag{3}
\]

Let \({\cal P}(A)=\operatorname{Tr}(A)I_3/3\) and
\({\cal Q}=I-{\cal P}\) on one local operator factor.  Denote by
\(\Pi_k\) the sum of the tensor products of \({\cal P},{\cal Q}\)
containing exactly \(k\) copies of \({\cal Q}\).

### Lemma 1

The two operators in (3) obey
\[
\boxed{
\begin{aligned}
 \Pi_2D_0&=D_0,& \|D_0\|_2^2&=72,\\
 \Pi_3E_0&=E_0,& \|E_0\|_2^2&=\frac{80}{3},\\
 \langle D_0,E_0\rangle&=0.
\end{aligned}}
\tag{4}
\]
They commute with \(U^{\otimes3}\) for every unitary \(U\), and they
are invariant under every permutation of the three tensor factors.

### Proof

For a Hilbert--Schmidt orthonormal Hermitian basis
\[
 F_0=\frac1{\sqrt3}I_3,\quad F_1,\ldots,F_8
\]
with \(F_1,\ldots,F_8\) traceless, the flip expansion is
\[
 F=\sum_{\mu=0}^8F_\mu\otimes F_\mu.
\tag{5}
\]
Consequently
\[
 F_{ij}-\frac13I
\]
is scalar on the missing site and traceless on the two displayed
sites.  The three summands are orthogonal, proving
\(\Pi_2D_0=D_0\).

Direct partial contraction of \(W=V+V^{-1}\) gives
\[
 \Pi_0W=\frac29I,\qquad
 \Pi_2W=\frac23D_0,\qquad
 \Pi_1W=0.
\tag{6}
\]
Hence \(E_0=W-\Pi_0W-\Pi_2W=\Pi_3W\).

For completeness, all norms follow from
\[
 \operatorname{Tr}P_\pi=3^{\,\#\text{ cycles of }\pi}.
\tag{7}
\]
If \(T=F_{12}+F_{13}+F_{23}\), then
\[
 \operatorname{Tr}T=27,\qquad
 \operatorname{Tr}T^2=99,
\]
and therefore
\[
 \|D_0\|_2^2
 =\operatorname{Tr}(T-I)^2
 =99-54+27=72.
\]
Also \(W^2=W+2I\), so
\[
 \|W\|_2^2=60.
\]
The mutually orthogonal terms in (6) have squared norms
\[
 \left\|\frac29I\right\|_2^2=\frac43,\qquad
 \left\|\frac23D_0\right\|_2^2=32.
\]
Thus
\[
 \|E_0\|_2^2=60-\frac43-32=\frac{80}{3}.
\]
Orthogonality of \(D_0,E_0\) follows from their different degrees.

Every tensor-factor permutation commutes with \(U^{\otimes3}\).
The sums in (3) are central in the permutation algebra, proving both
invariance assertions. \(\square\)

## 2. The exact high-rank stationary family

Put
\[
 c=\frac{2(1+\delta)}3,\qquad
 d=\frac{1-2\delta}{3},
\tag{8}
\]
and define
\[
\boxed{
 C_\delta=
 \sqrt{\frac{c}{72}}\,D_0
 +\sqrt{\frac{3d}{80}}\,E_0.
 }
\tag{9}
\]
The coefficients are positive in (1).  Lemma 1 gives
\[
\boxed{
\begin{aligned}
 \|\Pi_0C_\delta\|^2
 &=\|\Pi_1C_\delta\|^2=0,\\
 \|\Pi_2C_\delta\|^2&=c,\qquad
 \|\Pi_3C_\delta\|^2=d,\\
 \|C_\delta\|^2&=1.
\end{aligned}}
\tag{10}
\]
Since \(L^{\otimes3}\) has eigenvalues \(-1/2\) and \(1\) on
degrees two and three,
\[
\boxed{
 Q_3(C_\delta)=-\frac12c+d=-\delta,\qquad
 \sigma(C_\delta)=2Q_3(C_\delta)+3c=2.
 }
\tag{11}
\]

## 3. Complete local forms

At a fixed site \(i\), define
\[
\begin{aligned}
 h_i^L(A,B)
 &=\langle A_iC_\delta,
 L^{\otimes3}(B_iC_\delta)\rangle,\\
 k_i^L(A,B)
 &=\langle\Pi_2(A_iC_\delta),
 \Pi_2(B_iC_\delta)\rangle.
\end{aligned}
\tag{12}
\]
Define \(h_i^R,k_i^R\) by right multiplication.

The invariances in Lemma 1 imply
\[
 b(UAU^\dagger,UBU^\dagger)=b(A,B)
\tag{13}
\]
for each of these forms, while site-permutation invariance makes the
three left forms equal and the three right forms equal.

We use only the following elementary consequence of (13).  The scalar
line and the traceless matrices are orthogonal, and the restriction
to the traceless matrices is a scalar multiple of the
Hilbert--Schmidt form.  Indeed, an eigenspace of the representing
operator is invariant under every conjugation.  If a nonzero
invariant subspace of the traceless matrices contains \(A\), then
differentiating conjugation by \(e^{tX}\) shows that it contains
\([X,A]\) for every \(X\).  Matrix-unit commutators from any
non-scalar \(A\), followed by further matrix-unit commutators,
generate all traceless matrix units.  Hence there is no proper
nonzero invariant subspace.

The scalar eigenvalues follow from (10)--(11).  The traceless
eigenvalues follow either by the matrix-unit contraction in
Lemma 2 of `agent_n3_stationary_one_body_obstruction.md`, or by a
direct contraction with \(E_{01}\).  The result is
\[
\boxed{
\begin{array}{c|cc}
 &\text{scalar eigenvalue}&\text{traceless eigenvalue}\\ \hline
 h_i^L,\ h_i^R
 &-\delta/3&(5-8\delta)/48\\[1mm]
 k_i^L,\ k_i^R
 &2(1+\delta)/9&(31+22\delta)/216.
\end{array}}
\tag{14}
\]
For reference, before inserting the coefficients of (9), the exact
contractions with a unit traceless matrix are
\[
\begin{array}{c|ccc}
 &D_0,D_0&E_0,E_0&D_0,E_0\\ \hline
 h(E_{01},E_{01})&3/2&65/9&0\\
 k(E_{01},E_{01})&14&10/9&0.
\end{array}
\tag{15}
\]

Let \(n(A,B)=\langle A,B\rangle/3\).  Equations (14) imply
\[
\begin{aligned}
 h_i^{L,R}+\delta n&\succeq0,\\
 \frac{2(1+\delta)}3n-k_i^{L,R}&\succeq0,\\
 m_i^{L,R}
 :=2(1+\delta)h_i^{L,R}+3\delta k_i^{L,R}
 &\succeq0.
\end{aligned}
\tag{16}
\]
Every form in (16) has the scalar line as its kernel.  Thus
\(C_\delta\) is simultaneously stationary, with positive local
Hessian, for the endpoint quotient, the pair-sector quotient, and
the negative-depth quotient under all six one-site filters.

## 4. Full cyclic compatibility

Set
\[
 D=\Pi_2C_\delta=\sqrt{\frac{c}{72}}D_0
\tag{17}
\]
and define the actual first-order multiplication maps
\[
 T_i^L(A)=\Pi_2(A_iC_\delta),\qquad
 T_i^R(A)=\Pi_2(C_\delta A_i).
\tag{18}
\]
Because \(C_\delta-D\) is fully traceless, the local trace of its
commutator vanishes.  Therefore
\[
\boxed{
 T_i^L(A)-T_i^R(A)=[A_i,D].
 }
\tag{19}
\]
These are not abstract maps: they all arise from the one operator
\(C_\delta\).  Consequently, for distinct sites \(i,j\),
\[
\begin{aligned}
 [A_i,[B_j,D]]&=[B_j,[A_i,D]],\\
 [A_i,[B_i,D]]-[B_i,[A_i,D]]
 &=[[A,B]_i,D],
\end{aligned}
\tag{20}
\]
and every higher mixed multiplication identity holds identically.

Thus the common-derivation, same-site Jacobi, and cross-site
integrability constraints do not exclude the stationary data.

## 5. Where the construction fails

On the symmetric tensor subspace, every transposition and both
three-cycles act as the identity.  Hence
\[
 D_0|_{\mathrm{Sym}^3}=2I,\qquad
 E_0|_{\mathrm{Sym}^3}=\frac49I.
\tag{21}
\]
The eigenvalue of \(C_\delta\) there is
\[
 2\sqrt{\frac{c}{72}}
 +\frac49\sqrt{\frac{3d}{80}}>0.
\tag{22}
\]
The symmetric subspace has dimension ten: a basis is given by the
symmetrizations of the ten multisets of size three drawn from three
symbols.  Therefore
\[
\boxed{\operatorname{rank}C_\delta\geq10.}
\tag{23}
\]

Equations (19)--(20) show that imposing cyclic compatibility on the
formal local data is not enough.  Equation (23) identifies the first
missing nonlinear input: the third compound
\[
 \wedge^3 C=0
\tag{24}
\]
must be coupled directly to the local multiplication maps.  Treating
the determinantal condition and cyclic stationarity as separate
constraints loses exactly the information needed to rule out
\(C_\delta\).
