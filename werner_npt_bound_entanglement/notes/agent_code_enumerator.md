# Two-dimensional code swap enumerators

## Research log

### 2026-07-28 09:15 PDT — checkpoint 1

Goal: derive, from first principles, a systematic hierarchy of ``shadow''
inequalities
visible from the joint local-swap distribution of an arbitrary
two-dimensional code, and determine whether they imply the equal-Schmidt
endpoint inequality.

The basic complement transform and a full logical-Pauli Gram identity have
been derived below.  They are exact for every code and every subset of
physical sites.  The scalar nonnegative shadows alone do not immediately
settle the endpoint sign; their coefficient transform has negative middle
layers.

Best-guess completion toward this bounded enumerator investigation:
**35%**.

## 1. Code and swap notation

Let
\[
U:K\longrightarrow\mathcal V:=V_1\otimes\cdots\otimes V_n,
\qquad \dim K=2,
\]
be an isometry, and put
\[
P=UU^\dagger.
\]
For \(T\subseteq[n]\), let \(F_T=\prod_{i\in T}F_i\), where \(F_i\)
swaps the two replicas of \(V_i\).  Define the raw purity moments
\[
A_T:=\operatorname{Tr}[(P\otimes P)F_T]
=\left\|\operatorname{Tr}_{\bar T}P\right\|_2^2.
\tag{C1}
\]
The last equality is the swap contraction, proved by expanding product
indices.

For a local antisymmetry pattern \(R\subseteq[n]\), define
\[
\Pi_R=\prod_{i\in R}\frac{I-F_i}{2}
\prod_{i\notin R}\frac{I+F_i}{2},
\qquad
p_R:=\operatorname{Tr}[(P\otimes P)\Pi_R].
\tag{C2}
\]
Since both factors in the trace are positive,
\[
p_R\ge0.
\tag{C3}
\]
Expanding the projectors gives the exact Walsh transform
\[
\boxed{\quad
p_R=2^{-n}\sum_{T\subseteq[n]}(-1)^{|R\cap T|}A_T.
\quad}
\tag{C4}
\]
Conversely,
\[
A_T=\sum_{R\subseteq[n]}(-1)^{|R\cap T|}p_R.
\tag{C5}
\]

The global swap \(F_{[n]}\) has eigenvalue \((-1)^{|R|}\) on
\(\Pi_R\).  Its compression to \(K\otimes K\) is the logical swap.
Consequently,
\[
\sum_{|R|\ {\rm even}}p_R=\dim S^2K=3,\qquad
\sum_{|R|\ {\rm odd}}p_R=\dim\Lambda^2K=1.
\tag{C6}
\]

## 2. Equal-projection endpoint criterion

On the sector \(R\), the operator
\(\prod_i(F_i-\tfrac12I)\) has eigenvalue
\[
2^{-n}(-3)^{|R|}.
\]
Therefore
\[
\boxed{\quad
Q_n(P)=2^{-n}\sum_{R\subseteq[n]}(-3)^{|R|}p_R.
\quad}
\tag{C7}
\]
Equivalently, with
\[
E_k=\sum_{|R|=k}p_R,
\tag{C8}
\]
the equal-Schmidt projection problem is
\[
\sum_{k\ {\rm even}}3^kE_k
\ \ge\
\sum_{k\ {\rm odd}}3^kE_k,
\tag{C9}
\]
under the code constraints, not merely under
\[
E_k\ge0,\qquad
\sum_{k\ {\rm even}}E_k=3,\qquad
\sum_{k\ {\rm odd}}E_k=1.
\tag{C10}
\]
Conditions (C10) alone are far too weak: they allow all even mass at
\(k=0\) and all odd mass at the largest odd layer.

## 3. Logical Pauli complement identity

Let
\[
\sigma_0=I_2,\quad \sigma_1=X,\quad\sigma_2=Y,\quad\sigma_3=Z
\]
be the Pauli basis, normalized by
\(\operatorname{Tr}(\sigma_a\sigma_b)=2\delta_{ab}\), and define the
physical code operators
\[
\tau_a=U\sigma_aU^\dagger.
\tag{C11}
\]
The elementary Pauli completeness relation is
\[
\sum_{a=0}^3\sigma_a\otimes\sigma_a=2F_K.
\tag{C12}
\]
It follows by checking its action on the four matrix units
\(|r\rangle|s\rangle\).  Conjugating by \(U\otimes U\) gives
\[
\sum_{a=0}^3\tau_a\otimes\tau_a
=2(P\otimes P)F_{[n]}.
\tag{C13}
\]

Multiply (C13) by \(F_T\) and take the trace.  The swap contraction and
\(F_{[n]}F_T=F_{\bar T}\) give
\[
\sum_{a=0}^3
\left\|\operatorname{Tr}_{\bar T}\tau_a\right\|_2^2
=2\left\|\operatorname{Tr}_TP\right\|_2^2.
\tag{C14}
\]
Since \(\tau_0=P\), the three-Pauli shadow
\[
L_T:=
\sum_{a=1}^3
\left\|\operatorname{Tr}_{\bar T}\tau_a\right\|_2^2
\tag{C15}
\]
satisfies
\[
\boxed{\quad
L_T=2A_{\bar T}-A_T\ge0.
\quad}
\tag{C16}
\]
Here (C1) was used carefully:
\(\|\operatorname{Tr}_{\bar T}P\|_2^2=A_T\) and
\(\|\operatorname{Tr}_TP\|_2^2=A_{\bar T}\).

