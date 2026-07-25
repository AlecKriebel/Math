# Working classification: ramification in the line-image \((1,4)\) stratum

**Status:** proved and independently adversarially audited.  The audit caught
and repaired the combined-\(r\)-syzygy issue in the \(\{2,2\}\) splitting.
This is not peer reviewed, and no priority claim is made.

**Recorded:** 2026-07-25T00:34:00Z.

## 1. Setup

Continue the notation of `WORKING_LINE_TYPE_14.md`:
\[
H_4=(P(p,q),Q(p,q),0),\qquad
H_3=(U,V,R),\qquad H_2=(A,B,W),
\]
where \(P,Q\) are coprime binary quartics and
\[
a=J(Q,R),\qquad b=J(P,R),\qquad c=J(P,Q).
\tag{1}
\]
Put
\[
g=\gcd(a,b,c),\qquad \delta=\deg g.
\tag{2}
\]
The banked gcd-one theorem treats \(\delta=0\).  This note classifies the
possible syzygy shapes when \(\delta>0\).

The branch \(R=0\) is already an automorphism by the quadratic-component
exit, because the third component of the full map then has degree at most
two.  Throughout the unresolved counterexample analysis below, therefore,
\(R\ne0\).

## 2. Hilbert--Burch classification

Assume first that \(a,b\) are linearly independent.  Put
\[
d=5-\delta,\qquad
(a_0,b_0,c_0)=\left(\frac ag,-\frac bg,\frac cg\right),
\tag{3}
\]
whose degrees are \((d,d,d+1)\).  The triple has gcd one, so its homogeneous
syzygy module over \(S=\mathbb C[p,q]\) is free of rank two.  If the total
degrees of a minimal basis are \(e_1,e_2\), Hilbert--Burch gives
\[
e_1+e_2=3d+1.
\tag{4}
\]

The two gradient columns
\[
\sigma_p=(P_p,Q_p,R_p)^T,\qquad
\sigma_q=(P_q,Q_q,R_q)^T
\]
are independent syzygies of total degree \(d+3\); independence follows from
\(J(P,Q)=c\ne0\).  Hence \(e_i\le d+3\).  Since \(a_0,b_0\) are not
constant-linearly dependent, no syzygy has total degree below \(d+1\).
Writing
\[
k_i=d+3-e_i
\tag{5}
\]
therefore gives
\[
0\le k_i\le2,\qquad k_1+k_2=\delta.
\tag{6}
\]
In particular,
\[
\boxed{\delta\le4}
\]
and the only multisets are
\[
\begin{array}{c|c}
\delta&\{k_1,k_2\}\\ \hline
1&\{1,0\}\\
2&\{2,0\}\ \text{or}\ \{1,1\}\\
3&\{2,1\}\\
4&\{2,2\}.
\end{array}
\tag{7}
\]

If \(N_i=(u_i,v_i,w_i)^T\) is the basis column associated with \(k_i\),
its component degrees are
\[
\deg(u_i,v_i,w_i)=(3-k_i,3-k_i,2-k_i).
\tag{8}
\]
Moreover
\[
\begin{pmatrix}\sigma_p&\sigma_q\end{pmatrix}
=\begin{pmatrix}N_1&N_2\end{pmatrix}C,
\qquad
\det C\in\mathbb C^\times g,
\tag{9}
\]
where row \(i\) of \(C\) has degree \(k_i\).

## 3. The exceptional power fibre

Assume \(R\ne0\).  If \(a,b\) are linearly dependent, some nonzero
\(S=\alpha P+\beta Q\) satisfies
\[
J(S,R)=0.
\]
Unique factorization and \(\gcd(4,3)=1\) give
\[
S=\lambda L^4,\qquad R=\mu L^3.
\tag{10}
\]
Conversely (10) makes \(a,b\) dependent.  After normalization
\[
P=p^4,\qquad R=p^3,
\]
one has
\[
b=0,\qquad a=-3p^2Q_q,\qquad c=4p^3Q_q,
\]
and therefore
\[
\delta=5,\qquad g=p^2Q_q
\tag{11}
\]
up to a nonzero constant.  Thus degree five occurs exactly in the
power-fibre exception already isolated by the primitive line theorem.

