# Independent adversarial verification: fixed-horizon contact-process bridge

Author: independent audit agent, bridge_adversary. Work began 2026-10-12 00:55:44 UTC. This report does not use other priority-agent outputs. No external outreach, Git mutations, provider mutations, or publication were performed.

## Verdict and exact claim

**VERIFIED as a deduction from the published ADGO general explosion theorem, under the process definition specified below.** No mathematical gap or counterexample was found. This is an elementary contact-process corollary derived in this audit; it should not be described as a contact-process theorem explicitly stated by ADGO.

Let T be an ordinary rooted Galton-Watson tree with iid, almost surely finite integer offspring xi >= 1 and

    P(xi >= m) = m^(-1/4),  m = 1, 2, ... .

Independently give every ordered adjacent pair an independent rate-lambda Poisson arrow process, and every vertex an independent rate-1 Poisson recovery process. Initially only the root is infected. Define X_t by infection paths that start at the root at time 0, have finitely many arrow jumps, move forward in time, and avoid all recovery marks on vertical pieces. Equivalently, take the union of the coupled contact processes on finite balls around the root.

Then, for every fixed H > 0 and lambda > 0,

    P_annealed(|X_H| = infinity) > 0.

The probability integrates over T, arrows, and recoveries. It is not asserted to equal one, to be uniformly bounded below in H or lambda, or to hold for every fixed locally finite tree. Only finite infection paths are admitted. The conclusion therefore does not use an infinite-jump path as an infection path.

## Primary-source receipt

Pinned source: Amini, Devroye, Griffiths and Olver, *On explosions in heavy-tailed branching random walks*, Annals of Probability 41(3B), 1864-1899 (2013), DOI 10.1214/12-AOP806; arXiv:1102.0950v3, 14 June 2013.

PDF:

    /Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_branching_explosion_20261012/sources/adgo2013.pdf

Verified SHA-256:

    adde8c3c1dffff0c8fb29ab7a6f8ed15da69b1f8212e54257d11fe81137eaf22

Relevant PDF pages 2, 6, 7 were rendered and visually inspected in full; their text agrees with the supplied extraction. PDF page 2 identifies explosion with existence of an infinite ray having finite total nonnegative edge weight. Page 6 defines plump offspring and states its Equivalence theorem for the Galton-Watson tree conditioned on survival. Page 7, Theorem 1.3, gives the criterion

    sum_n F_W^(-1)(1/h(n)) < infinity,
    h(0) = m0,  h(n+1) = F_Z^(-1)(1 - 1/h(n)).

The displayed recurrence on page 7 says n >= 1 while giving only h(0). This is a source indexing blemish. Page 12 recalls the recurrence without that restriction. This report uses the explicit, well-defined recursion for n >= 0; a finite index shift would not affect summability.

## 1. Retention and conditioning

Fix H and set p = exp(-H), so 0 < p < 1. Let R_v be the event that vertex v has no recovery mark in [0,H]. The R_v are iid Bernoulli(p), independent of the tree and all arrows. Condition only on R_root, not on retained-tree survival.

The root-connected retained subtree T^R is an ordinary Galton-Watson tree with offspring law

    eta | xi ~ Binomial(xi,p).

Indeed, for any retained vertex, the retained status of its original children is independent of its offspring count; the children's own offspring and descendant marks are independent of those statuses and all earlier exploration. Compression of surviving child labels gives the usual iid Galton-Watson recursion. Conditioning on the root's retention leaves all those independent variables unchanged.

eta is almost surely finite. Its zero mass is positive, for example

    P(eta=0) >= P(xi=1)(1-p)
             = (1 - 2^(-1/4))(1-p) > 0.

Thus P(eta=1) < 1. Its mean is infinite by nonnegative conditional expectation:

    E eta = p E xi = infinity.

For a self-contained survival reduction, choose finite K with E[min(eta,K)] > 1. Put Z=min(eta,K) and g(s)=E[s^Z]. Then g(0)>0, g(1)=1, and g'(1)>1, so g(s)<s for s<1 sufficiently near 1. The intermediate value theorem gives a fixed point q in (0,1). Iterating g from 0 gives the generation-n extinction probabilities and an increasing limit no greater than q, so the truncated process survives with positive probability. Couple it below eta at every vertex. Consequently T^R has survival probability q_surv > 0.

**Conditioning warning:** offspring and descendant regeneration here refer to the unconditioned eta-GW law obtained after conditioning on R_root. They must not be asserted unchanged after conditioning T^R on survival.

## 2. Thinned tail bound and plumpness

