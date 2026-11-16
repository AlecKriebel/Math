# Independent source-first derivations and actual controls — 23393139

These deductions were completed from the actual manuscript before supplied code/results, archived audit opinions, current root/peer findings or new foreign bodies. The author's printed proof was necessarily visible; this is an independent reconstruction of that proof and its domain, not a claim of blindness to the manuscript. No scientific program or numerical simulation was used.

## 1. Exact area map and parameter reduction

At a point off the finitely many sites, all quantities in the influence comparison are positive. Taking the positive beta-th root gives
z_i^(alpha/beta)/|y-x_i| >= z_j^(alpha/beta)/|y-x_j|,
equivalently |y-x_i| <= (z_i/z_j)^q |y-x_j|, q=alpha/beta.
Squaring gives the pairwise inequality F_lambda<=0 with lambda=(z_i/z_j)^(2q). Thus A is identical, not just orbit-equivalent, for equal q values. Because the subtraction -z_i is also identical, the ODE has no induced time change.

For distinct sites a,b, the quadratic
F_lambda=(1-lambda)|y|^2-2(a-lambda b).y+|a|^2-lambda|b|^2
has a nonconstant line as zero set if lambda=1. If lambda!=1, its circle radius is sqrt(lambda)|a-b|/|1-lambda|>0. Its zero set is planar-null. A finite union of pairwise ties and site points is null, so almost every point has exactly one winner; sum_i A_i=area(D)=1 and 0<=A_i<=1. Strict comparisons at each such point persist under sufficiently small positive weight perturbations; dominated convergence proves area continuity. Unit area, finiteness and distinctness are all being used.

## 2. Local Lipschitz estimate, including equal weights

Let v=(1-lambda)y-a+lambda b and d=|a-b|. Expanding both sides gives the exact identity
|v|^2=(1-lambda)F_lambda+lambda d^2,
hence |grad F_lambda|^2=4[(1-lambda)F_lambda+lambda d^2].
This identity does not divide by 1-lambda.

Choose a compact parameter interval [m,M] with m>0 and H=max(1,|1-m|,|1-M|). If |F_lambda|<=epsilon<=m d^2/(2H), then
|grad F_lambda|^2>=4(m d^2-H epsilon)>=2m d^2.
At least one of its two coordinate derivatives has magnitude >=g=sqrt(m)d.

For a fixed second coordinate, the first-coordinate derivative is affine. The region where it is >=g is an interval, and the region where it is <=-g is another interval; each has fixed derivative sign. On either piece the preimage of [-epsilon,epsilon] has length <=2epsilon/g by the one-dimensional mean-value/integration bound. Thus the first-coordinate part of the band has area <=4epsilon/g. The same estimate holds for the other coordinate. The band is covered by those two parts, so its total area is <=8epsilon/g. Clipping each slice to [0,1] only decreases length. The coordinate supplying the derivative may vary with the point; the union/Fubini argument, rather than a fixed global coordinate, handles that.

When two dominance tests at lambda and mu differ,
|F_lambda|<=|F_lambda-F_mu|=|lambda-mu||y-b|^2<=2|lambda-mu|.
For sufficiently close parameters the preceding band estimate applies with epsilon=2|lambda-mu|, giving symmetric-difference area <=16|lambda-mu|/g. Finite intersections have symmetric difference contained in the union of their pairwise symmetric differences. On any sufficiently small positive-state neighborhood each smooth ratio (z_i/z_j)^(2q) is Lipschitz and lies in a compact positive interval. Summing over finitely many competitors proves local Lipschitz continuity of every A_i, including lambda=1, without assuming any fixed cell combinatorics.

Completed line-case hand control: a=(1/4,1/2), b=(3/4,1/2), lambda=1 gives F_1(y)=y_1-1/2, d=1/2 and |grad F_1|^2=1=4d^2. The exact area of its epsilon band is 2epsilon for 0<=epsilon<=1/2. With m=M=1, the displayed valid small-band threshold is epsilon<=1/8, g=1/2 and the claimed upper bound is 16epsilon, which safely contains the exact value. The equal-weight case is not a hidden singularity. The bound need not be sharp. As m tends to zero it is not uniform, so this argument supplies no closed-zero-weight Lipschitz claim.

