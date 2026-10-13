# Source-only independent mechanism baseline

Frozen before reading any candidate or assessment, at 2026-10-04T12:41:38.633149+00:00.

## Source and precise target

The independently retrieved AIM PDF is the 22 November 2004 version of the workshop document *Rational and integral points on higher dimensional varieties*, arising from the 11-20 December 2002 workshop. The lecture notes and problem list are credited primarily to John Voight and William McCallum, with overall arrangement by William Stein. Physical page 51, Question 17, asks for the 5-torsion of the genus-one normalization of the regular-pentagon quintic, whose five points at infinity are singled out. Its four remarks concern (i) infinity points among 5-torsion, (ii) possible principal homogeneous spaces and a twist of the X1(5) universal family, (iii) the relation to pencils of elliptic curves, and (iv) whether regularity is necessary and star-pentagon variants. The source itself does not specify an origin, a coordinate normalization, an exact singular-fiber set, or arithmetic descent.

## Independent approach family: dihedral geometry and double-cover normalization

Choose a unit circle and five equally spaced vertices; write the side-line product as P. The homogeneous pencil must be P + lambda Z C^2, since P has degree 5 while C has degree 2. Arbitrary scale choices for side equations rescale lambda. First derive the product from the actual side lines, over the real cyclotomic field, rather than guessing a quintic. At each vertex, the local degree-two term combines the two incident side-line linear terms and the square of the circle tangent. Generically this is an ordinary node. Five such nodes give arithmetic genus 6 minus 5 = geometric genus 1 only after irreducibility and absence of additional singularities are established.

A reflection of the regular pentagon preserves the pencil. Coordinates aligned with its fixed axis make the affine polynomial even in the transverse coordinate y. Set u = y^2. A useful algebraic route is to solve the quotient equation in x,u, preferably by a rational parameter, and then recover the curve via y^2=u. This creates a degree-two cover of a rational curve. If the branch divisor has degree four and is squarefree, the smooth normalization has genus one. The audit must verify both rational maps and both compositions, and exclude hidden components supported on every divided denominator. A birational statement over the generic field is weaker than a uniform claim for every smooth specialization; exceptional fibers require separate proofs.

The regular pentagon gives a rotation of order five. On a smooth genus-one curve an order-five automorphism, once an origin is chosen, has a translation component, while its origin-fixing component cannot have order five in characteristic zero. Thus a nontrivial order-five rotation is translation by a nonzero 5-torsion point. Its orbit on the five infinity points gives a cyclic order-five subgroup, after choosing one infinity point as origin. This yields the source's infinity subgroup geometrically but does not compute the remaining twenty geometric 5-torsion points. Those require an independent division-polynomial or isogeny mechanism and exact scheme-level claims.

## Falsifiable boundary checks and scope

1. Derive each side equation and verify its adjacent vertices. Bind the exact scale, circle equation, homogeneous pencil, and coordinate field.
2. Determine all singular parameter values directly, including lambda=0, any center degeneration, nonzero repeated-branch fibers, and lambda=infinity in the compactified pencil. Analyze every vertex's tangent cone, not just generic delta counts.
3. Check points at infinity: distinctness, smoothness, explicit tangent/gradient, reflection action, and origin. Circular infinity points are potential fixed points of rotation and must be checked against the pencil.
4. In the reflection route, prove quotient parametrization, quadratic-extension nontriviality, branch squarefreeness, primitivity, and absence of lost irreducible components. Verify forward and inverse rational formulas in both directions with all denominator hypotheses explicit.
5. Every discriminant, resultant, and factorization calculation is either a universal exact identity in a specified polynomial/rational-function ring or finite evidence. Label these differently.
6. The source's motivations about Sha, twists of the universal family, and nonregular variants are not theorem assumptions or completed consequences. An answer may delimit them, but must not silently convert motivations into proven global arithmetic statements.

## Independence record

No candidate manuscript, candidate PDF, metadata, review report, test script, or assessment ledger has been read before this baseline was written. Native retrieval and PDF extraction/rendering receipts preserve actual argv, UTC start/end, full stdout/stderr, exit code, HTTP response headers, curl response metadata, and source hash. The source-only mechanism is now fixed and its SHA-256 is recorded in BASELINE_FREEZE.json. Completion estimate at this checkpoint: 10% of this geometry-family audit.
