# Analysis of AMR-061-0083

## 1. Target and scope

Let X be Gromov-hyperbolic, and let G <= Isom(X) be discrete and finitely
generated. Write Lambda_X(G) for the accumulation set of an orbit in the
Gromov boundary. The question is whether connectedness of Lambda_X(G) always
forces local connectedness, in the boundary subspace topology.

This formulation must not be replaced by any of the following narrower ones:
the boundary of a hyperbolic group; a Bowditch boundary; a quasiconvex subgroup
limit set; a Kleinian limit set in the boundary of H^3; a CAT(0) visual
boundary; or a deformation space of representations. The last two are
different objects, not merely special cases.

The inspected primary list is dated October 24, 2007, although its workshop
origin and dataset year are 2005. Its page 21 labels this question Problem 83.
Some other versions index it as 84. The mathematical statement, author and
page are therefore stronger identity controls than the number alone.

Problem 83 does not print cocompactness, quasiconvexity, relative hyperbolicity,
finite presentation, absence of parabolics, constant curvature, or a dimension
bound. Local compactness is mentioned in the earlier CAT(0)-boundary discussion;
we do not turn any ambiguity in that convention into a claimed counterexample.
All group-action obstruction examples below use proper geodesic spaces and
proper actions. Thus they survive even a stronger properness interpretation.

Empty and one-point limit sets are locally connected. A two-point set is not
connected. None of these elementary cases resolves the nontrivial question.

**Disposition:** no complete proof, counterexample, or prior full resolution
has been verified for the stated arbitrary-space problem. `unsolved` describes
this attempt's outcome, not an exhaustive certification of the literature.

## 2. Approach 1: identify the orbit with a hyperbolic group boundary

### Mechanism and valid conditional conclusion

Assume additionally that X is proper geodesic and that a finite-generator
orbit map from a Cayley graph of G to X is a quasi-isometric embedding. Its
image is quasiconvex by stability of quasi-geodesics. The Cayley graph is
hyperbolic, and the boundary extension identifies its boundary with
Lambda_X(G). Consequently, if that limit set is connected, the known local
connectedness theorem for connected hyperbolic-group boundaries applies.
This includes a geometric action and the usual quasiconvex subgroup case.

The point requiring proof in the general problem is a *lower* bound on orbit
distances. Finite generation only gives the upper bound

    d_X(g o, h o) <= L |g^{-1} h|_S,
    L = max_{s in S} d_X(o,s o).

Properness of an orbit means that bounded orbit balls contain only finitely
many group elements; it supplies no linear lower bound.

### Exact obstruction: a parabolic cyclic action

In the upper half-plane model of H^2 let T(z)=z+1 and o=i. The action of
<T> is discrete and proper. The hyperbolic distance formula gives

    cosh d(i,T^n i) = 1 + n^2/2,
    d(i,T^n i) = 2 asinh(n/2).

For n=2^k, asinh(n/2) <= log(n+1) <= (k+1) log 2 <= k+1.
Therefore d(i,T^{2^k}i)/2^k <= 2(k+1)/2^k -> 0. No quasi-isometric
lower bound is possible. This action's limit set is the singleton {infinity},
which satisfies the target and is locally connected: this is an obstruction
to the inference, not a counterexample to the question. The exact rational
upper-bound sequence is replayed in `verify.py`.

**Remaining gap:** a different argument is needed whenever the orbit is
distorted or nonquasiconvex. Finite generation, discreteness and connectedness
do not provide the missing orbit identification.

## 3. Approach 2: parametrize the limit set by a Peano continuum

### A valid topological transfer lemma

If K is compact and locally connected, Y is Hausdorff, and f:K->Y is a
continuous surjection, then Y is locally connected. Here is the useful
closed-map argument. Given y in an open U subset Y, cover f^{-1}(y) by finitely
many connected open sets V_1,...,V_m inside f^{-1}(U), each meeting the fiber.
Their image union E is connected because every f(V_j) contains y. It lies
inside U. Compactness makes f closed, so

    W = Y \ f(K \ (V_1 union ... union V_m))

is an open neighborhood of y, contained in E. Thus y has arbitrarily small
connected neighborhoods. This implies local connectedness: in any open set,
the component of each point is a neighborhood of all its points, hence open.

For a one-ended hyperbolic group H, its compact boundary is locally connected.
A continuous boundary extension onto an orbit limit set would therefore
settle the question for that action. For surface groups the source is a
circle. Mj's theorem implements this strategy in the H^3 setting.

### Connected-tail lemma (proper actions)

**Lemma.** Suppose H is finitely generated and one-ended, X is a proper
geodesic hyperbolic space, and H acts isometrically with proper orbit map.
Then Lambda_X(H) is connected.

