# Independent finite-algebra derivation

Scope: PR734, problem 2515 / Kourovka Notebook 21.6, frozen head
`7a00d71fdf01ffb785863c859d75e88f943d38cf`. This derivation was made after
reading the governing proof and before reading any other audit or author code.
The mechanism uses the augmentation ideal and the Frattini subgroup, rather
than relying on a finite-group classification or on selected generators.

## 1. Action, group law, and parity kernel

Let V=F2^2, and let E be the additive group of functions V->F2. For t in V,
write T_t f(v)=f(v+t). Acting on D=V x F2, define

    A_(f,t)(v,e) = (v+t, e+f(v+t)).

If A_(g,u) is applied first, followed by A_(f,t), the second coordinate is

    e + g(v+u) + f(v+u+t).

This is exactly A_(f+T_t g,t+u). Thus the law is

    (f,t)(g,u) = (f+T_t g,t+u),
    (f,t)^(-1) = (T_t f,t).

Faithfulness is immediate: an element fixing D has t=0 by its first
coordinate, and f(v)=0 at each v by its second coordinate. There are 64
distinct permutations in E semidirect V.

Let epsilon(f)=sum_v f(v) in F2 and write t=t1 e1+t2 e2. Translation preserves
epsilon. Therefore chi(f,t)=epsilon(f)+t1 is an onto homomorphism to F2.
Its kernel P has order 32, projects onto V, and has base kernel

    K = {(f,0): epsilon(f)=0}, |K|=8.

P is transitive: the projection reaches all four fibres. Within any fibre,
an even function supported on that fibre and one other fibre interchanges
its two points. This supplies transitivity on all eight points.

## 2. Group-ring coordinates and the universal generation calculation

Identify E with the regular module R=F2[V], using the point indicator at 0 as
the unit. In this identification T_t is multiplication by the corresponding
group element. Set x=1+T_e1 and y=1+T_e2. Then

    R = F2[x,y]/(x^2,y^2),
    J = ker(epsilon) = span_F2{x,y,xy}.

The function xy is the indicator of all four points of V; in particular it
is nonzero. The base group K is the additive group J.

Take any q1=(f,e1), q2=(g,e2) in P. No particular lifts are selected.
Since epsilon(f)=1 and epsilon(g)=0, write

    f = 1 + alpha*x + beta*y + gamma*xy,
    g = delta*x + eta*y + theta*xy.

Directly from the multiplication law, using the commutator convention
[a,b]=aba^(-1)b^(-1),

    q1^2                  = (x*f,0) = (x+beta*xy,0),
    [q1,q2]               = (y*f+x*g,0) = (y+(alpha+eta)*xy,0),
    [q1^2,q2]             = (y*x*f,0) = (xy,0).

These three base vectors are linearly independent: their x,y,xy
coordinates form a triangular matrix with diagonal 1. Hence they generate
K. Together with the projections e1,e2 of q1,q2, they generate all of P.

Consequently every subgroup Q<=P whose fibre projection is all of V is P.
Any subgroup transitive on D has full fibre projection, so P is its only
transitive subgroup. This conclusion uses no assumption about a preferred
pair of generators or about a regular subgroup.

## 3. Frattini interpretation without an external classification

There are precisely three maximal proper subgroups of P: the preimages
under P->V of the three one-dimensional subspaces of V. Each has order 16.
To see exhaustiveness, a proper subgroup cannot project onto V by the
calculation above. Its image is therefore contained in one of those three
lines, placing it in the corresponding proper preimage. Each such
preimage has index 2 and is maximal.

Their intersection is K. Thus, from the definition as the intersection of
maximal proper subgroups, Phi(P)=K. This is an independent finite-algebra
description of the obstruction: projecting fully modulo Phi(P) forces
generation of P. The preceding explicit calculation proves that assertion
here, so the audit does not require the general Burnside basis theorem.

