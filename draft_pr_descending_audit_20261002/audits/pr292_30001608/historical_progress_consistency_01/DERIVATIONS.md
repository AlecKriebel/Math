# Independent historical mathematical audit

Scope: the exact40-file original attempt at PR292 head1198534928f4c2bf8bf758c9ceb16edaa3a496e8. The final TURN4 theorem was already independently reconstructed in my closed direct_drift_full_review_01 and accepted by ROOT. This effort checks all earlier mathematical progress and consistency; it does not establish worldwide priority or review a completed preprint. Native source/body reads and every original-file pin are in READ_SCOPE.json and the four READ_LEDGER files.

## Generator, boundary, and holding assumptions

For s=(a,b,x,y), D=x+y+1, the six rates are lambda/2,lambda/2,a(x+1)/D,b(y+1)/D,x(y+1)/D,y(x+1)/D. Zero decremented coordinates have zero rates. First downloads preserve population; departures reduce it; arrivals form a rate-lambda Poisson process. Each initial or arriving peer can make at most two nonarrival transitions. Thus actual jumps up to time t are bounded by 2N(0)+3Pi_lambda(t). This is a pathwise construction/nonexplosion argument, not an equilibrium assumption. Also total rate is at most lambda+N: each peer's nonarrival rate is at most one. These bounds justify localization and finite-time polynomial moments of N. Every finite state has finite positive holding rate for lambda>0. The permanent seed makes a prescribed finite path to zero possible; arrivals and prescribed first downloads build any target state from zero. Thus irreducibility holds for every fixed positive real lambda, including arbitrarily small lambda. The degenerate lambda0 irreducibility conclusion is excluded.

Write n=x+y,E=a+b,N=E+n, Z=a+x-b-y, W=2E+n, u=[a(x+1)+b(y+1)]/D, d=(2xy+n)/D. Independent generator calculation gives LW=2lambda-u-d, LZ=(y-x)/D, LZ²=lambda+d-2Z(x-y)/D. These agree in every historical turn and with the accepted theorem. They are coefficient identities, also checked independently by exact sparse Laurent polynomials.

## Turn1: affine low-load certificate and its limit

Choose 0<lambda<1 and 1<c<1/lambda, eta=(1-c lambda)/2. For V=cE+n,

 LV=c lambda-[(c-1)(a(x+1)+b(y+1))+2xy+n]/D.

The service bracket/D is at least [(c-1)E+n]/(n+1). If n is sufficiently large, n/(n+1)>=c lambda+eta. With n below that finite threshold R, choose K so (c-1)K/(R+1)>=c lambda+eta; E>=K then also gives negative drift. Thus LV<=-eta outside a finite set. V is nonnegative/coercive and its jumps are bounded. Stopped Dynkin on finite population sets, nonexplosion, Fatou, and a finite-set return argument yield positive recurrence. Constants depend on the fixed lambda and deteriorate at lambda1; no endpoint extrapolation is warranted.

For any positive affine coefficient certificate with pointwise negative drift outside a finite set, exchange the chunk names and average the two certificates. The averaged certificate has queue coefficient alpha and visible coefficient beta, both positive, and still negative drift outside a finite union. Along an a-only axis eventual negative drift requires alpha>beta; alpha<=beta has positive arrival drift or nonnegative service contribution. Along the x-only axis the averaged drift is lambda alpha-beta x/(x+1)>lambda alpha-beta. This is positive for lambda>=1 and alpha>beta. Therefore the specified positive affine family cannot prove the high-load conclusion. It is a family obstruction, not an instability theorem.

## Turn1: stationary balances without a population-moment assumption

Assume an invariant probability pi exists. For each integer k>=0 the bounded indicator 1_{A>k} changes only across A=k or A=k+1. Upcrossing intensity is (lambda/2)1_{A=k}; downcrossing intensity is r_A1_{A=k+1}, bounded by k+1. Under stationarity both expected crossing counts in any finite time interval are finite, compensation applies, and their means are equal. Hence

 E_pi[r_A 1_{A=k+1}]=(lambda/2)pi(A=k).

Summing this nonnegative identity over k by Tonelli gives E_pi r_A=lambda/2. The same proof gives E_pi r_B=lambda/2. For 1_{X>k}, its upcrossing intensity is r_A1_{X=k}, now integrable; downcrossing intensity r_X1_{X=k+1}<=k+1. The same finite expected crossing argument and Tonelli give E_pi r_X=E_pi r_A=lambda/2; similarly r_Y. No E_pi N assumption or unbounded-coordinate Dynkin substitution is required. Therefore

 E_pi[2XY/D]=lambda-1+E_pi[1/D],
 E_pi[(X-Y)/D]=0.