Applying (C16) also to \(\bar T\) gives the exact inversion
\[
A_T=\frac{L_T+2L_{\bar T}}{3},\qquad
A_{\bar T}=\frac{2L_T+L_{\bar T}}{3}.
\tag{C17}
\]
In particular,
\[
\frac12A_T\le A_{\bar T}\le2A_T.
\tag{C18}
\]

Substitution into the endpoint form yields the scalar shadow transform
\[
\boxed{\quad
Q_n(P)
=\frac13\sum_{T\subseteq[n]}
\left[
2\left(-\frac12\right)^{|T|}
+\left(-\frac12\right)^{n-|T|}
\right]L_T.
\quad}
\tag{C19}
\]
The coefficients in (C19) are not all nonnegative.  For odd \(n\), the
member of a complementary pair having the larger cardinality can have a
negative coefficient.  Thus (C16) alone is not an all-copy proof.

## 4. Full Pauli Gram complement identity

The scalar relation (C16) is the trace of a stronger \(3\times3\) identity.
For a subset \(T\), define the trace-preserving reduced code channel
\[
\mathcal N_T:M_2\longrightarrow\operatorname{End}
\left(\bigotimes_{i\in T}V_i\right),
\qquad
\mathcal N_T(B)=\operatorname{Tr}_{\bar T}(UBU^\dagger).
\tag{C20}
\]
Put
\[
J_T=\mathcal N_T(I),\qquad
X_{T,a}=\mathcal N_T(\sigma_a),\quad a=1,2,3,
\tag{C21}
\]
and define
\[
b_{T,a}=\operatorname{Re}\operatorname{Tr}(J_TX_{T,a}),\qquad
(G_T)_{ab}=\operatorname{Re}\operatorname{Tr}(X_{T,a}X_{T,b}).
\tag{C22}
\]

For a unit Bloch vector \(x\in\mathbb R^3\), the logical pure state
\(\rho_x=(I+x\cdot\sigma)/2\) is mapped to
\[
\mathcal N_T(\rho_x)
=\frac12\left(J_T+\sum_ax_aX_{T,a}\right).
\]
Because \(U\rho_xU^\dagger\) is a pure physical state, its reductions to
\(T\) and \(\bar T\) have equal nonzero eigenvalues and hence equal
purities.  Therefore, for every \(\|x\|=1\),
\[
\|J_T+x\cdot X_T\|_2^2
=\|J_{\bar T}+x\cdot X_{\bar T}\|_2^2.
\tag{C23}
\]

Comparing the odd part under \(x\mapsto-x\) gives
\[
b_T=b_{\bar T}.
\tag{C24}
\]
After removing the linear part, the difference of the two quadratic forms
is constant on the unit sphere.  A real symmetric matrix whose quadratic
form is constant on the unit sphere is a scalar multiple of the identity:
testing the coordinate vectors makes the diagonal entries equal, and
testing \((e_a+e_b)/\sqrt2\) makes every off-diagonal entry zero.  Hence
\[
G_T-G_{\bar T}=\delta_T I_3.
\tag{C25}
\]
Taking traces and using (C16) determines
\[
\delta_T=A_{\bar T}-A_T.
\]
Thus the exact matrix shadow identity is
\[
\boxed{\quad
G_T-G_{\bar T}=(A_{\bar T}-A_T)I_3,\qquad
b_T=b_{\bar T}.
\quad}
\tag{C26}
\]
Its trace is precisely \(L_T-L_{\bar T}
=3(A_{\bar T}-A_T)\).

## 5. A second scalar shadow from averaging logical pure states

Every output \(\mathcal N_T(\rho_x)\) is a density matrix, so its purity is
at most one.  Averaging over the unit sphere, using
\(\mathbb E x_a=0\) and
\(\mathbb E x_ax_b=\delta_{ab}/3\), gives
\[
\frac14\left(A_T+\frac13L_T\right)\le1.
\tag{C27}
\]
Using (C16),
\[
\boxed{\quad A_T+A_{\bar T}\le6.\quad}
\tag{C28}
\]
This is sharp for \(T=\varnothing\) or \(T=[n]\), where the two values are
\(4\) and \(2\).

The inequalities (C16), (C28), and the positive-semidefiniteness of every
Pauli Gram matrix \(G_T\) are all direct consequences of the code isometry.
They retain more information than the raw nonnegativity (C3), but a
positive-coefficient derivation of (C9) from them has not yet been found.

### 2026-07-28 09:40 PDT — checkpoint 2

For three physical sites the scalar shadow transform collapses to a single
clean monogamy assertion.  An exact pseudo-enumerator shows that all
subsetwise complement identities and bounds above are insufficient: the
missing ingredient must couple distinct, non-complementary subsets.

