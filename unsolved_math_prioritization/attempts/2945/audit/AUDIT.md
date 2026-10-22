# Independent mathematical audit: KP-4.69 / problem 2945

Audit date: 8 October 2026.

## Disposition

**Accept the frozen candidate as five completed partial mathematical approaches, with the original existence question unresolved. No candidate correction is required.**

The strongest conclusion, Theorem 6.3, survives the relative-boundary audit: the named Friedman–Witt–Kwasik–Schultz endpoint has a topological cylinder representative of zero Casson–Sullivan class, and its prescribed boundary map extends diffeomorphically over a finite interior stabilization of the cylinder. The proof does not produce an unstabilized cylinder diffeomorphism. In particular, this acceptance does not certify a solution, an example separating the two endpoint images, or novelty.

The original eight public files were read, and all their frozen byte counts and hashes match. The original frozen manifest is unchanged. Its SHA-256 is

`5ca5ea8c8f68876e60dbc5d576ff1cd4415adf22761ea2fcf1969cbdc428c901`.

The candidate tree SHA-256 is

`9373856af6e529c088f6df98cc42e147f3b8730e00494a90af7781e62d90cf83`.

Here the tree hash is SHA-256 of the frozen `files` array serialized as UTF-8 JSON with sorted object keys and separators `(',', ':')`, with no trailing newline. A separately pinned authored audit accompanies the unchanged candidate. No original candidate file, global queue, remote repository, or publication state was changed by this audit.

## 1. Statement and source boundaries

The printed 2026 K3 author-manuscript statement, pp. 247–248, asks about a diffeomorphism of a closed 3-manifold. The interpolating object is a self-homeomorphism or self-diffeomorphism of its 4-dimensional cylinder, with the bottom fixed and the prescribed diffeomorphism on the top. It need not preserve levels. This distinction is maintained throughout the candidate.

The original question does not require connectedness or orientability. The candidate explicitly confines its attempts to connected oriented test examples without claiming to exclude the other cases. A cylinder automorphism fixed on the bottom preserves each cylinder component. Projection onto the 3-manifold yields a homotopy of its endpoint to the identity. The candidate's component and orientation observations are therefore correct.

The K3 marked-embedding reformulation is also faithfully identified. Parametrized embeddings, rather than their identical underlying middle-fiber images, are essential. No argument in the candidate replaces the parametrized condition by an unparametrized one.

The topological pseudo-isotopy and ordinary non-isotopy of the chosen separating twist are imported results. Galvin's thesis, Theorem 9.2.6, identifies precisely the metacyclic-prism family used in the candidate; Question 9.2.8 isolates its smooth pseudo-isotopy problem. The original Friedman–Witt paper was inspected, but the original Kwasik–Schultz full text was not available and was not independently proof-audited here. The report discloses that limitation and correctly uses K3 and the thesis as the identified supporting sources. The broad modern formulation is not misattributed solely to the narrower original 1986 argument.

The term “metacyclic prism” is fixed by the report's own explicit convention: the 3-manifold is spherical and oriented, and its group is nonabelian with cyclic Sylow 2-subgroup. This is enough for the application. No claim that an arbitrary finite group satisfying only that group-theoretic condition necessarily acts freely on the 3-sphere is needed.

