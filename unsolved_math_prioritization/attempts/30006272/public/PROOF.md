# Incidence formulas for orbit closures of complexes

## Status and exact target

**Partial results only. The general Catalan-formula question remains unresolved.**
The catalogue name for 30006272 / OWR-14299283-013 incorrectly says
“Ekedahl–Oort”. In the primary report the notation is a canonical-basis element
indexed by an orbit, not an Ekedahl–Oort stratum. The actual question is to extend
the Fang–Reineke construction from irreducible components of varieties of complexes
to all their orbit closures by suitable Catalan combinatorics. No particular
Catalan indexing set or weight formula is specified in that report.

This note proves restricted formulas and obstructions to several straightforward
extensions. None is presented as new, or as a counterexample to the original
question. The semismall decomposition theorem is a standard external input;
the incidence constructions and their dimension criteria are proved below.

## 1. Notation and dimensions

Work over C, with rational intersection cohomology. Let n >= 1, let
r=(r_1,...,r_{n-1}) and h=(h_1,...,h_n) have nonnegative integer entries, and set
r_0=r_n=0 and d_i=h_i+r_{i-1}+r_i. On vector spaces dim V_i=d_i, put

    X(r,h) = { (f_i): f_{i+1} f_i=0 and rank f_i <= r_i }.

This is the closure of the orbit having ranks exactly r. Indeed, the image
incidence construction in §3 is irreducible, surjects onto this set, and is an
isomorphism over that orbit. Thus no independent normality assertion is needed.

For 0 <= k_i <= r_i, set k_0=k_n=0 and h[k]_i=h_i+k_{i-1}+k_i. Write S_k for
the orbit with ranks r-k. Let IC^0_X denote the intersection complex normalized
to be Q in degree zero on the smooth open stratum. Define

    P_{r,h;k}(q) = sum_j dim H^{2j}(IC^0_X)_x q^j,  x in S_k.

All stalks under discussion have no odd cohomology, by the standard type-A
quiver IC/canonical-basis theorem, recalled in Fang–Reineke §3. Our explicit
formulas below also establish evenness directly in their stated domains.

Define

    Q(k) = sum_{i=1}^{n-1} k_i^2 - sum_{i=1}^n k_{i-1}k_i
         = (1/2) sum_{i=1}^n (k_i-k_{i-1})^2.

The codimension of S_k in X(r,h) is

    c_h(k) = sum_i [ k_i^2 + k_{i-1}k_i + h_i(k_{i-1}+k_i) ].       (1)

Here and below sums with an h_i run from 1 to n. One verification of (1) is
as follows. A complex of ranks r decomposes as h_i copies of the simple at
vertex i and r_i copies of the interval representation on vertices i,i+1.
For interval representations U_[a,b], U_[c,d], a morphism from the former to
the latter is one-dimensional exactly when c <= a <= d <= b; otherwise it
is zero. This follows by writing the commuting scalar maps along the path.
Consequently

    dim End M(r,h) = sum_i (h_i^2+h_i r_i+r_i^2+h_i r_{i-1}+r_{i-1}r_i).

An orbit has dimension sum_i d_i^2 - dim End M. Substitute (r-k,h[k]) in this
expression and subtract; the difference is exactly (1). This proves the
formula for all h, without a sparse-support restriction.

We use the Gaussian polynomial G(N,a;q) = [N choose a]_q. It is the
Poincare polynomial, with cohomological degrees halved, of Gr(a,C^N). For
completeness, row-echelon forms decompose this Grassmannian into affine cells
indexed by partitions in the a by N-a rectangle. Each cell of complex
dimension j contributes q^j. Partition enumeration gives

    G(N,a)=G(N-1,a)+q^(N-a) G(N-1,a-1),

with G(N,0)=G(N,N)=1 and zero outside 0<=a<=N.

## 2. A transverse-slice reduction

**Proposition 1.** The germ of X(r,h) at S_k is, up to a smooth factor, the
germ of X(k,h) at its zero representation. In particular,

    P_{r,h;k}(q) = P_{k,h;k}(q).                                  (2)

