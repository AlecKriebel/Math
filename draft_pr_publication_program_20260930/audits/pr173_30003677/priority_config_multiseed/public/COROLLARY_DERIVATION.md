# Exact prior-theorem reduction of the candidate

## Status

The whole existence claim, including the deterministic sublogarithmic time schedule, follows from Ganguly–Ramanan's general local convergence theorem plus the elementary ray and diagonal arguments below. This is a mathematical corollary, not a claim that those authors singled out this question. Under the audit's rule that an exact corollary counts as prior resolution, it obstructs presenting this candidate as a first answer.

The relevant result was already in **arXiv:2205.01587v1, 3 May 2022**, Theorem 4.3 (p.12); strong well-posedness Theorem 4.2 (p.12), Corollary 5.16 (p.24). The empirical version is Theorem 4.6 and Corollary 4.7 (pp.14–15). Published equivalents are Theorem 4.7 (p.19), Theorem 4.3 (p.18), Corollary 5.16 (p.33), and Theorem 4.11/Corollary 4.12 (p.21), EJP 29 (2024), paper 185, DOI 10.1214/24-EJP1243. Actual theorem bodies and the original v1 were read; reliance is not on the abstract.

## 1. Markov realization and the multigraph issue

Use states X={0,1,2}: susceptible, weak, strong. Only transitions 0->1 and 0->2 are allowed. For a graph with capped multiplicity m_uv in {1,2}, set

r_1(v,x)=1{x_v=0} lambda1 sum_(u~v) m_uv 1{x_u=1},

r_2(v,x)=1{x_v=0} lambda2 sum_(u~v) m_uv 1{x_u=2}.

Loops are ignored. Vertex marks retain the original total degree. All mark spaces are discrete. The local rates are Borel, symmetric under graph isomorphism, and predictable. With closure cardinality k, both rates are bounded by C_k=2 max(lambda1,lambda2)(k-1)+1. Thus the standing assumption and Assumption 1 hold. Assumption 2 is automatic for discrete marks. Finite graphs are finitely dissociable, and Corollary 5.16 gives this for the UGW(D) limit when E[D^2]<infinity.

This Markov process has the same law as the candidate's independent exponential edge traversal process: a channel connecting an infected vertex to a susceptible one has an exponential remaining waiting time by memorylessness; an edge cannot have both endpoints infectious and still produce a new infection. There is no recoloring and no need to assign independent effective endpoint clocks to an already occupied edge.

The cap is necessary in invoking the stated theorem's bound uniform over marks; leaving an unbounded multiplicity mark would not satisfy that bound merely from the number of distinct neighbors. It costs probability o(1). Conditional on a degree list, let L=sum_i d_i and Delta=max_i d_i. The expected number Z_3 of sets of three parallel edges between distinct vertices is exactly

E[Z_3 | d] = 6 sum_(i<j) binom(d_i,3) binom(d_j,3) / [(L-1)(L-3)(L-5)].

For large L this is at most a constant times (sum_i d_i^3)^2/L^3. Under the candidate degree law, L>=2n, sum_i d_i^2=O_P(n), and Delta=o_P(sqrt(n)). Therefore sum_i d_i^3<=Delta sum_i d_i^2=o_P(n^(3/2)), and the conditional bound tends to zero in probability. Bounded conditional probabilities then give P(Z_3>0)->0. On Z_3=0 the capped process is exactly the candidate's multigraph process. The parity repair preserves these properties. Rare degree lists with a degree exceeding n-1 may be replaced by any benign graph; their probability tends to zero. This addresses the degree-vector range in the paper's configuration-model example.

## 2. The fixed-cutoff marked initial-data limit

Fix K>d0. Initially mark every vertex with original degree at least K as type 1, and the independent degree-d0 uniform root W_n as type 2. All other vertices are susceptible.

The configuration graph with a uniform test root U_n converges locally to UGW(D): root degree D, other total degrees D*. This follows under empirical degree-law and first-moment convergence; the latter also follows from the candidate's stronger second-moment condition. The original degree and multiplicity marks converge too. To see this without assuming independent degree marks, radius-r initial-state markings are determined by the radius-(r+1) degree-marked graph. For any bounded exposure cutoff, sequential uniform partner matching has the size-biased limit, and collisions vanish. Let the cutoff grow only after n tends to infinity. Two such test-root explorations are asymptotically independent, yielding local convergence in probability as well, if the stronger empirical theorem is desired.