The first follows from E_pi d=lambda and n/D=1-1/D; the second from r_Y-r_X=(y-x)/D. All terms are integrable since the rates now have finite means and 1/D is bounded. Historically these were conditional necessary identities; they did not prove existence of pi. The accepted final theorem supplies existence separately. The finite checker verifies the algebra only, not the invariant-distribution argument.

## Turn2: universal algebra and low-load nonlinear certificate

Let c=2/lambda and K=3+c. For V=Z²+c(a²+b²)+KW, multiplying the actual generator by D gives P3+P2+P1+P0 with

 P3=-2c(a²x+b²y),
 P2=-2c(a²+b²)-2(x²+y²)+4(ay+bx)-3(ax+by)-2cxy,
 P1=-(a+b)+(7lambda+4-c)(x+y), P0=7lambda+6.

This is not inferred from finite load examples. My own symbolic generator expands each one-step polynomial increment with exact binomial arithmetic in (a,b,x,y,lambda), permitting only a negative power of lambda to represent c. All 21 nonzero numerator coefficients agree exactly. The same independent control checks W,Z,Z² identities and the critical ray residual.

For lambda<2, c>1 and delta=2(c-1)/(c+1)>0. Young's bound 4ay<=(c+1)a²+4y²/(c+1) leaves (c-1)a²+delta y², at least delta(a²+y²) because c-1>=delta. The symmetric pair gives P2<=-delta sum(s_i²)<=-delta N²/4; the other quadratic terms and P3 are nonpositive. Set B=max(7lambda+4-c,0), C=7lambda+6. Then D LV<=-delta N²/4+BN+C. Choose a finite integer R>=1 with R>4(B+C+2)/delta. For N>=R this is at most -(N+1), and D<=N+1 implies LV<=-1. Nonnegative/coercive V and finite-set stopping yield positive recurrence. Polynomial jumps cause no integrability difficulty after localization; N<=N0+Pi_lambda(t) gives finite-time second moments as well. No uniformity near lambda2 is claimed.

The obstruction is ONLY the family V_{c,K}=Z²+c(a²+b²)+KW, c,K>0. Along (a,b,x,y)=(t m,0,0,m), the coefficient of m² in D LV is

 F(t)=-2ct²+(lambda c+2)t-2.

Its maximum at t=(lambda c+2)/(4c) is (lambda c+2)²/(8c)-2>=lambda-2. For lambda>2 it is positive and continuity permits a rational positive t giving integer rays. At lambda2, it is positive unless c1. For lambda2,c1,t1 the exact numerator is (8+2K)m+4+4K>0. Thus no K term repairs this family at or above2. This does not rule out different quadratic families or more general nonlinear functions. The final cutoff certificate is a genuinely different mechanism.

## Turn3: local all-load estimates, not a recurrence proof

For every fixed lambda>0 choose gamma=(lambda+1)/(lambda+2), finite R with mu_R>lambda, and epsilon=mu_R+1/2-lambda>1/2. Reflecting birth-death births gamma(k+1), deaths k, stationary weights gamma^k give mu_R tending to lambda+1. Solve Qg=k-mu_R with g(R)=0, extend g=0 above R. Prefix weighted means below the full mean imply g nonnegative and strictly decreasing below R. The reflecting terminal equation at R is essential and valid; it is not an omitted endpoint condition.

In F_X={x/D>=1/2,b/D>=gamma}, actual y-birth rate >=gamma(y+1), actual death rate <=y. The sign of the increments of g therefore yields Lg(y)<=y-mu_R for y<=R, including R. Also d>=y+1/2: subtracting (y+1/2)D from 2xy+x+y gives x(y+1/2)-(y²+y/2+1/2), nonnegative when x>=y+1. The condition x/D>=1/2 means x>=y+1. Consequently L(N+g(y))<=lambda-(y+1/2)+y-mu_R=-epsilon in the sector. For y>R all g increments vanish, and R>mu_R>lambda ensures the same negative drift bound. The symmetric statement follows exactly by chunk exchange.

The diagonal ray (0,m,m,0) and its mirror are eventually in these sectors when m>=lambda+1. These are the specific rays displayed in Turn3, not a claim that every possible obstruction ray in the broader quadratic family has been covered.

