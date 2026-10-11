# Fresh complete adversary: sealed criterion and independent reconstruction

Written 2026-10-01 UTC before reading root, sibling, historical reviewer,
scripts, results, manifests, corpus, or workflow receipts. This is the
initial reconstruction and acceptance criterion, not a final verdict.
I have read current operative README, SOURCE_AUDIT and
CURRENT_EXTERNAL_PROOF_SCOPE. They explicitly mention previous PASSs.
Independence means independent of their evidence, not blind to existence.
Fresh primary PDFs and pages were retrieved to ignored tmp/sources and are
bound by SOURCE_RECEIPTS.json. Only root/nested AGENTS and read-only Git
branch/status/remote metadata have otherwise been inspected.

## Exact claim and criterion

The literal 2013 post defines G_R with iid N(0,1/N), G_C with component
variances 1/(2N), and alpha_K(N)=E(N^-1 sum singular values of G_K).
Its scalar complex calculation removes the notation's ambiguity. The
MIT2015 Open Problem 1.2 states both non-strict inequalities for every
integer N>=1, p=n. Equivalently, for X_R having iid variance-one real
Gaussian entries and X_C iid circular complex entries with E|X_ij|^2=1,
alpha_K(N)=N^-3/2 ETr(XX*)^(1/2). Required: alpha_R(N+1)>=alpha_R(N)
and alpha_C(N+1)<=alpha_C(N), all N>=1. Strict external results suffice.
No rectangular, continuous-shape, moment-sign diagram, crossing or
transition result is required or promoted. N=1, parity, hard edge,
normalization, infinite-tail interchanges, initial conditions, asymptotic
constant, and imported decrement estimate are mandatory boundaries.

PASS requires: (i) an analytic, noncircular complete square proof from the
actual versioned bodies and independent reconstructable dependencies;
(ii) exact identification of 2800102/AMR-027-0102, original head and sixteen
bytes, current twenty-three bytes, source/prior payloads, historical and
current status/budget, and bounded duplicate/priority evidence; (iii)
isolated reproducibility of all submitted/historical and four family
scripts, scrutiny of their actual code, manifests, seals and limitations;
(iv) no unsupported priority, human review, proof-assistant, campaign
novelty, paper/DOI, or acceptance/integration claim. A statement of a
theorem, finite extrapolation, or reduction to an unsupported equally
hard lemma is insufficient. Review validates external work and must not
consume/reset the original 0/5 proof-search budget. Parent owns remote
integration and later accepted mirror, which remain outside this review.

## Gaussian law and finite density route

SVD change of variables for a real N by N Gaussian matrix gives ordered
eigenvalue density proportional to prod x_i^-1/2 exp(-x_i/2) prod_{i<j}
(x_j-x_i); complex gives prod exp(-x_i) prod_{i<j}(x_j-x_i)^2.
The real hard edge exponent -1/2 is integrable, and exponential decay
controls every polynomial moment. This is the square lambda=0 LOE/LUE,
with no continuous-shape inference needed. Let f_j(x)=x^j x^-1/2
exp(-x/2). Form M_ij=double integral sign(y-x)f_i(x)f_j(y) dxdy. De Bruijn
integration of the Vandermonde determinant gives its Pfaffian partition
function. For odd N append b_i=integral f_i and a zero corner. Functional
differentiation of the Pfaffian under w->w(1+t h) gives the counting
density from the inverse skew matrix; the odd border contributes an
extra single-weight term. This derivation does not assume the displayed
LOE density. It yields a finite exact target against which that density
must be verified for BOTH parities, with integral N and correct trace
moment. The real paper's citation is a dependency, not a free certificate.

Its square normalized density formula is
p_R=p_C-[Gamma((N+1)/2)/(2N Gamma(N/2))] L_(N-1)(Phi1-Phi2),
where epsilon=N mod2, Phi1=e^-x sum_{m=0}^{(N+epsilon-2)/2}
[2 Gamma(m+1-epsilon/2)/Gamma(m+3/2-epsilon/2)] L_(2m+1-epsilon),
and Phi2=(x/2)^-1/2 e^-x/2[(1-epsilon)2 Gamma(1/2,x/2)/Gamma(1/2)
+2epsilon-1]. The factor 1/2 is the x=2y Jacobian. The resulting
alpha_R=alpha_C-Xi has Xi=(Gamma((N+1)/2)/(2N^1.5 Gamma(N/2)))J.
Testing only even N or changing the variance while keeping the formula
would be a false acceptance. At N=1 the border is the whole law.

