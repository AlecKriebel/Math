# Independent review of the surface-isotopy partial package

**Verdict: PASS_SCOPED_CREDITED_SUBCLASS_AND_GLUING_DIAGNOSTICS.** No mandatory mathematical correction was found. Keep the original problem **unsolved, 1/5 approaches**. The higher-genus subclass is a consequence of credited published algorithms, not a new discovery or a general compatibility algorithm. This is an independent adversarial AI audit, not human peer review.

Frozen `PARTIAL_RESULT.md` SHA-256:
`75bba871e88b8ed5b4e811f8b3e6b0f8e3c211bb8472ac5789c7f0ab685be9d1`.

## 1. Exact target and effective category

I checked the complete [K3 primary manuscript](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf), Problem 3.32 and remarks on printed pp. 154–155. The ambient space is R³. The submission expressly chooses finite locally flat PL input, records the point at infinity, and limits its proved subclass to connected surfaces. It does not claim an algorithm for arbitrary wild embeddings or solve the disconnected target.

[Baroni's published paper](https://msp.org/agt/2025/25-8/agt-v25-n8-p08-s.pdf), Theorem 4.1, is indeed an **oriented** genus-two classification algorithm. Its Section 4.1 explicitly formulates the side-compatible complementary-homeomorphism problem. His conventions require orientation-preserving three-manifold homeomorphisms unless otherwise stated. This supports the candidate's orientation and side-preserving use of the theorem, rather than an unmarked S³ interpretation.

[Bellettini–Paolini–Wang v2](https://arxiv.org/abs/1909.09328) explicitly works in the PL category with an oriented based S³ and identifies based ambient isotopy with orientation-preserving homeomorphism fixing infinity. Its current arXiv metadata says a theorem from v1 was removed for a proof gap. The candidate uses the current introduction and Theorem 1.1, not the removed result.

## 2. The point-at-infinity diagnostic is valid

Let V be a trefoil regular neighborhood in S³ and E its exterior. With infinity in int E, the compact bounded side of the displayed torus is V, with group Z. Move a point of int V to infinity by an orientation-preserving homeomorphism h of S³. The new torus misses infinity, its side containing infinity is h(V), and its bounded side is h(E).

The exterior group is nonabelian: the trefoil presentation maps onto S₃ by the two adjacent transpositions, which satisfy the braid relation and generate S₃. Thus the two bounded sides have nonisomorphic groups. A homeomorphism of R³ takes the closure of a bounded complementary component, a compact set, to another compact set. It cannot switch it with the unbounded complementary closure. Consequently the two tori are not equivalent in R³, even though h exhibits equivalence in unmarked S³.

This correctly refutes only the shortcut that discards the distinguished complementary side. It is not a counterexample to decidability, nor an assertion that the bounded side of every torus in R³ is a solid torus.

## 3. Exact coset order and gluing

With a,b the two reference boundary maps S₁→S₂ and c=ab⁻¹, boundary compatibility is

    αa=βb for some α∈A, β∈B.

Composing on the right with b⁻¹ gives αc=β. Thus compatibility is equivalent to c∈A⁻¹B=AB. The order AB, rather than BA, is correct even when the two trace groups do not commute. Changing the reference maps replaces c by α₀cβ₀⁻¹, which preserves membership in AB.

Every possible complementary homeomorphism is a target self-homeomorphism after the reference map, so there are no missing boundary choices in this reduction. If the restrictions are only isotopic, the boundary isotopy extends across a collar and makes them equal before gluing. The induced boundary orientations are opposite on the two sides, but the restrictions of orientation-preserving side maps preserve the same chosen surface orientation after both identifications are fixed.

The glued map preserves the component marked by infinity. Its image of that point can be moved back by an isotopy supported inside that component, leaving the surface fixed. The use of unpointed boundary trace groups therefore does not lose the interior marked-point requirement. The standard based-S³ equivalence cited above then gives a point-fixing ambient isotopy. Independently, the evaluation fibration at a point, together with path-connectedness of orientation-preserving PL homeomorphisms of S³ and π₁(S³)=0, yields path-connectedness of the point stabilizer. Restricting that isotopy to the punctured sphere gives the R³ statement.

This proves the gluing equivalence. It does not decide the product-membership problem from finite generators alone.

## 4. Published hypotheses for the higher-genus subclass

I checked Theorem 2.23 in the complete typeset Baroni paper and inspected its rendered p. 4749. Its requirements match the candidate: an irreducible sufficiently large pair (M,R), no disk component of R, and an annular, possibly empty, complementary boundary. Its output is a finite union **Tf**, with the finite representative on the right, exactly as used in the submission.

The additional disjointness conclusion requires each characteristic I-bundle to be a product over a sphere with zero through three holes, or the orientable twisted I-bundle over a projective plane with zero through two holes. These are precisely the listed small-I-bundle cases. Without that extra assumption, only each generator's own pair is guaranteed disjoint.

For a connected embedded positive-genus surface, each complementary closure is irreducible: a sphere in one side bounds two balls in S³, and connectedness puts the original surface wholly on one side of that sphere. The other ball lies in the chosen complementary closure. On the boundary-irreducible side, a pushed-in boundary component is a two-sided incompressible positive-genus surface, establishing the sufficiently-large requirement. Taking R=∂M leaves an empty complementary boundary and no disk components. No omitted hypothesis is being obtained from a genus-two-only argument.

The handlebody side is boundary compressible and the other side is boundary irreducible, so an ambient equivalence cannot interchange them. Checking the recorded infinity location under this forced matching is necessary and correct.

## 5. The terminating algorithm is a credited consequence

Baroni's Theorem 1.4 supplies the oriented boundary-pattern homeomorphism decision used with empty pattern on the irreducible, boundary-incompressible side. The paper explicitly explains the orientation-preserving refinement. Once existence is decided, enumerating subdivisions and simplicial maps constructs a homeomorphism; for a promised pair of handlebodies, the analogous effective search terminates as well.

Under the small-I-bundle hypothesis, all the returned twist curves are pairwise disjoint. Their twists commute, so every element of T is exactly a finite product with one integer exponent per paired generator. For each representative f, the candidate asks whether D(h)fc extends over the handlebody. This is the direct input of Corollary 3.5.

I visually inspected published p. 4766 to resolve the inequality in its genus bound: it says **g≥1**, not merely genus two. The corollary explicitly allows m=0. Its paired exponents have the stated opposite signs; reversing all surface-orientation conventions just replaces h by −h, with no change to existential feasibility. Neither parallel curve classes nor dependent twists require unique exponent vectors, only that every element has a vector representation.

The imported extension algorithm tests the images of a complete meridian system in the **free fundamental group**. Theorem 3.4 supplies a finite semilinear description of the integer exponents for which fixed products of powers are trivial, and Corollary 3.5 imposes the shared exponent and sign constraints by integer linear feasibility. This yields terminating yes/no tests in arbitrary handlebody genus for the particular disjoint-multitwist problem. The finite number of representatives then gives termination of the stated subclass algorithm.

The general geometric algorithms are credited dependencies, not implementations provided by this package. The audit checks the applicability and reduction; it does not claim to independently redo every JSJ and free-group argument in the published paper.

## 6. Failure of the unrestricted shortcut

For the displayed punctured-torus matrices,

    P Q P⁻¹ = [[0,1],[-1,2]],
    P^m Q^n = [[1−mn,m],[-n,1]].

The lower-right entry excludes equality for every pair of integers m,n, not just the finite pairs tested by code. Consequently an arbitrary word in two intersecting-curve twists cannot be represented by the fixed two-block exponent pattern. On the doubled punctured torus, each paired generator has disjoint curves within its own pair, but its restriction to the first half still gives P or Q, so the same obstruction survives there.

The candidate makes no unsupported assertion that this doubled example is realized as the characteristic decomposition of a particular embedded complement. It is a diagnostic against a proposed algebraic shortcut. Likewise, a commutator can be nontrivial in a free group while having zero exponent sums, so replacing the handlebody extension word tests by homology would be invalid.

The full problem also includes complementary pieces beyond the promised handlebody/boundary-irreducible subclass and disconnected configurations. Neither the complete invariant of diagrams of groups nor a positive search through longer words supplies a termination certificate for all negative instances. These gaps remain explicit.

## 7. Checks and publication scope

All **4,238 author assertions** replayed byte-identically. The receipt SHA-256 is `0b40f8b77fae3d84866e4b9dc14b08de0ce7da7ac688b368114e53a6010421d5`.

A separately written checker passes **55,932 independent exact assertions**. It checks all 30 subgroups of S₄ for the product/coset condition, catches the AB-versus-BA distinction, tests reference-map changes, evaluates signed matrix identities without a symbolic-matrix library, checks free-word commutators and the trefoil quotient, and verifies the commuting-power/orientation conventions.

These controls do not triangulate embedded surfaces, compute a JSJ decomposition, construct an ambient isotopy, or implement the imported full algorithms. The proved scope is the source-qualified, credited subclass and the exact gluing/shortcut diagnostics. Preserve **unsolved, 1/5**, all point-at-infinity and orientation qualifications, and the absence of a novelty or undecidability claim.