Best-guess completion toward the bounded enumerator investigation:
**65%**.

## 6. Three copies are exactly a Pauli-information monogamy problem

For \(n=3\), the coefficient in (C19) depends only on \(s=|T|\):
\[
c_0=\frac{15}{8},\qquad
c_1=-\frac34,\qquad
c_2=0,\qquad
c_3=\frac34.
\tag{C29}
\]
The endpoint subsets have fixed values
\[
A_\varnothing=4,\quad A_{[3]}=2,\qquad
L_\varnothing=0,\quad L_{[3]}=6.
\tag{C30}
\]
Therefore (C19) becomes
\[
\boxed{\quad
Q_3(P)=\frac32-\frac14
\sum_{i=1}^3L_{\{i\}}.
\quad}
\tag{C31}
\]
Thus equal-projection positivity for three copies is equivalent to the
first-principles broadcast-channel inequality
\[
\boxed{\quad
\sum_{i=1}^3\sum_{a=1}^3
\left\|\mathcal N_{\{i\}}(\sigma_a)\right\|_2^2\le6.
\quad}
\tag{C32}
\]

In a fixed logical basis \(u=U|0\rangle,\ v=U|1\rangle\), put
\[
\rho_i^u=\operatorname{Tr}_{\bar i}|u\rangle\langle u|,
\quad
\rho_i^v=\operatorname{Tr}_{\bar i}|v\rangle\langle v|,
\quad
S_i=\operatorname{Tr}_{\bar i}|u\rangle\langle v|.
\]
Directly expanding the three Pauli matrices gives
\[
L_{\{i\}}
=\|\rho_i^u-\rho_i^v\|_2^2+4\|S_i\|_2^2.
\tag{C33}
\]
Consequently (C32) is invariant under changing the logical basis even
though the two displayed terms in (C33) are not.  It says that the total
squared one-site distinguishability and one-site coherence of a logical
qubit cannot exceed \(6\).

Equivalently, for a unit Bloch vector \(x\), let
\(\rho_i^\pm(x)=\mathcal N_{\{i\}}((I\pm x\cdot\sigma)/2)\).  Spherical
averaging gives
\[
\mathbb E_x\|\rho_i^+(x)-\rho_i^-(x)\|_2^2
=\frac13L_{\{i\}}.
\tag{C34}
\]
Hence (C32) is also
\[
\mathbb E_x\sum_{i=1}^3
\|\rho_i^+(x)-\rho_i^-(x)\|_2^2\le2.
\tag{C35}
\]
This makes the missing cross-subset constraint explicit: for one logical
basis classical information can be copied to all three sites, but the two
complementary Pauli directions then carry no one-site information.

## 7. Exact pseudo-enumerator proving subsetwise shadows are insufficient

Consider the following formal swap-sector weights for odd \(n=3\):
\[
p_\varnothing=3,\qquad p_{[3]}=1,\qquad
p_R=0\quad\text{otherwise}.
\tag{C36}
\]
They obey all elementary sector conditions (C3), (C6).  Their inverse Walsh
transform is
\[
A_T=3+(-1)^{|T|}.
\tag{C37}
\]
Thus
\[
(A_T,A_{\bar T})=
\begin{cases}
(4,2),&|T|\text{ even},\\
(2,4),&|T|\text{ odd}.
\end{cases}
\]
Every complement shadow is nonnegative:
\[
L_T=2A_{\bar T}-A_T=
\begin{cases}
0,&|T|\text{ even},\\
6,&|T|\text{ odd},
\end{cases}
\tag{C38}
\]
and every purity shadow is saturated:
\[
A_T+A_{\bar T}=6.
\tag{C39}
\]
The matrix identity (C26) is also algebraically consistent with positive
Gram matrices: take \(G_T=0\) on even layers and \(G_T=2I_3\) on odd
layers, with every \(b_T=0\).

Nevertheless,
\[
Q_3(P)_{\rm formal}
=2^{-3}(3-27)=-3.
\tag{C40}
\]
This formal distribution cannot come from a code: it would make every
one-site channel carry all three Pauli directions,
\(L_{\{i\}}=6\), while every complementary two-site channel carried none.
The contradiction is simultaneous broadcasting to three distinct sites.
Importantly, no individual subset/complement pair detects it.  Therefore:

> Any successful shadow/enumerator proof must include compatibility
> inequalities among at least three non-complementary subsets.  Positivity
> of every sector, Pauli Gram matrix, and subset/complement shadow is not
> sufficient.

The same obstruction exists for every \(n\ge3\), not only \(n=3\).  Fix
any odd subset \(R_0\subseteq[n]\) with \(|R_0|\ge3\), and set
\[
p_\varnothing=3,\qquad p_{R_0}=1,\qquad p_R=0\ \text{otherwise}.
\tag{C40a}
\]
Then
\[
A_T=3+(-1)^{|R_0\cap T|}.
\tag{C40b}
\]
Because \(|R_0|\) is odd, complementary subsets have opposite signs in
(C40b), so all relations (C16), (C28) are again satisfied with
\(L_T\in\{0,6\}\).  But
\[
Q_n(P)_{\rm formal}
=2^{-n}\left(3-3^{|R_0|}\right)<0.
\tag{C40c}
\]
Every singleton \(i\in R_0\) has \(L_{\{i\}}=6\), so the same simultaneous
isometry contradiction proves nonrealizability.  Thus the linear
enumerator relaxation fails uniformly at every copy number from three
onward.

