# Universal endpoint-barrier proof

Let (g_i)_{i>=1} be a countable family of homeomorphisms of R, with either orientation allowed. There is one increasing homeomorphism h:R->R such that, writing epsilon_i for the orientation of g_i,

    |h g_i h^(-1)(t) - epsilon_i t| <= 2i+1                 (all real t).

In particular, for all p,q,

    ||h g_i h^(-1)(p)-h g_i h^(-1)(q)|-|p-q|| <= 4i+2.

These constants are positive and finite, depend on the enumerated element, and need not be sharp.

## Construction and the one common coordinate

Put l_0=r_0=0 and I_0={0}. Given I_(n-1), its images under the finitely many g_j and g_j^(-1), j<=n, are compact intervals: the endpoint values determine each entire image even when the map reverses orientation. Choose finite l_n,r_n so that their open interval contains [-n,n], I_(n-1), and every such image interval. For example take one less than the minimum, and one more than the maximum, of these finitely many endpoint values and -n,n,l_(n-1),r_(n-1). Thus

    l_n<l_(n-1), r_n>r_(n-1), l_n<-n, r_n>n;
    g_j(I_(n-1)) union g_j^(-1)(I_(n-1)) subset int(I_n), j<=n.   (A)

No infinite maximum, locally uniform estimate on infinitely many maps, or summability choice occurs at one stage. Each stage uses only finitely many real numbers. The recursion is defined for every integer n.

Define h(0)=0, h(l_n)=-n, h(r_n)=n, with positive-slope affine interpolation on [l_1,0], [0,r_1], and consecutive left/right intervals. There are no finite accumulation points of knots because l_n->-infinity and r_n->infinity. These intervals cover R; their definitions agree at endpoints. Hence h is continuous and strictly increasing, its values exhaust both ends, and it is onto R with continuous inverse. The whole enumeration determines h once, before any i is fixed. No generator, point, or pair receives a separate coordinate.

## Four endpoint inequalities

Fix i and n>=i. Applying (A) at n+1 bounds both g_i(l_n) and g_i(r_n) strictly between l_(n+1) and r_(n+1). Applying its inverse part at n puts g_i^(-1)(l_(n-1)) and g_i^(-1)(r_(n-1)) strictly between l_n and r_n.

If epsilon_i=+1, monotonicity gives

    l_(n+1) < g_i(l_n) < l_(n-1),
    r_(n-1) < g_i(r_n) < r_(n+1).                         (B+)

If epsilon_i=-1, decreasing monotonicity gives

    r_(n-1) < g_i(l_n) < r_(n+1),
    l_(n+1) < g_i(r_n) < l_(n-1).                         (B-)

For n=i=1, l_0=r_0=0 is allowed; the inverse containment places the root g_i^(-1)(0) strictly inside I_1, so the same strict inequalities and correct tail signs hold. No exceptional zero case is omitted.

For t in [n,n+1], x=h^(-1)(t) lies in [r_n,r_(n+1)]. Applying (B) to n and n+1 and monotonicity bounds h(g_i(x)) between n-1 and n+2 in the increasing case, and between -n-2 and -n+1 in the decreasing case. Consequently |h(g_i(x))-epsilon_i t|<=2. For t in [-n-1,-n], use x in [l_(n+1),l_n] and the other endpoint inequalities to obtain the same bound. Every |t|>=i belongs to one of these annuli, including their endpoints.

If |t|<=i, then x is in I_i. By (A) at i+1, g_i(x) lies in I_(i+1), so |h(g_i(x))|<=i+1. Hence |h(g_i(x))-epsilon_i t|<=2i+1 on the whole core. Combining core and tails proves the claimed global bound.

Finally, write F_i=h g_i h^(-1). The reverse triangle inequality gives

    ||F_i(p)-F_i(q)|-|p-q||
      <= |(F_i(p)-F_i(q))-epsilon_i(p-q)|
      <= |F_i(p)-epsilon_i p|+|F_i(q)-epsilon_i q|
      <= 4i+2.

## Application and exact boundaries

Enumerate the image of any countable group action on R. Inverses exist because the maps are homeomorphisms; faithfulness is unnecessary. A finite family can be repeated to form the enumeration. Assign C(alpha)=4i+2 using any fixed index i of its image. The conjugacy automatically preserves composition and inverses. A second-countable 3-manifold has countable fundamental group, for example via a countable triangulation and finite edge loops. Thus the literal leaf-line condition in Calegari Q8.2 follows.

The proof is about arbitrary topological coordinates and the displayed per-element inequality. It does not supply a group-uniform constant, a coarse relation to the old metric, ambient leaf-distance bounds, or simultaneous Lipschitz regularity. A cyclic dilation fixing 0 cannot admit a group-uniform distance error under any conjugacy: for x!=0 its positive iterates go to an end while the fixed point stays fixed, so their conjugated distances diverge. For the uncountable family of all line homeomorphisms, a common coordinate is impossible: conjugation preserves that full family, which still contains t->2t with unbounded additive distortion. These are real quantifier boundaries.

The primary 2002 toroidal remark conflicts with the unrestricted topological reading. It does not explicitly state a replacement geometric condition, and none is inferred here. The independently checked deterministic theorem establishes the literal formula while preserving this unresolved historical-interpretation limitation. No novelty or human/formal verification is claimed.
