# Independent equal-rate whisker adversarial report

Audit date: 2026-10-21 UTC. Problem 30005455, alias OWR-12697708-008, PR1131.
Pinned head: `bacae693a1f2a33c89565b0bd716620885831289`; base: `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`.

## Bounded finding

I found no defect in the equal-rate theorem for every alpha >= 17/4 in the actual head proof. The proof excludes both strictly stable and critical non-whisker limiting equilibria. All five exponent intervals, the fractional-power caps, the unbounded tail, and the closed 17/4 endpoint survive exact independent checks. The local matching argument itself excludes cycles, so this independent whisker reconstruction does not rely on the manuscript's new forest theorem; the published HHK2023 stochastic bridge remains imported. It makes no novelty, priority, exhaustive-literature, publication-readiness, or external-review certification.

There is a **target-classification repair**: the literal OWR Open Problem 2 requests an improvement to the old >25 bound. A valid >=17/4 theorem supplies that improvement. The later suggestion that >4/3 might be sharp is a stronger unresolved target; it must not be silently substituted for the literal improvement request when assigning OPEN status. The same distinction applies to the literal forest improvement request, whose mathematical proof is outside this family's detailed remit.

There is also an **initial-count scope repair**: the manuscript and distributed status declare unit initial counts, whereas the original presentation gives initial counts without imposing that normalization. The almost-sure upper-bound conclusions extend to every positive integer initial count vector by the finite-path argument below. That extension should be stated explicitly. It does not, by itself, transfer positive-probability attainment of a specified equilibrium in the reverse direction.

## Inputs and primary-source checks

The complete actual PROOF and MATHEMATICAL_AUDIT and all six accompanying scope/source/inventory files were read from the pinned Git object, without running any supplied program. All eight byte identities are in EXACT_CERTIFICATE.json. In particular the actual proof has 16,964 bytes and SHA-256 `791ec6c1f849840785afd8ce15e4460b396e108bc2b203d93993cfb0a6103340`; the historical 16,977-byte manuscript is a different identified edition.

Fresh primary PDF copies, extraction, retrieval records and selected rendered pages remain private. SOURCES.json binds their public URLs, exact bytes and hashes without including third-party source text. I read OWR printed pp.653-655, essential HK2017 model/Condition G/definitions/Theorems 2-3/champion and least-weight passages, and HHK2023 model/Conditions 1-3/Theorem 1/Proposition 1 passages; the decisive pages were also inspected as rendered images.

