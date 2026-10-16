# Turn 5: the exact induced-C4 profile for rank-one latent-product kernels

**Original source problem unsolved; fifth and final substantive author turn.** This is a separate approach family from cotree decompositions. It completely optimizes the induced-C4 profile for kernels W(s,t)=f(s)f(t), 0≤f≤1, and shows that this whole family is strictly below the source's explicit multipartite construction at every nontrivial density. It is not an optimization over arbitrary graphons. No historical novelty is asserted for the moment method or its scoped consequences.

## 1. Exact factorization of the induced density

Let f:[0,1]→[0,1] be measurable, let W(s,t)=f(s)f(t), and put

    m_j=∫f(t)^j dt,      p=p(W)=m_1².

As in previous turns, c(W) is the probability of an **unlabeled induced** C4 on four independently sampled vertices, with conditionally independent edge states. There are three disjoint labeled C4 edge-pattern events. For one fixed cycle, the product of its four edge factors is ∏_{i=1}^4 f_i². The two missing diagonals contribute (1−f_1f_3)(1−f_2f_4). The independent diagonal pairs then factor the expectation, giving

    c(W)=3(m_2²−m_3²)².                                (1)

This includes all six edge/nonedge requirements. Replacing induced density by the ordinary C4 homomorphism density would incorrectly omit m_3.

## 2. Theorem: exact maximum at each prescribed edge density

