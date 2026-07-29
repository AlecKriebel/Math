# Weighted crossed-kernel trace at four copies

## Checkpoint

**2026-07-28 22:40--23:40 PDT.**  This note records two attempted
separators for the crossed local-effect Hessian.  The coordinate-free
reductions below are exact, but both proposed signs are false.
Section 5 refutes a pointwise sign at a nilpotent rank-one kernel point.
Section 6 gives an exact positive weighted trace which even satisfies
projection origin and local first-order stationarity.  The latter full
kernel restriction remains indefinite, so neither example refutes the
surviving spectral conjecture.

Fix one qutrit site, write \(E=(\mathbb C^3)^{\otimes3}\), and let
\[
 U:\mathbb C^2\longrightarrow\mathbb C^3\otimes E,\qquad
 P=UU^\dagger,\qquad R=\operatorname{Tr}_E P.
\]
Assume first that \(R>0\).  Put
\[
 T(A)=U^\dagger(A\otimes I_E)U,\qquad
 {\cal K}=\ker T
\]
on Hermitian matrices, and polarize the effect Hessian as
\[
 {\cal N}(A,B)=
 \operatorname{Tr}\!\left[
 (P\otimes P)(A\otimes B)
 (F_V-\tfrac12I)K_E
 \right],
 \quad
 K_E=\prod_{i=1}^3(F_i-\tfrac12I).
\tag{1}
\]

## 1. The congruence metric and its exact kernel covariance

Consider the positive inner product
\[
 g_2(A,B)=\operatorname{Tr}(RARB).
\tag{2}
\]
If \(Q=(Q_1,\ldots,Q_k)\) is any real basis of \({\cal K}\), let
\[
 (G_{\cal K})_{\mu\nu}=g_2(Q_\mu,Q_\nu),\qquad
 (H_{\cal K})_{\mu\nu}={\cal N}(Q_\mu,Q_\nu).
\]
The candidate separator was the basis-independent generalized trace
\[
 \tau_2(P)=\operatorname{tr}(G_{\cal K}^{-1}H_{\cal K}).
\tag{3}
\]

Define the positive superoperator
\[
 {\mathscr R}(A)=RAR
\]
and let \(T^*\) denote the Hilbert--Schmidt adjoint.  Thus
\[
 T^*(C)=\operatorname{Tr}_E(UCU^\dagger).
\tag{4}
\]
Put
\[
 {\mathscr G}=T{\mathscr R}^{-1}T^*.
\tag{5}
\]
The \(g_2\)-orthogonal projection onto \(\ker T\) is
\[
 \Pi_{\cal K}^{(g_2)}
 =I-{\mathscr R}^{-1}T^*{\mathscr G}^{+}T,
\tag{6}
\]
and its Hilbert--Schmidt covariance is
\[
 {\cal C}_{\cal K}
 ={\mathscr R}^{-1}
 -{\mathscr R}^{-1}T^*{\mathscr G}^{+}T{\mathscr R}^{-1}.
\tag{7}
\]
Consequently, if \({\mathscr H}\) represents (1) in the
Hilbert--Schmidt metric,
\[
 \boxed{\quad
 \tau_2(P)=\operatorname{Tr}_{\rm HS}
 \bigl({\mathscr H}{\cal C}_{\cal K}\bigr).
 \quad}
\tag{8}
\]
The Moore--Penrose inverse makes (6)--(8) valid without assuming that
\(T\) has real rank four.

For a full \(g_2\)-orthonormal Hermitian basis \((A_\mu)\),
\[
 \sum_{\mu=1}^9A_\mu\otimes A_\mu
 =(R^{-1}\otimes R^{-1})F_V.
\tag{9}
\]
Indeed, if \((\tau_\mu)\) is Hilbert--Schmidt orthonormal then
\(A_\mu=R^{-1/2}\tau_\mu R^{-1/2}\), and (9) follows from
\(\sum_\mu\tau_\mu\otimes\tau_\mu=F_V\).

Choose a Hilbert--Schmidt orthonormal Hermitian logical basis
\((\gamma_a)\), put
\[
 S_a=R^{-1}T^*(\gamma_a)R^{-1},\qquad
 G_{ab}=\langle\gamma_a,T(S_b)\rangle,
\]
and interpret \(G^+\) on the actual range when \(T\) is deficient.
The tensor covariance of a \(g_2\)-orthonormal kernel basis is
\[
 \boxed{\quad
 \Omega_{\cal K}
 =(R^{-1}\otimes R^{-1})F_V
 -\sum_{a,b}(G^+)_{ab}S_a\otimes S_b.
 \quad}
\tag{10}
\]
Equations (1) and (10) give the finite contraction
\[
 \tau_2(P)=
 \operatorname{Tr}\!\left[
 (P\otimes P)\Omega_{\cal K}
 (F_V-\tfrac12I)K_E
 \right].
\tag{11}
\]