## 8. Lorentzian form of the full complement identity

It is useful to package (C26) without choosing a Pauli direction.  Let
\(\Gamma_T\) be the \(4\times4\) real Gram matrix of
\[
J_T,\ X_{T,1},X_{T,2},X_{T,3}.
\]
Equations (C24)--(C26) give
\[
\boxed{\quad
\Gamma_T-\Gamma_{\bar T}
=(A_T-A_{\bar T})\operatorname{diag}(1,-1,-1,-1).
\quad}
\tag{C41}
\]
Both \(\Gamma_T\) and \(\Gamma_{\bar T}\) are positive semidefinite.
For a Hermitian logical operator
\[
B=b_0I+\sum_ab_a\sigma_a,
\]
(C41) is the exact quadratic identity
\[
\|\mathcal N_T(B)\|_2^2-\|\mathcal N_{\bar T}(B)\|_2^2
=(A_T-A_{\bar T})
\left(b_0^2-\sum_ab_a^2\right).
\tag{C42}
\]
The factor in parentheses is \(\det B\).  Rank-one logical inputs have
zero determinant, recovering equality of complementary reduced purities.
This Lorentzian identity is the complete degree-two information supplied
by a single subset and its complement; the pseudo-enumerator shows why an
all-copy proof needs genuinely multi-subset information.

## 9. Even the full matrix-valued linear enumerator relaxation fails

Define the compressed sector effects on the two logical replicas:
\[
\mathcal E_R
=(U^\dagger\otimes U^\dagger)\Pi_R(U\otimes U).
\tag{C43}
\]
They satisfy
\[
\mathcal E_R\succeq0,\qquad
\sum_R\mathcal E_R=I_{K\otimes K}.
\tag{C44}
\]
Because \(U\otimes U\) intertwines the logical and physical global swaps,
\(\mathcal E_R\) is supported on \(S^2K\) for even \(|R|\) and on
\(\Lambda^2K\) for odd \(|R|\).  The latter space is one-dimensional.
The matrix-valued moments
\[
\mathcal A_T
=(U^\dagger\otimes U^\dagger)F_T(U\otimes U)
=\sum_R(-1)^{|R\cap T|}\mathcal E_R
\tag{C45}
\]
obey
\[
\mathcal A_{\bar T}=F_K\mathcal A_T
=\mathcal A_TF_K.
\tag{C46}
\]
Taking traces recovers (C4)--(C6).

The pseudo-enumerator (C36) lifts to this entire matrix-valued relaxation:
\[
\mathcal E_\varnothing=\Pi_K^+,\qquad
\mathcal E_{[3]}=\Pi_K^-,\qquad
\mathcal E_R=0\quad\text{otherwise}.
\tag{C47}
\]
It satisfies (C44), the parity support rule, and every moment identity
(C45)--(C46), yet its endpoint value is still \(-3\).
For the all-\(n\) version (C40a), simply replace \([3]\) in (C47) by the
chosen odd set \(R_0\); the same conclusions hold.

Therefore positivity, completeness, parity, and complement identities for
the **full logical \(4\times4\) sector effects** are insufficient.  What is
missing is nonlinear tensor-square realizability:
\[
\mathcal E_R=B_R^\dagger B_R,\qquad
B_R=\Pi_R(U\otimes U),
\tag{C48}
\]
with the same one-copy isometry \(U\) in every \(B_R\).  The maps \(B_R\)
cannot be chosen independently; their symmetric and antisymmetric pieces
obey the quadratic Plücker relations of the two code columns.  Thus a purely
linear shadow-enumerator proof, even matrix-valued, cannot establish the
sharp sign unless it adds valid inequalities encoding this common
tensor-square origin.

### Why (C36) is not realizable

The nonrealizability assertion can be checked without invoking any external
result.  For the formal data, every singleton has
\(A_{\{i\}}=2\) and \(L_{\{i\}}=6\).  Equation (C27) then has equality, so
the average purity of \(\mathcal N_{\{i\}}(\rho_x)\) over logical pure states
is one.  Every integrand is at most one and continuous, hence every pure
logical input has a pure one-site output.

If a channel arising as a reduction of the isometry \(U\) has this property,
write the two logical basis outputs as
\[
U|0\rangle=a_0\otimes b_0,\qquad
U|1\rangle=a_1\otimes b_1
\]
across that site and its complement.  Purity of the output for every
superposition forces every
\(a_0\otimes b_0+z\,a_1\otimes b_1\) to be a product vector.  Its \(2\times2\)
coefficient minors, as polynomials in \(z\), then vanish identically.  The
coefficient of \(z\) says that either \(a_0,a_1\) are parallel or
\(b_0,b_1\) are parallel.  The value \(L_{\{i\}}=6\) rules out a constant
one-site channel, so \(a_0,a_1\) are not parallel; hence
\(b_0,b_1\) are parallel and the complementary channel is constant.
It is therefore impossible for two distinct singleton channels, much less
all three, to have \(L_{\{i\}}=6\).  This proves rigorously that (C36) is a
relaxation artifact.

