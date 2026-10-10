# Group 1 discovery metadata review

Checkpoint: 2026-10-10 14:05 PDT (21:05 UTC). Best-guess completion toward the assigned **content review and metadata drafting** goal: **100%**. Remote application and verification remain the parent workflow's responsibility.

All 15 exact deposited-PDF text files across these 14 records were read in full before keyword drafting. The extra file is the conditional height supplement of record 23205305. Each catalog source records the deposited PDF's MD5 and identifies its local checksum-matched extraction. This is a content-alignment and discovery metadata review; it is not a new proof audit or certification of cited external theorems.

All existing titles match the deposited manuscripts. All existing descriptions already provide precise results, attribution, assumptions and limitations, including substantial AI-use, unrefereed-status and priority caveats. **No title or description is rewritten.** All 14 patches replace keyword arrays with 14–17 precise subject/problem/object/method terms. English language is added only on the 12 records lacking it. Record 23217863 additionally gains three structured related identifiers that already appear verbatim as primary-source links in its existing description. All other existing related identifiers remain untouched. The generic keyword “mathematics” is replaced by precise group/operator-algebra terms on 23204212; worthwhile existing tags are otherwise retained. No MSC classifications, novelty adjectives, creator changes, DOI changes, versions, dates, licenses, access changes or file updates are proposed.

## 23271172 — Exact six-period correction to k108

Read source: `papers/23271172/k108_counterexample.txt`, exact deposited file `k108_counterexample.pdf`, MD5 `246d4799e32ac121540f2f725a1281bc` (5 PDF pages).

Checkable content evidence:

- Abstract and §1 define the literal quotient `k108=(A'/A)/product sin(theta_i/2)` for N=2 modulo 4. A' is the original boundary's outer tangent polygon, not a caustic-contact polygon. The source entry is experimentally asserted and unproved, not a theorem.
- §2 explicitly verifies two strictly convex primitive hexagons in `x²/4+y²=1`, nested confocal caustic parameter λ=4/9, finite-segment contacts, physical reflection, Joachimsthal J=1/3 and membership in the same connected oriented Poncelet family. Connected motion/symmetry are attributed to Stachel.
- §3 computes positive signed areas and original internal-angle half-sine products, with quotient values 11664/3125 and 3645/1024; their difference is positive. Shared two-witness values AA'=320/9 and `(A'/A) product sin(theta_i/2)=5/9` do not prove a repaired family or all-period theorem.
- §1 and §4 credit Garcia–Reznik's established horizontal coordinates/caustic. Exact rational/quadratic-field and symbolic diagnostics support the written proof, without proof-assistant formalization. Historical firstness and independent discovery remain unconfirmed.

Discovery rationale: retain the six existing tags; add k108, confocal elliptical caustics, outer tangent polygons, polygon area ratios, half-angle sine products, Poncelet porism, physical reflection and exact rational/symbolic methods. These identify the exact conjectural object and the proof method without implying new six-period geometry. Fifteen tags; add English language metadata.

Preserved caveats: unproved experimental assertion, established geometry and family machinery, credited source, attributed corrective application, no official erratum or all-period replacement, limited historical search, AI/unrefereed/no formalization.

Patch: `patches/23271172.json`.

## 23231145 — Four-period counterexample to k107

Read source: `papers/23231145/k107_counterexample.txt`, exact deposited file `k107_counterexample.pdf`, MD5 `e9979ae511b977ca9e63a0e3ce246e67` (4 PDF pages).

Checkable content evidence:

- §1 identifies the literal product `k107=(A'/A) product sin(theta_i/2)`, N=0 modulo 4, with original internal angles and outer tangent areas. It is marked unproved in the cited table.
- Lemma 1, §2 gives a continuous normal-coordinate family with `lambda=a²b²/(a²+b²)`, explicit boundary membership, reflection, strict interior caustic contacts, distinct vertices and nonzero denominators. Every member is primitive and strictly convex.
- Theorem 1, §3 proves nonconstancy for all a>b>0 and exact witnesses 288/625, 625/1152 at a=4,b=3. The excluded circle limit collapses to K=1/2. The argument covers reversed signed/unsigned area conventions but asserts only the four-period diagnosis.
- §§1,4 credit Garcia–Reznik's four-period construction and Ferudun's same witnesses/general family formula. Repository/deposit chronology does not establish exclusive global priority or independence. Exact finite and symbolic checks support the continuous-family proof, with no formalization claim.

Discovery rationale: retain all existing tags; add k107 and exact geometric objects/angle-product nomenclature, continuous family, reflection, rational and symbolic methods. Fifteen terms; add English language metadata. Description is retained with contemporary overlap, source-access limits and no corrected all-period theorem.

Patch: `patches/23231145.json`.

## 23224103 — Brownian first-visit cell lengths on a circle

Read source: `papers/23224103/brownian_first_visit.txt`, exact deposited file `brownian_first_visit.pdf`, MD5 `954fa7a778c00cd973486e7f6585fcd6` (6 PDF pages).

Checkable content evidence:

- §1 identifies Georgakopoulos's finite-particle question and independent Brownian motions on `R/Z`. Walkers keep moving through meetings, seeds and visited territory. Labels use earliest physical hitting time, with length ownership defined up to null sets.
- §2, equations (2)–(9) reduce finite-query ownership to interval-exit kernel densities, finite permutation sums and ordinary nonnegative integrals over strict linear inequalities in cumulative physical clocks.
- Theorem 1 supplies an absolutely convergent mixed-moment Laplace series, uniform factorial outer remainder bound, and moment determinacy on the compact simplex for arbitrary distinct fixed, equally spaced or independent uniform seeds.
- §3 uses Dirichlet heat kernels, optional stopping, strong Markov iteration, bounded moments and Stone–Weierstrass. A tie is absent almost surely at each fixed query and for almost every location, not simultaneously at every location. Uniform labels are exchangeable; equally spaced labels only have cyclic/dihedral symmetry.
- §4 distinguishes competing-walk painting predecessors and classical methods. The outer bound does not certify inner kernel truncation or numerical quadrature; no named/compact density, fast evaluator, large-k law, absolute priority or independent-discovery claim is asserted.

Discovery rationale: retain the six original terms and add Brownian-circle/independent-particle and first-passage nomenclature, stochastic geometry, the referenced “Voronoi-like decomposition” title, Georgakopoulos's circle partition question, exit/heat kernels, strong Markov, mixed moments and moment determinacy. Seventeen relevant tags; add English language metadata. Existing description preserves all major attribution/numerical/priority/review caveats.

Patch: `patches/23224103.json`.

## 23220043 — Focal antipedal vertex centroids, k405

Read source: `papers/23220043/antipedal_centroids.txt`, exact deposited file `antipedal_centroids.pdf`, MD5 `38ce60090b49db8897074639c4165905` (5 PDF pages).

Checkable content evidence:

- §1 and Theorem 1 define original-polygon, full-line antipedal intersections and their unweighted vertex mean, with strictly nested elliptical caustic and even **least** period. They prove center centroid zero and an explicit phase-independent focal coefficient. Area centroid and pedal-foot means are different observables.
- Theorem 1 covers primitive star polygons and both orientations; the circle is treated by central symmetry without dividing by c². Hyperbolic/degenerate caustics and two-bounce limits are excluded. Repeating an odd triangle twice does not acquire the theorem; §1 supplies a nonzero-centroid counterexample.
- Lemma 1, §2 uses finite circle actions to prove antipodal vertices. Lemma 2 uses perimeter stationarity and chord moments. §3 inserts a local opposite-edge antipedal identity into those moments.
- §4 credits classical symmetry/stationarity machinery and the same theorem/coefficient/pair mechanism in Ferudun's deposited note; chronology establishes only those specific records. No absolute/exclusive priority, independent discovery, copying or collaboration claim is made. Finite diagnostics do not prove Poncelet closure for all parameters.

Discovery rationale: retain six original tags and add focal antipedals, even least period, confocal caustics, Poncelet porism, central symmetry, perimeter stationarity, primitive star polygons, finite circle actions, billiard invariants and exact verification. Sixteen terms; add English language metadata. Existing careful description is retained.

Patch: `patches/23220043.json`.

## 23217863 — Ordinary Banach–Mazur rigidity of von Neumann algebras

Read source: `papers/23217863/paper.txt`, exact deposited file `paper.pdf`, MD5 recorded in the group catalog (7 PDF pages).

Checkable content evidence:

- §1 Theorem 1 gives `for every M, there exists epsilon_M>0, for every N` ordinary **complex** Banach–Mazur rigidity, with Jordan *-isomorphism and the same threshold for canonical preduals. The threshold depends on M; the zero algebra is covered explicitly.
- Theorem 2 is attributed ordinary bounded, self-coefficient Hochschild vanishing for every von Neumann algebra, using the fixed OpenAI source commit. Cochains are all bounded complex multilinear maps, with actual-image cohomology; no normality or complete boundedness is substituted.
- §2 supplies involution-compatible multiplication stability with fixed-algebra constants. §§3–5 use at most two fixed source algebras, full abelian carriers and finite type-I reconstruction; arbitrary nonseparable centers and infinite cardinal dimensions are allowed.
- §6 distinguishes completely bounded distance from ordinary distance, credits Roydor's 2020 conditional announcement, and does not silently remove the published article's separable-predual condition. No universal number, firstness, independently new cohomology theorem or reproduced Lean kernel verification is claimed.

Discovery rationale: retain five original tags and add operator algebras, Banach space geometry, ordinary complex distance, Jordan *-isomorphism, local/nonseparable rigidity, deformation stability, multiplication perturbations, type I and full abelian projections. Fifteen tags; add English language metadata.

Structured-source rationale: this record lacks `related_identifiers` although its existing description already lists (verbatim) the pinned OpenAI manuscript path, Roydor DOI 10.1142/S1793525321500151 and Ricard–Roydor arXiv 1108.1970v2. Adding the same three links improves machine-readable citation/dependency discovery without adding new intellectual claims. The upstream link uses `isDerivedFrom`; the two papers use `references`. The exact manuscript §1 and bibliography [1],[3],[4], repository `openai_followon_banach_mazur_von_neumann/zenodo-deposit.json`, `receipts/published_public_independent_readback_20261007.json`, `receipts/pinned_sources.json`, and `research/roydor_primary.md` corroborate identity and version. No existing identifier is removed. Source-link verification uses the manuscript and already tracked source receipts; no new priority claim or current live availability certification is made.

Patch: `patches/23217863.json`.

## 23204591 — Commuting bilinear ergodic Hilbert variation

Read source: `papers/23204591/paper.txt`, exact deposited file `paper.pdf`, MD5 `c63ad8716687753d928852902d4e4932` (5 PDF pages).

Checkable content evidence:

- §1 Theorem 1 assumes commuting invertible probability-preserving S,T, complex L³ inputs, symmetric odd-kernel Hilbert sums and every r>2. It gives pointwise r-variation in L^(3/2), a maximal estimate, almost-everywhere/norm convergence and maximal-tail norm convergence.
- Equation (4) is the inherited full annular continuous estimate from the fixed OpenAI manuscript, with the supremum over partitions inside the norm. Maximal/dyadic/fixed-partition estimates are expressly insufficient substitutes.
- §2 performs fixed positive-area box restriction to the lattice, with half-integer radial cutoffs and a uniform summable O(k^-2) signed kernel error.
- §3 gives finite-menu finite-window Calderón transference and measurable full-measure representatives, followed by convergence from finite variation.
- §4 retains commuting, symmetric, r>2 and L³ scope; no r=2, noncommuting, one-sided Cesàro or new continuous breakthrough claim. Older Lean maximal artifacts do not verify full variation or this note.

Discovery rationale: retain five existing terms; add ergodic/harmonic analysis, singular integrals, r-variation, annular truncations, commuting measure-preserving transformations, discrete restriction, almost everywhere convergence, maximal inequalities and symmetric Hilbert sums. Fifteen tags. English metadata is already present and is unchanged; existing precise description remains.

Patch: `patches/23204591.json`.

## 23204250 — Exact SDP complexity of symmetric TSP

Read source: `papers/23204250/paper.txt`, exact deposited file `paper.pdf`, MD5 `f52bedc96c0efbcbfbf8ad1916100558` (6 PDF pages).

Checkable content evidence:

- §1 Theorem 1 gives exact **real** semidefinite extension complexity `2^Theta(N)`, counting one PSD matrix's order or total block order, for undirected Hamiltonian-cycle incidence polytope. Largest-block-only size is expressly a different convention.
- §2 attributes exponential PSD rank of shifted matching matrices to OpenAI and gives an exact affine-slack bridge. The positive shift is removed with an extra factor dimension; rho=1 is excluded.
- §§3–4 make Yannakakis's inherited 3n face projection, a 2n contraction and all-city padding explicit. The 2n face needs diagonal-one constraints as well as cross-edge-zero constraints; missing the one constraints fails.
- §5 builds an exact subset-state DAG flow upper bound with arc count `2(N-1)+(N-1)(N-2)2^(N-3)`. Finite graph enumerations support gadgets but cannot prove the asymptotic external lower bound.
- Disclosures attribute the breakthrough, note Lean scope only superpolynomial, and disclaim approximation/hierarchy/bit-complexity/P-versus-NP/complex-cone consequences and first priority.

Discovery rationale: retain five original tags; add symmetric traveling salesman problem/TSP, semidefinite programming/SDP, exact real semidefinite lifts, exponential lower bounds, slack matrices, matching polytope, Hamiltonian cycles, face projections and subset-state dynamic programming. Sixteen terms; add English language metadata. The existing attributed/scoped description is unchanged.

Patch: `patches/23204250.json`.

## 23204212 — Thompson-family reduced C*-algebras

Read source: `papers/23204212/paper.txt`, exact deposited file `paper.pdf`, MD5 `d47f4c2acb85921e377cc69027d64fec` (4 PDF pages).

Checkable content evidence:

- §1 specifies standard dyadic PL Thompson F and T as discrete groups, the **full** abstract Aut(F) and abstract commensurator Comm(F), and reduced group C*-algebras/canonical trace.
- Established Theorems 1–2 cite Le Boudec–Matte Bon simplicity equivalences and BKKO's trivial-amenable-radical trace criterion. Corollary 3 applies the external OpenAI nonamenability input to all four groups; countability is proved using finite generators/finite-index subgroups.
- Corollary 4 concerns countable circle-homeomorphism overgroups containing the specified standard action of F. An arbitrary abstract embedding in an unrelated action is not sufficient.
- §3 credits every simplicity reduction and the input theorem; T's unique trace was already unconditional. Only reduced algebras are asserted, with explicit distinction from full group C*-algebras and abstract group simplicity. Input-dependent conclusions have the same dependency on the external theorem's validity.
- Disclosure retains extensive AI help, no human refereeing, source-audit/formalization limits and no first-observation/independent amenability solution claim.

Discovery rationale: retain four precise original keywords, replacing generic “mathematics” with the actual operator-algebra/group-theory objects. Add individual Thompson F/T, Aut(F), Comm(F), nonamenability, amenable radical, operator algebras, discrete groups, groups of homeomorphisms, circle actions and canonical trace. Fifteen tags; add English language metadata. No description or attribution changes.

Patch: `patches/23204212.json`.


---

# Follow-on source review supporting the remaining six group-1 records

Checkpoint: 2026-10-10 14:03 PDT (21:03 UTC). Estimated completion of this assigned **content review and metadata drafting** goal: **100%**. Remote application and post-publication verification remain the parent workflow's responsibility.

I read every line of the seven exact deposited-PDF text files in the catalog for records 23205305, 23205294, 23205181, 23205034, 23204952 and 23204810. This includes both the main paper and the standalone height repair for 23205305. The catalog identifies the PDFs by deposited MD5 and records local checksum matches. This is a metadata/content alignment review, not a new proof audit or independent certification of the external OpenAI theorems.

Each existing title matches the deposited paper and accurately identifies its topic. Each existing description already gives substantially more mathematical and attribution detail than a generic abstract. I retained them verbatim. The six proposed patches change only the keyword array and, on the five records lacking it, add `language: eng`. The patches contain changed fields only. No creator, affiliation, ORCID, coauthor, DOI, reserved DOI, related identifier, version, publication date, license, access field, publication type or file is changed. No MSC classification, unverifiable link, priority claim or promotional assertion was added. No remote mutation or external communication was performed.

## 23205305 — Rational-point undecidability

Read sources: `papers/23205305/paper.txt` (292 lines, 6 PDF pages) and `papers/23205305/height-repair.txt` (226 lines, 4 PDF pages).

Checkable evidence:

- Main paper, §1, lines 21–42: integer-polynomial H10(Q), homogeneous projective-equation presentations and the smooth/geometrically integral valid-input promise; ambient dimension, degree, number of equations and coefficient heights can vary.
- Main paper, Theorem 2, lines 81–109: effective component decomposition and geometric-integrality tests produce finitely many valid queries; the reduction is nonadaptive disjunctive, hence Turing, and is expressly not a single-output many-one theorem.
- Main paper, Corollaries 3–4 and §3, lines 112–147: rational-point existence is undecidable using the corrected external arithmetic input; no total computable presentation-size bound can ensure the height of one point.
- Main paper, §4, lines 150–238, and height supplement, Theorem 1 and §§2–5, lines 56–198: the two technical arithmetic repairs concern coefficient primes (5,2), modular Galois representations and the universal Euler-convention correction. The height supplement retains three geometric/height inputs and proves its bound conditionally on them.
- Main paper, §5 and disclosure, lines 242–265: naive compactification/resolution boundary pitfalls, no fixed-dimensional or curve/surface conclusion, credited Poonen reduction and OpenAI arithmetic input, AI use and no conventional peer review/full formalization.

Discovery rationale: retain all five original topic tags and add the explicit rational-field H10 name, geometrically integral objects, Diophantine equations, arithmetic geometry, computability and Turing-reduction vocabulary, the homogeneous-input representation, and the two genuinely developed height/modularity topics. Fourteen curated terms cover both the principal note and the deposited conditional supplement. Add English language metadata.

Preserved caveats: two source proof corrections; the height supplement's retained assumptions; variable dimension/size; no new base undecidability proof or geometric reduction; no many-one hardness, fixed-dimensional result or priority claim; AI/unrefereed/no complete formal-verification statements.

Patch: `patches/23205305.json`.

## 23205294 — Nonnegative binary rational hafnians

Read source: `papers/23205294/paper.txt` (282 lines, 6 PDF pages).

Checkable evidence:

- §1, lines 24–61: even-order symmetric matrices, nonnegative rational off-diagonal entries, irrelevant diagonal, support-matching feasibility and empty-order value one. The general-graph FPRAS is an external input; logarithmic weight removal and counting self-reduction are explicitly prior machinery.
- Lemma 1 and Theorem 2, lines 64–133: the binary-Horner DAG yields signature (W,1,0,0); denominator clearing gives a simple graph H with exact count `#PM(H) = D^m haf(A)` and weighted matching fibers. Graph size is polynomial in binary encoding length.
- Corollary 3, lines 136–148: exact support feasibility plus a positive-output adjustment gives zero exactly when the hafnian is zero, with every-execution polynomial bit complexity.
- Lemma 4 and Corollary 5, lines 152–227: bounded-bit categorical draws, counting self-reduction and feasibility fallback; an explicit total-variation bound contracts under projection to weighted matching fibers.
- §5, lines 230–247: finite checks do not certify the external FPRAS; nonnegative rational scope excludes signed/complex hafnians and unrestricted Gaussian boson sampling; upstream Lean statement inspection is not an independent rebuild or follow-on formalization.

Discovery rationale: retain the original six keywords and add the weighted matching problem, hafnian approximation, the expanded FPRAS name, exact reduction/gadget vocabulary, classical counting self-reduction, total variation, exact-zero behavior and bit complexity. Fifteen terms identify the exact algorithmic model and relevant approximate counting/sampling community. Add English language metadata.

Preserved caveats: inherited approximation breakthrough and reduction machinery; no first-publication/new-reduction assertion; worst-case bit model; only nonnegative rational input; finite checks versus proof/upstream certification; AI/unrefereed and code/prose licensing disclosures.

Patch: `patches/23205294.json`.

## 23205181 — Characteristic-two random-cone threshold

Read source: `papers/23205181/paper.txt` (334 lines, 7 PDF pages).

Checkable evidence:

- §1, lines 24–44: the upstream construction supplies `ab=1, ac=0, c≠0` in a torsion-free characteristic-two group algebra; the new contribution is calibration of an unchanged seven-extra construction, not the base breakthrough.
- Theorem 1 and §2, lines 48–116: the signed alphabet is built from PG(2,q) plus seven extras; a positive three-class quotient gives the exact least dyadic threshold q=32, contraction there and lower bounds at q=4,8,16. Certificates are rational, rather than numerical eigenvalue evidence.
- Proposition 2, lines 119–176: parameter-dependent probabilistic/planar estimates carry the model to a 532-edge rose and a finite two-dimensional classifying complex. Matching outcomes and group-ring multiplication witnesses are existential, not numerically supplied.
- §4, lines 180–225: classical HNN embedding gives a two-generator realization and preserves finite two-dimensional asphericity.
- Proposition 4 and Theorem 5, lines 228–277: `e=1-ba` is nontrivial; `P=eR` is a nonzero cyclic projective right module, `R≅R⊕P`, and `[P]=0` in K0. These identities extend to every characteristic-two field.
- §6 and disclosure, lines 280–299: the idempotent/module consequences were publicly recorded in triage; no global optimization, odd/zero-characteristic result, numerical matching certificate, first-priority claim or complete formalization.

Discovery rationale: retain all six existing keywords and add the exact group/ring property, random-cone and dyadic-calibration mechanism, finite projective planes, Perron–Frobenius method, HNN/two-generator/aspherical realization, and the cyclic module/K-theory interpretation. Seventeen terms connect the original theorem to group theory, probability and ring theory searches without suggesting that the threshold is a global optimum. Add English language metadata.

Preserved caveats: model-specific q=32 threshold; 532 counts this recipe; classical two-generator embedding; inherited source and duplicate triage consequences; existential construction; all-field extension confined to characteristic two; no nonzero K0-class assertion; AI/unrefereed and no formalization.

Patch: `patches/23205181.json`.

## 23205034 — Output-sensitive sparse finite-field factorization

Read source: `papers/23205034/paper.txt` (449 lines, 9 PDF pages).

Checkable evidence:

- §1, lines 24–67: explicit quotient-field representation, sparse univariate input with binary exponents, and dense output factors; D is total degree of distinct factors, not sparse output term count. Classical reconstruction, residue and Cartier tools are attributed.
- Theorem 1, lines 70–79: an independent reduction to at most 2b dense factorization calls of degree at most (b+1)D, with polynomial nonoracle cost and arbitrary binary multiplicities.
- §§2.1–2.4, lines 81–211: exact multiplicity recovery; acceptance only after an exact sparse Padé identity; numerator/denominator characteristic-p descent; denominator degree increases by at most D per level; signed residue accounting handles spurious intermediate factors.
- Theorem 2 and §3, lines 214–310: established prime-Frobenius/Berlekamp reductions, trace separation, multiplicities and inverse coefficient Frobenius. The prime-field factorization theorem is not proved here.
- §§4–5, lines 313–374: prescribed-degree irreducible construction is output polynomial in numeric degree; substitution of the OpenAI prime-field input requires the general cyclotomic Hecke zero-free companion, not a Dirichlet-only theorem.
- §6, lines 377–402: toy prime oracle only; huge branch not executed; no practical-efficiency claim, arbitrary-circuit result, sparse-only output complexity, binary prescribed-degree complexity or full formal verification.

Discovery rationale: retain the six original keywords and add the precise univariate factorization task, the common sparse/lacunary synonym, output-sensitive complexity, squarefree factoring, characteristic-p descent, logarithmic derivatives, Padé reconstruction, Cartier sections, multiplicities, Frobenius maps and symbolic computation. Seventeen tags distinguish this contribution's sparse/dense output invariant from generic dense factorization. Add English language metadata.

Preserved caveats: D counts dense factor degrees; arbitrary multiplicities use binary representations; the reduction theorem is distinct from its inherited upstream implementation; explicit cyclotomic dependency; prescribed/root degrees are numeric output parameters; toy checks cannot substantiate the external breakthrough; no priority or formalization claim; AI/unrefereed.

Patch: `patches/23205034.json`.

## 23204952 — Metric rigidity at the cubic boundary

Read source: `papers/23204952/paper.txt` (404 lines, 8 PDF pages).

Checkable evidence:

- Theorem 1 and §2, lines 67–74 and 101–151: weak KE normal klt Fanos with bounded potentials and an actual ample Cartier root `-K_X=rL`; strict `r>dim(X)/2+1`; stable tangent sheaves on finite quasi-étale covers and parallel orthogonal complex structures restricted to ±J. Equal-dimensional projective products falsify including equality.
- Theorem 2, lines 76–95, and §6, lines 273–307: cubic n-folds n≥5; ordinary metric GH fibers are conjugation orbits even at singular boundary points; every metric isometry is holomorphic or antiholomorphic and preserves the hyperplane Cartier polarization.
- §§3–5, lines 154–270: normalized volume, the global minimizing Reeb valuation, iterated-cone density bounds and the established Spotti–Sun transfer yield the complex-preserving comparison. This uses the external ordinary-double-point upper gap and retains the smoothing-locus/topological scope.
- §7, lines 313–339: the stronger complex algebraic comparison is already public; smooth stability/rigidity/conjugation precedents and DGP decomposition are credited. The additional deduction checks singular metric rigidity, without a first-priority or scheme/stack claim.

Discovery rationale: preserve the six original concepts, standardize the Kähler spelling with its conventional accent, and add the exact singular Fano objects, stable tangent sheaves/quasi-étale covers, parallel complex structures and conjugation, GIT terminology and the normalized-volume/Reeb tools used in the inherited comparison. Fifteen terms cover algebraic, differential and metric geometry audiences. English is already present and is unchanged.

Preserved caveats: genuine Cartier root and strict sharp threshold; n≥5 cubic application; bounded-potentials weak KE setting; external gap; prior stronger comparison and inherited transfers; smoothable coarse/closed-point homeomorphism scope; no scheme/stack upgrade, effective GH estimates, dimension-four counterclaim or formal verification; AI/unrefereed and original-code licensing statements.

Patch: `patches/23204952.json`.

## 23204810 — Sperner property of Artinian complete intersections

Read source: `papers/23204810/paper.txt` (224 lines, 5 PDF pages).

Checkable evidence:

- §1 and Theorem 1, lines 20–46: all ideals, including nonhomogeneous ideals, enter the Dilworth number; for any characteristic-zero field and a homogeneous regular sequence, that number is the maximum complete-intersection Hilbert-series coefficient. Empty/all-linear cases yield the field with maximum one.
- §2, lines 49–86: full-length Artinian EGH is the external input; degree-one elimination and descent from a finitely generated coefficient field justify arbitrary characteristic-zero fields.
- §3, lines 89–145: product-of-chains symmetric decomposition proves the monomial matching inequality; the already published EGH-to-matching/Sperner mechanism transfers it. No equality of generator counts from Hilbert matching is assumed.
- §4, lines 149–168: finite associated grading sends arbitrary ideals to homogeneous initial ideals and provides the upper bound without assuming `gr(mI)=m gr(I)`; a power of the maximal ideal attains equality.
- §5 and disclosure, lines 171–199: explicit Hilbert examples; no weak/strong Lefschetz property, nongraded complete-intersection extension or unrestricted positive-characteristic assertion. Both the arithmetic input and known implication are credited; no first-priority/formalization claim and no conventional peer review.

Discovery rationale: retain the four existing keywords and add standard graded algebras, the common EGH abbreviation, Dilworth number, Hilbert functions/series, generator counts and nonhomogeneous ideals, the matching/symmetric-chain proof vocabulary, and characteristic-zero scope. Fourteen tags reach commutative algebra and algebraic combinatorics searches. Add English language metadata.

Preserved caveats: immediate attributed consequence of external EGH and published Harima–Wachi–Watanabe implication; full-length standard graded/Artinian/characteristic-zero scope; explicit empty/all-linear and all-ideal boundary cases; no Lefschetz or ungraded theorem; AI/unrefereed/no formalization.

Patch: `patches/23204810.json`.

## Validation and remaining gap

All six patch JSON files parse, contain unique keyword arrays of 14–17 entries, and contain only `metadata.keywords` and (where absent previously) `metadata.language`. Existing careful descriptions and titles are unchanged, preserving their dependency, attribution and review-status caveats. The keyword terms were checked against the exact deposited text; this drafting stage neither opens a Zenodo draft nor publishes anything.

The remaining task is the parent's metadata-only edit/publish workflow and verification that record IDs, existing DOIs/concept DOIs, versions, files/checksums and immutable publication data remain unchanged. No new DOI or version should be created. Discovery ranking, indexing delays and readership cannot be guaranteed by metadata alone.


## Group-wide validation

All 14 patch files parse and contain changed metadata fields only. Keyword arrays are unique and comprise 14–17 terms. Only keywords, missing language and the three already-described source links for 23217863 change. All titles, descriptions, creator metadata, DOI/reserved DOI, concept-record relations, versions, publication dates, licenses, access and files remain unchanged in the proposed patches. Independent adversarial review and the parent metadata-only application/readback checks remain. No Zenodo mutation, external communication or git commit was performed by this reviewer.