**Proof.** Cancel a fixed invertible s by s minor in one differential.
Relative to the chosen source and target decompositions, write that map as

    A = [[a,b],[c,d]],  det(a) != 0.

Invertible changes of basis on its two spaces put it into
diag(I_s, d-ca^(-1)b). Explicitly multiply on the left by
[[I,0],[-ca^(-1),I]] and on the right by [[a^(-1),-a^(-1)b],[0,I]].
Change the adjacent maps by the inverse basis changes. The equations
A f_previous=0 and f_next A=0 then force respectively the s affected rows
and columns of those neighboring maps to be zero. All other relations are
precisely the equations for the smaller complex. Ranks of the adjacent maps
are unchanged; rank A is s plus the rank of its Schur complement.

The free parameters a,b,c form the smooth factor GL_s times an affine
space, and these operations and their inverses are algebraic on det(a)!=0.
Choose the pivots in the standard direct-sum normal form of the point in
S_k, and cancel its r_i-k_i contractible summands at each edge. Restrict to
the successive open pivot charts as necessary; each contains the given
point. The remaining dimension at vertex i is h_i+k_{i-1}+k_i, the remaining
rank bounds are k_i, and the point becomes zero. This proves the local
product assertion. Smooth pullback of the intersection complex with the
stated unshifted normalization gives (2). □

The reduction removes the ambient ranks, but not the arbitrary homology
sequence h. It is not itself a formula for the stalk at zero.

## 3. Image and kernel resolutions: exact smallness criteria

Choose subspaces U_i of dimension r_{i-1} and impose

    Im f_{i-1} subset U_i subset Ker f_i.

The incidence variety Y_im is the total space of the vector bundle

    direct_sum_i Hom(V_i/U_i, U_{i+1})

over product_i Gr(r_{i-1},V_i). In particular, it is smooth and irreducible.
The forgetful map pi_im:Y_im -> X(r,h) is projective: its incidence
description is closed in the product with a projective Grassmannian base.
It is surjective, since any lower-rank complex allows an intermediate
subspace of the required dimension. Over S_0 all the U_i are uniquely the
actual images. Thus it is a resolution, birational and an isomorphism there.

Over S_k its fiber is

    product_i Gr(k_{i-1}, C^(h_i+k_{i-1}+k_i)),

and therefore has dimension

    f_im(k)=sum_i k_{i-1}(h_i+k_i).                               (3)

The rank orbits give locally trivial strata for this map: over each orbit
the incidence fibers form the associated bundle of the stabilizer action.
Equivalently, this is a homogeneous Grassmannian family. Thus checking their
fiber dimensions suffices for smallness and semismallness.

Let Delta_i=h_{i+1}-h_i. Equations (1) and (3) give

    c_h(k)-2 f_im(k) = Q(k)-sum_i Delta_i k_i.                    (4)

**Theorem 2.** The image resolution is small if and only if
h_i >= h_{i+1} whenever r_i>0. In that case

    P_{r,h;k}(q) = product_i G(h_i+k_{i-1}+k_i,k_{i-1};q).         (5)

**Proof.** Under the stated inequalities, the right side of (4) is strictly
positive for every nonzero k, because Q(k)>0. Conversely, if Delta_i>=1
on an active edge, choose k=e_i; the right side of (4) is 1-Delta_i<=0.
The fiber then has positive dimension, so the smallness inequality fails.
This proves both directions. For a proper small resolution of a complex
variety by a smooth variety, R pi_* Q = IC^0_X. Proper base change identifies
its stalks with the cohomology of the fibers. The Grassmannian cell
decomposition now gives (5). □

Reversing the chain and dualizing all its spaces gives the kernel version:
pi_ker is small exactly when h_i<=h_{i+1} on every active edge, and then

    P_{r,h;k}(q) = product_i G(h_i+k_{i-1}+k_i,k_i;q).             (6)

