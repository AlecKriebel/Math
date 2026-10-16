# Independent analytic validation of the exact credited C3 content

This is a NEW verification derivation, not a new substantive author attempt or a literature/proof search. It checks the fixed, complete candidate and its attributed prior implications. All probabilities below concern the finite-path graphical process unless a weighted GW tree is explicitly specified.

## Explicit quantitative theorem: reconstruction and attacks

The mass function is the telescoping difference m^(-1/4) minus (m+1)^(-1/4). It is positive, sums to 1, puts no mass at infinity, and has divergent tail sum. Since every realized offspring count is finite, induction makes each generation and finite-radius ball finite. Countable intersection gives local finiteness of the entire tree. Offspring is always positive, with positive mass above one; these last two facts will be used in the quenched argument, not merely in showing infinite mean.

For a fixed finite lambda>0 put tau=1/(2lambda), s_n=tau(1-2^(-n)), and D_n=16^(n+2). Then ell_n=s_(n+1)-s_n=2^(-n-2)/lambda, and the root event xi_root>=256 costs exactly 1/4. At a selected vertex with its own known offspring at least D_n, inspect its first D_n children. For each child the qualifying event uses its own offspring and its incoming arrow process during the deterministic interval [s_n,s_(n+1)). Previous selection exposed neither those children's offspring nor the selected parent's outgoing processes. The selected parent's own offspring is biased, but that bias cannot affect the independent descendant coordinates now queried. Therefore the D_n indicators are conditionally iid with parameter

    p_n=2^(-n-3)(1-exp(-2^(-n-2))).

Writing x=2^(-n-2), one has 0<x<=1 and 1-exp(-x)>=x-x^2/2>=x/2. Hence D_n p_n>=4^(n+1). The first-failure events are disjoint, and conditional failure at stage n is bounded by exp(-4^(n+1))<=16^(-n-1). Their conditional sum given the root event is at most 1/15; no independence between stage events is required. Thus the infinite ray event G has probability at least (1/4)(14/15)=7/30.

G and the complete ray are measurable in the tree/arrow field alone. Condition on this field. Distinct selected vertices have independent rate-one recovery processes. Guard the root throughout [0,tau], and vertex n>=1 throughout [s_(n-1),tau]. The total forbidden length through vertex N is

    tau + sum_(n=1)^N tau 2^(-n+1) = 3tau-2tau 2^(-N).

It tends to 3tau. The finite no-recovery events decrease, so their conditional probabilities tend to exp(-3tau)>0. A guard window starts before the incoming arrow, and persists through the common horizon. Induction in n produces an ordinary finite infection path to each ray vertex at tau, contained in its depth-n ball. Thus all ray vertices are infected simultaneously, yielding exactly

    P(|X_tau|=infinity)>=(7/30)exp(-3/(2lambda)).

Potential counterarguments were checked: the conditional degree bias is real but is never asserted away; an unbounded but finite offspring count does not make a finite ball infinite; endpoints of deterministic intervals have probability zero in the countable Poisson field; infinitely many completed prefixes are not treated as one admitted infinite-jump path; and the shrinking guards, rather than a zero-probability infinite product of equal-duration guards, account for recovery.

## ADGO general theorem to the exact contact-process claim

The primary ADGO pages personally read are 2, 6, 7 and 12. They supply the weighted-ray meaning of explosion, plumpness, the survival-conditioned Equivalence theorem, and the quantile summability criterion. They do not print a contact-process simultaneous-population theorem. The following coupling is the audit's deduction.

Fix lambda>0 and H>0 first, and put p=exp(-H). Independently retain each physical vertex if its recovery process has no marks on [0,H]. Conditional only on retaining the root, its connected retained component is an ordinary unconditioned GW tree with eta|xi distributed as Bin(xi,p). To see this, expose generations: whether a retained vertex exists uses its ancestral offspring and its own retention, but not its offspring or its children's retention marks. Retention and offspring are independent. This is the required regeneration statement before any survival conditioning.

E eta=p E xi=infinity, although eta can equal zero with positive probability. By monotone convergence there is a finite K with E min(eta,K)>1. The bounded-offspring GW process with this truncated law embeds below the retained tree. Its generating function has derivative greater than one at 1 and is strictly below the diagonal just to the left of 1. Since its value at zero is positive, it has an extinction fixed point below 1. Consequently the retained component survives with positive probability. This explicitly supplies ADGO's conditioning event.

For integer m>=1 take k=ceil(2m/p). On xi>=k the first k children supply a Bin(k,p) subcount. Since kp>=2m and k<=3m/p, the half-mean Chernoff inequality gives

    P(eta>=m)>=(p/3)^(1/4)m^(-1/4)(1-exp(-m/4)).

For m>=M=ceil(110592p^(-3)), the exponential factor is at least 1/2 and the remaining constant times m^(1/12) is at least 1. This follows by raising the required inequality to the twelfth power: the threshold is 2^12 3^3 p^(-3)=110592p^(-3). Thus P(eta>=m)>=m^(-1/3) throughout that range.

