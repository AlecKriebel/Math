# Independent Fourier-witness derivation (frozen before comparison)

Audit family: functional Fourier / isonormal Gaussian witness. Target: PR 1071,
problem 30002170, exact head `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`.
This derivation uses the original `PROOF.md`, `ALL_H_COROLLARY.md`, and
`AREA_CONVENTION_CHECK.md`, and fresh primary-source reading. It does not use
the prior `INDEPENDENT_AUDIT.md`, status, provenance, README, manifest, or source
ledger. Their bytes were preserved without reading their contents. The embedded
acceptance labels in the three mathematical inputs have no evidentiary weight.

## Exact claim and success criterion

Let (H\in(1/4,1)), (T>0), (n\in\mathbb N\), and let (B^1,B^2)
be independent, centered, continuous Gaussian processes with covariance

\[
R_H(s,t)=\tfrac12(s^{2H}+t^{2H}-|t-s|^{2H}),\qquad s,t\ge0.
\]

The target is the canonical iterated integral

\[
X_T=\int_0^T B^1_t\,dB^2_t,
\quad\mathcal G=\sigma(B^i_{kT/n}:i=1,2,\ 1\le k\le n).
\]

Prove, for **every** (F\in L^2(\mathcal G)),

\[
\|X_T-F\|_2\ge c_HT^{2H}n^{1/2-2H}
\]

with an explicitly defined (c_H>0) independent of (n,T). No sharp
constant, normalized-error limit, endpoint, correlated-component, adaptive,
unequal-grid, or priority conclusion is part of this audit. This is an exact
finite-(n) inequality and includes (n=1).