## 10. Two-code enumerator for a general equal-singular-value matrix

The projection case does not exhaust equal Schmidt coefficients.  Let
\[
U,V:K\longrightarrow\mathcal V
\]
be two isometries and
\[
C=UV^\dagger
=\sum_{r=0}^1|u_r\rangle\langle v_r|.
\tag{C49}
\]
Every rank-two matrix with two equal nonzero singular values is a scalar
multiple of this form after absorbing a logical unitary into \(U\).

Let
\[
R_n=\bigotimes_{i=1}^n(I-\tfrac12F_i)
=2^{-n}\sum_R3^{|R|}\Pi_R
\tag{C50}
\]
and compress it between the two codes:
\[
M_{U,V}=(U^\dagger\otimes V^\dagger)R_n(U\otimes V)\succeq0.
\tag{C51}
\]
Direct expansion in the two code bases gives
\[
\boxed{\quad
Q_n(C)=\operatorname{Tr}(F_KM_{U,V}).
\quad}
\tag{C52}
\]
Equivalently, with
\[
\mathcal E_R^{U,V}
=(U^\dagger\otimes V^\dagger)\Pi_R(U\otimes V)\succeq0,
\tag{C53}
\]
\[
Q_n(C)
=2^{-n}\sum_R3^{|R|}
\operatorname{Tr}(F_K\mathcal E_R^{U,V}).
\tag{C54}
\]
Unlike the single-code effects (C43), these effects need not commute with
\(F_K\) and have no parity support rule.  Positivity of \(M_{U,V}\) alone
does not control (C52), since a positive operator can have more trace in
the logical antisymmetric direction than in the symmetric directions.

There is nevertheless an exact two-code Pauli shadow.  Define
\[
\tau_a^{U,V}=U\sigma_aV^\dagger,\qquad
\mathcal L_S^{U,V}
=\sum_{a=1}^3
\left\|\operatorname{Tr}_S\tau_a^{U,V}\right\|_2^2.
\tag{C55}
\]
Pauli completeness gives
\[
\sum_{a=0}^3
(\tau_a^{U,V})^\dagger\otimes\tau_a^{U,V}
=2(P_V\otimes P_U)F_{[n]}.
\tag{C56}
\]
Multiplying by \(F_{\bar S}\), taking the trace, and using the swap
contraction yields
\[
\sum_{a=0}^3
\left\|\operatorname{Tr}_S\tau_a^{U,V}\right\|_2^2
=2\operatorname{Tr}\left[
(\operatorname{Tr}_{\bar S}P_U)
(\operatorname{Tr}_{\bar S}P_V)\right].
\tag{C57}
\]
Hence, with
\[
B_S^{U,V}
=\operatorname{Tr}\left[
(\operatorname{Tr}_{\bar S}P_U)
(\operatorname{Tr}_{\bar S}P_V)\right],
\qquad
D_S^{U,V}=\|\operatorname{Tr}_SC\|_2^2,
\]
one has
\[
\boxed{\quad
\mathcal L_S^{U,V}=2B_S^{U,V}-D_S^{U,V}\ge0.
\quad}
\tag{C58}
\]

Formula (C58) is the exact two-code analogue of (C16).  It introduces the
mixed support purities \(B_S^{U,V}\), so it does not close on the desired
coefficients \(D_S^{U,V}\).  Cauchy--Schwarz only gives
\[
B_S^{U,V}\le
\|\operatorname{Tr}_{\bar S}P_U\|_2
\|\operatorname{Tr}_{\bar S}P_V\|_2,
\tag{C59}
\]
which loses precisely the coupled compensation required by the sharp
equal-Schmidt inequality.  Thus the general two-code problem contains a
strictly harder compatibility layer beyond the already unresolved
single-code broadcast inequality (C32).

## 11. Nesting shadows and a stronger exact pseudo-enumerator

The reduced channels also obey a cross-subset inequality.  If
\(S\subseteq T\), then
\[
\mathcal N_S=\operatorname{Tr}_{T\setminus S}\circ\mathcal N_T.
\]
For an operator \(X\) on \(A\otimes B\),
\[
\|\operatorname{Tr}_BX\|_2^2\le(\dim B)\|X\|_2^2.
\tag{C60}
\]
To prove this, write \(X\) in \(B\)-blocks.  The partial trace is the sum
of its diagonal blocks; Cauchy--Schwarz bounds the squared norm of that sum
by \((\dim B)\) times the sum of the squared diagonal-block norms, which is
at most \((\dim B)\|X\|_2^2\).  Therefore, for qutrit sites,
\[
\boxed{\quad
L_S\le3^{|T\setminus S|}L_T
\qquad(S\subseteq T).
\quad}
\tag{C61}
\]
This already rules out the extreme pseudo-enumerator (C36), because it has
\(L_{\{i\}}=6\) but \(L_{\{i,j\}}=0\).

