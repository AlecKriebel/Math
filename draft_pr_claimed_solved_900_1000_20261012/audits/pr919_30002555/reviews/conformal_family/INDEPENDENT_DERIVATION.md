# Independent conformal-family derivation

Recorded before 2026-10-15 05:12:03 UTC (the immediately subsequent tool clock reading), before opening the author proof, author source audit, or reviewer verdicts. Inputs read: root charter, identity preflight, exact source record, original snapshot hash table, and this family's assigned question. An initially estimated 05:14 timestamp was corrected to this tool-bounded time; no derivation content changed after opening the proof.

## Exact assertion under test

For an infinite-genus Riemann surface R, the action of Aut_hol(R) should have finite compact-set transporters: for compact C,D, only finitely many f satisfy f(C) intersect D nonempty. A connected compact set K on a surface with precisely three ends can be chosen to meet all of its homeomorphic images. Combining these would force every subgroup of holomorphic automorphisms to be finite. For a translation surface, the FULL inverse image I = D^{-1}(SO(2)) in the affine group is such a subgroup. Thus its derivative image cannot contain an infinite-order rotation. No lift of the abstract derivative group, splitting, or triviality of ker D is required.

## Derivation and adversarial checks

1. Uniformization. The universal conformal cover of R is the sphere, plane, or hyperbolic plane. A nonidentity Möbius transformation of the sphere has a fixed point, so a free deck group there is trivial. A free holomorphic deck transformation of the plane is a translation: z -> az+b has a fixed point if a != 1. A properly discontinuous discrete translation group has rank at most two, yielding plane, cylinder, or torus, of genus at most one. Hence infinite genus forces the hyperbolic cover H.

2. Write R = H/Gamma. Gamma is discrete and torsion free. It is nonabelian: an abelian torsion-free discrete subgroup of PSL(2,R) is trivial or cyclic (commuting nontrivial elements share an axis or parabolic fixed point, and discrete subgroups of the relevant one-parameter group are cyclic). Its quotient has genus zero. This also avoids presuming injectivity of an arbitrary compact subsurface's fundamental group.

3. Every conformal automorphism lifts, and Aut_hol(R) is N(Gamma)/Gamma. Suppose n_i in N(Gamma) tends to the identity. Fix noncommuting gamma,delta in Gamma. Because conjugation is continuous and Gamma is discrete, n_i gamma n_i^{-1}=gamma and n_i delta n_i^{-1}=delta for all sufficiently large i. In PSL(2,R), the centralizer of each nonidentity elliptic, parabolic, or hyperbolic element is abelian and its nonidentity members have the same centralizer. Consequently the intersection of centralizers of noncommuting gamma,delta is trivial. Thus n_i=1 eventually, proving N(Gamma) discrete. This is an identity-neighborhood argument, not an inference that every subgroup of a Lie group is discrete or closed. Closedness follows separately from discreteness as a subgroup, or directly from both conjugation inclusions in the limit.

4. A discrete subgroup of Isom^+(H) has finite compact-set transporters on H. One proof uses the properness of Isom(H) acting on H: moving one point into a bounded set gives bounded translation part and the stabilizer is compact. The transporter of two compact sets is compact in Isom(H), so its intersection with the closed discrete subgroup is finite. This is independent of the original flat metric's completeness.

5. Each compact subset C of H/Gamma has a compact covering lift Ctilde: use finitely many relatively compact evenly covered neighborhoods and local sections, taking finite unions of compact section images. If f(C) intersects D and n is ANY lift of f, some deck translate gamma n sends a point of Ctilde into Dtilde. There are only finitely many possibilities for gamma n, so only finitely many cosets Gamma n, and therefore finitely many f. This handles compact sets which do not themselves admit a single-valued section.

6. On a translation chart z, derivative in SO(2) gives z -> e^{i theta}z+c, holomorphic. This statement applies to every element in I, including every kernel element. If ordinary finite cone points belong to the surface, the local branch coordinate z=w^m gives the unique holomorphic extension across the cone apex. Excluded infinite-angle completion points must stay excluded; they are not manifold points to be filled. The exact source convention must still be checked. No boundary is permitted by the usual translation-surface definition; if the source instead allows boundary or a different underlying surface, that is a potentially material gap.

7. For a surface with exactly three ends, choose connected compact K whose complement has exactly three connected components, each carrying one end. If h(K) were disjoint from K, connectedness puts h(K) in one complementary component. The other two ends remain joined through K in the complement of h(K), contradicting that h(K) has a complement with three components each carrying exactly one end. This mechanism does not apply to one or two ends.

8. The explicit A=(1/5)[[3,-4],[4,3]] preserves the Euclidean norm, so every integral power is noncontracting under either operator-norm or strict norm-shrinking conventions. If A had finite order, lambda=(3+4i)/5 would be a root of unity. Then lambda+lambda^{-1}=6/5 would be a rational algebraic integer, impossible because it is not an integer. This proves infinite order for all nonzero exponents at once.

## Prospective falsification points

- The source might use an underlying object with boundary/nonmanifold points or different end conventions, invalidating step 6 or 7.
- A claim about all subgroups of PSL(2,R) being closed would be false; step 3 requires the normalizer's two noncommuting deck elements.
- A compact lift must be a finite union of section images, not a global section.
- Properness must use the complete hyperbolic metric, not the possibly incomplete flat metric.
- Finite cone-point removal can add planar ends; exact source meaning must be maintained.
- Linear chart conjugacy preserves tameness only if the conical neighborhoods can actually be identified with standard finite/infinite-angle cone models after deformation. A mere bilipschitz assertion is insufficient to prove the translation-structure model, though the exact SO(2) counterexample requires no conjugacy.

Provisional result: the conformal mechanism appears correct, conditional only on ordinary underlying-surface conventions. Completion estimate for this family's bounded audit: 35%; source/proof alignment and explicit dependency checks remain.
