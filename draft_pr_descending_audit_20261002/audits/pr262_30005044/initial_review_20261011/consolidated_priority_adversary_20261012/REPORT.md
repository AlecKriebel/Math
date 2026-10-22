# Consolidated independent adversarial priority review of PR262

Authored 2026-10-12 UTC by the fresh integration adversary. Problem 30005044 / OWR-9790363-003. Author attribution for the underlying research: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This report is an audit, not a paper, a publication clearance, a queue mutation, or a decision made on the parent's behalf.

## Verdict

**The exact historical existential target is category (b): an elementary consequence of older general theorems, with a necessary contact-process coupling written out in this audit.** It is not category (a) on the evidence actually inspected: ADGO's printed theorem is about weighted Galton-Watson trees, and BKV Proposition 6.2 is printed as global survival. It is not category (c): neither bridge leaves a central unsupported mathematical claim for the candidate to solve. In addition, the original authors expressly anticipated the candidate's power-law regime and BKV route in June 2024, retained in March 2026.

**GO** for the mathematical prior-result implication and for recording the existential target as already resolved by established theory. **HOLD** on promotion as a novel solution, first solution, currently open problem, or new qualitative mechanism; **HOLD** on an automatic research-paper/merge/DOI continuation justified by these priority reports alone. A truthful credited quantitative or expository note is mathematically possible, but a family reviewer's conditional note GO is not evidence that the numerical refinement is novel or significant enough to meet the project's research goal.

Recommended target disposition: a fresh evidence-bound assessment of **`already_solved`**, with the reason explicitly stated as an established-theory corollary rather than an exact old printed CP theorem. Preserve the historical submitted **`claimed_solved`** row as the eligibility fact. The explicit bound is valid mathematical content and deserves preservation/credit. It does not presently justify a newly-solved research disposition. Parent owns all queue, PR and publication decisions.

No substantive mathematical error was found in either final qualitative bridge. I independently checked the corrected BKV epsilon, including the previously omitted tail-separation condition. The strongest independently verified older-theory deduction is

    for every fixed lambda>0 and H>0, P_annealed(|X_H|=infinity)>0,

for the accepted offspring law and minimal finite-path process. A separate hereditary argument gives the accepted almost-every-tree, every-positive-rate eventual positivity. This conclusion is stronger in annealed time support than the historical existence question, but supplies no candidate numerical lower bound.

## Exact inputs and independence

The frozen corrected candidate C2 is

    W/scoped_candidate_v02/unsolved_math_prioritization/attempts/30005044

where W is `/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011`. CANDIDATE_MANIFEST.json has SHA256 `3bad9b517356b93a5339c776ebfde1825492b21c171d881f06c67946897fcea8`; the mathematical/source acceptance receipt has SHA256 `542f4233d8d696fe9804a42120b1c2e3e9cd164ed85c785d349544edd105bf13`. I rehashed both and all 33 candidate-manifest entries. None differed. Mathematical truth of the explicit candidate theorem remains a separately accepted input; this review does not pretend that rehashing proves it.

The assigned author-head identifier is `6ebe8222a1fabab97ff59885968bd8c8158d5d9f`. The preserved historical payload binding separately identifies commit `c805fbb48db939b82c59609c0b8be6cdcedd40e7` and the exact original QUEUE row `claimed_solved`, turns 1/5. Those identifiers have different recorded roles and are not equated here. No live-provider disposition or live-head recheck is claimed.

All seven required final reports were fully read: the author-version report and estimates bridge; the contact-literature report, proof implication and timing adversary; the branching report and bridge adversary. An initial combined display was truncated; I repaired it using individually bounded report/chunk displays. All 33 C2 entries and the three final family output manifests (581 author, 281 contact, 31 branching entries) were independently rehashed without mismatch. These checks establish exact evidence identity, not agreement with its interpretations.