## Abel completion and positive diagonal mechanism

Let sigma_j=[z^j]sqrt(1-z), b_j=-sigma_j>0 for j>=1,
h_r=Gamma(r+3/2)/r!, and Q(r,s)=integral sqrt(x)e^-x L_r L_s.
The finite Laguerre connection to parameter 1/2 proves
Q(r,s)=sum_{j<=min(r,s)} sigma_(r-j)sigma_(s-j)h_j.
Fourier coefficients of |1-e^(i theta)| prove
b_d-sum_{t>=1}b_t b_(t+d)=kappa_d=1/[pi(d^2-1/4)]>0.
The beta representation b_n=pi^-1 integral_0^1 t^(n-3/2)(1-t)^1/2 dt,
Tonelli, and tB'(t)=t/(2sqrt(1-t)) give
sum t b_t b_(t+d)=1/[pi(2d+1)]. Thus
-Q(r,r+d)/h_r=kappa_d+sum_{t=1}^r(1-h_(r-t)/h_r)b_t b_(t+d)
+sum_{t>r}b_t b_(t+d)>0. Ratios h_(r-t)/h_r increase with r,
so this kernel decreases with r. These are universal identities.

For an Abel parameter 0<zeta<1 the parity sum of Laguerre generators
is integrated against (1-z^2)^(omega-1), omega=1/2 at square.
For a monomial x^j in the fixed L_(N-1), the integrated ABSOLUTE value
of either signed branch equals a positive Gamma integral with scale
1/(1 +/- zeta z). It is bounded by a constant times
(1-z^2)^(omega-1)(1+z)^(j+1/2), uniformly in zeta. This majorant is
integrable, including omega=1/2. Hence Fubini and dominated convergence
are justified without cancellations. The boundary incomplete-gamma
formula then cancels the finite parity initial segment. For fixed r,
Q(r,s)=O_r(s^-3/2) by its finite connection sum, while w_m=O(m^-1/2),
so the tail is O(m^-2) absolutely, an ordinary series as well as its Abel
limit. Positivity alone would not justify signed-series interchanges.

Reindexing gives Xi_N=sum_{u>=1} A_(N,u) K_(N-1,u), K>0 and decreasing
in its first argument. At square
A_(N,u)=sqrt(2)N^-3/2 G(N/2)(N/2)_u/((N+1)/2)_u,
G(x)=Gamma(x+1/4)Gamma(x+3/4)/(Gamma(x)Gamma(x+1/2)).
Its adjacent ratio is (N/(N+1))^1.5(2N+1)/(2N)
prod_{j=0}^{u-1}(N+2j+1)^2/[(N+2j)(N+2j+2)]. Required: strict
N/(N+1)<ratio<1 for all u and the first-diagonal reserve. The printed
proof obtains the upper bound for N>=3 by auxiliary lambda=1 comparison;
any continuous-shape auxiliary must be checked or replaced by a square
proof, never accepted merely because a broader theorem is stated.

For u=1, A_(N,1)=q(N/2)/(N+1), q=G/sqrt(x), and
g(x)=(log G)'=integral_0^infinity e^-xt/(1+e^-t/4)dt>1/(2x),
so q increases. q(3/2)=(15/16)sqrt(pi/3)>15/16.
The exact ratio for u=1 is (2N+1)sqrt(N+1)/(2sqrt(N)(N+2))
<1-1/(2N) for N>=3, by 4N^3-4N^2-13N+4>0.
kappa_2=4/(15pi) then gives Xi_N-Xi_(N+1)>1/[8pi N(N+1)].
After the AP bound below, N>=4 follows from H_N+6log2-10/3<3N/4,
based at H_4 and log2<7/10. The reserve is >1/(160N^2).
N=3 uses the exact first-diagonal estimate; N=1,2 need independently
integrated radical/pi expressions and rational enclosures. No floating
point small-case sign may serve as an analytic certificate.

## Complex density, recurrence, sign and complete decrement dependency

