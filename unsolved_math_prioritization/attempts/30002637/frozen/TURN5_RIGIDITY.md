# Author turn 5/5: Ricci ground-state transform and the missing spectral comparison

## Result and status

The universal problem is **not solved** by this attempt. The following conditional instability criterion is proved below, in every dimension and without a curvature sign, complex structure, or topological hypothesis.

Normalize a connected closed gradient shrinker by

\[
\operatorname{Ric}+\nabla^2f=g.
\]

Let \(\lambda_f\) be the first positive eigenvalue of \(-\Delta_f\) in \(L^2(e^{-f}dV)\), and let \(\lambda_{\mathrm{Ric}}\) be the first positive eigenvalue of

\[
-\Delta_{f-2\log|\operatorname{Ric}|}
\quad\text{in }L^2(|\operatorname{Ric}|^2e^{-f}dV).
\]

For a non-Einstein compact shrinker, \(1<\lambda_f\leq2\). This attempt proves

\[
\boxed{\nu\text{-stable}\quad\Longrightarrow\quad
\lambda_{\mathrm{Ric}}\geq\lambda_f.}
\tag{A}
\]

Consequently,

\[
\boxed{\lambda_{\mathrm{Ric}}<\lambda_f
\quad\Longrightarrow\quad\nu\text{-unstable}.}
\tag{B}
\]

The conclusion concerns a genuinely positive eigenvalue of the actual Hessian on the diffeomorphism/scaling quotient. It is not merely positivity of a tensor operator before removing gauge. In the normalization above, (B) gives an eigenvalue of the quotient operator \(N\) at least \(1-\lambda_{\mathrm{Ric}}/2>0\).

There is **no proof here that the strict comparison in (B) holds for every non-Einstein shrinker**. Failure to establish or satisfy (B) does not imply stability. An exact, more sensitive scalar formula for \(\langle N(\phi\operatorname{Ric}),\phi\operatorname{Ric}\rangle_f\) is also derived. The missing geometric inequality is stated in Section 7.

These are deductions within this attempt from the cited known identities. No claim of literature novelty is made.

## 1. Sources, conventions, and basic identities

The target is the question in Klaus Kröncke, *Stability and Instability of Ricci Solitons*, Oberwolfach Report 36/2014, printed pp. 2017–2019, particularly p. 2019: whether every compact nontrivial Ricci soliton has a positive shrinker-entropy Hessian eigenvalue. Here nontrivial means non-Einstein. The all-dimensional compact target is retained.

The input spectral decomposition is Cao–Zhu, *Linear Stability of Compact Shrinking Ricci Solitons*, arXiv:2304.01453v4, Theorems 1.1–1.2, Lemmas 2.1–2.3, and Proposition 3.3. Their displayed normalization \(\operatorname{Ric}+\nabla^2f=g/2\) is rescaled here to coefficient 1. Their p. 13 still presents the stable-implies-Einstein assertion as an open conjecture, at least in dimension four.

Set

\[
T=\operatorname{Ric},\quad r=|T|,\quad
d\mu=e^{-f}dV,\quad A=-\Delta_f,\quad
L=\tfrac12\Delta_f+\operatorname{Rm}(\cdot).
\]

Write \(\langle\cdot,\cdot\rangle_f\) for the integrated weighted inner product and \(Q_L(h)=\langle Lh,h\rangle_f\). The normalization gives

\[
\operatorname{div}_fT=0,\qquad LT=T,\qquad
\Delta_fR=2R-2r^2,
\tag{1.1}
\]

and therefore

\[
m:=\int_Mr^2\,d\mu=\int_MR\,d\mu>0.
\tag{1.2}
\]

The scalar curvature is positive. For completeness, at a negative minimum the scalar equation in (1.1) is impossible. Thus \(R\geq0\); the strong maximum principle applied to \((\Delta_f-2)R=-2r^2\leq0\) shows that a zero forces \(R\equiv0\). That contradicts the integrated unweighted trace equation \(\int R\,dV=n\operatorname{Vol}(M)\). Hence \(R>0\), and \(r\geq R/\sqrt n>0\). All weights and logarithms used here are consequently smooth and positive.

The known orthogonal, \(L\)-invariant splitting is