I then independently extracted and read complete essential primary pages, and viewed regenerated full-page images: ADGO 2, 6, 7, 12; BKV 6, 17, 46–48; 2406.12689v1 15–16, v2 16; OWR PDF 42–44 / printed 618–620. `READ_SCOPE_RECEIPT.json` pins these 15 actual text/image visits. I do not claim a personal full read of the entire primary manuscripts. The two positive implications below rely on these actual primary bodies and independent derivations, rather than on a majority vote among reviewers.

The governing AGENTS.md, queue AGENTS.md, descending-program README, and relevant queue README lifecycle/assessment text were read. The program's requirement for a deep priority review does not disappear because a valid proof exists. The root's additional complete Pemantle–Stacey 2001 and JLM v2 read notes/receipt were read as attributed root evidence, not misrepresented as my own full-manuscript reading. They close the contact family's dated body-access gap in the integrated evidence, without creating an exhaustive absence certificate.

Exact input pins are in `INPUT_MANIFEST.json`; essential source pins are in `ESSENTIAL_SOURCE_MANIFEST.json`; the independently replayed manifest and rational checks are in `INDEPENDENT_REHASH_AND_ALGEBRA.json`. All authored outputs are confined to this owned folder. No individual was contacted, no outreach was prepared, and no provider/ref/PR/Zenodo/GWS/source/primary Git metadata write occurred. The separate 101-file research checkpoint is not PR disposition and is not used as a substitute for this review.

## Exact target and falsification criteria

Let xi be finite positive integer-valued with P(xi>=m)=m^(-1/4), m>=1. The physical GW tree has no leaves, is locally finite, and has infinite mean offspring. Start from the root only. Independently place rate-lambda Poisson arrows on ordered adjacent pairs and rate-one recoveries at vertices. X_t contains exactly endpoints of ordinary finite root-originating infection paths, or equivalently the increasing union of coupled finite-ball contact processes.

The candidate gives the separately accepted annealed bound

    P(|X_(1/(2lambda))|=infinity) >= (7/30) exp(-3/(2lambda)) > 0.

For almost every tree, every lambda>0 has positive dynamics probability of an infinite simultaneous configuration at some finite time. The time/probability may depend on the tree/rate. Finite fitness values at least 1 only add arrows. There is no universal infinite-mean criterion, uniform quenched deadline/probability, probability-one graphical explosion, or unique post-explosion continuation claim.

The exact OWR printed 619 wording asks whether explosion can occur after removing finite offspring mean. Printed 618 permits constant fitness 1. Thus one admissible example with infinitely many simultaneous infections at one finite time settles this existential subquestion. Adjacent mixed-moment, lower-fitness-bound, bounded-offspring and finite-graph questions remain distinct.

An adverse outcome for the older-theory implication would require a genuine gap in retention/GW regeneration, survival conditioning, strict quantiles, support at arbitrarily small times, adaptive arrow independence, simultaneous finite witnesses, or the BKV selective residual argument. Failure to locate a theorem with exactly the candidate constant is not such a gap. Conversely, identifying an old survival theorem alone is insufficient.

## Independent derivation 1: fixed-horizon thinning of ADGO

### Retained law and survival

Fix lambda>0 and H>0; set p=exp(-H). Retain a vertex when its recovery process has no mark in [0,H]. These indicators are independent Bernoulli(p), independent of offspring and arrows. Condition only on retaining the root. The retained root-connected component has the unconditioned ordinary GW law

    eta | xi ~ Binomial(xi,p).

A retained vertex's existence/retention reveals ancestors and its own retention indicator, not its own offspring or the independent retention indicators of its children. Generation-by-generation exploration therefore gives iid eta offspring. Root retention does not size-bias xi. Survival conditioning must not be carried into the descendant-regeneration argument below.

The retained tree can die: P(eta=0)>=P(xi=1)(1-p)>0. It is nevertheless supercritical, since E eta=p E xi=infinity. Choose finite K with E min(eta,K)>1. The bounded-offspring process with offspring min(eta,K) embeds in it and has positive survival probability. For completeness, its generating function g satisfies g(0)>0, g(1)=1 and g'(1)>1; hence g(s)<s just below 1 and has a fixed point below 1, so the increasing extinction-probability iteration from 0 has limit below 1. This supplies the positive survival required by ADGO's actual conditioning.

