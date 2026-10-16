# Independent adversarial audit: relative Kähler–Ricci positivity loss

Problem 30003571 / OWR-15582-005. Audit date: 2026-10-04 UTC.

## Verdict

**PASS for the stated mathematical claim.** The frozen construction is a counterexample to preservation of total-space positivity for the probability-normalized flow on \(\mathcal O_E(r)\) defined by Naumann's published equation (13). No mathematical defect was found in the global initial metric, the exact second-variation argument, or the negative value at the stated time. The necessary finite-time existence and smooth parameter dependence are explicitly supplied by the cited source theorem; they are not claimed to follow from symbolic tests.

The potentially decisive normalization objection was examined directly. Under the weight convention explicitly stated next to equation (13), the reaction coefficient is one. The printed equation (14), if read literally with the same weight and time conventions, fails even on an elementary stationary positive product metric. Thus this audit does not resolve the discrepancy merely by guessing that a symbol is a typographical error. Section 2 below gives an independent contradiction test and explains a possible root-metric/time change without attributing an undocumented intention to the author.

This verdict concerns the theorem as formulated in the frozen proof. It does not certify novelty, historical priority, the current literature status, a general answer about other relative-flow normalizations, or a result concerning the Griffiths conjecture itself. The source already constructs the relative flow; the nontrivial result audited here concerns total-space positivity.

## 1. Frozen object and primary-source scope

The target was verified before and after the audit:

- `FROZEN_MANIFEST.json`: SHA-256 `14e522b5bea40b8dc1c9a222d58048e4f667a4bc805df55dfb630d79b83a162c`.
- `PROOF.md`: SHA-256 `4deb64c3b249dcf26a87ccdd222bad837e61f107b5304ed0e3ad2c6f1e444b36`.
- All six file sizes and SHA-256 values listed by that manifest agree with the supplied files.
- The frozen files were not changed.

The complete Naumann contribution to the 2017 Oberwolfach report, printed pp. 2440–2443, was inspected. In the published article, the metric and geodesic-curvature definitions in Sections 1–2 and the complete flow construction, existence discussion, and positivity question in Sections 3.1–3.3 were inspected. PDF images of printed pp. 1519–1521 were also checked, so the crucial \(\mu_{\phi_t}\), \(r c(\phi_t)\), and explicit \(\mathcal O_E(r)\)-weight statements are not artifacts of text extraction.

Primary sources:

1. P. Naumann, *An approach to the Griffiths conjecture*, contribution to *Komplexe Analysis*, Oberwolfach Reports 14 (2017), pp. 2440–2443, [DOI 10.4171/OWR/2017/39](https://doi.org/10.4171/OWR/2017/39).
2. P. Naumann, *An approach to the Griffiths conjecture*, Mathematical Research Letters 28 (2021), no. 5, pp. 1505–1523, [DOI 10.4310/MRL.2021.v28.n5.a10](https://doi.org/10.4310/MRL.2021.v28.n5.a10).

The inspected publisher PDF digests are recorded in `AUDIT_MANIFEST.json`. No new online search was performed. In particular, the source gate's separate literature and repository-search assertions are not independently re-certified here.

### The actual initial-data requirement

The 2017 report first discusses metrics induced from a Hermitian metric on \(E\), then explicitly leaves that restricted setting and takes a general positive metric on \(\mathcal O_E(1)\). Its final question starts the flow at \(h^r\). The published Section 3.2 requires only fiberwise positive curvature; Section 3.3 starts with a positive metric \(h\) on \(\mathcal O_E(1)\), sets the initial metric on \(\mathcal O_E(r)\) equal to \(h^{\otimes r}\), and asks whether geodesic-curvature positivity persists.

There is no requirement that the initial metric already be fiberwise Fubini–Study or come from a metric on \(E\). Such a requirement would defeat the purpose of the proposed flow. The candidate's positive square root satisfies the actual requirement.

## 2. Defining equation, normalization, and the printed evolution equation

### 2.1 The scalar equation follows from the source's definitions

On a product trivialization, choose a nonvanishing holomorphic section of \(\det E\) and compatible local frames for the relative canonical bundle and \(L=\mathcal O_E(r)\). For fiber dimension one, let \(g=\phi_{z\bar z}\). The source's normalized density is

\[
\mu_\phi=\frac{e^{-\phi}dA_z}{I(s)},\qquad
I(s)=\int_{X_s}e^{-\phi}dA_z.
\]

This is exactly the specialization of the construction on printed pp. 1518–1519. The source says \(e^{-\phi}\) is the metric on \(\mathcal O_E(r)\), not its \(r\)-th root. Its Monge–Ampère measure is the curvature volume divided by the fixed fiber volume. Therefore its equation (13) reads

\[
\dot\phi=\log g+\phi+\log I+C.
\tag{A1}
\]

Here \(C\) is constant in the base and fiber variables. Curvature-form constants and the fixed total fiber volume change only \(C\). They cannot change the coefficient of \(\phi\).

A different holomorphic frame of \(\det E\) multiplies the unnormalized density and its integral by the same positive base factor. The normalized measure does not change. The second derivative of the logarithm of the modulus squared of a nonvanishing holomorphic frame change is zero. There is consequently no omitted base-curvature term in the calculation using the stated fixed frames.

Adding a time-independent function \(a(s)\) to \(\phi\) changes neither normalized measure. In (A1), its contribution to \(\phi\) cancels its contribution \(-a\) to \(\log I\). A freely chosen time-dependent base correction would change the defining flow and cannot be inserted to restore positivity.

### 2.2 An independent stationary-product contradiction test

Take the same compact bundle and the ordinary product weight

\[
\phi_{\mathrm{prod}}(s,z)=2\log(1+|s|^2)+2\log(1+|z|^2).
\]

It is a strictly positive metric on \(\mathcal O(2,2)\). On every fiber, both measures in equation (13) equal

\[
\frac{dA_z}{\pi(1+|z|^2)^2}.
\]

Thus equation (13) makes this metric stationary, with \(\partial_t c=0\). At \(s=0\), the geodesic curvature of this \(\mathcal O_E(2)\)-weight is \(c=2\); the horizontal lift has zero vertical component, its Kodaira–Spencer tensor vanishes, and the fiber Laplacian of \(c\) is zero. Moreover

\[
I(s)=\frac{\pi}{(1+|s|^2)^2},\qquad
(\log I)_{s\bar s}(0)=-2.
\]

The right side of the printed equation (14), read literally with \(r=2\) and these stated conventions, is therefore

\[
0+2\cdot2+0-2=2,
\]

whereas its left side is zero. This contradiction is independent of the proposed counterexample, Laplacian sign choices, and constant volume normalization. It proves that equation (14) cannot simultaneously have its displayed form and use the same weight/time conventions as equation (13).

### 2.3 Why the coefficient r can appear in another convention

This discrepancy need not be described as a particular typographical error. If \(\psi=\phi/r\) is the weight of the root metric and \(\tau=t/r\), then equation (A1) becomes, in dimension one,

\[
\partial_\tau\psi=\log\psi_{z\bar z}+r\psi+
\log\int e^{-r\psi}dA_z+C'.
\]

On a central fiber with vanishing first base derivatives, writing \(c=\psi_{s\bar s}\) gives

\[
\partial_\tau c=\Delta_\psi c+rc-r\int c\,\mu.
\]

This has the scaling displayed by equation (14). Both the metric and time variables have changed. With the original time \(t\), every term of this root-metric equation must instead be divided by \(r\).

The source does not announce that simultaneous change in Section 3.3; indeed it explicitly identifies \(e^{-\phi_t}\) as the metric on \(\mathcal O_E(r)\). Accordingly, the printed formula cannot override the defining equation. The frozen proof properly differentiates equation (13) directly. No general geodesic-curvature evolution theorem is needed. A positive time reparameterization and a positive scalar multiple of the curvature would also leave the property of losing positivity unchanged, although the reported time and coefficient would then have to be translated.

The report's unnormalized numerator differs from the published normalized numerator by a fixed fiber-volume factor. The solutions differ by a scalar function linear in time, which has no spatial curvature. This difference does not affect the counterexample.

## 3. Bundle, metric, and global strict positivity

### 3.1 Line bundle and charts

For \(E=A\otimes\mathbf C^2\), \(A=\mathcal O_{\mathbf P^1}(1)\), the projective bundle is the product and the convention \(f_*\mathcal O_E(1)=E\) gives

\[
\mathcal O_E(1)=A\boxtimes\mathcal O_{\mathbf P^1}(1),\qquad
L=\mathcal O_E(2)=\mathcal O(2,2).
\]

The relative anticanonical identification is consistent:
\(L\otimes f^*(\det E)^{-1}=\mathcal O(0,2)=K_{X/S}^{-1}\).
The sign and inverse in this identity matter and are correct.

The proposed weight is the standard \(\mathcal O(2,2)\) weight plus smooth global real functions of
\(p=|s|^2/(1+|s|^2)\) and \(x=|z|^2/(1+|z|^2)\). On inversion of either affine coordinate, subtraction of the corresponding \(2\log|\cdot|^2\) transition weight gives precisely the stated smooth formula. All four charts were differentiated independently. The global square root is a metric on the already specified line bundle \(\mathcal O_E(1)\), not an assumed square root of an arbitrary line bundle.

### 3.2 Universal positivity certificate

For \(\epsilon=1/96\), \(\delta=1/4\), the normalized Hessian entries are correctly

\[
A=4p+(\epsilon+\delta x^2)(1-2p),\quad
B=2+2\delta p x(2-3x),\quad
Q=4\delta^2p(1-p)x^3(1-x).
\]

Let

\[
A_0=\epsilon+\frac{167}{48}p,\quad B_0=\frac32,\quad Q_0=\frac p4.
\]

Their remainders have the following nonnegative expressions on the entire closed square \([0,1]^2\):

\[
\begin{aligned}
A-A_0&=\delta x^2+2\delta p(1-x^2),\\
B-B_0&=2\delta\big[(1-p)+p(1-x)(1+3x)\big],\\
Q_0-Q&=4\delta^2p\big[1-(1-p)x^3(1-x)\big].
\end{aligned}
\]

The last bracket is nonnegative since all factors of \((1-p)x^3(1-x)\) are in \([0,1]\). In particular \(A\ge A_0>0\), \(B\ge B_0>0\), and

\[
\begin{aligned}
AB-Q-(A_0B_0-Q_0)
&=(A-A_0)B+A_0(B-B_0)+(Q_0-Q)\ge0,\\
A_0B_0-Q_0&=\frac1{64}+\frac{159}{32}p>0.
\end{aligned}
\]

This proves positive definiteness everywhere, including infinity-chart endpoints. The reference Fubini–Study frames differ by unit-modulus factors on overlaps; diagonal coefficients, the mixed modulus, and the determinant are the appropriate invariant quantities. No sampled grid is needed for this conclusion.

## 4. Exact evolution and the negative direction

### 4.1 Why the second-variation equation is exact

The initial metric and defining flow respect rotation of the base coordinate. Fiberwise uniqueness therefore preserves this symmetry. On the full central fiber,

\[
\phi_s=\phi_{\bar s}=\phi_{s\bar z}=0.
\]

The initial central-fiber weight is \(2\log(1+|z|^2)+2-\epsilon\). Its two normalized measures agree, so it is exactly stationary, not merely stationary to first order. Hence

\[
g_F=\frac2{(1+|z|^2)^2},\qquad
\Delta_F=g_F^{-1}\partial_z\partial_{\bar z}.
\]

Set \(w=\phi_{s\bar s}|_{s=0}\). Differentiating (A1) gives

\[
(\log g)_{s\bar s}=\Delta_Fw,
\qquad
(\log I)_{s\bar s}=-\int w\,\mu_F.
\]

The first identity uses \(g_s=g_{\bar s}=0\). For the second, \(I_s=0\) and
\(I_{s\bar s}=\int(|\phi_s|^2-\phi_{s\bar s})e^{-\phi}dA=-I\int w\mu_F\).
Compactness and the cited finite-time smoothness justify differentiating under the integral. Thus

\[
w_t=\Delta_Fw+w-\int w\,\mu_F,
\qquad w(x,0)=\epsilon+\delta x^2.
\tag{A2}
\]

This is the equation of the actual nonlinear solution's second base derivative. No perturbative remainder is discarded. The frozen proof's uniqueness argument for both the scalar flow and (A2) is valid.

### 4.2 Eigenvalues, average, and time

Radial integration pushes \(\mu_F\) to \(dx\) on \([0,1]\), and the complex Laplacian is

\[
\Delta_FF=\tfrac12\big[x(1-x)F''+(1-2x)F'\big].
\]

Consequently \(P_1=2x-1\) and \(P_2=6x^2-6x+1\) have mean zero and eigenvalues \(-1\) and \(-3\). Since

\[
x^2=\tfrac13+\tfrac12P_1+\tfrac16P_2,
\]

the constant mode of (A2) is fixed, the first mode is fixed, and the second mode decays as \(e^{-2t}\). The candidate's exact solution follows:

\[
w=\epsilon+\frac\delta3+\frac\delta2P_1+
\frac\delta6e^{-2t}P_2.
\]

At \(x=0\),

\[
w(0,t)=\frac1{96}-\frac{1-e^{-2t}}{24}.
\]

It vanishes at \(t=\frac12\log(4/3)\) and is \(-1/96\) at \(t=\frac12\log2\), exactly as claimed. The reaction/Laplacian signs and all factors of two are consistent with the direct scalar equation.

The Schur complement is

\[
c(\phi_t)=\phi_{s\bar s}-\frac{|\phi_{s\bar z}|^2}{\phi_{z\bar z}}.
\]

At the point in question the mixed term vanishes, so \(c=w\). In fact the negative raw horizontal coefficient already evaluates the curvature negatively on the honest local tangent vector \(\partial_s\). The argument does not confuse fiberwise positivity with total-space positivity.

## 5. Analytic dependency and verification limits

Theorem 5 on printed p. 1519 states smooth existence on \(X\times[0,\infty)\) for the flow (13). Its proof identifies the fiberwise flow with the normalized anticanonical flow through a local frame of \(\det E\), and invokes Theorem 4. Theorem 4 explicitly includes finite-time smoothness over the total family. This is exactly the needed parameter-regularity assertion. Only finite time, uniqueness, and fiberwise positivity are used; no smoothness of a limiting metric in the base direction is required.

The global initial curvature bound is stronger than this theorem's fiberwise hypothesis. Loss of horizontal positivity therefore does not terminate or invalidate the fiberwise flow before the evaluation time. The source's separate issues about convergence along non-discrete automorphism groups or horizontal regularity at infinite time have no role in this example.

The supplied verifier was rerun without changing the frozen output: all 40 identities and 441 supplementary grid points passed. The independent `audit_verify.py` checks 43 exact identities and all frozen hashes, without using any grid. It independently checks all four chart Hessians, the universal determinant-remainder decomposition, spectral evolution, the exact sign, the stationary-product normalization contradiction, and the root/time scaling. These tests supplement the argument; neither verifier proves the imported analytic existence theorem.

## 6. Disposition

No mandatory mathematical repair was identified. For any presentation of this result, retain the precise scope “equation (13) on \(\mathcal O_E(r)\)” and the explicit existence dependency. The stationary-product test in Section 2 is a useful addition to the existing normalization discussion: it resolves the apparent conflict with the published general formula by direct evidence rather than an assertion about editorial intent.

The frozen candidate answers the source's universal positivity-preservation question negatively under its explicitly defined normalization. It does not disprove the Griffiths conjecture, deny the existence of good initial metrics on this bundle, or establish any historical priority claim.
