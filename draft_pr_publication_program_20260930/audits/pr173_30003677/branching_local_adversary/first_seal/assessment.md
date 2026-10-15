# Independent first assessment: local branching mechanism

Assessment written independently on 2026-10-12 UTC. Original PR head identified by assignment: `eb68ee2ecda39a8ec2748796d716c7a7598b7bc6`. Scientific inputs consumed so far are exactly the original `CANDIDATE.md` and `source_record.json`; their hashes are in `consumed_inputs.json`. No review, readiness, verification, root assessment, or other family material was read. This is an actual derivation and provisional assessment, before source-body verification.

## Exact hypothesis and scope

Let D be supported on integers at least 2, have finite second moment and unbounded support. Select all vertices of repaired degree at least a deterministic threshold k_n. A single competitor is selected uniformly among vertices of degree d0, with positive mass at d0. Two types have independent undirected edge traversal times Exp(lambda1) and Exp(lambda2), with 0 < lambda1 < lambda2 < infinity fixed. The proposed conclusion is occupation of fraction 1-o_P(1) by type 1 at deterministic times t_n tending to infinity but o(log n), while both seed-vertex density and seed-half-edge density vanish. This is a slowly growing seed-count existence theorem; no fixed-hub, sharp budget, or uniform-in-rate conclusion follows.

## 1. A noncircular finite-time branching calculation

Write mu=E[D], Q(d)=d P(D=d)/mu, B=D*-1, and nu=E[B]. The finite-second-moment assumption makes nu finite; the support condition gives B>=1. Define a genealogical branching tree with d0 initial active individuals. Each individual has an independent Exp(lambda2) lifetime, and on death produces B independent-mark children. For generation l (initial individuals have generation zero), the expected population count is d0 nu^l. Its expected number dying by T is

    d0 nu^l P(Gamma(l+1,lambda2) <= T).

This factorization is valid because the offspring determining existence of the individual is independent of the lifetimes on its ancestry. The gamma probability is at most (lambda2 T)^(l+1)/(l+1)!. Tonelli therefore gives

    E[number of deaths by T]
      <= d0 sum_{l>=0} nu^l (lambda2 T)^(l+1)/(l+1)!
      = d0 (exp(nu lambda2 T)-1)/nu < infinity.

Thus infinitely many events by T have probability zero. This constructs nonexplosion without first assuming the usual expected-population identity. Counting individuals alive at s instead gives, by the gamma survival convolution,

    E[A(s)] = d0 sum_{l>=0} nu^l exp(-lambda2 s)
                         (lambda2 s)^l/l!
            = d0 exp(lambda2 (nu-1)s).

The event expectation is exactly lambda2 integral_0^T E[A(s)] ds. Every event mark is a finite degree, so a finite event count gives finitely many revealed incident half-edges almost surely. The R-edge path has finitely many incident half-edges too, for each fixed R. Consequently the combined exposure amount has a probability-tight cutoff M. No log-time approximation has been derived or needed.

## 2. Empirical sampling and the conditioned root

For a degree list, Q_n(d)=d N_d/L_n, where L_n is its half-edge total. The weak law for D and pointwise empirical degree convergence give Q_n(d)->Q(d) for every fixed d. To see total variation directly, choose a finite set F with Q(F)>1-epsilon. Pointwise convergence on F gives both Q_n(F)>1-2 epsilon and sum_{d in F}|Q_n(d)-Q(d)|->0; the complement contribution is at most 3 epsilon asymptotically. Hence ||Q_n-Q||_TV->0 in probability. This uses finite first moment, with finite second moment supplying finite mean branching.

If at most M incident stubs have been exposed, one fresh partner in a uniform matching is uniform among remaining stubs. The distinction from the full empirical size-biased draw is at most a constant times M/(L_n-M), and matching to any already seen vertex has the same bound. For at most M such pairings the collision/reuse error is O(M^2/(L_n-M)); L_n>=2n. This bound requires the cutoff to count all incident stubs of every discovered vertex, not merely the number of vertices or events. Arbitrarily large discovered degrees are dealt with by taking M after the limiting tree is constructed.

Uniform selection of the degree-d0 root is handled before the exploration. N_d0/n->P(D=d0)>0. An independent uniform U equals W with probability 1/n. Given any exposed set of at most M vertices, a still-unselected uniform degree-d0 root hits it with probability at most M/N_d0=O_P(M/n). Selecting W first yields the same limiting tree because only its d0 stubs and one vertex are removed. No positive-degree-class mass is lost through that O(1/n) removal. Two sets of O(M) exposed stubs then yield asymptotically independent marks drawn from Q_n, and the conditioned root has deterministic degree d0.

## 3. Parity repair does not create a macroscopic perturbation