## 2. Whitening

Set
\[
 \widehat U=(R^{-1/2}\otimes I_E)U,\qquad
 \widehat P=\widehat U\widehat U^\dagger.
\tag{12}
\]
Then
\[
 \operatorname{Tr}_E\widehat P=I_3.
\tag{13}
\]
For \(B=R^{1/2}AR^{1/2}\),
\[
 {\cal N}_{P}(A,A)={\cal N}_{\widehat P}(B,B),\qquad
 T_P(A)=\widehat U^\dagger(B\otimes I_E)\widehat U.
\tag{14}
\]
Thus \(\tau_2(P)\) is exactly the ordinary Hilbert--Schmidt trace of
the whitened Hessian on the kernel of
\[
 {\cal C}(B)=\widehat U^\dagger(B\otimes I_E)\widehat U.
\tag{15}
\]
The map \({\cal C}\), after the harmless input transpose coming from
reshaping, is a trace-preserving completely positive map from a qutrit
to a qubit.  In particular, every rank-one
\(Z=|x\rangle\langle y|\in\ker{\cal C}^{\mathbb C}\) is traceless:
\[
 \langle y,x\rangle=\operatorname{Tr}Z
 =\operatorname{Tr}{\cal C}(Z)=0.
\tag{16}
\]
Thus whitening turns all rank-one kernel points into nilpotents with
orthogonal factors.

If \(R_a={\cal C}^*(\gamma_a)\) and
\(\widehat G_{ab}=\operatorname{Tr}(R_aR_b)\), then
\[
 \widehat\Omega_{\cal K}
 =F_V-\sum_{a,b}(\widehat G^+)_{ab}R_a\otimes R_b.
\tag{17}
\]
The full Hilbert--Schmidt trace before subtracting the compression
span is
\[
 \operatorname{tr}{\mathscr H}_{\rm full}
 =\frac34h-\frac12F(\widehat P),
\qquad
h=\operatorname{Tr}[(\widehat P\otimes\widehat P)K_E].
\tag{18}
\]
This full trace need not be nonpositive.  Therefore the desired sign
is the genuinely crossed inequality
\[
 \boxed{\quad
 \sum_{a,b}(\widehat G^+)_{ab}
 {\cal N}_{\widehat P}(R_a,R_b)
 \ \geq\
 \frac34h-\frac12F(\widehat P),
 \quad}
\tag{19}
\]
equivalently \(\tau_2(P)\leq0\).

## 3. Purification and residual-channel form

Purify \(\widehat P\) with a qubit \(K\):
\[
 |\Psi\rangle\in V\otimes E\otimes K,\qquad
 \widehat P=\operatorname{Tr}_K|\Psi\rangle\langle\Psi|.
\]
Equation (13) lets us reshape the same tensor as an isometry
\[
 W:V\longrightarrow E\otimes K.
\tag{20}
\]
For \(B\in\ker{\cal C}\), define
\[
 Y_B=\operatorname{Tr}_V[
 (B_V\otimes I)|\Psi\rangle\langle\Psi|]
 =WB^{\mathsf T}W^\dagger.
\tag{21}
\]
Then
\[
 \operatorname{Tr}_E Y_B=0,\qquad
 \|Y_B\|_2=\|B\|_2.
\tag{22}
\]

On two copies of the pure vector, the full replica swap is the
identity.  Hence \(F_V\) may be replaced by \(F_EF_K\), and (1)
becomes
\[
 \boxed{\quad
 {\cal N}_{\widehat P}(B,B)
 =
 \operatorname{Tr}\!\left[
 (Y_B\otimes Y_B)
 \left\{
 F_K\prod_{i=1}^3(I-\tfrac12F_i)
 -\frac12I_K\prod_{i=1}^3(F_i-\tfrac12I)
 \right\}
 \right].
 \quad}
\tag{23}
\]
Writing
\[
 Y_{B,a}=\operatorname{Tr}_K(\sigma_aY_B),
\]
one has \(\operatorname{Tr}Y_{B,a}=0\) for all four Pauli indices and
\[
 {\cal N}_{\widehat P}(B,B)
 =\frac12\sum_{a=0}^3\widetilde f_3(Y_{B,a})
 -\frac12 f_3(Y_{B,0}),
\tag{24}
\]
where
\[
 \begin{aligned}
 f_3(Y)&=\operatorname{Tr}[
 (Y\otimes Y)\prod_i(F_i-\tfrac12I)],\\
 \widetilde f_3(Y)&=\operatorname{Tr}[
 (Y\otimes Y)\prod_i(I-\tfrac12F_i)].
 \end{aligned}
\]
For traceless Hermitian \(Y\), if
\[
 m_S(Y)=\|\operatorname{Tr}_{S^c}Y\|_2^2,
\]
then
\[
 \begin{aligned}
 f_3(Y)
 &=m_{123}-\frac12\sum_{|S|=2}m_S
   +\frac14\sum_{|S|=1}m_S,\\
 \widetilde f_3(Y)
 &=-\frac18m_{123}+\frac14\sum_{|S|=2}m_S
   -\frac12\sum_{|S|=1}m_S.
 \end{aligned}
\tag{25}
\]

