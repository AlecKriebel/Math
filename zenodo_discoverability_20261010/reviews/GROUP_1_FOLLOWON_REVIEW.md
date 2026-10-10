# Discovery metadata review: six follow-on papers

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
