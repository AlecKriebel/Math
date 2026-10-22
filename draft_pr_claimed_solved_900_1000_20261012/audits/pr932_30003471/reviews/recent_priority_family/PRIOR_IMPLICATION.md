# Checkable implications of the prior comparison claims

This is an audit of applicability, not an independent proof of any paper's index theorem. Original candidate: `c09ef9df8b1f4642be0396ba6343344be8fa25b0`, exact `public/PROOF.md` SHA256 `6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415`.

## 1. Data and a genuinely smooth carrier map

Let P,Q be bounded full-dimensional convex 3-polytopes and let phi be the **given** face-lattice isomorphism. Let P = intersection {u_i<=0}, with one actual irredundant facet F_i={u_i=0} per index; phi(F_i)=G_i. Let C(x) be the unique face with x in its relative interior, allowing C(x)=P. Every face is the intersection of the facets that contain it.

Begin with a face-preserving PL homeomorphism h:P->Q: barycentric subdivision of all faces including the interior face P gives a simplicial homeomorphism carrying every face H onto phi(H). Its degree as a map of pairs (P,partial P)->(Q,partial Q) is +1 or -1, hence nonzero. No assertion that h is smooth is made.

Here is a finite **smooth partition** construction sufficient for WXY3 Definition 2.8 and Remark 2.9. For every x in P choose an ambient ball U_x so small that U_x is disjoint from every closed facet F_i **not containing x**. This is possible because there are finitely many closed facets and the distance from x to each one not containing it is positive. Choose y_x in relative interior phi(C(x)). Compactness gives a finite subcover U_a. Take smooth nonnegative ambient bump functions subordinate to these U_a whose sum is positive on a neighborhood of P; normalize to chi_a there. Put f(x)=sum chi_a(x)y_a.

If z is in a facet F_i and chi_a(z)>0, then U_a meets F_i. By the ball construction this forces its center x_a in F_i. Consequently C(x_a) is contained in F_i and y_a in G_i. Convexity gives f(F_i) subset G_i, and intersection of the relevant facets gives f(H) subset phi(H) for every face H. This proves the **fixed assignment**, including all edges and vertices. Near a vertex v, only cover sets centered at v can contain v; every other bump vanishes on some neighborhood of v. There are finitely many bumps. The centers equal to v all have y_a=phi(v), so f is constant on a sufficiently small neighborhood of v in P. This degeneracy is allowed expressly by Remark 2.9. Since f is smooth on an ambient neighborhood and P is compact, f is Lipschitz, including across edges and vertices.

For 0<=t<=1, H_t=(1-t)h+t f takes P into Q. On any closed face H, both endpoints belong to the convex face phi(H), so the entire homotopy does too. Thus this is a homotopy of pairs, preserving every assigned face, and deg f=deg h=+/-1. This is a degree map, not a local diffeomorphism. Its derivative may vanish at vertices and elsewhere. It does not transfer Q's metric to P.

### A stronger explicit map for the older stratum definitions

The finite construction above is enough for WXY3 but can collapse an open piece of a face onto a smaller face. Older WXY v6 Definition 2.8 and WX v2 Definition 2.3 require relative strata to map to relative strata. The following explicit formula also satisfies that condition.

For each nonempty face H of P, including P itself, choose y_H in relative interior phi(H). Put b(t)=exp(-1/t) for t>0 and b(t)=0 for t<=0, and define

    w_H(x) = product over i such that H is not contained in F_i of b(-u_i(x)),
    W(x) = sum over nonempty faces H of w_H(x),
    f_s(x) = [sum_H w_H(x)y_H]/W(x).

