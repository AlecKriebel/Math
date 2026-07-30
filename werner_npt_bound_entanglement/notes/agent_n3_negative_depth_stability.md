# Exact negative-depth simplex and the forbidden \(1/5\) endpoint

## Status

This note combines the three exact two-pair face certificates with the
fixed-left Haar-kernel classification.  It gives a quantitative
structural theorem for every hypothetical negative direction of the
full three-pair Schur residual.

If
\[
 H_V=S_V-F_1-F_2-F_3
\]
is negative on \(z\), normalize its generalized depth by
\[
 \delta
 =-\frac{\langle z,H_Vz\rangle}{\langle z,S_Vz\rangle}.
\]
Then
\[
 \boxed{0<\delta<\frac15.}
\]
More precisely, the three normalized frame masses belong to the exact
simplex
\[
 \boxed{
 \frac{\langle z,F_i z\rangle}{\langle z,S_Vz\rangle}
 =2\delta+(1-5\delta)\theta_i,\qquad
 \theta_i>0,\qquad \sum_i\theta_i=1.
 }
\]
The rank-six and Haar slacks admit a second exact simplex coordinate
\(\lambda_i\in(0,1]\).  Consequently all six face slacks tend to zero,
and all three frame masses tend to \(2/5\), if
\(\delta\uparrow1/5\).

At \(\delta=1/5\) the local Haar forms are exactly the forbidden
isotropic forms classified in
`agent_n3_haar_block_kernel_reduction.md`.  Thus the abstract scalar
model \(S=1,F_i=2/5\) is not only nonphysical at equality: compactness
gives a strict physical gap below \(1/5\).  The gap can be expressed as
one finite semialgebraic stability constant \(\mu_*>0\).  In fact,
\[
 \Delta_*=\frac15-\frac25\mu_*,
\]
and the unrestricted three-copy theorem is exactly the sharp
evaluation \(\mu_*=1/2\).  This note does not prove that evaluation.

The dependency-free exact checker is
`verification/verify_n3_negative_depth_stability.py`.

## 1. Intrinsic quantities

Fix an isometry
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}
\]
and its low-sector Schur operator \(S=S_V\).  Recall the uniform bounds
\[
 \frac5{12}I\preceq S\preceq I.
\]
Index the three pair frames by the complementary omitted site, and put
\[
 F_i=\frac12T_iT_i^\dagger,\qquad
 H=S-F_1-F_2-F_3.
\]
For a nonzero test vector \(z\), let \(C=C_z\) be the associated
rank-at-most-two transition matrix.  Define
\[
\begin{aligned}
 \sigma&=\langle z,Sz\rangle,\\
 h&=\langle z,Hz\rangle=2Q_3(C),\\
 f_i&=\langle z,F_i z\rangle.
\end{aligned}
\]
Thus
\[
 \sigma=h+\sum_i f_i.
\]

For the omitted site \(i\), retain the exact face slacks
\[
 r_i=\frac32w_i-t_i,\qquad s_i=3q_i-t_i,
\]
where \(w_i=f_i\), \(t_i=Q_2(\operatorname{Tr}_iC)\), and
\(q_i\) is the two-site energy retaining site \(i\).  The established
rank-six and block-Haar theorems give
\[
 r_i\geq0,\qquad s_i\geq0.
\]
Write
\[
 u_i=\frac13r_i+\frac23s_i.
\]
The sharp face identity is
\[
 \boxed{
 \langle z,(H+F_i)z\rangle
 =\frac12f_i+u_i.
 }
\tag{1}
\]

## 2. The Haar slack is exactly the strict local bracket

Let \(w_A=\|\Pi_A C\|_2^2\) be the scalar/traceless sector masses.
For \(\{i,j,k\}=\{1,2,3\}\), the sitewise Haar bracket from the
fixed-left analysis is
\[
 g_i=
 \frac14w_{\{i\}}
 -\frac12\left(w_{\{i,j\}}+w_{\{i,k\}}\right)
 +w_{\{1,2,3\}}.
\tag{2}
\]
The two-site energy and its traced version are
\[
\begin{aligned}
 q_i={}&
 \frac14(w_\varnothing+w_{\{i\}})
 -\frac12(w_{\{j\}}+w_{\{k\}}+
           w_{\{i,j\}}+w_{\{i,k\}})\\
 &+w_{\{j,k\}}+w_{\{1,2,3\}},\\
 t_i={}&3\left[
 \frac14w_\varnothing
 -\frac12(w_{\{j\}}+w_{\{k\}})
 +w_{\{j,k\}}\right].
\end{aligned}
\tag{3}
\]
Subtracting gives the exact identification
\[
 \boxed{s_i=3q_i-t_i=3g_i.}
\tag{4}
\]