The repair increases one independent uniform vertex V by one only when the original total is odd. The number of degree-d vertices changes by at most two, L_n changes by at most one, and the empirical second moment changes by (2D_V+1)/n on the repair event. E[D_V]=mu, so the expected absolute second-moment change is at most (2mu+1)/n. This is stronger than the candidate's max-degree bound for this particular random repair. The size-biased unnormalized mass changes in l1 by 2D_V+1, so its normalized total-variation perturbation tends to zero. A selected degree-d0 root is the repaired vertex with probability at most 1/N_d0, hence cannot introduce a nonvanishing root mixture. These arguments assume V is independent and uniform as stated.

## 4. What the edge clocks actually justify

An undirected edge has one type-specific time for traversal from whichever endpoint infects first. It is not globally legitimate to treat two independent endpoint clocks for the same already internal edge as two independent edge weights. Nevertheless, the local claim needs only the no-collision part of the exploration: reveal each newly encountered vertex's incident partners, give each fresh frontier edge its independent type-2 Exp(lambda2) time, and start that edge clock when its infected endpoint is reached. Before any repeated discovered vertex or frontier target, the revealed graph is a tree and all frontier edges are distinct. The construction then agrees exactly with the stated static edge-weight FPP. Stopping at the first collision makes its failure probability O(M^2/n). Type-1 marks on the auxiliary R-edge path are independent because the path selection uses only the matching and auxiliary ordering, never weights. Reversing the path uses the same undirected marks. Thus the needed limiting process is valid even though a global two-endpoint-clock equality would need a separate argument.

## 5. The path estimate and the diagonal follow from this local limit

Fix k>d0. Along the limiting forward ray, subsequent degrees are independent Q marks and have hit probability p_k=Q([k,infinity))>0. The probability of no hit among R marks is (1-p_k)^R. The root's own possibility of being a seed can be omitted from this upper bound. The R path weights sum to G_R with mean R/lambda1, so P(G_R>T)<=R/(lambda1 T). On disjointness from the unopposed competitor ball at T, every vertex of the reverse seed-to-root route is inaccessible to type 2 through T. Induction along that route gives type-1 infection by T. This does not use a false global Voronoi comparison.

Therefore, for fixed k,R,T,

    limsup_n P(U is not type 1 by T)
       <= (1-p_k)^R + R/(lambda1 T).

For j>=2 take K_j=d0+j, R_j=ceil(j^2/p_{K_j}), and finite increasing T_j>=j^2 R_j/lambda1. The right side is <=2/j^2. A limsup bound implies an eventual bound <=3/j^2 uniformly for all n beyond some deterministic N_j. Increasing N_j to satisfy log N_j>=jT_j and n q_j>=4j^2 for every n>=N_j is allowed. Set J(n)=max{j:N_j<=n}. Then t_n=T_{J(n)} is o(log n), J(n)->infinity, and the missing fraction Z_n satisfies E[Z_n]<=3/J(n)^2 because an independent uniform test vertex samples the realized fraction exactly. Markov gives Z_n->0 in probability. There is no claim that vertex indicators are independent.

For seed counts, the original count is Binomial(n,q_{J(n)}), of mean at least 4J(n)^2 and variance at most its mean. Its probability of falling below half its mean is <=1/J(n)^2. Repair can only increase this count. The seed fraction has expectation at most q_{J(n)}+1/n->0. The original seed-degree total has normalized expectation E[D 1_{D>=k_n}]->0. The additional amount due to repair is at most D_V+1, with expected normalized size <=(mu+1)/n. L_n>=2n then proves vanishing seed-half-edge fraction.

## Provisional assessment and exact gaps

The local branching family has not produced a mathematical counterexample under the exact assumptions. Its strongest independently derived result is the fixed-(k,R,T) missing-probability estimate above, together with a complete route from that estimate to the asserted existential schedules and resource limits. The central universal stochastic step has a proof using genealogical expectation, a finite incident-stub cutoff, and deferred matching; simulation is unnecessary.

The candidate's expected-population sentence is terse and could look circular if read without the genealogical nonexplosion construction. The edge-clock paragraph should explicitly stop on repeated vertices/frontier targets instead of relying on a global endpoint-clock representation. These are proof-expansion needs, not an exhibited contradiction. Source-body access, precise compatibility with the primary paper's exponential convention, and the original source's permitted seed scope remain unverified at this seal. The historical novelty assertion is expressly outside this family's verification. The original source_record's bibliographic year/label inconsistencies are provenance warnings, not mathematical counterexamples.

Completion estimate at first checkpoint: 60% of this independent probabilistic-family audit; the main derivation is complete, primary-source access and a falsification/control record remain.
