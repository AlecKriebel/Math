# A checkable square-complex model for a one-twist family

UTC: 2026-10-24. Status: candidate supporting deduction, awaiting nonauthor review. Discovery estimate toward full21.124: **3%**. This does not assert virtual specialness or a complete answer. No novelty claim is made; a separate bounded priority check is pending.

## Exact claim

Let F=F(a_1,...,a_r) have finite rank r≥1, let w∈F, and define

    G(w)=<F,t,c | [t,a_i]=1 (1≤i≤r), c^-1 t c=t w>.

Equivalently, conjugation by t fixes each a_i and sends c to c w, so G(w)=F_(r+1)⋊Z. If w=1, this is F_(r+1)×Z, a RAAG. Suppose w has nonzero abelianization. Then **G(w) is the fundamental group of a compact nonpositively curved square complex and has an index-two subgroup admitting a compact nonpositively curved VH square-complex model**. The argument below also constructs an injective map into an explicitly cubulated finite-rank-free-by-Z group H_k. These conclusions alone do not prove a virtual embedding in a RAAG.

Replacing w by a cyclic conjugate changes the vertex-group markings by an inner automorphism of F and gives an isomorphic HNN extension, because t commutes with F. Thus assume w cyclically reduced and nonempty. Put L=|w| and k=gcd{|e_i(w)|:1≤i≤r}>0, where e_i is the exponent sum of a_i in w. Choose integers χ_i with sum_i χ_i e_i(w)=k. Let χ:F→Z send a_i to χ_i.

## 1. A cubulated ambient group

Consider

    H_k=<F,z,c | [z,a_i]=1, c^-1 z^k c=w>.

Take a rose R_r in which every basis circle has k unit edges, and a circle S with L unit edges. Their product V=R_r×S is a compact nonpositively curved square complex with π_1(V)=F×<z>. A circle C with kL unit edges maps by a combinatorial local isometry to V in two ways: along z^k in {basepoint}×S, and along w in R_r×{basepoint}. Attach the two boundary circles of the square annulus C×[0,1] using these maps. The resulting square complex X_k has fundamental group H_k.

Here is a direct link check, rather than an unsupported gluing assertion. Each old vertex link is a complete bipartite graph between free-graph directions and circle directions. Each new transversal annulus-edge direction is incident only with the two incoming/outgoing directions of one lifted attaching path at that side of the annulus. Those directions are distinct, by the local immersion condition. Both of them belong to the same part of the old bipartite link. Thus adding that transversal direction creates neither a loop, a double link edge, nor a triangle. Different transversal edges give different link vertices. This also applies when a transversal edge is a loop: its two oriented directions are distinct and occur at different annulus sides. A two-dimensional all-right link is flag precisely when it has no loop, double edge, or triangle. Consequently X_k is NPC; its universal cover is a CAT(0) square complex.

The homomorphism η:H_k→Z given by η(z)=1, η(a_i)=χ_i and η(c)=0 is well defined because χ(w)=k. The Bass–Serre tree for the displayed HNN splitting has vertex group F×<z> and edge group <z^k>. Restricted to N=kerη, vertex stabilizers are free of rank r, while edge stabilizers are trivial. The quotient N\T has one vertex (η maps the vertex group onto Z) and k loop edges (η maps the edge group onto kZ). Therefore N≅F_(r+k), giving a finite-rank free-by-Z structure on H_k.

For an explicit basis, put x_i=a_i z^-χ_i and C_j=z^j c z^-j for 0≤j<k. Then conjugation by z fixes x_i, sends C_j to C_(j+1) for j<k−1, and sends C_(k−1) to C_0 w(x_1,...,x_r). The last identity follows from z^k c=cw(a) and w(a)=w(x)z^k. These formulas and their inverse give an automorphism of F_(r+k).

## 2. An injective map of the original group

Define a vertex-group map

    i:F×<t>→F×<z>,    i(a_i)=a_i z^-χ_i=x_i,  i(t)=z^k.

It is injective: projection onto F detects the free coordinate, and then the z coordinate detects powers of t. Its image B has index k and equals

    B={(g,z^n): n+χ(g)=0 modulo k}.

Furthermore i(tw)=w(a), so both associated cyclic subgroups <z^k> and <w(a)> of H_k are entirely contained in B. Their inverse images in F×<t> are exactly <t> and <tw>. Consequently sending c to c extends i to an injection G(w)→H_k by Britton's lemma: a reduced original HNN word remains reduced, because no coefficient outside an original associated subgroup can map into the corresponding ambient associated subgroup.

This embedding is generally infinite index; it is not being used to infer the CAT(0) property by inheritance from an arbitrary CAT(0) overgroup.

## 3. A compact square complex for G(w) itself

Let V_B→V be the k-sheeted covering corresponding to B. The two local-isometric loops z^k and w in V lift to closed local-isometric loops in V_B based at the selected lift, since their elements lie in B. Attach a square annulus with kL unit squares along those chosen lifts. Call the resulting complex Y_w. Its fundamental group is G(w), by the marking in Section2 and the graph-of-spaces presentation. It is compact, and the same link argument in Section1 proves it NPC. This proves the first assertion directly, including k>1.

The natural map Y_w→X_k is a local isometry: it is a covering on the vertex space and, at a new transversal direction, the two original attaching directions are exactly those of the selected ambient annulus lift. No ambient corner between already present link directions is omitted. Thus the preceding Britton injection also has an explicit cubical realization.

## 4. The index-two VH model

Map π_1(Y_w)→Z/2 by sending c to1 and the vertex group to0. The corresponding two-sheeted cover has two copies V_B^0,V_B^1 of the vertex space and two square annuli. Annulus0 has its z^k-side in copy0 and its w-side in copy1; annulus1 has its z^k-side in copy1 and its w-side in copy0. In copy0 color free-graph edges horizontal and z edges vertical; reverse these colors in copy1. Color transversal edges of annulus0 horizontal and those of annulus1 vertical. Every square has alternating horizontal/vertical sides, and colors agree on gluings. This is a compact NPC VH square complex.

VH does not imply virtual specialness. A proof for21.124 would still need to exclude every relevant hyperplane pathology in a suitable finite cover, or give a separate injective RAAG map. Hyperbolic cubical specialness theorems do not apply automatically: these groups contain F×Z.

## 5. Finite-rank control and a retraction

Let K=η^-1(kZ)≤H_k. It has index k. Its free fiber has basis x_i,C_j, and conjugation by u=z^k sends every C_j to C_j w(x) while fixing x_i. Hence K retracts onto i(G(w)) by fixing x_i,u and sending every C_j to C_0. Equivalently D_j=C_j C_0^-1 (j>0) are extra fixed free generators, so K is the original one-twist mapping torus with k−1 additional fixed free-fiber generators. This exact mechanism gives an explicit CAT(0)-preserving finite-rank envelope in this restricted family; it does not imply Linton's general envelope preserves CAT(0).

## Boundary cases and exact remaining gap

The case w=1 is a RAAG and was separated before division by k. A nontrivial w in [F,F] has k=0, so the construction cannot choose χ(w)=k>0 or a finite-index vertex subgroup of the stated form. There is no claim for that case. For r=2, the CAT(0) conclusion for w∉[F,F] is prior: Delage2602.08759v3, Theorem1.2(1), corrects the older Samuelson statement. Our candidate artifact gives explicit square-complex and VH models, not a claim of first discovery. Even if this supporting lemma passes review, the actual RAAG-embedding problem is open in this note, already for generic nonprimitive w of nonzero abelianization. The general CAT(0) free-by-cyclic target is not resolved.
