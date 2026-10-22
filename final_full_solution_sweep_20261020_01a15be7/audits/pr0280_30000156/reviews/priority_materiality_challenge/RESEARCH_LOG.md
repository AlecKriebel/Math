# PR280 independent priority/materiality challenge

Scope: adversarially test the inference that the candidate has no new mathematical increment because it is a direct consequence of existing literature. This is an evidence review, not historical novelty certification or publication clearance. Write scope restricted to this folder; no Git, PR, Sheet, or Zenodo mutation; no external contact.

## Checkpoint 1 — 2026-10-21T02:55:25.181934+00:00 — 25% complete

Read the pinned SOURCE_SNAPSHOT and original RESULT.md/PROOF.md. Verified every captured file against its pinned SHA-256. Did not read other priority reviews or inherited audit verdicts.

Independent reconstruction: on p=3 mod 4, each fiber multiplier a=u²+1 is nonzero. Points with v=0 have period 1; all other points have period ord(a). With N=p−1, every proper divisor of N is at most N/2, and for fixed x in [1/2,1), N>px eventually. Therefore D_p(x)=1−(p−1)P_p/p² exactly eventually, where P_p counts primitive values u²+1. Any standard estimate P_p=p·phi(N)/N+o(p) implies D_p(x)=1−theta_p+o(1).

Independent subset lemma: if the empirical distribution of theta_p over all primes converges weakly to an atomless probability law, theta_p cannot converge along a subset of positive relative prime upper density. If theta_p→a along such a subset S and delta=limsup pi_S(X)/pi(X)>0, then every closed interval [a−epsilon,a+epsilon] has limiting-law mass at least delta (Portmanteau, taking the same X subsequence); continuity from above yields an atom of mass at least delta at a, contradiction. The fixed class 3 mod 4 has density 1/2. This implication is valid without any independence of residue class and theta_p.

This qualitative argument alone does not give the numerical gap 23/24 or limsup D=1. Those require separate arithmetic input: Dirichlet/CRT yields theta→0 in the class; an explicit mean or distribution-mass bound is needed to force theta≥1/24 infinitely often. Next: verify primary-source hypotheses and locate exact earlier application, if any.

## Checkpoint 2 — 2026-10-21T02:59:09.633027+00:00 — 75% complete

Read and visually checked the key complete primary pages: BCST arXiv1803.01435v2 p.3 (definitions, eqs.(5)–(6), Lemma1); O&S arXiv0902.3884v3 p.2 (family construction); DH published p.78 (Prop2.1), plus extracted p.79; Vivaldi's full two-page author contribution; MP published pp.255 and 262–263 (mean specialization and its unconditional proof). Reading receipts and SHA-256 hashes preserved in SOURCE_RECEIPTS.json. No core source access failed.

Verified BCST specialization: e1=1,e2=p−1, Q=t²+1 meets a≠0 and discriminant≠0 for every odd p. Its N(1,p−1) excludes input zero; Q(0)=1 is nonprimitive when p≥3, so N equals the candidate's P exactly. Lemma1 gives the required p·theta+o(p) estimate.

Verified O&S specialization: m=1, g0(t)=t²+1,h0=0,a=1,b=0. Its map is ((X1²+1)X0,X1); exchanging coordinates conjugates it to the candidate. The generic family is prior art; this source did not isolate the exact counterexample application in the portions read/search-scanned.

Verified DH law: g(n)=phi(n)/n meets all three series conditions because log(1−1/ell)=O(1/ell), and continuity follows from divergence of the reciprocal sum over odd primes. m=2 gives the empirical law over all odd primes; no residue-class independence is needed for the subset lemma.

Explicit gap audited separately: the three-source qualitative chain alone does not quantify 23/24. The already-cited MP mean A and fixed-modulus prime distribution do; indeed if b=limsup theta on class3, then A≤1/4+b/2, so b≥2A−1/2≥1/12 using A≥7/24. Hence liminfD≤11/12, stronger than 23/24. Dirichlet/CRT supplies limsupD=1. No new analytic input is necessary for the coarse gap.

Bounded historical search (8 targeted query strings so far) located no exact earlier target application. Provisional assessment: the implication from known theorems is valid and technically elementary, but this is insufficient by itself to assert that no newly synthesized problem-specific corollary exists. Distinguish low technical increment from verified historical duplication. Final step: record checkable full derivation, scope/limitations and the precise unresolved historical/materiality gap.

## Final checkpoint — 2026-10-21T03:03:29.486031+00:00 — 100% of this independent evidence challenge complete

Completed DERIVATION.md, ASSESSMENT.md, SOURCE_SCOPE.md and SEARCH_LOG.md. Visually checked complete DH printed pp.78–79 and MP pp.262–263, in addition to the earlier BCST and O&S key pages. All core sources were accessible; unread alternatives explicitly distinguished from failed access. Sixteen targeted exact-application queries located no verified earlier version of the target dynamical conclusion.

Strongest verified outcome: the full candidate theorem follows unconditionally from known inputs with elementary specialization; the atomless-law route even excludes convergence after any positive-density thinning of the admissible class. The old mean provides a stronger coarse liminf bound 11/12. No exact earlier target application was found. Therefore the evidence supports low technical novelty, while a categorical claim of historical duplication or zero application-level increment remains unproved. Exact remaining gap: historical priority of the specific application and an explicit project materiality criterion. No publication package or clearance was attempted.

All writes stayed in this assigned folder. No Git, PR, Sheet, or Zenodo mutation occurred. No other priority agent/review was consulted. The parent received only internal progress reports.
