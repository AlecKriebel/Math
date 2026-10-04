# Independent mathematical reconstruction

Sealed 2026-10-02 07:40:11 UTC, before any original independent-review file, root conclusion, or sibling conclusion was read. This is verification of the frozen candidate, not new proof search or a proposed repair.

## Claim and hypotheses

Let h be a plane homeomorphism with one D >= 0 such that |h^k(x)-x| <= D for every x and every integer k. Assume positive integers n_j tend to infinity and h^(n_j) converges to the identity uniformly on each compact subset. The candidate claims h is the identity. This is the n=2 part of source 3009, not the all-dimensional conclusion or a novelty claim. The standard recurrence interpretation supplies n_j -> infinity; a constant sequence of zero powers would not be recurrence.

## Logical reconstruction

1. If D=0 the displacement inequality implies identity immediately. Suppose D>0.
2. For fixed a, every h^k(B(a,2D)) is an open connected nonempty set. It intersects the k=0 ball because h^k(a) lies both in its own image ball and in B(a,2D), using D<2D. A union of connected sets all meeting one connected member is connected; one need not require one common intersection point among all the image balls.
3. For y in the original ball, |h^k(y)-a| <= |h^k(y)-y|+|y-a| < 3D. Thus B(a,2D) is contained in U_a and U_a is contained in B(a,3D). The strict inequalities correctly use an open ball and D>0.
4. The index set is all integers, so shifting k proves h(U_a)=U_a. A forward-only union would not establish equality. A homeomorphism commutes with closure, so C_a=closure(U_a) is invariant, nonempty, compact, connected, and contained in the closed 3D ball.
5. The complement of C_a has exactly one unbounded component W_a. Indeed the connected exterior of a sufficiently large containing disk lies in one component; any unbounded component meets this exterior and therefore is that component. Complementary components are open because the ambient plane is locally connected.
6. Define K_a=R^2 minus W_a. This is closed. Every point strictly outside the closed 3D ball is in W_a because a radial ray to infinity avoids C_a; hence K_a is bounded and compact. Equivalently K_a is C_a with every bounded complementary component V adjoined. Each such V has nonempty boundary in C_a: it is a nonempty proper open set and a boundary point outside C_a would have a small connected ball in the open complement and therefore lie inside V. Its closure is connected and intersects C_a. The union C_a union all closure(V) is consequently connected and is exactly K_a. Its complement is W_a, connected by its definition. This supplies every continuum/nonseparation hypothesis; local connectedness of C_a or Jordan boundary is unnecessary.
7. Invariance of C_a makes h permute its complementary components. A plane homeomorphism is proper (the inverse takes compact sets to compact sets), so an unbounded component cannot have bounded image. Hence h(W_a)=W_a by uniqueness, and h(K_a)=K_a. The equivalent infinity-extension argument in the candidate is valid. It cannot be replaced by assuming arbitrary complementary components are invariant.
8. The one-step bound supplies the proper homotopy H_t(x)=x+t(h(x)-x). The estimate |H_t(x)|>=|x|-D is uniform in t; this ensures a continuous homotopy on S^2 fixing infinity. Its degree is +1, so h and its sphere extension preserve orientation. There is no assumption that H_t is injective or an isotopy.
9. Cartwright–Littlewood applies to precisely the compact connected nonseparating invariant set K_a and gives a fixed point in K_a. As a ranges arbitrarily far from the origin, this yields arbitrarily distant finite fixed points. For the only required counting step, choose centers with distance >6D, so their closed containing disks are disjoint, giving two distinct finite fixed points.
10. The tail estimate in the candidate follows from |h^k(x)|>=|x|-D and the chordal formula. For |x|>=R>D, its displayed upper bound is uniform in k and tends to zero as R grows. On the closed R ball compact-open recurrence supplies uniform chordal convergence. Thus the sphere extension is recurrent uniformly on the entire sphere; infinity is fixed.
11. The sphere extension has at least the two finite fixed points plus infinity and is an orientation-preserving recurrent sphere homeomorphism. The Kolev–Pérouème exactly-two-fixed-points theorem for a nonidentity map forces identity.

Initial verdict: the candidate's intrinsic planar chain is valid conditional on the stated imported theorems. No topological gap was found in U_a, filling, preservation of infinity, or the fixed-point count. Primary proof/version verification and adversarial controls remain to be completed.

## Boundary and scope checks

- For a boundary-fixed closed-disk homeomorphism, the identity extension to the exterior is a plane homeomorphism by the pasting lemma, including its inverse. All disk orbits stay in the disk and exterior points are fixed, giving a common bound 2 for the unit disk. Recurrence on the compact closed disk is uniform and pastes to compact-open recurrence on the plane. Its orientation follows already from bounded displacement; no independent orientation assumption has to be added to the disk question.
- No smooth pasting is needed for a diffeomorphism special case: forgetting smoothness allows the same homeomorphism proof. Matching derivatives at the boundary would be needed only for an unsupported assertion that the exterior extension is smooth.
- No n>=3 argument has been produced or verified. The planar proof imports specifically two-dimensional topology; in dimensions at least 3 sphere rotations already destroy its final fixed-point-count mechanism.
- A separate positive-turn proof budget must not be charged for this verification. Any future repair that introduces substantive new mathematics would require root/user handling of the original attempt budget.
