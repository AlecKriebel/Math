# Independent audit: KP-4.84 / problem 2960

Audit date: 8 October 2026.

## Decision

**Accept the mathematical report as a partial, unresolved result with five mathematical approaches. Correct the executable-checker interface and optimization behavior before treating it as a robust reproducibility artifact.** No mathematical correction to the report is required by this audit. No complete solution, universal negative theorem, or new literature-exhaustiveness conclusion has been established.

The audited input is the packet whose `MANIFEST.sha256.json` has SHA-256 `3308459e594672876a4953fac77a08719bb4cd52f13e3992a54600fff5904a5b`. All six manifest entries match their recorded byte counts and hashes. The original report, checker, result JSON, source metadata, ledger, README, and manifest are preserved unchanged. A separate hardening patch and full patched checker accompany this audit.

The most important acceptance boundary is intact: realizing a homology quotient, a topological mapping class, a standard subgroup, or a homotopy-coherent action does not generally realize a prescribed finite subgroup of the full smooth mapping class group. The strongest constructive conclusion remains the standard product-and-factor-swap subgroup theorem. The missing smooth-kernel and finite-complement arguments remain missing.

## 1. Target and quantifiers

The actual preliminary K3 problem list, printed and PDF page 259, was independently visually inspected using the existing page image, and the same page was freshly text-extracted from the hash-verified PDF. Problem 4.84 concerns the smooth quotient `Diff+(X) -> pi0 Diff+(X)` and a group-theoretic section over each prescribed finite subgroup. The manifold is existentially quantified; the subgroup is universally quantified. The report neither reverses those quantifiers nor replaces a section over each finite subgroup by one simultaneous section over the whole mapping class group. The [primary problem-list PDF](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) remains the correct source; the [AIM document](https://aimath.org/pastworkshops/kirbylistrep.pdf) was independently opened and is a four-page workshop summary.

The section equation implies injectivity and thus an effective action. The source imposes no simply-connected or symplectic condition. A torsion-free smooth mapping class group would suffice, but no candidate is proved to have one. Restricting a disconnected witness to one connected component is valid: an isotopy cannot change a component permutation, and an identity-extended component subgroup therefore has a section preserving every component. Restriction returns exactly the original component mapping classes. The report explicitly excludes an empty-manifold loophole.

## 2. Rational candidate, averaging, and the algebraic obstruction

### CP2 criterion

Complex conjugation on CP2 has real orientation sign `(-1)^2=+1`, changes the generator of second homology by a minus sign, and is an actual involution. It therefore splits the homological sign quotient of the smooth mapping class group. This does not compute its kernel.

The formulas `(k c)^2=k sigma(k)` and `h c h^-1=h sigma(h)^-1 c` have the correct multiplication order. If the kernel is torsion-free, every finite subgroup injects into the sign quotient and consequently has order at most two. Triviality of the nonabelian first-cohomology pointed set then conjugates every nontrivial finite subgroup to the standard complement. Choosing any diffeomorphism in the conjugating mapping class realizes that particular subgroup. Both extra hypotheses are genuinely additional; the report neither proves them nor calls complement conjugacy necessary.

### Rational averaging

For a finite subgroup of `V semidirect A`, torsion-freeness of the rational vector group makes projection injective. Its graph is a one-cocycle. The displayed average has the correct sign: `a v = v-z(a)`, hence `z(a)=v-a v`. Conjugation by `(v,1)` produces the graph subgroup. Surjectivity of the abstract map `D -> M` supplies a conjugating lift; no further lift coherence is required. An additive automorphism of a rational vector space is automatically rational-linear, so the action respects division by the finite group order. The assertion is sufficient and conditional, exactly as stated.

### Countermodel

The map `alpha(n,z)=(-n,z+n mod 2)` is additive and has square equal to the identity. Its semidirect product is therefore an actual group, rather than merely an associative finite sample. Projection deleting the central binary coordinate is a surjective homomorphism. A reflection with integer coordinate `n` has every lift square to `(0,n mod 2,0)`. In particular, the standard even reflection lifts to an involution, whereas the two lifts of the indicated odd reflection have order four. This proves the advertised logical counterexample without suggesting that this abstract group extension is a diffeomorphism extension. The finite associativity tests support the formula but are not its proof.

## 3. The torus

The linear map associated with an integral determinant-one matrix is an orientation-preserving torus diffeomorphism, and matrix multiplication gives an exact section for the linear subgroup. Its action on first homology proves injectivity into smooth mapping classes. For a diffeomorphism of a torus, the degree is the determinant of its action on first homology, so the orientation-preserving homology image is indeed contained in `SL(4,Z)`. The displayed linear construction makes that map surjective.

The matrix has order five and determinant one. Independently computed column-vector iterates give the displayed Gram matrix, which is `10 I - 2 J`; its eigenvalues are `2,10,10,10` and its determinant is 2000. Finite averaging gives a positive-definite invariant form by right multiplication of the finite group index. The 192 signed determinant-one permutations form the stated finite subgroup.

The path of translations is a smooth isotopy. Thus passing from linear to affine actions adds no smooth mapping classes outside the standard subgroup. Conjugating an already realized subgroup by a representative diffeomorphism realizes its prescribed conjugate. None of these facts handles arbitrary finite subgroups intersecting the torus kernel or nonstandard complements; this gap is correctly retained.

## 4. Product surfaces and swaps

The standard product homomorphism is well defined on isotopy classes. A swap cannot be isotopic to the identity because it interchanges the distinct first-homology summands. In the unswapped case, an inner automorphism of the product fundamental group restricts to inner automorphisms of its two factors. The extended Dehn–Nielsen–Baer identification then proves that both surface classes are trivial. This proves injectivity without classifying diffeomorphisms of the four-dimensional product.

The source hypothesis needed for the realization step was checked particularly carefully. Kerckhoff's introductory page explicitly includes orientation-reversing surface classes, states the isometric realization theorem for finite subgroups, and identifies the extended group with the relevant outer automorphism group. The existing scan of printed page 235 / PDF page 2 was independently visually inspected. The [Annals record](https://annals.math.princeton.edu/1983/117-2/p02) verifies the 1983 volume and pages. Thus the theorem is not being applied only to an orientation-preserving surface group while silently allowing orientation reversals.

For a finite swapped subgroup, normality of its unswapped part gives `a B2 a^-1=B1`. Squaring the chosen swapped element puts `ab` in `B1`. Conjugating by `(1,a)` consequently sends the unswapped subgroup into `B1 x B1` and the swapped representative to `(1,ab) tau`. The two-coset decomposition completes the containment proof. There is no requirement that all original coordinate entries generate a finite subgroup. Indeed, for an infinite-order element `a`, the order-two element `(a,a^-1) tau` already shows why that shortcut would fail.

Using one surface realization of `B1` on both equal factors makes the swap relation hold exactly. Conjugation back gives the original prescribed mapping classes. Product orientation is the product of the two surface signs; swapping two two-dimensional factors has sign `+1`. Conjugation preserves orientation even if the chosen conjugator reverses it. These points also cover unequal factors and the no-swap case under the stated genus bounds.

An independent implementation represents the wreath product as permutations of six points rather than importing the original triple multiplication. It finds all 112 subgroups, exactly 52 with swaps, and verifies the conjugation containment for all 228 possible choices of a swapped representative across those subgroups. These finite computations corroborate a valid general proof. They do not promote the standard subgroup to the whole smooth mapping class group.

## 5. Metric criterion

The identity component is normal, so inverse pullback defines the asserted quotient action. Averaging over an actual finite action gives an invariant positive-definite metric. Conversely, a section of the isometry stabilizer extension is already a realization. Fixedness of the metric orbit supplies an isometric representative in every prescribed component: if `f* h=d* h` with `d` identity-isotopic, then `f d^-1` preserves `h`. This proves the required surjectivity and identifies the kernel as stated.

The two conditions are not being conflated. A trivial identity-isotopic isometry kernel would make splitting automatic, but that condition is not proved for a selected candidate. In the unit-quaternion model, every `j z` in the nonidentity component of Pin(2) has square `-1`, so its component extension has no section. This is a valid abstract warning, not a claim that the extension occurs on a four-manifold. The report's averaging objection is also correct: arbitrary component representatives need not form the finite group whose multiplication is required to reindex the metric sum.

## 6. Fixed points and tangent representations

For a finite smooth p-group action on a compact manifold, a finite equivariant triangulation followed by barycentric subdivision has no simplex inversions. Nonfixed simplex orbits have size divisible by p. Fixed simplices form a subcomplex triangulating the common fixed set. Alternating simplex counts therefore yield the Euler-characteristic congruence. Compactness supplies finiteness. This use of Illman's theorem is appropriate to finite smooth group actions.

The original Illman full text was **not newly inspected** in this audit. Its bibliographic identity was independently found in the [EuDML record](https://eudml.org/doc/163108); direct retrieval returned 403, and the DOI route did not produce accessible full text. The report's metadata already discloses precisely this limitation. The classical equivariant-triangulation theorem remains an explicitly identified external input; no proof or full-source reinspection is claimed here.

If p does not divide the Euler characteristic, the common fixed set cannot be empty. Averaging a metric over the realized action and differentiating at such a point yields a representation in SO(4). An isometry with fixed point and identity derivative is the identity on the connected manifold, so effectiveness makes this representation faithful.

Commuting orthogonal involutions are simultaneously diagonalizable; determinant one leaves three independent signs. For odd p, nontrivial real irreducibles of an elementary abelian p-group are two-dimensional character pairs, so four real dimensions allow at most two independent nontrivial characters. Both bounds are sharp as representation bounds, witnessed by determinant-one diagonal signs and two independent rotation planes. The independent finite calculation checks binary character systems and rank-three character pairs for p=3 and p=5; the all-prime assertion rests on the representation-theoretic proof.

The Baraglia application really uses a smooth mapping-class-level splitting. Odd `n>=5` gives Euler characteristic `n+2` prime to two and a rank-n sign subgroup, hence a valid restricted obstruction. It is explicitly weaker than already-known results. The local-support periodicity lemma is correct and is not improperly transferred to finite-order mapping classes. No argument covers all four-manifolds, especially the Euler-zero case.

## 7. Source distinctions and provenance

All seven locally hashed PDFs match the original metadata in both size and SHA-256. The five modern research PDFs were freshly text-extracted from those verified bytes and the relevant introductions, definitions, and theorem statements checked. This is independent inspection of existing primary-source copies, not a claim of fresh network retrieval of each PDF. Public web records were separately checked for dates and status.

- [Lee, arXiv v2](https://arxiv.org/abs/2112.13500v2): Proposition 3.1 addresses the topological mapping class quotient and smooth representatives for the indicated three manifolds. The June 2023 version is correctly identified. It supplies no unknown smooth-kernel computation.
- [Baraglia](https://arxiv.org/abs/2310.18819): Theorem 1.4 gives the smooth mapping-class-level homology-image splitting for positive projective connected sums. Theorem 1.6 concerns the specified simply-connected connected sums with at least four signed projective summands. The current arXiv record independently confirms Algebraic & Geometric Topology 26 (2026), 1635–1653 and DOI 10.2140/agt.2026.26.1635. The publisher PDF was not audited.
- [Lee–Lewis–Raman](https://arxiv.org/abs/2504.17235v1): The quotient is topological. Theorem 1.1 requires `3<=n<=7`, a finite-order irreducible element in the specified index-two subgroup, and rank-one invariant second homology. The report appropriately describes a restricted cyclic theorem, not all smooth finite subgroups.
- [Pesikoff](https://arxiv.org/abs/2605.27537v1): The May 2026 manuscript studies homological realization and explicitly distinguishes mapping-class splitting from periodic representatives. Its positive constructions and negative results do not settle the existential target.
- [Lin–Sha](https://arxiv.org/abs/2606.24482): The current record confirms v2 dated 26 August 2026. Definition 1.3, Theorems 1.4 and 1.6, and Corollary 1.7 match the report's discussion. K3-type includes the stated Betti numbers and unique spin SpinC structure. The neck-twist theorem is conditional on a genuinely order-two mapping class; the non-kinetic corollary additionally requires simply-connected spin and nonzero signature. The report invokes the specified hypotheses rather than extending them to arbitrary manifolds.

The two public dataset files were independently rehashed: both original hashes and byte counts match. Numeric problem ID 2960 has exactly one match, its problem number is KP-4.84, the canonical statement hash matches, and the exact research-results key is absent. No dataset rows or source bodies are included in this audit. This verifies identity and provenance, not the truth of every dataset assertion.

The bounded current search found no contrary resolution and reidentified the primary problem-list question. This is not an exhaustive novelty check. Version, publication status, and inspection depth remain separate claims.

## 8. Reproducibility defects and separate patch

The original checker has **17** `assert` statements. Python removes them under both `-O` and `-OO`. Its final result still labels the run PASS. It also always rewrites `EXACT_CHECKS.json` beside the script, so the advertised command fails on a genuinely read-only copy even when its mathematics is correct.

All tests here ran with real and effective UID 1000, not as root. Read-only directories were mode 0555, files mode 0444, and both attempted file creation and modification were verified to raise PermissionError before testing. A writable clone reproduces the frozen JSON byte-for-byte in normal, `-O`, and `-OO` modes. The original read-only clone fails in all three modes at the attempted output write.

Four substantive mutations were tested: corrupting the order-five matrix, removing the countermodel's twisting term, using the wrong wreath conjugator, and replacing the determinant-one sign subgroup by the determinant-minus-one coset. The original normal run rejects all four. Each optimized original run wrongly returns PASS for all four; three corruptions even reproduce the original result JSON byte-for-byte.

The separate patch:

1. replaces all 17 removable assertions with explicit runtime guards;
2. checks the displayed Gram matrix/determinant and subgroup enumeration counts explicitly;
3. emits JSON to stdout by default, with optional `--output PATH` for deliberate writing.

The hardened checker has no removable assertions. It returns byte-identical frozen JSON from read-only copies in all three modes, rejects all twelve mutation/mode combinations, and successfully writes a requested external output while executing from the read-only copy under `-OO`. The patch leaves the mathematical algorithms and result schema unchanged. The frozen original is not rewritten.

`REPRODUCTION.json` records 36 primary runs plus the explicit-output test. `reproduce_checks.py` recreates them in a caller-specified new work directory. `independent_checks.py` and `INDEPENDENT_CHECKS.json` provide distinct exact computations for the matrix, rational averaging, countermodel, wreath lemma, and character bounds. These tests remain bounded algebraic checks, not solutions of smooth isotopy problems.

## 9. Final disposition

Accept the authored proofs, source distinctions, five-approach ledger, and unresolved classification. Carry the separate checker hardening into any successor packet, regenerate its own manifest after deliberate integration, and retain the original input hash as provenance. Existing source-access limitations must remain disclosed. The audit adds zero mathematical attempts and authorizes no global queue edits or publication by itself.
