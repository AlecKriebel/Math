# Bounded priority assessment and older-theory contact-process bridge

Prepared 2026-10-12 UTC as a credited audit correction, not a research paper. Underlying candidate author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This document adapts the accepted branching-family derivation and its independent bridge adversary, as checked again by the NEW consolidated adversary and accepted in Root's final qualitative-priority receipt. It records their mechanism and evidence with attribution; it is neither a fresh author proof attempt nor a firstness claim for this coupling.

## Assessment and exact boundary

The whole historical existential target is **`already_solved`, category (b): an elementary consequence of older general theory, with the necessary contact-process coupling supplied in the audit**. Category (a), an expressly printed exact older CP theorem, was not located in this bounded review. Category (c), a central unsupported implication left for the candidate, does not describe the complete bridge below. There is no exhaustive absence or earliest-priority claim.

The accepted law has finite positive integer offspring xi with P(xi>=m)=m^(-1/4). Start only at the root, with independent ordered rate-lambda arrows, rate-one recoveries and finite-path graphical infection, equivalently the increasing coupled finite-ball union. Constant fitness F=1 is allowed by OWR printed pp. 618–620 and original arXiv:2110.14537v1 pp. 4–5. The historical question on printed p. 619 asks whether explosion can occur with infinite offspring mean; one admissible example resolves its exact existential content. Other questions and universal infinite-mean criteria are outside scope.

The old-theory consequence proved here is

    for every fixed lambda>0 and H>0, P_annealed(|X_H|=infinity)>0.

An elementary separate hereditary argument gives almost-every-tree positivity at some finite time for every positive rate. PROOF.md's accepted explicit time1/(2lambda) and lower bound(7/30)exp(-3/(2lambda)) are preserved. The derivation below supplies no such numerical bound. Originality, sharpness, optimality and research significance of that bound remain unestablished. No first-solution, current-openness, new-mechanism, paper, merge, publication or DOI clearance follows. Root owns final PR/user disposition under the originally claimed_solved eligibility policy.

## Primary inputs, pages and actual reading scopes

