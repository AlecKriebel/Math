# Turn 3: one exponential-Laurent input suffices

## Main scoped theorem

Suppose that, after permuting the coordinates,

    f_1(z)=R(exp(Q(z))),                                    (1)

where R is a nonconstant Laurent polynomial and Q is a nonconstant polynomial. Let f_2 and f_3 be completely arbitrary nonconstant entire functions. Then every entire F on C^3 bounded on V={sum f_i(z_i)=0} is constant on V.

In particular, a single input that differs by a constant from a nonconstant zero-free finite-order entire function suffices. This does not impose any finite-order, finite-type, nonvanishing or branching restriction on the other two inputs.

This strengthens the scope of turns 1–2. It is proved by a different quotient argument, not by assuming that an infinite-component trace exists. The conclusion remains partial for the original question, which allows all three inputs to be outside (1). The classical irreducibility, removable-plurisubharmonic and abelian-covering results are credited dependencies. No novelty claim is made.

## 1. A finite-fiber criterion for an ultra-Liouville space

We use the following elementary lemma in precisely the stated form.

**Lemma.** Let Y be a connected complex manifold, and pi:Y->C^n a holomorphic map. Suppose an analytic subset A properly contained in C^n has the following properties:

- pi^{-1}(C^n minus A) is dense in Y;
- its map to C^n minus A is a surjective finite-sheeted unramified holomorphic cover, with some fixed positive degree d.

Then Y is ultra-Liouville: every bounded continuous plurisubharmonic function v on Y is constant.

**Proof.** For w outside A put

    m(w)=max{v(y):pi(y)=w}.

The maximum is over exactly d points. On a sufficiently small ball disjoint from A the cover is a union of holomorphic inverse branches, so m is the maximum of finitely many continuous plurisubharmonic functions. Thus m is continuous and plurisubharmonic outside A. It is bounded by the same global bounds as v.

The standard removable-singularity theorem for locally bounded-above plurisubharmonic functions across analytic subsets extends m plurisubharmonically to C^n. This extension is still bounded. A bounded-above plurisubharmonic function on C^n is constant: its restriction to each complex affine line is bounded-above subharmonic and hence constant, and any two points lie on such a line. Write the constant as c. On the original open set, m=c.

Choose any w outside A. Some point of its finite fiber attains the maximum c. On the dense set pi^{-1}(C^n minus A), all values of v are at most c. Continuity of v implies this inequality on every point of Y. Consequently v attains its global maximum at an interior point of the connected manifold Y. The plurisubharmonic maximum principle makes v constant. This proves the lemma.

The conclusion is stronger than ordinary Liouville, which is needed for the next cyclic-cover step. The proof depends on a genuinely finite maximum and density. A supremum over a nonproper infinite fiber is not substituted for this maximum.

## 2. The finite quotient associated with R

By the exact polynomial-precomposition equivalence of turn 1, it is enough to prove (1) with Q(z)=z. Write g=f_2 and h=f_3 and define

    V={(x,y,z):R(exp x)+g(y)+h(z)=0},
    Y={(u,y,z) in C* x C^2:R(u)+g(y)+h(z)=0}.

The map

    E:V->Y,   E(x,y,z)=(exp x,y,z)                         (2)

is surjective and locally biholomorphic. All three inputs of V are nonconstant entire. The credited Rubel–Squires–Taylor theorem makes V irreducible. It follows that Y is irreducible as well, since a proper analytic decomposition of Y would pull back under the surjective map (2). Their regular loci V_reg and Y_reg are connected, and (2) maps the former onto the latter.

The local singularities cause no hidden exception. For Y, singular points require R'(u)=g'(y)=h'(z)=0. The first zero set is finite in C*, and the other two are locally finite discrete sets. The same observation applies to V with derivative exp(x)R'(exp x). Thus singular points form a locally finite discrete set. Reducedness follows because a repeated hypersurface factor would force the gradient to vanish on a positive-dimensional component. Regular loci are dense. None of these facts asserts that the whole hypersurface is smooth.

Regard R as a rational map on the sphere of degree d>=1. Let E_R be the finite set of its finite branch values, together with R(0) and R(infinity) whenever finite. For every t outside E_R, the equation R(u)=t has exactly d distinct roots in C*.

Define the proper analytic subset

    A={(y,z): -g(y)-h(z) belongs to E_R} of C^2.             (3)

It is proper because g(y)+h(z) is nonconstant, and none of its finitely many level equations is identically zero. A finite union of their zero sets cannot contain an open set. Its complement is therefore nonempty and dense.

For pi:Y_reg->C^2, pi(u,y,z)=(y,z), the portion over C^2 minus A is a surjective d-sheeted unramified holomorphic cover. Indeed all roots u are in C*, distinct, and satisfy R'(u)!=0, so the holomorphic implicit function theorem supplies exactly the local inverse branches. In particular all these points are regular.

