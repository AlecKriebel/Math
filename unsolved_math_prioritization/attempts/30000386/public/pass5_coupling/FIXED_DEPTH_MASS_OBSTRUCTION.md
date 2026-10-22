# Age-admissible bad-center amplification at every fixed depth

Status: PASS5 verified obstruction to unweighted predecessor contraction. This does not produce a forcing strategy from the original empty history or refute the all-depth critical-gap hypothesis.

## 1. A natural profile that fails

For a finite preloaded pending set B, let L_k(B) be the set of spatial starting centers from which the Devil can force a loss within the next k moves against every Angel strategy. New Devil announcements retain the original one-per-round budget and occur after observing each move.

The proposed unweighted contraction

    |L_k(B)| <= |B|                                     (1)

fails at every fixed depth k>=2, even when B satisfies the exact age-tail constraints of some finite maximum-lead game and can occur in a legal nonlethal history.

## 2. Terminal periodic construction

Fix k>=2 and m with 3m>2k. On the spatial square {0,...,3m-1}^2 put

    P_m={0,...,3m-1}^2 minus {(x,y): x and y are divisible by 3}.

There are 8m^2 points. Preload all pairs (p,k), p in P_m, and no other effective pair. Thus |B|=8m^2 and the only old lethal time is relative time k.

Every consecutive side-three square wholly inside the large square contains exactly one omitted point and eight preloaded points. Consider any starting center

    a in {k,...,3m-k-1}^2.

After k-1 moves every possible Angel position q has both coordinates between 1 and 3m-2. Therefore N(q) lies inside the large square and contains exactly eight preloaded final-time bombs.

Make harmless announcements through relative round k-2. After observing the Angel's position q at relative time k-1, announce the unique missing point of N(q) with target time k. This is a legal lead-one announcement. All nine possible final moves are now bombed. Hence

    {k,...,3m-k-1}^2 subset L_k(B),
    |L_k(B)| >= (3m-2k)^2.                           (2)

The argument is online and the final announcement is chosen after the penultimate move. It protects neither a precommitted offline path nor an assumed single bomb per target time.

## 3. Quantitative amplification

For each fixed k,

    liminf_(m->infinity) |L_k(B)|/|B| >= 9/8.

An entirely explicit strict counterexample at every depth is m=12k. Equations (1)-(2) would then require

    |L_k(B)|/|B| >= 34^2/(8*12^2) = 289/288 >1,

contradicting contraction.

This is compatible with a uniform bound larger than one, such as the separately studied four-thirds envelope for static A8 iterations. It rules out contraction, not every bounded nonlinear profile.

## 4. Exact bounded-lead admissibility and legal preload history

Set N=8m^2 and H=N+k-1. At a before-move state with all N pairs at relative time k, the age-tail inequalities hold:

    #{pairs with target>=j}=N <= H-j+1  for 1<=j<=k,
    #{pairs with target>=j}=0          for j>k.

There is also a direct legal history. During actual rounds 1,...,N announce the N distinct points of P_m, one each round, all with common target T=N+k. The largest lead is T-1=N+k-1=H; every later announcement has a smaller positive lead. No preloaded bomb explodes during those N rounds.

For any chosen a in the interior set of (2), the Angel can legally reach a from the original origin within these N moves and then stay there: max-coordinate distance is at most 3m-1<=N. The resulting post-round-N state has exactly the asserted pending set and center. The final-hole announcement in the subsequent play has lead one, also within H.

This proves existential legal reachability for the bad configurations and compatibility with all age constraints. It does not force the Angel to choose that earlier path or interior position. A different full-history strategy may preempt the configuration while the bombs are being announced.

## 5. What the obstruction leaves open

The critical-gap hypotheses concern states satisfying W_k but failing W_(k+1); this construction only establishes a large losing-center set at a stated horizon. It therefore does not disprove those hypotheses. Nor does it justify treating an existentially reachable preload as an empty-board Devil force.

The sharp conclusion is that one cannot repair a spatial-cardinality contraction argument simply by increasing its fixed predecessor depth or appending the exact bounded-lead age constraints. Further information about viable histories, geometry, or robust continuation is necessary.
