# PR173 ROOT mathematical reconstruction (preliminary)

The exact hypothesis is the candidate's existential theorem for IID unbounded integer D with D>=2 a.s. and E[D²]<infinity, one degree-d0 fast root chosen independently of matching/weights, and all degree-at-least-k_n vertices initially slow. The proposed conclusion is a deterministic sufficiently slow k_n,t_n tending to infinity, t_n=o(log n), with vanishing seed vertex/half-edge fractions but slow occupation fraction tending to one in probability. No fixed hub count, polynomial budget, adversarial graph-dependent fast root, bounded-support degree law, or general passage-time claim follows. These are material scope restrictions, not hidden universal extensions.

ROOT read the complete original CANDIDATE.md and source_record.json, the full OWR contribution on printed3442–3443, and arXiv1711.02902v1 pp1–8 and pp12–16 (model, assumptions, complete initial coupling, ending proof/future-work/references). It did not read original review/verifier verdicts. While this reconstruction was being developed, two independent families sent sealed first-assessment summaries. This ROOT record is therefore not represented as a blinded or pre-feedback first assessment. Independent family seals remain separate evidence.

## Pathwise protection, without a Voronoi shortcut

Actual type2 infection genealogy yields a walk from w with total X2 traversal cost equal to its infection time. Nonnegative costs allow loop erasure; every actual fast vertex through T is in the unopposed X2 ball B2(T). If every vertex of a slow seed-to-v path avoids this entire ball and the sum of its X1 costs is <=T, then induction along the path forces type1 arrival no later than the cumulative sums. An earlier type1 arrival only helps; a type2 arrival through T is impossible. This reasoning is valid on multigraphs, for loops and parallel channels and nonnegative weights, including zero weights under any consistently resolved simultaneous events. The stochastic model uses continuous positive exponentials, so stochastic ties have probability zero. Comparing only dist1(S,v) and dist2(w,v) would fail when the slow minimizing path is blocked at an intermediate vertex.

## A noncircular finite-time localization derivation

Write mu=E[D], nu=E[D(D-1)]/mu, finite and >=1. In the limiting locally tree-like graph rooted with degree d0, the expected number of generation-r vertices is d0*nu^(r-1). For any particular generation-r path, its r independent Exp(lambda2) costs satisfy

P(sum<=T) <= (lambda2*T)^r/r!.

This follows directly by integrating the joint density over the positive simplex, bounding its exponential factor by one. Consequently the expected total number of vertices reached by time T is bounded by

1 + sum_(r>=1) d0*nu^(r-1)*(lambda2*T)^r/r! < infinity.

There are therefore finitely many reached vertices almost surely, and their incident degrees are finite almost surely. This proves nonexplosion and tight incident-stub cutoffs without first assuming that an infinite-population process is well defined. The expectation formula for active stubs in the candidate is standard and compatible, but a paper should include this short noncircular justification or an explicitly localized branching-process proof.

An alternate route to the joint statement uses fixed unweighted-radius explorations. For a finite degree list with total L_n and A_n=sum_i d_i(d_i-1), conditioned degree-d0 root, expected simple paths of length r from it are bounded by

d0*(A_n/(L_n-2r))^(r-1)

for fixed r and sufficiently large n. This overcounts distinct choices and uniformly bounds the remaining pairing denominators; endpoint selections may be summed without enforcing distinctness, making it an upper bound. Exponential weights are independent of every such simple path. The probability that B2(T) exits the unweighted radius-r neighborhood is thus at most the same path bound times (lambda2*T)^r/r!: any exit has a shortest nonnegative-weight simple path with an r-edge prefix costing at most T. For n tending to infinity, A_n/L_n tends to nu in probability; restrict to a degree-law typical event with bounded ratio, then send r to infinity. Fixed-radius neighborhoods and the fixed R-edge ray contain finitely many stubs in the limit; cutoff M gives collision probability O(M²/n), and the degree-d0 root class has asymptotic positive density. Thus their vertex sets are disjoint with probability tending to one. This also avoids assuming a growing-time branching approximation.

