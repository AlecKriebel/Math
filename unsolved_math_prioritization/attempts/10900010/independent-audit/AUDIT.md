# Independent adversarial audit: rank 672, problem 10900010

## Verdict and exact binding

**PASS AS QUALIFIED PARTIAL RESULTS. Retain NO RESOLUTION / unsolved, five approaches completed.** No proof or counterexample to the general fixed-edge-cover question was found. No theorem-breaking error was found in the authored special cases under their stated hypotheses. The arithmetic checks are supporting controls, not a formal verification of the topology.

This audit is bound to the 23,418-byte author archive with SHA-256
`808dd53041a58e139590fd5eb31c85b8667f06637c6995024708256e8eddddce`.
It contains exactly 11 regular file members, all byte-identical to the reviewed author-safe directory. Its manifest SHA-256 is `94868f587e11bc5cf7e275beacd7cdec8beaf6b033dc8d48e557d83e1225559b`; all ten enumerated member hashes and sizes match. The original archive and its files were not modified.

The only proposed clarification is nonblocking: distinguish the action-defined class from a literal assertion of two nonempty end-sides for every edge of a nonminimal tree. A pendant-edge example below makes the distinction explicit. It does not invalidate any partial theorem or produce a negative answer.

## 1. Mathematical review

### The target and its conventions

The source is Agol Question 3.2 in Delp--Hoffoss--Manning, *Problems In Groups, Geometry, and Three-Manifolds*, PDF page 2. The page was checked in text and visually. It selects the class in a covering determined by an edge stabilizer and asks for a minimizing surface embedding downstairs. The packet correctly keeps this upstairs minimization separate from minimizing the pushed-forward class. The short source leaves several manifold and coefficient conventions unstated; the packet's closed, oriented, smooth, integral-homology and inversion-free restrictions are explicit limitations, not claims to settle those omitted cases. [Primary problem](https://arxiv.org/pdf/1512.04620)

A compact representative of an ordinary degree-two homology class is understood here to be a closed oriented surface. The term should not be read as permitting unpaired boundary components. Proper surfaces for a manifold with boundary require a relative class. Noncompact supports or locally finite homology must not be substituted into the proofs.

### Lemma 1: compact descending dual representative and canonical class

The compactness argument is valid with the stated finite-type construction. A finite fundamental collection of lifted simplices meets finitely many points of the midpoint orbit. Translates carrying a fixed such orbit point to the selected midpoint form one left stabilizer coset. Modulo the stabilizer, only finitely many compact pieces remain. This establishes compactness even if the covering has infinitely many sheets or its subgroup is infinitely generated. It does not rely on a compact core.

The coorientation is consistent because no group element reverses the selected edge. The orientation of the base manifold then orients the dual surface. If two selected-level points project to the same point downstairs, their identifying group element fixes the midpoint, hence lies in the edge stabilizer. This proves injective descent; compactness upgrades the local embedding to an embedding. The finite-type equivariant homotopy gives a compact oriented bordism modulo the same subgroup, so the ordinary homology class is independent of the map. Geodesic homotopy stays in a finite subtree over each fundamental simplex after taking finite hulls.

The proof does not imply connectedness, incompressibility, equality of dual trees, or nonzero class for every edge. Reversing the chosen edge orientation reverses the class and leaves the minimum unchanged. Inversions cannot be dismissed by subdivision without tracking the change from setwise to pointwise stabilizers.

### Compression and the pushforward bound

An actual compressing disk downstairs lifts along the prescribed lifted boundary; its interior is disjoint from the whole projected surface. The lifted surgery preserves the upstairs class and the descent property and cannot increase the closed-surface negative Euler complexity. This is correctly used only to remove compressions, not to prove optimality.

For a compact embedded upstairs representative, its covering projection is a compact immersed oriented surface downstairs. The singular/embedded norm inequality yields the lower bound used in Proposition 2. Cooper--Tillmann explicitly apply it on printed page 13, with closed oriented irreducible hypotheses stated earlier. The audit checked those hypotheses and the displayed application. This is sufficient for the covering application. The general map version rests on Gabai's singular-norm theorem as identified by the packet; neither author nor auditor claims to have inspected a readable original Gabai PDF. [Cooper--Tillmann](https://msp.org/pjm/2009/239-1/pjm-v239-n1-p01-p.pdf)

No properness of the covering projection is needed for pushing forward an ordinary finite homology cycle. A taut downstairs surface alone is not enough: one must prove liftability into the prescribed cover and identify the correct sum of lifted classes. The sandwich argument is correct when those data are supplied.

### Theorem 3: translation-line actions

The proof is complete under its stated closed, connected, oriented, irreducible hypotheses. A cooriented embedded representative of the primitive dual class, including a disconnected one, gives a circle-valued map by traversing the circle on each oriented collar and mapping the complement to the basepoint. Its character is the intersection character. No assertion that the map is a fibration is used.

