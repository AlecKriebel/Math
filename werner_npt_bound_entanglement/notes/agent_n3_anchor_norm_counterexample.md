# Exact failure of the rank-one anchor operator-norm bound

For three copies put
\[
 {\cal L}=L_1L_2L_3,\qquad
 L_i(X)=X-\frac12\operatorname{Tr}_i(X)\otimes I_i,
\]
and, for a unit vector \(w\),
\[
 A_w={\cal L}(|w\rangle\langle w|).
\]
The proposed sufficient estimate
\[
 \|A_w\|_\infty^2\leq \frac18Q_3(|w\rangle\langle w|)
 \tag{1}
\]
is false already on three local qubits.

Take
\[
 w=\frac{|000\rangle+|111\rangle}{\sqrt2}.
 \tag{2}
\]
Every nontrivial one- or two-party reduction of
\(P_w=|w\rangle\langle w|\) has Hilbert--Schmidt norm squared \(1/2\).
Consequently
\[
\begin{aligned}
 Q_3(P_w)
 &=1-\frac12\frac32+\frac14\frac32-\frac18\\
 &=\frac12.
\end{aligned}
\tag{3}
\]
Self-adjointness of \({\cal L}\) gives
\[
 \langle w,A_ww\rangle
 =\langle P_w,{\cal L}(P_w)\rangle
 =Q_3(P_w)=\frac12.
\tag{4}
\]
Thus
\[
 \|A_w\|_\infty^2\geq\frac14
 >\frac1{16}
 =\frac18Q_3(P_w).
\tag{5}
\]
In fact direct contraction gives
\[
 A_ww=\frac12w,\qquad
 A_ww_-=-\frac12w_-,
 \quad
 w_-=\frac{|000\rangle-|111\rangle}{\sqrt2},
\tag{6}
\]
and all other eigenvalues have absolute value at most \(1/8\), so
\(\|A_w\|_\infty=1/2\).  Hence (1) fails by the exact factor four.

This does **not** refute the intended anchored Gram inequality
\[
 |{\cal B}_3(P_w,|u\rangle\langle v|)|^2
 \leq Q_3(P_w)Q_3(|u\rangle\langle v|).
\tag{7}
\]
For example, taking \(u=v=w_-\) in (7) gives equality: the large
negative eigenvalue in (6) is accompanied by
\(Q_3(P_{w_-})=1/2\), rather than only the universal rank-one lower
bound \(1/8\).  Any proof of (7) must retain this correlation.

## Exact positive-map form of the surviving problem

The correlation can be isolated without any optimization.  For a unit
vector \(v\), define
\[
 K_v=\sum_{S\subseteq[3]}
 \left(-\frac12\right)^{|S|}
 \rho_S^v\otimes I_{\bar S},
 \qquad
 \rho_S^v=\operatorname{Tr}_{\bar S}P_v.
\tag{8}
\]
For every \(u\),
\[
 \langle u,K_vu\rangle
 =Q_3(|u\rangle\langle v|).
\tag{9}
\]
Indeed, the term indexed by \(S\) in (9) is
\[
 \left\|\operatorname{Tr}_S|u\rangle\langle v|\right\|_2^2
 =\operatorname{Tr}(\rho_S^u\rho_S^v).
\tag{10}
\]
If \(a=Q_3(P_w)\), self-adjointness of \({\cal L}\) also gives
\[
 {\cal B}_3(P_w,|u\rangle\langle v|)
 =\langle v,A_wu\rangle.
\tag{11}
\]
Consequently the anchored Gram inequality for a fixed pair \(w,v\)
is exactly the operator inequality
\[
 \boxed{\qquad
 aK_v-A_wP_vA_w\succeq0.
 \qquad}
\tag{12}
\]
Equivalently, if
\[
 {\cal K}(V)=\sum_{S\subseteq[3]}
 \left(-\frac12\right)^{|S|}
 \operatorname{Tr}_{\bar S}(V)\otimes I_{\bar S},
\tag{13}
\]
then the full anchored problem is positivity of
\[
 \Theta_w(V)=a{\cal K}(V)-A_wVA_w
\tag{14}
\]
on every \(V\succeq0\).  It suffices to test rank-one \(V=P_v\).

The universal replica bound only says \(K_v\succeq I/8\).  Replacing
\(K_v\) by this state-independent lower bound turns (12) into the
false estimate (1).  Thus (12), rather than an operator norm of
\(A_w\), is the smallest surviving domination statement: it retains
the necessary dependence on the second anchor \(v\).
