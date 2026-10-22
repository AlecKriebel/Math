# Completed mathematical verification after the independent early freeze

The early derivation remains byte-frozen. Its last Brownian sentence said
`n^-1 RMS`; that was my exponent slip. The correct Brownian RMS order is
`n^-1/2`, exactly as the target states. The new rational projected-kernel
checks give variance `(r-1)/(4nr)` on an r-fold fine polygonal refinement,
converging to `1/(4n)`. This correction concerns the review sketch, not the
candidate. The sketch also correctly left its quantitative Gram step open;
the following direct covariance-path proof closes the needed mechanism.

## Gaussian normalization and regularity

For each fixed H in (1/4,1), the integral
`D_H = integral |exp(i xi)-1|^2 |xi|^(-1-2H) dxi` is strictly positive and
finite. The integrand is O(|xi|^(1-2H)) near zero and O(|xi|^(-1-2H)) at
infinity. On the real conjugate-symmetric subspace of complex L2(R),
`K_t=D_H^(-1/2)(exp(i t xi)-1)|xi|^(-H-1/2)` has squared increment norm
`|t-s|^(2H)`. Real polarization therefore gives exactly standard fBm
covariance, with no hidden constant or independent-component contraction.

With the negative-sign Fourier transform, the dual direction
`u_h=sqrt(D_H)/(2pi) |xi|^(H+1/2) conjugate(hhat(xi))` is real in this
Hilbert-space sense. Substituting into `<K_t,u_h>` yields `h(t)-h(0)` by
absolute Fourier inversion. Omitting the conjugation would reverse the
covariance path. This is checked algebraically, not by sampled quadrature.

Set phi=x^4(1-x)^4 on [0,1], zero elsewhere, f=phi', g=phi. Both f and g
have zero traces through derivative2, so their zero extensions lie in
W^(3,1), without third-derivative boundary masses. They need no C-infinity
regularity. Three integrations by parts give `|rhat|<=L_r` and
`|rhat(xi)|<=N_r |xi|^-3`. With alpha=2H+1 in (3/2,3), the weighted
squared transform is integrable both at zero and at infinity. Exact
polynomial integration independently yields `a=4/45045`,
`integral(phi'')^2=24/5005`, the stated endpoint traces, and the correct
positive deterministic area pairing. The original replay also checks the
three stated L1 identities. Floating values of N_f and c_H in that checker
are finite consistency checks, not interval certificates.

## The uniform Gram estimate

For |theta|<=pi, split the periodized weighted Fourier energy into its
central term and all nonzero translates. The central term is at most
`pi^alpha L_r^2`. The lth nonzero term is at most
`N_r^2 [pi(2|l|-1)]^(alpha-6)`. Since alpha-6<-3, the decreasing-series
comparison gives `sum_{l>=1}(2l-1)^(alpha-6) <= 1+1/[2(5-alpha)]`.
Both tails are present. This is exactly the candidate's Pbar_r.

For r_j(t)=Delta^H r(t/Delta-j), Fourier scaling cancels the cell width:
`2H+2-alpha-1=0`. Periodizing the nonnegative squared norm of any finite
linear combination, then applying finite trigonometric Parseval, yields
`||sum b_j u_j^r||^2 <= [D_H Pbar_r/(2pi)] sum b_j^2 = M_r sum b_j^2`.
No pointwise lower bound, interchange of signed infinite series, or lower
increment coercivity is used. Integer translation is essential to this
proof; arbitrary meshes do not follow. Telescoping unit increments prove
the tempting rough-H lower coercivity route false because its all-one
variance is n^(2H), while its diagonal sum is n.

## Canonical-area input and sufficient convergence

