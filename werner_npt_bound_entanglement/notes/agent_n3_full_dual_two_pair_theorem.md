# The full three-copy dual: an exact two-pair theorem

## Status

This note proves the full inverse-marginal residual inequality whenever
at most two of the three pair coefficients are nonzero.  Thus, for
every isometry
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
and arbitrary doubly-traceless \(B_{12},B_{13}\),
\[
\boxed{
 \left\langle
 (B_{12}^{(12)}+B_{13}^{(13)})V,\,
 S_V^{-1}(B_{12}^{(12)}+B_{13}^{(13)})V
 \right\rangle
 \leq
 2\bigl(\|B_{12}\|_2^2+\|B_{13}\|_2^2\bigr).
}                                                        \tag{1}
\]
Permutation gives every two-component face.

The proof uses the established unrestricted two-copy endpoint theorem,
one exact fourth-moment calculation in dimension three, and the
elementary fact that tracing a three-dimensional factor can increase
matrix rank by at most a factor of three.  It covers the genuinely
full-qutrit-support case left open by local-support floors.

The dependency-free exact checker is
`verification/verify_n3_full_dual_two_pair_theorem.py`.

## 1. The exact two-component residual

Use the normalized code purification
\[
 |\Psi\rangle
 =\frac1{\sqrt2}\sum_{r=0}^1V|r\rangle\otimes|r\rangle_K,
 \qquad P=|\Psi\rangle\langle\Psi|.                      \tag{2}
\]
Put
\[
 e_i(X)=I_i\otimes\operatorname{Tr}_iX,\qquad
 E_i=e_i-\frac13\operatorname{id},\qquad
 \Phi_i=e_i-\frac12\operatorname{id}.                   \tag{3}
\]
The isometry condition is
\[
 2e_1e_2e_3(P)=I.                                       \tag{4}
\]

The low-sector Schur operator and the two pair-frame operators are
\[
\begin{aligned}
 S_V&=I-\frac16(e_1+e_2+e_3)(P)+\frac1{12}P,\\
 F_{12}&=E_1E_2(P),\qquad F_{13}=E_1E_3(P).
\end{aligned}                                             \tag{5}
\]
Direct expansion gives
\[
\boxed{
\begin{aligned}
 S_V-F_{12}-F_{13}
 &=
 \left[
 2e_1\Phi_2\Phi_3+\frac16(E_2+E_3)
 -\frac1{36}\operatorname{id}
 \right](P).
\end{aligned}}                                           \tag{6}
\]
The first three terms before the final rank-one subtraction are
positive: trace replacement at site \(1\) leaves only the
two-dimensional logical ancilla for the established two-copy
positivity of \(\Phi_2\Phi_3\), while \(E_2,E_3\) are completely
positive.  What remains is the sharp common rank-one domination by
\(P/36\).

We now prove that domination without separating its three positive
terms.

## 2. Intrinsic rank-two form

For an arbitrary test vector \(x\) on the
physical-output--logical space, define
\[
 C=\operatorname{Tr}_K|\Psi\rangle\langle x|.            \tag{7}
\]
Then \(\operatorname{rank}C\leq2\).  Conversely, after choosing its
left two-plane, every matrix of rank at most two has the form (7), up
to an irrelevant common scalar normalization.

Let
\[
 {\cal L}(A)=A-\frac12\operatorname{Tr}(A)I_3.
\]
Define the two-site energy retaining site \(1\):
\[
 q=Q_{23}(C)
 :=\left\langle
 C,(\operatorname{id}_1\otimes{\cal L}_2\otimes{\cal L}_3)(C)
 \right\rangle.                                         \tag{8}
\]
Also put
\[
 T=\operatorname{Tr}_1C.                                \tag{9}
\]
Write \(T=T_0+T_1+T_2\) by the number of traceless local factors on
sites \(2,3\), and set
\[
 w_j=\|T_j\|_2^2.                                       \tag{10}
\]
Thus
\[
 Q_2(T)=\frac14w_0-\frac12w_1+w_2.                      \tag{11}
\]

The standard transition identity
\[
 \langle x,e_S(P)x\rangle
 =\left\|\operatorname{Tr}_{\overline S}C\right\|_2^2
 \tag{12}
\]
and (6) show that \(S_V-F_{12}-F_{13}\succeq0\) is
equivalent to
\[
 2Q_3(C)+3\|\Pi_{011}C\|_2^2\geq0
 \qquad(\operatorname{rank}C\leq2).                     \tag{13}
\]
Here \(\Pi_{011}\) selects the sector scalar on site \(1\) and
traceless on sites \(2,3\).

