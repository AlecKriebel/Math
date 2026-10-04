# Independent mathematical seal (before candidate access)

Time: 2026-10-03 07:48 UTC (UTC minute estimate; exact chronological tool timestamps are recorded in research log). Target snapshot: c683fc4b84266a6a153c087e182cf427ed502d6c. This seal precedes candidate, author-code and earlier-review access.

## Exact target

For symmetric measurable W:[0,1]^2->[0,1], edge density p=int W and induced probability
P(W)=3 int W12 W23 W34 W41 (1-W13)(1-W24).
The factor 3 counts the 4!/8 labeled copies of C4. The unrestricted goal at p>1/2 is to maximize this over all graphons; a local or rank-one result is strictly narrower.

## Rank-one deduction, all measurable f

Let W(x,y)=f(x)f(y), X=f(U), 0<=X<=1, m=E X=sqrt(p), a=E X^2, b=E X^3. Direct expansion gives P=3(a^2-b^2)^2. Cauchy-Schwarz applied to X^(1/2), X^(3/2) gives b>=a^2/m for m>0; m^2<=a<=m. Since a>=b>=0, P<=3[a^2-a^4/m^2]^2. Setting c=a/m in [m,1], the unsquared nonnegative expression is m^2 c^2(1-c^2).

Consequently the exact rank-one profile is 3p^2/16 for 0<=p<=1/2 and 3p^4(1-p)^2 for 1/2<=p<=1. For 0<p<1/2 equality requires X in {0,1/sqrt(2)}, with positive mass sqrt(2p); at p>=1/2 equality requires X=sqrt(p) almost surely. At p=0 and p=1, the mean forces respectively X=0 or X=1 a.s. At junction p=1/2 the two descriptions coincide. This proof is universal; finite distributions test implementation only.

Strict comparison: at p in (0,1/2], the unrestricted attainable value 3p^2/2 is eight times larger. For p in [1/2,1), complete multipartite probability 3[(sum a_i^2)^2-sum a_i^4] is at least 3p(1-p)^2? That last inequality is NOT established and is not assumed: the LMR quantity is an upper bound with equality at knots. A sufficient independently checkable lower comparison is any complete bipartite contribution of a triangle-density construction; comparison throughout dense branches remains to be checked exactly. Endpoints both zero.

## Universal small-amplitude mechanism

Let W0 be complete multipartite on fixed positive parts Ai of masses ai, S2=sum ai^2. Every feasible h=W-W0 is nonnegative within parts, nonpositive across parts. With fixed density, addition and deletion masses both s=||h||1/2. Differentiate the six-factor polynomial:
DP[h] = -6 sum_i (S2-ai^2) int_Ai^2 h +6 sum_i!=j [(ai+aj)^2-S2] int_Ai x Aj h.
Therefore DP[h] <= -3g ||h||1 where g=min_i!=j(ai+aj)^2-max_i ai^2. For the triangle-density construction with k-1 equal masses a and one smaller b>0, g=(a+b)^2-a^2=b(2a+b)>0. At balanced knots discard zero blocks and g=3a^2>0.

A universal polynomial remainder is |P(W0+h)-P(W0)-DP[h]| <=171 ||h||infty ||h||1 when ||h||infty<=1: expand all subsets of >=2 among six factors, bound one h by its L1 integral, the other h factors by ||h||infty, and use 3 sum_{r=2}^6 binomial(6,r)=171. Hence epsilon<g/57 yields strict loss. This establishes a fixed-partition L-infinity local bound for arbitrary measurable perturbations. Constants depend on the fixed construction/density and are not asserted uniform across vanishing b or p->1.

## Topology and tying mechanism

L-infinity closeness forbids changing a 0-1 graphon by order-one values even on tiny area; L1 and cut closeness allow it. Cut distance <=L1 distance. A strict L-infinity bound cannot imply strict L1 or cut local uniqueness.

Independent exact tie mechanism: retain k-2 independent parts of equal mass a, join them completely to a residual B of mass d=a+b. The original B is complete bipartite with masses a,b and absolute edge integral e=2ab. Replace B with complete bipartite parts u,v satisfying uv=ab and u+v<=d, plus isolated B mass z=d-u-v. All C4 contributions depend only on e and induced C4 within B. The latter is 6u^2 v^2=6a^2 b^2. Thus p and P are preserved; for interior b<a take u,v tending to a,b with u+v<d, so L1 distance tends to zero. For z>0, a positive paw can arise from one retained part, one edge uv and one isolated B vertex, which forbids equivalence to any complete multipartite graphon. This requires k>=3 and b<a. At balanced knots the fixed product requires u+v>=2sqrt(ab)=d, so this specific mechanism has no isolated slack. Formal paw constant and edit-separation inequality remain to be derived.

## Pre-candidate controls

Owned independent code will check labeled normalization against all 64 four-vertex graphs, exact finite multipartite derivative coefficients, general rank-one polynomial/moment bound, small finite distribution checks, and an exact rational interior tying construction. These controls are source-free mathematics, distinct from the fresh source bindings above. No candidate verifier will be used to produce this verdict.
