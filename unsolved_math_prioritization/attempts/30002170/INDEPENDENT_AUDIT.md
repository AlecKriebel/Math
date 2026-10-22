# Independent audit of the fractional Lévy area lower bound

Audit date: 10 October 2026 UTC. Target: rank 1239, problem 30002170, alias OWR-12013-003.

## Verdict and exact accepted scope

**ACCEPTED FOR THE FULL ORIGINAL LOWER-BOUND TARGET.** The rough-range proof establishes the claimed lower bound for the optimal conditional-expectation approximation, including every positive integer sample count. No blocking mathematical error was found. The separate all-H supplement is also accepted; its scope extension is audited in Section 10 below.

Precisely, let the two components be independent, centered, standard fractional Brownian motions with covariance

\[
R_H(s,t)=\frac12(s^{2H}+t^{2H}-|t-s|^{2H}),\qquad s,t\geq0.
\]

For each fixed \(H\in(1/4,1)\), there is \(c_H>0\) such that, for every \(T>0\) and every integer \(n\geq1\),

\[
\left\|X_T-\mathbb E[X_T\mid\mathcal G_{T,n}]\right\|_2
\geq c_HT^{2H}n^{1/2-2H},\qquad
\mathcal G_{T,n}=\sigma(B^i_{jT/n}:i=1,2;\ j=1,\ldots,n),
\]

where \(X_T=\int_0^T B^1_s\,dB^2_s\) is the canonical iterated integral. The proof actually bounds the error of every \(F\in L^2(\mathcal G_{T,n})\). The accepted rough residual is \(1/4<H<1/2\); the all-H conclusion comes from the separately identified supplement. Neither document claims a sharp constant, existence of an exact normalized-error limit, an endpoint construction, or arbitrary/adaptive sampling.

This is a mathematical audit conditional only on the explicitly identified standard Gaussian/Fourier facts and the established area-convergence theorem below. It is AI-assisted and unrefereed, not external human peer review, formal proof-assistant verification, or a global novelty certificate.

## 1. Distributed proof editions and source boundary

The original authored arguments were read completely and accepted without a mandatory mathematical correction. The distributed editions below preserve those arguments, with status wording updated after acceptance. References below to the candidate mean the proof reviewed during this audit:

- [PROOF.md](PROOF.md): 11,413 bytes; SHA-256 `95f7e49ce01784aa9e63b6a0c735230056a17cb8e37764689b630f8da71459f1`.
- [ALL_H_COROLLARY.md](ALL_H_COROLLARY.md): 3,294 bytes; SHA-256 `08c222ad9bf5451745a21d3fbb10ddceca49eefec141f0f913b32802fc1badff`.
- [AREA_CONVENTION_CHECK.md](AREA_CONVENTION_CHECK.md): 2,901 bytes; SHA-256 `13f534584f5939a3a198ae34134847376e4d0aec22b9112b9390b41cfab3d6db`. This companion source-applicability note is also accepted, as independently justified in Section 7.