| Source | Decisive actual body location | Audited reading and provenance |
|---|---|---|
| OWR12/2022, DOI10.4171/owr/2022/12, [official report](https://ems.press/content/serial-article-files/46949) | Printed618–620 = PDF42–44; exact question619 | Source-fidelity and author-version families read/viewed all three contribution pages. Consolidated adversary independently read/viewed PDF42–44. |
| Amini–Devroye–Griffiths–Olver, *On explosions in heavy-tailed branching random walks*, AnnProb41(3B),1864–1899(2013), DOI[10.1214/12-AOP806](https://doi.org/10.1214/12-AOP806), [arXiv1102.0950v3](https://arxiv.org/pdf/1102.0950v3) | Reprint/PDF2: weighted-ray explosion;6: plumpness, survival-qualified Equivalence theorem;7:Theorem 1.3;12:recalled recursion | Branching family read all36 reprint pages in four complete chunks. Bridge adversary checked decisive pages. Consolidated adversary independently read/viewed2,6,7,12. Reprint pagination differs from journal1864–1899. |
| Bartha–Komjáthy–Valesin, *Degree-penalized contact processes*, DOI[10.1017/fms.2025.10144](https://doi.org/10.1017/fms.2025.10144), Sigma14(2026)e6; [arXiv2310.07040v1](https://arxiv.org/pdf/2310.07040v1),10October2023 | Publisher6:Definition 1.7;17:(19), finite-path process;46–48:Proposition 6.2/proof,(100)–(107). v1 pp38–41, narrower mu domain | Contact family collectively read all 85 publisher pages, personal1–18,45–48,82–85 plus delegated19–45,49–82. Timing adversary independently checked17,46–48. Consolidated adversary independently read/viewed6,17,46–48. v1 essential38–41 separately read. |
| Cardona–Tobón–Ortgiese–Seiler–Sturm, *The contact process on dynamical random trees with degree dependence*, [arXiv2406.12689v1](https://arxiv.org/pdf/2406.12689v1),18June2024; [v2](https://arxiv.org/pdf/2406.12689v2),10March2026 | v1 pp15–16; v2p16:classical explosion discussion and BKV route | Author-version family read full 55-page v2; v1 pp1–30,55–56, not entire 56-page v1. Consolidated adversary independently read/viewedv1 15–16/v2 16. Qualified prior anticipation, not an exact bound theorem. |
| Original fitness paper2110.14537v1–v4 and actual Cambridge publisher DOI[10.1017/apr.2026.10066](https://doi.org/10.1017/apr.2026.10066) | v1 model4–5/nonexplosion12; v2–v4 nonexplosion11; publisher nonexplosion10 | Author-version family fully read actual42/42/38/41-page versions and37-page publisher paper. Finite mean is retained; these nonexplosion theorems do not apply to the example. |

The C3 editor fully read all distinct C2 files, the seven final decisive family reports/bridges/adversaries, Root's math/source acceptance, the full consolidated report and Root's final qualitative receipt. The editor did **not** personally reread these primary manuscripts or perform new proof/literature search. The table attributes actual primary scopes to their readers; extraction, hashing and copied records are not substituted for reading.

Local audit evidence is recorded by repository-relative identifiers under `draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/`: `priority_branching_explosion_20261012/REPORT.md` and `bridge_adversary/verification.md`; `priority_contact_literature_20261012/REPORT.md`, `BKV_PROOF_IMPLICATION.md`, `timing_adversary/REPORT.md`; `priority_author_versions_20261012/AUTHOR_VERSIONS_PRIORITY_REPORT.md` and `BKV_ESTIMATES_BRIDGE.md`; `consolidated_priority_adversary_20261012/REPORT.md`; `ROOT_SCOPED_MATH_SOURCE_ACCEPTANCE.json`; `root_priority_20261012/ROOT_FINAL_QUALITATIVE_PRIORITY_ADJUDICATION.json`. Their hashes/read scopes are pinned in the owned audit input manifest and source_manifest.json. No primary PDFs are copied into this candidate.

## Full ADGO-to-CP deduction

**1. Fix the horizon before thinning.** Fix lambda>0 and H>0 and p=exp(-H). Retain each vertex iff its recovery process has no mark in[0,H]. Indicators are iid Bernoulli(p), independent of offspring and arrows. Condition only on retaining the root. Its root-connected retained component is an ordinary unconditioned GW tree with offspring

    eta | xi ~ Binomial(xi,p).

At a retained vertex, existence/retention depends on ancestral offspring/indicators and its own retention, not its own offspring or children's retention. Generation exploration gives iid eta rows. Root retention does not bias xi. Retained-tree survival conditioning is used only later for ADGO, not for descendant regeneration.

eta is finite a.s. and has positive zero mass, at least P(xi=1)(1-p)>0, so it may die despite the physical tree's no leaves. Eeta=pExi=infinity. Choose finite K with E min(eta,K)>1. The bounded-offspring process with Z=min(eta,K) embeds below it and survives positively: g(s)=E[s^Z] has g(0)>0,g(1)=1,g'(1)>1, so g(s)<s just below1 and a fixed point below1. Its increasing extinction iteration from0 has limit below1. Thus the retained tree has positive survival probability, exactly the conditioning required by ADGO.

**2. Verify strict plumpness, with integer rounding.** For integer m>=1 put k=ceil(2m/p). On{xi>=k}, retain its first k children, independently of that event. Because kp>=2m and k<=3m/p, the half-mean Chernoff bound gives

    P(eta>=m) >= k^(-1/4) P(Bin(k,p)>=m)
       >= (p/3)^(1/4)m^(-1/4)(1-exp(-m/4)).

For M=ceil(110592p^(-3)), every m>=M has exponential factor>=1/2 and ((p/3)^(1/4)/2)m^(1/12)>=1. Hence P(eta>=m)>=m^(-1/3). For sufficiently large real h>2 and j=ceil(h^2)<=2h^2,

    P(eta>=j) >= j^(-1/3)
       >= 2^(-1/3)h^(-2/3) > 1/h.

This is the required plumpness with exponent1 and strict slack. Infinite mean by itself would not verify that hypothesis.

**3. Check the published quantile criterion.** Define generalized inverse Q_eta(u)=inf{z:F_eta(z)>=u}. Choose large integer h0>=max(M,3), and set h(0)=h0,h(n+1)=Q_eta(1-1/h(n)) for n>=0. Each quantile is finite because eta is finite a.s. The strict tail inequality gives F_eta(j-1)<1-1/h, so h(n+1)>=j>=h(n)^2 and h(n)>=h0^(2^n). For W~Exp(lambda),

    Q_W(1/h) = -log(1-1/h)/lambda <= 2/(lambda h), h>=2,
    sum_n Q_W(1/h(n)) <= 2/[lambda(h0-1)] < infinity.

ADGO's Equivalence theorem and Theorem 1.3, reprint pp6–7, now imply a finite-total-weight infinite ray a.s. conditional on retained-tree survival. Positive survival gives positive **unconditioned** probability of such a ray. The source's p7 display gives h0 but writes n>=1, leaving h1 unspecified; p12 recalls the recursion without that omission. The explicit n>=0 initialization is the well-defined intended recurrence, and a finite index shift cannot change summability. This recorded indexing detail is not an unproved replacement theorem.

**4. Recover this exact horizon using unconditioned regeneration.** Let V be the infimum of total weights of infinite root rays, infinity if none has finite total. On a locally finite nonnegative-weight tree it equals the increasing limit of minimum root-to-generation weights: if finite-level minima are bounded by a, the finitely branching tree of paths with sums<=a has a ray by compactness/Konig. This gives measurability and the ray interpretation.

Claim P(V<a)>0 for every a>0. Otherwise use countable Ulam labels u. Existence of u depends only on ancestral offspring, while V_u is defined from independent descendant offspring/weights with the original unconditioned retained-GW law. Thus P(u exists,V_u<a)=0 for every u. Their countable union is null. Yet the positive-probability finite-total root ray has tail sum<a at some existing descendant, contradiction. Apply a=H after fixing eta=Bin(xi,exp(-H)); neither p nor the model changes during the argument. Survival-conditioned regeneration is never asserted.

**5. Couple exponential waits to fresh downward arrows.** Conditional on the physical tree/recoveries, define t_root=0. At each finite generation, t_child is the first downward arrow after t_parent, and W_edge=t_child-t_parent. t_parent depends solely on finitely many ancestor-edge processes. Its outgoing processes are unused, independent of that time and of one another. At every deterministic shift s their first waits are independent Exp(lambda), with law independent of s. Induction over generations therefore yields a joint iid exponential edge field independent of retained tree/recoveries. Establish this law before selecting any ray; do not claim it remains unbiased after success-based ray selection. The ancestor-only constructed time is used, not a full CP first-infection time that might depend on that edge.

**6. Certify simultaneous infection by finite witnesses.** On root retention and{V<H}, some infinite ray has total weight<H. Every finite prefix arrives before H and every vertex on it is recovery-free through H. For each endpoint, prepend its finite sequence of arrows and append a vertical segment to H. This is an ordinary finite infection path contained in a finite ball of its depth. Thus infinitely many distinct endpoints belong to X_H simultaneously. No infinite-jump path is admitted, no endpoint at infinity is infected and no post-explosion Markov restart is invoked. Restoring the independent root retention gives

    P_annealed(|X_H|=infinity)
       >= exp(-H) P_(GW(eta),Exp(lambda))(V<H) > 0.

This completes the qualitative historical existential target using the printed old general theorem and explicit audit coupling. H=0/lambda=0 are excluded; small positive horizons/rates need not have uniform positive bounds.

**7. Separate quenched/all-rates upgrade.** For fixed classical lambda, call a physical rooted tree good if for some positive integer N it has positive conditional probability of|X_N|=infinity. Step6 at H=1 gives positive GW probability of goodness. If a child subtree is good, require no parent/child recoveries on[0,1] and an arrow across their edge during that interval, probability exp(-2)(1-exp(-lambda))>0. At time1 the child is infected; future descendant marks are independent and stationary. Concatenating finite witnesses gives parent positivity at N+1. This uses deterministic-time future marks, not restarting at an explosion.

With q the GW probability of a bad tree, parent bad implies all child subtrees bad, so q<=E[q^xi]. Positivity gives q<1. Since xi>=1 and P(xi>=2)>0, E[q^xi]<q for0<q<1, contradiction; hence q=0. Intersect over positive rational rates and add arrows for larger real rates. One full-measure tree set then works for every lambda>0, with a time/probability that may depend on tree/rate. Finite fitnesses>=1 add independent finite-rate arrows and preserve both conclusions. No uniform quenched or probability-one dynamics claim follows.

## Independent corroboration and credit limits

BKV's existing eligible-child pools and rates also give the qualitative answer. Its published Definition 1.7 and Proposition 6.2/proof admit alpha=1/4,mu=0. Choose s1=3/2,s2=2,epsilon=1/64; separation requires epsilon<alpha(s2-s1)/(s2+s1)=1/28, and a=delta=77/128. The earlier audit epsilon=1/16 failed that separation condition and was repaired in final evidence. Restoring graph degree=offspring+1 and integer pool floors changes only constants: total first-arrow rate R_m>=c_mu lambda K^(delta s1^m), c_mu=2^(-mu)/8 for large K.

The independent contact-family addendum chooses first eligible arrows and reveals only pre-arrow recovery success. For W_m~Exp(R_m),H_m~Exp(1), local successful wait expectation R_m/(R_m+1)^2<=1/R_m. Successful-prefix variables, set to0 on failure, imply weighted wait summability on the positive infinite-success event; no unsupported expectation conditional on that event is needed. With winner rate r_i, successful wait w and residual recovery e, the density factors as r_i exp(-(R_m+1)w)exp(-e)dw de. Future selective ray steps never reveal old residuals, giving independent Exp(1) residuals conditional on the selective skeleton. Weighted remaining durations are summable, so conditional Borel–Cantelli leaves infinitely many simultaneous endpoints at the limiting time; independent residual survival also gives fixed finite horizons of positive probability. Every endpoint has a finite witness. The separately verified deterministic-window bridge is another valid adaptation of the same existing estimates. Survival alone or a bare finite-weight transmission ray alone would not justify simultaneity.

Original-author2406v1 pp15–16/v2p16 expressly anticipated classical explosion for b in(1,2) and this BKV route. The present mass m^(-1/4)-(m+1)^(-1/4) is asymptotic to(1/4)m^(-5/4), squarely b=5/4. This prior discussion must be credited even though it is qualified prose rather than the printed numerical theorem. Older epidemic contagious-period/thinning and increasing-degree/residual-life antecedents are documented in the final family reports; no exhaustive earliest attribution is claimed here.

The final consolidated adversary independently verified both positive qualitative implications and the repaired BKV algebra. Root's final receipt accepted `already_solved` for the qualitative target and maintained HOLD on novel-research-paper/publication. A reviewer family's conditional GO for a truthful quantitative/expository note does not establish originality, significance or permission to publish it. The exact remaining research gap is a separately defined refinement with affirmative originality/significance evidence. This correction provides checkable mathematics, complete credit and preservation; it neither prepares a paper nor authorizes merge/publication.
