# Independent hand derivations and adversarial controls — before any support/foreign findings

These are source-only personal calculations, not imported archived results. They define falsifiable interfaces for the later full-original adversarial review; no native scientific program has run.

## Deterministic physical model and every-optimizer quantifiers

A height-H full binary tree has2^(H+1)-1=4k-1 vertices and maximum degree3. Each physical edge separates a descendant leaf subset of exactly one root side from the other side. Its load is the sum of the corresponding terminal row sums or column sums. At original unit demands it is k*k_e. At doubled original demands the unique physical paths force each edge individually to carry2k*k_e, and those lower bounds are jointly feasible. A cost sum with every increment coefficient strictly positive is uniquely minimized at this componentwise forced vector. This argument would fail with zero/negative prices or topology changes; neither is allowed.

Every feasible row/column system with bound2k makes all internal edge loads<=2k*k_e by summation, while terminal edges force the row/column inequalities. Thus no internal physical cut has been silently omitted by the transportation reduction. Feasible admitted matrices form a nonempty compact polytope for every finite t>=1; an optimizer exists.

If all offered terminal totals are strictly below2k, y=d is feasible. Every entry gap d_ij-y_ij is nonnegative, so any optimizer attaining sum d has all gaps zero. Therefore the admitted matrix is unique, and every internal load is a finite sum of strict terminal inequalities. Every physical edge is strictly spare for every optimizer, including both root edges. It is not enough merely that some optimizer has a convenient sparse support.

The total admitted traffic is <=sum row capacities=2k^2. If equality holds, the nonnegative row deficits sum to zero, hence each row is2k; the same holds for columns. Every physical edge is then exactly saturated for EVERY optimizing matrix. Commodity-level degeneracy cannot leave an internal edge spare. The full vertex set still has4k-1 vertices, so the largest edgeless component is1, not0; only normalized M/N tends to0.

## Cut formula and right derivatives

Put source-side left nodes A and source-side right nodes B in the three-layer network. Crossing capacity is2k(k-|A|)+sum_{i in A,j notin B}d_ij+2k|B|, giving the exact printed formula. The all-middle cut A=L,B=empty has slope S and offered-total intercept; the two exterior cuts have constant capacity2k^2 and slope0. All other cut slopes lie in[0,S]. Finite max-flow/min-cut for real capacities is the central external import still to be checked after resume.

The finite minimum of affine nondecreasing cuts is continuous, nondecreasing, concave and piecewise affine. At a tie, the RIGHT derivative is the minimum of active slopes; using the maximum would confuse the left derivative. Its ratio by S lies in[0,1] for S>0. S=0 is excluded on an almost-sure event, not divided by as a deterministic identity for every artificial input.

Strict terminal slack at t_minus persists in a right neighborhood because there are finitely many constraints/slopes. This proves r(t_minus)=1 as a right derivative, rather than merely a left-endpoint statement. At t_plus, one maximum admitted matrix remains feasible at all later times by entrywise monotonicity of offered demands. The fixed total ceiling then makes F constant from that endpoint onward, including right derivative0. These endpoint events are deterministic implications on a finite random sample, so no union bound over uncountably many times/optimizers is needed.

## Tail exponents and the all-cut count

For Z=sum of n independent Exp(1), MGF=(1-lambda)^(-n) for lambda<1. With lambda=1-1/a, exponential Markov gives exp(-n*(a-1-log a)) for upper tail a>1 and for lower tail0<a<1. For the latter lambda<0 reverses the event before applying Markov to exp(lambda Z); the sign is essential.

With I(a)=a-1-log a, differentiation of I(1/(1-delta)) gives delta/(1-delta)^2>=delta; differentiation of I(1/(1+delta)) gives delta/(1+delta)^2>=delta/4 for0<delta<1. Integrating from0 gives respectively delta^2/2 and delta^2/8. Lower-endpoint offered row/column sums are k+(1-delta)Z. Reaching2k implies Z>=k/(1-delta). The2k-event union bound is2k*exp(-k*delta^2/2), with no row/column independence assertion. At delta_k^2=64log(k)/k this equals2k^-31. The complement gives strict slack, not a weak <=capacity condition.

For an upper cut put D=R\B, a=|A|, d=|D|. Cuts a+d<=k are automatic. For a+d>k, ad-k(a+d-k)=(k-a)(k-d)>=0. Failure implies ad+(1+delta)Z<2k(a+d-k)<=2ad, hence Z<ad/(1+delta). This implication remains safe for cuts whose original failure threshold is negative/impossible; it only overbounds. A given failing cut is bounded by exp(-c*ad), c>=delta^2/8.

