# An explicit failure of a uniform-height metric ansatz

UTC: 2026-10-24. Status: supporting construction, pending independent review. Discovery estimate toward full21.124 remains **3%**. This note disproves only a proposed sufficient-construction ansatz. It does **not** disprove virtual specialness of the example.

## Mechanism under test

For a tubular graph of groups equipped with a character χ nonzero on every edge group, write χ(x,y)=y at each Z² vertex. A positive definite flat form has the shape

    Q_v(x,y)=A_v(x-s_v y)^2+B_v y^2,  A_v,B_v>0.

Here B_v=D_v-C_v²/A_v if the matrix is [[A_v,C_v],[C_v,D_v]]. The squared norm of χ as a covector is1/B_v. A tempting extension of the one-vertex reflection construction is to choose compatible vertex metrics with a common B_v, making all height directions have the same scale before constructing a finite wall arrangement. The following explicit CAT(0) free-by-cyclic example shows that the common-B condition is not forced by the hypotheses, even after allowing arbitrary positive definite metrics on the original graph of groups.

## The eligible example

Take two vertex groups

    A=<a,t | [a,t]=1>,     B=<b,s | [b,s]=1>.

Join their vertices by six parallel unoriented edges. In the A vertex, the six primitive edge vectors are

    (7,1),(7,1),(8,1),(8,1),(13,1),(13,1).

In the B vertex, the corresponding primitive vectors are

    (1,1),(-1,1),(4,1),(-4,1),(11,1),(-11,1).

The character χ sends t,s to1 and a,b to0; choose stable letters of height0. It is compatible with every edge relation and is nonzero on every edge group.

Give the A torus the flat quadratic form Q_A(x,y)=x²+y² and the B torus Q_B(x,y)=x²+49y². Their corresponding edge curves have exactly equal metric lengths, because

    7²-1²=8²-4²=13²-11²=48.

All curves are primitive and hence embedded locally geodesic circles. Join corresponding equal-length curves by flat metric cylinders. The universal tree of vertex planes and strips is CAT(0): each gluing line is a closed convex subspace, and the standard tree-of-CAT(0)-spaces gluing theorem applies. The finite quotient is compact and the action is proper and cocompact. Thus this is a CAT(0) tubular group.

The kernel of χ acts on the Bass–Serre tree with two vertex-orbits, each having vertex stabilizer Z, and six edge-orbits with trivial edge stabilizers. Indeed χ is onto on both vertex groups and every edge group. The underlying finite quotient graph has first Betti number6−2+1=5, so

    kerχ ≅ Z*Z*F_5 ≅ F_7.

This gives an explicit CAT(0), F_7-by-Z group in the exact class of21.124.

## All compatible flat forms on this original graph

Let Q_A=A_1x²+2C_1xy+D_1y² and Q_B=A_2x²+2C_2xy+D_2y² be arbitrary compatible forms. For each of y=1,4,11, equality of the B lengths at (y,1) and(-y,1) forces C_2=0. The three positive-side equalities then say

    (A_1-A_2)x²+2C_1 x+(D_1-D_2+48A_2)=0

at the three distinct values x=7,8,13. Therefore this polynomial vanishes identically:

    A_1=A_2=A,    C_1=C_2=0,    D_2=D_1+48A.

Conversely these identities satisfy every edge equation. Positive definiteness is exactly A>0,D_1>0. The two Schur complements are B_A=D_1 and B_B=D_1+48A, so they can never be equal.

This excludes every uniform-height compatible metric on the **original two-vertex graph**. It does not establish the corresponding exclusion after arbitrary finite covers, where different lifts of a vertex may carry different metrics and new constructions may use additional dimensions. In particular, it supplies no obstruction to a virtual RAAG embedding.

## Explicit linearly growing monodromy

Choose the edge (7,1)↔(1,1) as a maximal-tree edge and put

    T=a^7 t=b s.

Then both a and b commute with T. The remaining five stable letters u_1,...,u_5 have relations

    u_i^-1 a^(x_i-7) T u_i = b^(y_i-1) T

with (x_i,y_i)=(7,-1),(8,4),(8,-4),(13,11),(13,-11). Consequently the group is the mapping torus of the following automorphism of the free group F(a,b,u_1,...,u_5):

    a↦a, b↦b,
    u_1↦u_1 b^-2,
    u_2↦a^-1 u_2 b^3,
    u_3↦a^-1 u_3 b^-5,
    u_4↦a^-6 u_4 b^10,
    u_5↦a^-6 u_5 b^-12.

The inverse replaces the left/right exponents by their negatives. The n-th iterate sends u_i to a^(n p_i)u_i b^(n q_i), with (p_i,q_i)=(0,-2),(-1,3),(-1,-5),(-6,10),(-6,-12). The monodromy is linearly growing. This presentation is a useful eligible test case for future affirmative or negative work, without a claimed priority or solution status.

## Remaining gap

The uniform-height ansatz is blocked on this example. A new mechanism could permit varying height norms, higher-dimensional ambient flat data, noncanonical cubulations, or suitable finite covers. Merely asserting that the original CAT(0) metric can be rescaled to a common Schur complement is false. No claim of non-VRC, nonlinearity, failure of virtual RFRS, or failure of virtual specialness is made.