### Strict tail/quantile control

For integer m>=1 let k=ceil(2m/p). Retaining the first k physical children on {xi>=k}, independently of that event, gives

    P(eta>=m) >= k^(-1/4) P(Bin(k,p)>=m)
              >= (p/3)^(1/4) m^(-1/4) (1-exp(-m/4)).

Here kp>=2m and k<=3m/p; the standard half-mean Chernoff estimate bounds the failure by exp(-kp/8)<=exp(-m/4). For example M=ceil(110592 p^(-3)) suffices for P(eta>=m)>=m^(-1/3) for every integer m>=M: the exponential factor is at least 1/2 and the remaining constant is absorbed by m^(1/12).

For real h>2 sufficiently large, j=ceil(h^2)<=2h^2, and

    P(eta>=j) >= j^(-1/3) >= 2^(-1/3) h^(-2/3) > 1/h.

This is strict plumpness with exponent 1 after increasing the threshold, with safe rounding. With the generalized inverse Q_eta(u)=inf{z:F_eta(z)>=u}, F_eta(j-1)<1-1/h forces Q_eta(1-1/h)>=j. Start h0 as a sufficiently large integer and define h(n+1)=Q_eta(1-1/h(n)). Every h(n) is finite and integer and

    h(n+1)>=h(n)^2,   h(n)>=h0^(2^n).

For W~Exp(lambda), Q_W(1/h)=-log(1-1/h)/lambda<=2/(lambda h) for h>=2. Thus

    sum_n Q_W(1/h(n)) <= 2/[lambda(h0-1)] < infinity.

The inspected ADGO Equivalence theorem and Theorem 1.3, pp. 6–7, now apply: conditional on retained-tree survival, an iid exponentially weighted retained tree has a finite-total-weight infinite ray. Therefore it has one with positive unconditioned retained-GW probability. The source's p. 7 recurrence displays n>=1 after only h(0) is given; p. 12 recalls the recursion without that omission. Initializing at n>=0 is the intended well-defined recursion, and a finite index shift cannot change this summability conclusion. This is a recorded source detail, not an unsupported replacement theorem.

### Arbitrarily fast positive probability for this fixed retained law

Let V be the infimum of weights of infinite root rays, with V=infinity if none has finite total. It is measurable as the increasing limit of minimum generation distances. Local finiteness and nonnegative weights give the ray interpretation by the finitely branching compactness/Konig argument.

If P(V<a)=0 for some a>0, use countable Ulam labels u. Existence of u depends only on ancestral offspring, whereas the descendant arrays defining V_u have the original unconditioned retained-GW weighted law and are independent of that existence. Hence P(u exists,V_u<a)=0 for each label, and their countable union is null. But a finite-total-weight ray, which has positive probability, has a tail of sum<a at some existing descendant. Contradiction. Therefore P(V<a)>0 for every a>0.

Apply a=H after fixing eta=Bin(xi,exp(-H)). The proof never changes p halfway through and never asserts regeneration under survival conditioning. This resolves the actual time-support gap; qualitative eventual weighted-tree explosion alone would not directly specify this horizon.

### Adaptive arrow clocks and simultaneous finite witnesses

Given the tree and recovery marks, define t_root=0. Recursively at finite generations, let t_child be the first downward arrow after the already defined t_parent and W_edge=t_child-t_parent. Each t_parent uses only ancestor-edge processes. Its outgoing processes have not been used and are independent of that time. At every deterministic shift s, the outgoing first-wait law is Exp(lambda), independently across outgoing edges and independent of s. Induction therefore gives a joint iid exponential edge-weight field independent of the retained tree/recoveries. This proves the required law before choosing a ray; it does not assert independence after a success-biased ray is selected. The full CP first-infection time is not substituted for this ancestor-only time.

