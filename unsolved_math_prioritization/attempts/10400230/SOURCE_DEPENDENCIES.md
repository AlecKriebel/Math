# Exact source dependencies and their limits

## Target

Ohtsuki (editor), Geometry & Topology Monographs4 (2002), Problem12.25 and complete remark, printed541/PDF169. The proposer is A. Stoimenow. The target is simultaneous primeness, alternation and achirality at every odd sum of two squares other than1,9,49. The exact primary page was visually checked. The source PDF hash is in SOURCE_MANIFEST.json.

## The graph-to-knot implication actually used

Stoimenow, Communications in Analysis and Geometry13(3) (2005),591–631, DOI10.4310/CAG.2005.v13.n3.a5:

1. Printed617–618 (PDF27–28): alternating medial diagrams and checkerboard graphs; switching checkerboard colors/plane duality mirrors the crossing choices
2. Lemma6.3, printed618/PDF28: diagram primeness from absence of a cut vertex
3. Lemma6.4, printed618–619/PDF28–29: determinant equals spanning-tree count for an alternating checkerboard graph
4. Proposition6.5, printed619/PDF29: odd determinant forces a single link component
5. Theorem4.12, printed604/PDF14: a reduced alternating diagram is prime precisely when the represented link is prime, credited there to Menasco1984
6. Proposition6.6, printed619/PDF29: only the graph-to-knot direction is used. No converse involving re-embeddings, flypes or mutation is needed

The pages604,618,619 were visually verified in addition to the exact target/conjecture page606. All new graphs explicitly have an orientation-preserving isomorphism with their **plane** dual, verified by the base rotation systems and paired ribbon substitution. This gives a sphere homeomorphism taking the alternating diagram to its mirrored crossing choice. Orientation-preserving sphere homeomorphisms are isotopic to the identity and extend preserving the ambient orientation, so the knot is achiral. Abstract graph self-duality or equality of determinant polynomials alone is not substituted for this requirement.

The source's Definition6.2 prints a nonstandard “removal of any ≤2 edges” formulation. Our proofs do not invoke that formulation. They check absence of **loops and bridges** directly. A crossing of an alternating medial diagram is nugatory exactly when the corresponding checkerboard edge is a loop or a bridge: the latter is a loop in the dual graph. This follows from the separating curve at a nugatory crossing. This is the elementary reduced-diagram criterion used here. Subdivisions may create two-edge cuts, which do not invalidate this criterion. Absence of cut vertices is separately established for diagram primeness.

Menasco's original article is *Closed incompressible surfaces in alternating knot and link complements*, Topology23(1) (1984),37–44, DOI10.1016/0040-9383(84)90023-5. Its author/institution bibliographic record was checked, but the publisher DOI retrieval failed. We do **not** claim to have retrieved or reread that entire original article; the exact credited prime-diagram theorem was read in Stoimenow's primary published paper. This is a source-access limit, not a replacement of the theorem by finite computation.

## Previously settled classes and obstruction

Stoimenow2005 Theorems4.1–4.2 (printed600–602) supply the separately-prime/alternating and primitive rational cases; Theorem4.21 and its proof (606–610) supply the perfect-square case. Claim4.25 (611–612) concerns a different three-tangle construction and is only a template obstruction. These were read and credited. Our norm constructions and closure are not promoted to an arbitrary-n realization.

## Arithmetic and linear algebra

The two norm-Euclidean ring arguments and the integer descent in turn3 are written out. The classical finite-field cyclicity/Cauchy consequence, Gauss lemma, sum-of-two-squares theorem, matrix-tree theorem and Smith normal form are identified as established tools, not new results. Dirichlet's theorem is needed only to turn the template-obstruction progression in turn2 into an infinite family; its original1837 paper in English translation is separately bound by SOURCE_ADDITION_TURN_2.json. The explicit missing examples require no analytic number theory.

No knot table, numerical knot recognizer, floating-point determinant, or experimental prime pattern is used to establish a universal theorem. The finite scripts check exact arithmetic, graph counts and polynomial identities. The topological bridge rests on the established theorems and explicit embedding arguments above.