The fresh original OWR report, printed pp. 2524-2525 (PDF pages 32-33), has
precisely this integral and the vector observations, and asks for a positive
constant in this inequality, not for an exact asymptotic limit. Its Brownian
optimum is (T/(2\sqrt n)). [Primary original](https://ems.press/content/serial-article-files/46412),
DOI [10.4171/OWR/2012/41](https://doi.org/10.4171/OWR/2012/41).

## 1. Standard normalization and real Fourier space

Use (widehat h(\xi)=\int e^{-it\xi}h(t)\,dt). Put

\[
D_H=\int_{\mathbb R}|e^{i\xi}-1|^2|\xi|^{-1-2H}\,d\xi.
\]

The zero-frequency bound (O(|\xi|^{1-2H})) and large-frequency bound
(4|\xi|^{-1-2H}) prove (0<D_H<\infty) exactly for (0<H<1).
The real Hilbert space consists of (L^2(\mathbb R;\mathbb C)) functions
(u(-\xi)=\overline{u(\xi)}), with
(\langle u,v\rangle=\int u\overline v). The integral is real: changing
(\xi\mapsto-\xi) conjugates it. Completeness follows from the closedness of
this symmetry condition in complex (L^2), regarded as a real Hilbert space.

Define

\[
K_t(\xi)=D_H^{-1/2}(e^{it\xi}-1)|\xi|^{-H-1/2}.
\]

Each (K_t) is in the real space. A change of variable gives
(\|K_t-K_s\|^2=|t-s|^{2H}), and (K_0=0). Polarization then gives exactly
(\langle K_t,K_s\rangle=R_H(s,t)). Independent real isonormal processes
(W_1,W_2) realize (B^i_t=W_i(K_t)). A continuous modification exists by
the Gaussian increment moment bound and Kolmogorov's criterion, so it has the
standard continuous-path fBm law; finite sum laws alone also suffice below.

Supplementary explicit evaluation, not needed for the proof: writing
(\beta=2H\in(0,2)) and using a positive Laplace representation,

\[
\begin{aligned}
D_H
&=\frac4{\Gamma(1+\beta)}\int_0^\infty t^\beta
   \left[\int_0^\infty(1-\cos x)e^{-tx}\,dx\right]dt\\
&=\frac4{\Gamma(1+\beta)}\int_0^\infty\frac{t^{\beta-1}}{1+t^2}\,dt
=\frac{2\pi}{\Gamma(1+2H)\sin(\pi H)}.
\end{aligned}
\]

Tonelli is valid for the nonnegative Laplace integrand, and the last integral
is the beta integral. In particular (D_{1/2}=2\pi), agreeing with the
standard Brownian normalization.

For a real compactly supported (h) with (h(0)=0), define

\[
u_h(\xi)=\frac{\sqrt{D_H}}{2\pi}|\xi|^{H+1/2}
               \overline{\widehat h(\xi)}.
\]

If (\int|\xi|^{2H+1}|\widehat h|^2<\infty), it belongs to the real
Hilbert space. The conjugation is essential: it ensures

\[
\langle K_t,u_h\rangle
=\frac1{2\pi}\int(e^{it\xi}-1)\widehat h(\xi)\,d\xi
=h(t)-h(0)=h(t).
\]

For the functions below the Fourier transform is absolutely integrable, so
ordinary Fourier inversion applies at every (t). This calculation checks
both the Fourier sign and every (2\pi,D_H) factor.

## 2. Deterministic functions, endpoints, and their area

On ([0,1]), let

\[
\phi=x^4(1-x)^4=x^4-4x^5+6x^6-4x^7+x^8,
\quad f=\phi',\quad g=\phi,
\]

and extend by zero outside. Since (phi,phi',phi'',phi''') vanish at
both endpoints, (f,g), and their first and second derivatives, have zero
boundary values. Consequently the zero extensions are in (W^{3,1}(\mathbb R)):
the third weak derivatives are the piecewise polynomials (f'''=\phi'''')
and (g'''=\phi'''); no boundary delta masses occur. It is not necessary that
(f''') itself vanish at the endpoints; in fact its values there are 24.
This distinction was explicitly checked.

Three distributional integrations by parts give

\[
|\widehat r(\eta)|\le L_r:=\|r\|_1,
\qquad |\widehat r(\eta)|\le N_r|\eta|^{-3},
\quad N_r:=\|r'''\|_1,\ r=f,g.
\]

The exact polynomial coefficients give

\[
f=4x^3-20x^4+36x^5-28x^6+8x^7,
\quad g'''=24x-240x^2+720x^3-840x^4+336x^5,
\]

\[
f'''=24-480x+2160x^2-3360x^3+1680x^4.
\]

Thus all norms are finite, (L_f=1/128), (L_g=1/630), and

\[
a=\int_0^1fg'\,dx=\int_0^1(\phi')^2\,dx=\frac4{45045}>0.
\]

The exact value was recomputed by rational polynomial multiplication and
integration, rather than accepted from the submitted audit labels.

## 3. Periodization and a uniform **upper** Gram estimate

Set (\alpha=2H+1\in(3/2,3)). Define

\[
P_r(\theta)=\sum_{\ell\in\mathbb Z}|\theta+2\pi\ell|^\alpha
                        |\widehat r(\theta+2\pi\ell)|^2,
\qquad |\theta|\le\pi.
\]

The central summand is at most (\pi^\alpha L_r^2). All noncentral terms
are bounded by (N_r^2[\pi(2|\ell|-1)]^{\alpha-6}). For (p=6-\alpha>3),

\[
\sum_{\ell\ge1}(2\ell-1)^{-p}
\le1+\int_1^\infty(2x-1)^{-p}\,dx
=1+\frac1{2(p-1)}.
\]

Hence the submitted explicit choice is valid over the full range:

\[
0<\overline P_r:=\pi^\alpha L_r^2+
  2N_r^2\pi^{\alpha-6}\left(1+\frac1{2(5-\alpha)}\right)<\infty,
\qquad P_r\le\overline P_r.
\]

The weighted transform is integrable at zero (bounded transform and
(\alpha>0)) and at infinity (power (\alpha-6<-3)). All such (u_h)
are legitimate. Positivity of the explicit bound follows already from (L_r>0).

For (\Delta>0), define

\[
r_j(t)=\Delta^H r(t/\Delta-j).
\]

Its transform is (\Delta^{H+1}e^{-ij\Delta\xi}\widehat r(\Delta\xi)).
The powers in the inner product are
(\Delta^{2H+2}\Delta^{-\alpha}\Delta^{-1}=\Delta^0), exactly. Thus

\[
\langle u_{r_j},u_{r_k}\rangle
=\frac{D_H}{4\pi^2}\int|\eta|^\alpha|\widehat r(\eta)|^2
                              e^{i(j-k)\eta}\,d\eta.
\]

For any finitely supported real (b=(b_j)), nonnegative-integrand Tonelli
allows periodization. The trigonometric polynomial is (2\pi)-periodic, and
its squared integral is (2\pi\sum b_j^2). Therefore

\[
\left\|\sum_jb_ju_{r_j}\right\|^2
\le M_r\sum_jb_j^2,\qquad
M_r=\frac{D_H}{2\pi}\overline P_r.
\]

The argument uses only an upper Gram bound on selected smooth covariance
paths. It does not use a coercive lower estimate for arbitrary fBm increments.
Such an increment estimate would be false for (H<1/2): coefficients all 1
give variance (n^{2H}), not a lower constant times (n).

## 4. Invisible joint Gaussian vector and product variance

Take (\Delta=T/n), (j=0,\ldots,n-1), and

\[
U_j=W_1(u_{f_j}),\quad V_j=W_2(u_{g_j}),\quad Y=\sum_jU_jV_j.
\]

Each covariance path (f_j,g_j) vanishes at **every** grid point, including
all other cells and both endpoints. Cross-component covariances vanish by
component independence. All witness coordinates and all (2n) observations
form one centered finite Gaussian vector. Its cross-covariance block is zero,
so its characteristic function factors into witness and observation factors.
The witness vector is consequently independent of the complete observation
vector, not merely separately uncorrelated with individual observations.
This yields independence from (\mathcal G). Also (E[Y]=0), because the
entire (U)- and (V)-vectors come from independent isonormal processes.

Let (A=E[UU^\mathsf T]), (C=E[VV^\mathsf T]). They are real symmetric
positive semidefinite, with (A\le M_fI), (C\le M_gI). Component
independence gives

\[
E[Y^2]=\sum_{j,k}A_{jk}C_{jk}=\operatorname{tr}(AC)
\le M_f\operatorname{tr}(C)\le nM_fM_g.
\]

The first inequality follows since
(\operatorname{tr}((M_fI-A)C)=\operatorname{tr}(C^{1/2}(M_fI-A)C^{1/2})\ge0).
Entrywise covariance signs are immaterial. It is not legitimate to replace
these inequalities by entrywise bounds on signed off-diagonal entries, and the
submitted proof does not do so.

## 5. Fresh audit of the stochastic-area input

Source: A. Neuenkirch, S. Tindel, J. Unterberger,
[arXiv:0902.0497v1](https://arxiv.org/pdf/0902.0497v1), downloaded afresh with
SHA-256 `de4d91bff1cde45c02298d9f7f49f34790b6c4043232eb6ef5da999af3128ebf`.
The version page lists v1 submitted 3 February 2009; the currently served PDF
has internal typesetting date 22 March 2022. The receipt identifies those
distinct facts and does not pretend these bytes were downloaded in 2009.
The journal citation is SPA 120 (2010), 223-254,
DOI [10.1016/j.spa.2009.10.007](https://doi.org/10.1016/j.spa.2009.10.007).
The exact journal PDF was not obtained and is not represented as inspected.

The required source premise is **only** existence of the standard (L^2)
area and convergence of the actual Euler sums. Fresh reading includes printed
pp. 1-14: covariance and integral definitions (4)-(5), Theorem 1.1, the Brownian
calculation, analytic-area Proposition 2.3, moment formulas, the local-area
decomposition, and the complete proof of Theorem 1.1 in Section 3.2. The
definition is an iterated integral, not an antisymmetric difference.

There is a source error worth isolating. On printed p. 12, equation (27) claims
the sum of rough-range off-diagonal covariances is (o(n^{1-4H})). That
does not follow from summability and is false using its own equation (26).
For (H\ne1/2), the covariance at lag 2 has a strictly positive product
kernel, so at least (2(n-2)) copies contribute. Thus the normalized sum
cannot tend to zero. None of that stronger assertion is needed here.

Here is an independent sufficient convergence derivation that retains the
valid source ingredients and avoids that error. From analytic-area existence,
Chen's identity, and joint self-similarity, write

\[
X_T-L_m=\sum_{j=0}^{m-1}J_j,
\qquad E[J_jJ_k]=T^{4H}m^{-4H}E[I_jI_k],
\quad I_j=A_{j,j+1}.
\]

The diagonal variance (c_1=E[I_0^2]) is finite by the (L^2) area
existence; nearest-neighbor covariances have absolute value at most (c_1)
by Cauchy-Schwarz. For (r=|j-k|\ge2), the two cell triangles stay a
distance at least (r-1) apart. Passing the smooth approximation covariance
kernel to its limit is legitimate away from the diagonal. Independence and
the differentiated standard covariance give the product kernel

\[
E[I_jI_k]=H^2(2H-1)^2
\int_{j<s<j+1}\int_{k<t<k+1}
\int_{j<u<s}\int_{k<v<t}|u-v|^{2H-2}|s-t|^{2H-2}
\,dv\,du\,dt\,ds.
\]

Because (2H-2<0), its absolute value is at most
(\tfrac14H^2(2H-1)^2(r-1)^{4H-4}); the triangle volumes multiply to
(1/4). The finite (r=0,1) terms require no singular-kernel manipulation.
Counting the (2(m-r)) pairs gives

\[
\|X_T-L_m\|_2^2
\le C_HT^{4H}m^{-4H}\left[m+
             \sum_{r=2}^{m-1}(m-r)(r-1)^{4H-4}\right].
\]

The bracket is (O(m)) for (H<3/4), (O(m\log m)) for (H=3/4),
and (O(m^{4H-2})) for (H>3/4). Thus the three sufficient upper bounds
are (O(m^{1-4H})), (O(m^{-2}\log m)), and (O(m^{-2})), all tending
to zero for (H>1/4). The same calculation for (H=1/2) follows directly
from the Itô isometry, with exact Euler squared error (T^2/(2m)).
This validates the full-(H) input used by the witness proof, including the
critical smooth value (H=3/4), without adopting questionable exact source
asymptotic coefficients. The standard (L^2) analytic-area existence result
is an explicit, inspected external theorem premise, not an optimal-
approximation lower bound or an equivalent claim.

## 6. Euler / polygonal canonical interface

The classical integral of the piecewise linear interpolations satisfies,
exactly for finite (m),

\[
P_m=L_m+Q_m,\qquad
Q_m=\tfrac12\sum_{k=0}^{m-1}\Delta_kB^1\Delta_kB^2,
\quad \delta=T/m.
\]

It is the one-half correction on **each cell**, obtained by integrating
((B^1_{k\delta}+u\Delta_kB^1)\Delta_kB^2du) over (0\le u\le1).
Component independence gives (E[Q_m]=0) and

\[
E[Q_m^2]=\frac{T^{4H}m^{-4H}}4
\left[m+2\sum_{r=1}^{m-1}(m-r)\rho_H(r)^2\right],
\]

\[
\rho_H(r)=\tfrac12(|r+1|^{2H}+|r-1|^{2H}-2|r|^{2H}).
\]

For (r\ge2), the second difference is the integral of the second
derivative of (x^{2H}) against the triangular weight on ([-1,1]).
Since (x\asymp r) there, ( |\rho_H(r)|\le C_Hr^{2H-2}). The
case (r=1) is finite, and at (H=1/2) all nonzero-lag values are exactly
zero. The same pair count as above gives convergence to zero in all three
regimes. Therefore (P_m-L_m\to0) in (L^2), and both have the same
limit. In particular the dyadic polygonal construction of the canonical
iterated integral has the source area's limit. This supplies the source-
to-canonical identification and checks the half correction; it is not a
bare equality of constructions by terminology.

At (H=1/2), independent components have zero mutual quadratic variation,
so Itô and Stratonovich iterated integrals coincide. At (H=1/4), neither
the preceding local-area convergence estimate nor this canonical input
extends. At (H=1), the harmonic normalization diverges. The proof asserts
neither endpoint and requires no constants uniform as an endpoint is approached.

## 7. Covariance with the actual integral and final bound

For each fixed (j), finite Euler sums and independence give exactly

\[
E[L_mU_jV_j]=\sum_{k=0}^{m-1}f_j(kT/m)
                 [g_j((k+1)T/m)-g_j(kT/m)].
\]

There are no extra Wick pairings: the component-1 and component-2
expectations factor separately. Each (U_jV_j\in L^2), and (L_m\to X_T)
in (L^2), so Cauchy-Schwarz allows the left limit. On the right, classical
Riemann-Stieltjes convergence applies to the continuously differentiable
functions. It gives

\[
E[X_TU_jV_j]=\int_0^Tf_jg'_j\,dt=\Delta^{2H}a.
\]

The derivative contributes (\Delta^{H-1}), the integrand (\Delta^H),
and (dt=\Delta dx): the total is exactly (\Delta^{2H}). Summing the
finite set of (n) cells,

\[
E[X_TY]=na\Delta^{2H}>0.
\]

For every (F\in L^2(\mathcal G)), joint independence and centering
yield (E[FY]=E[F]E[Y]=0); integrability follows from Cauchy-Schwarz.
Therefore

\[
na\Delta^{2H}=E[(X_T-F)Y]
\le\|X_T-F\|_2\sqrt{nM_fM_g}.
\]

This proves the exact claim with

\[
c_H=\frac{a}{\sqrt{M_fM_g}}
=\frac{2\pi a}{D_H\sqrt{\overline P_f\overline P_g}}>0.
\]

The bound directly includes all nonlinear estimators measurable with respect
to both component grids; it is not restricted to linear or quadratic
estimators. Conditional expectation is in (L^2), so the stated optimal
residual follows as a special case.

The isonormal witnesses need not be path-measurable in an initially supplied
model. This causes no gap: finite Euler sums and observations have the same
joint law in the isonormal realization; convergence in (L^2) fixes the
joint law of (X_T) and observations. The minimum error over all observation
functions depends only on this law. Alternatively any given measurable
observation function (F=f(Z)), obtained by the Doob-Dynkin lemma, can be
transferred to the same finite observation vector in this realization.
Thus the external witness can be used on that realization to bound the
original model's error.

The witness targets (int B^1dB^2), not twice the antisymmetric area.
The observed endpoint product obeys (B^1_TB^2_T=I_{12}+I_{21}) by the
polygonal identity and its limit. Hence an antisymmetric normalization
would have a different factor; no replacement of the target was made.

## 8. Brownian and prior-scope cross-checks

At (H=1/2), Plancherel gives the witness Gram entries
(\int r'_jr'_k\). Distinct cell interiors do not overlap, hence the two
Gram matrices are diagonal. Exact rational integration yields
(\int(\phi')^2=4/45045) and (\int(\phi'')^2=24/5005). The sharper
constant for this same witness is (sqrt{1/54}\), less than the Brownian
optimum (1/2). The submitted looser periodization constant is consistent
and not sharp.

An independent Brownian variance calculation also checks the target:
the cell iterated integral (I) has variance (delta^2/2), the product
of its endpoint increments has variance (delta^2), and
(E[I\Delta B^1\Delta B^2]=\delta^2/2). Subtracting one-half of that
endpoint product yields cell variance (delta^2/4). Distinct cells are
independent, so the trapezoidal residual variance is (T^2/(4n)), matching
the original target's RMS (T/(2\sqrt n)).

The primary author-uploaded July 14, 2015 Neuenkirch-Shalaiko preprint has
Theorem 1 on printed p. 3 with positive liminf and finite limsup for
(H>1/2), for the same integral and both component observations. Its
journal metadata is J. Complexity 33 (2016), 107-117, DOI
[10.1016/j.jco.2015.09.008](https://doi.org/10.1016/j.jco.2015.09.008).
[Author-uploaded primary PDF](https://www.researchgate.net/profile/Taras-Shalaiko/publication/280310281_The_maximum_rate_of_convergence_for_the_approximation_of_the_fractional_Levy_area_at_a_single_point/links/55b14b8208aec0e5f431112a/The-maximum-rate-of-convergence-for-the-approximation-of-the-fractional-Levy-area-at-a-single-point.pdf).
This prior theorem is attribution, not a premise of the all-(H) witness
lower bound. No global novelty or current-open-status conclusion is drawn.

## Frozen independent conclusion

The complete Gaussian-witness mechanism, explicit positive constant,
finite-(n,T) quantifiers, every measurable estimator, and the full range
(H\in(1/4,1)) verify. The source/canonical interface is independently
checked at the needed convergence strength. No P0-P3 defect in the submitted
mathematical lower-bound claim was found. The false stronger remainder in
the external arXiv proof is separately documented and avoided; it does not
invalidate the needed convergence or the submitted lower bound.

This is a mathematical-scope acceptance only. It does not certify first/world
priority, an endpoint construction, exact error constants or limiting laws,
or the current status of the historical problem.