Orthogonality and the determinant joint law give counting density
rho_N=e^-x sum_{k=0}^{N-1}L_k(x)^2. Let Y_N=N^1.5 alpha_C(N),
u_n=pi^-1/2 integral sqrt(x)e^-x L_n^2. The same finite connection
gives U(z)=sum u_n z^n=(1/2)(1-z)^-3/2 F(z),
F=_2F1(-1/2,-1/2;1;z). Thus Y generating function is
sqrt(pi)z(1-z)^-5/2 F(z)/2. F solves z(1-z)F''+F'-F/4=0.
Substitution proves Y_(n+1)-2Y_n+Y_(n-1)=3Y_n/(4n^2), Y_0=0,
Y_1=sqrt(pi)/2. This avoids relying on unsupported Carlson continuation
or on the withdrawn 2016 Lemma1. Normalizing this exact recurrence,
the scalar fourth-order binomial remainder
(1+x)^1.5+(1-x)^1.5-2-(3/4)x^2>0 on 0<x<=1 gives the complex
decrement induction. BD's printed 'any x>=0' is invalid as a real-domain
statement; only x=1/N in [0,1] is used. The x=1 series is absolutely
convergent, with a strictly positive fourth-order term.

The real proof needs more than that sign. AP's all-n bound is
0<Delta_n<(H_n+6log2-10/3)/[8pi n^1.5(n+1)^1.5].
Its generating function has no singularity on the unit circle except 1,
is analytic on the slit plane C\[1,infinity), and admits a Delta-domain.
F(1-t)=4/pi-t/pi+[t^2/(16pi)](8log2-5)-[t^2/(8pi)]log t
+O(t^3 log t) in closed subsectors. Multiplication by z(1-z)^-5/2,
Gamma/digamma coefficient extraction and Delta-domain transfer give
alpha_C(n)=8/(3pi)+(log n+gamma+6log2-17/6)/(16pi n^2)
+O(log n/n^4), once the odd inverse powers are eliminated by the
recurrence. At expansion index j the multiplier j(j-2) is nonzero for
odd j; use arbitrarily deep transfer remainders BEFORE comparing
coefficients, so recurrence substitution is legitimate. In particular
Delta_n=(log n+C0)/(8pi n^3)+O(log n/n^4),
C0=gamma+6log2-10/3. The needed E_n limit is C0 for
E_n=8pi n^1.5(n+1)^1.5 Delta_n-log n.

Put q_d=(d+2)^1.5-2(d+1)^1.5+d^1.5-3/[4sqrt(d+1)].
The exact recurrence gives E_d-E_(d-1)=8pi q_(d-1)Y_d-log(d/(d-1)).
Convexity of 1/sqrt(x) against the triangular second-difference kernel
gives q_d>0. Positive F coefficients plus F(1)=4/pi, and strict Gamma
log-convexity, give alpha_C(d)<(8/(3pi))(d+1/2)/d without assuming
monotonicity. AP Lemma6's coefficient proof actually proves its scalar
inequality for all 0<t<1. Even coefficients are compared using
lambda_j=(128/3) binom(3/2,2j+4), lambda_(j+1)/lambda_j<
(j+1)/(j+2) for j>=3; odd coefficients of -log(1-t)/(t(1+t/2))
are nonnegative. Initial coefficients 0,2,4 are exact and strict at2.
Therefore t=1/2 covers q_1, omitted by the stated d>=2 domain.
Together these prove E_n strictly decreases to C0, hence the lower
Delta bound and alpha_C(n)>8/(3pi). The positive q_(d-1) binomial
series gives q_(d-1)>3/(64d^2.5); hence 8pi q_(d-1)Y_d>1/d.
Telescoping E_(d-1)-E_d<log(d/(d-1))-1/d to the established limit
gives E_n-C0<H_n-log n-gamma, exactly the upper bound required.
No monotonicity or upper bound is assumed in proving its own input.

## Planned materially distinct challenges

After sealing, compare the new square Gamma-product and Gaussian
angular/arctangent routes with this independent reconstruction. Use new
controls based on symbolic differential identities and arbitrary linear
test-function Pfaffian variations, endpoint/normalization mutations,
complex generating-function singular coefficients, and all-N inequality
polynomials. Read actual scripts to identify overlap before claiming a
new mechanism. All finite diagnostics will be labeled bounded; Decimal
point samples are not interval proofs. Full byte/history/source/workflow
acceptance and isolated execution are required before a final PASS.
