# Turn 5: a metric-dependent isometric stellar obstruction

Problem 30002820. Fifth and final author turn. **The intended isometric subdivision problem remains unresolved.** This turn excludes arbitrary metric-dependent face-stellar choices on a closed triangulated sphere, without continuity or locality assumptions, and gives a contrasting isometric single-edge construction on a triangular disk. Neither result is universal nonexistence of every isometric scheme.

Conformal comparisons use the vertex/edge correspondence inherited from the original indexed triangulation. The negative statements are not assertions about quotienting metrics by arbitrary relabellings.

## 1. The class to be excluded

Let T be the boundary triangulation of a tetrahedron, viewed as an **intrinsic** triangulated sphere. Its input consists of six positive lengths making each of its four faces a nondegenerate Euclidean triangle; a simultaneous embedding as the boundary of a Euclidean tetrahedron in R³ is not required.

Suppose a scheme retains every old edge and inserts exactly one point strictly inside each old face, joining it to the three old vertices. All new lengths are required to be the induced Euclidean lengths in that old face. The choice of each point may depend on the entire input metric and on labels, with no regularity or symmetry requirement.

**Theorem.** No scheme in this class preserves discrete conformal equivalence for all valid input metrics on this fixed closed sphere.

The same argument excludes a universal isometric one-center stellar rule on a single triangular disk. The closed-sphere construction below prevents the conclusion from relying on a boundary convention in the source.

## 2. Old boundary edges fix the old vertex factors

Take as reference input the metric with every tetrahedral edge length 1. Fix one face ijk. Let P be the scheme's inserted reference point in that equilateral face, and let its distances to the three vertices be alpha_i, alpha_j, alpha_k>0. Choose i so that alpha=alpha_i is largest, and write beta=alpha_j, gamma=alpha_k. Put

    Delta=alpha−|beta−gamma|>0.                             (1)

The strict positivity follows because beta,gamma>0 and alpha≥max(beta,gamma).

For any conformally rescaled input mu_uv=a_u a_v lambda_uv, an assumed refined conformal equivalence has multipliers b_v. Since all old edges are retained with their original lengths, b_u b_v=a_u a_v on every old edge. On an old triangle this forces b_i=a_i, b_j=a_j, b_k=a_k: the positive quotients b_v/a_v have pairwise products 1. This does not require the three old vertices to remain a face of the refined complex; retaining the three edges suffices.

If Q is the corresponding inserted point in the new face and t>0 is its refined multiplier, its distances must therefore satisfy

    |Q−i|=t a_i alpha,   |Q−j|=t a_j beta,   |Q−k|=t a_k gamma.  (2)

## 3. A quantitative thin-triangle obstruction

Choose

    0<h=min(1/4, Delta/[6(beta+gamma)]),
    b_h=sqrt(1/4+h²).

Scale the old vertices by a_i=b_h, a_j=a_k=1, and give the fourth tetrahedral vertex multiplier 3/4. In face ijk the side lengths become b_h,b_h,1. Realize it as

    j=(0,0),       k=(1,0),       i=(1/2,h).

The other two faces through i have lengths b_h,(3/4)b_h,3/4, and the remaining face has lengths 1, 3/4, 3/4. All are strictly valid: 1/2≤b_h<1, so (7/4)b_h>3/4 and the other triangle inequalities are immediate. Thus this is a valid intrinsic tetrahedral metric and is conformally equivalent to the reference input. It need not be an extrinsically embedded tetrahedron, which is not a hypothesis here.

Any possible inserted point Q=(x,y) in the new face satisfies 0≤x≤1 and 0≤y≤h. Put

    delta_j=|Q−j|−x,       delta_k=|Q−k|−(1−x).

The Euclidean norm bounds imply 0≤delta_j,delta_k≤h. From (2),

    t(beta+gamma)=1+delta_j+delta_k≥1,
    t(beta−gamma)=2x−1+delta_j−delta_k.

Hence

    |2x−1|≤t|beta−gamma|+h,
    |Q−i|≤|x−1/2|+h≤t|beta−gamma|/2+3h/2.

But (2) also says |Q−i|=t alpha b_h≥t alpha/2. Consequently any such Q would require

    t Delta≤3h,      and therefore Delta/(beta+gamma)≤3h.   (3)

Our choice of h instead gives 3h≤Delta/[2(beta+gamma)], contradicting (3). Thus no point even in the closed thin triangle can have the required distances. In particular the supposed scheme cannot choose a valid interior point there.

This is a quantitative finite counter-input derived from the scheme's reference output, not an argument assuming that its chosen points vary continuously. The proof applies even to nonlocal or discontinuous point-selection rules in the stated stellar class.

## 4. A contrasting positive isometric disk example

The theorem does not say that metric-dependent isometric refinement is never possible. On a single triangular disk, choose just one edge ij with opposite vertex k, write a=l_jk,b=l_ik,c=l_ij, and insert the angle-bisector-foot fraction

    t=b/(a+b)

on ij. Join the inserted point m to k and use all **induced** Euclidean lengths, producing two triangles. Their only interior edge is mk. The associated length cross ratio is

    (l_ik l_mj)/(l_jk l_im)=b(1−t)/(a t)=1.                (4)

Therefore all such refined triangles are discretely conformally equivalent, by the two-triangle criterion in Bobenko–Pinkall–Springborn, Sections 2.2–2.3. This can also be checked directly by solving the endpoint-multiplier equations on the two triangles. The fraction is metric-dependent; this example is outside turn 2's fixed-affine class and turn 3's medial 1-to-4 topology, and it has no interior stellar center.

It is a scheme for this one-face disk class only. Applying independently chosen feet to both sides of an interior surface edge does not in general give the same edge point. No all-surface isometric extension follows from (4).

## 5. Final synthesis and honest source disposition

The five-turn packet establishes:

- sharp midpoint rigidity for induced refinement;
- nonexistence for every proper fixed-affine induced refinement;
- nonexistence for medial 1-to-4 metrics with fixed edge fractions, even with arbitrary inner metric choices;
- a fully defined, conformal, proper **non-isometric** output-metric scheme retaining old edge totals and factors;
- the isometric stellar obstruction above, and the limited two-triangle positive scope control.

Turn 4 answers the explicitly stated output-metric formulation by a substantial construction rather than an identity or constant output. Equation (6) of that turn proves why it does not preserve the original intrinsic face metric. The original source does not make this compatibility requirement explicit; the surrounding barycentric-subdivision context makes it plausible but does not supply an authoritative clarification. We therefore recommend a qualified **unsolved/source-interpretation hold, 5/5** for the intended metric-compatible question, with the positive output-metric theorem recorded prominently. Do not advertise an intended isometric problem as solved through the omission of that axiom.

The results here do not exhaust metric-dependent isometric subdivisions with arbitrary topology, and no iterative-convergence theorem is claimed for the non-isometric scheme. Independent review should audit both the mathematical statements and the recommended source-sensitive disposition. No historical novelty assertion is made. The standard conformal/cross-ratio facts are credited to Luo and Bobenko–Pinkall–Springborn; exact source https://ems.press/content/serial-article-files/46561 , printed 721–722.

The exact checker verifies rational height certificates, valid conformally rescaled closed-sphere inputs, the elementary distance bounds, and complete conformal compatibility for bounded pairs of the two-triangle disk construction. The universal conclusions follow from the proofs, not finite sampling.

Five substantive author turns completed. Final subjective estimate toward the intended unrestricted metric-compatible problem: 20%. Freeze the packet for full independent review; no sixth author search.
