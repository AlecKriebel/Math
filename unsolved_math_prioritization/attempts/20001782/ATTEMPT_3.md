# Attempt 3: real spectral compression of the element-order route

3 October 2026. Outcome: stronger quantitative conditional bounds, without
a proof of a dimension-only element-order bound. General target unresolved.
Discovery-goal completion estimate: 15% (subjective).

## What is being tested

The earlier reduction uses a complex diagonalization of an abelian subgroup
and pays m^d when all element orders are at most m. Real orthogonal
representations have conjugate-paired eigencharacters. Could this extra
structure either close the argument or isolate a smaller obstruction?

## Real abelian bound

Let A be a finite abelian subgroup of O(q) with all element orders at most m.
Its exponent e is realized as an element order, so e<=m. Simultaneous unitary
diagonalization of commuting normal matrices, followed by pairing nonreal
conjugate characters, decomposes its real representation into t real lines
and s invariant real planes, with t+2s=q. On a real line the image has
at most two elements; on a plane the common action is by rotations and its
image is cyclic of order dividing e. A map acting trivially on all summands
is the identity. Consequently

    |A| <= 2^t m^s
         <= F_q(m):=max_{0<=s<=floor(q/2)} 2^(q-2s)m^s.       (1)

Trivial real summands may be included; repeated characters only make the
bound less sharp. For m>=4 this gives

    F_q(m)=2^(q-2 floor(q/2)) m^floor(q/2).

For m<=4 the convenient formula gives F_q(m)=2^q. No incorrect assertion
that the exponent of an arbitrary nonabelian group is realized is used;
this step applies only to A.

Let J_C(q) be a Jordan constant for finite subgroups of GL_q(C). Every
finite G<=O(q) has an abelian normal subgroup of index at most J_C(q).
Thus if m(G)=max_g ord(g),

    |G| <= J_C(q) F_q(m(G)).                              (2)

For growing m the exponent floor(q/2) cannot be improved for arbitrary
orthogonal groups: the block rotations C_m^floor(q/2), with trivial
remaining line when q is odd, have maximum element order m and order
m^floor(q/2). These abstract groups are not claimed to be Delone examples.

The use of Jordan's theorem is classical and credited; the elementary
real-representation refinement is not asserted to be novel.

## Applying it only to the missing kernel

With k-dimensional short span from Attempt 2, let q=d-k and let m_K be
the maximum element order in the restriction kernel. If q>=1, then

    |S_x(2R)| <= (a+1)^(k^2) J_C(q) F_q(m_K).             (3)

This is a better-targeted sufficient claim than bounding every element of
the original group. In dimension four with k=2, the kernel lies in O(2).
Its orientation-preserving subgroup is cyclic of index at most two, so
the sharper elementary estimate |K|<=2m_K is available without Jordan.
The full order of a multi-plane rotation is an lcm, not the angle order
in a single arbitrarily chosen plane.

## An independent geometric bound, avoiding Jordan

For completeness, a direct metric argument confirms that a maximum-order
bound is genuinely sufficient without any classification. If m>=2 and
G<=O(q) has all element orders at most m, then for distinct g,h in G the
nonidentity orthogonal map g^(-1)h has a nontrivial root-of-unity eigenvalue
of order n<=m. Hence

    ||g-h||_F >= ||I-g^(-1)h||_op >= 2 sin(pi/m)=delta.

All matrices of G lie on the radius-sqrt(q) sphere in R^(q^2). Disjoint
open Euclidean balls of radius delta/2 around them fit in the ball of
radius sqrt(q)+delta/2. Comparing volumes proves

    |G| <= (1 + sqrt(q)/sin(pi/m))^(q^2).                 (4)

For m=1 the group is trivial. The minimum root separation used above is
valid because 2<=n<=m and sin(pi/n)>=sin(pi/m).

## Why the original target still does not follow

Equations (2)–(4) are conditional on an order or isolation estimate that
has not been obtained for the Delone kernels. Packing cluster points
only gives displacement bounds scaled by r/R, which tends to zero in
the exact lattice family of Attempt 1. An abstract cyclic rotation can
approach the identity arbitrarily closely. Neither real diagonalization
nor metric packing incorporates centered equivalence at neighboring
Delone points. They reduce and sharpen the missing assertion; they do
not prove it. This route is blocked at that precise geometric step.