For the rank-one family just defined, the maximum is

    R(p) = { 3p²/16,             0≤p≤1/2;
           { 3p⁴(1−p)²,         1/2≤p≤1.              (2)

For 0<p<1/2 the maximizer, up to measure-preserving rearrangement and null sets, has

    f=1/√2 on a set of measure √(2p), and f=0 elsewhere.

For 1/2≤p≤1 the maximizer has f=√p almost everywhere, so W is the constant graphon p. The p=0 case is f=0 almost everywhere. The two descriptions agree at p=1/2.

**Proof.** If p=0, then f=0 almost everywhere, and there is nothing to prove. For p>0, Jensen and 0≤f≤1 give

    m_2≥m_1²=p,       m_2≤m_1=√p.

Define z=m_2²/p, so

    p≤z≤1.                                             (3)

Cauchy–Schwarz applied to f^(3/2) and f^(1/2) yields

    m_3 m_1≥m_2²,

and therefore

    0≤m_2²−m_3²
      ≤m_2²−m_2⁴/p
      =p z(1−z).                                       (4)

The first inequality follows independently from m_3≤m_2. Squaring the nonnegative quantities in (4) and using (1),

    c(W)≤3p²[z(1−z)]².

If p≤1/2, the largest value of z(1−z) on [p,1] is1/4, attained at z=1/2. This gives3p²/16. The stated two-valued f has m_1=√p, m_2=√(p/2), m_3=√p/2, and attains the bound.

If p≥1/2, z(1−z) is decreasing on [p,1], so its largest value is p(1−p), yielding3p⁴(1−p)². The constant f=√p attains it.

For completeness, equality below1/2 requires z=1/2 and equality in Cauchy–Schwarz. The latter means f is constant on its positive support. Writing that positive value as d gives z=d², hence d=1/√2 and support mass√(2p). Above1/2, equality requires z=p; that means m_2=m_1² and thus f is constant almost everywhere. At p=1/2 the same conclusion holds because the maximizing z is still p; at p=1 the mean bound f≤1 forces f=1. ∎

The piecewise formula is continuous at1/2, where both branches equal3/64. It classifies this model exactly; it does not identify a candidate for the full source maximum.

### The entire rank-one vertical feasible interval

Every c between0 andR(p) is attained within this family. For p>0, choose d∈[√p,1], let f=d on a set of measure√p/d and zero elsewhere. Then the edge density is p and

    c=3p² d⁴(1−d²)².                                  (5)

For p≤1/2, let d range from1/√2 to1; for p≥1/2, let it range from√p to1. Continuity makes (5) range from R(p) down to0. For p=0 the interval is the singleton0. Thus the rank-one feasible region at density p is exactly [0,R(p)].

These limiting densities are realized by ordinary graph sequences: the low-density optimizer is a random graph with edge probability1/2 on an active fraction√(2p) of vertices and isolated vertices elsewhere; the high-density optimizer is G(n,p). For each fixed finite motif, pairs of sampled vertex sets with no common vertex have independent indicators, so their normalized count variance is O(1/n). Edge and induced-C4 densities therefore approach the stated values in probability, and one may select deterministic realizations approaching them. No exact finite-n optimizer or rate is asserted.

## 3. Strict separation from the known source construction

Let F(p) be the explicit multipartite construction value from turn1. Regardless of whether the full source conjecture is true, F(p) is **achievable**, so a rank-one kernel cannot be globally optimal whenever R(p)<F(p).

In fact R(p)<F(p) for every0<p<1. Below or at1/2 this follows exactly from

    F(p)−R(p)=(21/16)p²>0.                              (6)

For the above-half range, put q=1−p. Turn4 gives F(p)≥3q²/2. Hence when1/2≤p≤3/4,

    F(p)−R(p)≥(141/256)q²>0,                           (7)

because p⁴≤81/256.

For3/4≤p<1, use the minimizing vector for L(q). With r=floor(1/q), its largest mass a satisfies

    a≤1/r≤q/p,

since r≥1/q−1=p/q. Therefore

    L(q)≤a²q≤q³/p²,
    F(p)≥3q²(1−q/p²).

Subtracting R(p)=3p⁴q² gives

    F(p)−R(p)
       ≥[3q³/p²] [p²(1+p+p²+p³)−1]
       ≥(1653/1024)q³>0.                               (8)

For the last step, the bracket is increasing in p and at3/4 equals551/1024; also1/p²≥1. Equations(7)–(8) are conservative explicit gaps, not sharp differences between the profiles. Both apply at3/4, and the endpoint p=1 has F=R=0.

Thus the entire latent-product family is ruled out as a source extremizer at every interior edge density, including all the above-half densities asked about in the conjecture. This conclusion only uses the existence of the source construction; it does not assume its unproved global optimality.

As another exact consequence of (2), the largest induced-C4 density anywhere in the rank-one family is16/243, attained at p=2/3 by the constant graphon2/3. The low-density branch increases up to1/2, and the derivative of the upper branch is6p³(1−p)(2−3p), giving this maximum. This is a restricted-family value, not the unrestricted C4 inducibility3/8.

## 4. Final disposition and remaining gap

Five substantive turns are now complete. The packet establishes the all-weight multipartite optimization, complete-join replacement and triangle-minimizer consequence, a carefully qualified small-amplitude local theorem, the full cograph profile, and the exact rank-one profile with a strict source-construction gap. It also preserves non-multipartite equality examples and the failure of an L1 first-variation shortcut.

No argument bounds every non-cograph, non-rank-one graphon with positive triangle excess by F. There is no verified full proof or counterexample to Liu–Mubayi–Reiher's profile conjecture. The original is **unsolved5/5**. Author search stops here; further work on this packet is limited to independent review, any necessary corrections and authorized publication.

## Verification

`verify_turn5.py` uses exact fractions. It checks the factorized formula against independent four-vertex kernel integration, the moment inequalities on finite-support rational examples, both optimizer branches through rational kernels, the explicit gap constants and all-parameter derivative algebra controls. It uses no Monte Carlo or floating-point evidence. The universal moment proof and equality conditions above establish the theorem.

The original source and construction remain those in `SOURCE_GATE.md`: https://ems.press/journals/owr/articles/10252930 and https://arxiv.org/abs/2106.16203v2 . The latent-product family is explicitly defined here and is only a restricted comparison model.