\[
\Gamma(S^2T^*M)=\mathcal G\oplus\mathbb RT\oplus\mathcal V,
\quad
\mathcal G=\operatorname{Im}(\operatorname{div}_f^*),
\quad
\mathcal V=\ker\operatorname{div}_f\cap T^\perp.
\tag{1.3}
\]

Here \(\operatorname{div}_f^*\omega=-\tfrac12\mathcal L_{\omega^\sharp}g\). The actual stability operator satisfies

\[
N|_{\mathcal G\oplus\mathbb RT}=0,
\qquad N|_{\mathcal V}=L|_{\mathcal V}.
\tag{1.4}
\]

The positive eigenvalue \(LT=T\) is therefore removed, not an instability.

Weighted Bochner with \(\operatorname{Ric}+\nabla^2f=g\) gives, for \(Au=\lambda u\),

\[
\int|\nabla^2u|^2d\mu
=\lambda(\lambda-1)\int u^2d\mu.
\tag{1.5}
\]

Every nonconstant scalar eigenfunction has \(\lambda>1\): equality would make its Hessian zero, hence make it constant on a compact manifold. Also \(\Delta_ff=-2f+C\), so if \(f\) is nonconstant, its weighted mean-zero part is an \(A\)-eigenfunction with eigenvalue 2. Thus

\[
1<\lambda_f\leq2
\quad\text{on every non-Einstein compact shrinker.}
\tag{1.6}
\]

## 2. The full gauge bound, including nongradient one-forms

The bound needed for (A) is stronger than the universal \(L|_{\mathcal G}<1/2\), and must cover all gauge tensors.

Define

\[
\kappa=1-\frac{\lambda_f}{2}\in[0,1/2).
\tag{2.1}
\]

We prove

\[
Q_L(h)\leq\kappa\|h\|_f^2
\qquad (h\in\mathcal G).
\tag{2.2}
\]

Every smooth one-form has the weighted orthogonal decomposition

\[
\omega=du+\eta,\qquad \operatorname{div}_f\eta=0,
\tag{2.3}
\]

where \(u\) is obtained by solving \(\Delta_fu=\operatorname{div}_f\omega\) with mean zero. This decomposition includes all nongradient and harmonic components in \(\eta\); no simple-connectedness or vanishing-cohomology hypothesis is used.

The corresponding tensor summands are orthogonal because

\[
\operatorname{div}_f\nabla^2u=d(\Delta_fu+u),
\]

and therefore \(\langle\nabla^2u,\operatorname{div}_f^*\eta\rangle_f=0\). Both summands are \(L\)-invariant, using the rescaled Cao–Zhu commutators

\[
L(\nabla^2u)=\tfrac12\nabla^2(\Delta_fu+2u),
\quad
L(\operatorname{div}_f^*\eta)
=\tfrac12\operatorname{div}_f^*(\Delta_f\eta+\eta).
\tag{2.4}
\]

The latter one-form remains weighted divergence-free, since
\(\operatorname{div}_f\Delta_f\eta=\Delta_f\operatorname{div}_f\eta+\operatorname{div}_f\eta\).

On the gradient summand, an \(A\)-eigenfunction of eigenvalue \(\lambda\) produces the nonzero Hessian eigentensor with eigenvalue \(1-\lambda/2\). Expansion in a scalar eigenbasis consequently bounds this entire summand above by \(\kappa\).

On the nongradient summand, let \(h=\operatorname{div}_f^*\eta\) with \(\operatorname{div}_f\eta=0\). Its entropy correction potential is zero. Indeed, for a Lie derivative \(\mathcal L_{\omega^\sharp}g\), the correction potential is \(2\operatorname{div}_f\omega\); linearity gives the assertion for \(h\). It is also orthogonal to \(T\). Since \(Nh=0\), the actual Hessian formula gives

\[
Lh+\operatorname{div}_f^*\operatorname{div}_fh=0,
\qquad
Q_L(h)=-\|\operatorname{div}_fh\|_f^2\leq0.
\tag{2.5}
\]

Combining the orthogonal invariant summands and \(\kappa\geq0\) proves (2.2). The bound is attained on Hessians of first scalar eigenfunctions, so it is the actual top gauge eigenvalue in the non-Einstein setting.

This check matters: a positive \(L\)-Rayleigh quotient below \(\kappa\) could lie entirely in gauge and says nothing about \(\nu\)-instability.

