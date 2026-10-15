# PR173: testable older-theorem reduction

Recorded 2026-10-12, after the three priority families' first substantive seals. This is ROOT's additive derivation, not a claim of pre-feedback independence: the configuration/multiseed family alerted ROOT to Ganguly–Ramanan and to the bounded-multiplicity reduction. ROOT then read the actual v1 theorem, rate assumptions, graph definitions, and finite-dissociability argument. Publication and disposition remain pending an independent falsification attempt.

## Exact hypothesis and old dependency

For the exact repaired PR173 statement (IID integer D>=2, unbounded support, finite second moment; fixed positive rates; all degree>=K vertices initially weak and one uniformly degree-d0 vertex initially fast), the existence of deterministic growing thresholds and sublogarithmic growing observation times with weak occupation tending to one is a corollary of Ganguly–Ramanan, arXiv:2205.01587v1 (3 May 2022), Theorem 4.6, Corollary 4.7, and Corollary 5.16. This is an implication claim. The old paper need not print the identical hub-selection proposition. No conclusion about sharp seed budgets or the complete strategic-placement programme follows.

ROOT consumed v1 section 2.4 (simple marked graph topology), section 3.1 and the Poisson dynamics definition in 3.2, Assumptions 1 and 2, Definition 4.4, Theorems 4.5–4.6, Corollary 4.7 and its proof, Example 4.8, Definitions 5.9–5.11, Proposition 5.15 including its proof and Corollary 5.16 including its proof. Other proof sections of the 53-page body have not been claimed fully read by ROOT. The PDF is retained privately with SHA256 05fcbfc2a3ddc6bafd54be1b22244a9d843e68b174d8ffb34a696aca1f3aa3ca, 745608 bytes; no raw response headers were retained.

## 1. A bounded marked-simple-graph encoding

Erase self-loops, which cannot change any color. Replace each non-loop bundle by one undirected simple edge carrying the discrete multiplicity mark min(m,2). Retain each vertex's actual (parity-repaired multigraph) degree as a discrete mark. For fixed K, initial colors are 1 on degree>=K vertices, 2 at the degree-d0 fast seed (take K>d0), and 0 otherwise. Set X={0,1,2}, J={1,2} and give each jump type mass 1/2 in the driving measure. Define

    r_j(v,x) = 2 lambda_j 1{x_v(t-)=0} sum_{u~v} min(m_uv,2) 1{x_u(t-)=j}.

The factor 2 compensates for the probability measure on J in equation (3.3); the actual transition intensity is lambda_j times the number of infectious edge channels. These predictable local rates are invariant under marked graph isomorphism, measurable, and bounded by C_{k,T}=4 max(lambda_1,lambda_2) k for a closed neighborhood with k vertices. Marks are discrete, so Assumption 2 holds. The same bounds apply on every graph in the marked-simple-graph model, not merely with high probability on sampled inputs.

Static independent type-specific exponential edge delays have the same finite-graph color-process law as these Markov rates: each eligible edge/type clock has exponential residual waiting time; clocks become irrelevant when a target is colored. There is no identification of two directional clocks for an edge that could recolor vertices. Color states are absorbing. This is equality in distribution, not pathwise identity of independent global constructions.

## 2. Why capping at two preserves the original model with probability tending to one

Let L=sum_i d_i, S2=sum_i d_i^2 and Delta=max_i d_i for actual repaired degrees. IID finite second moment implies L/n->mu>0, S2/n->E[D^2] and Delta/sqrt(n)->0 in probability; adding one stub at one uniformly chosen vertex changes these by negligible amounts. The repair contribution to S2 is 2D_V+1, which divided by n vanishes in probability; its effect on Delta is at most one.

Conditional on the degree list, the expected number of unordered triples of edges joining distinct i,j is exactly

    sum_{i<j} (d_i)_3 (d_j)_3 / [6 (L-1)(L-3)(L-5)]

when L>=6. Choose three stubs at each endpoint and one of 3! pairings; their appearance probability is the reciprocal of the displayed three odd factors. Since sum_i (d_i)_3 <= Delta S2, this expectation is bounded by a constant times Delta^2 S2^2/L^3 on L large. The bound is o(1) in probability on typical degree lists. Conditional failure probabilities are bounded by min(1, this expectation), whose expectation tends to zero. Thus no triple parallel bundle occurs with probability tending to one. The capped process agrees with the original color process on that event, for every observation time. We do not condition the configuration model on being simple or discard double-edge channels.

## 3. Initial marked local convergence, including the conditioned singleton

For each fixed K, the empirical marked rooted neighborhoods converge in probability to UGW(D), with vertex degree marks equal to actual tree degrees, every edge multiplicity mark one, and initial color 1 exactly when degree>=K; there are no color-2 vertices in the limit. The usual finite two-root configuration-model exposure proves convergence in probability: truncate all incident stubs in the exposed fixed-radius neighborhood, use convergence of the empirical size-biased degree law and the vanishing finite-exposure collision probability, then remove the cutoff. The parity repair changes one local mark and one stub, with negligible probability of entering such a truncated exploration.

