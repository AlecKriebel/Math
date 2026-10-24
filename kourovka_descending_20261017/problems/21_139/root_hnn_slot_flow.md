# Exact slot-flow covers of a partial mapping-torus family

Checkpoint 2026-10-24T16:47:38.629177+00:00. Full21.139 discovery estimate **15%**. This is a restricted-family construction, not a solution of21.139 and not a first-priority claim. The qualitative unboundedness of this hyperbolic graph-of-free-groups family is already covered by Fruchter–Morales; the present note supplies explicit covers and their homology.

For q≥2 put

    G_q = 〈a,b,t | t⁻¹ a t = (ab)^(q−1)b〉.

The standard graph of spaces has vertex rose〈a,b〉 and one cyclic edge, attached along a and w=(ab)^(q−1)b. Both maps are injective, so its mapping-cylinder complex is a finite two-dimensional K(G_q,1). The word w is primitive: with u=ab,v=b, the pair u,u^(q−1)v is a free basis. Hyperbolicity and virtual compact specialness are separately checked in the companion HNN report; no category assertion is needed for the cellular calculation below.

## The exact theorem

For every q≥2 and n≥1 there is a connected cover of this K(G_q,1) of degree2nq with

    b₂ = n(q−2)+1.

Thus every fixed q≥3 has unbounded second rational Betti numbers, with an explicit linear lower bound in the degree. For q=2 the formula is1; it does not incorrectly assert unboundedness for the closed nonorientable genus-three surface group G₂. Every standard cover defined by the height homomorphism a,b↦0,t↦1 has b₂=0, since its b-coordinate cellular boundary is multiplication by −q.

## Construct the action

Take a connected bipartite q-regular multigraph D with n left vertices L_i and n right vertices R_i, indices modulo n. It has one edge of every color j=0,...,q−1 incident at every vertex. Color0 joins L_i to R_i; color1 joins L_i to R_(i+1); all other colors join L_i to R_i. Multiple edges are permitted. The color0/color1 edges make D connected, including n=1. There are2n vertices and nq edges.

The cover's2nq vertices are the incidence slots (v,j). Let P rotate the q slots around each vertex v. Let R interchange the two slots at the ends of each graph edge. R is a fixed-point-free involution. Set T=R∘P, with ordinary function composition.

Use a right permutation action: v·a=v, v·b=P(v), v·t=T(v). A word is traversed from left to right along these directed edges; this convention is fixed throughout. Since a acts trivially and b^q acts trivially, the defining relator closes at every vertex, for every choice of T. Connectivity follows because P connects all slots of each graph vertex and R connects adjacent graph vertices;〈P,T〉=〈P,R〉 is transitive. The action therefore defines a connected degree2nq cover and a subgroup of that index.

## Derive the boundary without a Fox transpose convention

Let V=Q^(2nq), indexed by cover vertices. Matrix P sends e_v to e_(P(v)), and similarly for T,R. Identify the face module C₂ with V and the three edge-coordinate blocks of C₁ with V_a⊕V_b⊕V_t. Put N=I+P+...+P^(q−1).

Read each face boundary directly as the path

    t⁻¹ a t w⁻¹.

The two t-edges cancel because a fixes every vertex. The b-edges traverse a full negative P-cycle, giving −N. The positive a-edge lies at T⁻¹(v). The negative a-edges in w⁻¹ occur at all slots of the P-cycle except P⁻¹(v). Consequently the boundary blocks are exactly

    D_a = T⁻¹+P⁻¹−N,
    D_b = −N,
    D_t = 0.

This is the actual boundary C₂→C₁ with columns indexed by faces, not the kernel of a transposed boundary. The independent relator-walk implementation constructs these columns before comparing them to the displayed formula.

Since T=RP, on ker N we have

    D_a = P⁻¹(R+I).

Therefore

    ker D₂ = {x∈V : Nx=0 and Rx=−x}.

The second condition assigns opposite coefficients to the two incidence slots of each edge. Orient each edge from left to right and identify its coefficient with its left slot value. The first condition says the sum of slot values at each graph vertex is zero, exactly the incidence-boundary condition for an ordinary graph flow. Thus

    ker D₂ ≅ H₁(D;Q).

The graph is connected, so its cycle-space dimension is

    |E(D)|−|V(D)|+1 = nq−2n+1 = n(q−2)+1.

There are no three-cells, and the complex is aspherical, so this kernel is H₂ of the subgroup itself. This proves the theorem for every q,n, independently of the finite tests.

## Reproducibility, scope and controls

`root_artifacts/verify_hnn_slot_flow.py` uses exact integers and Fraction elimination. It builds the permutations and relator paths independently of the claimed formula, checks the relation at every vertex, verifies d₁d₂=0, then compares the direct matrix with the formula and computes its rank. The fifteen cases q=2,...,6 and n=1,2,3 all pass. For q3 the covers of degrees6,12,18 have b₂=2,3,4. These finite checks corroborate the universal cycle-flow proof; they are not its substitute.

The sequence is not a residual cofinal chain: every cover action kills a, and its normal closure is in every action kernel. Positive normalized growth here therefore does not contradict vanishing second L²-Betti number of the one-relator group. Varying n for one fixed q is essential to the unboundedness statement; varying q across different groups would not suffice.

This construction resolves a known restricted family explicitly. It creates no argument that an arbitrary partial HNN with higher-rank free-factor edge groups admits the same slot system. The existence of compatible finite actions with many independent boundary kernels remains the general gap. No paper, DOI, or publication is proposed from this partial construction.