Each weight is smooth in ambient space. At x in relative interior C, w_C(x)>0, and w_H(x)>0 implies that every facet containing C also contains H, equivalently H subset C. Therefore W>0 on P and on an ambient neighborhood of P; all active target points lie in phi(C), with y_C in its relative interior receiving positive weight. Hence f_s(x) lies in relative interior phi(C). In particular f_s preserves all strata exactly. It is globally smooth and Lipschitz; smoothness in every base direction follows immediately. It has nonzero degree by the same face-preserving straight homotopy to h. This construction works equally at nonsimple vertices: it is smooth and may have degenerate derivative there. It is not an attempted smoothing through local face diffeomorphisms.

## 2. Polyhedral and spin hypotheses

P and Q, with their actual Euclidean metrics, satisfy WXY3 Definition 2.5: use the finite supporting planes as ambient smooth hypersurfaces. Distinct intersecting planes meet transversally; parallel ones are disjoint. At each boundary point the convex tangent cone is full-dimensional with a connected spherical polygon link, and its bounding planes are exactly those of the incident facets. Arbitrarily many facets may meet at a vertex. P is a compact connected topological 3-ball. Orient P,Q arbitrarily; degree may have either nonzero sign, which the theorem permits.

Both tangent bundles are restrictions of the trivial oriented Euclidean bundle. Thus TP plus f* TQ is the trivial oriented rank-six bundle with a spin structure. P itself is spin. This verifies both the theorem's source spin condition and the paper's Definition 2.10 of a spin map. There is no metric equality between corresponding faces and no invertible derivative assumption.

## 3. Recent WXY3 theorem implies the exact comparison

The actual primary PDF is Wang-Xie-Yu, arXiv:2606.30130v1, submitted 2026-06-29, Theorem 1.2 on printed p2 and Theorem 6.7 on pp72-73. Take source (Mbar,gbar)=(P,Euclidean), target (M,g)=(Q,Euclidean), with f or f_s above and the assigned phi. Scalar curvature and facet mean curvature are zero on both. Both are convex, so all actual interior dihedral angles lie in (0,pi). The only nontrivial comparison hypothesis is exactly theta_P(i,j)<=theta_Q(phi(i),phi(j)) on each source edge. The target angle is constant, so its pullback has that same value regardless of f's behavior along the edge.

Thus the **stated theorem**, with every nonanalytic hypothesis checked here, gives equality of every corresponding edge angle whenever all these weak inequalities hold. The original OWR statement follows: if theta_P>theta_Q at every corresponding edge, reverse source and target, apply the theorem, and contradict strictness. This handles any given phi, not a favorable relabeling.

Certification boundary: I checked the actual theorem, definitions and endpoint proof, and the geometric bridge above. I did **not** independently check all local singular-domain self-adjointness, gluing and index steps in the 74-page paper. Therefore the rigorous priority description is 'the exact comparison is an immediate consequence of the theorem asserted in a prior preprint,' not 'a fully independently verified accepted prior proof settles current status.'

## 4. WXY3's actual proof yields the stronger entire normal Gram matrix

The theorem statement alone announces only edge-angle equality and flatness. Equality of edge angles alone must not be silently promoted to the full Gram matrix. The actual pp72-73 endpoint proof supplies more: a **nonzero parallel section** sigma of E=S(TP plus f* TQ), satisfying the assigned facet boundary condition. The source's Lemma 2.17 and its proof on pp15-16 explain the normal relation.

Because P and Q are Euclidean subsets, choose global parallel oriented orthonormal frames of TP and TQ. The pullback of the target's flat connection is the trivial connection in the pulled-back frame for **any** f: its coefficients are zero, independent of df. The direct-sum spin structure on the contractible P has a global parallel trivialization. In that trivialization sigma is one nonzero constant vector s, the grading operator Ecal is constant and unitary, and Clifford multiplication by each constant source or target facet normal is a constant skew-Hermitian matrix with square minus its Euclidean squared norm. Standard parallel regularity makes the trace condition an ordinary condition on every facet interior; since s and these matrices are constant, the same relation is an algebraic identity in one common fiber, separately for every facet.