For all sufficiently large real h>2 let j=ceil(h^2). Then j<=2h^2 and

    P(eta>=j)>=j^(-1/3)>=2^(-1/3)h^(-2/3)>1/h.

The strict final inequality avoids discrete inverse-CDF ambiguity. F_eta(j-1)<1-1/h implies Q_eta(1-1/h)>=j. Choose large integer h0 and recurse h_(n+1)=Q_eta(1-1/h_n). These finite integers satisfy h_n>=h0^(2^n). Exponential weights have Q_W(1/h)=-log(1-1/h)/lambda<=2/(lambda h) for h>=2. Since 2^n>=n+1,

    sum_n Q_W(1/h_n)<=2/[lambda(h0-1)]<infinity.

ADGO therefore yields a finite-weight infinite ray almost surely conditional on survival, and hence with positive unconditioned retained-GW probability. The recurrence's n>=1 display on page 7 leaves the first iterate unspecified; page 12 recalls the well-defined recurrence. Initializing at n=0 and allowing a finite index shift does not alter summability. C3 explicitly records this source detail rather than silently changing it.

A separate short-time-support argument is essential. Let V be the infimum of infinite-ray sums, or infinity if there is no finite ray. The minimum root-to-generation weight is nondecreasing, and its limit equals V by finitely branching compactness: if all minima are <=a, the tree of prefixes whose sums are <=a has arbitrarily great depth and therefore an infinite ray. This also makes V measurable. If P(V<a)=0 for some a>0, every existing Ulam-labelled descendant would almost surely have V_u>=a, since label existence uses only ancestral offspring and its descendant weighted arrays retain the original unconditioned law. A countable union preserves that assertion. But any finite-total root ray has a tail sum below a at some descendant, a contradiction on the positive-probability explosion event. Thus P(V<a)>0 for every a>0 for this fixed retained law. This argument uses no regeneration conditional on survival and never changes p after selecting H.

Finally construct downward waits from actual arrows. Set t_root=0 and define t_child as the first downward arrow after t_parent. Every t_parent depends only on ancestor-edge processes; all its outgoing processes remain independent of that time. Their shifted first waits have independent Exp(lambda) laws whose conditional joint law does not depend on the shift. Finite-generation induction gives the iid exponential weight field, independent of the retained tree/recoveries, before ray selection. Using the actual full-process first-infection time instead would risk revealing the tested edge and is correctly avoided.

On root retention and V<H, choose a ray with total sum below H. All its prefixes arrive before H, and every retained vertex has no recovery through H. Each endpoint has a finite arrow/vertical path to H. Hence

    P(|X_H|=infinity)>=exp(-H)P_GW(eta),Exp(lambda)(V<H)>0.

The infinite ray is used to supply countably many finite witnesses; it is not itself admitted as a space-time path to a vertex at infinity. This finishes the exact historical existential target by an established theorem plus the audit coupling, with no central unsupported implication.

## BKV corroboration, repaired epsilon and recovery conditioning

The personally inspected published BKV pages 6,17,46–48 show weak power-law tails, finite graphical paths and a proposition printed as global survival. Its displayed proposition/proof allow alpha=1/4, mu=0 even though the section introduction advertises the mu>=1/2 regime. The independently inspected 2023 v1 pages 38–41 have mu in [1/2,1) in Proposition 6.2; alpha=1/4 and mu=1/2 satisfy alpha+mu<1, and the classical rates dominate this penalized process.

The published estimate requires both positive growth exponent and tail separation. For s1=3/2,s2=2,epsilon=1/64,mu=0,

    epsilon<alpha(s2-s1)/(s2+s1)=1/28,
    a=delta=1-(alpha+epsilon)s1=77/128,
    -alpha(s2-s1)+epsilon(s2+s1)=-9/128.

The earlier epsilon=1/16 fails the strict separation, even though some positive-growth inequalities would still pass. C3 contains the repaired value. For actual offspring L sufficiently large, a pool of floor(L^a/4)>=L^a/8 exists except probability <=exp(-L^a/48). The inclusive tail interval can be lower-bounded by the difference of the two tails, so an endpoint equality typo does not invalidate the bound. Restoring physical nonroot degree offspring+1 gives an edge rate >=lambda 2^(-mu)L^(-mu s2). Therefore total pool-arrow rate satisfies R_m>=c_mu lambda K^(delta s1^m), with c_mu=2^(-mu)/8.

The selective construction begins at the high-degree root, uses fresh descendants, and chooses the first pool arrow. At stage m, arrival at a fresh vertex has revealed none of its recovery process. Given selective past and local rates, W_m is Exp(R_m), H_m is Exp(1), and they are independent. The successful-prefix expectation is

    E[W_m 1_(W_m<H_m)]=R_m/(R_m+1)^2<=1/R_m.

