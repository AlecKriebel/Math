# Independent actual-outcome gate: PRs 1151–1200

Recorded 2026-10-17T16:29:45.829541+00:00. Completion estimate: 100% for this outcome-identification subtask.

Read every pinned local PR body and metadata record in this range without consulting QUEUE.md or another classifier. This gate identifies recorded claims only; it does not validate mathematics, priority, or publication readiness. No PR mutation, external message, publication, commit, or mathematical audit was performed.

**Eligible explicit full-solution claims: #1151 and #1155.** Generic novelty/priority disclaimers do not negate their full target claims. Their mathematics and priority still require independent auditing.

Counts: 2 explicit full claims; 40 scoped/partial/unresolved outcomes; 8 credited prior full resolutions; 0 missing outcome records.

Scoped-prior boundary cases #1168 and #1198 were checked against pinned ACCEPTANCE.json and README.md. Both exclude a newly claimed full original solution. Each also credits prior work for the accepted scope. STATUS.json was absent at each pinned problem path; retained fetch errors document that absence.

## Per-PR evidence

### PR #1151: explicit_full_solution_claim

Problem 30003321; pinned head `a10129f4c09a87460642c36284f300d46d419cab`.

Full affirmative resolution expressly claimed for the targeted discrete additive-group question. Generic novelty disclaimers do not attribute this resolution to prior work.

`evidence/pr1151/PR_BODY.md:3`:

> Every discrete initial ordered additive subgroup of the surreal numbers No is order-group-isomorphic onto an initial subgroup of the omnific integers Oz. The statement covers sets and proper classes in NBG with global choice, including the trivial group. Initiality refers to sign-sequence prefixes. Multiplicative closure and preservation of the original simplicity order are not required. The known discrete initial subdomain theorem is not being substituted for this group result.

`evidence/pr1151/PR_BODY.md:1–9`:

> ## Full affirmative additive-group result
> 
> Every discrete initial ordered additive subgroup of the surreal numbers No is order-group-isomorphic onto an initial subgroup of the omnific integers Oz. The statement covers sets and proper classes in NBG with global choice, including the trivial group. Initiality refers to sign-sequence prefixes. Multiplicative closure and preservation of the original simplicity order are not required. The known discrete initial subdomain theorem is not being substituted for this group result.
> 
> The complete proof obtains a minimum exponent -alpha and bottom coefficient group 2^(-n) Z from discreteness. A transfinite sign rotation moves the minimum to zero without creating right-predecessor obligations; scaling the bottom coefficient group gives Z. The canonical Hahn-image characterization then gives initiality, and the Oz normal-form criterion gives containment.
> 
> The independent internal AI audit accepts the full stated argument without a mathematical correction. Its complete explicit inverse, all prefix and cross-branch cases, empty tails, arbitrary limit ordinals and successors, canonical Hahn-characterization hypotheses, bottom-unit-monomial normalization, and proper-class bookkeeping are retained. The construction transports only source series and does not silently complete the group to a full Hahn product.
> 
> The imported source results are from Philip Ehrlich and Elliot Kaplan, [Number systems with simplicity hierarchies: a generalization of Conway’s theory of surreal numbers II](https://doi.org/10.1017/jsl.2017.9), JSL 83 (2018), 617–633. The target is Question 9.1 in the [authenticated author manuscript](https://elliotakaplan.github.io/Number_systems_with_simplicity_hierarchies_II.pdf) and Question 1 in the Kaplan–Ehrlich contribution to [Oberwolfach Report 60/2016](https://ems.press/content/serial-article-files/46663). Source dependencies were checked against that author manuscript, not a byte-authenticated publisher PDF. Public metadata retain the source hashes, byte counts, retrieval and inspection history, and precise source-version qualifications.

Scope note: Generic no-novelty/priority certification disclaimer does not negate the explicit full target-result claim; this gate performs no priority audit.

### PR #1152: explicitly_prior_full_resolution

Problem 30001214 / OWR-3397-002; pinned head `88ea2f29062814da760a1056c71a7dfb4b1d9fed`.

The negative resolution expressly credits Bell–Launois–León Sánchez–Moosa; no new counterexample is claimed.

`evidence/pr1152/PR_BODY.md:5`:

> The essential existence theorem is prior work of Jason Bell, Stéphane Launois, Omar León Sánchez and Rahim Moosa, [Poisson algebras via model theory and differential-algebraic geometry](https://doi.org/10.4171/JEMS/712), J. Eur. Math. Soc. 19 (2017), 2019–2049. Their Theorem 4.1 supplies a differential domain R of Krull dimension n=d-1. Its Manin-kernel foundations are imported rather than independently reproved. No new counterexample or novelty is claimed.

### PR #1153: partial_or_unsolved

Problem 30002950; pinned head `a64946ead38e407195a605545877312b10d56914`.

Multiple-distinct-interior-slope single-orbit assertion explicitly remains unresolved.

`evidence/pr1153/PR_BODY.md:9`:

> The full single J-orbit assertion when there are multiple distinct interior slopes remains unresolved. Hull and colength do not determine the full invariant function. Sampled J-profiles and finite controls are not a universal orbit proof. The full conjecture is neither proved nor disproved, and no novelty is claimed.

### PR #1154: partial_or_unsolved

Problem 30001551 / OWR-4425-006; pinned head `a53633e4f49626b7e38140857b6bd9ef4c32fd2d`.

Finite searches and erasing-witness reductions do not settle the exact target.

`evidence/pr1154/PR_BODY.md:15`:

> Both bounded searches were reconstructed independently with exact arithmetic and every signature bit compared: 157,800 equations / 216 binary morphisms / 5 signatures / 10 triples, and 28,216 equations / 2,744 binary morphisms / 15 signatures / 455 triples. No triple passes on either finite pool. This does not rule out longer or nonbinary witnesses at the searched equation lengths, longer equations, or systems whose common nonperiodic solutions are all nonerasing. It does not exclude erasing common nonperiodic solutions. The exact target remains unresolved by this work.

### PR #1155: explicit_full_solution_claim

Problem 30000214; pinned head `7bc343bc88e5211e06841e375e97015fa8e5d155`.

An explicit negative answer to the unqualified homology-sphere-cover assertion is claimed. Characteristic-zero counterexamples suffice for this claimed negative answer.

`evidence/pr1155/PR_BODY.md:3`:

> The complete authored proof constructs a finite two-dimensional simplicial complex K that is doubly Cohen–Macaulay over Q, and hence over every characteristic-zero field, but contains no two-dimensional homology-sphere subcomplex over any field. Homology sphere includes all face-link conditions. Thus Nevo's homology-sphere-cover question has a negative answer before its overlap and reordering requirements arise.

`evidence/pr1155/PR_BODY.md:1–5`:

> ## Accepted negative solution to the unqualified assertion
> 
> The complete authored proof constructs a finite two-dimensional simplicial complex K that is doubly Cohen–Macaulay over Q, and hence over every characteristic-zero field, but contains no two-dimensional homology-sphere subcomplex over any field. Homology sphere includes all face-link conditions. Thus Nevo's homology-sphere-cover question has a negative answer before its overlap and reordering requirements arise.
> 
> The coefficient distinction is essential: the building is over F_11, while Cohen–Macaulayness is proved over Q/characteristic zero. No counterexample for every individually prescribed positive characteristic is claimed. No subdivision, immersion, minimal-cycle substitute or global-homology-only sphere is used.

Scope note: Generic no-novelty/priority certification disclaimer does not negate the explicit full target-result claim; this gate performs no priority audit.

### PR #1156: partial_or_unsolved

Problem 30003650; pinned head `57c07523247d0de1a2fbb76f3243d0369caff682`.

Equality of maxima does not determine the second maximum-gap question in the combined target.

`evidence/pr1156/PR_BODY.md:5`:

> The combined two-question target is ACCEPT_AS_PARTIAL. Its maximum-gap question g_n=max(cp^+(A)-cp(A)) remains undetermined in general. The result does not supply explicit ordinary maxima p_n in every order, and does not assert equality of the two ranks for every individual matrix. No novelty is claimed.

### PR #1157: partial_or_unsolved

Problem 102 / GREEN-012; pinned head `b063643e3453220a5babe49aec47c2e872fed0c7`.

The high-density theorem and bounded-order cases leave the unrestricted target unresolved.

`evidence/pr1157/PR_BODY.md:5`:

> The stronger exact claim is F(r) <= 5 on the stated domain r = (1-alpha)/alpha <= 1 and 0 < alpha < 1. The decimal threshold near 0.86946194679 is explanatory only. Subgroup-coset and complement-coset cases, quotient/product closure, and the exact finite result through group order 16 are also accepted. All 398,350 subsets across 25 abelian group types were independently checked with no violation. That bounded-order result does not establish the unrestricted target.

### PR #1158: partial_or_unsolved

Problem 30000879 / OWR-1738-004; pinned head `4de62d288bd90452c5ee8ab4766a085e22b34af3`.

Splitting and dimension inequalities leave the exact conjecture unresolved in 2 <= r < n.

`evidence/pr1158/PR_BODY.md:14`:

> The original [Aljadeff problem source](https://ems.press/content/serial-article-files/46141), printed p. 3171, reports r = n as affirmative. Its unnamed proof was not audited. After that credited prior status and the elementary boundary, the outstanding range remains 2 ≤ r < n. Automatic splitting does not establish the required dimension equality, the sharpness examples do not compute their twisted global dimensions, and no general witness in the jump case is produced. The exact conjecture remains unresolved by this work.

### PR #1159: partial_or_unsolved

Problem 1903 / EP51; pinned head `7b491ed13d8bc91ce499db7630c95a1dcb268aa0`.

Least-preimage divergence explicitly remains unresolved.

`evidence/pr1159/PR_BODY.md:11`:

> Repeated transport supplies no uniform control of usable primes as the seed changes and does not prove divergence of reciprocal increments. The exact least-preimage divergence question remains unresolved by this work. “Accepted” means the independent internal AI audit's stated partial scope. These AI-assisted documents are unrefereed; no external human peer review, journal acceptance, formal proof-assistant certification, or fresh worldwide open-status determination is claimed.

### PR #1160: partial_or_unsolved

Problem 1900013; pinned head `6124be0d9baffbfb83d80d7273a2389146b3cf1d`.

The arithmetic reduction leaves the full geometric classification unresolved.

`evidence/pr1160/PR_BODY.md:11`:

> The finite conductor quotient is a structural reduction, not a supplied turnkey algorithm for general class-group and fundamental-unit computations. The full geometric classification of face data and decorated torus decompositions remains unresolved by this work. The conclusions are confined to the historical complete eight-sail model; no blanket assertion about the generalized models in the later survey is made. No novelty, priority, or exhaustive current-literature-status claim is made.

### PR #1161: partial_or_unsolved

Problem 11000008 / AMR-109-0008; pinned head `4a410fc1cb58b6df8e87fcde033a3d5eb4b8bcc9`.

The genus-two list is not an upper classification and the full genus >=2 spectrum remains unresolved.

`evidence/pr1161/PR_BODY.md:5`:

> In genus two, finitely generated witnesses realize 0, 1, 2, and continuum many relative ends. The two-ended and continuum-ended witnesses have generating sets of at most ten and eight elements. The separate genus-zero and genus-one spectra are {0} and {0,continuum}. The genus-two list is not an upper classification. The full spectrum for every g >= 2, including the other high-dimensional cases, remains unresolved by this work. No novelty or global-openness claim is made.

### PR #1162: partial_or_unsolved

Problem 1889 / EP25; pinned head `df23bb3357786a85c8e59e54b4ad8d7e8ccf22b3`.

The finite affine-pattern theorem does not resolve the unrestricted singleton problem.

`evidence/pr1162/PR_BODY.md:11`:

> “Accepted” means the independent internal AI audit's stated partial scope. These AI-assisted authored documents are unrefereed. No external human peer review, journal acceptance, formal proof-assistant certification, novelty, or fresh worldwide open-status determination is claimed. The unrestricted singleton EP25 problem remains unresolved by this work.

### PR #1163: partial_or_unsolved

Problem 1910 / EP68; pinned head `536afbfe54c8a558d4ced34f74eefb18eca3dbb9`.

Reduced-denominator growth does not decide the series irrationality target.

`evidence/pr1163/PR_BODY.md:13`:

> The result proves neither rationality nor irrationality of S. It establishes no pointwise growth for every N, threshold claim at c = 1/3, density exactly 1/2, density one, optimality, or exclusion of a helpful sparse subsequence. The original irrationality target remains unresolved by this work; novelty and current exhaustive worldwide status are not certified.

### PR #1164: partial_or_unsolved

Problem 1954 / EP143; pinned head `6ca4d4bc9ce9e2a36a420aa673734d4e30a9ba59`.

The credited harmonic corollary does not supply weighted convergence or solve the two-part problem.

`evidence/pr1164/PR_BODY.md:7`:

> The weighted-convergence question, sum_{x in A} 1/(x log x) < infinity, is not supplied or attempted. The summation-by-parts boundary is preserved. The full two-part problem is not classified as solved. No novelty, new harmonic theorem, stronger universal counting-density or Behrend-rate estimate, or current worldwide openness claim is made.

### PR #1165: partial_or_unsolved

Problem 20000970; pinned head `884189521d2f6765a8233deef53c988fa5cd1705`.

The general efficient-sampling target remains unresolved; arbitrary cores have exponential fallback.

`evidence/pr1165/PR_BODY.md:35`:

> remains unresolved by this work. Arbitrary large residual cores have an

`evidence/pr1165/PR_BODY.md:34–38`:

> The unrestricted [AIM sampling question, Problem 5](https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf)
> remains unresolved by this work. Arbitrary large residual cores have an
> exponential fallback. No general polynomial-time exact sampler, FPAUS,
> rapid-mixing bound, impossibility theorem, novelty, or exhaustive current
> literature status is claimed.

### PR #1166: partial_or_unsolved

Problem 1988 / EP-197; pinned head `e24c651839759de8c6544edd081b136892d436cb`.

The bounded-deficit obstruction and dense construction do not decide the full two-set target.

`evidence/pr1166/PR_BODY.md:5`:

> For each prescribed nondecreasing unbounded f:N->N, an adaptation of Geneson's construction yields one 3-permutable set with upper natural density at least 2/3 and infinitely many full intervals with positive deficits at most f of their starts. Those deficits still diverge. The proof also gives translation equivalence of the zero-based and positive-integer two-set existence questions. Neither an admissible complement nor a theorem ruling out all two-colorings is supplied. The full two-set target remains unresolved by this work; no novelty, priority or exhaustive worldwide-status claim is made.

### PR #1167: partial_or_unsolved

Problem 2000004 / AMR-019-0004; pinned head `f91ebbdad3ec84fda41c8d3398609f41927117f0`.

The credited two-component CN result does not solve the original connected-domain boundary-only formulation.

`evidence/pr1167/PR_BODY.md:13`:

> No unqualified solution to Ball's connected-domain, boundary-only formulation, no everywhere-injective homeomorphism-class result, and no novelty are claimed. Remark 3.1 does not supply the missing connector estimates or preserve boundary-only constraints by itself. The bounded correction search on 10 October 2026 found no repair; it was not exhaustive. No author was contacted.

### PR #1168: partial_or_unsolved

Problem 20000973; pinned head `bce229ff4e150f5f99b4c854ce2eef0df650cf73`.

The credited prior minimum-equivariance criterion is scoped; stronger original naturality is not established and no full original-problem solution is claimed.

`evidence/pr1168/PR_BODY.md:13`:

> The precise scope is the minimum automorphism-equivariance requirement in

`evidence/pr1168/PR_BODY.md:3–21`:

> The anonymous, unrefereed [manuscript, version 0.2.0-candidate](https://raw.githubusercontent.com/ipitchford/symmetry-respecting-tree-torsors/main/PAPER.md),
> *An exact criterion for symmetry-respecting critical-group torsors*, passes the
> independent AI-assisted proof audit. Its exact full-Aut(G)-compatible critical-group
> torsor criterion, cohomology-class and actual-action-map counts, effective finite
> evaluation, simple generalized-theta classification and simple cactus construction
> are accepted. The complete substantive authored proof audit, source-hypothesis
> audit and all scope clarifications are retained. No mathematical correction is
> required. Acceptance credits an existing manuscript; no new discovery or
> historical-priority claim is made.
> 
> The precise scope is the minimum automorphism-equivariance requirement in
> [Problem 8 of the 2013 AIM workshop list, physical PDF page 4](https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf).
> Stronger unspecified naturality, a uniquely preferred general action, additional
> graph-map or minor consistency and an efficient algorithm remain unestablished.
> Isomorphism-compatible selection follows after an action is chosen on each
> admissible representative; that selection is not thereby unique. Mere finite
> decidability already followed from enumerating bijections. The family theorems
> retain their simple-graph hypotheses and the general criterion retains the actual
> induced Jacobian action and all subgroup marks simultaneously.

`gate_reviews/upper/pr1168/ACCEPTANCE.json:4–10`:

>   "decision": "ACCEPTED-PRIOR-MINIMUM-EQUIVARIANCE",
>   "scope": "The exact prior manuscript criterion for a full-Aut(G)-compatible critical-group torsor, its cohomology and action counts, and stated simple generalized-theta/cactus theorems.",
>   "mathematical_corrections": [],
>   "stronger_unspecified_naturality_established": false,
>   "efficient_algorithm_established": false,
>   "historical_priority_established": false,
>   "new_discovery_claimed": false,

`gate_reviews/upper/pr1168/README.md:13–21`:

> This is the minimum full-Aut(G)-equivariance interpretation of [Problem 8 in the
> 2013 AIM workshop list, physical PDF page 4](https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf).
> The source leaves stronger meanings of “natural” unspecified. The result does
> not establish a uniquely preferred general action, compatibility with
> unspecified graph maps or minor operations, an efficient algorithm, or
> historical priority. Isomorphism-compatible selection is possible after
> choosing an action on each admissible isomorphism-class representative; those
> choices are not thereby unique. Finite decidability alone was already
> immediate by enumerating bijections.

Scope note: Minimum-equivariance interpretation has a complete credited prior criterion, while stronger unspecified original naturality is unestablished. Classified scoped/partial for the original target; either interpretation excludes a new full original-solution claim.

### PR #1169: explicitly_prior_full_resolution

Problem 2066 / EP-348; pinned head `55ea68bb05104433655f6438da5ebe71f0be5936`.

The complete deletion-threshold classification is expressly a credited prior Geneson result.

`evidence/pr1169/PR_BODY.md:28`:

> This is an AI-assisted, unrefereed audit of an existing arXiv preprint, not a new

`evidence/pr1169/PR_BODY.md:3–9`:

> Theorem 1 of Jesse Geneson, *Deletion thresholds and exponential examples for
> complete sequences*, [arXiv:2609.25107v1](https://arxiv.org/abs/2609.25107v1),
> is accepted within the exact original eventual-completeness and indexed-occurrence
> deletion conventions. For every pair of integers 0 <= m < n, a nondecreasing
> integer sequence complete after every m-occurrence deletion and incomplete after
> every n-occurrence deletion exists exactly when m <= 1. Each deletion can have
> its own eventual threshold. No mathematical correction was required.

### PR #1170: explicitly_prior_full_resolution

Problem 2009 / EP252; pinned head `fe3bfa1919c963671f4b342adf5085a85449dc7f`.

The full irrationality argument is attributed to prior author Tokengrinder; the formal reproducibility hold does not create a new-solution claim.

`evidence/pr1170/PR_BODY.md:5`:

> k >= 0. Credit remains with the prior author. The complete seven-step

`evidence/pr1170/PR_BODY.md:3–9`:

> This AI-assisted authored audit finds no mathematical gap in the prior
> Tokengrinder argument for irrationality of sum sigma_k(n)/n! for every integer
> k >= 0. Credit remains with the prior author. The complete seven-step
> reconstruction is retained without mathematical changes: exact factorial-tail
> integrality, the scaled Stirling remainder, progression means including k = 1,
> a fixed coprime finite-difference grid, squared CRT moduli, the isolated-shift
> contradiction, and the separate positive-tail proof for k = 0.

### PR #1171: partial_or_unsolved

Problem 2041 / EP312; pinned head `b825709b43bdbf06c6981326426240eb6bc730ed`.

The universal arbitrary-multiset exponential theorem and logarithmic-mass assertion remain unresolved.

`evidence/pr1171/PR_BODY.md:29`:

> assertion remain unresolved by this work. No novelty, optimal constant,

`evidence/pr1171/PR_BODY.md:28–30`:

> The universal arbitrary-multiset exponential theorem and logarithmic-mass
> assertion remain unresolved by this work. No novelty, optimal constant,
> external referee approval, or exhaustive literature coverage is claimed.

### PR #1172: partial_or_unsolved

Problem 2020 / EP-269; pinned head `d62713eed9b25837a4790be6fb59485a3a26770b`.

The phase asymptotic and polynomial obstruction do not prove irrationality; arbitrary integer carries remain unresolved.

`evidence/pr1172/PR_BODY.md:7`:

> No fixed finite family of real polynomial corrections can give a little-o leading-scale remainder, even with arbitrary indexwise choice. Fixed-period quasipolynomials are excluded in particular. For {2,3,5}, the progression oscillation constant is certified strictly between 0.0127214469683 and 0.0127214469684, and the limsup/liminf ratio is at least 5/3. Singleton supports are excluded: their normalized tails are constant. Arbitrary nonpolynomial integer carries remain the unresolved arithmetic obstruction; no irrationality proof, counterexample, or cofinal residue-escape theorem is claimed.

### PR #1173: partial_or_unsolved

Problem 2033 / EP291; pinned head `ffe001232d56438d04996aa875171fc83cb4c9c7`.

Fixed-prime control leaves growing-prime control and full coprimality infinitude unresolved.

`evidence/pr1173/PR_BODY.md:24`:

> Neither fixed-set density nor pairwise independence settles full infinitude.

`evidence/pr1173/PR_BODY.md:19–24`:

> The local criterion requires p <= n and exponent at least one; its modular
> calculation retains the invertible multiplier L_n/p^e, and q_n is always odd.
> The distinction n=33 is essential: 33 survives universal-digit deletion,
> but q_33=11 because its leading base-11 digit is 3 and H_3=11/6. The other
> harmonic zero digits across a growing prime family remain uncontrolled.
> Neither fixed-set density nor pairwise independence settles full infinitude.

### PR #1174: partial_or_unsolved

Problem 2071 / EP-357; pinned head `8b2970df8a3464580c45ca3cc397d0e2b5edb590`.

Credited partial bounds do not establish residual sublinearity.

`evidence/pr1174/PR_BODY.md:9`:

> Here f(n) is the largest length of a strictly increasing sequence of positive integers at most n whose nonempty indexed consecutive block sums are all different. Singleton blocks, overlapping blocks and collisions across lengths are included. The residual f(n)=o(n) question is not established. Neither the order of growth of f nor f(n)~n/2 is claimed.

### PR #1175: partial_or_unsolved

Problem 2037 / EP302; pinned head `832f02f35398f0a61b24942c6cd2906a5fe40938`.

Full resolution is expressly disclaimed; the lower improvement additionally has a verification hold.

`evidence/pr1175/PR_BODY.md:30`:

> No full resolution, convergence theorem, exact limiting density, novelty,

`evidence/pr1175/PR_BODY.md:30–32`:

> No full resolution, convergence theorem, exact limiting density, novelty,
> priority, external human peer review, journal acceptance, or new explicit
> numerical lower improvement above 5/8 is claimed.

### PR #1176: partial_or_unsolved

Problem 2070 / EP354; pinned head `66dd0fca2e557a15ae632b8c21eee81814050949`.

The variable-base counterexample leaves the original fixed-base-two question unresolved.

`evidence/pr1176/PR_BODY.md:24`:

> it does not resolve the original fixed-base-2 question or classify all bases.

`evidence/pr1176/PR_BODY.md:21–24`:

> The original hypotheses permit beta=gamma alpha for irrational gamma.
> At gamma=2 the corresponding ratio is rational and inadmissible. Therefore
> this counterexample addresses the universal extension to 1<gamma<2;
> it does not resolve the original fixed-base-2 question or classify all bases.

### PR #1177: partial_or_unsolved

Problem 2083 / EP377; pinned head `92b21cf7edce96b464560abf4d0ad9946a76278e`.

The absolute bound is explicitly neither proved nor refuted.

`evidence/pr1177/PR_BODY.md:24`:

> reciprocal mass remains uncontrolled: sup_n f(n)<infinity is neither proved

`evidence/pr1177/PR_BODY.md:23–26`:

> construction does not produce actual simultaneous nondivisibility. Deep-shell
> reciprocal mass remains uncontrolled: sup_n f(n)<infinity is neither proved
> nor refuted. The empty prime set in the sublogarithmic theorem is explicitly
> clarified as vacuous; this is an editorial clarification, not a theorem change.

### PR #1178: partial_or_unsolved

Problem 2087 / EP385; pinned head `15abff8335f629acbd60643c10b7e9640b1104e6`.

Natural-density divergence does not establish eventual positivity or pointwise divergence.

`evidence/pr1178/PR_BODY.md:7`:

> natural density. Neither eventual positivity for all sufficiently large n

`evidence/pr1178/PR_BODY.md:4–9`:

> mathematical audit. For n>=5, let F(n) be the maximum of m+p(m) over composites
> 4<=m<n, with p(m) the least prime divisor. For every fixed real K, the integers
> with F(n)-n<=K have natural density zero. Thus F(n)-n tends to infinity in
> natural density. Neither eventual positivity for all sufficiently large n
> nor pointwise divergence is established. A density-zero set is not proved
> finite, and no global last exception is claimed.

### PR #1179: partial_or_unsolved

Problem 2112 / EP423; pinned head `f7cc04cc66206ad5092c7609824c44f886af7706`.

The plateau lower bound leaves the original exact asymptotic and upper estimates untouched.

`evidence/pr1179/PR_BODY.md:32`:

> The exact asymptotic, b_n=o(n), and even an O(n) upper bound for a_n remain

`evidence/pr1179/PR_BODY.md:32–35`:

> The exact asymptotic, b_n=o(n), and even an O(n) upper bound for a_n remain
> untouched. A plateau-length upper bound supplies no upper control on the
> frequency of omissions. Synthetic crossing obstructions are not established
> actual greedy prefixes. No global novelty, priority or optimality is claimed.

### PR #1180: partial_or_unsolved

Problem 2104 / EP413; pinned head `08df895fa0e2c4273e2e67087dc72e36d98aac4d`.

The corrected credited logarithmic barrier does not resolve the original coefficient-one question.

`evidence/pr1180/PR_BODY.md:22`:

> Coefficient one remains unresolved. The logarithmic result controls it only

### PR #1181: partial_or_unsolved

Problem 2129 / EP-461; pinned head `3bc95aa5364f8b17b91423d5603606aae1a420ac`.

The finite obstruction caps a possible coefficient but does not establish a positive uniform lower coefficient.

`evidence/pr1181/PR_BODY.md:13`:

> claim follows. A positive uniform lower coefficient remains unresolved.

`evidence/pr1181/PR_BODY.md:7–13`:

> The independent internal audit accepts f(N,500)=208 for a positive 424-digit
> integer N. Hence any universal coefficient in f(n,t)>=ct satisfies
> c<=52/125=0.416. This improves the specific 218/500 example in
> [Patrick White + Claude, wave 5w, 26 July 2026](https://www.erdosproblemaday.com/report/461)
> by exactly 1/50. The source is an AI-disclosed working report. The earlier
> example was independently reproduced; no minimum at t=500 or best-in-literature
> claim follows. A positive uniform lower coefficient remains unresolved.

### PR #1182: explicitly_prior_full_resolution

Problem 2141 / EP486; pinned head `d2dc8ab5de3bd62d5e1b4831dedd6efd3b2a39bf`.

The arbitrary-residue counterexample expressly accepts the prior Wang theorem.

`evidence/pr1182/PR_BODY.md:13`:

> This is acceptance of an identified prior theorem, with no novelty claim.

`evidence/pr1182/PR_BODY.md:3–14`:

> The complete prose proof of Shouqiao Wang, *A Proposed Solution to Erdős
> Problem 486*, is accepted after mathematical audit. One fixed infinite set
> of positive moduli, with fixed arbitrary residue sets, has survivors B with
> 
>     liminf L_B(x) <= 177/200 < 49/50 <= limsup L_B(x),
>     L_B(x) = (1/log x) sum_{1<=m<x, m in B} 1/m.
> 
> Source: [ten-page Wang manuscript](https://multiscalar.ai/results/erdos-486/paper.pdf),
> 350612 bytes, SHA-256
> `01ce6f1d22b0c9208cc45ecaa15039f0ee13ea75c334908ca65f371c365b9048`.
> This is acceptance of an identified prior theorem, with no novelty claim.
> The arbitrary-residue result does not settle singleton-residue EP25.

### PR #1183: explicitly_prior_full_resolution

Problem 2142 / EP488; pinned head `9ee887e69bb3476634a5765c425e7b49787124b4`.

The original multiples inequality is refuted by an expressly credited prior complete proof of Declan Gessel.

`evidence/pr1183/PR_BODY.md:1`:

> ## Accepted prior full finite refutation

`evidence/pr1183/PR_BODY.md:3–18`:

> The complete elementary proof of Declan Gessel, with disclosed GPT-6 Astra
> assistance in Codex, September 2026, is accepted after mathematical audit.
> There is a nonempty finite set A of integers greater than 1 and positive
> integer endpoints m>n>=max(A) for which
> 
>     2 m M_A(n) < n M_A(m),
> 
> where M_A(x) counts positive integers at most x divisible by at least one
> member of A. This is a strict reverse of the proposed multiples-density
> inequality. The proof yields a finite existential integer 0<=k<4096;
> neither k nor its generator set and endpoints have been enumerated.
> No new discovery or priority claim is made.
> 
> Prior proof: [pinned complete prose note](https://gist.github.com/declangessel/d8e15e5ff1b6c7e99e3d86d7c66f1d08/raw/9bbb516e782229c8ee2fe08dfe3bd53acac8b258/proof-note.md),
> 9365 bytes, SHA-256
> `a279254e71d06e8b5c9809f466f47fd675820a38acd0caa9e04345ac867ee8df`.

### PR #1184: explicitly_prior_full_resolution

Problem 2166 / EP538; pinned head `8a9d3fac6f38bc2343905197761667502c883da0`.

The full fixed-r matching-order result expressly credits the prior STARFLEET Math claim.

`evidence/pr1184/PR_BODY.md:12`:

> This is an audit of a prior public claim, credited to STARFLEET Math, with

`evidence/pr1184/PR_BODY.md:3–13`:

> The prior STARFLEET Math result for Erdős Problem 538 is accepted as a
> conventional mathematical proof. For every fixed integer r>=2,
> 
>     E_r(N)=Theta_r(log N/log log N).
> 
> E_r(N) maximizes S(A)=sum_{a in A}1/a over positive a<=N, with at most r
> ordered pairs (p,a), p prime, a in A, m=pa, for every integer m.
> The cap includes products above N. Arbitrary admissible sets need not be
> squarefree; squarefreeness is used only in the constructed lower witnesses.
> This is an audit of a prior public claim, credited to STARFLEET Math, with
> no novelty claim.

### PR #1185: partial_or_unsolved

Problem 2273 / EP710; pinned head `0c6610ab4be72629c2dc4b7c39d29e52c6aa50f1`.

The finite route obstruction does not resolve the fixed-start asymptotic target.

`evidence/pr1185/PR_BODY.md:23`:

> The fixed-start asymptotic question remains unresolved by this work.

`evidence/pr1185/PR_BODY.md:21–23`:

> No asymptotic equivalent, improved bound, eventual obstruction, asymptotic
> failure of a tail method, novelty, priority or full resolution is claimed.
> The fixed-start asymptotic question remains unresolved by this work.

### PR #1186: partial_or_unsolved

Problem 2274 / EP-711; pinned head `e02f8815db7a8b53c01023d4e2da8706860ebb51`.

Credited interval-matching bounds leave the uniform exponent-one upper question unresolved.

`evidence/pr1186/PR_BODY.md:9`:

> The last lower bound and the known diagonal upper estimate imply [F(n)-f(n,n)]/(n log n)->infinity. This is a consequence of the credited prior results, not a new theorem. The uniform upper question F(n)<=n^(1+o(1)) remains unresolved by these results. The fixed-start asymptotic in Erdos Problem 710 is separate and is not settled here. A 4/3 upper exponent does not approach 1.

### PR #1187: partial_or_unsolved

Problem 2150 / EP509; alias 2304007 / AMR-022-4007; pinned head `345a5aa2fb5b1beaf169d880bc34745d2213a198`.

Binomial-family exact covers do not solve the unrestricted disk-cover problem.

`evidence/pr1187/PR_BODY.md:3`:

> The full EP-509 question remains unresolved. This edition preserves the complete

### PR #1188: partial_or_unsolved

Problem 2249 / EP677; pinned head `a07dfa203ea3c664ac026178adbd81e8eaa9a744`.

Finite lengths/gaps and reductions leave the arbitrary-length arbitrary-gap target unresolved.

`evidence/pr1188/PR_BODY.md:20`:

> The arbitrary-length, arbitrary-gap problem remains unresolved by this work.

### PR #1189: partial_or_unsolved

Problem 2334 / EP839; pinned head `86c69038c87d2ac9066f1e73d4aa47a574d5544f`.

Separated-block estimates and a source repair leave both universal original questions unresolved.

`evidence/pr1189/PR_BODY.md:3`:

> Both original EP-839 questions remain unresolved for arbitrary admissible

`evidence/pr1189/PR_BODY.md:3–5`:

> Both original EP-839 questions remain unresolved for arbitrary admissible
> sequences: lower natural density zero, and H_A(x)/log x tending to zero.
> No novelty or priority is asserted.

### PR #1190: explicitly_prior_full_resolution

Problem 2283 / EP730; pinned head `78f50353df043afb8763bfee3746a6090a75b3bb`.

The full binomial-prime-support result is expressly prior work with named attribution, not a new-solution claim.

`evidence/pr1190/PR_BODY.md:6`:

> This is an audit of prior work, with no new-solution or novelty claim.

`evidence/pr1190/PR_BODY.md:3–12`:

> The prior EP730 proof is accepted as a conventional mathematical solution:
> infinitely many distinct positive n<m have equal prime supports of
> binomial(2n,n) and binomial(2m,m). Infinitely many consecutive pairs occur.
> This is an audit of prior work, with no new-solution or novelty claim.
> 
> As credited by the author's public formalization manifest, Liam Price
> provided the informal idea, Tomodovodoo an algebraic follow-up, and Will Blair
> the analytic reconstruction/formalization. The author describes review as
> self-assessed and the earlier informal argument as unadjudicated. Priority
> and unavailable antecedent material were not independently authenticated.

### PR #1191: partial_or_unsolved

Problem 2291 / EP757; pinned head `f6bdd27605a82a5a24ae22b733b68d510b83506a`.

The all-real obstruction concerns extensions of one exact seed; the universal target remains unresolved.

`evidence/pr1191/PR_BODY.md:66`:

> The original universal problem remains unresolved by this work. No global

### PR #1192: partial_or_unsolved

Problem 2364 / EP885; pinned head `07122aab017254f3d52bae6f78ee9887bfac5e2f`.

Fixed-seed saturation/support statements do not resolve unrestricted k=5 or arbitrary k.

`evidence/pr1192/PR_BODY.md:64`:

> Unrestricted k=5 and the universal arbitrary-k target remain unresolved by

### PR #1193: partial_or_unsolved

Problem 2503 / EP1122; pinned head `20dd56f3fe11a27f679d4f2aa3025ee157f3abc4`.

The periodic-residual premise is not derived from the original density-zero hypothesis.

`evidence/pr1193/PR_BODY.md:19`:

> The unrestricted EP 1122 / 2503 problem remains unresolved by this work.

### PR #1194: explicitly_prior_full_resolution

Problem 3100034; pinned head `7fa783b69fb45039ddf9d9b5c621b8a6a1d091af`.

The complete balanced-permutation classification expressly credits the published Combinatorica resolution.

`evidence/pr1194/PR_BODY.md:13`:

> This is an audit of a prior published resolution, with no novelty claim.

`evidence/pr1194/PR_BODY.md:3–15`:

> This authored exposition records the exact finite balanced-subsequence-pattern
> classification proved by Gal Beniamini, Nir Lavee and Nati Linial in
> [*How Balanced Can Permutations Be?*](https://doi.org/10.1007/s00493-024-00127-x),
> Combinatorica 45, article 9 (2025). For integers n>=k>=1:
> 
> - k=1: every n>=1.
> - k=2: n>=2 and n=0 or 1 modulo 4.
> - k=3: n>=3 and n=0,1,9,20,28,29 modulo 36.
> - k>=4: no n>=k.
> 
> This is an audit of a prior published resolution, with no novelty claim.
> The pattern definition uses arbitrary increasing index sets. Endpoints,
> infinitude for each k<=3, and nonexistence for each k>=4 are included.

### PR #1195: partial_or_unsolved

Problem 2440 / EP1016; pinned head `d60ac3486306d80bb70b1f12a6be2e8098858a51`.

Outerplanar and star-weak-dual results leave the unrestricted crossing-chord problem unresolved.

`evidence/pr1195/PR_BODY.md:68`:

> log-star lower bound remain unresolved by this work. No novelty, priority,

`evidence/pr1195/PR_BODY.md:67–72`:

> The unrestricted crossing-chord divergence question and coefficient-one
> log-star lower bound remain unresolved by this work. No novelty, priority,
> or exhaustive literature-status claim is made. This AI-assisted work is
> unrefereed. Acceptance means an independent internal AI audit. No external
> human peer review, journal acceptance, or formal proof-assistant
> certification is claimed.

### PR #1196: partial_or_unsolved

Problem 3000017; pinned head `5b737a886c7cd10f3f15ebbadd5128a18c16ae8d`.

The certifying algorithm covers weighted cacti, while arbitrary Eulerian multigraph halting remains unresolved.

`evidence/pr1196/PR_BODY.md:8`:

> the exact block definition; arbitrary Eulerian multigraph halting remains

`evidence/pr1196/PR_BODY.md:3–9`:

> This authored edition proves a certifying halting algorithm for connected,
> loopless directed-cycle block cacti with independent positive binary-encoded
> weights on their cycle blocks. It uses O(n²) exact integer arithmetic
> operations and polynomial intermediate bit length. Every independently
> weighted bidirected tree is included. A bidirected triangle is excluded by
> the exact block definition; arbitrary Eulerian multigraph halting remains
> unresolved by this work.

### PR #1197: partial_or_unsolved

Problem 3000008; pinned head `8fc2d63f2a3b51aefe66ec094cc2fbb04571d2b5`.

The fixed-rank sufficient criterion does not settle the unrestricted two-sided matroid target.

`evidence/pr1197/PR_BODY.md:78`:

> The unrestricted simultaneous additive Δ−1 guarantee remains unresolved

### PR #1198: partial_or_unsolved

Problem 2678 / K3 Problem 1.19; pinned head `3586a64988bc5aba234c8cb27b44fa14505e6d2c`.

The credited closed-oriented smooth 3-manifold result does not certify the broader literal K3 target; a full broader resolution is expressly disclaimed.

`evidence/pr1198/PR_BODY.md:44`:

> The conclusion is a scoped prior-result audit. No novelty, priority,

`evidence/pr1198/PR_BODY.md:10–14`:

> The preliminary K3 Problem 1.19 formulation does not explicitly state
> closedness or orientability. Boundary, noncompact, nonorientable, and
> other broader literal variants are not certified. The optional claim
> about every hyperbolic knot, its finite-order extension route, and a
> classification of sphere twists are not included or accepted here.

`evidence/pr1198/PR_BODY.md:34–48`:

> Alper Ferudun's [version 1.1](https://doi.org/10.5281/zenodo.23165876),
> dated 5 October 2026, is an unrefereed public prior treatment.
> Aceto–Bregman–Davis–Park–Ray,
> [*Isotopy and equivalence of knots in 3-manifolds*](https://arxiv.org/abs/2007.05796v3),
> May 2026, p. 6, records an Etnyre–Margalit announced prior proof extending
> to the non-prime case. That announcement was inspected; the announced
> proof itself was not. Ferudun's report that their paper is forthcoming
> is attributed public manuscript status, not private author confirmation.
> No author was contacted.
> 
> The conclusion is a scoped prior-result audit. No novelty, priority,
> new-solution, or full broader K3-resolution claim is made. This AI-assisted
> work is unrefereed. Acceptance means an independent internal AI audit,
> not external human peer review, journal acceptance, or formal
> proof-assistant certification.

`gate_reviews/upper/pr1198/ACCEPTANCE.json:4–19`:

>   "status": "ACCEPT_SCOPED_PRIOR_RESULT_CORE",
>   "required_correction": null,
>   "edition_scope": {
>     "closed_connected_oriented_smooth_3_manifolds": true,
>     "one_asymmetric_hyperbolic_knot_detects_every_nonidentity_orientation_preserving_mapping_class": true,
>     "ambient_isotopy_of_unoriented_embedded_circles": true,
>     "complete_core_proof_and_exact_dependencies_retained": true,
>     "point_push_and_boundary_unrestricted_isotopy_retained": true,
>     "continuous_collar_gluing_and_inverse_retained": true,
>     "solid_torus_relative_kernel_and_TOP_smooth_comparison_retained": true,
>     "classical_theorem_statements_and_applicability_audited": true,
>     "historical_classical_proofs_independently_reproved": false,
>     "every_hyperbolic_knot_claim_certified": false,
>     "finite_order_extension_certified": false,
>     "broader_literal_K3_scope_certified": false,
>     "novelty_or_priority_claimed": false,

Scope note: The exact accepted closed-oriented category has a prior treatment. Broader literal K3 variants are uncertified; this is scoped/partial rather than a full original-resolution claim.

### PR #1199: partial_or_unsolved

Problem 2366 / EP887; pinned head `eb7d097e149eb7e28341c45cf1e5e3e74438a422`.

The credited five-divisor construction gives K>=5 but leaves the general uniform-bound problem unresolved.

`evidence/pr1199/PR_BODY.md:9`:

> formulation therefore satisfies K≥5. The general EP887 question remains

`evidence/pr1199/PR_BODY.md:3–12`:

> This authored edition independently reconstructs the core of Theorem 1 in
> M. Czech's pinned July 2026 manuscript. Every positive integral solution of
> z²−56x²=65 with x≥37 gives five explicit distinct divisors of
> n=(x²−1)(x²−4)(x²−16)(x²−49) in the strictly open right interval
> (√n,√n+31 n^(1/4)). A positive Pell recurrence from (37,277) yields
> infinitely many distinct n. Any K in the original one-sided uniform-bound
> formulation therefore satisfies K≥5. The general EP887 question remains
> unresolved by this work.
> 
> This is an audit of a prior construction, not a newly claimed theorem.

### PR #1200: partial_or_unsolved

Problem 3000065; pinned head `a3309d3527ab1a45ce05d2a9c70e182b2d2536a5`.

The regular-or-empty 2-core sufficient class does not settle unrestricted bipartite proportional factors.

`evidence/pr1200/PR_BODY.md:84`:

> The unrestricted same-partition target remains unresolved by this work.