Even (C61) is not enough.  The following permutation-symmetric formal
three-copy data satisfy every scalar shadow derived above:
\[
A_0=4,\qquad A_1=2,\qquad A_2=\frac52,\qquad A_3=2,
\tag{C62}
\]
where \(A_s\) denotes the common value on subsets of size \(s\).  Their
Walsh sector weights, per individual subset, are
\[
p_0=\frac{39}{16},\qquad
p_1=\frac3{16},\qquad
p_2=\frac3{16},\qquad
p_3=\frac7{16}.
\tag{C63}
\]
They are all nonnegative and have even and odd total masses \(3\) and \(1\).
The Pauli shadows are
\[
L_0=0,\qquad L_1=3,\qquad L_2=\frac32,\qquad L_3=6.
\tag{C64}
\]
Thus every nesting inequality (C61) holds:
\[
3\le3\cdot\frac32,\qquad
\frac32\le3\cdot6,
\]
and all remaining inclusions are weaker.  Complement purity gives
\(A_1+A_2=9/2\le6\).

The full Gram relaxation is again consistent: take
\[
G_0=0,\qquad G_1=I_3,\qquad
G_2=\frac12I_3,\qquad G_3=2I_3,\qquad b_T=0.
\tag{C65}
\]
This satisfies (C26) and positive semidefiniteness.  The full sector POVM
relaxation is obtained by making every even effect a scalar multiple of
\(I_{S^2K}\) with the traces in (C63), and every odd effect the corresponding
scalar on \(\Lambda^2K\).

Nevertheless,
\[
Q_3(P)_{\rm formal}
=\frac18\left[
\frac{39}{16}
-3\left(3\frac3{16}\right)
+9\left(3\frac3{16}\right)
-27\frac7{16}\right]
=-\frac34.
\tag{C66}
\]
Thus sector positivity, all complement identities, full Pauli Gram
positivity, and the natural dimension-dependent nesting inequalities still
do not imply the sign.  A successful all-copy enumerator inequality must be
a sharper nonlinear compatibility condition, not merely data processing
under partial trace.

### 2026-07-28 10:05 PDT — checkpoint 3

The enumerator hierarchy has now been pushed through scalar, Pauli-Gram,
matrix-valued sector, complement, and nesting levels.  Exact negative
pseudo-enumerators survive every relaxation except the most extreme one,
which nesting detects.  No actual two-dimensional code violating the sharp
coupled inequality was found, and no all-\(n\) SOS emerged.

The decisive missing property is common-\(U\) tensor-square realizability,
equivalently the cross-subset Plücker constraints among the maps
\(\Pi_R(U\otimes U)\).  The three-copy projection case is already exactly
the monogamy inequality (C32).

Best-guess completion toward this bounded enumerator investigation:
**95%**.  Completion toward a definitive all-copy equal-Schmidt theorem
remains low; the work here isolates why linear shadow methods do not suffice.

## 12. Long flags reduce the two-code case to code projections

The extra mixed moments in Section 10 make the two-code case harder at a
fixed copy number, but not for an all-copy theorem.  Here is the exact
reduction.

Write the endpoint sesquilinear form as
\[
\mathfrak B_n(A,B)
=\operatorname{Tr}\!\left[A^\dagger L^{\otimes n}(B)\right],
\qquad
L(Z)=Z-\frac12\operatorname{Tr}(Z)I_3.
\tag{C67}
\]
Thus \(Q_n(A)=\mathfrak B_n(A,A)\), and direct tensor contraction gives
\[
\mathfrak B_{n+m}(A\otimes C,B\otimes D)
=\mathfrak B_n(A,B)\mathfrak B_m(C,D).
\tag{C68}
\]

Let \(D=\sum_{i=0}^1|l_i\rangle\langle r_i|\), where each of
\(\{l_0,l_1\}\) and \(\{r_0,r_1\}\) is orthonormal.  Put
\[
P_L=\sum_i|l_i\rangle\langle l_i|,
\qquad
P_R=\sum_i|r_i\rangle\langle r_i|.
\]
For \(m\) new qutrit sites, choose
\[
a=|0\rangle^{\otimes m},\qquad b=|1\rangle^{\otimes m},
\qquad
w_i=a\otimes r_i+b\otimes l_i,
\]
and set
\[
E_m=\sum_{i=0}^1|w_i\rangle\langle w_i|.
\tag{C69}
\]
The two \(w_i\)'s are orthogonal and have squared norm \(2\), so
\[
\frac12E_m
\quad\text{is a rank-two orthogonal projection.}
\tag{C70}
\]

