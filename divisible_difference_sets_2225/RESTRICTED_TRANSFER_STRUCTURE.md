# Finite-state structure of the all-odds restriction

This is an elementary structural deduction within a RESTRICTED family. It does not bound unrestricted M_t(N), establish novelty, or resolve EP-635. Throughout t≥2 is a fixed integer.

Let H_t(N) be the maximum number of evens which can be adjoined to ALL odds in [1,N]. By the odd-neighbor characterization, the relevant evens are exactly 2^k m≤N with k≥1 and m in the finite type set T={1,3,…,2floor(t/2)−1}. Put h=|T|, m*=max T, and R=floor(log_2(2m*)).

Claim: there is a rational, finitely computable number rho_t such that

H_t(N)=rho_t log_2 N+O_t(1).

Consequently the best admissible set containing every odd integer has size ceil(N/2)+rho_t log_2 N+O_t(1). NO assertion here says a global extremizer contains all odds.

## Translation-invariant finite-range graph

Same-level vertices 2^k m and 2^k n do not form edges, since m−n is even and cannot divide odd n. For levels k>l, the edge test, independent of the numerical ordering of the endpoints, is

|2^(k−l)m−n| divides n, and 2^l |2^(k−l)m−n|≥t.

Indeed the difference divides either endpoint if and only if it divides the lower-valuation endpoint 2^l n. The absolute value is nonzero since its two terms have opposite parity. If it divides n, it is at most n, implying 2^(k−l)m≤2n≤2m*. Hence k−l≤R.

For l≥K=max(1,ceil(log_2 t)), the threshold inequality is automatic. The graph on these levels therefore has h types per level and a fixed edge rule depending only on the type pair and level gap, at most R.

## Boundary reduction

The complete levels K≤k≤floor(log_2(N/m*)) contain every type. Levels below K contain O_t(1) vertices. Levels above floor(log_2(N/m*)) and at most floor(log_2 N) also contain O_t(1) vertices. Deleting these boundary vertices changes the independence number by at most their number. For asymptotically large N, the number of complete levels is L=log_2 N+O_t(1). Small N can be absorbed into the t-dependent constant.

## Finite-state optimization and rational slope

A state records a feasible pattern of selected types in the preceding R levels. There are at most 2^(hR) states. Appending a subset S of types is allowed precisely when it does not create any edge to the recorded levels; shift the record one level and give this transition integer reward |S|. The maximum reward over L transitions starting from the all-empty state is exactly the independence number of the L-level strip.

Every feasible state is reachable from the empty state in R transitions by building its recorded pattern. Every state can reach the empty state by appending R empty layers. The feasible state digraph is therefore strongly connected. It contains the empty self-loop, with reward zero.

Let rho_t be its maximum directed cycle mean, total reward divided by cycle length. It is rational and computable by enumerating the finite digraph and its simple cycles (efficiency is not claimed). To upper-bound a length-L walk, remove cycles until a simple path remains. Every removed cycle has reward at most rho_t times its length; the remaining path has bounded length and weight depending only on t. Thus its total reward is at most rho_t L+O_t(1).

For the converse, travel from the empty state to a maximizing cycle, repeat that cycle as many whole times as the desired length permits, and use a bounded number of arbitrary feasible steps for the remainder. Nonnegative transition rewards and bounded connector/remainder lengths give at least rho_t L−O_t(1). This proves the claim.

The explicit spaced-level construction gives rho_t≥h/(R+1); trivially rho_t≤h. At t=2 the graph is the ordinary one-vertex-per-level path, hence rho_2=1/2. No values for larger t are certified here. The finite-state method is a way to determine the restricted coefficient, not a global logarithmic-error upper bound.
