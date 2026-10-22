# Author turn 1: measured addition does not descend by forgetting measures

**Scoped obstruction to one proposed construction; the original unmeasured Haken-sum question remains unresolved.** 2026-10-01.

The first route is to use the classical linear normal-coordinate/branched-weight construction and then forget transverse measures. This turn makes the failure of that route precise. It does not assert that no other unmeasured operation exists.

## 1. The classical cone and what it actually supplies

For a fixed finite normal disk-type system with at most one chosen quadrilateral type per tetrahedron, let A be its matching matrix. Nonnegative measured weights form a cone

    W={w:A w=0, w>=0}.

The linear equations are closed under addition and nonnegative scalar multiplication. A sum does not create an incompatible quadrilateral because the type system was fixed beforehand. Integer solutions are the classical finite normal-surface case, credited to the standard construction described in Schleimer's thesis Section2.6. Branched-sector equations have the same algebraic form; Hatcher's cited draft describes the corresponding measured construction and its additional geometric equivalences. We do not use its unfinished global theory as a proved classification.

If a positive linear functional ell is used to normalize nonzero weights, the slice ell(w)=1 is convex, and hence contractible when nonempty. This is a statement about the **measured weight chart**. It does not identify that chart with the source's space of unmeasured laminations modulo an unspecified monotone equivalence, nor supply a topology on that space.

Already projective addition cannot be defined by simply adding representatives: for linearly independent u,v and distinct positive a,b, the vectors au+v and bu+v are not proportional. Indeed if au+v=t(bu+v), independence forces t=1 and a=b. Forgetting all measures could identify still more points than projectivizing, so a geometric example is needed to show that the ambiguity survives in an unmeasured setting.

## 2. A common-carrier example with different underlying outputs

In an oriented two-torus take the standard meridian alpha and longitude beta meeting once, both oriented positively. Smooth their crossing into a train track tau with two switches and a common branch. The three branch weights satisfy z=x+y. The ray u=(1,0,1) carries alpha and v=(0,1,1) carries beta. More generally the integral weight (a,b,a+b), for a,b>0, resolves the oriented crossings of a copies of alpha and b copies of beta.

This resolution has total homology (a,b). It has no contractible component: choose the track smoothing so every oriented branch is positive for the closed form dx+dy; the integral of this form on every carried component is positive, while it is zero on a contractible loop. Disjoint essential simple curves on a torus are parallel, and their primitive common homology direction is (a/g,b/g), where g=gcd(a,b). Since all orientations are positive, there are exactly g components. Thus u+v gives one curve of slope (1,1), while 2u+v gives one curve of slope (2,1).

Now take the product with a circle. The embedded branched surface B=tau×S^1 in M=T^2×S^1 carries the two tori alpha×S^1 and beta×S^1. Giving alpha×S^1 transverse measure1 or2 does not change its underlying unmeasured support. But the two measured sums above have underlying tori of slopes (1,1) and (2,1). Their classes in H_2(T^3;Z) are respectively

    e1 wedge e3 + e2 wedge e3,
    2 e1 wedge e3 + e2 wedge e3,

which are distinct primitive classes even up to sign. Hence the output tori are not ambiently isotopic. Their fundamental-group images are also distinct rank-two subgroups. The ambiguity remains under the specifically defined operation of inserting/removing parallel product regions, since that operation preserves the primitive slope of a torus family. No assertion is made about an alternative, unspecified equivalence relation.

This construction is in the source's common-carrier model. It does not assert that the pair has been supplied in a particular preassigned triangulation, or that every common branched carrier is simultaneously a compatible normal carrier. Establishing such an equivalence would require another argument.

## 3. Exact no-descent statement and its limitations

There is no operation on the unmeasured carried supports in this example which, for **every** choice of transverse measures on its two inputs, is the underlying support of measured coordinate addition. The same two input supports would have to return both nonisotopic output slopes above.

This is not a counterexample to the existence of an unmeasured Haken sum in the sense asked by Schleimer. For these finite compact leaves, choosing unit multiplicity recovers the usual finite-surface operation. An operation may specify such extra data or use a different geometric rule. The original problem asks when a meaningful construction exists, not whether all arbitrary measured choices agree. The example only blocks the particular proposal “choose arbitrary transverse measures, add, then forget them.”

For general laminations transverse measures may not exist at all, and normal disk cardinalities do not supply finite real coordinates. The next route must therefore retain transverse dynamics rather than treat all unmeasured laminations as points of a finite-dimensional cone.

Substantive author turns:1/5. Estimated completion15%. Classical measured/finite results are credited; no novelty or full-resolution claim.