The independently inspected NTU institutional journal-formatted body gives
analytic area existence in Lp and Chen's relation in Proposition6 p229;
Remark10 and Theorem2 identify the linear interpolation convention. The
paper also supplies a sufficient convergence derivation that does not use
any exact Euler coefficient. Chen, stationarity and joint scaling decompose
the Euler error into m cell areas. The variance is exactly
`T^(4H)m^(-4H)[m c0+2(m-1)c1+2 sum_{r=2}^{m-1}(m-r)c_r]`.
For separated cells r>=2 the differentiated kernels are nonsingular;
component independence supplies two factors H(2H-1). The square is
nonnegative even for H<1/2, and the two triangle volumes give 1/4. Thus
`0<=c_r<=H^2(2H-1)^2(r-1)^(4H-4)/4`; stationarity and Cauchy-Schwarz
give `|c1|<=c0<infinity`. The series bound gives vanishing variance of
orders m^(1-4H), m^-2(1+log m), and m^-2 below, at, and above H=3/4.
At H=1/2 independent-component Ito isometry gives T^2/(2m).

Cellwise polygonal integration gives `P_m=L_m+Q_m` with
`Q_m=(1/2)sum Delta B1 Delta B2`. Independence makes its variance exactly
`T^(4H)m^(-4H)[m+2 sum(m-r)rho_H(r)^2]/4`. For r>=2, the integral
second-difference formula bounds rho by `H|2H-1|(r-1)^(2H-2)`;
r=1 is finite. The same three regimes show Q_m tends to zero for H>1/4.
Consequently the Euler and canonical polygonal limits coincide. This
uses no same-cell singular derivative integral and no unsupported exact
coefficient. At H=1/4 its diagonal variance is T/4, so this bridge cannot
extend to that endpoint. At H=1 the Fourier normalization diverges and
the area is recovered from endpoints; Q_m itself still tends to zero.

The specific old arXiv v1 Eq27 discards every lag beyond1 at little-o
scale. Its Eq26 gives strictly positive lag2 bounded below by
`H^2(2H-1)^2 3^(4H-4)/4` away from Brownian H. The 2(m-2) such terms
contradict the claimed little-o. The institutional journal proof retains
the near lags through log n and removes only the remaining tail. This
version distinction is essential and the current paper states it correctly.

## Universal estimator, variance, pairing, and scale

Every cell covariance path f_j,g_j vanishes at all observed grid times,
including both endpoints. The entire vector of witness coordinates and
observations is jointly Gaussian with a zero cross block. Hence the whole
witness vector, and therefore `Y=sum U_j V_j`, is independent of the whole
observation vector. Component independence gives E Y=0. This proves
E[FY]=0 for every L2 grid estimator, with no linearity restriction.

Within-component cells may have signed correlations. Their covariance
matrices satisfy `0<=A<=M_f I`, `0<=C<=M_g I`. Independent components
give `E Y^2=tr(AC)<=M_f tr(C)<=n M_f M_g`. The first inequality follows
by sandwiching `M_f I-A` with C^(1/2). Neither commuting matrices nor
nonnegative entries are needed. The new rational noncommuting signed Gram
example checks precisely this hidden-assumption boundary.

For each fixed j,n,T, the finite Euler pairing factors by component
independence into `sum f_j(t_k)[g_j(t_{k+1})-g_j(t_k)]`. L2 convergence
passes the random side to X, while ordinary Riemann-Stieltjes convergence
passes the deterministic side to `integral f_j g'_j=a Delta^(2H)`.
Only a finite sum over n follows; there is no coupled m,n limit exchange.
Thus `E[X Y]=n a Delta^(2H)`. Cauchy-Schwarz gives RMS at least
`a sqrt(n) Delta^(2H)/sqrt(M_f M_g)` which is exactly
`[2pi a/(D_H sqrt(Pbar_f Pbar_g))] T^(2H)n^(1/2-2H)`.

The constant is strictly positive and H-only, with all T>0 and n>=1
covered directly. The auxiliary Gaussian realization is sufficient:
finite sums and the observations have the same joint law as in any
original model; their L2 limits preserve it. Every grid-measurable L2
estimator is a Borel function of that finite vector modulo null sets.
The bound therefore transfers without path measurability of the witness.

The halved antisymmetric area differs by the observed endpoint product
divided by2 and has the same conditional residual. The unhalved difference
has twice its RMS residual. Brownian exact optimum and the smooth rate
remain prior. Nothing above proves novelty, a sharp constant, an exact
limit, endpoints, H-uniformity, adaptive/nonuniform information, unequal-H
or correlated-component extensions. No mathematical counterexample or
unsupported central step in the current exact theorem was found.