The fast root disappears in this marked local limit. Conditional on the degree list and graph, it is uniform among asymptotically n P(D=d0) vertices. A fixed-radius neighborhood of U_n is tight, so the probability that it contains W_n tends to zero. Equivalently, first truncate its cardinality at M and use M/(n P(D=d0)+o_P(n)), then let M grow. This argument uses independence of W_n from the matching conditional on degrees; it would not establish the same claim for a graph-inspecting adversarial root.

The limiting marked tree therefore has only susceptible and weak states, with every total-degree-at-least-K vertex initially weak. Arbitrary initial markings are permitted by the local theorem; no i.i.d. uniform seeding or worst-all-path reachability hypothesis is imposed. Theorem 4.3 of v1 (published Theorem 4.7) now gives convergence of the dynamics at U_n for each fixed T. Time-T evaluation is a continuity event because the root has a finite rate bound and no jump at a fixed deterministic positive time.

Write q_K(T)=P(the limiting root is weak at time T). We obtain

P(U_n is weak by T)->q_K(T).

The empirical hydrodynamic theorem is stronger than needed. The expectation identity for U_n followed by Markov's inequality suffices for the candidate's near-total claim, so the reduction does not rely on an unnecessary concentration assertion.

## 3. Limiting-tree success

Since D>=2, each non-root vertex has at least one forward half-edge. Select a forward ray using auxiliary randomness independent of clocks. The next R total degrees are independent D*, so absence of a seed among them has probability (1-p_K)^R, p_K=P(D*>=K)>0. Infection traverses the reversed seed-to-root route in a sum of at most R independent Exp(lambda1) costs. The limiting process has no type-2 seed, and thus no type-2 competition. Consequently

1-q_K(T) <= (1-p_K)^R + R/(lambda1 T).

In particular q_K(T)->1 as T->infinity for every fixed K. The general prior local theorem has already handled the single faster seed's possible finite-graph interference, so a new protected-path competition-transfer lemma is not required for this reduction.

## 4. Diagonal with all resources and the time refinement

Let K_j=d0+j, p_j=P(D*>=K_j), a_j=P(D>=K_j). Choose R_j=ceil(j^2/p_j), and increasing T_j with T_j>=j^2 R_j/lambda1 and T_j>=j. Then 1-q_Kj(T_j)<=2/j^2. Local convergence supplies a deterministic N_j such that for all n>=N_j the corresponding missing probability is at most 3/j^2. Enlarge N_j to make it strictly increasing, n a_j>=4j^2 whenever n>=N_j, and log N_j>=j T_j. Set J(n)=max{j:N_j<=n}, k_n=K_J(n), t_n=T_J(n).

The expected missing vertex fraction is at most 3/J(n)^2 and hence tends to zero; Markov's inequality gives N1(n,t_n)/n->1 in probability. The time bound is t_n/log n<=1/J(n)->0. The binomial mean n a_J(n)>=4J(n)^2, variance at most its mean, implies a diverging weak seed count with probability tending to one. Tail integrability gives the vanishing seed stub density, and P(D>=k_n)->0 gives the vanishing vertex density. The single parity repair changes these resource limits by a negligible amount. All schedules depend only on the degree law, d0 and rates. This recovers every simultaneous conclusion of the candidate, not merely a terminal positive fraction.

## 5. Scope and boundaries

This corollary is for the same irreversible nearest-neighbor exponential model, with finite second moment, unbounded support, minimum degree two, degree-only weak selection, and a fixed-degree independently chosen fast root. It covers every fixed positive lambda1<lambda2. It does not settle sharp budgets, optimal schedules, a fixed number of hubs, or adversarial roots chosen after viewing matching or clocks. If the degree law has leaves, the infinite ray used here can die and near-total occupation need not follow. If the second moment is infinite, the cited finite-dissociability corollary no longer supplies this proof. Neither infinite-mean power-law results nor random-regular competitive theorems are being treated as substitutes.

There remains bounded historical uncertainty about whether an even earlier paper states this strategic-start corollary explicitly. Such uncertainty cannot restore priority over the checked 2022 theorem implication.
