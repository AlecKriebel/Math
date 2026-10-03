# Independent cograph proof reconstruction and sealed verdict

VERDICT: Supported scoped theorem; no mandatory mathematical correction found in Turn 4. The original unrestricted conjecture remains unresolved. Audit estimate at seal: 85%; cograph verification: 100%; unrestricted discovery: 0%. Timestamp: 2026-10-03T07:52:06.185046Z.

This verdict was reached before reading any candidate verifier, old independent review, candidate check receipt, candidate manifest, or sibling/root derivation. Candidate prose read after my independent baseline seal: `TURN_1.md`, `TURN_2.md`, `TURN_4.md`, `FINAL_RESULT.md`, in the frozen snapshot target `problems/30005116_induced_four_cycle_profile`. The parent clarified that `A/snapshot` was a placeholder; the actual root is `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr374_30005116/snapshot`. No broader filesystem search was made. The source and baseline scopes, source byte identities, failed controls, and timestamp corrections are preserved in the accompanying files.

## Exact claim and scope

Let p be edge probability under independent graphon sampling, and c the probability that four sampled vertices induce an unlabeled C4. Put q=1−p. For q>0 set r=floor(1/q), d=((r+1)q−1)/r, a=(1+sqrt(d))/(r+1), b=(1−r sqrt(d))/(r+1), L(q)=ra^4+b^4, and F(p)=3(q²−L(q)); F(1)=0. Then every finite weighted cograph graphon made from empty leaves and finite complete joins/disjoint unions satisfies c≤F(p). Allowing complete leaves gives the same theorem, since their (p,c)=(1,0) is a valid induction base and the join endpoint argument below applies. Zero-mass children are omitted. The profile is attained for 0≤p<1 by complete multipartite graphons; p=1 is attained in the closure (or by the optional complete leaf). Every sequence of finite cographs of unbounded orders and arbitrary, possibly increasing cotree depths satisfies limsup ρ_ind(C4,G_n)≤F(x) when x(G_n)→x. Limits in the two stated densities inherit the inequality.

The unrestricted source asks about all graph sequences above density 1/2. This theorem does not establish any decomposition or same-density replacement for non-cographs. A finite order-six enumeration could verify examples or formulas but cannot supply that missing reduction or the all-depth proof. No unrestricted promotion follows.

## Checked multipartite input

I reconstructed the Turn 1 moment argument rather than treating its optimization as an axiom. For each feasible fixed dimension, compactness gives a minimizing nonnegative vector. Restrict to positive coordinates. At a reciprocal q=1/s, Hölder gives Σa_i^4≥q³ with equality exactly for a uniform positive support. Otherwise the two constraint gradients are independent, and Lagrange multipliers give 4z³−2λz−μ=0 for each positive coordinate. This cubic has at most two positive roots because three distinct positive roots would have positive sum despite its zero quadratic coefficient. Denote the two by t<u. Subtraction gives 2λ=4(t²+tu+u²). If at least two coordinates are t, the difference direction between those coordinates is tangent to both constraints and has Lagrangian Hessian 8(t−u)(2t+u)<0. The regular common constraint manifold supplies a feasible twice differentiable curve in that direction, contradicting a minimum. Thus there is exactly one small coordinate and r larger coordinates. Their constraints imply 1/(r+1)<q<1/r, uniquely fixing r and the displayed masses. Cauchy–Schwarz ensures the required support fits every feasible dimension. Boundary supports and reciprocal cases are covered. This proves the moment input for every finite part count; no unsupported optimization premise remains.

The profile is continuous at every reciprocal knot: both neighboring part vectors converge to the same uniform positive support, with a vanishing last coordinate allowed. At q→0, 0≤L(q)≤q² yields F→0. At p≤1/2 the two-part formula gives F(p)=3p²/2. For p>1/2, r≥2; differentiating ra+b=1 and ra²+b²=q gives L'(q)=2(a²+ab+b²) and F'(p)=−6[(r−1)a²−ab]≤0. Continuity extends monotonicity across knots. Hence 0≤F≤3/8. Also every positive part is at most a and q≥ra²≥2a², so L≤a²q≤q²/2 and F≥3q²/2 on [1/2,1]. All these properties are valid at endpoints by continuity.

## Universal coupled join argument

My independently derived recursion is c=Σw_i^4c_i+6Σ_{i<j}w_i²w_j²q_iq_j, and q=Σw_i²q_i. Assume c_i≤F(p_i). For every child with p_i<1, replace it by the multipartite model with the same p_i and density F(p_i). This keeps each q_i fixed, so it keeps the full cross-child term and total edge density fixed, while increasing the internal term. The resulting join is itself complete multipartite, and the moment theorem bounds its density by F(p). The argument handles arbitrary child masses and internal densities; setting child densities to a guessed global density would have been invalid.

