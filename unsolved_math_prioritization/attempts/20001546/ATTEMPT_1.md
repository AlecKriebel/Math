# Attempt 1: test the geometric central-quotient graph

Recorded 2026-10-03 UTC. Outcome: an explicit obstruction to the first natural
proper cocompact candidate; the original question is unresolved. Budget: 1/5.

## Construction and goal

Let A be the group in SOURCE_GATE.md. Choose the cyclic order a,b,c. Put

    d=b^-1 a b, e=c^-1 b c, f=a^-1 c a,
    p=ab, q=bc, r=ca,
    S={a,b,c,d,e,f,p,q,r} union their inverses.

The three rank-two dual intervals are {1,a,b,d,p}, {1,b,c,e,q},
{1,c,a,f,r}. Their union gives the cyclic-type structure in Haettel–Huang,
Section 5.2. By their Corollary 4.5, the Bestvina complex obtained from their
Garside group A x Z is the flag completion of Q=Cay(A,S). The A-action on Q
is free, proper, and cocompact. If Q were Helly this would answer AIM 4.2.

## Exact counterconfiguration

The three radius-one balls centered at 1, a^2, and p^2 intersect pairwise but
have empty total intersection. More strongly,

    B_Q(1,1) intersect B_Q(a^2,1) = {a},
    B_Q(1,1) intersect B_Q(p^2,1) = {p}.

The first two pairwise intersections are witnessed by a and p respectively.
For the remaining pair, a^2 b is a common neighbor, since

    p^2 = abab = aaba = (a^2 b)a.

The two singleton intersections are disjoint because a != p; for instance
abelianization sends a to 1 and p to 2. Therefore Q is not Helly.

## Complete finite exclusion certificate

The singleton assertions concern only 19 candidates: 1 and S. To rule out
unlisted common neighbors, it is enough to map A to ANY concrete group and
check that the images of v^-1 n do not lie in the images of {1} union S for
each candidate n. Faithfulness is not needed: unequal images imply unequal
group elements. The positive candidates a and p are established in A itself.

The supplied Python script uses automorphisms of the free group on four
letters. Define sigma_i by

    x_i -> x_i x_(i+1) x_i^-1,
    x_(i+1) -> x_i,

fixing the other letters. Its inverse sends x_i to x_(i+1) and x_(i+1) to
x_(i+1)^-1 x_i x_(i+1). Use

    a -> sigma_2,
    b -> sigma_3,
    c -> sigma_1^2 sigma_2 sigma_3 sigma_2^-1 sigma_1^-2.

Direct free reduction verifies all three defining braid relations, so this is
a homomorphism from A. The script verifies these relations, all inverse pairs,
all nine dual-interval products, and the two full finite neighbor tests. It
also verifies that the 19 images are distinct. Thus it is a certificate of
non-Hellyness, not a heuristic word-problem test. The initial exploratory ball
of radius 2 has 211 distinct image values; its exact size in A is not needed.

## What this does and does not establish

This rules out the exact geometric weakly modular graph provided by the
finite Garside central quotient. It does not rule out its Helly hull being at
bounded distance, a different generating set, a different graph, or an action
with several vertex orbits. A bounded radius-one defect cannot imply failure
of coarse Hellyness. Attempt 2 will test whether a scalable obstruction or a
uniform enlargement bound can be extracted from this configuration.