In this normalization, degree seven becomes
\[
-3U_r+4pW_r=0,
\]
so
\[
U=\frac43pW+U_0(p,q),
\qquad V\ \text{is unrestricted at this degree}.
\tag{11a}
\]
The exact degree-six identity then simplifies to
\[
\begin{aligned}
0={}&-3p^2Q_qA_r+4p^3Q_q\lambda\\
&+W_r\!\left[
\left(\frac43W+(U_0)_p\right)Q_q-(U_0)_qQ_p
\right]
+3p^2(U_0)_qV_r ,
\end{aligned}
\tag{11b}
\]
and in particular
\[
Q_q\mid (U_0)_q\bigl(3p^2V_r-Q_pW_r\bigr).
\tag{11c}
\]

## 4. Exact degree-seven normal form

The degree-seven Keller identity is
\[
aU_r-bV_r+cW_r=0.
\tag{12}
\]
After division by \(g\), it is a syzygy of the reduced triple (3).  Extending
the basis \(N_1,N_2\) from \(S\) to \(S[r]\) gives the exact expression
\[
(U_r,V_r,W_r)^T
=f_1N_1+f_2N_2,\qquad
\deg f_i=k_i-1.
\tag{13}
\]
Terms with \(k_i=0\) do not occur.  A \(k_i=1\) column enters with a
constant multiplier, while a \(k_i=2\) column enters with an arbitrary
linear form in \(p,q,r\).  Hence (7) is also a complete list of the possible
third-direction dependence left after degree seven.

## 5. Local form of a ramification root

For every linear factor of \(g\), move it to \(q=0\).  Target changes in the
\((P,Q)\)-plane and a source shear preserving that point put
\[
\begin{aligned}
P&=p^4+A_0p^2q^2+B_0pq^3+C_0q^4,\\
Q&=D_0p^2q^2+E_0pq^3+F_0q^4,\\
R&=G_0p^3+H_0pq^2+I_0q^3.
\end{aligned}
\tag{14}
\]
Indeed, the common-Jacobian conditions successively kill the \(p^4\) and
\(p^3q\) terms of \(Q\), the \(p^3q\) term of \(P\), and the \(p^2q\)
term of \(R\).  Then
\[
N_q=\left(\frac{P_q}{q},\frac{Q_q}{q},\frac{R_q}{q}\right)^T
\tag{15}
\]
is the canonical syzygy attached to that root.

Because \(P,Q\) are coprime,
\[
\operatorname{ord}_q c=\operatorname{ord}_qQ-1\le3.
\]
Thus every root of \(g\) has multiplicity at most three outside the
power-fibre case.  Up to \(\operatorname{PGL}_2\), the possible necessary
ramification divisors are therefore
\[
\begin{array}{c|l}
\delta&g\\ \hline
1&q\\
2&q^2,\ pq\\
3&q^3,\ q^2p,\ pq(p-q)\\
4&q^3p,\ q^2p^2,\ q^2p(p-q),\
pq(p-q)(p-\lambda q).
\end{array}
\tag{16}
\]
This is a necessary divisor list, not an existence assertion for Keller
maps.

## 6. The exact degree-six frontier

Let \(\lambda=(L_0)_{3r}\).  Without assuming that \(U,V,W\) are binary,
the degree-six identity is
\[
aA_r-bB_r+c\lambda+T_6=0,
\tag{17}
\]
where
\[
\begin{aligned}
T_6={}&
\det(dP,dV,dW)
+\det(dU,dQ,dW)\\
&+\det(dU,dV,dR).
\end{aligned}
\tag{18}
\]
Consequently \(g\mid T_6\), and after division by \(g\), the polynomial
\(-T_6/g\) must lie in the degree-six image generated by
\(a_0,b_0,c_0\) with coefficient degrees \(1,1,0\).