## 3. Ricci ground-state identity and the conditional comparison

For every smooth real \(\phi\), the equation \(LT=T\) gives the exact ground-state identity

\[
\boxed{
Q_L(\phi T)
=\int\phi^2r^2d\mu
-\frac12\int|d\phi|^2r^2d\mu.}
\tag{3.1}
\]

One direct verification uses

\[
L(\phi T)=\left(\phi+\tfrac12\Delta_f\phi\right)T
+\nabla_{\nabla\phi}T.
\]

Upon integration, the cross term from \(\Delta_f\phi\) cancels
\(\phi\langle\nabla_{\nabla\phi}T,T\rangle
=\tfrac12\phi\langle d\phi,d(r^2)\rangle\).

Let \(d\rho=r^2d\mu\). If \(\int\phi\,d\rho=0\), then \(\phi T\perp T\). Under the stability assumption, decompose

\[
\phi T=h_G+h_V,
\qquad h_G\in\mathcal G,\quad h_V\in\mathcal V.
\]

The invariant splitting, (2.2), and \(L|_{\mathcal V}\leq0\) yield

\[
Q_L(\phi T)
\leq\kappa\|h_G\|_f^2
\leq\kappa\|\phi T\|_f^2.
\]

Using (3.1) therefore proves the genuine scalar Poincaré inequality

\[
\int|d\phi|^2\,d\rho
\geq\lambda_f\int\phi^2\,d\rho
\qquad\left(\int\phi\,d\rho=0\right).
\tag{3.2}
\]

Taking the infimum gives (A).

For clarity, (B) can also be proved directly without merely taking a contrapositive. Take a first \(\rho\)-eigenfunction and set

\[
a=1-\lambda_{\mathrm{Ric}}/2>\kappa\geq0.
\]

Then \(Q_L(\phi T)=a\|\phi T\|^2\), so

\[
Q_L(h_V)
\geq a\|h_V\|^2+(a-\kappa)\|h_G\|^2.
\tag{3.3}
\]

In particular \(h_V\neq0\), and its quotient Rayleigh quotient is at least \(a>0\). Elliptic spectral theory on the compact quotient gives the claimed positive \(N\)-eigenvalue.

There is also a multiplicity version: if the first \(k\) positive scalar \(\rho\)-eigenvalues are strictly below \(\lambda_f\), their Ricci multiples project injectively to a \(k\)-dimensional subspace of \(\mathcal V\) on which \(L-\kappa\) is positive definite. Thus there are at least \(k\) quotient eigenvalues greater than \(\kappa\).

These are usable sufficient criteria; they are not unconditional assertions about those scalar spectra.

## 4. Exact gauge-corrected Ricci-multiplier formula

The preceding min–max criterion deliberately avoids computing the gauge projection. The full entropy formula yields a sharper test with all corrections explicit.

In the present normalization,

\[
Nh=Lh+\operatorname{div}_f^*\operatorname{div}_fh
+\tfrac12\nabla^2v_h
-T\frac{\langle T,h\rangle_f}{m},
\quad
(\Delta_f+1)v_h=\operatorname{div}_f\operatorname{div}_fh.
\tag{4.1}
\]

The potential is mean zero. Since \(\lambda_f>1\), \(A-1\) is positive and invertible on mean-zero functions.

For \(h=\phi T\), define the one-form and function

\[
b=T(\nabla\phi,\cdot),\qquad
D=\operatorname{div}_fb=T:\nabla^2\phi.
\tag{4.2}
\]

The second equality uses \(\operatorname{div}_fT=0\). In particular \(\int D\,d\mu=0\). Two weighted integrations by parts give
\(\langle\nabla^2v_h,h\rangle_f=\langle v_h,D\rangle_f\), while
\(v_h=-(A-1)^{-1}D\). Therefore

\[
\boxed{
\begin{aligned}
Q_N(\phi T)
={}&\int\phi^2\,d\rho
-\frac12\int|d\phi|^2\,d\rho
-\frac{(\int\phi\,d\rho)^2}{m}\\
&+\int|T(\nabla\phi,\cdot)|^2d\mu
-\frac12\langle D,(A-1)^{-1}D\rangle_f.
\end{aligned}}
\tag{4.3}
\]