There is a compact residual-channel statement.  For
\(S\subseteq E\cup\{K\}\), let
\[
 {\cal E}_S(B)=\operatorname{Tr}_{S^c}(WB^{\mathsf T}W^\dagger),
\quad
\Pi=I-{\cal C}^*({\cal C}{\cal C}^*)^+{\cal C},
\]
and set
\[
 t_S=\|{\cal E}_S\Pi\|_{\rm HS}^2.
\tag{26}
\]
Thus \(t_S\) is the sum of
\(\|\operatorname{Tr}_{S^c}Y_B\|_2^2\) over any
Hilbert--Schmidt orthonormal basis of \(\ker{\cal C}\).  In particular,
\[
 t_\varnothing=t_K=0,\qquad
 t_{E\cup K}=\dim_{\mathbb R}\ker{\cal C}.
\tag{27}
\]
Expanding (23) gives
\[
 \boxed{\quad
 \tau_2
 =
 \sum_{Q\subseteq E}(-\tfrac12)^{|Q|}t_{K\cup Q}
 -\frac12\sum_{R\subseteq E}
   (-\tfrac12)^{3-|R|}t_R.
 \quad}
\tag{28}
\]
For a full-rank compression, \(t_{E\cup K}=5\), so equivalently
\[
 \begin{aligned}
 \tau_2={}&-\frac58
 -\frac12\sum_i t_{Ki}
 +\frac14\sum_{i<j}t_{Kij}\\
 &-\frac18\sum_i t_i
 +\frac14\sum_{i<j}t_{ij}
 -\frac12t_E.
 \end{aligned}
\tag{29}
\]
The initially proposed target was that the right side of (28) is always
nonpositive for an isometry (20).  Section 6 disproves this.

There is also an exact full-Casimir identity.  Let
\((\tau_\nu)_{\nu=1}^9\) be a Hilbert--Schmidt orthonormal Hermitian
basis of \(M_3\), and put
\[
 Q=WW^\dagger,\qquad Y_\nu=W\tau_\nu^{\mathsf T}W^\dagger.
\]
Then \(Q\) is a rank-three projection, the \(Y_\nu\)'s are an
orthonormal basis of the operators supported on \(\operatorname{ran}Q\),
and
\[
 \sum_{\nu=1}^9Y_\nu\otimes Y_\nu=(Q\otimes Q)F_{E K}.
\tag{30}
\]
It follows that the unrestricted channel norm to any subsystem \(S\)
is the purity of the complementary marginal of \(Q\):
\[
 \boxed{\quad
 t_S^{\rm full}
 :=\sum_{\nu=1}^9
 \|\operatorname{Tr}_{S^c}Y_\nu\|_2^2
 =\operatorname{Tr}[(Q\otimes Q)F_{S^c}]
 =\|\operatorname{Tr}_S Q\|_2^2.
 \quad}
\tag{31}
\]
The four-dimensional space subtracted from this full Casimir has an
equally intrinsic form.  For a qubit observable \(\gamma\),
\[
 W({\cal C}^*\gamma)^{\mathsf T}W^\dagger
 =Q(I_E\otimes\gamma)Q.
\tag{32}
\]
Thus the residual norms (26) are obtained from the full Casimir (31)
by removing, with its exact Gram inverse, the compressed qubit operator
system
\[
 \{Q(I_E\otimes\gamma)Q:\gamma=\gamma^\dagger\}.
\tag{33}
\]
This identifies the remaining target as a Casimir inequality for a
rank-three projection with a distinguished qubit factor.

## 4. Exact and numerical stress data