On root retention and {V<H}, take a ray with total weight<H. Every vertex on it is retained, and each finite prefix gives a finite downward arrow path arriving before H and avoiding all recovery marks through H. Append its terminal vertical segment to H. Each endpoint is infected at H in the appropriate finite ball. Infinitely many distinct endpoints therefore belong to X_H simultaneously. No infinite-jump path is itself admitted, no vertex at infinity is infected, and no explosive-time Markov restart is invoked.

Multiplying back the independent root-retention probability yields

    P_annealed(|X_H|=infinity)
       >= exp(-H) P_(GW(eta),Exp(lambda))(V<H) > 0.

This derivation has no remaining central mathematical gap. ADGO expressly prints the general weighted-tree input, not this exact contact-process corollary. The coupling is audit-supplied and must be identified as such.

## Independent derivation 2: BKV's ray, waits and residual recovery

### Repaired source hypotheses

Actual BKV Definition 1.7, p. 6, supplies weak power-law tails. The candidate satisfies it with alpha=1/4, including real arguments after integer rounding. Actual Proposition 6.2, p. 46, assumes alpha+mu<1, D>=1 and maximum-degree penalty. The section introduction mentions mu>=1/2, but the published proposition/proof do not impose that lower restriction; mu=0 fits the displayed algebra. A separate inspected 2023-v1 comparison in the contact report covers the classical process through mu=1/2 domination, but the present independent proof uses the actual published body.

The tail separation preceding (100) is essential:

    0<epsilon<alpha(s2-s1)/(s2+s1),
    a=1-(alpha+epsilon)s1>0,
    delta=a-mu s2>0.

With alpha=1/4, mu=0, s1=3/2, s2=2, epsilon=1/64, the strict upper bound is 1/28, a=delta=77/128, and the separating exponent -alpha(s2-s1)+epsilon(s2+s1) is -9/128. The old epsilon 1/16 fails 1/28. The final author bridge is repaired. I checked these as exact rational identities; reviewer agreement is not the reason for acceptance.

For actual parent offspring L, (100)–(101) give a pool of more than L^a/4 eligible children with offspring in [L^s1,L^s2], except probability at most exp(-L^a/48). A minor endpoint equality in the printed tail subtraction can always be read as a lower bound for the inclusive interval; the proof only needs that lower bound. Select M=floor(L^a/4) by deterministic labels, increasing K so M>=L^a/8. Actual nonroot degrees are offspring+1 and root degree is smaller, so every selected edge has rate at least lambda2^(-mu)L^(-mu s2). Consequently

    R_m >= c_mu lambda L^delta,
    c_mu=2^(-mu)/8,  L>=K^(s1^m).

The finite degree offset and rounding modify constants only. Selection uses newly exposed children and does not claim selected degrees remain iid. Starting with {D_root>=K} avoids an unnecessary full-process high-degree hitting-time conditioning.

### Finite time without conditioning on infinite success

Choose the first eligible arrow, an allowed specialization of BKV's child selection. At stage m, W_m~Exp(R_m), H_m~Exp(1) are independent given the selective past/rates; arrival at this fresh vertex was determined without using its recovery process. Success requires W_m<H_m. The local integral is

    E[W_m 1{W_m<H_m} | selective past,rates]
      = integral_0^infinity t R_m exp(-(R_m+1)t) dt
      = R_m/(R_m+1)^2 <= 1/R_m.

Let Z_m be this successful wait when the prefix exists and the pool is available, zero otherwise. The count/race failure bounds give a positive-probability infinite success event A for large K. Also

    E sum_m(m+1)Z_m
      <= (c_mu lambda)^(-1) sum_m(m+1)K^(-delta s1^m)<infinity.

This is an unconditional successful-prefix expectation, or the same expectation conditional only on the initial high-degree event. It is not the unsupported E[W_m|A]. On A, Z_m=W_m, so Tonelli implies S_infinity=sum_m W_m<infinity and sum_m(m+1)W_m<infinity.