**Proof.** Let Gamma be a locally finite Cayley graph of H. Map its vertices
to the orbit of o and each edge continuously to a geodesic in X. The lengths
of all these edge images are bounded above by one constant L. The resulting
map f:Gamma->X is proper: any edge whose image meets a fixed bounded set has
an endpoint in its L-neighborhood, and there are only finitely many such
vertices by orbit properness and finitely many incident edges.

Remove a finite connected combinatorial ball B_n from Gamma, and let C_n
be the unique infinite component. The C_n can be chosen nested as n grows.
There are finitely many components of Gamma\B_n, since Gamma is locally
finite and the removed ball is finite. The components other than C_n are
finite. It follows that C_n contains all but finitely many vertices of Gamma.

In the compact Gromov compactification X union partial X, set
K_n=closure(f(C_n)). Each K_n is nonempty, compact and connected; the K_n
are nested. Hence their intersection K is connected and nonempty. Properness
of f implies K contains no point of X. Every orbit limit belongs to every
K_n since C_n contains all but finitely many vertices. Conversely, every
boundary accumulation point of f(C_n) is an orbit limit: each point on an
edge image is within L of an orbit vertex, and bounded-distance sequences
have the same boundary limit. Thus K=Lambda_X(H). QED.

This proof uses neither existence of a boundary map nor local connectedness
of the limit set. Properness of X and of the orbit map are essential to this
particular proof; they have not been inferred for an arbitrary nonproper X.

### An in-scope obstruction to the universal boundary-map strategy

Take H to be a closed orientable surface group of genus at least two.
Matsuda--Oguni, Theorem 1.1 (empty peripheral collection), supplies a
hyperbolic group K containing H such that no continuous H-equivariant map
partial H -> partial K exists. Let X be a Cayley graph of K with a finite
generating set. It is proper and geodesic, and the restricted H-action is
proper, discrete and isometric. The connected-tail lemma proves that its
limit set is connected. Yet the desired Cannon--Thurston map is absent.

This is stronger than merely citing the free-subgroup Baker--Riley example:
connectedness of the present limit set has actually been proved. It shows
that imposing connectedness does not rescue a universal Cannon--Thurston
argument.

It does **not** prove non-local-connectedness. A locally connected compactum
can be the image of an interval or circle by a map that is not equivariant
and is unrelated to the orbit map. The converse to the transfer lemma does
not assert an equivariant extension. No such converse is used here.

**Remaining gap:** prove local connectedness without an equivariant
parametrization, or verify a non-locally-connected limit set for one of these
actions by a separate argument. Neither has been accomplished.

## 4. Approach 3: relative hyperbolicity and the cut-point tree

Dasgupta--Hruska, Theorem 1.1 in the inspected 2024 version, proves that a
connected Bowditch boundary is locally connected, with no old restrictions
on peripheral groups. Thus the target is affirmative whenever its limit-set
action is identified with the geometrically finite boundary action of a
relatively hyperbolic pair. Peripheral finite presentation, one/two-endedness
and torsion hypotheses are not a remaining obstacle in that theorem.

One might try to obtain that identification from finite generation and the
convergence action supplied by a proper hyperbolic-space action. The missing
condition is geometric finiteness, not merely the convergence property.
Concretely, every limit point would have to be conical or bounded parabolic.

The surface-group action in Section 3 proves this attempted general reduction
false. Every nonidentity element of H has infinite order and acts
loxodromically in the hyperbolic Cayley graph of K. The boundary action
therefore has no parabolic subgroups. If it were geometrically finite, it
would realize the Bowditch boundary of (H,empty). Uniqueness of that boundary
would supply a continuous H-equivariant homeomorphism from partial H onto
Lambda_X(H), followed by its inclusion in partial K. Matsuda--Oguni excludes
even a continuous equivariant map of this kind.

**Remaining gap:** the non-geometrically-finite part of the target cannot be
discarded or renamed a Bowditch boundary. A direct local-topology mechanism
outside this reduction is needed. This argument does not refute the target.

## 5. Approach 4: finite connected approximations and chain refinement

For any connected metric space Z and any epsilon>0, every two points are
joined by a finite epsilon-chain. Indeed the points epsilon-chain-reachable
from a fixed point form a relatively open and relatively closed subset.
Applied to Lambda_X(G), this supplies arbitrarily fine *global* chains.

The tempting next step is to put such chains inside a uniformly small
neighborhood and pass to a connected limit. That step requires extra control.
The following explicit compact example pinpoints both missing uniformities.

Let D={0} union {1/n:n>=1}, and let

    C = ([0,1] x {0}) union (D x [0,1]).

Equip C with the Euclidean subspace metric. It is compact, since D is closed,
and it is path connected: join each point down its vertical tooth to the base
and then along the base. Let p=(0,1/2) and q_n=(1/n,1/2). The distance p q_n
is 1/n, but every connected subset E of C containing p and q_n meets the
base y=0. To see this, project E to its x-coordinate. The image is connected
and contains 0 and 1/n, so it contains the entire interval [0,1/n]. Choose
x in that interval outside D; the only point of C with that x-coordinate is
(x,0). Therefore diam(E)>=1/2.