Use inward normals u_i=-n_i and v_i=-m_i, matching the source convention. In the source's two Clifford actions, the facet relation is

    Ecal c_target(v_i) s = - c_source(u_i) s.

For arbitrary facets i,j, whether or not they meet, add the i and j identities with real coefficients a,b:

    Ecal c_target(a v_i+b v_j) s = -c_source(a u_i+b u_j) s.

Taking squared norms and using Ecal unitary and c(w)*c(w)=|w|^2 I gives

    |a v_i+b v_j|^2 |s|^2 = |a u_i+b u_j|^2 |s|^2.

Cancel |s|^2>0, expand in a,b, and compare the cross coefficient (or set a=b=1). It follows u_i dot u_j=v_i dot v_j and hence n_i dot n_j=m_i dot m_j for **every** pair. There is no need to assume these faces intersect or to prove a matrix invertible. This is an independently checked Euclidean corollary of the stronger output explicitly produced by WXY3's proof, conditional on the paper's analytic existence argument.

## 5. Earlier asserted routes and their caveats

WXY arXiv:2112.01510v6 (2023-03-08), Theorem 1.7, also asserts the exact comparison: the explicit map f_s satisfies its stricter polytope-map definition, the target is convex/flat with Euler characteristic one, and in equal dimension its A-hat-degree is ordinary nonzero degree (only the degree-zero A-hat component contributes). The target scalar and facet mean curvatures vanish, so factors involving derivatives in that theorem multiply zero. Its full 116-page proof is not audited here.

WX arXiv:2203.09511v2 (2023-03-21), Theorem 2.9(iii), literally gives the entire Gram conclusion after identifying Euclidean parallel transports with constant vectors and selecting arbitrary facet-interior points x_i,x_j. Its condition of boundary distance contraction is removed for flat target facets by Remark 2.12; independently, it can be satisfied by scaling the source metric to L^2 times Euclidean with L at least the Lipschitz constant of f_s. Constant scaling preserves zero scalar and face mean curvatures, dihedral and unit-normal inner products, spin, and degree. All theorem hypotheses then hold, including target Euler characteristic one. Source boundary distance contraction follows from length comparison under the Lipschitz map. This is an asserted prior all-Gram result; its proof invokes the older WXY index theorem.

Bär-Hanke-Schick arXiv:2202.05180v2 (2026-07-15) refutes specific claims in WXY **v2** and says WXY **v6** remains under verification. Its counterexamples use nonconvex domains. They are not counterexamples to the present convex P,Q comparison. Nor do they automatically refute WXY3 v1. They prevent treating all older assertions as independently validated merely by citing their theorem labels. Brendle-Wang's published acute-angle paper also records a verification caveat about the older program. Neither caveat is a proof that the exact convex comparison remains open on 2026-10-15.

## 6. Why Bi and the published smoothing headline theorems are different

Bi arXiv:2608.06320v1 assumes a smooth positive-definite metric on a neighborhood of **one fixed** polytope. Arbitrary face-lattice equivalence does not furnish a face-preserving local diffeomorphism at a nonsimple vertex, so neither h nor the deliberately degenerate smooth maps above permit a nondegenerate pulled-back metric there. The map f_s is a degree map and can have zero derivative. Consequently Bi's theorem statement is not, by the metric-pullback argument alone, an unconditional literal prior theorem for every P,Q here. The same obstruction affects naive use of Brendle's matching-angle theorem and Brendle-Wang's restricted acute-angle theorem; the latter also imposes the nonobtuse all-incident-normal inequalities.

Nevertheless Bi explicitly states that the precise form of its positive degree-one hemisphere map q is inessential, and its construction/proof contains nearly the whole candidate's later mechanism. Replacing Bi's radial source-normal q by the candidate's compatible target-normal q, and using exact Euclidean rank-one arclength contraction, is the identifiable adaptation. This is evidence for a specialized independent proof/simplification, not for a first comparison theorem or a new general smoothing method.