An explicit majorant is useful: s1^m>=1+m(s1-1), so with r=K^(-delta(s1-1))<1,

    sum_m(m+1)K^(-delta s1^m) <= K^(-delta)/(1-r)^2.

This tends to0 as K increases. Conditional on initial degree>=K, count/race failure probability tends to0 while this expected total tends to0. Markov's inequality therefore gives positive probability of A and S_infinity<h for every prescribed h>0 after choosing K large. No exact candidate numerical bound follows.

### The residual sigma-field is the decisive recovery check

At a successful stage define E_m=H_m-W_m. With eligible rates r_i and R=sum_i r_i, the density for winner i, successful wait w and residual e is

    r_i exp(-(R+1)w) exp(-e) dw de,   w,e>0.

The exp(-e) factor is independent of wait/winner. Future steps use fresh descendants and never expose the parent's post-arrow recovery. Therefore, conditional on the selective successful skeleton (tree, ray, degrees, waits, winners and success indicators), the residuals are iid Exp(1). Finite-cylinder factorization extends to the countable ray; A has positive probability. This statement would fail if the conditioning included full CP history or selected future recovery behavior. The final bridge avoids both.

Since

    sum_m(S_infinity-S_(m+1))=sum_(j>=1)j W_j<infinity,

the conditional probabilities of a ray vertex's first recovery between its outgoing arrow and S_infinity are summable. Conditional first Borel-Cantelli leaves all but finitely many vertices unrecovered at S_infinity. Earlier ancestors need avoid recovery only until their outgoing arrows; later ancestor recovery does not destroy their already completed path. Each surviving endpoint has a finite graphical witness to the same S_infinity.

For fixed h>S_infinity, the residual-survival indicators have independent conditional probabilities exp(-(h-S_(m+1)))>=exp(-h)>0. Conditional second Borel-Cantelli gives infinitely many endpoints at h. A countable union over integer h gives some deterministic finite h of positive annealed probability; the preceding majorant also permits every prescribed positive horizon with positive probability. Thus simultaneous infinitude, not merely visits to infinitely many sites, follows from the old proof with this short addendum.

### Separate deterministic-interval adaptation

The author family's repaired alternative also passes independently. Put L_m=K^(s1^m), ell_m=K^(-(delta/2)s1^m), s_m=sum_(j<m)ell_j and tau=sum_j ell_j. During [s_m,s_(m+1)] select the first arrow into the pool, consulting only tree/arrows. The conditional stage-failure bound is

    exp(-L_m^a/48)+exp(-c_mu lambda L_m^(delta/2)).

Both sums tend to0 for large K. For example, for b>0,

    K^(b s1^m)>=K^b[1+b(s1-1)log(K)m],

which gives a geometric majorant for exp(-C K^(b s1^m)). Also ell_m<=K^(-delta/2)r0^m, r0=K^(-(delta/2)(s1-1))<1, so

    sum_m(m+2)ell_m <= K^(-delta/2)(2-r0)/(1-r0)^2<infinity.

Keeping the root recovery-free on [0,tau] and v_m on [s_(m-1),tau], m>=1, costs exactly exp(-sum_j(j+2)ell_j)>0 conditional on the selected tree/arrow ray. These windows begin before each incoming arrow. Finite-prefix witnesses then infect every selected endpoint at the common tau. This adaptation is correct; it is another elementary use of the existing pool/rate estimates, not an unsupported replacement central theorem.

## Independent quenched upgrade and exact quantifiers

For classical rates, call a physical tree good when for some positive integer N it has positive conditional probability of |X_N|=infinity. The annealed fixed-horizon deduction at H=1 implies a positive GW probability of being good.

If a child subtree is good, force parent and child to have no recovery in [0,1] and a parent-to-child arrow during that interval. Its probability is exp(-2)(1-exp(-lambda))>0. At time 1 the child is infected. Future subtree marks after the deterministic time 1 are independent and have the original law. Prepend the finite transmission to the child's positive-probability witness at N; this gives one at N+1 for the parent. No restart after explosion or rounding of an arbitrary explosion time is assumed.