The fixed-left kernel and factor-pencil classification proves that a
negative rank-two transition cannot have \(g_i=0\) at even one site.
Therefore
\[
 \boxed{Q_3(C)<0\quad\Longrightarrow\quad s_i>0
 \quad(i=1,2,3).}
\tag{5}
\]
This is the nonlinear physical input in the argument below.

## 3. Exact negative-depth simplex

Assume \(h<0\), and define
\[
 \delta=-\frac h\sigma>0.
\tag{6}
\]
Equation (1) becomes
\[
 -\delta\sigma+f_i=\frac12f_i+u_i,
\]
or
\[
 \boxed{\frac12f_i-\delta\sigma=u_i.}
\tag{7}
\]
Since
\[
 \sum_i f_i=\sigma-h=(1+\delta)\sigma,
\]
summing (7) gives
\[
 \boxed{
 \sum_i u_i=\frac12(1-5\delta)\sigma.
 }
\tag{8}
\]
Nonnegativity gives \(\delta\leq1/5\).  Equality would force every
\(u_i=0\), hence every \(s_i=0\), contradicting (5).  This proves
\[
 \boxed{0<\delta<\frac15.}
\tag{9}
\]

Because every \(s_i>0\), every \(u_i>0\).  Define
\[
 \theta_i=
 \frac{2u_i}{(1-5\delta)\sigma}.
\tag{10}
\]
Then
\[
 \theta_i>0,\qquad\sum_i\theta_i=1,
\]
and (7) is exactly
\[
 \boxed{
 \frac{f_i}{\sigma}
 =2\delta+(1-5\delta)\theta_i.
 }
\tag{11}
\]

There is a second intrinsic coordinate
\[
 \lambda_i=\frac{2s_i}{3u_i}.
\tag{12}
\]
Since \(u_i=r_i/3+2s_i/3\), one has
\[
 0<\lambda_i\leq1.
\]
Equations (10)--(12) give the complete scalar parametrization
\[
\boxed{
\begin{aligned}
 \frac{f_i}{\sigma}
 &=2\delta+(1-5\delta)\theta_i,\\
 \frac{r_i}{\sigma}
 &=\frac32(1-5\delta)\theta_i(1-\lambda_i),\\
 \frac{s_i}{\sigma}
 &=\frac34(1-5\delta)\theta_i\lambda_i,\\
 \frac{g_i}{\sigma}
 &=\frac14(1-5\delta)\theta_i\lambda_i.
\end{aligned}}
\tag{13}
\]
Conversely, every scalar tuple satisfying (13) satisfies all the
summed face identities.  Physical realizability imposes further
common-code constraints.

Several useful bounds are immediate:
\[
\boxed{
 2\delta<\frac{f_i}{\sigma}<1-3\delta,
 \qquad
 \left|\frac{f_i}{\sigma}-\frac25\right|
 <\frac35(1-5\delta),
}
\tag{14}
\]
and
\[
\boxed{
\begin{aligned}
 \sum_i r_i&\leq\frac32(1-5\delta)\sigma,\\
 \sum_i s_i&\leq\frac34(1-5\delta)\sigma,\\
 \sum_i g_i&\leq\frac14(1-5\delta)\sigma.
\end{aligned}}
\tag{15}
\]
Thus a sequence with \(\delta\uparrow1/5\) is forced toward the
simultaneous formal configuration
\[
 F_i\sim\frac25S,\qquad r_i,s_i,g_i\longrightarrow0
\quad(i=1,2,3).
\tag{16}
\]

In intrinsic coefficient-matrix language,
\[
 \sigma=2Q_3(C)+\sum_iw_i
       =2Q_3(C)+3\|\Pi_2C\|_2^2.
\tag{17}
\]
Hence (9) is equivalently the strict negative-case improvement
\[
 \boxed{
 Q_3(C)<0
 \quad\Longrightarrow\quad
 Q_3(C)>-\frac14\|\Pi_2C\|_2^2.
 }
\tag{18}
\]
The non-strict version was the previously summed two-face estimate.