This is an exact scalar-multiplier reduction of the actual Hessian, not the unprojected \(L\)-form. If its right side is positive for any \(\phi\), the target instability follows for that shrinker. If it is never positive, other symmetric-tensor directions may still be unstable.

To see precisely the sign of the correction, decompose

\[
b=du+\beta,\qquad \operatorname{div}_f\beta=0,
\qquad \int u\,d\mu=0.
\]

For a weighted orthonormal scalar eigenbasis \(Ae_j=\lambda_je_j\), write \(u=\sum u_je_j\). Since \(D=\Delta_fu=-Au\), the last line of (4.3) becomes

\[
\boxed{
\|\beta\|_f^2
+\frac12\sum_{j\geq1}
\frac{\lambda_j(\lambda_j-2)}{\lambda_j-1}\,u_j^2.}
\tag{4.4}
\]

Thus the correction need not be nonnegative when \(\lambda_f<2\). Its only negative scalar contributions come from \(1<\lambda_j<2\), exactly the range responsible for positive Hessian gauge modes. If \(\lambda_f=2\), the correction is nonnegative. Equality then requires \(\beta=0\) and \(u\) to lie in the scalar eigenvalue-2 space.

A fully local sufficient test follows as well. Set

\[
c=\frac{2-\lambda_f}{\lambda_f-1}\geq0.
\]

Because \((x-2)/(x-1)\) is increasing for \(x>1\), (4.4) is at least \(-c\|b\|_f^2/2\). Hence a mean-\(\rho\)-zero \(\phi\) satisfying

\[
\int\left(r^2|d\phi|^2+c|T(\nabla\phi,\cdot)|^2\right)d\mu
<2\int\phi^2r^2d\mu
\tag{4.5}
\]

proves instability. Conversely, stability implies the reverse weak inequality for every such \(\phi\). No universal validity of the strict test is asserted.

### Sign and normalization checks

* A constant multiplier gives zero in (4.3), as required by \(NT=0\).
* At an Einstein metric with \(T=g\), a scalar eigenfunction \(A\phi=\lambda\phi\) gives \(b=d\phi\), \(D=-\lambda\phi\), and
  \[
  Q_N(\phi g)
  =\frac{(2-\lambda)((n-1)\lambda-n)}{2(\lambda-1)}\|\phi\|_f^2.
  \]
  This follows directly from (4.3) and checks both the resolvent sign and the Ricci-line subtraction. It vanishes on the first round-sphere conformal gauge mode \(\lambda=n/(n-1)\). This Einstein calculation is only a consistency check, not an attempt to replace the non-Einstein target with an Einstein example.

## 5. Why the tensor ground-state transform is not scalar positivity

One might hope that a stable shrinker has a unique top \(L\)-eigentensor \(T\), and that a tensor version of the positive ground-state principle would force \(T\) to be parallel. This does not follow.

Put \(U=T/r\), a smooth unit symmetric tensor, and write \(W=\operatorname{Rm}(\cdot)\) as a symmetric bundle endomorphism. The Ricci Bochner equation gives

\[
\frac{\Delta_fr}{r}
=2-2\langle WU,U\rangle+|\nabla U|^2.
\tag{5.1}
\]

For an arbitrary smooth symmetric tensor \(k\), integration by parts then yields the exact bundle transform

\[
\boxed{
\begin{aligned}
Q_L(rk)-\|rk\|_f^2
=\int r^2\bigg[&-\frac12|\nabla k|^2+\langle Wk,k\rangle\\
&-\langle WU,U\rangle|k|^2
+\frac12|\nabla U|^2|k|^2\bigg]d\mu.
\end{aligned}}
\tag{5.2}
\]

Equivalently,

\[
r^{-1}(L-1)(rk)
=\frac12\Delta_{f-2\log r}k+Wk
+\left(\frac12|\nabla U|^2-\langle WU,U\rangle\right)k.
\tag{5.3}
\]

Substituting \(k=\phi U\) makes the \(|\nabla U|^2\) and curvature terms cancel, recovering (3.1). For a transverse tensor \(k\), however,

\[
\langle Wk,k\rangle-\langle WU,U\rangle|k|^2
\]

has no sign under the hypotheses. It cannot be discarded to turn (5.2) into a rigidity proof.