The degree-d0 class has size n P(D=d0)+o_p(n). Conditional on degrees and matching the fast root remains uniform in that class. For a uniform observed root U, any fixed-radius ball has tight size by local convergence; truncate to at most M vertices. On the event that the class size is at least n P(D=d0)/2, its chance of meeting the fast root is at most 2M/[n P(D=d0)]. Let n->infinity and then M->infinity. This proves that the singleton color mark disappears from every empirical local test. It does not assert that the singleton is globally absent, or that finite-n competing infections have independently assigned final distances.

The countable common vertex-label set may be N. Finite initial graphs are finitely dissociable. The limit is finitely dissociable by Corollary 5.16 because E[D^2]<infinity. Thus Theorem 4.6 and Corollary 4.7 apply to the encoded process, despite unbounded degrees and non-IID degree-selected initial marks.

## 4. Fixed-time consequence and eventual occupation on the limit tree

At each deterministic finite T, a limit vertex has no jump exactly at T: its degree is finite and its rates are bounded by a finite constant on its fixed local neighborhood. Evaluation at T is therefore almost surely continuous under the trajectory law. Corollary 4.7 and the continuity-set version of weak convergence imply that the fraction weak at T converges in probability to p_K(T)=P(X_root(T)=1).

There are no fast vertices anywhere in the limiting marked tree, so this is the one-type irreversible infection process at positive rate lambda_1. Because D>=2, each non-root vertex has at least one child. Choose an infinite ray by the first child in a random enumeration independent of degrees and infection clocks. Non-root degrees along it are IID D*. For every finite K, q_K=P(D*>=K)>0 by unbounded support. Almost surely some finite vertex on this ray is initially weak. A finite path from that seed to the root has finite total exponential passage time almost surely. The monotone process therefore colors the root by some finite random time. Consequently p_K(T)->1 as T->infinity.

## 5. The elementary slow diagonal supplies the exact n-varying claim

Choose K_j=d0+j and nondecreasing deterministic T_j>=j tending to infinity so that p_{K_j}(T_j)>=1-j^(-2). Let a_j=P(D>=K_j)>0. Fixed-time convergence gives deterministic increasing N_j so that for every n>=N_j, the probability that weak fraction at T_j is below 1-2/j is at most 1/j. Enlarge N_j to ensure log N_j>=j T_j and N_j a_j>=j^2. Define J(n)=max{j:N_j<=n}, k_n=K_{J(n)}, t_n=T_{J(n)} (finite initial n may use any admissible convention). Then J(n)->infinity, k_n,t_n->infinity, t_n/log n<=1/J(n), and the weak occupation fraction tends to one in probability.

The original IID count of degree>=k_n seeds has expectation n a_{J(n)}>=J(n)^2; binomial variance is at most its mean, so the count tends to infinity in probability. Its vertex fraction tends to zero because a_j->0; its initial stub mass divided by L tends to zero because E[D 1{D>=K_j}]->0. The parity repair changes seed count by at most one and stub-tail sum by at most D_V+1; this divided by n vanishes in probability. The original conditioned degree-d0 seed exists with probability tending to one. The small missing-class convention does not affect any stated limit.

## Adversarial checks still required before disposition

Check the exact probability-measure normalization of jump types, all-graphs rate bound, global triple-bundle estimate under only a second moment, actual-degree marks at truncated boundaries, empirical convergence in probability rather than one-root annealed convergence, and whether source revisions repair a relevant v1 theorem defect. Challenge the claimed implication from the exact earlier theorem, not a proxy single-source heuristic. If accepted, this supports crediting an earlier general theorem and treating PR173 as an elementary independent proof of an already implied existence result, not alleging that the exact hub-selection theorem was printed verbatim in 2022. No sharp or fixed-budget novelty is present in the original candidate.

## Separate source limitation: all-path local reachability

The current author-hosted Epidemic Forecasting on Networks manuscript's equation (9) requires a supremum over all simple paths, stronger than PR173's one chosen ray. It cannot be automatically applied to degree-threshold marks. For the candidate's concrete even-geometric law P(D=2m)=2^(-m), mu=4, the offspring count of unseeded vertices for threshold K=8 has mean sum_{d<8}(d-1)P(D*=d)=1/4+3/4+15/16=31/16>1. The resulting unseeded subtree survives with positive probability from an unseeded root. On that event there are arbitrarily long seed-free paths and their conditional probability of avoiding the deterministic initial seed set is one. Thus the all-path condition need not hold. This does not falsify PR173 or the Ganguly–Ramanan reduction; it excludes that different shortcut.