For
\[
 \begin{aligned}
 u&=(|1001\rangle+|1022\rangle+2|2202\rangle)/\sqrt6,\\
 v&=(2|0022\rangle+|0220\rangle)/\sqrt5,
 \end{aligned}
\]
direct rational contraction gives
\[
\tau_2=-\frac5{16}.
\tag{34}
\]
Here
\[
 R=\operatorname{diag}(1,\tfrac13,\tfrac23).
\]
In the kernel basis
\[
 \operatorname{diag}(0,-2,1),\ X_{02},Y_{02},X_{12},Y_{12},
\]
the Hessian diagonal is
\[
 (-\tfrac5{18},\tfrac16,\tfrac16,-\tfrac1{18},-\tfrac1{18}),
\]
while the \(g_2\)-metric diagonal is
\[
 (\tfrac89,\tfrac43,\tfrac43,\tfrac49,\tfrac49).
\]
The sum of the five entrywise ratios is \(-5/16\), so no spectral
approximation is involved.

For
\[
 \begin{aligned}
 u&=(-|1221\rangle+|2022\rangle+|1202\rangle)/\sqrt3,\\
 v&=(|1122\rangle-|1022\rangle+|0202\rangle)/\sqrt3,
 \end{aligned}
\]
it gives
\[
\tau_2=-\frac7{48}.
\tag{35}
\]
In this case
\[
 R=\operatorname{diag}(\tfrac13,\tfrac43,\tfrac13).
\]
For the kernel basis
\[
 \operatorname{diag}(1,-\tfrac12,1),\
 X_{02},Y_{02},\
 X_{01}+X_{12},Y_{01}+Y_{12},
\]
the Hessian diagonal is
\[
 (-\tfrac5{36},\tfrac1{36},\tfrac1{36},
   -\tfrac16,-\tfrac16)
\]
and the \(g_2\)-metric diagonal is
\[
 (\tfrac23,\tfrac29,\tfrac29,\tfrac{16}9,\tfrac{16}9).
\]
Their generalized trace is \(-7/48\).
These are precisely stress cases where the unrestricted Hessian,
ordinary kernel trace, or kernel determinant has the wrong sign for
simpler scalar arguments.

An initial exact rational discovery audit over 250 additional sparse
frames found no positive value of (3), and initial dense and sparse
searches likewise found no positive value.  The exact counterexample
below shows that those samples missed a thin sparse family.

## 5. A positive nilpotent rank-one-kernel value

Whitening makes \({\cal C}\) trace preserving.  Consequently every
rank-one \(Z=|x\rangle\langle y|\in\ker{\cal C}^{\mathbb C}\) has
\(\langle y,x\rangle=0\).  If \(V_x,V_y:\mathbb C^2\to E\) are the two
conditioned maps, then the kernel equation also gives
\(V_x^\dagger V_y=0\).  It is therefore tempting to conjecture the
pointwise sign
\[
 \langle V_xV_x^\dagger,\Phi_3(V_yV_y^\dagger)\rangle
 -\frac12
 \langle V_yV_x^\dagger,\Phi_3(V_xV_y^\dagger)\rangle
 \leq0.
\tag{36}
\]
This is false.

On the ordered physical support
\[
 |212\rangle,\ |202\rangle,\ |221\rangle,\ |011\rangle
\]
take the two maps
\[
 V=
 \begin{pmatrix}
 -2&1\\1&0\\-4&2\\-4&2
 \end{pmatrix},
\qquad
 W=
 \begin{pmatrix}
 4&6\\0&0\\0&-2\\-2&-1
 \end{pmatrix}.
\tag{37}
\]
Direct multiplication gives
\[
 V^\dagger W=0,\qquad
 \|V\|_2^2=46,\qquad\|W\|_2^2=61.
\tag{38}
\]
Exact three-party contractions give
\[
 \begin{aligned}
 \langle VV^\dagger,\Phi_3(WW^\dagger)\rangle&=\frac{233}{2},\\
 \langle WV^\dagger,\Phi_3(VW^\dagger)\rangle&=\frac{113}{2}.
 \end{aligned}
\tag{39}
\]
After normalizing the two maps, the left side of (36) is therefore
\[
 \boxed{\qquad \frac{353}{11224}>0.\qquad}
\tag{40}
\]
The two normalized row states are orthogonal and can be completed by a
third row state to an isometry \(W_{\rm total}:\mathbb C^3\to
E\otimes\mathbb C^2\).  Hence this is an honest nilpotent rank-one
kernel point of a trace-preserving whitened compression, not merely a
pair of unrelated maps.  Any pointwise proof is impossible; an
aggregate relation among all kernel directions is essential.

## 6. Exact refutation of the weighted-trace sign