## 4. Quantitative convergence to forbidden isotropy

Let \({\mathscr H}_i\) be the complete left local-filter form of
\(C\), and put \(q=Q_3(C)\).  The homogeneous form of the established
quantitative-isotropy theorem is
\[
 \left\|
 {\mathscr H}_i+\frac{2q}{3}{\cal L}
 \right\|_{\rm op}
 \leq360\sqrt{15}\,\sqrt{\|C\|_2^2g_i}.
\tag{19}
\]
For the normalized code purification used in the transition map,
\[
 \|z\|^2=2\|C_z\|_2^2.
\]
The bounds \(5I/12\preceq S\preceq I\) therefore give
\[
 \frac56\|C\|_2^2\leq\sigma\leq2\|C\|_2^2.
\tag{20}
\]
Combining (15), (19), and (20) yields the explicit near-isotropy
estimate
\[
\boxed{
 \frac1{\|C\|_2^2}
 \left\|
 {\mathscr H}_i+\frac{2q}{3}{\cal L}
 \right\|_{\rm op}
 \leq180\sqrt{30}\,\sqrt{1-5\delta}.
}
\tag{21}
\]

Likewise, let \(\beta_i\) be the complete \(9\times9\) two-copy block
Gram at site \(i\), and
\[
 \gamma=-\frac{2q}{3}>0.
\]
The quantitative block-collapse estimate gives
\[
\boxed{
 \frac1{\|C\|_2^2}
 \left\|
 \beta_i-\gamma
 |\operatorname{vec}I_3\rangle
 \langle\operatorname{vec}I_3|
 \right\|_2
 \leq2376\sqrt{30}\,\sqrt{1-5\delta}.
}
\tag{22}
\]
Thus the exact fixed-left kernel obstruction is approached at an
explicit square-root rate when the generalized negative depth
approaches \(1/5\).

## 5. The global face-sum gap

The exact face identity has an operator-level consequence.  Define
\[
 K_i(V)=H_V+\frac12F_i.
\tag{23a}
\]
For every \(z\),
\[
 \langle z,K_i(V)z\rangle=u_i(C_z)\geq0,
\]
so
\[
 K_i(V)\succeq0.
\tag{23b}
\]
Their sum is
\[
\boxed{
 K(V):=\sum_iK_i(V)
 =\frac12S_V+\frac52H_V.
}
\tag{23c}
\]

### Proposition 5.1

For every physical code plane \(V\),
\[
 \boxed{K(V)\succ0.}
\tag{23d}
\]

### Proof

If \(K(V)\) had a nonzero kernel vector \(z\), positivity of all three
summands in (23b) would give
\[
 K_i(V)z=0\qquad(i=1,2,3).
\]
Equation (23c) would then give
\[
 H_Vz=-\frac15S_Vz,
\]
so the associated transition \(C_z\) would have \(Q_3(C_z)<0\).
Moreover every \(u_i(C_z)=0\), hence every
\(s_i(C_z)=3g_i(C_z)=0\).  This contradicts the fixed-left
strictness theorem (5). \(\square\)

The Stiefel manifold of isometries \(V\) is compact, while
\(S_V\succeq5I/12\).  Hence the generalized face-sum gap
\[
\boxed{
 \mu_*=
 \min_{\substack{V^\dagger V=I_2\\z\ne0}}
 \frac{\langle z,K(V)z\rangle}
      {\langle z,S_Vz\rangle}
}
\tag{23e}
\]
is attained and satisfies
\[
 \boxed{\mu_*>0.}
\tag{23f}
\]
It is a real-algebraic optimization constant: after fixing
\(\langle z,S_Vz\rangle=1\) and splitting real and imaginary parts,
both the compact constraint set and the objective are polynomial over
\(\mathbb Q\).

