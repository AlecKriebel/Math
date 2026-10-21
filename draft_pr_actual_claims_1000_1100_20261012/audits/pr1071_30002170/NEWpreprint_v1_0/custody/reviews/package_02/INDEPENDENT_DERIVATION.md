# Independent reconstruction before historical verdicts

Read first: the current seven-page source, Git-authenticated submitted PROOF,
ALL_H_COROLLARY and AREA_CONVENTION_CHECK. No earlier review verdict/report,
root acceptance, repair verdict or priority verdict has been read at this stage.

## Claim and success criterion

Fix one H in (1/4,1). For independent centered standard equal-H fractional
Brownian components, the canonical iterated integral I12 on [0,T] has distance
from every square-integrable function of BOTH endpoint-inclusive n-cell grids
at least c(H) T^(2H) n^(1/2-2H), for all T>0 and n>=1. We must establish c(H)>0
without treating cells as independent, demanding increment lower coercivity,
or restricting the estimator to a linear/polynomial class. This is not an
exact asymptotic limit or new-priority assertion.

## Reconstruction

1. The real subspace u(-xi)=conjugate(u(xi)) of complex L2 has real inner
product integral u conjugate(v). Define K_t=(exp(it xi)-1)|xi|^(-H-1/2)/sqrt(D).
The squared difference is |t-s|^(2H) by a single change of variables. Real
polarization supplies precisely the standard covariance, with no factor 2.
The integral D has powers 1-2H at zero and -1-2H at infinity and is strictly
positive for H in (0,1).

2. For Fourier transform with negative sign, u_h=sqrt(D)/(2pi)
|xi|^(H+1/2) conjugate(hhat) gives <K_t,u_h>=h(t)-h(0). Removing the conjugation
would give a reflected covariance path and fail the intended finite pairing.
Choose phi=x^4(1-x)^4 on [0,1] and zero outside; f=phi', g=phi. Both and their
first two derivatives have zero endpoint traces. Hence the third weak
derivatives have no endpoint point masses. A jump of f''' is harmless for
W^{3,1}. Three integrations by parts give |rhat|<=min(L_r,N_r |xi|^-3).
This proves absolute Fourier inversion and the weighted L2 integrability for
alpha=2H+1 in (3/2,3).

3. For r_j(t)=Delta^H r(t/Delta-j), the Fourier factor is
Delta^(H+1) exp(-ij Delta xi). In the u_j Gram form the total scaling is
Delta^(2H+2-alpha-1)=1. The periodized weight is bounded by a central term
pi^alpha L^2 and paired tails 2 N^2 pi^(alpha-6) sum_{l>=1}(2l-1)^(alpha-6).
The tail sum is at most 1+1/[2(5-alpha)] by a decreasing integral bound.
Parseval for a FINITE trigonometric polynomial then gives A<=M_f I and
C<=M_g I, where M_r=D Pbar_r/(2pi). This is upper Bessel control. It does
not assert any false lower coercivity for rough fBm increments.

4. u_j covariance paths vanish at every grid time. The complete Gaussian
vector (all u^f coordinates in component 1, all u^g in component 2, both
observed grids) has zero cross blocks between witness and observations.
Thus the full witness vector is independent of the full observation vector;
nonlinear estimators cause no additional issue. Set Y=sum U_j V_j. Separate
components imply E Y=0 and E Y^2=sum A_jk C_jk=tr(AC). PSD order gives
tr(AC)<=M_f tr C<=n M_f M_g, even for signed off-diagonal entries and
noncommuting A,C. Entrywise comparison would be invalid.

5. For a fixed cell j, a finite left sum L_m satisfies
E[L_m U_j V_j]=sum f_j(kT/m)[g_j((k+1)T/m)-g_j(kT/m)]. This uses only
component independence and the exact covariance identity, so it has no
stochastic integration-by-parts gap. L2 convergence of L_m, together with
U_j V_j in L2, passes the left side to the canonical integral. The ordinary
deterministic Riemann sum on the right tends to integral f_j g_j'=
Delta^(2H) a, a=integral(phi')^2>0. Hold n,T,j fixed throughout this limit.
Consequently E[I12 Y]=n a Delta^(2H). For every observed L2 F, E[FY]=0.
Cauchy--Schwarz gives exactly c=a/sqrt(M_f M_g)=2pi a/(D sqrt(Pbar_f Pbar_g)).

6. The only substantive stochastic-area bridge is canonical existence and
L2 convergence of left sums. Given analytic iterated area with Chen,
stationarity and scaling, the exact error is the sum of same/adjacent and
separated-cell covariances. Separated-cell differentiation is legitimate away
from the diagonal and produces TWO factors H(2H-1), hence nonnegative
c_r for r>=2, including the rough range. Each of the two simplex volumes
is 1/2 and both distances are at least r-1, so
0<=c_r<=H^2(2H-1)^2 (r-1)^(4H-4)/4. Bound the adjacent covariance in absolute
value by c_0; no singular diagonal kernel is integrated. The resulting
power sum vanishes after multiplication by m^(1-4H) in the rough regime,
with the log threshold H=3/4 and m^-2 in the smooth regime. At H=1/2 use
the independent-component Ito isometry directly.

7. The exact polygonal correction is Q_m=(1/2) sum Delta B1 Delta B2. Its
variance is delta^(4H)/4 times [m+2 sum (m-r) rho(r)^2], not a signed sum of
rho itself. The second-difference representation bounds rho(r) by
H|2H-1|(r-1)^(2H-2), giving the same three vanishing regimes. Hence polygonal
and analytic/left-sum targets agree. At H=1/4 the diagonal contribution is
T/4; at H=1 the normalized Fourier realization fails and the target is
endpoint-recoverable. Neither endpoint is claimed.

8. The auxiliary witness may live on an enlarged Gaussian realization.
Finite left sums and the observation vector have the same joint law there
as in the supplied fBm model. L2 limits preserve that joint law; Doob--Dynkin
applies to each L2 observed variable. Therefore the lower bound transfers
to every observed estimator without requiring the witness to be measurable
in the original probability space.

## Remaining checks, not assumed results

Confirm target wording and original convention in the OWR primary document;
verify canonical-existence/Chen interfaces in the actual NTU source, and
distinguish its v1 leading-coefficient defect from the journal-formatted
proof. Independently recompute polynomial constants and exact signed PSD,
finite pairing, correction-variance and tail identities, with mutation
controls. Confirm all seven PDF pages, exact metadata/asset identity,
all output writers and bootstrap checks, and every supplied custody mapping.
Historical novelty and complete worldwide priority remain unknown; local
source checks cannot prove their absence.