This portion is dense in Y_reg. The holomorphic function R(u) cannot be constant on any open part of the irreducible two-dimensional hypersurface Y: fixing its value restricts u to a finite set and then g(y)+h(z) to one fixed value, producing sets of complex dimension one. Thus no one of the finitely many exceptional equations R(u)=e, e in E_R, holds on an open part of Y_reg. Their finite union has empty interior. Equivalently the inverse image of the complement of (3) is dense.

All hypotheses of the lemma apply to the connected manifold Y_reg. Hence

                         Y_reg is ultra-Liouville.          (4)

This finite-fiber maximum argument permits arbitrary g and h. They may have infinitely many critical points, essential growth and asymptotic values; those do not change the rational fiber degree d or the analytic nature of (3).

## 3. The cyclic cover and the original bounded entire function

The restriction E:V_reg->Y_reg is a connected regular unramified holomorphic cover. Its deck group is Z, acting by

    (x,y,z) -> (x+2 pi i k,y,z),  k in Z.

The action preserves the hypersurface and its regular locus, is free, and acts transitively on every fiber. The regular loci are connected by the irreducibility input, so this is not an unexamined disconnected cover.

Lin's theorem, as stated in Lin–Zaidenberg Theorem 1.6, says that a connected abelian cover over an ultra-Liouville base is Liouville. Apply it using (4). Thus every bounded holomorphic function on V_reg is constant. In particular an ambient entire F bounded on V has constant restriction to V_reg. Density and continuity give the same constant on every singular point of V. Finally apply turn 1 with polynomial precomposition Q in the first coordinate and identities in the others. The main theorem follows.

The zero-free finite-order corollary uses the classical Hadamard factorization as in turn 1. The previously known case with one polynomial input, already stated by Demailly, remains separately credited. Neither case includes every finite-order entire function, for example a general canonical product with infinitely many zeros.

## 4. Why the argument cannot be iterated without checking the base

There is a concrete obstruction to replacing the polynomial phase by an arbitrary entire phase in this proof. It is an obstruction to the method, not a counterexample to the source question.

Consider

    W={(x,y,z):exp(exp x)+exp y+exp z=0}.

Quotienting by the first logarithmic coordinate gives

    Y_*={(u,y,z) in C* x C^2:exp u+exp y+exp z=0}.           (5)

Before removing u=0, the latter hypersurface is biholomorphic to S x C, where

    S={(a,b):exp a+exp b=1},

via a=u-z-pi i, b=y-z-pi i and the remaining coordinate z. Lin–Zaidenberg Remark 1.9.2 explicitly records that S is transient and hence is not ultra-Liouville, even though it is Liouville. This is credited prior work, not inferred from its universal covering disc alone.

A positive Green function G on S gives a bounded continuous nonconstant subharmonic function exp(-G), extended by zero at its pole. Locally G is a positive multiple of -log|t| plus a harmonic term, so the extension is continuous and subharmonic. Away from the pole subharmonicity follows by differentiating exp(-G), and 0<=exp(-G)<=1. Pulling this function back to S x C produces a bounded nonconstant continuous plurisubharmonic function. Removing the analytic set u=0 leaves an open dense subset, and the restriction remains nonconstant. Therefore the base (5) is not ultra-Liouville.

This does **not** show W is non-Liouville. In fact W is already affirmative by the main theorem, since its second input is exp y; it is also within Demailly's earlier two-exponential setting after a coordinate permutation. The example shows why choosing the first cyclic quotient and iterating the cover theorem would be invalid. The base condition is a real requirement, not an automatic property inherited from a Liouville hypersurface.

## 5. Remaining question at 3/5

The source's unrestricted triple is still unresolved. The remaining cases include those in which no input is polynomial or a Laurent polynomial of a polynomial-phase exponential. One cannot extend the argument by replacing the finite root maximum with a supremum over arbitrary entire-function fibers, by assuming ordinary Liouville implies ultra-Liouville, or by passing to compact approximations without a uniform bound on the approximating zero sets.

The next search must supply a different way to treat infinite fibers and their topology, or construct an actual bounded nonconstant function on a source-admissible hypersurface. The non-ultra-Liouville quotient just displayed is explicitly not such a function on W.

## Verification and references

The exact checker verifies Laurent-to-rational fiber formulas, clearing denominators, derivative identities, and degree/multiplicity controls on a deterministic family. The finite arithmetic does not substitute for the plurisubharmonic extension theorem, connectedness or the abelian-cover theorem. Source editions remain bound by SOURCE_MANIFEST.json. The original irreducibility paper is an explicitly cited classical dependency whose statement was checked in Demailly's primary text; its complete original proof has not been retrieved.