These are restricted formulas for arbitrary n, including many orbit
closures whose homology support is not sparse.

## 4. One-edge blocks and a failed unrestricted sparse formula

For n=2 at least one of the two resolutions above is small. Hence

    P_{r,(h_1,h_2);k}(q)=G(k+min(h_1,h_2),k;q).                 (7)

This is the usual determinantal formula, here derived with both size
chambers and all lower-rank stalks. If positive entries of r never occur
on consecutive edges, X is a product of these determinantal varieties
(all other arrows are zero), so its stalk polynomial is the product of
the expressions (7) over its active edges. A product of these small
resolutions is small: codimensions and fiber dimensions add, with a
strict inequality for each non-open factor. Thus this assertion follows
without any unproved product formula for singular spaces.

The sparse-support hypothesis in Fang–Reineke's formula cannot simply be
dropped. Take r_1=1 and h=(1,1). Then X is the rank-at-most-one 2 by 2
determinantal cone, and its origin has polynomial 1+q by (7): the small
resolution has fiber P^1 there. In the literal sparse formula with this
non-sparse h, every summation parameter is forced to zero and every
Gaussian factor is 1, giving the incorrect answer 1. This is a
counterexample to that *unrestricted extrapolation*, not to the report's
unspecified Catalan extension.

## 5. Semismallness and bounded Motzkin paths

Call [a,b] an active interval if r_a,...,r_b are all positive, where
1<=a<=b<=n-1.

**Theorem 3.** The image resolution is semismall if and only if

    h_{b+1}-h_a <= 1 for every active interval [a,b].              (8)

When (8) holds, a stratum S_k is relevant exactly when both conditions hold:

1. |k_i-k_{i-1}|<=1 for every i=1,...,n;
2. every connected interval [a,b] in every nonempty superlevel set
   {i:k_i>=m}, m>=1, satisfies h_{b+1}-h_a=1.

Thus the relevant nonnegative height paths have zero endpoints, steps
-1,0,1, bounds k_i<=r_i, and the stated additional interval condition.
They are Motzkin paths with restrictions; this does not identify them
with the report's unspecified Catalan combinatorics.

**Proof.** Necessity of (8) follows from (4) with k the indicator of [a,b],
for which Q(k)=1. For sufficiency, decompose k into its nonempty integer
superlevel sets, and decompose each into intervals. If R(k) is the total
number of these intervals, then

    sum_i Delta_i k_i
       = sum_(level intervals [a,b]) (h_{b+1}-h_a) <= R(k),
    R(k) = (1/2) sum_i |k_i-k_{i-1}| <= Q(k).

The first equality is telescoping; the second counts upward crossings
of each level; the final inequality uses x^2>=|x| for integer x.
Every level interval is active. This proves (4) is nonnegative.

Equality in both inequalities occurs exactly when every interval rise
equals 1 and every step has absolute size 0 or 1. These are precisely the
asserted conditions for c_h(k)=2 f_im(k). □

Here is the exact consequence of the semismall decomposition theorem.
Let R(r,h) be the set of relevant t, including t=0. Then, for all k<=r,

    product_i G(h_i+k_{i-1}+k_i,k_{i-1};q)
      = sum_(t in R(r,h), t<=k)
          q^(c_h(t)/2) P_{r-t,h[t];k-t}(q).                     (9)

**Justification.** Each fiber is a product of Grassmannians, hence is
irreducible. Its unique top-dimensional component has trivial permutation
monodromy, so the local system for every relevant stratum is the constant
rank-one system. The projective semismall decomposition theorem applies
to the smooth source and gives one IC summand for each relevant orbit
closure. The summand for t has support X(r-t,h[t]). Passing from perverse
normalization to IC^0 shifts it by -c_h(t), giving q^(c_h(t)/2) on stalks.
The point S_k lies in that support exactly when t<=k. Proper base change
and the Grassmannian cells give (9).