This differs from the biased expectation conditional on an infinite success event. Put the wait to zero when the prefix/pool/success fails. The deterministic rate lower bounds give finite unconditional expectation of the weighted sum (m+1)Z_m. The stage failure sums tend to zero as K grows, so the infinite success event A has positive probability. Tonelli then gives sum_m(m+1)W_m<infinity on A. The majorant K^(-delta)/(1-K^(-delta(s1-1)))^2 also shows arbitrarily small positive total-time support after increasing K.

For a winner of rate r_i, successful wait w and post-arrow residual e, the joint density is

    r_i exp(-(R_m+1)w)exp(-e) dw de.

The residual factor is independent of the selective winner/wait. Subsequent ray steps inspect fresh descendants and never inspect this old residual. Finite-cylinder factorization therefore gives iid Exp(1) residuals conditional on the successful selective skeleton, including its whole ray/waits/A. Such independence would fail for conditioning on full CP history; C3 uses the smaller selective information.

If S_infinity=sum W_m, then sum_m(S_infinity-S_(m+1))=sum_(j>=1)j W_j<infinity. Conditional first Borel–Cantelli implies only finitely many selected vertices recover after their outgoing arrow but before S_infinity. All later vertices consequently have finite path witnesses at that common time. For any deterministic h>S_infinity, their independent residual-survival probabilities are at least exp(-h), so conditional second Borel–Cantelli gives infinitely many endpoints at h. The small-time-support majorant gives positive probability of S_infinity<h for each prescribed h>0. This verifies the qualitative consequence, without importing the candidate's numerical coefficient.

The alternative deterministic-window adaptation uses ell_m=K^(-(delta/2)s1^m). Tree/arrows select the ray without recoveries; the pool/no-arrow errors are summable. The sum of required recovery-window lengths is sum_m(m+2)ell_m<infinity. Its conditional no-recovery probability is positive, and guards start before incoming arrows. This is another valid elementary use of the old estimates, not a claim that BKV printed the exact simultaneous theorem.

## Quenched/all-rates and fitness boundaries

Fix lambda and call a physical tree good when at one of the countable deterministic times tau+m the root-started process has positive probability of infinite simultaneous infection. The quantitative bound implies positive GW probability of goodness. A good child makes the parent good: forbid parent/child recovery through time 1 and require a parent-child arrow in [0,1/2]. This event has probability exp(-2)(1-exp(-lambda/2))>0. At time 1 the child is infected, and future marks are independent and stationary. Suppress outside edges, concatenate the finite access path and the child's future finite witnesses, and obtain a parent witness at tau+m+1. This is a deterministic-time comparison, not a restart at explosion.

With b the probability of badness, inheritance and independent offspring subtrees imply b<=E[b^xi]. Annealed positivity gives b<1. If 0<b<1, positive offspring gives b^xi<=b, with strict inequality on xi>=2, which has positive mass. Thus E[b^xi]<b, a contradiction. Hence b=0. Countable intersection over positive rational rates gives one full-measure tree set; any real lambda>0 dominates a positive rational rate and inherits positivity at that rate's finite time. No common quenched time or uniform lower probability is derived.

For any fixed finite fitness assignment F_v>=1, add arrows independently at rate lambda(F_uF_v-1) on each ordered edge. Every individual rate is finite, and the same base infection paths remain. This works for arbitrary fixed finite assignments, including iid finite values with unbounded support. The boundary lambda=0 is excluded, since no arrows spread the root infection. H=0 is excluded, since only the root is initially infected. Fitness approaching zero, infinite fitness and universal infinite-mean classification are not covered.

## Falsifiable countercontrols and credit conclusions

On a bounded-degree binary tree, the downward SIR comparison has offspring mean 2lambda/(1+lambda)>1 for lambda>1, so global survival is possible. Yet total reached vertices are dominated by a Yule process of per-particle rate 3lambda, finite at each fixed finite time. Survival alone is therefore insufficient.

A deterministic schedule arriving at v_n at 1-2^(-n) and recovering after its outgoing arrow but before 1 gives a finite-sum ray and infinitely many cumulative visits, with no simultaneous infection at time 1. Recovery information is therefore essential. This is a logical counterexample to a bare implication, not a positive-probability refutation of the correctly guarded Poisson construction.

If offspring can be zero, the strict hereditary fixed-point contradiction can fail: a law with mass 1/2 at zero and 1/2 at two has generating function (1+b^2)/2, which exceeds b for b=1/2. If every vertex has one child, it is exactly b. The actual positive, nontrivial offspring law avoids both failures. An arbitrary mixture of environments likewise would not permit inferring almost-every-environment positivity merely from annealed positivity.

The original-author 2024 v1 pages 15–16 and 2026 v2 page 16 expressly discuss the classical explosion regime and BKV route in qualified prose. The candidate mass is asymptotic to (1/4)m^(-5/4), putting b=5/4 in their stated (1,2) range. This is affirmative anticipation, not an exact printed numerical bound. ADGO's general theorem plus coupling already resolves the full exact existential target. The numerical bound is verified, while its firstness, sharpness, optimality and research significance remain unestablished. A credited partial artifact refers to the contribution's scope/value, not an unsolved residual of the historical target.