OWR2023 places both requested improvements in the finite-graph discussion. Equal rates apply to the whisker request; unequal rates are allowed for the forest request. Its subsequent sharp-threshold suggestion is distinguishable from the two requests. The original initial-count notation is not restricted there to all ones. [OWR source, printed 653-655](https://ems.press/content/serial-article-files/47008).

HK2017 uses uniform vertex selection for its whisker theorem, defines whiskers by tree diameter at most three, supplies the previous universal bound, credits the champion/least-weight mechanism, and explicitly warns through a nonuniform-rate path example that general rates can invalidate whisker conclusions. Its initial model permits positive counts and then normalizes them to one. [HK2017 author manuscript](https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf).

HHK2023 Theorem 1, printed 3016/PDF5, applies to finite graphs, alpha>1 and positive rates, and gives a.s. convergence to stable or critical equilibria; its attainment clause is for strict stability. The stated process starts with unit counts. Proposition 1, printed 3021/PDF10, requires bounded positive rates and bounded degrees, both automatic here, and identifies infinite reinforcement with positive asymptotic growth. [HHK2023 published PDF](https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf).

No infinite-graph conditional-law theorem is needed. No outside individual was contacted, and no other fresh review family was read.

## Independent local stability reduction

Normalize a common positive rate to one by changing time. On a positive support edge e=uv, put q=a_e^alpha/S_u and r=a_e^alpha/S_v. Then q+r=a_e, with 0<q,r<=1, so a_e<=2. Directly differentiating the vector field at equilibrium gives

    J_ee = alpha - 1 - alpha*(q^2+r^2)/a_e.

On the positive support the vector field is diag(a) grad L, where

    L = -sum_e a_e + (1/alpha) sum_v log S_v.

Consequently J is similar to the symmetric matrix diag(sqrt(a)) Hess(L) diag(sqrt(a)). If it has no positive eigenvalue, that symmetric matrix is negative semidefinite and every diagonal entry, including J_ee, is nonpositive. Therefore every such edge satisfies

    (q^2+r^2)/(q+r) >= 1 - 1/alpha.                    (1)

This is a necessary condition, not a sufficient test for stability. The left side is a weighted mean of q and r, so at least one endpoint probability is at least 1-1/alpha (the champion consequence). Zero eigenvalues do not weaken (1).

At a stochastic limit every positive-rate vertex has a positive incident edge: its incident count sum dominates its firing count, and division by time and the Poisson law of large numbers give an incident limiting-weight sum at least its rate. All denominators thus stay positive. For alpha>1 a zero edge has derivative -1 in its own row, while all derivatives connecting zero and positive coordinates vanish, because the derivative of x^alpha at zero from the nonnegative side is zero. An explicit C1 extension using (max(x,0))^alpha gives the same derivative. Positive support perturbations are two-sided admissible locally, so a positive support eigenvalue excludes the full boundary equilibrium. No differentiability at an all-zero vertex is invoked.

Take an edge of least positive weight in one finite support component. If neither endpoint is a support leaf, each endpoint has a competitor no lighter than it. Then q,r<=1/2, violating (1) when alpha>2. It therefore has a leaf endpoint, contributing one unit of rate, and its weight is at least one. Every edge of that component has weight at least one. In fact the least-edge weight is strictly above one, but the weak bound suffices.

For any edge with no leaf endpoint and weight a in [1,3/2], each endpoint has a distinct positive competitor of weight >=1. Hence

    q,r <= s_alpha(a) := a^alpha/(1+a^alpha),  q+r=a.

The feasible q interval is [a-s,s], where s=s_alpha(a)>=a/2. The convex function q^2+(a-q)^2 reaches its maximum at an interval endpoint. Thus

    (q^2+r^2)/a <= f(a,s) := (s^2+(a-s)^2)/a.          (2)

For s>=a/2, partial_s f=2(2s/a-1)>=0. Since a>=1, s_alpha(a) is nondecreasing in alpha. These facts justify replacing alpha by an upper interval endpoint B in (2); no feasible split is assumed outside that constraint set.

## Complete finite interval certificate

For 3<=B<=7 and 1<=a<=3/2, write z=s_B(a)/a. Both bounds

    1/2 <= z <= 2/3                                  (3)

have elementary proofs. The first is equivalent to a^(B-1)(2-a)>=1. Here a^(B-1)>=a^2, and

    a^2(2-a)-1 = (a-1)(1+a-a^2) >=0,

since 1+a-a^2 decreases from 1 to 1/4 on [1,3/2]. For the second, s_B<=s_7, and z<=2/3 follows from

    R(a)=2a^7-3a^6+2 >0.

Indeed R'(a)=2a^5(7a-9), so its minimum on a>=0 is at 9/7, with exact value 52763/823543>0.

Direct differentiation, with s=s_B(a), gives

    d_a f(a,s_B(a)) = 1-2z^2 + 2(2z-1)s_B'(a) >= 1/9,

using s_B'(a)>0 and (3). Thus the maximum on the weight interval occurs at a=3/2. For A<=alpha<=B,

    (q^2+r^2)/a <= f(3/2,s_B(3/2)).

Let T>=(3/2)^B and S=T/(1+T). All the following S are >=3/4, so the monotonicity needed to replace s_B(3/2) by S is valid. The exact rational table is:

| A | B | T | S | f(3/2,S) | (1-1/A)-f |
|---|---|---|---|---|---|
|17/4|13/3|29/5|29/34|1325/1734|1/1734|
|13/3|9/2|25/4|25/29|3869/5046|163/65598|
|9/2|5|243/32|243/275|117039/151250|5399/1361250|
|5|6|729/64|729/793|991335/1257698|74117/6288490|
|6|7|2187/128|2187/2315|8580639/10718450|527104/16077675|

The first two T bounds follow, without floating-point powers, from

    (29/5)^3-(3/2)^13 = 504313/1024000 >0,
    (25/4)^2-(3/2)^9  = 317/512 >0.

The other T values are exact integer powers. All margins are strictly positive. Since 1-1/A<=1-1/alpha, every row contradicts (1). Consecutive endpoints agree exactly; all intervals are closed and their union is [17/4,7]. In particular the first positive margin proves the closed 17/4 endpoint, without a limiting argument.

## Complete analytic tail

For alpha>=7 and a=1+r0 in [1,3/2], q,r<=1 and q+r=a imply q^2+r^2<=1+r0^2 by the same convex endpoint argument on [r0,1]. Combining with (1) yields

    h(r0):=alpha*r0^2-(alpha-1)*r0+1 >=0.             (4)

Now h(0)>0 and h(1/2)=(6-alpha)/4<0. Because h is an upward quadratic, exactly one root r_minus lies in (0,1/2), its second root exceeds 1/2, and (4) forces r0<=r_minus.

Put C=3-sqrt(2). Then 1<C<8/5, C/alpha<1/2, and C^2+C=7(C-1). Substitution gives

    h(C/alpha)=-(C-1)*(1-7/alpha)<=0.

It follows that r_minus<=C/alpha and r0<=C/alpha. The inequality log(1+r0)<=r0 now proves a^alpha<=exp(C). To bound this last constant rigorously, sqrt(2)>7/5 gives C<8/5. The exponential series through degree four is 9067/1875. Its tail starting at degree five has initial term (8/5)^5/5!, and every subsequent term ratio is at most (8/5)/6=4/15. Thus

    exp(C) < exp(8/5)
           <= 9067/1875+4096/34375
            = 510973/103125 < 6 <= alpha-1.

Therefore s_alpha(a)<(alpha-1)/alpha. Both q and r would be strictly below the champion bound from (1), a contradiction. This argument includes alpha=7 and covers every larger real alpha; it is not a sampled numerical assertion.

## Diameter conclusion and scope controls

Every edge having no leaf endpoint must consequently have weight >3/2. At a vertex incident to two such edges, each edge's probability at that vertex is greater than 1/2: its other endpoint contributes at most one to its weight. Their sum would exceed one, impossible. Such edges therefore form a matching.

The matching property also rules out every cycle directly: every edge of a cycle has two non-leaf endpoints, and two consecutive cycle edges are adjacent. Thus the support is a forest without invoking the manuscript's new cycle theorem. If one of its trees had diameter at least four, take a simple four-edge path v0-v1-v2-v3-v4. Its two middle edges share v2; neither has a leaf endpoint, since v1,v2,v3 each have two path neighbors. This contradicts the matching condition. Thus every component has diameter <=3.

The unit rates are essential to the bounds a=q+r<=2 and a>=1 and to the probability conclusion at a common vertex. With unequal rates, the equilibrium identity becomes a=lambda_u*q+lambda_v*r. The manuscript's unequal-rate diameter-four path at alpha=2 is therefore outside this theorem and supplies no counterexample to it. No claim about arbitrary-rate whiskers, loops, infinite graphs, or alpha=4/3 is justified by this proof. The declared finite simple loopless model matches the ordinary simple-graph reading of the problem; the original passage does not explicitly settle alternative loop or multigraph conventions. A one-vertex loop would defeat a forest assertion, so broadening that convention silently is invalid.

## Positive integer initial counts: one-sided extension

Let m=(m_e) have positive integer entries on a finite graph, and let M=sum_e(m_e-1). Starting from ones, prescribe any sequence of M edge reinforcements that raises edge e exactly m_e-1 times; at each step choose one fixed endpoint of that edge to fire. Every prescribed vertex/edge pair has strictly positive conditional probability: its firing probability is lambda_v/Lambda>0 and its chosen-edge probability is a positive finite weight divided by a positive finite sum. The event E that the first M pairs match this prescription has a positive product probability, and the count vector at the Mth jump is exactly m.

The strong Markov property at that jump, or the discrete jump-chain Markov property plus memoryless Poisson clocks, says that the shifted future conditional on E has exactly the process law started at m. Every event used in the upper-bound bridge is invariant under deletion of a finite initial segment and a finite time shift: convergence of counts/time, equilibrium location and absence of positive eigenvalues, positive-growth support, infinitely reinforced support, and the forest/whisker structure of that support. If any corresponding failure had positive probability from m, conditioning on E would give a positive probability of failure from ones, contradicting the published a.s. bridge and deterministic proof. This proves the upper-bound conclusions for all positive integer m.

This implication is one-sided. From positive attainment of a stable equilibrium at the unit state one cannot infer its positive attainment from every m by this conditioning argument. No such inference is used here. The allowed unit state alone suffices for the manuscript's universal-threshold obstruction. If the original notation is interpreted as arbitrary positive real weights rather than integer urn counts, finite-path conditioning does not establish that extension; zero initial weights or undefined all-zero denominators also need a separate convention. These are explicit scope qualifications, not counterexamples to the stated positive-integer conclusion.

## Reproducibility and exact remaining gap

The proof above is the universal certificate. VERIFY.py uses only the Python standard library and recomputes all finite rational quantities, polynomial identities, coverage, and the quadratic-field identity; it does not convert finite checks into a universal claim. Its negative controls reject bad power caps, changed margins, an interval gap, an omitted interval, a claimed lower endpoint outside the proof, a bad exponential tail constant, and a broadened rate scope. Explicit exceptions, rather than Python assert statements, enforce every check.

MANIFEST.json hashes the other public files, while the external PUBLIC_MANIFEST.sha256 pins the manifest. Verify a new copy with `python3 -B VERIFY.py --manifest-sha256 HASH`, substituting that pinned digest; repeat with `-O -B` and `-OO -B`. The review's actual runs execute fresh read-only copies and check byte preservation before/after. No original, captured, or sealed program was executed in place, and no checker is a substitute for the written calculus or imported theorem.

The stronger equal-rate whisker claim for 4/3<alpha<17/4 remains unproved here, as does stochastic behavior at 4/3. These are gaps to the sharpness suggestion; they do not undo the literal bound improvement. No mathematical repair to the >=17/4 argument was found. Needed presentation repairs are target classification and explicit positive-integer initial-count extension. No provider, PR, ledger, Git index, branch, or reference was mutated in this independent review.