Define the largest generalized violating depth, allowing zero, by
\[
 \Delta_*=
 \max_{\substack{V^\dagger V=I_2\\z\ne0}}
 \left(
 -\frac{\langle z,H_Vz\rangle}
       {\langle z,S_Vz\rangle}
 \right).
\tag{23g}
\]
Equation (23c) gives the exact affine relation
\[
\boxed{
 \mu_*=\frac12-\frac52\Delta_*,
 \qquad
 \Delta_*=\frac15-\frac25\mu_*.
}
\tag{23h}
\]
The known exact zero transitions have
\(\langle z,H_Vz\rangle=0\), so \(\Delta_*\geq0\) and
\(\mu_*\leq1/2\).  Consequently
\[
\boxed{
 0<\mu_*\leq\frac12,
 \qquad
 0\leq\Delta_*<\frac15.
}
\tag{23i}
\]
Most importantly, unrestricted three-copy positivity is exactly
\[
\boxed{
 Q_3(C)\geq0\text{ for every }\operatorname{rank}C\leq2
 \quad\Longleftrightarrow\quad
 \mu_*=\frac12.
}
\tag{23j}
\]
Thus the fixed-left classification proves strict positivity of the
global face-sum gap.  The remaining theorem is the sharp evaluation
of this one common-code constant, not merely its positivity.

## 6. Shellwise effective constants

The preceding endpoint exclusion can be made into one compact
semialgebraic constant.  Fix a rational
\[
 0<a<\frac15.
\]
Let \({\cal K}_a\) be the set of pairs \((V,z)\) satisfying
\[
\begin{aligned}
 V^\dagger V&=I_2,\\
 \langle z,S_Vz\rangle&=1,\\
 -\langle z,H_Vz\rangle&\geq a.
\end{aligned}
\tag{23}
\]
It is compact: the isometry manifold is compact and
\(S_V\succeq5I/12\) uniformly bounds \(z\).  If it is nonempty,
define
\[
 \eta(a)=
 \min_{(V,z)\in{\cal K}_a}\ \min_i g_i(C_z).
\tag{24}
\]
Every member has \(Q_3(C_z)<0\), and (5) gives
\[
 \boxed{\eta(a)>0.}
\tag{25}
\]
All constraints and objectives become real polynomials with rational
coefficients after splitting real and imaginary parts.  Hence
\(\eta(a)\) is a finite real-algebraic optimization constant and is,
in principle, certifiable by exact quantifier elimination or a
polynomial certificate.

For any physical negative direction of depth \(\delta\geq a\),
(15), with \(\sigma=1\), gives
\[
 3\eta(a)
 \leq\sum_i g_i
 \leq\frac14(1-5\delta).
\]
Therefore
\[
\boxed{
 \delta\leq\frac15-\frac{12}{5}\eta(a).
}
\tag{26}
\]
If \({\cal K}_a\) is empty, every negative depth is already \(<a\).
Writing \(\Delta_*\) for the supremum of all physical negative
depths, the nonempty case gives
\[
\boxed{
 \Delta_*
 \leq
 \max\left\{
 a,\ \frac15-\frac{12}{5}\eta(a)
 \right\}
 <\frac15.
}
\tag{27}
\]
In the empty case the corresponding conclusion is simply
\(\Delta_*\leq a<1/5\).

One may express the same reduction directly through anisotropy.
Define
\[
 D_i(C)=
 \left\|
 {\mathscr H}_i+\frac{2Q_3(C)}3{\cal L}
 \right\|_{\rm op}
\]
and, when \({\cal K}_a\ne\varnothing\),
\[
 \kappa(a)=
 \min_{(V,z)\in{\cal K}_a}\ \min_i
 \frac{D_i(C_z)^2}{\|C_z\|_2^2}.
\tag{28}
\]
The fixed-left classification excludes \(D_i=0\) at a negative
transition, so \(\kappa(a)>0\).  The homogeneous square of (19) gives
\[
 g_i\geq\frac{D_i(C)^2}
 {1\,944\,000\,\|C\|_2^2},
\]
and hence
\[
\boxed{
 \Delta_*
 \leq
 \max\left\{
 a,\ \frac15-\frac{\kappa(a)}{810\,000}
 \right\}
 <\frac15.
}
\tag{29}
\]
Equation (29) is again for the nonempty case; if
\({\cal K}_a=\varnothing\), use \(\Delta_*\leq a\).

Equations (24) or (28) isolate an exact remaining stability constant:
evaluating it is a finite nonlinear common-code problem, not another
linear sector inequality.  A proof of unrestricted positivity still
requires excluding every \(\delta>0\), not merely improving the
universal upper bound \(1/5\).
