# Independent review of the surface pure braid packet 10400078

## Verdict and disposition

**Scoped PASS. No mandatory mathematical correction was found. Recommend `unsolved`, five substantive author turns used.** The five-turn packet proves its explicitly qualified two-strand statements. It does not settle the full original question across closed surfaces and strand numbers, and it does not determine every convention implicit in the original chord-diagram target.

This is an independent AI mathematical audit, not human peer review, a formal proof certificate, or a historical novelty certification. The review examined all five arguments and their primary dependencies, replayed every author receipt, and implemented separate exact controls. The author proofs were frozen before review and were not edited.

## Exact version reviewed

Repository: `AlecKriebel/Math`; commit `5a285d429b138a8cc43bfcbc3bc6c465bb06e0f7`; folder `problems/10400078_surface_braid_embeddings`.

The final author manifest has SHA-256:

`b76be37580205020aea35dcbd6a888bc18418fb1c5a187116a7a5de80c6b6229`.

All 26 files bound by that manifest match locally. The manifest itself and those 26 files were independently compared with the raw Git blob identities returned for the fixed remote commit: all 27 match. `AUTHOR_BINDING.json` records file sizes, SHA-256 and Git blob identities; `REMOTE_BINDING.json` records the remote check. The five proof hashes are:

- Turn 1: `788286744e54c2bda7503f90a961f62ce640b94c2287ac43184269806bdb996e`
- Turn 2: `fb4f82b0babcda2be73112277155192192009b472da9cf44c5bd95ba715f65da`
- Turn 3: `69bd468b39b7dda787f191b74e28c62d688a491828d7e968b281601f3344df8c`
- Turn 4: `36f97a0c4c21b712b5443a1ea79be0a4d60a96d2a1b5e9875a1ffe8dae434db2`
- Turn 5: `384643d610cfd8e04877f2d7cad65e6bb4b8bcc4378c1c2a657505dc7b8aaa93`

## Source scope and the meaning of the target

The original is Kohno's Problem 3.28, Ohtsuki Section 3.10, printed pp.443–444. I read the section and visually inspected printed p.444. It concerns a closed oriented surface and a rational injective multiplicative homomorphism from its pure braid group to horizontal chord diagrams. The particular question does not explicitly add a completion, a prescribed degree-zero map, or a universal associated-graded isomorphism. Its finite-type context is relevant, but these are different extra conditions. [Original source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