Equation (9) is an exact relation, not an unconditional closed recurrence:
the smaller supports on its right need not satisfy (8).
For example, r=(2,2,2), h=(0,1,0,1) satisfies (8), and t=(1,1,1) is
relevant. The smaller support has r-t=(1,1,1), h[t]=(1,3,2,2), whose
first active edge rises by 2. Thus even closure of this particular
semismall class under the displayed relation would be a false shortcut.

### A fully evaluated non-sparse example

Take n=3, r=(1,1), h=(1,2,1), so d=(2,4,2). Condition (8) holds. The only
nonzero relevant t is (1,0), with codimension 4. Its closure is the variety
with first map zero and second map a rank-at-most-one 2 by 4 matrix. The
origin stalk of that closure is 1+q by (7). At the origin k=(1,1), (9) gives

    P_{(1,1),(1,2,1);(1,1)}
      = G(4,1)G(2,1)-q^2 G(2,1)
      = 1+2q+q^2+q^3+q^4.                                     (10)

At k=(1,0) and (0,1) the polynomials are both 1+q; at k=0 it is 1.
These four formulas are proved by the decomposition and determinantal
calculation, not inferred from matching numerical values.

## 6. Canonical-basis translation and remaining obstruction

Let E(r,h) be the PBW element and C(r,h) the canonical-basis element
indexed by the same orbit. With Fang–Reineke's normalization their
geometric comparison is

    C(r,h) = sum_(k<=r) v^(-c_h(k)) P_{r,h;k}(v^2)
                              E(r-k,h[k]).                      (11)

This translates (5)–(7) and (10) into actual canonical-basis formulas in
the stated cases. In a small-resolution chamber the top power of v in
each non-leading coefficient is 2 f(k)-c_h(k)<0, as required. For the
example (10), c_h(1,1)=9 and the largest power is v^(-1); the two
one-edge coefficients are v^(-4)(1+v^2).

The source's sparse case is already established by Fang–Reineke. The
semismall route does not replace their theorem or cover arbitrary h.
For an explicit obstruction to extending our chosen geometric route,
take r=(1,1), h=(1,3,1), d=(2,5,2). The image resolution over k=(1,0)
has fiber dimension 3 and stratum codimension 5, so it is not semismall.
The dual kernel resolution similarly fails at k=(0,1).

Adding both image and kernel data does not repair this example. The full
flag resolution chooses U_i subset W_i subset V_i with dimensions
r_{i-1}, d_i-r_i, and lets f_i factor V_i/W_i -> U_{i+1}. It is a smooth
vector bundle over products of flag varieties, projective and birational
over X. Over S_k its fiber at vertex i is the flag variety of dimensions
k_{i-1}, h_i+k_{i-1} inside dimension h_i+k_{i-1}+k_i. Its total dimension is

    f_flag(k)=sum_i [ h_i(k_{i-1}+k_i)+k_{i-1}k_i ].             (12)

In the example, f_flag(1,0)=4 while c_h(1,0)=5. Thus even the semismall
inequality fails. These calculations rule out only the three specified
incidence maps as a universal semismall strategy. They do not rule out
other resolutions, other decompositions, or a Catalan formula.

The unresolved step is a uniform explicit construction for C(r,h), or
equivalently all P_{k,h;k}, when h has arbitrary adjacent positive entries
and rises/drops. It must specify its Catalan objects and weights and prove
bar invariance and triangularity (or the corresponding IC identity),
including the additional supported and shifted summands outside the
semismall range. No such construction or a counterexample to its existence
has been obtained here.

## References and verification boundary

The precise primary statement and inspected proofs are recorded in
SOURCE_GATE.md. The only deep external tools used here are smooth
invariance of IC, the small/semismall decomposition theorem, proper base
change, and the standard quiver IC/canonical-basis comparison. Their
hypotheses are checked where used. The accompanying standard-library
checker verifies dimensions, polynomial identities, smallness criteria,
level-path criteria, and the worked examples on bounded exact cases;
it does not implement intersection cohomology or prove the general question.