In the kernel cover, the lift changes by exactly one under the positive deck generator. Each point of the downstairs regular fiber has exactly one lift at a specified real level. Thus the chosen level is compact, projects diffeomorphically to the whole downstairs fiber, and has the action-defined class by Lemma 1. This remains true when different components need different choices of lift. The pushforward lower bound and this upper bound agree.

For translation lengths multiplied by a positive integer k, one selected edge orbit still corresponds to the primitive class, not k times that class. There are k edge orbits. A lifted map scaled by k proves the stated extension. The independent controls explicitly test this distinction. Neither orientation-reversing line actions nor branching-tree stabilizers are silently included.

### Proposition 4 and Corollary 5: surface-group certificate

The cup-product proof correctly uses rational coefficients and a nonzero degree. Naturality and the nondegenerate pairing make the pullback on first cohomology injective, forcing the genus of that component to be at least the target genus. A disconnected representative with total degree one has some nonzero-degree component; it need not have a degree-one component. This yields the exact lower bound needed for the primitive surface class, without claiming a linear lower bound for all multiples. The torus case follows just from nonnegativity.

For a closed aspherical base and an embedded, two-sided, oriented, incompressible surface of positive genus, the preferred lift to the exact surface-subgroup cover induces a fundamental-group isomorphism. Both spaces are aspherical CW spaces, so this lift is a homotopy equivalence and has the required homotopy inverse. The selected edge in the geometric Bass--Serre splitting has precisely this lifted surface as its dual level. Asphericity and the exact subgroup hypothesis are sufficient; no homotopy retraction is asserted for arbitrary overgroups.

### Dihedral family and universal-cover obstruction

The diagonal involution in the example is free because the surface involution is free, and it preserves three-dimensional orientation because both factors reverse orientation. The finite cover is aspherical, hence so is the quotient. The regular infinite cover has infinite-dihedral deck group; torsion in that deck group causes no contradiction because the covering space is not simply connected.

Only the identity sends the chosen height 1/2 to itself. The slice therefore descends injectively. Its surface projection gives the degree lower bound, while its downstairs image bounds one side of the interval-valued quotient. Consequently its upstairs norm is positive and its pushed-forward class is zero. This verifies a strict failure of the auxiliary equality, with a descending minimizer visibly present. It is not a counterexample to the target.

Lemma 6's condition involving every group element outside H is equivalent to injective descent. Freeness of the universal deck action gives the needed implication from equality modulo H to equality of deck elements. A normalizer-only check is insufficient for a nonnormal subgroup, including when the quotient deck group is nontrivial. The extended S4 enumeration below tests that stronger hazard.

## 2. Literature scope and current versions

The current arXiv records were independently checked on 2026-10-04: the splitting-complexity paper remains v2 dated 31 August 2026, and the sutured-hierarchy paper remains v2 dated 13 July 2026. No peer-review status is inferred from the arXiv records. Seven local scholarly PDFs also match their recorded public hashes and byte counts.

Jaikin-Zapirain--Kudlinska--Sánchez-Peralta define splitting complexity by taking an infimum over admissible splittings dual to a nonzero character. Corollary 1.5 supplies an optimal such splitting, with its edge group allowed to vary. The statement and proof, including the definition of admissible splitting, were checked; PDF page 3 was also inspected visually. It does not supply a norm-minimizing embedded projection in a previously fixed edge cover. Its own text recognizes an earlier route to the three-manifold case. The packet correctly avoids treating its recent date as a new resolution of Agol's question. [Current splitting-complexity version](https://arxiv.org/abs/2606.31774v2)

