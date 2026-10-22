# Derivation before prior package opinions

Reconstruction checkpoint recorded in RESEARCH_LOG.md (the original manually typed 06:53 timestamp was corrected to the actual automatic log). This reconstruction follows the five exact copied release files and independently fetched Aldous request/index. No previous package report or verdict was read first.

## Claim and criterion

For binary k=2^(H-1), a complete height-H physical tree has 2k leaves and 4k-1 vertices. Only cross-root leaf pairs carry commodities, initially one apiece. Capacities are designed once, then held fixed while independent Exp(1) slopes grow demands affinely. Success is a simultaneous, all-time outer-phase event with exact stated error bound and every-optimizer slack graph, not merely a throughput limit or a numerical plot.

## Physical model and deterministic identity

Every descendant leaf under edge e communicates with all k leaves on the opposite root side, so its initial load is k*k_e and its doubled-demand load 2k*k_e. Unique paths force these capacities componentwise; any strictly positive linear edge price makes that feasible componentwise minimum uniquely cheapest. This optimizes increments on a fixed topology, not topology itself. Capacities diverge with k and the traffic matrix is dense even though the physical graph has degree at most three.

Terminal row/column inequalities each with ceiling 2k imply every ancestor-edge inequality because those loads add over descendant terminals. Conversely terminal edges impose them. A source-to-left arc 2k, left-to-right arc d_ij, right-to-sink arc 2k therefore gives precisely the physical optimization. A cut with source-side leaves A,B has value 2k(k-|A|+|B|)+sum(A x (R\B))d. The two trivial cuts show F<=2k^2. A finite minimum of affine functions is continuous, piecewise affine, and concave; all slopes are subset sums of positive X, and the right derivative at a tie is the least active slope. Normalization by realized S, not k^2, places the marginal in [0,1].

If all offered row/column sums are strictly below 2k, y=d is feasible and the unique matrix reaching offered total, since each y_ij<=d_ij. All ancestor sums then have strict slack. If F=2k^2, every one of the k row and column sums of any optimizer equals 2k; therefore every ancestor edge saturates. No optimizer selection can change these two conclusions. A measurable optimizer selection is needed only to describe intermediate random graph variables; a Borel selection exists for this nonempty compact finite LP. The event proved here needs no such choice.

## Probability reconstruction

For n exponential variables, MGF (1-lambda)^(-n) and optimized exponential Markov give exp[-n(a-1-log a)]. With a=(1-delta)^(-1), rate derivative delta/(1-delta)^2>=delta gives I>=delta^2/2. With a=(1+delta)^(-1), derivative delta/(1+delta)^2>=delta/4 for 0<delta<1 gives I>=delta^2/8. The lower phase requires strict endpoint row/column slack; an upper-tail union of 2k events gives 2k exp(-k delta^2/2)=2k^-31 at delta=8sqrt(log k/k). Strict finite slack persists right of that endpoint, proving its right derivative also equals S. Monotonicity covers the uncountable interval without an uncountable union.

For upper saturation, every transport cut must meet 2k^2. Write a=|A|, d=|R\B|. If a+d<=k it is automatic. Otherwise failure requires sum d_ij<2k(a+d-k). Since ad-k(a+d-k)=(k-a)(k-d)>=0, this implies sum X_ij<ad/(1+delta), with probability <=exp(-c ad), c>=delta^2/8. For q=min(a,d), ell=k-max(a,d), one has 0<=ell<q. If q<=floor(k/2), the number for each ell is <=2 C(k,q)C(k,ell), so all ell contribute <=2q k^(2q), and ad=q(k-ell)>=qk/2. At c>=8log(k)/k, the sum is <=sum_(q>=1)2q k^(-2q)=2k^-2/(1-k^-2)^2. If q>k/2, ad>k^2/4 and there are at most 4^k rectangles, giving (4/k^2)^k. Dependencies among rectangles and between row/column events are irrelevant to these unions. This includes q=1, ell=0, full and almost-full rectangles and ties in a,d. Increasing d retains a full optimum forever, so the upper all-time event follows from one endpoint.

Combining endpoint events gives exactly epsilon. Delta<1 excludes small k; first admissible binary k is 512, to be checked computationally. No formula is used at k=1. Every fixed t<2 eventually lies in the lower interval and t>2 in the upper interval. S/k^2 has mean 1 and variance k^-2. At t=2, the lower endpoint F=k^2+(1-delta)S sandwiches F(2) below 2k^2. This proves throughput at two without any derivative-limit exchange. Failure probabilities are summable over binary k, so the first Borel-Cantelli lemma works under arbitrary couplings with these marginals. No independent coupling across sizes is assumed.

## Deliberately invalid shortcuts

Offered row and column totals exceeding 2k do not suffice for full flow. For binary k=4 take d_ij=1.1 in the first three rows/first two columns and 10 elsewhere. Every offered row and column exceeds 8, but A={first3}, D={first2} has mass 6.6<8, hence a cut of 30.6<32. These entries have strictly positive slopes at any chosen t>1 and an open neighborhood has positive exponential probability. Dense cuts, not just singleton checks, matter.

Replacing S by its expectation breaks the exact marginal claim: at t=1 and all slopes two, F'_+=2k^2 while the advertised normalized marginal is one. Tree topology alone also does not imply optimizer-independent spare graphs at intermediate times. No central step is transferred to an unsupported asymptotic feasibility theorem.

## Scope

The independently recovered index calls congestion type 0.7, on the conceptual side of the spectrum, and its source asks for the right tractable toy model rather than a uniquely specified conjecture. This example implements the fixed-design suggestion with a different variance law, no rerouting, no topology optimization, no SOC/adaptation, dense traffic, growing capacities, and a sufficient width only. The exact theorem appears internally supported; suitability as a canonical explanatory model and worldwide priority remain separate, uncertified judgments. Priority/body and operational review remain pending.