## 3. Positive simplex and global classical solution

Local Lipschitz continuity of A-z on the open positive orthant gives the standard local existence/uniqueness theorem. Along the local solution, sum z_i satisfies s'=1-s, whence s=1 for normalized initial data. Since A_i>=0, differentiation of e^t z_i gives a nonnegative derivative, so z_i(t)>=e^(-t)z_i(0)>0 while the solution exists. Positive coordinates summing to one also give z_i<=1 and |z_i'|<=1.

If the maximal positive solution had finite endpoint T, then for all t<T every coordinate lies in [e^(-T)z_i(0),1]. This compact set is inside the positive orthant. The derivative bound makes z(t) uniformly Lipschitz in time, hence Cauchy at T; its limit is positive and normalized. The local theorem at that limit extends the solution, contradicting maximality. Therefore the trajectory is global, unique and classical. No p<1 assumption entered this part.

The weaker e^(-t) bound alone tends to zero and cannot establish uniform persistence. This separates finite-time continuation from the stronger asymptotic assertion.

## 4. Protected neighborhood against every competitor

Take any h_i satisfying BOTH the domain square condition and all pairwise 8h_i^2<=d_ij^2. They exist because there are finitely many distinct interior sites. For z in the positive simplex, 0<z_i^q<=1, so
Q_i=x_i+[-h_i z_i^q,h_i z_i^q]^2
lies in D and has area 4h_i^2 z_i^(2q).

For every y in Q_i and every j!=i,
|y-x_i|<=sqrt(2)h_i z_i^q,
|y-x_j|>=d_ij-|y-x_i|>=sqrt(2)h_i(2-z_i^q)>=sqrt(2)h_i.
Thus |y-x_i|<=z_i^q|y-x_j|<=(z_i/z_j)^q|y-x_j|, since z_j<=1. This is simultaneous dominance over the entire finite competitor set, not a nearest-site-only argument. Therefore Q_i is inside the actual winning cell apart from irrelevant null conventions, and
A_i>=K_i z_i^p, K_i=4h_i^2, p=2q.
No knowledge of global cell shape or connectedness is required.

For consistency, the original unscaled squares also cannot overlap in positive area: for any pair, sqrt(2)(h_i+h_j)<=d_ij follows by applying each site's geometric bound to that pair. Thus sum K_i<=1. Each K_i<1 for n>=2 and strictly interior sites. The forthcoming asymptotic lower constants are consequently compatible with normalization. This consistency observation is a hand check, not a replacement hypothesis.

## 5. Scalar comparison and exact all-time bounds

For 0<p<1 put r=1-p>0 and u_i=z_i^r. Direct differentiation and the previous actual-cell inequality give
u_i'=r z_i^(-p)(A_i-z_i)>=r(K_i-u_i).
Therefore (e^(rt)u_i)' >=r K_i e^(rt). Integrating from zero gives
u_i(t)>=K_i+(u_i(0)-K_i)e^(-rt).
This is a positive convex combination of K_i and u_i(0), even when the starting value lies below K_i. The inverse power 1/r is increasing; raising both sides gives the exact stated quantitative bound. Its minimum over t>=0 is min(z_i(0),K_i^(1/r))=eta_i, and its limit is K_i^(1/r), so liminf z_i>=K_i^(1/r) without assuming a limit. Sum the OTHER coordinates' eta bounds and use normalization to obtain z_i<=1-sum_(j!=i)eta_j<1.

Completed sign/control check: if z_i(0)^r<K_i, the scalar comparison increases; if it is >K_i, it decreases. Neither sign invalidates the convex-combination argument. At equality it is constant. Differentiating the exact scalar lower function gives w'=K_i w^p-w, so its integrating-factor formula is internally consistent. When p=1, r=0 and the substitution becomes the constant 1; the original argument cannot yield an asymptotic positive floor. For p>1, multiplying by r reverses the inequality and the inverse power is decreasing. The theorem does not export its p<1 conclusion across that boundary. As p tends to 1 from below, K_i^(1/(1-p)) tends to zero for K_i<1, so the bound is not uniformly positive in that limiting parameter.