For a child with p_i=1, 0≤W_i≤1 implies W_i=1 almost everywhere and c_i=0. Replace it by balanced k-partite children with p_i^(k)=1−1/k and c_i^(k)=3(k−1)/k³. Those quantities converge to (1,0). In the finite join recursion both global densities converge to the original ones. Continuity of F passes the replacement bound to the limit. The limiting replacement need not preserve edge density at finite k; convergence of the two densities is sufficient and is explicitly used. No positive-mass finite part vector of density exactly one is claimed.

## Universal union argument and exact strictness

For a disjoint union, x=Σw_i²p_i and c=Σw_i^4c_i. If x≤1/2, the independently proved matching inequality c≤3x²/2=F(x) suffices. The matching inequality is pointwise: an induced C4 has two of the three perfect matchings present, so 1_C4≤M/2 and E[M]=3p².

Suppose 1/2<x<1. Let w be the largest child mass, s=1−w, and p its internal edge density. Then x≤Σw_i²≤w, so w>1/2 is unique. The remaining children contribute at most Σ_{others}w_i²≤s², giving p≥(x−s²)/w²≥x. The latter comparison is exactly s[x(1+w)−s]≥0; both x,w>1/2 ensure it. Because F decreases above 1/2, F(p)≤F(x). Each other child has c_i≤3/8. Therefore c≤w^4F(x)+(3/8)s^4.

Let q=1−x. Since s≤q and 1−w^4≥s,

F(x)−c ≥ (1−w^4)F(x)−(3/8)s^4
          ≥ s[(3/2)q²−(3/8)q³]
          = (3/8)s q²(4−q).

The final quantity is strictly positive for a nontrivial positive-mass union at 1/2<x<1. It vanishes if w=1 or x=1; zero-mass children do not make a nontrivial union. A nontrivial union cannot have x=1 anyway, while any graphon with x=1 has c=0. The candidate claims only a local positive gap, not uniform global stability. My exact controls include a fixed-density sequence w→1 for which the certified positive gap tends to zero. Equality at densities ≤1/2 is possible, including a bipartite component plus isolates. Joining such low-density ties can give the known paw examples, so high-density strictness at a union node is consistent with non-multipartite cograph ties at the root.

## Arbitrary depth and finite-sequence normalization

Induct over the finite cotree. Both bases (empty and optional complete) satisfy the inequality. Each node is covered by one of the two proved closures, with no depth-dependent error. DMTCS Section 6.2 supplies only the standard recursive cograph definition; complements flip joins/unions, so ordinary finite cographs admit this recursive construction. No P4-free equivalence theorem is required.

For a finite n-vertex cograph, its adjacency graphon has singleton empty leaves of mass 1/n and p=2e(G)/n²=(1−1/n)x(G). In four independent samples, the probability of any repeated vertex is at most Σ_{i<j}1/n=6/n. Conditional on no repetitions, the induced graph is distributed as a uniform four-element subset. Consequently |c(W_G)−ρ_ind(C4,G)|≤6/n and

ρ_ind(C4,G)≤F((1−1/n)x(G))+6/n.

This is uniform over graphs, orders, numbers of leaves, and depths. Continuity of F suffices to take limsups along every cograph sequence; no fixed-depth approximation theorem is needed. The same closed inequality passes to limits in p and c. Endpoint x=0 and x=1 have F=0, and knots require no additional argument.

## Evidence and exact remaining gap

Independent rational controls: 210 direct ordered-tuple checks of random weighted cotrees (1–7 leaves, arbitrary recursive depth at those sizes, zero weights, both diagonal leaf types), balanced multipartite endpoint identities k=2,...,12, and unbalanced bipartite equalities. Independent exact union controls: 31,941 parameter tuples, of which 3,666 are relevant high-density largest-child tuples, including 1,404 degenerate endpoint tuples. Independent numerical falsification probe: 100,000 relaxed join tuples and 100,000 relaxed union tuples; after the preserved branch-tolerance repair, largest excess 4.44e-16 is roundoff at an equality. These finite computations test formulas and arithmetic; the universal theorem rests on the written proof above. No candidate control code was used to derive this verdict.

Strongest verified result: the full proposed profile is exact for every finite weighted cotree and every cograph sequence, with the stated strict high-density local union gap. Exact remaining gap: no reduction controls arbitrary non-cograph hosts at intermediate density; therefore the original unrestricted problem remains unsolved. External theorem input used for this scoped reconstruction: none beyond the sourced recursive cograph terminology; Hölder, Cauchy–Schwarz and elementary constrained calculus are demonstrated in their application. Primary LMR supplies the problem formulation and credited candidate, not a substituted proof of the cograph extension.