The kernel dimension of this degree-six map is exactly the number of
\(k_i=2\) columns:
\[
\begin{array}{c|c}
\{k_1,k_2\}&\dim\ker\\ \hline
\{1,0\},\{1,1\}&0\\
\{2,0\},\{2,1\}&1\\
\{2,2\}&2.
\end{array}
\tag{18a}
\]

For \(\delta=0\), (13) makes \(U,V,W\) binary, so \(T_6=0\); equation (17)
then recovers the already banked gcd-one proof exactly.  For
\(\delta>0\), the curvature term \(T_6\) cannot be discarded.

The top \(r\)-coefficient already gives a useful exact obstruction.  Sum
the \(r\)-parts of all \(k=2\) multipliers and put
\[
N_\gamma=\sum_{k_i=2}\gamma_iN_i=(u,v,w).
\tag{19}
\]
The \(r^3\)-coefficient of \(T_6\) forces
\[
C(N_\gamma)=0.
\tag{19a}
\]
Here
\[
2C(N)=
wJ(P,v)+wJ(u,Q)-vJ(u,R)+uJ(v,R).
\tag{20}
\]
This combined formulation is essential in the \(\{2,2\}\) case: the
quadratic expression has cross terms and cannot be applied to the two basis
columns separately.  Since the \(N_i\) form a basis, \(N_\gamma=0\) is
equivalent to the vanishing of every \(\gamma_i\).  Thus all \(r\)-parts
vanish unless their nonzero combined syzygy lies on the explicit
contact-divergence locus.

The latter locus has one exact unresolved normal form.  If \(w=0\), the
nonzero combined syzygy normalizes to \(N_\gamma=(p,q,0)\) and
\[
C(N_\gamma)=-\frac32R\ne0.
\]
Here \(u,v\) must be independent: dependence would turn the syzygy into a
constant-linear dependence between \(a_0,b_0\).  When \(w\ne0\), rank zero
for \((u,v)\) would force \(c_0=0\), so the remaining ranks are one and two.
If \(w\ne0\) and \(\operatorname{rank}(u,v)=1\), normalize to
\(N_\gamma=(p,0,1)\); then
\[
C(N_\gamma)=\frac12Q_q\ne0.
\]
Indeed, \(Q_q=0\) would give \(Q=\kappa p^4\), while the syzygy gives
\(P_q=pR_q\), hence \(P-pR\in\mathbb C[p]\).  Then \(p\) divides both
\(P\) and \(Q\), contradicting coprimality.  If
\(w\ne0\) and \(\operatorname{rank}(u,v)=2\), normalize to
\(N_\gamma=(p,q,1)\).  In that case
\[
C(N_\gamma)=\frac12(P_p+Q_q-3R),
\]
so an \(r\)-multiplier can survive only on
\[
\boxed{
R=\frac{P_p+Q_q}{3},\qquad
pJ(Q,R)-qJ(P,R)+J(P,Q)=0.
}
\tag{20a}
\]

Once \(s=(u,v,w)=(U_r,V_r,W_r)\) is binary, write
\[
(U,V,W)=(U_0,V_0,W_0)+rs.
\]
The coefficient of \(r\) in \(T_6\) is
\[
\begin{aligned}
K(s)={}&
P_p(v_qw-vw_q)-P_q(v_pw-vw_p)\\
&+w(u_pQ_q-u_qQ_p)+u(Q_pw_q-Q_qw_p)\\
&+v(u_qR_p-u_pR_q)+u(v_pR_q-v_qR_p).
\end{aligned}
\tag{20b}
\]
Equation (17) requires the sharper membership condition
\[
K(s)\in\operatorname{span}_{\mathbb C}\{a,b\}.
\tag{20c}
\]