The half-edge exploration in the candidate can instead be localized directly. Until a partner is an already discovered vertex/frontier, an edge gets its type2 clock from its first reached endpoint only; static undirected edge clocks and active-half-edge clocks agree. Frontier collisions must be stopped explicitly, rather than claim a finite cyclic graph has independent clocks at both ends of the same edge. Their probability vanishes under the finite incident-stub cutoff. Type1 costs on the fixed ray are independent of matching, degree-based ray selection and type2 costs.

## Degree conditioning and parity

The IID empirical law and first/second moments converge to those of D by laws of large numbers applied to D and D². The one uniform-vertex parity repair changes only one degree. The normalized second-moment change is at most (2max_i D_i+1)/n, tending to zero. In fact n*P(D>epsilon sqrt(n)) <= E[D² 1_(D>epsilon sqrt(n))]/epsilon² tends to zero, proving max_i D_i=o_P(sqrt(n)). The degree-d0 class still has asymptotic density P(D=d0)>0. Empirical size-biased masses converge pointwise and have total mass one; truncation of the countable probability space yields total-variation convergence in probability. Sampling boundedly many partner stubs without replacement versus with replacement has vanishing discrepancy. Root U may equal W or be a seed, but equality costs o(1), while being a seed helps the bound.

## Fixed parameters, diagonalization and resources

For fixed k>d0, R and T, the ray's R nonroot degrees have IID D* limiting law. Failure to encounter a seed is (1-p_k)^R; the full ray X1 sum has mean R/lambda1, so Markov gives at most R/(lambda1 T). The joint disjointness error is o(1) only for fixed parameters. Hence the candidate's limsup inequality follows from the path lemma.

Choose K_j=d0+j, R_j=ceil(j²/p_j) and monotone finite T_j>=j²R_j/lambda1. Both fixed-parameter errors are <=1/j². A limsup <=2/j² guarantees a deterministic N_j for EVERY n>=N_j with total error<=3/j². Increasing N_j to meet all additional finite inequalities cannot harm that guarantee; strict increasing N_j has no finite accumulation. On intervals N_j<=n<N_(j+1), choose the j parameters. Then J(n) tends to infinity and T_j/log n<=1/j. This never substitutes growing parameters into a fixed-time limit.

For an independent uniform U, conditional chance of missing type1 is exactly Z_n=1-N1/n, even though infection indicators are dependent. Thus E[Z_n]<=3/J(n)² and Markov proves Z_n to zero in probability. Initially the unrepaired seed count is Bin(n,q_j), its mean>=4j² and variance<=mean. Chebyshev gives count>=mean/2 with failure<=1/j²; parity only increases the count, so it diverges. Its expected density is <=q_j+1/n to zero. Tail incident-degree expectation E[D 1_(D>=k_n)] tends to zero by finite mean; crossing the cutoff after repair adds at most D_repair+1, with expected normalized size <=(mu+1)/n. Full degree total>=2n then gives vanishing half-edge fraction. No independent-vertex concentration claim is needed.

## Original source alignment and remaining gate

OWR57/2017 printed3442 explicitly permits growing initial populations and degree-based selections before asking the weaker-versus-stronger high/low-degree possibility question. The same open question is arXiv1711.02902v1 Section5, printed15; its fixed-initial-set main theorem and fixed-set remark do not contradict this candidate. The exact traversal model is printed2 and the parity repair is permitted there. Unbounded support is an added hypothesis giving diverging degree-selected seeds; a theorem for that nonempty class can witness an existential possibility, but is not a universal characterization for every finite-variance law. Source curation's 2018/2019 report labels require correction to Report57/2017.

Preliminary ROOT conclusion: the written mechanism appears to establish the candidate's stated existential growing-seed theorem. It needs precise full source/scope checks, independent complete-family reviews and finite-check reproduction before mathematical clearance. Historical novelty has not been assessed or accepted. Audit-time alternate localization proof above is a verification route, not a new published theorem. Case remains preliminary, estimate15%; programme34/dated99=34.34%,19published; no MAIN writer authority.
