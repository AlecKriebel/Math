# Independent mathematical rederivation

This document follows the initial independent checkpoint and reads the proposed TURN_4 certificate, but does not use inherited verdicts. It records deductions separately from finite computational evidence.

## Target and assumptions

For every fixed real lambda > 0, on nonnegative integer states (a,b,x,y), D=x+y+1 and the six transitions/rates in TURN_4 define a nonexplosive irreducible positive recurrent CTMC. Rates vanish when the coordinate decremented is zero. The seed contributes every indicated +1. Downloads preserve a+x and b+y. This review treats this exact CTMC as its target; source priority and identification are separate work. Success requires a single coercive nonnegative V with pointwise LV <= -1 off a finite set and a legitimate passage from localized Dynkin identities to finite expected hitting times. Finite tests alone cannot establish this all-state, all-real-load theorem.

## Rounded imbalance: independently derived

Let Z=a+x-b-y and W=2a+2b+x+y. Direct calculation yields LW=2 lambda-u-d and LZ=(y-x)/D. Z-changing jumps are the two arrivals and the two departures, of total rate lambda+d and increments +/-1. For h_m(z)=z^2/(2m)+m/2 on |z|<=m and |z| outside, the derivative is clipped z/m, continuous at +/-m and globally 1/m-Lipschitz. Integrating the derivative along any segment gives h(z+v)-h(z)-h'(z)v <= v^2/(2m), even when z or z+v straddles either interface and for noninteger m. Therefore the candidate bound (2) follows exactly with c/(2m)=1/8. The coefficients beta=17 lambda/8 and q=7/8 have the correct arrival and departure signs. Because |y-x|/D<1, the imbalance contribution is at most c. If Z>=m and x>=3(y+1), 2(x-y)>=D follows from x>=3y+3 (the required weaker condition is x>=3y+1), so that contribution is at most -c/2. The negative Z/small x case follows by swapping (a,x) with (b,y).

## Finite Poisson corrector: independently derived

For Q births gamma(k+1) below R and deaths k, detailed balance is gamma^k gamma(k+1)=gamma^(k+1)(k+1). Thus normalized gamma^k are invariant. The truncated mean mu_R strictly increases to gamma/(1-gamma)=theta+1: adding the mass at R+1 raises the mean because R+1 exceeds the old mean. Hence some finite integer R satisfies mu_R>theta and the second condition in (3) for every fixed real lambda>0.

Writing t_k=g(k+1)-g(k), the given formula solves gamma(k+1)t_k-k t_(k-1)=k-mu at 0<=k<R. The total centered weighted sum is zero, so at R it also gives -R t_(R-1)=R-mu. This is the terminal Poisson equation; omitting it would invalidate the proof. Each prefix centered sum is strictly negative, since the mean conditional on 0,...,k is below the full mean. Thus all t_k<0, g>=0, and g is decreasing until g(R)=0; the extension beyond R is zero. In the actual CTMC, for y<=R and b/D>=gamma, the birth rate is at least Q's birth rate, multiplying a nonpositive increment, while the death rate is at most Q's death rate, multiplying a nonnegative increment. Hence Lg(y)<=y-mu. At y=R, the upward increment is exactly zero and the terminal equation remains valid; at y=R+1 the death increment is also zero. The x statement is symmetric.

Further interface, region, and CTMC conclusion checks are in progress.

## Signed interfaces: independently rederived

Use the post-jump product identity Delta(fg)=f Delta g+g_post Delta f. At each first download D increases, its own waiting numerator decreases and the other waiting numerator is unchanged. Thus both ratio cutoffs decrease, and every interface term is nonpositive because g_post>=0. Also the affected visible corrector decreases, while the other stays fixed, so each complete J summand is nonincreasing. No upper bound on a,b or their download rates is needed.

At an arrival exactly one cutoff changes, by at most ell/D, with g unchanged; summed over the two arrival rates the interface cost is at most lambda ell G/D. At a departure D>=2 and the numerator w is fixed. If w/D>=eta, both cutoffs are saturated and the difference is zero. Otherwise w<eta D, so 0<=Delta f<=ell w/[D(D-1)]<ell eta/(D-1)<=2ell/D. There are two products, each with g_post<=G, giving at most 4ell G/D per departure. This proves (9), including D=1 because departures then have rate zero. For the coarser (10), first downloads remain nonpositive, each arrival costs at most G, and each departure at most 2G, yielding lambda G+2dG.

## Three exhaustive regions: independently rederived

I. If min(x,y)>=R+1, source g values vanish. A one-step decrease can only reach R, where g(R)=0, so all successor J values vanish as well. For x>=y, d-y=[y(x-y)+x]/D>=0, and the symmetric case gives d>=min(x,y). Thus (2) and q(R+1)>beta+c+2 imply LV<-2.