For \(F_{xy}=|x\rangle\langle y|\), direct one-site evaluation and
tensorization give
\[
\begin{aligned}
\mathfrak B_m(F_{aa},F_{aa})
&=\mathfrak B_m(F_{bb},F_{bb})=2^{-m},\\
\mathfrak B_m(F_{aa},F_{bb})
&=\mathfrak B_m(F_{bb},F_{aa})=(-\tfrac12)^m,\\
\mathfrak B_m(F_{ab},F_{ab})
&=\mathfrak B_m(F_{ba},F_{ba})=1,
\end{aligned}
\tag{C71}
\]
and every other pairing among these four flag matrices is zero.  Expanding
\[
E_m
=F_{aa}\otimes P_R+F_{bb}\otimes P_L
+F_{ab}\otimes D^\dagger+F_{ba}\otimes D
\tag{C72}
\]
therefore yields the exact identity
\[
\boxed{\quad
Q_{m+n}(E_m)
=2Q_n(D)
+2^{-m}\!\left[Q_n(P_R)+Q_n(P_L)\right]
+2(-\tfrac12)^m
\operatorname{Re}\mathfrak B_n(P_R,P_L).
\quad}
\tag{C73}
\]
All quantities after \(2Q_n(D)\) are fixed finite scalars times a factor
whose magnitude tends to zero.  Hence
\[
Q_n(D)<0
\quad\Longrightarrow\quad
Q_{m+n}(E_m)<0
\quad\text{for every sufficiently large finite }m.
\tag{C74}
\]
Homogeneity and (C70) then give a negative rank-two **code projection**.

Consequently, positivity of \(Q_N(P)\) for every copy number \(N\) and every
rank-two orthogonal projection \(P\) rules out every equal-singular
partial-isometry witness.  Thus the nonlinear common-\(U\) problem isolated
above is globally decisive for the equal-singular case, even though its
fixed-\(n\) enumerator is simpler than the two-code enumerator.

### Copy doubling removes unequal singular values

For completeness, the equal-singular hypothesis can also be removed exactly.
Let a negative rank-two matrix have a singular decomposition
\[
C=s_1C_1+s_2C_2,\qquad
C_i=|u_i\rangle\langle v_i|,
\tag{C75}
\]
with both displayed pairs orthonormal.  Define the Hermitian \(2\times2\)
matrix
\[
H_{ij}=\mathfrak B_n(C_i,C_j).
\tag{C76}
\]
The diagonal entries are nonnegative by the all-copy rank-one bound.  Since
some linear combination of the \(C_i\)'s has negative quadratic form,
\(H\) is not positive semidefinite and hence
\(\det H<0\).

Now set
\[
D=C_1\otimes C_2-C_2\otimes C_1.
\tag{C77}
\]
Its two left vectors are orthonormal, as are its two right vectors, so its
two nonzero singular values are both one.  Tensor factorization gives
\[
\boxed{\quad
Q_{2n}(D)
=2H_{11}H_{22}-2H_{12}H_{21}
=2\det H<0.
\quad}
\tag{C78}
\]
Applying the long-flag construction (C69)--(C74) to \(D\) produces a
negative rank-two orthogonal projection after finitely many additional
copies.  The converse is immediate.  Therefore the complete all-copy
endpoint problem is exactly equivalent to
\[
\boxed{\quad
Q_n(P)\ge0
\quad\text{for every }n
\text{ and every rank-two orthogonal projection }P.
\quad}
\tag{C79}
\]
This makes the common-\(U\) tensor-square constraints the central problem,
not a restricted subclass.

## 13. The exact nonlinear core at three copies

Write
\[
E_k=\sum_{|R|=k}p_R.
\]
For \(n=3\), (C6) says
\[
p_\varnothing+E_2=3,\qquad E_1+p_{[3]}=1.
\tag{C80}
\]
Substituting these identities in (C7) eliminates the zero-weight layers:
\[
\boxed{\quad
Q_3(P)=E_2-3p_{[3]}.
\quad}
\tag{C81}
\]
Thus the precise three-copy Plücker inequality is
\[
\boxed{\quad E_2\ge3p_{[3]}.\quad}
\tag{C82}
\]
The left side is the total squared norm of the three components in which
two physical replica pairs are antisymmetric and the remaining pair is
symmetric.  The right side is three times the squared norm of the component
in which all three pairs are antisymmetric.  The latter is carried by the
single logical bivector \(u\wedge v\).  Conditions (C43)--(C48) explain why
an arbitrary sector POVM need not obey (C82): it is a nonlinear consequence,
if true, of that bivector's common tensor-square origin.

There is an equivalent entropy form.  Normalize the code state as
\[
\rho=\frac12P,\qquad
s_T=1-\operatorname{Tr}(\rho_T^2).
\tag{C83}
\]
Since \(\operatorname{Tr}\rho^2=1/2\), direct substitution in the
partial-trace formula gives
\[
\boxed{\quad
Q_3(P)
=2\sum_{|T|=2}s_T-\sum_{|T|=1}s_T-\frac32.
\quad}
\tag{C84}
\]
Equivalently,
\[
Q_3(P)
=\sum_{i=1}^3
\left(s_{\{i,j\}}+s_{\{i,k\}}-s_{\{i\}}-s_{[3]}\right),
\qquad \{i,j,k\}=[3].
\tag{C85}
\]
Hence the Pauli broadcast inequality (C32), the sector inequality (C82),
and nonnegativity of the **cyclic sum** of the three linear-entropy
differences in (C85) are exactly the same assertion.