For completeness, (13) has the following shorter form.  Orthogonality
of the scalar/traceless split on site \(1\) gives the recursion
\[
 Q_3(C)=q-\frac12Q_2(T),                                \tag{14}
\]
while
\[
 3\|\Pi_{011}C\|_2^2=w_2.                              \tag{15}
\]
Therefore the entire two-component theorem is exactly
\[
\boxed{\qquad
 {\cal F}(C):=2q-Q_2(T)+w_2\geq0
 \qquad(\operatorname{rank}C\leq2).
 \qquad}                                                 \tag{16}
\]

## 3. A block-Haar inequality

View \(C\) as a \(3\times3\) block matrix on site \(1\), with
\(9\times9\) blocks.  After an arbitrary unitary change of basis
\(U\) on that site, write the blocks as
\[
 C^U_{ab}
 =
 (\langle a|U^\dagger\otimes I)C(U|b\rangle\otimes I).
 \tag{17}
\]
Every block has rank at most two.  The established unrestricted
two-copy endpoint theorem therefore gives
\[
 Q_2(C^U_{ab})\geq0\qquad(a,b=0,1,2).                  \tag{18}
\]
Moreover, block orthogonality and the fact that the two-copy
superoperator acts only on sites \(2,3\) give
\[
 \sum_{a,b}Q_2(C^U_{ab})=q.                             \tag{19}
\]
In particular,
\[
 q\geq0.                                                \tag{20}
\]

We need one more consequence of the off-diagonal blocks.  If \(x\)
is a uniformly averaged unit vector in \(\mathbb C^3\), direct
unitary invariance and normalization give the fourth moment
\[
 \int x_a\overline{x_b}\,\overline{x_c}x_d\,dx
 =
 \frac{\delta_{ab}\delta_{dc}+\delta_{ac}\delta_{db}}
 {3\cdot4}.                                             \tag{21}
\]
This formula can also be proved without invoking any integration
theorem: phase invariance leaves only the two displayed contractions,
permutation invariance makes their coefficients equal, and
\(\sum_{a,c}|x_a|^2|x_c|^2=1\) fixes the coefficient to \(1/12\).

For
\[
 C_x=(\langle x|\otimes I)C(|x\rangle\otimes I),
\]
substitution of (21) into the polarized quadratic form \(Q_2\)
gives
\[
 \int Q_2(C_x)\,dx=\frac{q+Q_2(T)}{12}.                 \tag{22}
\]
The three diagonal blocks of a uniformly averaged orthonormal basis
therefore have total average
\[
 \frac{q+Q_2(T)}4.                                      \tag{23}
\]
Subtracting this from the invariant total (19), the six off-diagonal
blocks have average
\[
 \frac{3q-Q_2(T)}4.                                     \tag{24}
\]
Every summand being nonnegative by (18), (24) proves
\[
\boxed{\qquad Q_2(T)\leq3q.\qquad}                      \tag{25}
\]

## 4. The rank-six trace bound

Tracing one qutrit can increase matrix rank by at most three.  Indeed,
write
\[
 C=\sum_{\nu=1}^r|u_\nu\rangle\langle v_\nu|,
 \qquad r\leq2,
\]
and split
\[
 u_\nu=\sum_{a=0}^2|a\rangle u_{\nu a},\qquad
 v_\nu=\sum_{a=0}^2|a\rangle v_{\nu a}.
\]
Then
\[
 T=\sum_{\nu=1}^r\sum_{a=0}^2
 |u_{\nu a}\rangle\langle v_{\nu a}|,
 \]
so
\[
 \operatorname{rank}T\leq3r\leq6.                      \tag{26}
\]
The trace/nuclear-norm inequality and Cauchy--Schwarz on the at most
six nonzero singular values give
\[
 |\operatorname{Tr}T|^2
 \leq\|T\|_1^2
 \leq6\|T\|_2^2.                                       \tag{27}
\]
Because
\[
 w_0=\frac19|\operatorname{Tr}T|^2,\qquad
 \|T\|_2^2=w_0+w_1+w_2,
\]
equation (27) is exactly
\[
\boxed{\qquad w_0\leq2w_1+2w_2.\qquad}                 \tag{28}
\]
Using (11),
\[
\boxed{\qquad Q_2(T)\leq\frac32w_2.\qquad}              \tag{29}
\]

