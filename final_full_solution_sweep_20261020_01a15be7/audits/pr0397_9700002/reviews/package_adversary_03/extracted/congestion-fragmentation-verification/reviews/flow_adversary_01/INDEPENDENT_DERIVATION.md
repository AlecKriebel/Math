# Independent deterministic reconstruction

The statements below concern the exact declared model, including nonnegative admitted quantities and simple tree paths. Positive finite rate arrays are the quenched domain; the independent exponential law lies in that domain almost surely. This note does not assert historical novelty or decide whether a conceptual research program has a canonical resolution.

## Geometry and design

For height H, the two root sides have k=2^(H−1) leaves each and the whole tree has 4k−1 vertices. Removing a nonroot edge separates a descendant set of k_e terminals, all on one root side. Exactly kk_e left-to-right commodities cross that edge. Requiring two admitted units for each such commodity forces C_e≥2kk_e. Routing the doubled matrix on its unique tree paths realizes all these lower bounds simultaneously. Because every capacity-increment price is strictly positive, any vector with a strict excess in even one coordinate costs strictly more. Thus C_e=2kk_e is the unique least-cost enlargement on the fixed topology.

This argument would lose uniqueness if a price were zero; strict positivity is part of the candidate. It makes no statement about optimizing topology or robustness against future rate samples.

## Exact transportation reduction

For any k-by-k admitted matrix y, a left terminal edge carries its row sum and a right terminal edge its column sum. Both capacities are 2k. Every internal edge load is a sum of these terminal loads over its descendant set, and its capacity is the sum of the corresponding terminal capacities. Consequently all physical capacity inequalities are equivalent to the k row inequalities and k column inequalities, together with 0≤y_ij≤d_ij.

Use a finite directed auxiliary network with source-to-left capacities 2k, left-to-right capacities d_ij, and right-to-sink capacities 2k. Conservation gives precisely the admitted matrices, with value sum y_ij. Put left set A and right set B on the source side of a cut. The cut has capacity

    2k(k−|A|+|B|) + sum_{i∈A,j∉B} d_ij.

Substituting d_ij(t)=1+(t−1)X_ij proves the displayed finite formula by the ordinary finite max-flow/min-cut theorem. No approximate or asymptotic equivalence is being used. The auxiliary network is only a proof device; physical spare edges remain edges of the original tree.

## Right marginal, including ties

Write the cut lines as l_a(t)=b_a+m_a(t−1), with finitely many indices a. At any fixed t, every inactive line has a positive gap above the minimum. Finiteness gives a right neighborhood where no inactive line overtakes all active lines. Among the active lines, the one with smallest slope is minimal immediately to the right. Thus

    F'_+(t)=min {m_a : l_a(t)=F(t)}.

The left derivative, when needed, uses the largest active slope. Each m_a is a sum of a subset of the nonnegative rate entries, hence lies between zero and S=sum X_ij. Therefore 0≤F'_+/S≤1 for S>0. Normalizing by S is exactly differentiation with respect to the actual affine offered total Q(t)=k²+(t−1)S. Normalizing by the initial total k² is a different finite observable. The independent exact controls exhibit this difference; it is not silently interchangeable.

## Every optimizer in both outer phases

If all offered terminal sums are strictly below 2k, y=d is feasible. It attains the sum of all coordinate upper bounds. Any maximizer has sum(d_ij−y_ij)=0 with every term nonnegative, so y=d coordinatewise. Its terminal loads are strictly slack and every internal load is a sum of strictly slack terminal loads; hence every physical edge is strictly spare. There is no favorable selection among optima.

Conversely, every feasible matrix has total at most 2k² by summing row inequalities. If equality is attained, every one of the k row inequalities and every one of the k column inequalities must be equality. Every internal edge is therefore saturated as well. This conclusion holds for all maximizing matrices even when they are not unique. The spare graph then has no edges and its largest component has one vertex.

These statements require the declared simple-path physical model. Gratuitous circulations would be extraneous to that model and are not covered by the all-optimizer assertion. They also do not imply any optimizer-independent statement at an arbitrary intermediate or critical-time realization; fresh exact controls give optimal matrices with different spare-edge counts there.

## Endpoint and continuum-of-times checks

Strict offered terminal slack at t_minus persists on some right neighborhood because there are finitely many finite positive terminal slopes. Thus the right marginal at the lower endpoint is exactly one. Coordinatewise demand monotonicity extends full admission and slack backward to every time in [1,t_minus].

If a feasible admitted matrix has total 2k² at t_plus, it remains feasible at every later time. The global upper bound remains 2k². Throughput is therefore constant to the right of t_plus, including at the endpoint in the right-derivative convention; its right marginal is zero. All optimizers saturate all physical edges at every such time. A probability event at two deterministic endpoints suffices; no uncountable time-union argument is missing.

## Check of the candidate's all-cut event

For A and D=R\B, a=|A|, d=|D|, only a+d>k imposes a positive transportation cut demand. The identity

    ad−k(a+d−k)=(k−a)(k−d)≥0

implies that a failing cut at t_plus=2+δ forces the rectangle rate sum below ad/(1+δ). The exponential lower-tail bound consequently applies. Setting q=min(a,d), ell=k−max(a,d) gives exactly 0≤ell<q and ad=q(k−ell). For q≤floor(k/2), the candidate's count 2q k^(2q) and area lower bound qk/2 are valid overestimates. For q>k/2 the area exceeds k²/4 and the count 4^k is valid. With δ=8 sqrt(log k/k)<1, the advertised two supercritical error terms follow. Terminal sums alone would not prove feasibility; the new mixed-cut witness verifies that this tempting shortcut is false.

The subcritical event uses the corresponding 2k terminal upper tails. A union bound combines the two endpoints without any independence assertion between cuts or between row and column events. I found no algebraic gap in these displayed arguments. Separate stochastic/source/priority reviewers are responsible for their own complete family assessments; this note's distinctive verification mechanism is exact primal/dual transport and physical-edge identities.

## Exact controls and their limits

The new program imports neither author code nor the previous independent code. It constructs rational Dinic primal flows with residual-cut dual certificates and builds physical routes using binary words rather than the frozen heap/BFS representation. Its 534 rational instances yield 687 exact primal/dual certificates, 153 true envelope-kink checks, and 3972 physical-edge identities. It also checks synchronized ties, actual-slope normalization, a mixed-cut obstruction, and optimizer dependence in the excluded region.

The finite controls are not proofs of the random large-k theorem and do not adjudicate novelty. The general deductions above, not successful experiments, establish the deterministic claims.