The exhaustive standard-library reconstruction finds50 subgroups, exactly
three maximal subgroups, and intersectionK, agreeing with this deduction.
Its subgroup enumeration builds the lattice by repeatedly adjoining every
possible new element, so it does not presume the lattice size or the
minimal-transitivity conclusion.

## 4. A cycle that crosses a block translate

Use the zero-based labels2v+e, with v=0,1,2,3 corresponding to
0,e1,e2,e1+e2. Let b=(0,e2) and z=(delta_e1+delta_e2,0). Both belong to P.
The orbit C of (0,0) under b is exactly

    C = {(0,0),(e2,0)}.

The element z fixes (0,0) but flips the second coordinate above e2. Hence

    z(C) = {(0,0),(e2,1)},
    |C intersection z(C)|=1, z(C) != C.

Since C is a whole two-cycle of b, P lacks the required cycle-support
property. In one-based labels this is C={1,5}, z(C)={1,6}.
Combining this with the universal transitive-subgroup calculation excludes
every transitive subgroup with the cycle-support property.

## 5. Transfer to a block-stabilizer image

Let B be an ambient G-block with induced action G_B^B permutation-isomorphic
to P. For any transitive H<=G and any x,y in B, choose h in H with h(x)=y.
The intersection h(B) intersection B contains y. The block definition
therefore gives h(B)=B. Consequently H_B^B is a transitive subgroup of P
and equals P.

Lift b and z to elements h_b,h_z of H_B. Their other actions may be
arbitrary, and the restriction map may have a kernel. Because h_b
stabilizes B, its two-cycle C in B is a whole cycle in the entire domain:
the successive orbit points never leave B. Because h_z restricts to z,
its image of C crosses C as above. Thus C is not an H-block.

This proof needs surjectivity of the block action, not containment of the
embedded copy of P in H. It therefore addresses all transitive H, including
those with correlated actions on different finite blocks.

## 6. The infinite union

Put Omega_n=D x {0,...,2^n-1} and Omega=D x N0. Let G0=P. Define
G_(n+1)=(G_n x G_n) semidirect C2 with the nonidentity top element swapping
the two consecutive copies coordinate by coordinate. Embed G_n as its
first base factor, and extend all stage elements by the identity outside
Omega_n. The embeddings are actual faithful permutation embeddings.

Each G_n is finite of 2-power order, with |G_(n+1)|=2|G_n|^2, and transitive
on Omega_n. Any finite set of group elements lies in one stage, so the
union G is locally finite and every element has 2-power order. Every
element has finite support. Any two points lie in some Omega_n and are
joined by G_n, establishing transitivity on the infinite Omega.

For m>=n, G_m preserves the partition of Omega_m into consecutive copies
of Omega_n. This induction holds for the two base actions and for the top
swap. For m<n the embedded element stabilizes Omega_n. Thus each Omega_n
is a finite G-block. Every finite subset of Omega lies in one Omega_n.
This proves total imprimitivity according to the Notebook's exact
definition, without needing an alternative characterization by maximal
proper blocks. The same blocks are H-blocks for every subgroup H<=G.

At every stage, the bottom fibres D x {i} are permuted; every map between
them has a D-coordinate action in P. It is true at G0, is inherited by the
two base factors, and is preserved by a coordinate-for-coordinate swap.
An element stabilizing B=Omega0 consequently restricts to P. The embedded
G0 realizes every member of P, so G_B^B=P exactly.

The transfer argument excludes every transitive H<=G with the desired
cycle-support property. Taking p=2 and S=G meets the source's Sylow
condition: the whole 2-group is a maximal2-subgroup of itself. This remains
valid under either the periodic2-group or locally finite 2-group
formulation, because G satisfies both. No assertion about Sylow
subgroups of the entire infinite symmetric group is used.

The union proof is deductive. The independent2048-element first-wreath
check is a model sanity check, not a finite substitute for the induction.