For integer m >= 1 set k = ceil(2m/p). On {xi >= k}, retain the first k original children. Their retained count B has Binomial(k,p) law and is independent of {xi >= k}. Therefore

    P(eta >= m) >= P(xi >= k) P(B >= m).

Since k <= 3m/p and mu = kp >= 2m, the usual Bernoulli Chernoff bound gives

    P(B < m) <= P(B <= mu/2) <= exp(-mu/8) <= exp(-m/4).

Consequently

    P(eta >= m)
      >= (p/3)^(1/4) m^(-1/4) (1 - exp(-m/4)).                 (2.1)

In particular, there is an integer M such that

    P(eta >= m) >= m^(-1/3),  all integer m >= M.             (2.2)

An explicit sufficient choice is M = ceil(110592 p^(-3)): the exponential factor in (2.1) is then at least 1/2 and

    ((p/3)^(1/4)/2) m^(1/12) >= 1.

For any sufficiently large real x let j = ceil(x^2), so j <= 2x^2. Equation (2.2) implies

    P(eta >= x^2) = P(eta >= j)
      >= j^(-1/3) >= 2^(-1/3) x^(-2/3) > 1/x

as soon as x > 2 and j >= M. This supplies ADGO plumpness with epsilon = 1, with strict slack that also removes discrete quantile ambiguities.

## 3. ADGO quantile criterion, with safe rounding

Write Q_eta(u) = inf{z : P(eta <= z) >= u}. Choose an integer h0 >= max(M,3), and define

    h(0)=h0,  h(n+1)=Q_eta(1-1/h(n)),  n >= 0.

Every h(n) is finite because eta is finite almost surely and 1-1/h(n) < 1. For h=h(n) and j=ceil(h^2), the strict bound above gives

    P(eta <= j-1) = 1 - P(eta >= j) < 1 - 1/h.

Hence

    h(n+1) >= j >= h(n)^2,
    h(n) >= h0^(2^n).                                      (3.1)

This proves the needed growth directly rather than trusting a discrete tail/quantile equivalence at an equality boundary.

For W~Exponential(lambda),

    Q_W(1/h) = -log(1-1/h)/lambda <= 2/(lambda h),  h >= 2.

Equation (3.1) yields the explicit convergent upper bound

    sum_n Q_W(1/h(n))
      <= (2/lambda) sum_n h0^(-2^n)
      <= 2/[lambda(h0-1)] < infinity.

ADGO Theorem 1.3 and its survival-qualified Equivalence theorem therefore give a finite-weight infinite ray almost surely conditional on survival of T^R. Since q_surv > 0, explosion has positive probability under the unconditioned eta-GW law.

## 4. Every positive horizon: regenerative ray-tail lemma

Here T^R has the unconditioned eta-GW law. Give it independent W edge weights. Let V be the infimum of total weights over all infinite rays, with infimum infinity if there is no infinite ray; nonexplosive infinite trees also have V=infinity. This quantity is measurable: on a locally finite nonnegative-weight tree it equals the increasing limit of the minimum root-to-generation-n weight. The finite-level characterization and the ray characterization agree by the finitely branching tree compactness/Konig argument.

**Lemma.** If a Galton-Watson tree with iid nonnegative edge weights has positive probability of a finite-weight ray, then P(V<a)>0 for every a>0.

**Proof.** Realize the tree by independent offspring and edge-weight arrays on the countable set of finite Ulam words. For every word u, let A_u be its existence event, and let V_u be the corresponding relative subtree explosion time from the independent descendant arrays. A_u depends only on ancestral offspring. Therefore V_u has the same law as V and is independent of A_u.

If P(V<a)=0, then P(A_u and V_u<a)=0 for every u. Countability implies that almost surely no existing descendant has a ray of relative weight less than a. But on the positive-probability event of a finite-weight root ray, the tails of that convergent nonnegative series tend to zero. At some existing descendant u its remaining ray has weight less than a, so V_u<a. Contradiction. This proves the lemma.

Apply it with a=H to the fixed offspring law eta=Binomial(xi,exp(-H)). This does not change H or p while applying the lemma. It gives

    r_H,lambda := P(V<H | R_root) > 0.                      (4.1)

The notation on the left is the root-retained law, not the survival-conditioned law. Passing to survival conditioning before invoking descendant regeneration would invalidate that part of the proof.

## 5. Arrow coupling and iid exponential edge weights

Condition on the tree and all recovery marks. Root retention is among this conditioning. For each downward retained edge e=(u,v), let N_e be its independent rate-lambda arrow process. Set t_root=0, and recursively by finite generations set

    t_v = first point of N_(u,v) strictly after t_u,
    W_(u,v) = t_v - t_u.