With q the GW probability of a bad tree, heredity and independent subtrees give q<=E[q^xi]. Annealed positivity gives q<1. For 0<q<1, xi>=1 and P(xi>=2)>0 imply E[q^xi]<q, contradiction. Hence q=0. Intersect full-measure sets over positive rational rates and use additional-arrow monotonicity to obtain one full-measure tree set for every real lambda>0. Every rate's time/probability may differ.

For the general penalized BKV comparison, use conservative augmented degree D_v+1 even at the root, so that fresh child subtrees have exactly the same rate convention. This only decreases the physical root-edge rates. Every finite bridge rate stays finite and strictly positive. The same deterministic-time heredity proof applies. The auxiliary convention resolves a finite root-degree discrepancy without introducing a new qualitative mechanism.

## Counterimplication and boundary controls

1. **Global survival alone does not imply explosion.** On the deterministic binary tree, the downward first-infection SIR comparison has iid per-vertex offspring with mean2lambda/(1+lambda)>1 for lambda>1; it survives with positive probability. The larger CP therefore survives. Yet maximum degree 3 gives a pure-birth/Yule upper bound on total reached vertices with expected size at most exp(3lambda t), so it is finite almost surely at every fixed finite t. Thus survival is the wrong predicate unless the actual accelerating clock estimates are inspected.
2. **A finite-sum transmission ray alone does not imply simultaneous infection.** As a deterministic graphical schedule, take arrivals t_n=1-2^(-n) and first recovery of v_n at r_n=(1+t_(n+1))/2. Every transmission occurs before its parent's recovery, and infinitely many sites have been visited before 1. At every t<1 only finitely many have arrived; at 1 all have recovered. This is a logical counterexample to the bare path implication, not a positive-probability counterexample to the Poisson residual/thinning proofs. Those proofs supply precisely the missing recovery information.
3. **Annealed positivity alone is not almost-every-environment positivity.** An arbitrary mixture of favorable/unfavorable trees would violate that inference. Here the independent GW regeneration, positive offspring and strict fixed-point inequality are actually used. Dropping those hypotheses removes this proof.
4. **A zero-probability all-ray retention event is not used.** Requiring an independently chosen infinite ray's every vertex to be recovery-free through H would cost zero. The ADGO route instead studies a random retained branching subtree that itself survives/explodes with positive probability. The BKV-window route instead has summable late-vertex windows.
5. **H=0 and lambda=0 are excluded.** At time0 the configuration is root-only; without arrows there is no spread. Positivity for very small H/lambda is not a uniform lower bound. Infinite mean alone is not substituted for plumpness; the exact retained tail proves plumpness. The b=2 boundary mentioned by the original authors is outside this example and is not settled here.
6. **No infection from infinity.** Every endpoint has a finite path inside a finite ball. No uniqueness or dynamics after explosion is needed. The almost-sure original local finiteness and finite individual rates remain intact.

## Primary interpretation and credit

The actual OWR pp. 618–620 support the existential interpretation and constant-fitness case. The primary question does not demand unbounded fitness, classify every infinite-mean law, or bundle the adjacent questions into this target. The displayed finite-mean theorems do not refute the accepted infinite-mean construction.

ADGO pp. 2/6/7/12 explicitly give the weighted-tree model, plumpness, survival conditioning and quantile criterion. They do not expressly print an active-contact-population theorem. The audit's retention/finite-path proof is therefore category(b), even though the printed general input predates the OWR question.

BKV p. 17 explicitly uses finite graphical paths and admits explosion. Its pp. 46–48 print a survival proposition and the accelerating degree/pool/rate estimates. The proof plus the independently verified timing/residual or deterministic-window addendum gives the same qualitative phenomenon. It would overstate the source to call Proposition 6.2 a printed simultaneous-explosion theorem; it would understate it to call its method merely loosely related.