Let q=min(a,d), ell=k-max(a,d); then0<=ell<q and ad=q(k-ell). For q<=floor(k/2), the at-most2*binom(k,q)*binom(k,ell) choices allow interchange (overcounting ties harmlessly). Sum over ell=0,...,q-1 and use binomial<=k^q to get <=2q*k^(2q), while ad>=q*k/2. For q>k/2 both factors exceed k/2; there are at most4^k pairs of subsets in total. No independence among cut events is needed. At c>=8log(k)/k, the first contribution is bounded by sum_{q>=1}2q*k^(-2q)=2k^-2/(1-k^-2)^2; the second is(4/k^2)^k. Combining with the lower event gives exactly epsilon_k. The small-q bound is deliberately loose but has the required vanishing order. No efficient exhaustive algorithm or exact critical-window probability has been proved by this count.

## Explicit adverse finite controls

1. Uniform deterministic positive slopes X_ij=1 give offered d=t. For every k, F=k^2*min(t,2), r=1 before2 and r=0 at/after2, using RIGHT derivative. At t=2 every optimizer saturates every physical edge. This tie/degenerate-slope control lies in a probability-zero configuration under the continuous law but tests the deterministic formulas and shows why no r(2) limit may be inferred by differentiating the throughput limit.

2. A robust binary-k=4 transportation trap shows terminal offered totals alone cannot prove the upper phase. At t=2 use d entries11/10 in rows1,2,3/columns1,2 and in row4/columns3,4, and5 in the other eight positions. All X=d-1 are strictly positive. Every offered row and column exceeds its cap8, yet A={1,2,3},D={1,2} has cross sum66/10<8. Its cut is24+66/10=153/5<32. Thus F<2k^2 despite all offered row/column totals exceeding capacity. Nearby open sets of positive slopes retain the obstruction. This does NOT falsify the theorem: its upper proof uses every cut, and k4 has delta_k>=1 outside the finite quantitative assertion. It tests and rejects the tempting weaker substitute.

3. At binary k=2, t=2, use X=[[10,1/10],[1/10,1/10]], hence d=[[11,11/10],[11/10,11/10]], terminal caps4. The row2 offer is11/5, so F<=4+11/5=31/5. The feasible matrix[[29/10,11/10],[11/10,11/10]] attains that bound; column1 is4, column2 is11/5. Every optimum has that unique matrix. Exactly two terminal edges saturate, both root edges remain spare, and the spare graph has largest component5 of N7. In a right neighborhood, F=4+2+(t-1)/5, so r=(1/5)/(103/10)=2/103. This attacks accidental all-time all-or-nothing claims and demonstrates residual components/intermediate marginal admission outside the proven outer event. It is consistent with the original theorem's declared window/finite-k limits.

4. Extremely small positive row slopes can delay saturation, and an exceptionally large stream can saturate a terminal edge early. Those deterministic samples belong to the possible bad event; the theorem is probabilistic, not a guarantee for every slope realization. Repeated/zero slopes and equal cut lines do not break the finite minimum/right-derivative formula when S>0. An all-zero artificial slope matrix has S=0 and is outside the a.s. normalization domain.

## Limit quantifiers and unverified context

S/k^2 has mean1 and variance1/k^2. At fixed t<2, the good outer event eventually contains t and gives F/k^2=1+(t-1)S/k^2, r=1 and M/N=1. At fixed t>2 it gives F/k^2=2, r=0, M/N=1/(4k-1). At t=2, on the same event, 1+(1-delta_k)S/k^2<=F(2)/k^2<=2, which yields the claimed throughput limit using Chebyshev plus epsilon_k->0. No limit/derivative interchange is justified or needed. Summability of the failure bounds along binary k gives eventual outer events under any coupling preserving each model marginal, by first Borel-Cantelli without across-k independence. This is not a uniform assertion for all finite k, nor a stronger critical-profile theorem.

Pending actual primary/interface work after explicit resume: real-capacity finite max-flow/min-cut; precise Aldous conceptual request/index/tree-realism caveat; credited random-transport antecedent and actual1988/final1993 edition distinction; scope separation from sequential shortest-path percolation/HOT. Native support/replay policies/older output/priority-search assertions remain completely unread and unadopted. Any later ordinary check must be chosen after full exact code/input/safety reading; one meaningful route maximum, no retries/repair/campaign. No full-original verdict is assigned here.