The cyclic qualification is essential.  The individual summands in (C85)
can be negative, even for a sparse exact code.  Take
\[
\begin{aligned}
u&=\frac{|212\rangle+|220\rangle}{\sqrt2},\\
v&=\frac{|012\rangle+|020\rangle+|210\rangle}{\sqrt3}.
\end{aligned}
\tag{C86}
\]
The vectors are orthonormal.  For \(P=|u\rangle\langle u|+
|v\rangle\langle v|\), direct contraction gives
\[
\begin{array}{c|cccccc}
T&\{A\}&\{B\}&\{C\}&\{A,B\}&\{A,C\}&\{B,C\}\\ \hline
A_T&20/9&37/18&37/18&25/18&25/18&26/9 .
\end{array}
\tag{C87}
\]
For example, \(\operatorname{Tr}_{BC}P\) is diagonal with entries
\(2/3,0,4/3\), giving \(A_A=20/9\).  The other five values follow by the
same two- or three-term contraction, so (C87) is an exact rational
calculation.
After division by four to obtain the purities of \(\rho=P/2\), the three
summands in (C85) are
\[
\frac{13}{36},\qquad-\frac1{18},\qquad-\frac1{18}.
\tag{C88}
\]
Equivalently, the relevant exact sector weights are
\[
p_{AB}=p_{AC}=\frac19,\qquad
p_{BC}=\frac{19}{36},\qquad p_{ABC}=\frac16.
\tag{C88a}
\]
Their sum is \(Q_3(P)=1/4>0\).  Thus proving three separate
linear-entropy inequalities is impossible; the proof must retain the cyclic
compensation.

An apparently natural spectral decoupling fails as well.  In a logical
basis \(u,v\), put
\[
x_i=\operatorname{Tr}(\rho_i^u\rho_i^v),\qquad
y_i=\operatorname{Tr}(\rho_{\bar i}^u\rho_{\bar i}^v).
\tag{C89}
\]
Equation (C33) gives
\[
\sum_iL_{\{i\}}
=\sum_i\left[
\operatorname{Tr}\!\left[(\rho_i^u)^2\right]
+\operatorname{Tr}\!\left[(\rho_i^v)^2\right]
-2x_i+4y_i\right].
\tag{C90}
\]
Bounding the six individual purities by one would reduce (C32) to the
tempting inequality
\[
\sum_i x_i\ge2\sum_i y_i.
\tag{C91}
\]
It is false at the sharp boundary.  For
\[
u=\frac{|000\rangle+|111\rangle}{\sqrt2},\qquad
v=\frac{|000\rangle-|111\rangle}{\sqrt2},
\tag{C92}
\]
one has \(x_i=y_i=1/2\) for all three sites, so the two sides of (C91) are
\(3/2\) and \(3\).  At the same time every one-site purity in (C90) is
\(1/2\), exactly compensating the negative cross term and giving
\(\sum_iL_{\{i\}}=6\).

This leaves (C82) as the smallest exact unresolved statement exposed by the
enumerator analysis: a cyclic comparison between the \(S^2K\) and
\(\Lambda^2K\) images that cannot be decomposed into independent cuts or
independent spectral terms.

## 14. An orthonormal-family kernel strengthening is false

One might try to prove the quantitative positive-matrix conjecture by a
stronger positive-definite-kernel statement on every orthonormal family.
That strengthening would also apply to arbitrary signed Hermitian spectral
coefficients, and it is false.

At two copies let
\[
X=|0\rangle\langle1|+|1\rangle\langle0|,
\qquad C=I_3\otimes X.
\tag{C93}
\]
The matrix \(C\) is Hermitian, \(\operatorname{Tr}C=0\), and
\(\|C\|_2^2=6\).  Since
\[
L(I_3)=-\frac12I_3,\qquad L(X)=X,
\]
tensor factorization gives
\[
Q_2(C)
=\langle I_3,L(I_3)\rangle
\,\langle X,L(X)\rangle
=-\frac32\cdot2=-3,
\tag{C94}
\]
whereas
\[
2^{-2}\left(2\|C\|_2^2-|\operatorname{Tr}C|^2\right)=3.
\tag{C95}
\]
Diagonalizing \(C\) therefore gives an orthonormal eigenfamily and a real
signed coefficient vector on which the proposed kernel matrix has a
negative quadratic form.  This does **not** refute copositivity for
nonnegative spectral coefficients \(H\succeq0\); it only shows that replacing
that copositivity problem by positive semidefiniteness of the full
orthonormal-family kernel loses valid cases.

### 2026-07-28 10:45 PDT — checkpoint 4

The projection reduction is now complete, including unequal singular
values.  At three copies the target has been reduced to the single cyclic
Plücker inequality (C82), and exact examples rule out two plausible
decouplings of it.  No proof of (C82), all-\(n\) recursion, or actual
negative projection has been obtained.

Best-guess completion toward this bounded enumerator and obstruction
investigation: **100%**.  Completion toward the definitive all-copy theorem
remains unresolved.