Every generation is finite almost surely because all original offspring counts are finite. Every finite-depth t_v is finite almost surely. Crucially, t_u is a function of ancestor edge processes only; the entire outgoing process N_(u,v) is independent of t_u and has not been exposed in the recursion.

Given every previously exposed ancestor edge process and the tree/recoveries, outgoing edge processes are independent. For every nonnegative deterministic value s of t_u,

    P(first point of N_e after s - s > x) = exp(-lambda x).

Here x>=0. This conditional law does not depend on s. Thus all outgoing waits in a generation are conditionally iid Exponential(lambda), independent of the previous generations. Induction gives iid exponential W over the entire retained tree, independent of the conditioned tree and recoveries. No strong-Markov assertion at an anticipative time is used: independence from the whole outgoing process suffices. The definition uses the constructed downward arrival t_u, not a full contact-process infection time that might depend on the same edge process.

## 6. Finite paths, simultaneity, and unconditional probability

On {V<H}, there is a ray rho=v0,v1,... with total W-weight <H. Its finite partial sums are t_vn. They are strictly increasing almost surely and all less than H. Every v_i is retained, so it has no recovery mark anywhere in [0,H]. For each n, the n downward arrows at times t_v1,...,t_vn, followed by the vertical segment from t_vn to H, form a legal finite infection path from (rho,0) to (v_n,H).

This path lies inside the finite ball B_n. Thus v_n is infected at H already in the process on B_n. In fact B_n's process has all n+1 vertices v0,...,vn infected at H. The coupled ball processes increase with n; each admitted finite path lies in some finite ball. Their union is exactly the prescribed X_H. Hence

    V<H and R_root  =>  |X_H|=infinity.

No traversal past the ray's limit point and no infinite-jump infection path are required. All vertices are certified at the same H, rather than merely at their individual arrival times.

Finally, root recovery marks are independent of T and all other marks. Multiplying back the root-retention probability gives

    P_annealed(|X_H|=infinity)
      >= exp(-H) r_H,lambda > 0.                            (6.1)

This is a conclusion for the original, unconditional graphical-process law.

## Adversarial checks and boundaries

| Possible failure | Check / correction | Status |
| --- | --- | --- |
| Root conditioning alters graph law | Recovery at root is independent of T; descendant offspring remain eta iid | Pass |
| Retained tree might die out | It does have positive extinction probability; infinite mean gives positive survival, and ADGO is invoked only conditional on survival | Pass |
| Offspring are not locally finite | xi and eta are finite almost surely; every finite graph ball is finite | Pass |
| Tail/quantile equality could round incorrectly | Use ceil(h^2) and strict P(eta>=ceil(h^2))>1/h | Pass |
| ADGO h(1) not initialized in source display | State recursion for n>=0; page 12 and finite index invariance support intended use | Corrected source detail |
| Explosion at some finite time does not imply explosion before any H | Countable regenerative ray-tail lemma on unconditioned eta-GW law | Pass |
| Conditioning on survival destroys regeneration | Drop survival conditioning after deriving positive-probability explosion; use unconditioned law in lemma | Necessary wording safeguard |
| Arrow waits are chosen adaptively | Parent arrival uses only ancestor edges, never the outgoing edge being sampled | Pass |
| Chosen ray might bias the waits | Establish iid joint law before selecting a ray; no claim of independence after ray selection | Pass |
| Infinite-path legality | Each witness at H has a finite prefix, and lies in a finite ball | Pass |
| Arrival times differ, so infection need not be simultaneous | Retention eliminates recoveries on every witness vertex through the common H | Pass |
| Only conditional probability was proved | Multiply by exp(-H)>0 to return to original law | Pass |
| H=0 or lambda=0 | Excluded; root-only X_0 is finite and no-spread lambda=0 cannot yield the result | Boundary checked |
| Very small H or lambda | Bounds remain positive but may be extremely small; no uniform positivity bound claimed | Pass |
| Arbitrary graph / alternative process conventions | Claim is annealed for this GW law and minimal finite-path process only | Scope fixed |
| Literature attribution | ADGO supplies general weighted-tree theorem; contact-process bridge is a derived corollary, not an identified explicit theorem in that paper | Scope fixed |

Strongest verified result: equation (6.1) for every fixed H>0 and lambda>0. Remaining mathematical gap within this precise claim: none identified. Remaining literature gap: whether any prior source explicitly states this contact-process corollary was not established by this verification and cannot be inferred from ADGO's general theorem alone.