## 5. Completion and equality

Put \(t=Q_2(T)\).

If \(t<0\), then (20) gives
\[
 {\cal F}(C)=2q-t+w_2\geq-t+w_2>0.                      \tag{30}
\]

If \(t\geq0\), equations (25) and (29) give
\[
 q\geq\frac t3,\qquad t\leq\frac32w_2.
\]
Consequently
\[
\boxed{
 {\cal F}(C)
 \geq w_2-\frac t3
 \geq\frac12w_2
 \geq0.
}                                                        \tag{31}
\]
In fact, the two cases together give the quantitative face bound
\[
\boxed{\qquad {\cal F}(C)\geq\frac12w_2(T).\qquad}       \tag{31a}
\]
This proves (16), hence (13), hence the operator inequality
\[
 S_V-F_{12}-F_{13}\succeq0.
 \tag{32}
\]
The frame equivalence then proves (1).

The proof also gives a useful exact equality reduction.  Equality in
(16) forces
\[
\boxed{
 q=0,\qquad Q_2(T)=0,\qquad w_2(T)=0.
}                                                        \tag{33}
\]
Conversely these three conditions plainly imply equality.  Thus any
attempt to combine the three two-component faces only has to match
their highly constrained common kernels; a generic full-support code
has strict slack on every face.

There is also an immediate global consequence.  Let
\[
 c_i=\|\Pi_{\{1,2,3\}\setminus\{i\}}C\|_2^2,\qquad
 c=c_1+c_2+c_3=\|\Pi_2C\|_2^2 .
\]
For the face omitting the pair complementary to \(i\), equations
(13), (15), and (31a) say
\[
 2Q_3(C)+3c_i\geq\frac32c_i.
\]
Summing the three inequalities gives the new uniform estimate
\[
\boxed{\qquad
 Q_3(C)\geq-\frac14\|\Pi_2C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
\qquad}                                                  \tag{33a}
\]
In degree masses this is
\[
 -\frac18w_0+\frac14w_1-\frac14w_2+w_3\geq0.
 \tag{33b}
\]
This does not by itself prove \(Q_3(C)\geq0\), but it is a nonlinear
rank-two invariant inherited simultaneously from all three exact
faces.

## 6. Remaining three-component frontier

The proof has an exact slack form which exposes the next obstruction.
For each \(i\), put
\[
\begin{aligned}
 T_i&=\operatorname{Tr}_iC,&
 t_i&=Q_2(T_i),&
 w_i&=w_2(T_i)=3c_i,\\
 q_i&=Q_{\{1,2,3\}\setminus\{i\}}(C),&
 r_i&=\frac32w_i-t_i,&
 s_i&=3q_i-t_i.
\end{aligned}                                            \tag{34}
\]
The rank-six trace argument proves \(r_i\geq0\), while the averaged
off-diagonal block argument proves \(s_i\geq0\).  Substituting
\[
 t_i=\frac32w_i-r_i,\qquad
 q_i=\frac{s_i+t_i}{3}
\]
into the \(i\)-th face functional gives the exact identity
\[
\boxed{
 2Q_3(C)+3c_i
 =\frac12w_i+\frac13r_i+\frac23s_i.
}                                                        \tag{35}
\]
Summing (35) over the three sites, and writing
\[
 R=\sum_i r_i,\qquad S=\sum_i s_i,\qquad
 c=\sum_i c_i,
\]
gives
\[
\boxed{\qquad
 36Q_3(C)=-9c+2R+4S.
\qquad}                                                  \tag{36}
\]
Consequently unrestricted three-copy positivity is now exactly the
common-slack inequality
\[
\boxed{\qquad 2R+4S\geq9c.\qquad}                       \tag{37}
\]
Separate nonnegativity of the six slacks proves all coordinate faces
but not (37).  A successful triangle argument must use the fact that
the three rank-six trace slacks and the three Haar off-diagonal
two-copy slacks arise from the same rank-two matrix \(C\).

The exact full residual is
\[
 S_V-(F_{12}+F_{13}+F_{23})
 =2(\Phi_1\Phi_2\Phi_3)(P).                              \tag{38}
\]
The present theorem proves every \(2\times2\) principal face of its
three-component coefficient Gram.  What remains is a single common
three-component determinant/off-diagonal compatibility problem.  In
particular, no failure can occur on a coordinate plane, including
planes with full qutrit support.