For \(\delta=1\), one has \(s=\kappa N_q\).  In the local form (14), the
necessary divisibility \(q\mid K(s)\) gives
\[
\kappa^2
\left[4(E_0H_0-D_0I_0)+3G_0(B_0D_0-A_0E_0)\right]=0.
\tag{20d}
\]
If the bracket is nonzero, \(s=0\); since the \(\{1,0\}\) splitting has no
\(k=2\) kernel in (18a), equation (17) then forces
\[
A_r=B_r=\lambda=0
\]
and the binary plane-shear argument proves that \(F\) is an automorphism.
The vanishing-bracket locus still has to pass the stronger test (20c).

## 7. Exact representatives

Each nonexceptional splitting type in (7) occurs at the level of the binary
ramification data.  The following table records one exact representative;
the verification harness checks its gcd and displayed basis syzygies.

\[
\begin{array}{c|c|c}
\delta,\{k_i\}&(P,Q,R)&\text{basis columns shown by }(u,v,w)\\ \hline
1,\{1,0\}&
\begin{gathered}
p^4+p^2q^2+pq^3+q^4,\\
p^2q^2+pq^3+2q^4,\\
p^3+2pq^2+3q^3
\end{gathered}&
(2p^2+3pq+4q^2,\ 2p^2+3pq+8q^2,\ 4p+9q)
\\[6pt]
2,\{1,1\}&
\begin{gathered}
p^4+p^2q^2+2q^4,\\
2p^4+3p^2q^2+q^4,\\
p^3+q^3
\end{gathered}&
\begin{gathered}
(4p^2+2q^2,\ 8p^2+6q^2,\ 3p),\\
(2p^2+8q^2,\ 6p^2+4q^2,\ 3q)
\end{gathered}
\\[6pt]
2,\{2,0\}&
\begin{gathered}
p^4+pq^3+q^4,\\
pq^3+2q^4,\\
p^3+q^3
\end{gathered}&
(3p+4q,\ 3p+8q,\ 3)
\\[6pt]
3,\{2,1\}&
\begin{gathered}
p^4+4p^2q^2+4pq^3+2q^4,\\
q^4,\\
p^3+3pq^2+3q^3
\end{gathered}&
\begin{gathered}
(52p+40q,\ -8p+12q,\ 39),\\
(-q(5p+q),\ p^2+q^2,\ 0)
\end{gathered}
\\[6pt]
4,\{2,2\}&
\begin{gathered}
p^4+2q^4,\ q^4,\ p^3+q^3
\end{gathered}&
\begin{gathered}
(-p+2q,\ q,\ 0),\\
(4p,\ 0,\ 3).
\end{gathered}
\end{array}
\]

These are ramification and syzygy examples, not Keller maps.  In particular,
\(g\ne1\) does not by itself force the power-fibre case.

## 8. Sharpness of the degree-six frontier

The first three top identities do not always kill a nonzero \(k=1\)
syzygy.  Take
\[
\begin{aligned}
P&=p^4+p^2q^2+q^4,\\
Q&=p^2q^2+2q^4,\\
R&=p^3+2pq^2,
\end{aligned}
\qquad
N=(2p^2+4q^2,\ 2p^2+8q^2,\ 4p).
\]
Here \(g=q\).  Set
\[
U=rN_1,\qquad V=rN_2,\qquad W=rN_3,\qquad
A=4r^2,\qquad B=8r^2,
\]
and take the linear part \(L_0X=(r,q,p)\).  Exact expansion gives zero
homogeneous determinant coefficients in degrees eight, seven, and six, but
degree five is
\[
-2q(p^2+2q^2)(3p^2+4q^2)\ne0.
\]
This is not a Keller map.  It proves that no exclusion based only on the
three highest coefficients is valid beyond the exact membership and
curvature tests above.