Nor does \(R>0\) provide a positive-definite Ricci eigentensor or an order-preserving tensor heat operator. At a boundary point of the cone of positive semidefinite symmetric tensors, the reaction term in a null direction is a weighted sum of sectional curvatures. With no curvature sign, its sign is not controlled. A scalar Perron–Frobenius or positive-ground-state argument cannot simply be applied to this tensor operator.

## 6. The ordinary Bochner identities do not close the argument

The integrated Ricci identity is

\[
\int\operatorname{Rm}(T,T)d\mu
=\int r^2d\mu+\frac12\int|\nabla T|^2d\mu.
\tag{6.1}
\]

It relates curvature energy to the nonparallel part of Ricci, but supplies neither the sign of the transverse curvature term in (5.2) nor an upper bound for a scalar spectral gap.

There is also an important exact zero mode:

\[
H:=\nabla^2f=g-T\in\mathcal G,
\qquad LH=L(g)-L(T)=T-T=0.
\tag{6.2}
\]

Consequently

\[
\int\operatorname{Rm}(H,H)d\mu
=\frac12\int|\nabla H|^2d\mu
=\frac12\int|\nabla T|^2d\mu.
\tag{6.3}
\]

This does not force either side to vanish. Expanding \(H=g-T\) shows that (6.3) is already a consequence of (1.2) and (6.1). It is therefore circular to use it as an independent nonnegative term that would force \(f\) constant.

A nonconstant \(f\) thus supplies a nonzero **gauge** zero mode, compatible with \(L|_{\mathcal V}\leq0\). Min–max must produce a mode strictly above the gauge threshold or explicitly evaluate (4.3); merely exhibiting \(T\), \(\nabla^2f\), or nonparallel Ricci is insufficient.

Finally, the Bakry–Émery tensor for the Ricci-weighted scalar measure is

\[
\operatorname{Ric}+\nabla^2(f-2\log r)
=g-2\nabla^2\log r.
\tag{6.4}
\]

Equation (5.1) controls a drift trace of \(\log r\), with an uncontrolled curvature contraction. It provides no required bound on the full Hessian in (6.4), and a scalar Bochner estimate for this new measure does not yield the desired strict upper comparison of gaps. In particular, one cannot infer \(\lambda_{\mathrm{Ric}}<\lambda_f\) simply from the fact that \(r\) is nonconstant.

## 7. Precise missing inequality and endpoint

A sufficient geometric bridge for this route would be the following unconditional assertion:

> For every non-Einstein compact shrinker, there exists a smooth \(\phi\), with \(\int\phi|\operatorname{Ric}|^2e^{-f}dV=0\), such that
> \[
> \int|d\phi|^2|\operatorname{Ric}|^2e^{-f}dV
> <\lambda_f\int\phi^2|\operatorname{Ric}|^2e^{-f}dV.
> \tag{7.1}
> \]

Equivalently, the bridge is the strict gap decrease \(\lambda_{\mathrm{Ric}}<\lambda_f\). Proving it would close the target by Section 3. It has **not** been proved here and is **not** asserted to be necessary for instability.

A potentially weaker bridge is to prove that the right side of the exact formula (4.3) is positive for some multiplier on every non-Einstein compact shrinker. This too remains unproved. These scalar-multiplier tests do not exhaust \(\mathcal V\), so their failure could not disprove the original instability statement.

The currently used soliton and Bochner identities do not establish either bridge: the reweighted Hessian is uncontrolled, the transverse curvature terms are indefinite, and the known potential zero mode is removed by gauge. No permitted argument in this attempt forces \(f\) constant from \(\nu\)-stability.

**Final outcome:** a checked conditional scalar spectral obstruction to stability, a checked full-gauge min–max argument, and an exact gauge-corrected Ricci-multiplier formula; the universal all-dimensional conjecture remains unresolved. This is the fifth and final proof-attempt response.

## Primary references

1. Klaus Kröncke, *Stability and Instability of Ricci Solitons*, Oberwolfach Report 36/2014, pp. 2017–2019. DOI: https://doi.org/10.4171/OWR/2014/36 .
2. Huai-Dong Cao and Meng Zhu, *Linear Stability of Compact Shrinking Ricci Solitons*, arXiv:2304.01453v4 (2 February 2024), especially pp. 3–13. https://arxiv.org/abs/2304.01453 .

Only a short newly written paraphrase of the source question is used; no source PDF or source-page image is included.