Stopping at sector exit tau, localized Dynkin and nonnegative N+g give E tau<=(N0+g0)/epsilon. This proves a finite expected exit time. It does not prove entry into a compact set, negative contraction across repeated sectors, or recurrence; all these limits are expressly retained by the original turn.

For E_X={x>=K(y+1),b<gamma D}, K=2(1+gamma)/(1-gamma)=4lambda+6, v=(K-1)/(K+1)>0,

 Z>a+(1-gamma)x-(1+gamma)y-gamma>=a+(1-gamma)x/2>0,
 (x-y)/D>=(K-1)/(K+1)=v, so LZ<=-v.

On departure from the sector, one jump changes Z by at most1; Z+1 remains nonnegative until and at the stopping time. Localized stopping therefore gives E tau<=(Z0+1)/v. Since N(t)<=N0+Pi_lambda(t), compensation stopped at tau and monotone convergence give E N(tau)<=N0+lambda E tau<=N0+lambda(Z0+1)/v. No independence of tau and arrivals or stationary averaging has been assumed. This growth bound is not a contraction. The global interface gap at lambda>=2 remained explicitly open in the original turn.

## Turn4, source background, and historical narrative

TURN4 introduces W+c h_m(Z)+f(b/D)g(y)+f(a/D)g(x). First downloads have nonpositive cutoff-product errors, the reflecting Poisson bound includes its cap, and the remaining errors are O((lambda+d)/D); bounded visible population is handled separately by the queue service. Its exhaustive-region proof closes the earlier interface gap for every fixed positive real lambda. This is already independently reconstructed in my earlier frozen review, not accepted here merely because the old review/byte verifier says PASS. I have read the entire exact TURN4 and both original review programs again for historical correspondence. The old portable program was replayed unchanged and reproduces its saved finite output exactly. The large certificate constants in saved output are not estimates of actual equilibrium size or load-uniform bounds.

The old SOURCE_AUDIT correctly credits Norros, Reittu, and Eirola for the large-system ODE and unstable behavior. ROOT's current additive erratum corrects a typo confined to its closed mathematical acceptance scope_limits[1]; the original40 already spell Eirola correctly. Independent substitution gives the equilibrium curve (a,b,x,y)=(theta,lambda theta/(2theta-lambda),lambda theta/(2theta-lambda),theta), theta>lambda/2. In the open region y>a>lambda,0<x<lambda/2,b>lambda/2(1+x/y), let F=y-a and beta=b-lambda/2(1+x/y). The equations give x'<0,k'<0,beta'=-y beta/(x+y)-k' and F'=y beta/(x+y)-xF/(x+y), preserving positivity. Thus a',y'>=lambda/2-x0>0, a,y diverge while x,b remain bounded, and b decreases to lambda/2. This is credited prior large-system dynamics; the scaling has arrival Nlambda and occupancy/N at fixed time. It is not a fixed-lambda fluid proof of the stochastic theorem. The visible-zero singularity is outside this positive-coordinate region.

Original source notes and old review transparently disclose fresh HAL access failure at their historical checkpoint. The current authenticated gate supplies a fresh January2011 author-proof read. Carry forward the edition qualification: no unseen final publisher body identity, and all fixed positive lambda is a formalization of the unqualified parameterized conjecture/context, not a literal universal quote. Retain the opposite conjecture in2009 and distinguish other protocols/OWR questions. Old bounded searches and four source-PDF hashes are historical provenance, not a current exhaustive priority certificate or downloads made by this reviewer. Worldwide novelty is separately pending. No other investigator's new priority findings were consulted.

TURN_STATE, CURRENT_STATE, CURRENT_STATE_TURN3, CURRENT_STATE_TURN4, and CURRENT_STATE_ACCEPTED encode1,2,3,4,4 substantive author turns, respectively. Partial/result/proof/review phase labels are coherent. LATEST expressly points to the accepted state and keeps prior states historical; intermediate percentages are guesses, not mathematical bounds. The old manifest chain and portability change are independently authenticated by the unchanged verifier's72 checks. Assertions about earlier Git/server events and original HTTP attempts are preserved historical statements; their actual native provenance is not independently certified by reading the40 bodies or their byte hashes.

Strongest historical verified result before Turn4: global positive recurrence for0<lambda<2, conditional stationary flow identities without population moments, precise family obstructions, and all-load local sector drift/finite expected exit estimates. Turn3 had no global high-load recurrence conclusion. No earlier mathematical assertion contradicts the accepted exact-chain theorem.