In the open set U=C intersect {y>1/4}, each connected subset has constant
x-coordinate, since its x-projection is a connected subset of D. The component
of p is the vertical segment at x=0, and it contains no neighborhood of p:
the q_n converge to p from other components. Hence C is not locally connected.
This also proves failure of any uniform small-continuum modulus directly.

Now retain only the teeth 0,1,1/2,...,1/N and the base, giving C_N. Each C_N
is a finite connected graph and is locally connected. Nevertheless C_N
converges to C in Hausdorff distance, with the elementary estimate

    d_H(C_N,C) <= 1/(N+1),

because omitted teeth lie within that distance of the x=0 tooth. Thus local
connectedness of all finite approximants does not pass to their compact limit.
The family also has no common local-connectedness modulus: p and q_N require
a continuum of diameter at least 1/2 despite distance 1/N.

`verify.py` checks exact rational finite combs, their disconnection above a
horizontal cutoff, decreasing distances and the relevant bound. It does not
mistake a finite graph calculation for the infinite non-local-connectedness
proof, which is the projection argument above.

**Remaining gap:** use the group action to establish uniform local control,
not just connectedness, finite nets, or fine global chains. No such control
has been derived from the target hypotheses. C is a topological control,
not an asserted group limit set.

## 6. Approach 5: manufacture a counterexample using a hyperbolic cone

The converse construction is to start with C and build a hyperbolic space
whose entire ideal boundary is C. The hyperbolic cone construction realizes
bounded compact metric spaces as boundaries; it is described by the metric
in Koivisto, page 2, following Bonk--Schramm. This boundary-realization step
alone does not realize C as an orbit limit of a finitely generated discrete
isometry group.

The natural lifted symmetries demonstrably fail. Write D_0=diam(C), and use
coordinates (x,t) with t>=0. The cone metric is

    rho((x,t),(y,s)) =
      2 log((d(x,y)+max(exp(-t),exp(-s))*D_0)
            /(exp(-(s+t)/2)*D_0)).

For completeness, the boundary identification can be checked directly from
this formula. With base point (z,0), put a(x)=log(1+d(z,x)/D_0), so that
0<=a(x)<=log 2. The Gromov product of (x,t) and (y,s) is exactly

    a(x)+a(y)-log(d(x,y)/D_0+max(exp(-t),exp(-s))).

A sequence (x_n,t_n) is a Gromov sequence if and only if t_n tends to infinity
and (x_n) is Cauchy. Since C is compact, x_n converges to some x in C. Two
such sequences are equivalent precisely when their x-limits agree. The
displayed product also gives the original topology on C. Thus the missing
ingredient is genuinely the group action, rather than this boundary
identification. Hyperbolicity of the cone is the cited construction theorem;
the product calculation is not offered as a replacement for that theorem.

Any isometry a of C lifts to (x,t)->(a(x),t). At a fixed height t, all pairwise
distances are at most 2 log(1+exp(t)). Hence every orbit of these lifted
symmetries is bounded and has empty ideal limit set. Even if such a symmetry
group were finitely generated and discrete, its limit set would not be C.

Adding the same positive height shift h to every point is not a remedy.
For x!=y at the same height t the distance changes from

    2 log(1+exp(t)*d(x,y)/D_0)

to the strictly larger expression with t+h. It is not an isometry; it is also
not surjective on a cone with t>=0. An affine scaling argument would require
new similarities of C and an invariant two-sided construction, with fresh
verification of hyperbolicity, action discreteness and the orbit limit set.
Those properties have not been established.

The exact rational reparametrization u=exp(-t) permits controls without
floating point: exp(rho)=(d+D_0 max(u,v))^2/(D_0^2 u v). The checker confirms
the bounded fixed-height inequality and strictly changed distance under
u->u/2, including zero-distance controls.

**Remaining gap:** exhibit an actual finitely generated discrete action
with C (or another connected non-locally-connected continuum) as its *orbit*
limit set. Merely realizing a wild boundary, or attaching a group to a
space, does not meet the target.

## 7. What was and was not established

The two known affirmative source theorems cover important special cases.
The connected-tail lemma and the Matsuda--Oguni corollary rigorously rule out
universal equivariant-boundary-map and geometrical-finiteness proof schemes.
The parabolic, comb and cone controls invalidate three further shortcuts.
None of these results is presented as novel, a solution, or a counterexample
to Kapovich's full question.

The exact open obligation for this attempt remains: either derive local
connectedness from the full group-action hypotheses with no hidden
quasiconvexity/geometric-finiteness assumption, or give a verified group,
space, isometric discrete action, connected limit set, and explicit failure
of local connectedness. Finite controls cannot replace any of these clauses.