Let \(E=(\mathbb C^3)^{\otimes3}\) and retain only the four
\(E\otimes K\) basis vectors
\[
 |122\rangle|1\rangle,\quad
 |220\rangle|0\rangle,\quad
 |220\rangle|1\rangle,\quad
 |212\rangle|0\rangle.
\]
In this ordered output basis, define the isometry
\(W:\mathbb C^3\to E\otimes\mathbb C^2\) by the three columns
\[
 \frac1{\sqrt5}(2,-1,0,0)^{\mathsf T},\qquad
 \frac1{\sqrt{30}}(1,2,-5,0)^{\mathsf T},\qquad
 (0,0,0,1)^{\mathsf T}.
\tag{41}
\]
The columns are orthonormal.  Let
\[
 {\cal C}(B)=\operatorname{Tr}_E(WB^{\mathsf T}W^\dagger).
\]
Its real rank is four.  Direct exact contraction of (23), followed by
the ordinary Hilbert--Schmidt trace on \(\ker{\cal C}\), gives
\[
\boxed{\qquad \tau_2=\frac{59}{312}>0.\qquad}
\tag{42}
\]
For a short independent certificate, an orthogonal kernel basis is
\[
 A_0=
 \begin{pmatrix}
 -17&4\sqrt6&0\\
 4\sqrt6&12&0\\
 0&0&5
 \end{pmatrix},
 \quad X_{02},Y_{02},X_{12},Y_{12}.
\tag{43}
\]
Its squared Hilbert--Schmidt norms are
\[
 650,\ 2,\ 2,\ 2,\ 2,
\]
and the corresponding Hessian diagonal is
\[
 -\frac{375}{4},\quad
 \frac3{20},\quad\frac3{20},\quad
 \frac{11}{60},\quad\frac{11}{60}.
\tag{44}
\]
Therefore
\[
 \tau_2
 =-\frac{375/4}{650}
 +2\frac{3/20}{2}
 +2\frac{11/60}{2}
 =\frac{59}{312}.
\tag{45}
\]
The only nonzero off-diagonal entries in this basis are
\[
 {\cal N}(X_{02},X_{12})
 ={\cal N}(Y_{02},Y_{12})=\frac{\sqrt6}{30}.
\tag{46}
\]
In particular, \(A_0\) is an exact negative direction; the
crossed-kernel spectral conjecture survives this example.

This is not an extraneous trace-preserving channel which cannot arise
from a rank-two projection.  Indeed,
\[
 R=
 \begin{pmatrix}
 13/24&1/\sqrt6&0\\
 1/\sqrt6&1/2&0\\
0&0&23/24
\end{pmatrix}
\tag{47}
\]
is positive definite:
\[
\det R_{\{0,1\}}=\frac5{48}>0,\qquad R_{22}=\frac{23}{24}>0,
\]
and direct multiplication gives
\[
{\cal C}(R)=I_2.
\tag{48}
\]
Consequently
\[
U=(R^{1/2}\otimes I_E)\widehat U
\]
is an isometry whose whitening is exactly (36).  Thus (37) refutes
\(\tau_2\leq0\) even on the projection-origin locus.

Even local first-order criticality does not repair the trace sign.  The
only nonzero kernel pairing of \(R\) is
\[
 {\cal N}(R,A_0)=-\frac{75}{32}.
\]
Since \({\cal N}(A_0,A_0)=-375/4\), the affine representative
\[
 R_{\rm crit}=R-\frac1{40}A_0
 =
 \begin{pmatrix}
 29/30&\sqrt6/15&0\\
 \sqrt6/15&1/5&0\\
0&0&5/6
\end{pmatrix}
\tag{49}
\]
obeys
\[
{\cal C}(R_{\rm crit})=I_2,\qquad
{\cal N}(R_{\rm crit},\ker{\cal C})=0.
\tag{50}
\]
It is positive definite, with leading \(2\times2\) determinant \(1/6\),
and
\[
{\cal N}(R_{\rm crit},R_{\rm crit})=\frac{11}{48}>0.
\tag{51}
\]
Thus the missing hypotheses are genuinely second-order and
negative-value conditions, not merely projection origin or stationarity.

The ordinary crossed-kernel spectral assertion still holds for this
example: a positive trace does not imply positive definiteness.
Although (49) is locally stationary, its endpoint value is positive
and its kernel Hessian has the negative direction \(A_0\).  Thus this
counterexample refutes only the pointwise and scalar-trace shortcuts.
It does not refute the surviving least-support target, where one has
simultaneously a negative endpoint value and
\({\cal N}|_{\ker{\cal C}}\succ0\).

The standard-library verifier
`verification/verify_weighted_trace_counterexample.py` reconstructs
both (37)--(40) and (41)--(51) using exact arithmetic in
\(\mathbb Q(\sqrt5,\sqrt6)\).