For the packet's standard target, González–Meneses–Paris Section 1.4 gives the labelled generators, the three/four-distinct-strand relations, and the bead actions. At two strands there are no such higher-strand relations, leaving the free associative algebra on the labels. The pure bead group is the product of the two surface groups; the symmetric-group factor belongs to the full braid target and is omitted here. The action is `(a,b)t_gamma(a,b)^(-1)=t_(a gamma b^(-1))`. Proposition 2.2 identifies powers of the kernel ideal with the kernel group's augmentation powers, and Theorem 1.2 supplies separation. Theorem 1.3 supplies a module invariant and a graded algebra isomorphism; it does not assert that the original invariant is an algebra homomorphism. These statements were checked directly. [González–Meneses–Paris](https://arxiv.org/abs/math/0006014)

I also read the published Bellingeri–Funar article, including its full-group theorem, Definition 2.2, and the handle relation in Theorem 2.1. I visually checked that relation on printed p.159. The later Brochier discussion explicitly phrases the cited obstruction for pure groups, but still concerns a universal multiplicative invariant. The packet does not claim that its proper graded injection is the canonical graded isomorphism, extend it to the full braid group, or refute either source. In particular, a linear-functional factorization convention should not silently be equated with an isomorphism onto a specified diagram algebra. Resolving all such conventions is not needed for the scoped theorems and has not been claimed here. [Published Bellingeri–Funar](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/j.crma.2003.11.014.pdf), [Brochier](https://msp.org/agt/2013/13-6/agt-v13-n6-p12-p.pdf)

All 15 locally recorded source-file hashes match the initial and additive source manifests. The source binding file records them. The Lurie lecture's complete primary text was independently read through the web tool, including its cyclic-centralizer proof; there is no claim of a local PDF hash for the unavailable download. No source PDFs or screenshots are part of this public review bundle. The prior-attempt gate records bounded search coverage rather than a proof that no inaccessible attempt exists. The focused review search did not establish a prior resolution of the exact unrestricted bare-injection question.

## Turn 1 audit

The torus difference-coordinate map has the stated continuous inverse, so `P_2(T^2)=Z^2 x F_2`. This supplies the direct product used in both constructions; no nonexistent higher-genus splitting is being assumed.

The Magnus syllable proof is valid. For a nontrivial reduced word with `k` maximal syllables, the selected length-`k` word has `k` nonempty alternating blocks. Omitting a syllable cannot produce that many blocks. Thus every syllable must contribute its linear term, giving the nonzero product of its integer exponents. Negative exponents use formal geometric/binomial series, which exist over the stated rational completion. Every individual word uses finitely many variables and gives finite support in each homogeneous degree.

Diagonal torus beads act trivially on all labels, and they commute with the free-series image. Equality to the identity first determines the diagonal bead and then the free word. This establishes the bare completed group injection.

For the finite-sum algebra, the ordered bead-support leading term is unique and has a nonzero free-algebra coefficient. This proves the domain assertion. Multiplication adds top chord degrees, so a unit has degree zero. The max/min support argument then gives precisely rational scalar monomials as Laurent units. The resulting abelian unit group cannot contain `Z^2 x F_2`. This is a finite-sum obstruction, not a statement about completed units. The collision meridian's first nonzero Magnus term in this first construction has degree two, as stated.

## Turn 2 audit

The sign convention is consistent throughout. Second-strand beads shift labels by the negative displacement. Inverting `(1+t_0)V` puts the inverse series at label `+e_2`, exactly as the downward-edge rule requires. A positive vertical edge receives the negative of its lower endpoint; a downward edge receives the inverse generator with the same geometric lower-endpoint address.

For consecutive vertical letters separated by horizontal letters, free reduction makes the intervening horizontal block a nonzero pure power of `x`, so its column changes. If no horizontal block intervenes, consecutive vertical letters have the same sign. Thus the vertical-label word is already freely reduced. If there are no vertical letters, the final horizontal displacement detects the word. This proves the lattice-path injection for every reduced word, not just the tested range.

Equivariance of the free Magnus substitution follows directly from relabelling variables. The first bead coordinate detects the separate torus factor. The degree-zero term is exactly the original strandwise map. Direct multiplication gives the meridian image `(1+t_(-e_1))(1+t_0)^(-1)` and its difference symbol. The first-order zero-sum condition for the full kernel ideal also follows by grouping the finite group-ring combination by bead support; a fixed bead block has a fixed vertical exponent sum. The normalized map is therefore filtered, and its first graded image cannot contain a single standard chord.

## Turn 3 audit

The proposed grid tree is connected and acyclic: all horizontal lines are joined only through the vertical line at column zero. Its unique finite path to `(i,j)` is `y^j x^i`. Collapsing this tree gives the `r_(i,j)` basis. Direct multiplication verifies `q_(i,j)=r_(i+1,j)r_(i,j)^(-1)`. Both inverse substitutions telescope with the displayed ordering, including negative columns. Every basis change uses finite words, so no unproved infinite Nielsen limit is needed.

The kernel-ideal decomposition is valid as a vector-space decomposition even though the chosen section need not be a group homomorphism. Normality of the kernel permits commuting its augmentation powers past section representatives. When taking a leading degree, section cocycles lie in `1+I` and do not alter that degree. This establishes the stated graded multiplication and justifies using the pure permutation sector of the published filtration result.

For a free group, ordered products of augmentation generators span each graded quotient. Their Magnus images have distinct leading tensor words, proving independence. Hence the augmentation graded algebra is the tensor algebra on the indicated grid-face basis. The map on that basis is the adjacent horizontal difference with the audited sign. Finitely supported adjacent differences are independent on each infinite row; conversely every finitely supported row-sum-zero vector is a finite telescoping sum of them. Tensor powers of this injective map remain injective over the rational field.

It follows that the exact graded image is `T(W_0) rtimes Q[H]`, where `W_0` is rowwise coefficient-sum zero, and that this image is proper already in degree one. Bead translations preserve that subspace. Graded injectivity implies strictness at every finite filtration level. Separation follows from the free-kernel Magnus filtration and the direct coset decomposition (and agrees with the cited separation theorem). Thus the claimed rational group-algebra injection is justified. The proof does not establish a surjective expansion onto the entire target or a completed source-algebra statement with a different bead-support topology.

## Turn 4 audit

For genus at least two, choose the two strand basepoints and their short connecting path compatibly. The unit-tangent map `(p,v) -> (p,exp_p(epsilon v))` then projects strandwise to the diagonal surface-group map. The bundle homotopy sequence gives a surjection onto the surface group, while orientation makes its fiber central. No section of the circle bundle is needed. Its fiber maps to one collision meridian, not merely an unspecified power. The punctured-surface group injects in the two-point configuration group because the base surface has zero second homotopy group, so this meridian is nontrivial.

The published handle relation makes that meridian a commutator of two pure braids: each displayed argument has even/trivial permutation. In fact membership in the pure commutator subgroup would suffice for the scalar-quotient step; the stronger displayed relation is supported by the source.

The surface-group centralizer input is correct. A nontrivial deck transformation is hyperbolic; its commuting orientation-preserving deck transformations form a discrete translation subgroup on the same axis and hence an infinite cyclic group. Its index in the closed surface group is infinite. Thus no nonidentity element has a finite conjugacy class. [Lurie, Lecture 36, Lemma 1](https://math.mit.edu/~lurie/937notes/937Lecture36.pdf)

In every fixed positive degree, diagonal bead conjugation simultaneously conjugates every chord label and both bead coordinates. A finite orbit therefore forces all these coordinates to be the identity. A finite-support invariant coefficient is consequently a scalar multiple of `t_e^d`. Comparing the first nonzero degree of the normalized meridian image is legitimate, since positive-degree corrections to the commuting braid images only contribute in higher degree. The algebra map sending every chord to one commuting variable and every bead to one is defined degreewise and detects that one-dimensional invariant space. It kills commutators, giving the desired contradiction.

Finite homogeneous support and the natural strandwise degree-zero hypothesis are essential. The packet states both. The abelian torus case fails the conjugacy-orbit hypothesis and is properly excluded.

## Turn 5 audit

Boyer–Rolfsen–Wiest Theorem 1.4 applies to the closed oriented surface groups here; its two exceptional surfaces are not among them. A product group inherits a bi-order. The top-support argument for a crossed-product domain uses both left and right invariance of this order, rather than a general torsion-free unit conjecture. The max/min proof that the group-ring units are scalar monomials is valid also for nonabelian bi-ordered groups. [Boyer–Rolfsen–Wiest](https://numdam.org/item/10.5802/aif.2098.pdf)

The unit tangent circle bundle has Euler number `+(2-2g)` or its negative according to orientation. The proof only needs that it is nonzero. The given presentation follows from the two-cell clutching description; the fiber is central. For any map to a surface group, a nontrivial image of the fiber would force the entire tangent-bundle subgroup into its cyclic centralizer. All the handle commutators would then vanish and the Euler relation would make that image torsion, a contradiction. This argument does not require injectivity of the tangent-bundle subgroup in the braid group. Bowden's discussion of the corresponding central extension and fiber class agrees with this use. [Bowden, printed pp.2213–2214](https://msp.org/agt/2011/11-4/agt-v11-n4-p12-p.pdf)

Every degree-zero map to the unit group splits into a scalar character and two group homomorphisms to the surface group. The scalar part kills the meridian because it is a commutator; both coordinate homomorphisms kill it by the Euler argument. Therefore an arbitrary completed meridian image starts with one. For the finite-sum target, there are no higher-degree unit terms at all, proving nonexistence without normalization for all the stated positive-genus two-strand cases.

The strengthened finite-orbit argument also passes. If one projection of the degree-zero tangent-bundle image is nonabelian, each finite-index subgroup of that projection remains nonabelian: otherwise it would be virtually cyclic, and the torsion-free hyperbolic-axis argument makes it cyclic. A normal core fixing a finite monomial orbit has such a nonabelian projection. Its first chord forces the other projection to be its conjugate. Its bead coordinates must then centralize nonabelian groups and hence be trivial; its remaining chord labels must equal the first label. Two possible first labels differ by an element centralizing that same nonabelian projection, so they coincide. Normality makes the whole finite orbit a singleton. A common normal core gives the same uniqueness across two finite orbits. Thus in each positive degree the invariant space is zero or is spanned by one monomial `t_gamma^d`, detected by the scalar quotient. The first-term commutator contradiction follows exactly as claimed. Scalar degree-zero multipliers do not interfere because they cancel under conjugation.

This leaves the case where both coordinate images on the tangent-bundle subgroup are cyclic or trivial. The argument does not eliminate that case, and the frozen conclusion correctly leaves it open.

## Reproducibility and limits

All five author checkers were replayed with stdout byte-identical to their receipts: **28,038 new assertions**. Turn 3's imported prior controls are not counted again. `AUTHOR_REPLAY.json` records the receipts.

The independent checker imports no author code and passes **48,298 exact assertions**. It checks geometric edge addresses against directly multiplied truncated crossed-product series, inverse products, 13,121 distinct semidirect images through free-word length eight, grid basis changes, first symbols, tensor inclusion ranks through degree four, finite telescoping, and algebraic controls for fixed chords and the nonzero Euler relation. These are bounded controls, not a finite verification of surface topology, infinite conjugacy classes, or arbitrary-degree faithfulness. Those points are addressed in the proof audit above.

Recommended publication scope: preserve the five-turn proofs and their source qualifications as reviewed partial results; record the original as **unsolved 5/5**. Retain the unrestricted completed higher-genus case, higher strand numbers, and intended target conventions as explicit gaps. Do not label this a new solution to Kohno's complete question, a refutation of the cited universal-invariant literature, or a historical priority result.