Cigna's current manuscript concerns extracting norm information from taut hierarchies in compact manifolds, with the stated orientation, irreducibility and boundary conditions. It does not provide the missing universal translate-disjointness conclusion for a fixed infinite edge cover. The inspected initial theorems and method description support the packet's bounded claim. [Current hierarchy version](https://arxiv.org/abs/2604.19611v2)

Freedman--Hass--Scott's Theorem 5.1 requires a least-area incompressible map homotopic to a two-sided embedding and retains a one-sided double-cover alternative. Theorem 6.2 requires homotopically disjoint maps. These requirements were checked in the primary text. Homological equality alone does not supply them. The packet appropriately does not claim that these theorems, finite-cover embedding, or an arbitrary compact truncation close the gap. [Freedman--Hass--Scott](https://www.math.ucdavis.edu/~hass/Research/Papers/Minimal/FreedmanHassScott82.pdf)

This audit did not reproduce every historical search, independently recount either catalogue corpus, or establish an exhaustive current literature status. NO RESOLUTION describes this investigation, rather than a theorem that no published or unpublished resolution exists.

## 3. Additional adversarial examples

These are checks of hypotheses and failed reductions, not new counterexamples to the target.

1. **Arbitrarily expensive essential dual representatives.** In the product example replace the three affine crossings by 2k+1 alternating crossings. The signed class is still one, every slice is incompressible, and the complexity is 2k+1 times the minimizing slice. Thus incompressibility alone gives no uniform approximation ratio. Twenty such exact controls pass.

2. **Nonprimitive translation lengths.** For a k-scaled line action, the k midpoint-orbit levels in one primitive period each yield one primitive class. Their union yields k times that class. Confusing the union of all orbits with one selected edge changes the problem. Scales 1 through 20 pass.

3. **Reflection vertices and inverted edges.** In the dihedral family, an integer-height slice is preserved by a nontrivial reflection and projects two-to-one onto a one-sided nonorientable surface. A noninteger-height slice has no such isotropy. Replacing the reflection by t↦1−t inverts the integer edge (0,1); its midpoint stabilizer has index two over the pointwise edge stabilizer. Subdivision selects the smaller half-edge stabilizer. The arithmetic checks cover 317 rational heights and the inverting midpoint. This validates the packet's choice of an interior nonreflection level and its inversion exclusion.

4. **Dropping the exact surface subgroup breaks the certificate.** In the same dihedral base, enlarge the subgroup from the surface group to the entire fundamental group. The resulting cover is the identity. The incompressible separating genus-g surface now has class zero, whose norm is zero, although its own negative Euler complexity is 2g−2. Asphericity of the ambient manifold does not fix this. The missing hypothesis is precisely the surface-group homotopy equivalence or an independently verified degree-one retraction.

5. **Boundary is not cosmetic.** In a solid torus, a meridian disk is naturally a generator of relative degree-two homology, whereas absolute degree-two homology is zero. Its lift to D²×R remains a compact proper disk and a relative cycle, not a closed absolute cycle. Thus replacing the packet's closed surfaces by arbitrary proper surfaces without changing coefficients and groups would invalidate the formulation. The packet correctly does not assert that extension.

6. **A nonminimal tree can have a vacuous edge class.** Take a product surface group acting through its circle character on an integer line, and attach one terminal edge equivariantly at every integer vertex. The action has no global fixed point. For a terminal edge, an equivariant map landing on the invariant line avoids its midpoint, so Lemma 1 gives α_e=0. One component of the tree cut has no end at all. Hence fixed-point-free alone does not imply two nonempty end-sides for every selected edge. The action-class version is still defined and has a descending zero-complexity representative. This is a source-convention clarification, not an obstruction to its intended nondegenerate question.

7. **Cup pairing is intentionally weaker than the full mapping-degree inequality.** The same-dimensional rational matrix diag(d,1) on each symplectic block satisfies AᵀJA=dJ for every positive d. Consequently pairing injection alone cannot prove a |d|-scaled genus bound. These matrices are not asserted to come from maps between equal-genus hyperbolic surfaces. The packet uses only the weaker conclusion that it actually proves, which is sufficient for the class at hand.

## 4. Exact reproduction results

The original verifier exits zero and emits 4,145 bytes, byte-for-byte equal to CONTROL_RESULTS.json, SHA-256 `fbf14c00d60c2df0e2eeb08d87b51a62115209b9c3a57057f5f8f0df2af210b2`.

The independent verifier rederives all six control groups without importing or invoking the author's helper functions: direct affine evaluation; fraction-free pairing determinants; symbolic affine group composition; independent one-based permutation/coset enumeration; the absolute-value formula for Euler truncation; and explicit rooted branch enumeration.

Five additional exact control groups pass. Notably, all eight H-invariant S3 subsets were checked, with four normalizer-only false negatives. In S4, H has order two and its normalizer has order four: among all 66 unions of two H-cosets, all fail the full descent model but 60 escape the nontrivial normalizer deck-group test. These remain finite algebraic models, not constructions of manifold counterexamples.

## 5. Packet safety and limitations

The audit supplement contains authored analysis, exact standard-library controls, public-source identification and verification metadata only. It contains no scholarly PDF, extracted scholarly text, source screenshot, catalogue record, dataset content, authentication material, or private coordination file. Its portable verifier needs only the frozen safe author packet and archive. It does not read scholarly inputs or use the network. No remote write, commit, push, publication, or third-party contact was performed.

The five approach categories are substantively distinct and honestly bounded: dual surfaces/compression; pushforward norm and translations; surface-group retraction; least-area/uncrossing; normal/finite-cover/algebraic certificates. The remaining general step is still a norm-preserving choice satisfying every translate-disjointness condition, or a verified example proving such a choice impossible. The audit establishes neither.