II. Suppose y<=R, x>=N. All values of J_Y at source and successors vanish. The bound d<=2y+1<=2R+1 follows by subtracting the positive quantity (2y^2+2y+1)/D from 2y+1. Since x>=3(R+1)>=3(y+1), x/D>=3/4, (x-y)/D>=1/2, and qd>=(21/32)(2y+1)>=y. The interface remainder is at most one by the chosen N. When b/D>=eta, f=1; the Poisson bound and qd>=y imply LV<=beta+c-mu+1<-3. When b/D<eta, Z=a+x-b-y>=(1-eta)x-(1+eta)y-eta>=m; the rounded slope is one, and the imbalance term is <=-c/2. If f=0, its principal term is exactly zero. Otherwise b/D>gamma, so the Poisson inequality applies; in either case f Lg(y)<=f(y-mu)<=y because mu>0 and 0<=f<=1. Hence LV<=beta-u-c/2+1=-3-u. Symmetry covers the other orientation, including the whole transition band.

III. Every remaining state has min(x,y)<=R and max(x,y)<N, so x+y<=N+R (a deliberately loose bound). Then d<=x+y, u>=(a+b)/(N+R+1), and (2),(10) imply LV<=beta+c+G[lambda+2(N+R)]-(a+b)/(N+R+1). Thus a+b>B gives LV<-1. Every state outside F belongs to one of these negative-drift cases, and F is finite. Equality at a+b=B is inside F whenever it is an integer; equality x=N is handled by II, and y=R+1 by I when the other visible count is also large.

## Real-load endpoints and limits

All constants are algebraic continuous functions of an arbitrary fixed real lambda>0 until the integer choices R,N. With beta>0, c=2beta+8>8, m=4c>0, theta=3beta+12>12, we have gamma=(theta+1)/(theta+2) in (0,1), eta in (gamma,1), ell=2(theta+2) finite, and limiting Poisson mean theta+1>theta. Existence of R needs no rational-load assumption. N and B are finite after R is fixed, since G is a finite sum with nonzero denominators. As lambda tends to infinity the thresholds diverge, which is permitted because the claim fixes lambda before choosing them. As lambda decreases to zero the algebra remains well defined; lambda=0 itself lies outside the irreducibility claim and has no positive arrival paths from the empty state. No argument exchanges either limit with the recurrence conclusion.

## CTMC construction, localization, and recurrence

Each initial or arriving peer undergoes at most two later transitions (first download and final download/departure), and arrivals occur at total constant rate lambda. On every finite time interval, the number of actual jumps is at most 2*initial_population+3*Poisson_arrivals, hence is finite almost surely. All individual state rates are finite. This establishes nonexplosion. The permanent seed makes every prescribed download/departure with a positive decremented coordinate have positive rate. From any state, a finite sequence can download and remove all peers. From the empty state, prescribed arrivals followed by the selected first downloads build any target (a,b,x,y). Each finite path has positive probability, proving irreducibility for lambda>0.

For a fully explicit localization, let T_M be the first time total population reaches M and stop at tau_F wedge t wedge T_M, with M larger than the initial population. Before stopping, only finitely many states can be visited, so stopped Dynkin is legitimate, including the one-step exit boundary. The pointwise LV<=-1 gives E[tau_F wedge t wedge T_M]<=V(s), since terminal V>=0. Nonexplosion and the pathwise population bound initial_population+arrivals ensure T_M tends to infinity almost surely. Fatou yields E[tau_F wedge t]<=V(s), then monotone convergence gives E tau_F<=V(s). No uniform integrability of terminal V is needed because it is discarded before taking limits.

For completeness, V also has linear growth and bounded jumps for each fixed load: |Z|<=population, h_m(Z)<=|Z|+m/2, J<=2G, and a jump changes W by at most 2 and h_m by at most 1. These facts provide a second integrability check if desired. The chain is locally finite: F and its exit-neighbor set are finite, and V is uniformly finite there. The standard irreducible CTMC finite-set Foster criterion applies. Equivalently, excursions from F have uniformly finite mean, exit rates on finite F are finite and positive, and a finite collection of positive-probability paths to a selected state gives finite expected numbers of such excursions; this yields a finite-mean return cycle. Holding times at any fixed state have finite positive mean. Thus the theorem is a statement about CTMC positive recurrence, not merely the embedded jump chain.

Current analytic conclusion: no mathematical gap found in the proposed certificate for the exact six-rate model. This is an independent check of the displayed deductions, subject to completing executable falsification controls. It does not certify source priority or authorize publication.
