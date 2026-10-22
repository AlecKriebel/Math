# Independent audit: problem 30005026, rank 788

## Verdict and limits

PASS_SCOPED_WITH_NONBLOCKING_SOURCE_ERRATA. The written partial results withstand this independent audit. The original finite-valued problem remains UNRESOLVED, with all five approach families used. The countable-alphabet example refutes only the broadened catalog wording. It must never be labeled a solution or counterexample to the original finite-output problem.

Two source errata are specified exactly in CORRECTIONS.md. They can be supplied as an accompanying addendum without changing the frozen author package. This is an AI-assisted independent check, not journal peer review, a novelty determination, or a certification of the external literature theorems.

The audit was conducted from the frozen author ZIP identified in BINDING.json, without changing its bytes. All 10 manifest entries match. The original verifier passes with 141,484 exact assertions. A separately implemented reconstruction also passes 141,484 assertions, and an additional independent suite passes 46,913 assertions, including all 6,672 ternary maps on four finite binary-block supports and three rejected invalid relaxations. Counts are supplementary controls; the infinite-process conclusions require the arguments below.

## 1. Target and source interpretation

Question 8.3 on printed p.35 of Meyerovitch–Spinka's arXiv:2201.06542v1 explicitly assumes a finite-valued stationary process on Z^d and asks for a finite-valued IID source simultaneously having a small entropy surplus and exponential coding-radius tails. Spinka's report contribution supplies the setting on pp.447–449 and poses the simultaneous-efficiency question on p.449. Those pages and the decisive rendered question pages were inspected. The full catalog record omits the finite-output restriction. The primary target reconstruction is correct. [Primary question](https://arxiv.org/pdf/2201.06542v1), [report](https://ems.press/content/serial-article-files/46944).

The quantifier is: for each epsilon > 0 choose a source, law, alphabet, code, and positive tail constants. It does not request uniform constants or a uniform alphabet bound. Entropy means process entropy per site; it must not be replaced by the one-site marginal entropy for a dependent target. The original IID source can be countable or more general. The lower inequality h(X) <= H(Y_0) is entropy monotonicity, not an additional difficulty.

The report records a February 2022 workshop, and EMS dates publication to March 11, 2023. A bibliographic '(2023)' is compatible with that chronology. The frozen wording implying that the citation necessarily confuses these dates needs C1. [Publication metadata](https://ems.press/journals/owr/issues/2056).

## 2. Essential local determination and Proposition 1

Fix the law mu of a finite-alphabet source Y and the output observable f(Y)=X_0. A positive-probability cylinder [w] decides f exactly when the conditional law of f given that cylinder is a point mass. Define the essential radius as the least r whose witnessed B_r-cylinder decides f. This is a stopping radius: the event that it is at most r is a union of deciding B_r-cylinders. A cylinder of measure zero can be ignored.

For all r, all finite words, and all translated sites, there are only countably many relevant exceptional events. Remove their union. On the resulting invariant full-measure set every deciding cylinder has the asserted output. This makes the essential-radius convention compatible with local constancy on a full-measure domain and makes null-set modifications harmless. It would be incorrect to infer local determination merely because the map agrees at the single observed sample, or to require agreement on arbitrary null configurations outside the domain.

There are at most b^|B_r| source words, each with at most one decided output. The set S_r of those outputs therefore has that cardinality bound, and {R<=r} is contained, modulo a null set, in {X_0 in S_r}. Consequently P(R>r) >= T_p(b^|B_r|). No IID, independence of the radius, or stationarity is needed for this counting step. Any admissible coding radius is at least the essential radius almost surely, so the lower bound also applies to nonminimal coding radii. Proposition 1 passes.

## 3. Countable finite-entropy obstruction

The proposed law has group mass w_k=4/[k(k+1)(k+2)]. Direct telescoping gives total mass one, group tail 2/[K(K+1)], and E[K]=2. Each group has exactly 2^k equiprobable atoms.

The entropy claim can be justified without applying infinite relative entropy prematurely. Partition the group index into 1,...,n and a final tail atom. Compare that finite law with the geometric law 2^-k, similarly lumped. The finite Gibbs inequality bounds its entropy by the cross-entropy

sum(k w_k, k<=n) + n P(K>n) = 2 - 2/(n+1) < 2.

These finite partition entropies increase to H(K), so H(K)<=2. Conditional entropy inside group k is k bits, hence H(X_0)=H(K)+E[K]<=4. The frozen proof already first establishes finite H(K) before its relative-entropy comparison; the finite-partition argument confirms that no infinite-entropy circularity is needed.

For a set of at most M symbols, put K=ceil(log_2 M)+1. Every group k>=K has at least 2M atoms, so at least half its mass is missed. Thus T_p(M)>=1/[K(K+1)]. This argument needs no assumption about which atoms are largest. For the optional exact top-M controls, per-atom probabilities strictly decrease with k, with ratio k/[2(k+3)].

Substitution of M=b^((2r+1)^d) proves the frozen bound. For b>=2, K_r grows at most as a constant times (r+1)^d. Thus P(R>r)>=c_b,d (r+1)^(-2d), which excludes an exponential tail. In the integer tail formula for the 2d-th moment, the increments (r+1)^(2d)-r^(2d) are of order r^(2d-1), giving a divergent harmonic lower bound. For b=1 a positive uniform lower bound prevents finitariness itself.

The countable IID target is its own radius-zero source. It is therefore a valid finite-entropy counterexample to a formulation allowing countable output, even if the proposed finite-alphabet source is not IID. It lies outside the original finite-output target. Qualitative entropy-efficient finitary coding is compatible with this result because it promises no exponential tail for this recoding; the relevant countable-output extension is Theorem 1.2 of the entropy-efficient preprint, p.2. Proposition 2 passes.

## 4. Composition

On a common full-measure domain, deciding the intermediate outputs at all v in B_T and then the final output gives an admissible radius at most T+max_{v in B_T}S_v. If T<=r and S_v<=r for every v in B_r, the queried source sites lie in B_2r. The union bound gives the stated estimate, with stationarity replacing each marginal P(S_v>r) by P(S_0>r). No independence between these radii is used.

Let a=min(c_1,c_2)>0. The right side is at most [C_2+C_1(2r+1)^d] exp(-ar). The polynomial can be absorbed in a finite constant times exp(ar/2); taking r=floor(n/2) then yields a valid exponential estimate for every n. Proposition 3 passes. Entropy monotonicity correctly explains why simulating a pre-existing wasteful IID source cannot eliminate its entropy overhead.

## 5. Literature-dependent Markov subclass

Theorem 2 on p.3 of Harvey–Holroyd–Peres–Romik has the required finite alphabets, irreducibility, aperiodicity, stationary laws, strict entropy gap, and exponential tail conclusion. Section 5 is a literature proof sketch, not something this audit or the author independently proves. Its actual page extent is pp.28–31, requiring C2. [Author-hosted paper](https://www.math.ucdavis.edu/~romik/data/uploads/papers/expoplms.pdf).

Interpolating a point mass and a sufficiently large finite uniform law yields a full-support IID marginal whose entropy lies strictly between h and h+epsilon. Treating that IID process as a mixing finite-state Markov chain meets the source hypotheses. The claimed one-dimensional consequence follows. Applying the identical map separately on all first-coordinate lines preserves full Z^d translation equivariance, retains the one-dimensional radius law, and produces independent target lines. A side-n box contains n^(d-1) independent chain blocks, so division by n^d yields the one-dimensional entropy rate in the limit. Corollary 4 passes as a correctly restricted external-theorem consequence.

## 6. Periodic phase obstruction

Group sites of an IID field into L-sided cells. Under translations by LZ^d, the vectors of cell coordinates form another IID process, so that sublattice action is ergodic. Every phase fiber would be invariant under it and would have probability zero or one. A finite phase would then be constant almost surely. A unit shift must change it by a nonzero residue, contradicting invariance of a constant. Proposition 5 passes, including for a degenerate source. It only rules out an IID-derived global periodic phase, not nonperiodic marker schemes.

## 7. Uniform-tail compactness

At each radius there are finitely many finite-alphabet source words and finitely many possible records: a forced output or a star. Diagonal extraction is therefore legitimate. Every word over supp(p) has positive limiting probability and positive p_n probability for all sufficiently large n. Compatibility of nonstar records on nested such cylinders passes to the limit; if an inner record decides, every supported outer extension decides the same value.

The finite sum of cylinder probabilities for 'undecided at radius r' converges. Words using a symbol outside supp(p) carry vanishing total probability at each fixed radius. This proves the same Ce^-cr bound for the first-deciding-record construction. Countability of the lattice supplies an invariant full-measure domain where all sites are decided. The essential radius of the resulting map may be smaller, so it also satisfies the bound.

For any finite output set F, default-symbol truncation at radius r is a finite-coordinate function. Its law converges along the extracted subsequence. The probability it differs from the true output vector is at most |F|Ce^-cr, both before and after the limit. First passing n to infinity and then r to infinity identifies all finite-dimensional output laws. Continuity of Shannon entropy on a fixed finite simplex proves the entropy statement, even when source atoms vanish. Proposition 6 passes; a varying or countable source alphabet would invalidate this particular compactness argument.

For the prescribed ternary family, H(p(t))=H_binary(t)+(1-t) and its derivative is log_2((1-t)/(2t)), negative for t>1/3. There is exactly one t_* in (1/3,1) with entropy one. Positive ternary marginals at that point cannot be symbol permutations of a fair binary marginal. Theorem 1.2 of Gabor's publicly posted 2025 preprint supplies the excluded equal-entropy exponential factor, so compactness contradicts common tail constants for the approaching source family. The application uses finite marginals and meets the cited hypotheses. This remains an external-theorem corollary; the preprint was not independently proved or certified. [Preprint](https://arxiv.org/pdf/2509.06018v1).

The fair binary target can itself be used as an efficient source. Thus this prescribed-family example does not refute the original existential question. The package preserves that distinction.

## 8. Provenance, prior attempts, and reproducibility

All three complete local corpora were rehashed and parsed. Their byte counts and SHA-256 digests match the frozen metadata; the two upstream corpus hashes also match a freshly retrieved pinned repository manifest. The catalog's Git blob SHA-1 matches pinned directory metadata. The full target record, descriptor, statement hash, and canonical review hash were recomputed. The prior-report key is absent, so the join is the empty object. DATA_AUDIT.json records only metadata, not source records.

Independent all-state PR searches, exact branch and commit searches, and default-branch code search found no target-specific prior artifact. The complete immediate attempts-directory listing has 63 entries, is nontruncated, and contains no target directory. This is not a recursive reading of every unrelated attempt. The pinned queue shows 0/5 historically; the completed author's current budget is 5/5. Neighboring finite-mean and MRF-characterization questions have distinct targets. PRIOR_WORK_AUDIT.json preserves the bounded scopes and limits. These negative checks establish no novelty claim.

No current general resolution was located in the bounded source search. That is not proof of nonexistence. The live catalog page remains unverified. Published entropy-paper metadata was checked, but its published full text was not; the mathematical question is bound to the inspected arXiv version. All five stored source PDF hashes match. Decisive source renderings were viewed, and no source PDFs, extracts, images, raw corpora, or private coordination files are in this audit bundle.

Run verify_audit.py against the frozen author ZIP to validate the bundle, replay the author test, reconstruct its finite scope, and run the additional controls. Optional verify_inputs.py checks complete source inputs against the published metadata without redistributing their contents. No remote writes were performed. No sixth approach family or extension of the original search was undertaken.
