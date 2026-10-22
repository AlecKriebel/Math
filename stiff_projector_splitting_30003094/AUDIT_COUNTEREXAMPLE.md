# Independent audit of direct stiff projector splitting

Problem 30003094, queue row 1829. Audit date: 20 October 2026.

## Verdict and acceptance boundary

**Accept the exact-subflow counterexamples and the explicitly conditional affine subclass results described below. Do not classify the broad original PDE question as solved.**

The right-affine projection identity, the Lie and standard symmetric Strang error limits \(1/\sqrt2\) and (1), and the two-sided endpoint limit 

\[
\begin{pmatrix}3/8&0\\1/8&0\end{pmatrix}
\]

survive independent algebraic derivation. The examples disprove a specified, unrestricted stiffness-uniform robust estimate for the original direct K–S–L method. They do not disprove all PDE-compatible estimates, do not contradict the published bounded-ODE theorem, and do not contradict the 2019 theorem for a different algorithm. The smooth-target example permits small but spatially rough initialization errors; it is not an exact-projection initialization counterexample.

The positive local and global estimates for \(F(Y)=AY+C\) are valid under the numerical-stage defect and subspace-regularity hypotheses stated below. Those hypotheses are substantive, not consequences of smoothness of the exact solution. None of the audited estimates requires an explicit inverse retained singular value, but rank-preserving QR steps and uniform stage bounds must still be verified in an application.

This audit evaluates authored mathematical arguments, not literature priority or the correctness of every later paper cited in the source review. Executable checks provide corroboration only. No publication or queue change is part of this audit.

## 1  Method and the sources actually checked

All unqualified norms below are Frobenius norms; 

\[
P(Y)Z=ZVV^T-UU^TZVV^T+UU^TZ,
\qquad Y=USV^T
\]

is the orthogonal tangent projector for rank \(r\). The direct method solves, exactly and in this order,

\[
K'=F(KV_0^T)V_0,\qquad
S'=-U_1^TF(U_1SV_0^T)V_0,\qquad
(L^T)'=U_1^TF(U_1L^T),
\]

where \(K(\tau)=U_1\widehat S\), \(S(0)=\widehat S\), and \(L(0)=V_0S(\tau)^T\). The returned matrix is \(U_1L(\tau)^T\). In particular, the S subflow has the negative sign. It cannot be omitted or approximated by a stable forward flow when verifying these claims.

The inspected primary statements were:

- Kieri–Lubich–Walach, *Discretized dynamical low-rank approximation in the presence of small singular values*, SIAM J. Numer. Anal. 54 (2016), §§2.2–2.4 and Theorem 2.1. The theorem assumes boundedness and Lipschitz control of the full vector field and gives a first-order robust estimate for both Lie and Strang. Its constants may therefore grow with stiffness in the examples here. [Published article](https://doi.org/10.1137/15M1026791), [institutional published text](https://www.diva-portal.org/smash/get/diva2%3A874116/FULLTEXT01.pdf).
- Kieri's report in *Geometric Numerical Integration*, Oberwolfach Reports 13 (2016), printed pp. 910–912. The last paragraph asks for a PDE extension without specifying a PDE class, spatial method, regularity class, or complete universal estimate. The K equation in the short report lacks a terminal \(V_0\); the dimensionally correct form above agrees with the longer paper. [EMS record](https://ems.press/journals/owr/articles/14226), [report PDF](https://ems.press/content/serial-article-files/46621).
- Ostermann–Piazzola–Walach, *Convergence of a low-rank Lie–Trotter splitting for stiff matrix differential equations*, SIAM J. Numer. Anal. 57 (2019), §§3.2, 4 and Theorem 1. The method is 
  \(\Phi^A_\tau\circ\widetilde\Phi^G_\tau\), with projector splitting applied only to \(G\), not to \(AY+YA^T+G(Y)\). The stated hypotheses require existence of the full solution and the exact projected rank-\(r\) solution on the interval, analytic-semigroup estimates, \(C^1\) nonstiff \(G\), and a small normal remainder along the rank-\(r\) solution. They do not impose a uniform initial graph norm. [Published article](https://doi.org/10.1137/18M1177901), [primary arXiv version](https://arxiv.org/html/1803.10473v2).

These distinctions are necessary for the conclusions, not merely bibliographic qualifications.

## 2  The right affine identity

For \(F(Y)=YB+C\), set \(B_0=V_0^TBV_0\), \(D=U_1^TCV_0\), and \(P_1=U_1U_1^T\). No symmetry or dissipativity of \(B\) is needed for the identity.

The K equation is \(K'=KB_0+CV_0\). With \(U_1\) fixed at the endpoint, \(Q(t)=U_1^TK(t)\) solves \(Q'=QB_0+D\) and satisfies \(Q(\tau)=\widehat S\). The S equation is its autonomous inverse flow, so

\[
\widetilde S=Q(0)=U_1^TU_0S_0.
\]

This equality is exact even if the separate inverse flow has very large coefficients. The L equation is \((L^T)'=L^TB+U_1^TC\). Therefore

\[
Y_1=P_1\left(Y_0e^{\tau B}+\int_0^\tau Ce^{sB}\,ds\right).
\]

This proves the manuscript's Lemma 1. If \(B+B^T\le0\), then 

\[
\|Y_1\|\le\|Y_0\|+\tau\|C\|.
\]

An inaccurate output in this family is not evidence of a growing output norm or numerical roundoff. The K step may select an inappropriate column subspace even though the exact full flow and complete numerical step obey norm bounds.

## 3  The first order one obstruction

Let \(B=\operatorname{diag}(0,-\lambda)\), \(C=\eta e_2e_1^T\), \(v=(1,1)^T/\sqrt2\), and \(Y_0=e_1v^T\). Direct integration gives

\[
X(\tau)=\begin{pmatrix}1/\sqrt2&e^{-\lambda\tau}/\sqrt2\\\eta\tau&0\end{pmatrix},
\quad
k=e^{-\lambda\tau/2}e_1+
\frac{\sqrt2\eta}{\lambda}(1-e^{-\lambda\tau/2})e_2.
\]

Both K components are positive for finite positive parameters. Thus the K factor has rank one and the normalized direction \(u=k/\|k\|\) is unambiguous up to an irrelevant simultaneous sign. The identity above gives \(Y_1=uu^TX(\tau)\).

For \(\lambda=n^2\), \(\tau=\eta=1/n\), the ratio of the first K component to the second is

\[
\frac{n^3e^{-n/2}}{\sqrt2(1-e^{-n/2})}\longrightarrow0.
\]

Hence \(u\to e_2\), \(X(\tau)\to e_1e_1^T/\sqrt2\), \(Y_1\to0\), and

\[
\|Y_1-X(\tau)\|\longrightarrow1/\sqrt2.
\]

For every finite parameter the first column of \(uu^TX(\tau)\) is nonzero, because its scalar coefficient \(u_1/\sqrt2+u_2\eta\tau\) is positive. The example therefore avoids both ambiguous K QR and zero final rank.

The linear vector field (YB) is tangent to the rank-\(r\) manifold. For rank one,

\[
(I-P(Y))C=(I-uu^T)C(I-vv^T),\qquad
\|(I-P(Y))C\|\le\eta.
\]

The right-multiplication semigroup is contractive. Its generator smoothing bound is uniform because 

\[
\lambda e^{-\lambda t}\le\frac1{et}.
\]

The forcing has norm \(\eta\) and zero state derivative. At the first grid point, \(\delta=0\), \(\varepsilon=\eta\to0\), and both \(\tau\) and \(\tau(1+|\log\tau|)\) tend to zero. Consequently no estimate with either of those temporal terms and constants and a step threshold controlled only by these uniform quantities, bounded initial norm and fixed final time can hold for the direct method.

The quantifiers matter. This does not exclude an estimate whose constants depend on initial graph norms or additional numerical-subspace regularity. The initial high-frequency amplitude here does not vanish as the spatial frequency increases.

## 4  A fixed smooth target with small rough initialization error

Take \(\alpha=n^{-1/4}\), \(c=\sqrt{1-\alpha^2}\), \(v=(c,\alpha)^T\), \(\lambda=n^2\), \(\tau=\eta=1/n\), and numerical initial value \(Y_0=e_1v^T\). The comparison target starts at the fixed \(X_0=e_1e_1^T\), so

\[
\delta=\sqrt{2-2c}\to0,
\qquad X(t)=(e_1+\eta t e_2)e_1^T.
\]

The K endpoint is

\[
k=e^{-\sqrt n}e_1+c n^{-5/2}(1-e^{-\sqrt n})e_2.
\]

Again its normalized direction tends to \(e_2\). The full flow from the numerical initial value is

\[
\widehat X(\tau)=
\begin{pmatrix}c&\alpha e^{-n}\\n^{-2}&0\end{pmatrix}
\longrightarrow e_1e_1^T.
\]

Thus \(Y_1=uu^T\widehat X(\tau)\to0\), whereas \(X(\tau)\to e_1e_1^T\). The claimed limit 

\[
\|Y_1-X(\tau)\|\to1
\]

is correct. It is compatible with contractivity of the full affine flow, since 

\[
\|\widehat X(t)-X(t)\|\le\delta;
\]

the defect is created by the numerical subspace selection, not amplified by the exact equation.

The alternative sequence \(\alpha=1/n\), \(\lambda=n^4\), \(\tau=\eta=1/n\) is also valid: 

\[
k=e^{-n}e_1+c n^{-3}(1-e^{-n})e_2,
\quad
\widehat X(\tau)=
\begin{pmatrix}c&n^{-1}e^{-n^3}\\n^{-2}&0\end{pmatrix}.
\]

It yields the same error limit with \(\delta\sim1/n\). For a heat-equation embedding, this alternative uses active frequency \(N=n^2\), not \(N=n\).

The exact target is smooth and rank one, but the numerical initializers are not its exact Galerkin projections. In the first sequence \(\|Y_0B\|=\lambda\alpha=n^{7/4}\); in the alternative it is \(n^3\). Both diverge. A theorem excluding rough initialization errors is not contradicted.

### Exact projected solution exists and stays away from rank loss

For completeness, this obstruction is not explained by the nonexistence of a rank-one dynamical approximation. Write that approximation as \(Y=suv^T\), initially \(s=1\), \(u=e_1\), \(v=(c,\alpha)^T\), with nonnegative unit-vector factors. In orthogonal gauges the equations are

\[
u'=\frac{\eta v_1}{s}(e_2-u_2u),\quad
v'=(I-vv^T)\left(Bv+\frac{\eta u_2}{s}e_1\right),\quad
s'=-\lambda s v_2^2+\eta u_2v_1.
\]

The nonnegative quadrant is invariant: \(u_2'=\eta v_1u_1^2/s\ge0\), \(u_1'=-\eta v_1u_1u_2/s\), 

\[
v_1'=\lambda v_1v_2^2+\eta u_2v_2^2/s\ge0,
\quad
v_2'=-\lambda v_1^2v_2-\eta u_2v_1v_2/s.
\]

Substitution yields

\[
Y_{11}'=(su_1v_1)'=\eta u_1u_2v_2^2\ge0.
\]

Therefore \(s=\|Y\|\ge Y_{11}\ge c>0\). Also \(s'\le\eta\), giving \(s\le1+\eta t\). For each finite \(\lambda\), these bounds continue the smooth factor ODE through any fixed finite interval. If \(\widehat X\) is the full solution from the same initial value, variation of constants gives

\[
\widehat X(t)-Y(t)=\int_0^t
 (I-P(Y(s)))C\,e^{(t-s)B}\,ds,
\quad
\|\widehat X(t)-Y(t)\|\le\eta t.
\]

Thus the numerical error is also order one relative to a well-defined exact rank-one projected solution, while the modeling error is small. Against the fixed smooth target in this section the projected-solution error is at most \(\delta+\eta t\).

## 5  The same obstruction for standard symmetric Strang

This section concerns the standard autonomous composition

\[
\mathcal S_\tau=\Psi_{\tau/2}^{*}\circ\Psi_{\tau/2},
\]

where \(\Psi\) is KSL and its adjoint \(\Psi^*\) is LSK. The consecutive L half-subflows merge into one L subflow of length \(\tau\); this is the K–S–L–S–K version of projector Strang splitting. QR changes are orthogonal changes of factor coordinates and do not change any represented matrix. At the joining point the fixed column basis is the same for both L half-flows, so the merging is valid.

For \(F(Y)=YB+C\), \(B+B^T\le0\), apply the left-affine identity in Section 8 to the transposed equation. If the input is \(Y=USV^T\), the first L step is

\[
L_h=e^{hB^T}VS^T+\int_0^h e^{sB^T}C^TU\,ds
   =V_1\widehat S^T.
\]

With \(b_1=V_1^TBV_1\), the exact adjoint endpoint is

\[
\Psi_h^*(Y)=U L_h^T
 +(I-UU^T)CV_1\left(\int_0^h e^{sb_1}\,ds\right)V_1^T.
\]

The exact full endpoint is

\[
\Phi_h(Y)=U L_h^T+
 \int_0^h(I-UU^T)Ce^{sB}\,ds.
\]

Each of the two residual forcing terms has Frobenius norm at most \(h\|C\|\), since \(B\) and its compression \(b_1\) are dissipative. Therefore

\[
\|\Psi_h^*(Y)-\Phi_h(Y)\|\le2h\|C\|,
\qquad
\|\Psi_h^*(Y)\|\le\|Y\|+3h\|C\|.
\]

This bound is deliberately only \(O(h\|C\|)\); no higher-order local accuracy is claimed.

Set \(h=\tau/2\) and use either one-sided family from Sections 3–4. The K endpoint exponent is merely halved, so its normalized direction still tends to \(e_2\), and the first-half matrix \(Z=\Psi_h(Y_0)\) still tends to zero. The displayed norm bound implies

\[
\|\mathcal S_\tau(Y_0)\|
\le\|Z\|+3h\eta\longrightarrow0.
\]

The full exact target at time \(\tau\) tends to \(e_1e_1^T/\sqrt2\) in Section 3, and to \(e_1e_1^T\) in Section 4. The Strang errors therefore tend to \(1/\sqrt2\) and \(1\), respectively, under the same norm-only uniform bounds. This does not claim second-order robust convergence or use a putative second-order estimate; it rules out even the stated unrestricted uniform first-order estimates for this symmetric method.

Here is a rank check for the composition, including the S interval. Write the first-half rank-one output as \(Z=u r^T\), taking \(u\) positive. Then

\[
r_1=u_1c+u_2\eta h>0,\qquad
r_2=u_1\alpha e^{-\lambda h}>0,
\]

with \(c=\alpha=1/\sqrt2\) in Section 3. In each diagonal family, \(r_1/(\eta h)\to1\), whereas \(r_2\) is exponentially smaller. The first adjoint L endpoint is

\[
L_h=(r_1+\eta h u_2,\ r_2e^{-\lambda h})^T,
\]

so \(L_h/(\eta h)\to(2,0)^T\), its norm \(\widehat s>0\), and its normalized direction \(\bar v\to e_1\). More precisely, \(\lambda h\bar v_2^2\to0\). The following negative S equation is

\[
S'=\lambda\bar v_2^2S-\eta u_2\bar v_1,\qquad S(0)=\widehat s.
\]

Its explicit solution gives, uniformly for \(0\le t\le h\),

\[
\frac{S(t)}{\eta h}=2-\frac th+o(1).
\]

Consequently S remains positive for all sufficiently large members of the sequences. The final K equation starts with positive entries and has diagonal scalar damping and nonnegative forcing, so it remains nonzero. An independent endpoint check follows from the adjoint formula: the final column factor has component along \(u\) equal to \(\widehat s>0\), because the correction is orthogonal to \(u\). Thus the composition is not exploiting undefined QR choices or a hidden zero-rank endpoint.

In fact the manuscript's stronger positivity assertion for every finite \(n\ge2\) is valid. Put \(\beta=\lambda\bar v_2^2\) and \(d=\eta u_2\bar v_1\). The exact S solution is
\[
S(t)=e^{\beta t}\left[\widehat s-d\int_0^t e^{-\beta z}\,dz\right].
\]
Since \(\widehat s\ge r_1+\eta h u_2\), \(d\le\eta u_2\), and the integral is at most \(h\), the bracket is at least \(r_1>0\). During the first KSL half, its S trajectory is \(u^TK(h-t)>0\). Thus both S intervals, both QR endpoints and the final matrix maintain rank one without an asymptotic restriction.

## 6  The two sided parabolic example

Set \(A=B=\operatorname{diag}(0,-\lambda)\), \(C=\eta I_2\), \(Y_0=vv^T\), \(v=(1,1)^T/\sqrt2\), and \(E=e^{-\lambda\tau/2}\). The K equation is \(k'=(A-\lambda I/2)k+\eta v\), so

\[
k_1=\frac{E+2\eta(1-E)/\lambda}{\sqrt2},
\qquad
k_2=\frac{E^3+2\eta(1-E^3)/(3\lambda)}{\sqrt2}.
\]

Let \(u=k/\|k\|\), \(a=-\lambda u_2^2\), \(b=-\lambda/2\), \(q=a+b<0\), \(d=\eta(u_1+u_2)/\sqrt2\), and \(\widehat s=\|k\|\). Exact integration of S gives

\[
\widetilde s=e^{-q\tau}(\widehat s+d/q)-d/q.
\]

Since \(q\widehat s+d=u^Tk'(\tau)\), the exact L endpoint can be written without subtracting the enormous separate S terms:

\[
L(\tau)=e^{\tau(A-bI)}v\frac{u^Tk'(\tau)}q
-e^{\tau(A+aI)}v\frac dq
+\eta\int_0^\tau e^{s(A+aI)}u\,ds.
\]

This identity, not a floating-point S computation, controls the limit. We have

\[
k'(\tau)=\frac1{\sqrt2}
\begin{pmatrix}(-\lambda/2+\eta)E\\(-3\lambda/2+\eta)E^3\end{pmatrix}.
\]

For either fixed positive \(\tau,\eta\) and \(\lambda\to\infty\), or the diagonal sequence \(\lambda=n^2,\tau=\eta=1/n\),

\[
u\to(3,1)^T/\sqrt{10},\quad a/\lambda\to-1/10,
\quad q/\lambda\to-3/5.
\]

The first component of the first L term tends to \(5u_1/12\); its second component tends to zero. The second L term has norm \(O(\eta/\lambda)\), and the integral term is also \(O(\eta/\lambda)\), since \(u_2^2\) is eventually bounded away from zero. Therefore

\[
Y_1=uL(\tau)^T\longrightarrow
\begin{pmatrix}3/8&0\\1/8&0\end{pmatrix}.
\]

The exact full solution is

\[
X(\tau)=\begin{pmatrix}
1/2+\eta\tau&e^{-\lambda\tau}/2\\
e^{-\lambda\tau}/2&e^{-2\lambda\tau}/2+
\eta(1-e^{-2\lambda\tau})/(2\lambda)
\end{pmatrix}.
\]

For fixed positive \(\tau,\eta\), the error limit is 

\[
\sqrt{(1/8+\eta\tau)^2+(1/8)^2}\ge1/(4\sqrt2).
\]

For the diagonal sequence it tends to exactly \(1/(4\sqrt2)\). The limiting nonzero numerical singular value is \(\sqrt{10}/8\), so the example does not require a small initial or final nonzero singular value. The K factor does become small.

For the counterexample tail, all factors stay away from exact rank loss throughout their subflows. Indeed, when λ>2η, both components of k′(τ) are negative, so ŝ+d/q=(uᵀk′(τ))/q>0. Hence S\(t\)=exp(−qt)\(ŝ+d/q\)−d/q is positive for the entire S interval. Positive S output, forcing and diagonal L semigroup then make the L factor positive. This verifies the required ranks for all sufficiently large parameters in either limit; no assertion about every arbitrary triple of positive parameters is needed.

### The 2019 assumptions and the different algorithm

For the two-sided semigroup, the entrywise generator eigenvalues are \(0,-\lambda,-\lambda,-2\lambda\). Its operator norm is at most one and its differentiated semigroup norm is at most (1/(et)). Thus \(\omega=0\) and \(C_s=1/e\) work uniformly.

The forcing \(G(Y)=\eta I_2\) is \(C^1\), has Lipschitz constant zero and norm \(\sqrt2\eta\). For any rank-one \(2\times2\) matrix,

\[
\|(I-uu^T)\eta I_2(I-vv^T)\|\le\eta.
\]

The exact projected solution is symmetric and has the explicit representation

\[
r(t)=\|e^{tA}v\|^2=(1+e^{-2\lambda t})/2,
\quad u(t)=e^{tA}v/\sqrt{r(t)},
\quad
s(t)=r(t)\left(1+\eta\int_0^t r(z)^{-1}\,dz\right),
\quad Y(t)=s(t)u(t)u(t)^T.
\]

Differentiation gives \(u'=(I-uu^T)Au\), \(s'=2(u^TAu)s+\eta\), exactly the projected equation. Since \(s(t)\ge r(t)\ge1/2\), rank-one existence holds on every finite interval. The full linear affine equation also has global existence. Thus all the stated 2019 hypotheses are met with uniform bounds and initial error zero.

The 2019 algorithm, however, first applies projector splitting to the constant \(G\) field and then the full linear semigroup. Starting from \(vv^T\), the \(G\) step is \((1+\eta\tau)vv^T\), in either projector-splitting order, because the column and row direction stays \(v\). Its full output is

\[
(1+\eta\tau)e^{\tau A}vv^Te^{\tau A}.
\]

Its slow-entry error against the full solution is \(\eta\tau/2\), not order one. There is no contradiction with the published theorem. The valid conclusion is that its hypotheses cannot be transferred unchanged to the original direct full-field KSL algorithm.

## 7  The PDE norm and the family being varied

On the periodic torus take the orthonormal real modes \(f_0=1/\sqrt{2\pi}\), \(f_N=\cos(Ny)/\sqrt\pi\). Tensor products of orthonormal bases identify the coefficient Frobenius norm exactly with function \(L^2\). This is a Galerkin norm identity, not an unweighted sampled-grid approximation.

The right-sided examples are invariant active blocks of

\[
\partial_t z=\partial_y^2z+\eta g_1(x)f_0(y),
\]

with fixed smooth orthonormal left modes \(g_0,g_1\) and a y Fourier cutoff containing \(f_N\). The coefficient operator on the active right modes is \(\operatorname{diag}(0,-N^2)\). Exact flow and all three subflows preserve the active block. Choosing cutoff \(N=n\) realizes the first two sequences; the alternative in Section 4 uses \(N=n^2\).

This PDE is parabolic in y but has no x diffusion. The manuscript correctly treats the separate two-sided example as the fully two-sided heat case; one should not silently describe the right-sided PDE as uniformly elliptic in both variables.

In the fixed-target example, the exact target is \([g_0+\eta t g_1]f_0\), with zero spatial truncation error once the fixed left modes are included. It is uniformly smooth, but the numerical initialization contains a varying high mode. The forcing shape is fixed, with a varying amplitude \(\eta_n\). These are families of problems and approximations with uniform stated bounds, not one fixed forcing amplitude at all n.

For the two-sided case, the equation is \(\partial_t z=(\partial_x^2+\partial_y^2)z+\eta(f_0\otimes f_0+f_N\otimes f_N)\), with initial data \((f_0+f_N)\otimes(f_0+f_N)/2\). Both data and forcing shape vary in their high-frequency component. Their \(L^2\) norms are uniformly bounded, but not their spatial derivatives.

There is a small dimension distinction in using the normal-defect bound after embedding. The bound \(\eta\) holds for arbitrary rank-one matrices in the active \(2\times2\) block and along the actual active-block projected trajectory. For arbitrary rank-one matrices in the larger Galerkin space, \(\sqrt2\eta\) is a safe global bound because the embedded forcing has Frobenius norm \(\sqrt2\eta\). Either bound tends to zero and suffices; the sharper global \(2\times2\) assertion should not be asserted for all larger-space rank-one matrices without this qualification.

## 8  Conditional positive results

### Homogeneous separable exactness

For \(F(Y)=AY+YB\), KSL is exact for arbitrary constant square (A,B), not merely dissipative ones. Indeed,

\[
K(\tau)=e^{\tau A}U_0S_0e^{\tau B_0}=U_1\widehat S,
\quad B_0=V_0^TBV_0,
\quad a_1=U_1^TAU_1.
\]

The middle equation gives \(\widetilde S=e^{-\tau a_1}\widehat S e^{-\tau B_0}\), and the last gives

\[
Y_1=U_1e^{\tau a_1}\widetilde S V_0^Te^{\tau B}
=e^{\tau A}Y_0e^{\tau B}.
\]

The needed ranks are preserved because the matrix exponentials are invertible. This exactness does not imply affine exactness, as the counterexamples demonstrate.

### Left affine endpoint and local error

The invariant-column exactness statement in SUBCLASS_BOUNDS.md, Proposition 2, is also correct. If a fixed rank-\(r\) space \(W\) is \(A\)-invariant and contains all forcing columns, the K endpoint basis spans \(W\) whenever it has rank \(r\). Its fixed-basis coordinate \(U_1^TK(t)\) solves the same autonomous affine equation whose inverse is the S subflow. The final L equation then is the full affine equation in \(W\). This establishes exactness under the stated rank condition; the forcing cannot leave the chosen column space.

Suppose \(F(Y)=AY+C\), \(A+A^T\le0\), and \(C\) is constant. Write \(\varphi_h(A)=\int_0^h e^{sA}\,ds\), \(Q_0=I-V_0V_0^T\), and \(a_1=U_1^TAU_1\). Assuming the K endpoint has full rank,

\[
K_h=e^{hA}U_0S_0+\varphi_h(A)CV_0,
\quad
Y_1=K_hV_0^T+U_1\varphi_h(a_1)U_1^TCQ_0.
\]

To verify the endpoint, the S equation is \(S'=-a_1S-U_1^TCV_0\). The L equation is \((L^T)'=a_1L^T+U_1^TC\). Inserting the exact S endpoint into the exact L solution cancels the first integral in the \(V_0\) component and leaves precisely the displayed \(Q_0\) contribution.

The full exact endpoint is \(K_hV_0^T+\varphi_h(A)CQ_0\). Set \(P_1=U_1U_1^T\), 

\[
\varepsilon_1=\|(I-P_1)CQ_0\|,
\quad \gamma_1=\|(I-P_1)AU_1\|_2,
\quad M_0=\|CQ_0\|.
\]

Dissipativity implies contractivity of \(e^{sA}\) and \(e^{sa_1}\). The exact identity

\[
e^{sA}U_1-U_1e^{sa_1}
=\int_0^s e^{(s-t)A}(I-P_1)AU_1e^{ta_1}\,dt
\]

gives an operator-norm bound \(s\gamma_1\). Splitting \(CQ_0\) into its \(P_1\) and \(I-P_1\) parts therefore proves

\[
\|\Phi_h(Y_0)-Y_1\|
\le h\varepsilon_1+\frac{h^2}2\gamma_1M_0.
\]

This estimate is correct in the sharper \(M_0=\|CQ_0\|\) form, and hence also with \(\|C\|\) in place of \(M_0\). The displayed residual is the normal component of \(C\) at the mixed-stage matrix \(U_1SV_0^T\), not automatically the normal defect at the exact projected solution.

### Global propagation

The exact affine flow is contractive in its initial value. If each numerical step has the stage quantities above, direct comparison with the exact flow from that numerical input gives

\[
\|X(t_j)-Y_j\|\le\delta+
\sum_{i<j}h_i\varepsilon_i+
\frac12\sum_{i<j}h_i^2\gamma_iM_i.
\]

Thus, when \(\varepsilon_i\le\varepsilon\), \(\gamma_i\le\Gamma\), \(M_i\le M\), and \(h_i\le h_{\max}\),

\[
\|X(t_j)-Y_j\|\le\delta+T\varepsilon+\tfrac12T h_{\max}\Gamma M.
\]

No Lipschitz stability of the numerical map is used. The estimates contain no explicit inverse singular value or \(\|A\|\), but \(\Gamma\) is a numerical-subspace regularity hypothesis that can itself fail uniformly with increasing stiffness. Removing that hypothesis has not been proved here.

### PDE corollary acceptance conditions

For a periodic Fourier-Galerkin discretization of \(\partial_t z=\partial_x^2z+f(x,y)\) with time-independent \(f\), the matrix equation has the left-affine form. Orthonormal coefficients identify Frobenius and \(L^2\) norms; orthogonal spatial projection commutes with the heat semigroup. If \(z_0,f\in H^p\), the exact spatial error is bounded by \((1+(N+1)^2)^{-p/2}(\|z_0\|_{H^p}+T\|f\|_{H^p})\), for a tensor cutoff retaining all frequencies with both component magnitudes at most \(N\). Adding the conditional temporal bound is valid.

The condition \(\|A_NU_{i+1,N}\|_2\le\Gamma\) is sufficient for the required commutator leakage bound and corresponds to uniform second-x-derivative control of all normalized vectors in each numerical column subspace. Smoothness of the exact target and forcing alone does not establish it. The corollary is therefore conditional, and applies to diffusion in x only unless a separate argument treats the y diffusion. It is not a theorem for a general two-sided nonlinear parabolic equation.


The final right-affine graph-norm estimate in SUBCLASS_BOUNDS.md,
\(\|\Phi_h(Y)-\Psi_h(Y)\|\le h(\|YB\|+2\|C\|)\),
is valid as stated. It follows by bounding the displacement of K from its initial factor, using \((US)(V^TBV)=YBV\), and then projecting the full right-affine flow. Its order is only \(h\), not \(h^2\); the manuscript correctly declines to infer a vanishing global error by summing it.

## 9  Computational checks and remaining scope

The independent literal-subflow script `audit_exact_subflows.py` integrates each finite-dimensional affine K, negative S and L system using an augmented matrix exponential with arbitrary precision. A fresh rerun reproduced the saved results: the one-sided error at \(n=300\) is about (0.7071067811865475); the two-sided error there is about (0.1767844081603991), approaching \(1/(4\sqrt2)\); and the rough-initialization example at \(n=10000\) has error numerically indistinguishable from (1) at the printed precision. These values support the exact limits but are not their proof.

The analytic calculations above also validate what the seeded rank-two regression tests are checking: homogeneous exactness, right-affine projection, left-affine endpoint, and the left-affine local bound. Those tests cannot establish a general theorem or extrapolate to inexact subflows.

A fresh rerun of all 24 rank-two regression cases passed; the largest endpoint-identity discrepancy was \(5.5868\times10^{-16}\). The six-subflow Strang checker was inspected and rerun for \(n=10,30,100,300\). Its identity, coarse error bound, positive S endpoints and nonzero QR checks passed. At \(n=100\) its error was \(0.9999999999999999999903558\); at \(n=300\) the printed error was \(1\). The clean sequence's large full damping rate is not mistaken for a proof: the exact identities and rank arguments above establish the result.

Acceptance does not extend to second-order robust Strang convergence, arbitrary spatial discretizations or norms, arbitrary hyperbolic PDEs, nonlinear parabolic equations, tensor formats, adaptive ranks, or finite-precision robustness of very ill-conditioned inverse S subflows. Nor does it establish a counterexample with fixed smooth data and exact projected initialization. The appropriate overall outcome remains **partial progress on the original unresolved problem**.

## Audited manuscript versions

The acceptance applies to the following SHA-256 versions. The five-avenue summary is consistent with the proven results and counts distinct mathematical avenues, not independent historical sessions.

- RESEARCH_REPORT.md: 97ba989523bd45fc9e439a100b6289d248a1adba172b8c7e5880d95aed372454
- SUBCLASS_BOUNDS.md: a42041d73eb082b3959b44a5ee34efc7796e430e97441735a81e2c5ed467604c
- STRANG_OBSTRUCTION.md: c03d292ecffbdbf473f07c9c7399aec7a294f4a8c631faedd1601376c0ff79f9
- FIVE_AVENUE_SUMMARY.md: c6480cd80e0337892a278d999ba854163eaa839d9f3d7ee9d03ca306e8dab2dc