## 6. Exact asymmetric witness, all arithmetic by hand

The coordinate differences are
x_2-x_1=(11/20,1/12),
x_3-x_1=(1/5,11/20),
x_3-x_2=(-7/20,7/15).
Squaring and adding gives respectively:
121/400+1/144=(1089+25)/3600=557/1800;
1/25+121/400=137/400;
49/400+49/225=49/144.
All exceed 1/32. All are distinct; in particular 137/400-49/144=1/450, and 49/144-557/1800=37/1200>0.

The orientation determinant is (11/20)(11/20)-(1/12)(1/5)=121/400-1/60=343/1200, nonzero. Thus the triangle is scalene/noncollinear, with no symmetric-equilibrium-only interpretation. The minimum distance of any listed site coordinate to a side of D is 1/5>1/16, so each h-square is strictly interior. Initial shares sum to 1 and are positive.

With h_i=1/16, 8h_i^2=1/32, K_i=4/256=1/64. With alpha=2,beta=8, q=1/4,p=1/2,r=1/2, K_i^(1/r)=(1/64)^2=1/4096. Every initial share exceeds it, so each eta_i=1/4096. The upper bound is 1-2/4096=2047/2048. Substitution into the proved comparison gives the stronger explicit lower function [1/64+(sqrt(z_i(0))-1/64)e^(-t/2)]^2, hence the published looser constant range for every t, without sampling.

## 7. Literal counterclaim and overlap interface, not yet externally authenticated

If the original 2007 clause really states collapse for alpha>1 with all beta>0 in this same fixed-city equation, the just-proved upper bound excludes z_i(t)->1 for every coordinate on the nonempty open region alpha>1,beta>2alpha. The theorem holds for every distinct interior configuration and positive normalized initial state there; a conventional genericity restriction deleting only lower-dimensional or null exceptional data cannot remove all such examples. The manuscript's caveat that general position is undefined must remain. This implication is mathematically complete CONDITIONAL on the exact original source wording/domain. It is not a refutation of a different stochastic founding process.

Independent conditional derivation of the credited overlap: suppose Ferudun's actual symmetric two-city map has f(1/2)=1/2 and the stated derivative f'(1/2)=p(a+1/(12a)), with a=1/4 admitted. Then the derivative is 7p/12. For 0<p<1, F(z)=f(z)-z has F(1/2)=0 and F'(1/2)=7p/12-1<0. By differentiability, sufficiently near but distinct endpoints L<1/2<R have F(L)>0 and F(R)<0. They trap the one-dimensional flow in [L,R], so collapse is excluded for initial states inside. Continuity in site positions preserves strict endpoint signs on an open nearby position set. Choosing any alpha>1 and beta=2alpha/p gives overlap with the manuscript's regime, with no time change. This is a qualitative local two-city basin, not the all-site/all-positive-initial-state quantitative theorem. Actual lemma hypotheses, symmetric configuration and continuity statement remain to be read; source-reported assertions alone are not external verification.

## 8. Hypothesis attacks and model limits

Coincident sites with equal weights would have F identically zero, ties of positive area and the naive >= cells both equal D, destroying the partition sum. Distinctness is material. Boundary sites cannot support a full positive h-square in D under the stated construction; the theorem does not claim them. Zero shares are outside smooth ratio and positive-power differentiation domains; delayed/nonunique boundary behavior is not addressed. The n=1 trivial model is deliberately excluded from the noncollapse counterexample.

The deterministic fixed-city model assumes hard maximal influence, uniform area measure, finite fixed sites and normalized relaxation. The exponent 2q comes from planar area of a linearly scaled neighborhood, not from empirical population data. No convergence, unique positive equilibrium, initial-value-independent limit, city creation, stochastic process theorem, calibrated exponent or real-world prediction follows merely from these bounds.

## Source-first outcome

C1-C3 and C6 have complete checkable deductions and actual hand controls here. No core analytic defect found. Full original C4/C5 attribution/model/overlap claims still require the finite actual-primary-interface pass. No native checker, old audit/replay/builder or new scientific program was executed, and no numerical evidence was mistaken for the universal proof. Preserve this result before any such exposure; do not extend a defect into a repair route.
