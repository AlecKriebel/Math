# FIRST_CONCLUSION — independent graph proof adversary

Recorded UTC: 2026-10-04T16:25:09.151331+00:00

## Verdict and exact boundary

**CONDITIONAL GRAPH ARGUMENT VALID.** I did not find a counterexample or a universal gap in the graph argument, conditional on the exact imported formula (4), its endpoint patterns P and T, and its once-per-three-element-subset convention. The formal signed arrow evaluation obeys the advertised bound for every directed chord diagram, including nonrealizable diagrams and arbitrary crossing signs. This is a mathematical derivation, not an extrapolation from finite computation. No computation has yet been used to reach this first conclusion.

This does **not** independently certify that formula (4) computes the normalized classical knot invariant v3. That is the exact remaining bridge. A defect in the primary formula transcription, normalization, or embedding multiplicity could invalidate the knot conclusion while leaving this graph lemma intact. Primary target matching and literature priority are also outside this graph verdict. The root reports authenticated original head 78f4a7fadac0fd24e147a617956cb409eb6a579e; I have not read that original checkout or independently authenticated it.

## Freshness and inputs

Before this conclusion I read only the three authorized files in fresh_restricted_mathematical_inputs_20261004: CANDIDATE.md, source_record.json, and MANIFEST.json. Their hashes are recorded below. I have read no original checker, original research notes, sibling reports, root mathematical assessments, or primary-source material. The authorized source_record.json itself contains upstream historical/open-status text under prior_upstream_report; that text supplied no graph proof assessment, was not relied on, and was not treated as an independent mathematical result. This is disclosed because the authorized package was described as opinion-free although its source-record metadata contains status opinions.

- CANDIDATE.md: 9121 bytes; SHA256 fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698.
- source_record.json: 3676 bytes; SHA256 075059240df7ba3bfac89aaf96f8f9fb176b12b61e6e7f7fdd1f8e1d93a8d4bc.
- MANIFEST.json: 407 bytes; SHA256 03a83fe5ce419e0c454b1843f72888dccff752cda3cc94d1cd066e54bf030660.

## Independent universal derivation and falsification attempts

1. **Antisymmetry.** Rotate the circle so the tail of c is first. An intersecting pair has one of the endpoint orders (t_c,t_d,h_c,h_d) or (t_c,h_d,h_c,t_d). In the first case t_d lies in the positive open arc from t_c to h_c, while t_c lies outside the positive arc from t_d to h_d. In the second case both statements reverse. Thus precisely one of c→d and d→c holds. Endpoints of distinct crossings are distinct, so the open-arc boundary cannot produce a tie. This exhausts all alternating orders with arbitrary arrow orientations.

2. **P.** With c=(3,0), a=(5,1), b=(2,4), the endpoint order is h_c,h_a,t_b,t_c,h_b,t_a. The intervals for c and b contain t_a and t_c, respectively. The only alternating pairs are {c,a} and {b,c}; hence b→c→a. The pair {a,b} has endpoint order h_a,t_b,h_b,t_a and is nested, so the third edge is absent. Rotating endpoint labels does not affect alternation or arc membership.

3. **T.** With c=(3,0), a=(1,4), b=(5,2), the endpoint order is h_c,t_a,h_b,t_c,h_a,t_b. All three pairs alternate. Their arc memberships give c→b, b→a, a→c, a directed cycle. Reversing the oriented circle complements membership in each positive arc, reversing all edges and preserving the path/cycle properties.

4. **Once-per-subset counting.** Define P(S) and T(S) as Boolean isomorphism predicates on unordered three-crossing subsets. Their intersection graphs have two and three edges, so they are disjoint. Cyclic symmetries of a pattern do not create further subsets. This step is valid as a definition of the formal sum; whether the primary imported formula uses this exact convention remains an external dependency.

5. **Completion probabilities.** Independently orient absent pairs by fair coins. For each unordered triple S use one cyclicity indicator I_S. For T(S), E[I_S]=1. For P(S), the unique absent edge either closes the fixed directed two-edge path or produces a transitive triple, so E[I_S]=1/2. Every other triple contributes a nonnegative expectation. No assertion that all paths are P or all cycles are T is necessary. Correlation between indicators for overlapping triples cannot invalidate linearity of expectation. Independence among missing-edge coins is a sufficient construction; only the relevant missing-edge marginal is needed for each P contribution.

6. **Signed domination.** For signs ε_c=±1, let F=1/2 Σ_{P(S)} product ε_c + Σ_{T(S)} product ε_c. Triangle inequality gives |F|≤N_P/2+N_T≤E[C]. Cancellation, mixed signs, and unrealizable sign assignments cause no problem. No integrality of F is required for this step.

7. **Degree identity.** In any tournament, a transitive triple has exactly one vertex pointing to both others, while a cyclic triple has none. Counting these ordered choices gives C=binom(n,3)−Σ_i binom(d_i,2), with Σ_i d_i=n(n−1)/2. Set μ=(n−1)/2. Then Σ d_i²=Σ(d_i−μ)²+nμ². Direct substitution yields C=n(n²−1)/24−(1/2)Σ(d_i−μ)². The derivation is valid for n≥1 and also formally works for n=0 with an empty sum.

8. **Floors and expectation.** Every deterministic tournament has an integer cycle count bounded by the real number B=n(n²−1)/24. Therefore every completion has C≤floor(B), so E[C]≤floor(B). This does not round the expectation downward without justification: the integer rounding occurs pointwise before averaging. Combining the preceding inequalities gives the claimed universal bound for F.

9. **Even n.** If n is even and n≥2, μ is a half-integer and each integer d_i has (d_i−μ)²≥1/4. Consequently C≤B−n/8=n(n²−4)/24. For n=2k this number equals k(k−1)(k+1)/3, an integer because one of three consecutive integers is divisible by 3. For n=0 the empty diagram and empty tournament have value zero. For n=1 and n=2 there are no triples and the stated bounds are zero. For n=3 the general bound is 1. Thus the small cases introduce no missing exception.

## Remaining work and completion estimate

At this checkpoint: **80% complete toward this assigned graph audit** (universal proof review completed; independently written finite diagnostics, receipts, final inventory and adversarial report remain). The overall knot-discovery completion percentage is not assessed here. This graph route does not transfer its central difficulty to an unsupported graph claim. It does depend explicitly on the independently audited primary arrow-formula bridge. No publication, priority, or solved-label decision is made by this report.