2406.12689v1 p. 15 and v2 p. 16 expressly discuss finite-time explosion for offspring mass exponent b in (1,2), point to BKV Proposition 6.2, and suggest removing the penalization. The candidate mass m^(-1/4)-(m+1)^(-1/4) is asymptotic to (1/4)m^(-5/4), so b=5/4 lies within that prior discussion. Its qualified language is not an exact theorem, but it is affirmative prior anticipation of this regime and route. That credit must accompany any future presentation.

The primary contact-family and branching-family comparisons identify older growing-degree, residual-life, contagious-period and thinning antecedents. I have not personally re-proved every peripheral cited theorem, and no negative conclusion over the entire literature follows. The integrated root full-read receipt closes the dated Pemantle–Stacey retrieval gap; its bounded-degree source exclusion is consistent with the explicit Yule control above. These extra exclusions are not premises needed to establish the decisive positive ADGO/BKV implications.

## Disposition under the authorized research process

The submitted row's claimed_solved status made this case eligible for audit. It is not an acceptance or a novelty finding. The project aims at novel independently verifiable contributions and requires a deep priority audit before its paper/publication sequence. This audit supplies positive reasons against a new qualitative solution claim, rather than merely an unsuccessful search for an exact theorem.

For the exact historical existential question, recommend a fresh **already_solved** assessment, explicitly saying that the affirmative answer is a demonstrated elementary consequence of established theory. Do not erase the original claimed_solved row or its proof. Do not mark the original existential target merely partial: the old-theory corollary resolves the whole exact existential claim. If the workflow preserves a **credited partial contribution**, that phrase should describe the explicit quantitative artifact's unestablished research value, or a separate clearly defined refinement target, not an alleged unsolved portion of the old question.

The candidate's explicit time 1/(2lambda) and lower bound (7/30)exp(-3/(2lambda)) remain a checked, useful concrete estimate. Neither derivation above gives those constants. But "not present in the inspected sources" does not establish bound priority; "self-contained" does not establish mechanism novelty; an all-rates quenched formulation is already obtainable by the separate elementary inheritance argument. No numerical sharpness, optimality, substantially broader criterion, or independent significance result is established here.

Accordingly I recommend **HOLD the novel-research-paper pipeline for this target**. Preserve the candidate and the attributed corollary derivations as credited audit/research evidence. A modest quantitative/expository note could be truthfully framed if Parent decides it is appropriate under the human's process, but the reports' conditional note GO does not automatically clear novel-contribution priority, merge, immutable publication, or a DOI tracker entry. No paper was prepared in this task. Any subsequent promotion needs a separately stated quantitative/refinement claim, affirmative originality/significance evidence, complete credit, and fresh whole-package review. The exact remaining gap is that priority/significance gate, not the mathematical existential proof.

This is not a claim that no prior author printed the CP corollary anywhere, that the present coupling is first, that the entire infinite-mean problem was settled universally, or that the b=2 boundary is now open. It is a bounded positive derivability verdict with precisely identified source inputs.

## Completion and reproducibility

Best-guess completion of this assigned independent integration adversary: 100%. The inherited whole-case 35% and priority 70% figures remain as-of inputs only; Parent must set final disposition/progress. Completion of this bounded review is neither 100% novelty confidence nor publication acceptance.

`RESEARCH_LOG.md` records UTC checkpoints and estimates. `INPUT_MANIFEST.json`, `ESSENTIAL_SOURCE_MANIFEST.json` and `READ_SCOPE_RECEIPT.json` pin actual inputs/read scopes; `INDEPENDENT_REHASH_AND_ALGEBRA.json` records 33 candidate and 893 family-entry controls plus exact rational arithmetic. `verify_inputs.py` independently replays frozen input identity and rational controls without touching inputs. `OUTPUT_MANIFEST.json` pins all owned deliverables and rendered pages, excluding itself. Hash/location controls are reproducibility evidence, not an automated substitute for the proofs above.