Public source references: [K3 author manuscript](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), [Galvin thesis](https://theses.gla.ac.uk/84595/1/2024GalvinPhD.pdf), [Friedman–Witt](https://www.maths.gla.ac.uk/~mpowell/Friedman-Witt-Homotopy-is-not-isotopy-homeos-3-mflds.pdf), [Kwasik–Schultz bibliographic record](https://doi.org/10.1016/0040-9383(95)00017-8).

## 2. Priority audit: relative Casson–Sullivan realization

### 2.1. Version, category, and dimensions

The source used for the current argument is Galvin's arXiv:2405.07928v2, dated 9 July 2026. A fresh public arXiv metadata check confirms that it is the final author version designated to appear in Compositio Mathematica. Its locally inspected PDF has 43 pages, 767268 bytes, and SHA-256

`a7e90dc2a28c1b6681638d724f260adf268514d77f8264ef53a89c604ef5a5a0`.

The older author-site PDF is separately identified and is not used for the final theorem numbering. Relevant passages were read in extracted text, and printed pages 13 and 28–30 were also inspected as rendered pages.

The geometry has three different dimensions that must not be conflated:

1. The endpoint manifold M has dimension 3.
2. The cylinder X and each supported realization region Z have dimension 4.
3. The surgery and pseudo-smoothing arguments concern 5-dimensional cobordisms of those 4-manifolds.

The realization step is topological relative surgery followed by a topological relative product identification. It is not an invocation of a smooth 4-dimensional s-cobordism theorem. The later smooth conclusion is obtained only after the explicit interior stabilizations allowed by Proposition 2.27.

### 2.2. The finite-group hypothesis really applies to the pieces

Let P be a punctured spherical factor Y, and let Z be the corner-rounded product P times a closed subinterval lying strictly inside the cylinder interval. Then Z is compact, connected, smooth, and oriented. Removing the ball and taking the interval product do not change its fundamental group, so its group is the finite group of Y.

The group is good in the topological 4-manifold sense because it is finite. Its cyclic Sylow 2-subgroup has vanishing SK1, which is the alternative hypothesis used by Galvin's Proposition 4.13. Thus the surgery obstruction of a normal invariant with zero degree-two coordinate vanishes. For a desired relative Casson–Sullivan class, the degree-four integral normal coordinate can be chosen to reduce to its suspended mod-2 class. The necessary integral-to-mod-2 reduction is surjective: the next Bockstein term maps by multiplication by two on the top relative integral cohomology of the connected oriented 5-manifold, which is torsion free.

This argument never applies the good-group theorem to the free product of the two finite factors. In particular, the finite-cover calculation elsewhere in the report is not being used as a substitute for a missing ambient good-group hypothesis.

There are small notational inconsistencies within the source: Definition 4.11 and introductory text in Section 4.4 say “closed”, while Theorem 1.7, Proposition 4.10, and Proposition 4.13 explicitly state compact hypotheses and use relative groups. Some displayed arguments also suppress relative notation. The relevant proof can be carried out with the full boundary pair, as above. Consequently the present application is justified by the relative construction, not by silently treating “closed” and “compact” as interchangeable. The reversed inequality printed in the instability sentence after the Steenrod-square diagram in Lemma 4.9 is another source typographical issue: the required fact is the usual vanishing of Sq² on degree-one classes, including the relative suspension version. For the realization classes used here, the degree-two normal coordinate is zero in any event.

### 2.3. Boundary-fixed realization is stronger than merely boundary-smooth realization

This is the decisive source check. The bare statement of Theorem 1.7 does not spell out “identity on the boundary.” That property must be extracted from the relative construction in Proposition 4.10. The candidate does this, and the extraction is valid.

Here is a precise marking argument. Give the produced 5-dimensional cobordism N its boundary marking into the boundary of Z times an interval. Write its incoming, lateral, and outgoing parts as N+, N0, and N−. The lateral part is identified, using that marking, with the boundary of N+ times the interval. The relative product homeomorphism fixes both N+ and this marked lateral product. After identifying N+ with Z by its incoming marking, obtain a product identification P from N to Z times the interval which agrees with the original boundary marking on N+ and N0.

Let q− be the outgoing boundary marking, and let P− be the restriction of P to N−. The induced endpoint self-homeomorphism is P− composed with the inverse of q−, up to choosing the reverse mapping-cylinder convention. On the boundary of Z, P− and q− agree because both are restrictions of the already fixed lateral marking. Their composite is therefore the identity on the boundary of Z. Either convention has the same boundary-fixed conclusion.

Topological collar uniqueness then changes this map, through a boundary-relative isotopy, to one which is the identity near the boundary. Its relative Casson–Sullivan class is unchanged. This gives exactly the form needed to extend by the identity into X. Merely knowing that the boundary restriction was some diffeomorphism would not have sufficed; the proof supplies the stronger statement.

### 2.4. Supported realization and extension by zero

For a codimension-zero region Z in the interior of X, let C be the closure of its complement. A self-homeomorphism supported away from the boundary of Z has identical source and pulled-back smooth reductions on a neighborhood of C. Its difference class is therefore defined first relative to C. Excision identifies this supported difference class with the relative class on Z. The map of pairs from the boundary pair of X to the complement pair then carries it to the ordinary relative class on X.

Equivalently, collapse C to a point and use the quotient identified with Z modulo its boundary. This yields the extension-by-zero homomorphism from H³(Z, boundary Z; F2) into H³(X, boundary X; F2). This is a cohomology map with support, not the ordinary restriction map in the opposite direction.

Poincaré–Lefschetz duality converts this supported map into the inclusion on H1. For the two disjoint punctured factors, the direct sum of these H1 maps is an isomorphism onto H1(M times I; F2). This is the usual connected-sum H1 decomposition; the interval and corner rounding add no H1. Hence the two supported realization families span every ambient relative degree-three class. No cohomology class in the neck is missing.

This locality argument uses the stable smoothing-difference definition of the invariant. It does not assume that an arbitrary ordinary cohomology restriction would be surjective, and it does not confuse absolute H³ with the required relative group. For the concrete Dic_3 pair the latter group has two mod-2 coordinates, consistently with the independent arithmetic.

### 2.5. Composition and the fixed-end coset

Let h be identity on a neighborhood of the entire boundary of X. Its restriction to the bottom copy of M is the identity, and that inclusion is a homotopy equivalence. Thus h induces the identity on H1(X; F2). For a manifold self-homeomorphism, duality relates pullback of a relative cohomology class to the inverse pushforward of its dual homology class. Since this pushforward is already the identity, h acts trivially on the relative degree-three group.

The Casson–Sullivan composition rule, with the composition order used in the candidate, is

`cs(F composed with h) = cs(h) + h* cs(F)`.

The right-hand pullback is by h, not by F. It therefore drops out in this cylinder setting. The formula is valid even when F has the nonidentity prescribed smooth map on the top: all three stable reductions agree on the specified smooth boundary data, and their difference classes obey the same torsor addition rule relative to that boundary. The proof does not require F to be boundary-fixed.

The image of the boundary-fixed group under cs is consequently a subgroup. Any other map with the same straightened boundary collars differs from F by such an h, so its class lies in exactly the stated coset. Conversely each element of the subgroup is attained by composition. By the supported realization calculation this subgroup is the whole obstruction group. Choosing cs(h) equal to cs(F) cancels the class because the coefficient field has characteristic two. Both original endpoint maps remain exactly as prescribed.

The independent arithmetic includes two safeguards illustrating why the geometric hypotheses matter: a proper one-coordinate realization subgroup cannot cancel the other coordinate, and an artificial coordinate-swapping pullback would invalidate naive equal-class cancellation. Neither computation proves the geometric hypotheses; the preceding proof does.

### 2.6. Stable smoothing does preserve the endpoint map

Galvin's Definition 2.20 fixes the prescribed boundary map throughout a pseudo-isotopy between boundary-smooth homeomorphisms of 4-manifolds. Proposition 2.27 uses that convention. Its construction begins with the 5-dimensional mapping cylinder carrying the fixed lateral smooth product; stabilizations and handle modifications occur away from that lateral boundary. The resulting smooth map therefore has the original restrictions on every boundary component.

Applying it to the zero-class F0 gives a diffeomorphism of X with finitely many interior S² times S² connected summands, restricting to the identity on the bottom and the chosen twist on the top. The theorem at this stage requires no good-group hypothesis on X. The surviving conclusion is exactly Theorem 6.3, with some finite nonnegative k and no asserted bound.

For positive k the domain has changed. Its second Betti number has increased by 2k, so it cannot simply be identified with the original cylinder in this rational-homology-sphere test family. Consequently stabilization cannot be discarded by notation, collar straightening, or the identity restriction on the ends. The candidate correctly leaves this as its unresolved step.

Source reference for this section: [Galvin, final v2 manuscript](https://arxiv.org/pdf/2405.07928v2), especially Sections 2.3–2.4 and 4.2–4.4. The marking, support, and composition deductions above are the audit's explicit checks of the candidate's use of that source, not a claim that the cited theorem statement alone contains all these intermediate conclusions.

## 3. Derivative and framing approach

The necessary stabilized-derivative condition is correct. In a product framing of the tangent bundle of X, the derivative of a cylinder diffeomorphism yields a path of matrix maps. At an end, preservation of the boundary gives a block upper-triangular matrix. The normal scalar is positive because the inward half-space is preserved. Contracting the off-diagonal vector and positive scalar gives the claimed stabilized endpoint matrix. This needs no preservation of interval levels.

For a separating sphere twist, the full derivative matrix map is identity outside the neck, for any fixed global tangent framing. It factors through the neck with both boundary spheres collapsed to one basepoint. That quotient has the homotopy type S³ wedge S¹. The induced degree-one mod-2 class pulls back to the dual of the separating sphere, which vanishes. The matrix map therefore lifts to the universal cover of SO(3), after deformation retracting the positive general linear group.

Maps from a connected oriented closed 3-manifold to S³ are classified by degree. The two possible lifts differ by the antipodal map, whose degree is positive one on S³. Thus no sign or order-two ambiguity survives in the integer degree. The square of the twist is isotopic to identity because the square of its rotation loop contracts in SO(3). The derivative chain rule then gives a product of the derivative map and its pullback by the orientation-preserving twist which is null-homotopic. After lifting, degrees add; precomposition by that twist preserves degree. Twice the lifted degree is zero in the integers, so the degree and the derivative class vanish.

Deformation retraction to SO(3) need not be a strict group homomorphism; this is harmless because the product of the two deformation homotopies provides the needed homotopy of matrix products. The lift and degree argument is therefore valid as stated. This null-homotopy supplies formal tangent data only. The candidate does not treat it as an integrable cylinder diffeomorphism.

The supporting derivative and twist-class comparison was checked against [Brendle–Broaddus–Putman, Sections 4–6](https://www.maths.gla.ac.uk/~tbrendle/papers/SplitLaudenbach.pdf).

## 4. Extension over fillings

A collared pseudo-isotopy extends the endpoint over any fixed smooth filling by placing the cylinder map in the boundary collar and using the identity elsewhere. Both the map and its inverse glue smoothly. The inner edge is identity, whereas the outer edge has the prescribed endpoint.

The explicit split-filling map is also valid. On the joining handle D³ times I it rotates the D³ factor according to the defining loop. The loop is stationary near the two attaching ends, so the handle map glues to the identity maps on both filling pieces. The radial action preserves the lateral boundary sphere and gives exactly the desired twist there. Corner smoothing can be done invariantly under these rotations.

Thus every filling with a boundary-connected-sum decomposition matching the chosen neck admits the extension. An arbitrary boundary identification which does not match this splitting is not silently included in that statement. The gluing argument using this extension gives a diffeomorphism between the two capped closed manifolds for any compatible cap. This defeats that particular split-filling obstruction, without proving the stronger extension over a cylinder with the other end fixed.

## 5. Finite covering and loss of equivariance

The free-product projection onto the product of the finite groups has degree equal to the product of their orders. Each punctured factor lifts to copies of its universal cover, a 3-sphere with the relevant number of balls removed. Tracking the two group coordinates gives the complete bipartite graph of pieces and necks described in the candidate.

A spanning tree uses g1+g2−1 edges. Each of the remaining g1*g2−g1−g2+1 edges contributes an S² times S¹ summand. This gives the claimed free rank. For the concrete groups of order 12, the degree is 144 and the number of summands is 121.

The natural lift twists on every lifted neck. Their mod-2 sphere sum is the boundary of the union of pieces from one side of the bipartition, after including half-necks if a literal codimension-zero region is desired. Its homology class is zero. The product lies in the sphere-twist subgroup, and BBP Corollary 5.2 is injective on that subgroup for connected sums of S² times S¹. Hence the lift really is smoothly isotopic to identity, rather than merely having a vanishing detectable class.

The independent graph test uses fundamental rectangular cycles instead of the candidate's bit-matrix elimination. The all-edge cochain pairs evenly with every such cycle. A single edge, and the result of omitting that edge from the full twist collection, pair oddly with some cycle. These are meaningful negative controls against accidentally declaring all sphere-twist products trivial.

The isotopy is not asserted to commute with the deck group. Such an equivariant ordinary isotopy would descend and contradict the imported ordinary non-isotopy downstairs. The candidate correctly distinguishes this from the unresolved possibility of a deck-equivariant pseudo-isotopy.

## 6. Marked mapping tori and invariant calculations

The chosen convention identifies the bottom point x with the top point f(x). It is the inverse of another common mapping-torus convention, so the explicit formulas matter. Under this convention, a collared cylinder map with endpoints identity and f descends to a map from the identity torus to the f torus that fixes the parametrized fiber and preserves its normal coorientation.

Conversely, cutting a diffeomorphism preserving that parametrized cooriented fiber produces a diffeomorphism of the two cut cylinders. The fiber marking determines identity at the bottom. On the opposite boundary, the target point representing the same marked x has coordinate f(x). Therefore the top restriction is f, exactly as claimed. Coorientation prevents the two sides from being interchanged. The same construction works topologically with locally flat fibers and collars.

An arbitrary unmarked diffeomorphism of the closed tori has neither of these controls. The report does not infer a pseudo-isotopy from one.

The imported topological pseudo-isotopy makes the mapping torus homeomorphic to M times a circle. Each spherical factor is a rational homology 3-sphere, and connected sum preserves that rational homology. The rational Betti numbers are therefore 1, 1, 0, 1, 1; Euler characteristic and signature vanish. For the Dic_3 pair the integral first homology of M is two copies of Z/4, while integral second homology is zero. The integral Künneth calculation then gives exactly the five groups listed in the candidate. In particular, the torsion in degree two of the product comes from H1(M) tensor H1(S¹); it is not a spurious Tor term or a free intersection-form contribution.

## 7. Exact execution, controls, and reproducibility

The execution record contains 36 subprocess runs. All ran with UID and effective UID exactly 1000. The working copies had directory permissions 0555 and file permissions 0444. Actual attempts to open an existing file for writing and to create a new file were denied. The original supplied candidate was not chmodded, edited, or used as a mutation target. Bytecode output was disabled and the temporary inputs were verified unchanged after every run.

In each of normal, -O, and -OO Python:

- The original checker completed and reproduced the saved EXACT_CHECKS.json byte for byte.
- A separately implemented checker completed with identical results across optimization modes.
- Ten invalid mathematical controls were rejected by explicit RuntimeError, not by syntax errors, missing files, or optimization-disabled assertions.

The independent group implementation uses 2-by-2 matrices over the exact ring Z[zeta_6], with zeta_6 squared equal to zeta_6 minus one. It generates the twelve matrix elements, checks all 144 normal-form products against that representation, constructs the commutator subgroup, and independently confirms the cyclic order-four quotient and Sylow subgroup. It uses no floating-point trigonometric approximation.

The ten mutations test the x-square relation, conjugation, derived subgroup, Smith invariant, missing twist in the all-edge cancellation, false single-edge cancellation, incorrect cover rank, incorrect Künneth input, a noncancelling obstruction operation, and an explicit false acceptance predicate. All 30 mutation runs fail for their intended mathematical check. Neither the candidate nor independent checker contains an AST Assert node.

The original exact checker is an arithmetic verifier, not a manifest verifier. Running it alone does not promise to detect an altered prose report or changed saved output. The audit harness separately enforces the external frozen-manifest hash, reconstructs the tree hash, verifies every public filename, length, and digest, and then compares the computed output bytes. This separation is disclosed rather than silently attributing bundle-integrity guarantees to the original script.

To rerun from an ordinary UID-1000 account:

`python -B reproduce_audit.py /path/to/pseudoisotopy_2945 /path/to/new_execution_audit.json`

The sibling independent_checks.py file must accompany the harness. The supplied candidate must include its unchanged CANDIDATE_FREEZE.json and public directory. No private source text or network access is needed for these arithmetic reproductions.

## 8. Source pins, approach count, and acceptance boundary

All nine locally available PDFs listed with byte counts in the candidate source manifest were independently rehashed and matched. SOURCE_AUDIT.json records their public titles, URLs, sizes, hashes, and the bounded metadata checks. The unavailable original KS96 paper and abstract-only screening of OPRW25 remain explicitly outside full-text proof verification.

The corpus's two file hashes and byte counts were independently reproduced. Exactly one problem record matched numerical ID 2945 and its problem number KP-4.69. Its canonical record hash matched the candidate. The two candidate research lookup keys were absent, and a nested identity scan found no matching research entry. Only verification metadata is included in the public audit; no dataset contents are copied.

The five mathematical approaches are genuinely distinct: derivative/framing data, extension over fillings, finite-cover lifting, marked mapping tori, and relative smoothing obstruction. Each establishes the stated partial result or reduction. Source normalization, literature search, arithmetic checks, and this audit earn no extra mathematical-approach credit.

The final accepted status is **partial/unresolved, 5/5 approaches completed**. The candidate is accepted unchanged, conditional on its clearly identified external geometric theorems. Neither computation nor source searching proves the absence of later or unindexed solutions. No publication was performed, and no broad claim of exhaustion or novelty is accepted.