The original source was independently read in extracted text and visually inspected at PDF pages 32–33, printed pages 2524–2525: Andreas Neuenkirch, “A conjecture on the optimal approximation of the fractional Lévy area,” in *Rough Paths and PDEs*, Oberwolfach Report 41/2012, [DOI 10.4171/owr/2012/41](https://doi.org/10.4171/owr/2012/41). Retained PDF: 448,314 bytes; SHA-256 `302476077b9e76aab36045af07d2d262611914ec1ae2484367ad6d10af29dcb1`. Its vector-valued conditioning includes both components; its target is the stated iterated integral, without a factor-of-two change to an antisymmetric area. Its displayed lower-bound formulation has the same rate and sample-count interpretation.

The non-elementary stochastic input is Neuenkirch–Tindel–Unterberger, *Discretizing the fractional Lévy area*, Stochastic Processes and their Applications 120 (2010), 223–254, [DOI 10.1016/j.spa.2009.10.007](https://doi.org/10.1016/j.spa.2009.10.007), [arXiv:0902.0497](https://arxiv.org/abs/0902.0497). Retained arXiv PDF: 424,962 bytes; SHA-256 `de4d91bff1cde45c02298d9f7f49f34790b6c4043232eb6ef5da999af3128ebf`. Its pages 3–4 were independently visually inspected, including equations (4)–(5), Theorem 1.1, the immediately following Brownian calculation, and the analytic-approximation convention. Pages 1–4 and the convention statement at the beginning of page 5 were also read in extracted text. The exact needed consequence is L2 convergence of the left cross sums; the equality of its analytic-approximation area with the canonical polygonal integral is explicitly checked in Section 7. The published theorem's proof is treated as an established source, not re-proved here. The retained arXiv bytes are not asserted to be journal-identical. The arXiv record lists version 1 submitted 3 February 2009; the different printed PDF date is not used to invent a new submission version.

Prior attribution was separately checked in [the author-uploaded Neuenkirch–Shalaiko text](https://www.researchgate.net/publication/280310281_The_maximum_rate_of_convergence_for_the_approximation_of_the_fractional_Levy_area_at_a_single_point). Theorem 1 assumes H greater than one half and proves positive lower liminf and finite upper limsup at the stated rate. The text expressly excludes the rough range from its increment lower-bound argument. Its journal citation is J. Complexity 33 (2016), 107–117, [DOI 10.1016/j.jco.2015.09.008](https://doi.org/10.1016/j.jco.2015.09.008). The current DOI tool open failed, so this audit retains the source gate's publisher-metadata confirmation and does not claim a newly downloaded or visually inspected journal PDF. The exact Brownian optimum is already credited by the original OWR report. None of these prior cases is presented as a new discovery.

## 2. Standard fBm normalization and Fourier signs

Let \(\mathcal K\) be the real Hilbert space of square-integrable complex functions satisfying \(u(-\xi)=\overline{u(\xi)}\). Its inner product \(\int u\overline v\) is real: the integrand at \(-\xi\) is the conjugate of the integrand at \(\xi\), and the integral is absolutely convergent by Cauchy–Schwarz.

For

\[
D_H=\int_{\mathbb R}|e^{i\xi}-1|^2|\xi|^{-1-2H}\,d\xi,
\]

the local exponent is \(1-2H>-1\) and the tail exponent is \(-1-2H<-1\) exactly when \(0<H<1\). The integrand is positive on a set of positive measure. Thus \(0<D_H<\infty\). The proposed \(K_t\) has the required conjugate symmetry. Directly,

\[
\|K_t-K_s\|^2
=D_H^{-1}\int|e^{i(t-s)\xi}-1|^2|\xi|^{-1-2H}\,d\xi
=|t-s|^{2H}.
\]

Together with \(K_0=0\), real polarization gives precisely \(R_H\). There is no hidden complex-Gaussian factor of two: the proof uses real isonormal processes with covariance equal to this real Hilbert inner product.

Using the stated Fourier transform \(\widehat h(\xi)=\int e^{-it\xi}h(t)\,dt\), the definition

\[
u_h(\xi)=\frac{\sqrt{D_H}}{2\pi}|\xi|^{H+1/2}\overline{\widehat h(\xi)}
\]

has the correct conjugation. For real h, it belongs to the real symmetry subspace. Its squared norm is

\[
\frac{D_H}{4\pi^2}\int |\xi|^{2H+1}|\widehat h(\xi)|^2\,d\xi.
\]

Since the inner product conjugates its second entry, multiplication by \(K_t\) gives \((2\pi)^{-1}(e^{it\xi}-1)\widehat h(\xi)\). Fourier inversion therefore yields \(h(t)-h(0)\), and the proposed cells have \(h(0)=0\). Every sign and the factor \(2\pi\) in the covariance identity are correct.

## 3. Membership and endpoint regularity

The zero extension of \(\phi=x^4(1-x)^4\) on \([0,1]\) is C3 and piecewise polynomial. Its first three derivatives vanish at both endpoints. For \(g=\phi\) and \(f=\phi'\), the endpoint traces of r, r', and r'' all vanish. Thus, upon differentiating the zero extensions three times distributionally, no boundary Dirac masses appear. Both functions belong to \(W^{3,1}(\mathbb R)\). A jump of \(f'''=\phi''''\) at an endpoint is allowed; the proof does not falsely assert that f is C3 there.

Three integrations by parts consequently give \(|\widehat r(\eta)|\leq\|r'''\|_1|\eta|^{-3}\), and \(|\widehat r|\leq\|r\|_1\). This proves absolute integrability of each Fourier transform. The weighted squared transform is integrable at zero because \(\alpha=2H+1>-1\), and at infinity because \(\alpha-6<-1\). In the rough interval the latter exponent is below -4; for the all-H extension it is below -3. Scaling and translating preserve all needed properties, and integer translates satisfy \(r_j(0)=0\).

The area pairing is positive without any computer calculation, since \(f=g'=\phi'\) is a nonzero polynomial on an interval:

\[
a=\int_0^1(\phi')^2>0.
\]

## 4. Uniform Gram bound and the explicit constant

For \(r_j(t)=\Delta^H r(t/\Delta-j)\), the Fourier transform is

\[
\widehat{r_j}(\xi)=\Delta^{H+1}e^{-ij\Delta\xi}\widehat r(\Delta\xi).
\]

In the Gram integral, changing variables to \(\eta=\Delta\xi\) produces the total power

\[
\Delta^{2H+2}\Delta^{-(2H+1)}\Delta^{-1}=1.
\]

The conjugation in u gives the phase \(e^{i(j-k)\eta}\), as written. A sign reversal here would leave the real quadratic form unchanged, but the candidate's written sign is in fact correct.

For \(-\pi\leq\theta\leq\pi\), the central term of the periodization is bounded by \(\pi^\alpha\|r\|_1^2\). The remaining terms satisfy

\[
|\theta+2\pi\ell|^\alpha|\widehat r(\theta+2\pi\ell)|^2
\leq\|r'''\|_1^2[\pi(2|\ell|-1)]^{\alpha-6}.
\]

Writing \(p=6-\alpha>1\), the positive decreasing function \((2x-1)^{-p}\) gives

\[
\sum_{\ell=1}^{\infty}(2\ell-1)^{-p}
\leq1+\int_1^{\infty}(2x-1)^{-p}\,dx
=1+\frac1{2(p-1)}.
\]

This is exactly the displayed constant in formula (7). The factors of two for positive/negative translates and \(2\pi\) from Parseval are both present. Nonnegative-integrand periodization and finite-polynomial Parseval then give

\[
\Big\|\sum_jb_ju_j^r\Big\|^2
\leq \frac{D_H\overline P_r}{2\pi}\sum_jb_j^2=M_r\sum_jb_j^2.
\]

All constants depend only on H and the two fixed polynomials, never on n or T. Their finiteness and positivity are established. No lower bound for arbitrary linear combinations of fBm increments is used. In particular, the known rough-range failure of such an increment bound is irrelevant to this upper Gram estimate.

## 5. Independence from both sampled components

For every cell j and grid index k, both \(f_j(k\Delta)\) and \(g_j(k\Delta)\) vanish, including the first and last grid points. Equation (4) therefore kills all same-component covariances between the witness coordinates and observations. Opposite-component covariances vanish because the isonormal processes are independent.

The finite combined vector of all witness coordinates and all observed coordinates is jointly centered Gaussian. Its block-zero covariance proves independence of the entire witness vector from the entire observation vector. It is stronger than pairwise independence, and the proof invokes the correct joint-Gaussian fact. Consequently \(Y=\sum_jU_jV_j\) is independent of \(\mathcal G_{T,n}\).

The two witness families are mutually independent, so every \(\mathbb E[U_jV_j]=0\); hence \(\mathbb E[Y]=0\). For any square-integrable measurable approximation F, integrability of FY follows by Cauchy–Schwarz and independence gives \(\mathbb E[FY]=\mathbb E[F]\mathbb E[Y]=0\). This is orthogonality to every possibly nonlinear estimator based on both components, not just to their linear span or to one quadrature rule.

## 6. Witness variance with signed correlations

The within-component covariance matrices A and C are real symmetric positive semidefinite. The Gram estimate is exactly \(A\preceq M_fI\) and \(C\preceq M_gI\). Component independence yields

\[
\mathbb E[Y^2]=\sum_{j,k}A_{jk}C_{jk}=\operatorname{tr}(AC).
\]

The trace inequality follows because \(C^{1/2}(M_fI-A)C^{1/2}\) is positive semidefinite. It does not require AC itself to be symmetric, A and C to commute, or their entries to be nonnegative. Thus

\[
\mathbb E[Y^2]\leq M_f\operatorname{tr}(C)\leq nM_fM_g.
\]

This establishes the essential square-root-n denominator while allowing correlated cells. No false claim of cell independence is made.

## 7. Covariance with the stochastic integral and L2 passage

For each fixed n, T and j, the left sum \(X_T^{(m)}\) has the stated finite covariance with \(U_jV_j\): each expectation separates into one expectation in each independent Gaussian component, and equation (4) applies to each factor. There is no within-component four-variable Wick expansion and no missing contraction term.

The exact source theorem uses the same variable \(X_T\) and the same left sum. For \(1/4<H<1/2\), its mean-square error is asymptotic to a finite coefficient times \(T^{4H}m^{1-4H}\); since \(1-4H<0\), it tends to zero. Only that convergence is imported. An error lower bound for the Euler rule would not by itself lower-bound the optimal estimator; the present argument never makes that invalid inference.

The source's analytic-approximation convention needs an explicit identification with the canonical polygonal convention. Let \(P_m\) be the ordinary integral of the two piecewise linear interpolations on the m-cell grid, and \(L_m=X_T^{(m)}\). Direct integration of a linear function on each cell gives

\[
P_m-L_m=Q_m=\frac12\sum_{k=0}^{m-1}\Delta_kB^1\Delta_kB^2.
\]

Writing \(\delta=T/m\) and

\[
\rho_H(r)=\frac12\bigl(|r+1|^{2H}+|r-1|^{2H}-2|r|^{2H}\bigr),
\]

the independent-component covariance identity gives exactly

\[
\mathbb E[Q_m^2]
=\frac{\delta^{4H}}4\left[m+2\sum_{r=1}^{m-1}(m-r)\rho_H(r)^2\right].
\]

For r at least 2, the second-difference integral formula bounds \(|\rho_H(r)|\) by a constant depending on H times \(r^{2H-2}\). The lag 1 term is finite; at H=1/2 all nonzero lags vanish. Summing \(r^{4H-4}\) proves mean-square bounds of orders \(T^{4H}m^{1-4H}\) for \(1/4<H<3/4\), \(T^3m^{-2}(1+\log m)\) at H=3/4, and \(T^{4H}m^{-2}\) for \(3/4<H<1\). Each tends to zero. Therefore \(P_m-L_m\to0\) in L2, so the source theorem's limit equals the polygonal limit, including the dyadic subsequence defining the canonical lift. This independently verifies the companion convention note and rules out an unproved change of stochastic integral. The factor one half is the cell's linear-interpolation correction, not an antisymmetric-area renormalization.

Because \(U_jV_j\in L^2\), Cauchy–Schwarz allows passage from \(\mathbb E[X_T^{(m)}U_jV_j]\) to \(\mathbb E[X_TU_jV_j]\). On the deterministic side, write each increment of g as the integral of its continuous derivative. Uniform continuity of f on \([0,T]\) then bounds the discrepancy from \(\int f_jg_j'\) by its mesh modulus of continuity times \(\int|g_j'|\), which tends to zero. Thus the limiting pairing is an ordinary deterministic integral.

Substitution \(t=\Delta(x+j)\) gives the independent scaling check

\[
\int_0^Tf_j(t)g_j'(t)\,dt
=\Delta^H\Delta^{H-1}\Delta\int_0^1f(x)g'(x)\,dx
=a\Delta^{2H}.
\]

There are n complete cells, with no endpoint-cell loss, so \(\mathbb E[X_TY]=na\Delta^{2H}\). All limiting operations hold with n fixed; a uniform-in-n exchange of limits is neither used nor needed.

## 8. Validity of the auxiliary Gaussian realization

The witness need not be measurable with respect to the original path. This is legitimate, and the candidate explicitly recognizes it. Here is a precise law-transfer justification.

On the auxiliary realization, the finite-dimensional distributions of the two fBm components agree with the original ones. Hence, for every m and m', the joint distributions of the observations and \((X_T^{(m)},X_T^{(m')})\) agree. Since the original sequence is L2 Cauchy, so is the represented sequence. Define its L2 limit on the represented probability space. Taking the joint distributional limit together with the fixed finite observation vector proves equality of the joint laws of the observations and the target area.

The minimum of \(\mathbb E[(X-f(Z))^2]\) over Borel functions f of a finite observation vector Z depends only on this joint law. Completion of the observation sigma-field changes nothing modulo null sets. It therefore suffices to prove the lower bound on the enlarged Gaussian realization. Extra independent Gaussian directions can change the witness norm but cannot invalidate Cauchy–Schwarz or the joint-law argument. No assumption that the chosen Hilbert representation is minimal is required.

## 9. Final exponent and finite sample counts

Combining exact covariance, orthogonality to F, and the variance upper bound gives

\[
na\Delta^{2H}
=\mathbb E[(X_T-F)Y]
\leq\|X_T-F\|_2\sqrt{nM_fM_g}.
\]

Therefore

\[
\|X_T-F\|_2\geq\frac{a}{\sqrt{M_fM_g}}\sqrt n(T/n)^{2H}
=\frac{2\pi a}{D_H\sqrt{\overline P_f\overline P_g}}
T^{2H}n^{1/2-2H}.
\]

The candidate's exponent, scale factor, RMS interpretation, and constant are all correct. No step requires n large, n even, or a dyadic grid. In particular n=1 gives one nontrivial cell whose two endpoint covariances vanish. T is any positive real number. Conditional expectation is in L2 because the source theorem gives \(X_T\in L^2\), and its optimality follows from the standard orthogonal-projection property.

## 10. Separate audit of the all-H supplement

The supplement changes only the allowed H interval; the rough-range mathematical argument remains unchanged. For \(1/4<H<1\), one has \(3/2<\alpha<3\). The weighted Fourier tail has exponent \(\alpha-6<-3\), the series estimate remains valid, and \(5-\alpha>2\). The harmonic normalization requires only \(0<H<1\). Every algebraic, independence, variance and scaling step is unchanged. In particular the same formula (15) gives a positive finite constant for every fixed H in this larger interval.

The inspected NTU page 3 supplies the only additional stochastic input:

- For \(1/2<H<3/4\), the mean-square Euler error tends to zero as \(m^{1-4H}\).
- At \(H=3/4\), it tends to zero as \(m^{-2}\log m\).
- For \(3/4<H<1\), it tends to zero as \(m^{-2}\).
- At \(H=1/2\), the displayed exact Euler mean-square error is \(T^2/(2m)\), which tends to zero. This Euler error is distinct from the smaller conditional-expectation optimum \(T^2/(4m)\).

Accordingly the all-H, all-n statement is proved directly. It is not obtained by assuming that a positive asymptotic lower limit automatically controls finitely many initial n. The source problem's demanded positive lower constant is also weaker than the exact limiting-constant conjecture stated elsewhere in the NTU article; the accepted result does not claim that stronger limit.

The smooth-H optimal asymptotic rate and Brownian exact case remain prior results. The candidate's treatment of those intervals supplies explicit finite-n coverage within this argument, without assigning new priority to known cases.

## 11. Exclusions and final acceptance

No claim is accepted at H=1/4: the canonical L2 area convergence used here is unavailable there, irrespective of other renormalized constructions. H=1 is also outside scope and makes the displayed harmonic normalization divergent. There is no H-uniform positive constant near either endpoint. The audit accepts no arbitrary-mesh, adaptive-information, unequal-H, correlated-component, or alternative-area-normalization extension.

No blocking changes are requested. The proof and supplement may be treated as mathematically accepted for their stated mathematical scope, subject to the ordinary reliance on the cited established L2 convergence theorem. Any later mathematical edit requires review against its own content and hash.
