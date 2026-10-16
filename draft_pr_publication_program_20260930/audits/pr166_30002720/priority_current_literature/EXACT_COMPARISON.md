# Exact scope comparison and an independent boundary deduction

Input candidate: stationary binary source μ=(1/2,1/2), p00=p11=3/4, p01=p10=1/4; independent strings; singleton-stopping bucket cost Y_n(floor(nt)+1). Its assertion is existence of one explicitly constructed, fixed t in (0,1), outside all cylinder endpoints and continuous for m∘h, with (Y_n−c_n)/√n non-tight for every deterministic real sequence c_n. The square-position word has ones at j² for j≥2. This is not a varying-rank assertion, an almost-everywhere claim or a random-centering claim.

| Evidence | Same operation/model? | Rank and centering | Relation to exact candidate |
|---|---|---|---|
| [LNS process v2](https://arxiv.org/pdf/1605.02352v2), equations(2)–(3), §2.4, Props2.8–2.10 and proof | Same independent positive Markov strings and singleton stopping | Dense fixed jump-boundary marginals; prescribed deterministic profile center. Separate random center converges | Prior obstruction; not a stated continuity-rank construction |
| [LNS2014](https://arxiv.org/pdf/1404.3672v1), §3.1, Theorem3.1 and proof outline, Theorem3.2 | Same Radix bucket cost | Mean asymptotic at nonboundaries; memoryless functional limit | Does not state the candidate obstruction |
| [2015 thesis](https://d-nb.info/107268702X/34), §5.2 relevant proofs, §5.3 theorem | Same Radix cost | Mean, worst case, whole process, grand averages | Checked quantile passages lack this fixed continuity-rank claim |
| [Ischebeck–Neininger2403.07685v2](https://arxiv.org/pdf/2403.07685), Theorem1.1, proof §§2.2–2.3; Cor1.5 proof | Pivot comparison costs, random partition intervals | √n residual about random limit; rank transfer also random center | Neither operation nor deterministic center matches |
| [Fill–Matterer2025](https://doi.org/10.1017/S0963548325100102), definitions §§1–2,4; Theorem5.1 and proof, Theorem6.1 | QuickVal comparison cost; Markov source costs permitted | √n(S_n/n−S), with coupled random S | Markov applicability does not identify Radix bucket cost or deterministic center |
| [GVR2604.22312v1](https://arxiv.org/pdf/2604.22312v1), baseline algorithm contract §§2.1–2.3 | Finite floating-point top-k GPU kernels | Temporal predictions, finite-array performance | Different mathematical target |
| [Sample-Guided2609.08450v1](https://arxiv.org/pdf/2609.08450v1), §§2.1–2.3 | Materialized FP32 rows, exact top-k indices | Sampling and full-row certification | No infinite-string fixed-marginal limit assertion |

Full PDFs were acquired for these comparisons. Complete relevant definitions/theorem/proof passages were used, rather than an abstract or search snippet. Acquisition of a full PDF is not a claim that every irrelevant proof in it was line-by-line verified. Additional primary author manuscript and accepted manuscript agree on the relevant LNS obstruction and open passage. The final published typeset LNS full text was not recovered.

## Boundary all-centers failure is already available from the prior mechanism

The following deduction is my explicit mathematical inference, not a verbatim theorem attribution. It isolates precisely which part of the candidate can be credited as additional.

In the candidate source, let a=00 111… and b=01 000…. These are the adjacent endpoint strings at τ=3/8: all strings beginning00 have probability (1/2)(3/4)=3/8. With q=3/4,

m(a)=1+1/2+3/8+(3/32)/(1−q)=9/4,
m(b)=1+1/2+1/8+(1/32)/(1−q)=7/4.

At the fixed rank proportion τ, the order statistic's side of the boundary has asymptotic probabilities1/2 and1/2 by the binomial CLT. Within either side, its arbitrarily long prefix agrees with a or b, respectively; m is continuous in prefix topology. These are the exact ingredients of the cited boundary proof. Proposition2.8's process tightness also implies that the supremum norm of the randomly centered √n residual is O_P(1): the supremum norm is continuous for the Skorokhod topology. In particular that residual divided by √n tends to0 in probability.

It follows that, for any fixed δ∈(0,1/4),

P(Y_n(floor(nτ)+1) ∈ n[9/4−δ,9/4+δ]) → 1/2,
P(Y_n(floor(nτ)+1) ∈ n[7/4−δ,7/4+δ]) → 1/2.

For example δ=1/16 leaves a gap3n/8 between these bands. For every fixed M>0 and every real a_n, an interval [a_n−M√n,a_n+M√n] intersects at most one band once n is large. Hence

limsup_n sup_a P(|Y_n(floor(nτ)+1)−a|≤M√n) ≤ 1/2.

Thus *every* deterministic center fails already at this boundary. The theorem's explicit quantifier over centers extends beyond the published displayed statement, but follows directly from the same two-band argument. It cannot by itself substantiate priority for the candidate.

At the square-word candidate rank, all finite prefixes contain the rank strictly in their cylinder interiors. There is no fixed jump at t. The candidate instead arranges nearby boundary distances o(w_j) and jump heights P_j with √n_j w_j→1 and √n_j P_j→∞. That extra relationship is the precise step not supplied by the checked boundary theorem: density of jumps alone gives no required height/distance comparison at one fixed continuity point. Whole-process non-tightness alone also supplies no such marginal. This scope distinction does not independently verify the candidate's complete proof.

The OWR and later open sentence leave the quantifier convention implicit. Reading the latter as a classification, an almost-everywhere question, or a continuity-rank question is an interpretation. This audit does not attribute any of those refinements as an explicit original statement. The candidate excludes deterministic centers at one continuity rank; it leaves typical ranks, classification and data-dependent centers unresolved.
