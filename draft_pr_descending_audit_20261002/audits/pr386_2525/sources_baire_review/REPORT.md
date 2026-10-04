# PR386 source and topology audit

Review target: exact head `76d804cffb0cdbd2c88416dad1ead6e2a89989d6`.

Recorded UTC: 2026-10-03T01:33:46.649251+00:00. Source reconstruction was checkpointed before reading the candidate mathematics. The previous `final_review/REVIEW.md` verdict was not consulted. This is an audit of the frozen source normalization and Turn5, with current status checked in README, RESULT and the frozen queue. Turns1–4 have a separate algebra review. PR387's final disposition has precedence. No author turn6, candidate edit, Git/index/checkout mutation, PR action, publication, or external communication was performed.

**Finding:** Turn5's mathematical claims pass independent reconstruction under their stated assumptions. Its numerical checker reproduces exactly. No mathematical repair is required in the product, closed profinite, compact Baire, or analytic-generator arguments. **Full seven-PDF source certification is incomplete:** six PDFs were retrieved independently and exactly match the claimed bytes/hashes; the Maltcev repository PDF returned503 or timed out on every attempted primary route. The thesis attribution is therefore not independently certified here. It is not a premise of the accepted mathematics.

## Original target and present status

The maintained October2026 Kourovka21st PDF, printed/PDF179, problem21.16, confirms the exact distinction:

* CB: for every abstract group-generating X, the symmetric word diameter is finite.
* MB: for every abstract monoid-generating S, the positive word diameter is finite.

Every individual bound may depend on its set. The question asks whether CB can hold while MB fails. It imposes no topology, cardinality, measurability, definability, or common bound for all generating sets. Empty-word/identity padding does not change finiteness. Proper semigroups and densely generating semigroups fail the required monoid-generation premise.

The current maintainer home links the same October main and updates-only URLs used in the candidate. The target is unmarked as solved in the main source, and no21.16 entry occurs in the updates-only text. This verifies the maintained listing, not an exhaustive literature/novelty result. No new search for mathematical solutions was conducted.

The frozen candidate README3 records `unsolved,5/5` with a historical independent scoped-review PASS. Its README19 explicitly preserves historical pending wording in frozen author files. RESULT3 and the final author Turn5 still describe their original proposed disposition as pending full independent review. The queue row425 says `unsolved,5/5`. These are not conflicting mathematical claims; they concern different checkpoints. The old PASS is not used as evidence for this audit, and the incomplete Maltcev fetch prevents this audit from independently repeating an unqualified all-seven-source PASS.

No separating group and no unrestricted equivalence proof appears in Turn5. The exact remaining mathematical gap is still: construct S which reaches every element by a finite positive word, has unbounded such finite lengths, and belongs to G for which every symmetric applicable generating set has finite diameter; or prove this impossible. Compact/analytic restrictions do not close that gap.

## Source provenance and statement scope

See `FETCH_MANIFEST.json` for exact independent download UTCs, resolved URLs, HTTP metadata, lengths and SHA256 values. `SOURCE_FIRST_RECONSTRUCTION.md` records the order and primary reconstruction. All51 frozen files match `snapshot_manifest.json` in both byte length and SHA256 (`SNAPSHOT_INTEGRITY.json`).

| Source | Independent bytes | Exact claimed hash | Inspected source scope |
|---|---:|---|---|
| Kourovka October main | 1,881,857 | yes | title/current21st edition; printed/PDF17921.16, visually inspected |
| Kourovka October updates | 510,255 | yes | complete extracted-text target search, no21.16 hit |
| Bergman | 202,307 | yes | arXivmath/0401304v2; PDF4–6, visually inspected |
| Maltcev thesis | unavailable | unverified | primary repository metadata/indexed chapter21 excerpt only; full chapter not read |
| Khelif | 63,405 | yes | complete four-page2006 note read; scope declaration on printed378 |
| Jarnevic–Osin–Oyakawa | 269,341 | yes | arXiv2206.10712v2; introduction/Corollary1.6 and historical-open sentence, PDF3 visually inspected |
| Rosendal | 339,630 | yes | author-hosted manuscript; PDF4,8,9, visually inspected |

The unversioned arXiv URLs currently resolve to the candidate's exact PDFs. Bergman's downloaded margin identifies v2/27May2005 and its displayed manuscript date is30September2018; this is not a fetched typeset2006 journal PDF. JOO's current arXiv metadata identifies v2/29April2023. Rosendal's source is the author manuscript with Proposition3.9 on page9, not a source with the earlier arXiv proposition number. The candidate distinguishes these versions correctly.

[Bergman](https://arxiv.org/pdf/math/0401304) separately labels countable subgroup cofinality and Cayley boundedness, proves their conjunction implies MB, and asks both separation and MB-with-countable-cofinality questions. His proper positive monoid in the infinite symmetric group is a warning about generating conventions, not a separating witness. The candidate's normalization retains that distinction.

[Khelif's note](https://www.numdam.org/item/10.1016/j.crma.2006.01.010.pdf) explicitly supplies brief indications while deferring full demonstrations. Its asserted index2 example cannot be certified as a reconstructed HNN construction from this note. [JOO](https://arxiv.org/pdf/2206.10712) proves the countable mixed-identity-free exclusion; its unrestricted countable Cayley-graph question is a historical2023 statement, not a current all-cardinal answer to21.16. The candidate does not inflate either source.

The university [Maltcev repository record](https://research-repository.st-andrews.ac.uk/handle/10023/3226) identifies the thesis and2012 issuance. Indexed primary text confirms chapter2 discusses group/semigroup conventions and joint work with Mitchell/Ruškuc. The exact alleged unknown-converse sentence and later Khelif attribution in SOURCE_NORMALIZATION11 remain unread and unverified here. No indexed snippet substitutes for that inspection. `MALTCEV_FETCH_RETRY*.json` records attempts including query permutations, no-query routes, legacy bitstream paths, encoded/literal semicolon routes, and alternative sequence numbers; all failed. A curl request also returned HTTP503 with a2,097-byte HTML response, retained as `sources/maltcev_503_response.html`, not misidentified as a PDF.

## Cartesian positive length: independent proof and adversarial controls

Let I be any set, G=product G_i, S_i contain1, and S=product S_i. Set positive length to infinity for unreachable elements and include length0 for1. For every g=(g_i):

    length_S(g) = sup_i length_(S_i)(g_i).

Projection supplies the lower bound. If the right side is a finite integer m, every coordinate has a word of at most m letters. Choose these coordinate words (ordinary set-theoretic choice), pad them to m with1, and assemble their jth letters into a tuple s_j in S. Coordinate multiplication proves g=s_1...s_m. If the supremum is infinite, no finite global word can project to all coordinates. The proof works for infinitely many factors and for noncommutative groups; the letters are never reordered. For the empty product use the trivial group and sup(empty)=0. If a factor is trivial, S_i={1} contributes0.

If each D_i is finite and the family is unbounded, construct distinct i_n inductively with D_(i_n)>n and choose g_(i_n) of length>n, leaving other coordinates1. Such coordinates exist outside any finite previously selected family because its finite diameters have a finite maximum. The resulting element is unreachable, rather than merely having a large finite length. Thus the proposed unbounded Cartesian widths destroy algebraic monoid generation. They cannot witness MB failure.

Independent exact controls cover every identity-padded monoid-generating subset of S3 and D8:25 and108 sets, respectively. Their2,700 rectangles satisfy the length formula on all48 product elements. This supplements the author's abelian-only Cartesian controls with noncommutative multiplication. The distinct-coordinate diagonal example S_i={0,1} in additive C_(i+2) has g_i=i+1 and infinite global length; finite windows reproduce exact lengths1,...,8. This diagonal mechanism differs from growing support in a direct sum.

Two falsifications show why the assumptions matter. Without identity padding, S_i={1} in C2 and C3 gives Cartesian singleton{(1,1)}, which generates the finite product, but (0,1) has global length4 versus coordinate maximum1. Without rectangular form, {0,(1,0),(0,1)} in C2xC2 has full coordinate projections of diameter1 but (1,1) has length2. None contradicts Turn5, which states both assumptions.

The direct sum of nontrivial finite cyclic groups with one generator per coordinate fails CB: every word affects at most its length many coordinate positions, including signed words. Increasing support therefore supplies an unbounded symmetric generating metric. Turn5 correctly rejects it as a separating candidate.

## Closed profinite inverse limits: exact compactness obligations

For the stated sequential inverse limit of finite groups with surjective bonding maps, G is compact Hausdorff and its coordinate projections separate points. A closed S containing1 is compact. For finite m, the product-domain S^m is compact (distinguish this from the subset of G consisting of products). For fixed g, define F_n to be the tuples whose product has nth projection pi_n(g). If nth projected positive length is at most m, identity padding makes F_n nonempty. Each F_n is closed, and compatibility makes the F_n nested. Compactness provides a tuple in every F_n. Projection separation identifies its product with g. This proves the extended-value equality:

    length_S(g) = sup_n length_(pi_n S)(pi_n g).

For m=0 the singleton empty-tuple domain represents only the identity; projection separation handles this case. For a general directed profinite presentation replace nestedness by the finite-intersection property of a cofinal family of finite projections. The candidate only claims the sequential version and does not silently include arbitrary nonmetrizable presentations.

A finite uniform quotient diameter bound therefore lifts to finite global width. Separate finite bounds without uniformity do not. In Z_2, S={0,1} has quotient diameters2^n-1; -1 requires precisely2^n-1 letters in the nth quotient and has infinite global positive length. The hull is embedded nonnegative integers; the abstract subgroup generated by1 is embedded integers. Both are dense, neither equals Z_2. This is a generation failure, not an MB witness.

Closedness has a sharp failure control: let S be the embedded dense subgroup Z in Z_2, including0. Every finite quotient is covered in one letter, yet a nonintegral2-adic g has length infinity in S. For an explicit g, choose the2-adic sum sum_(j>=0)2^(2j); multiplying by3 gives -1, while no ordinary integer solves3z=-1. Thus the supremum of projected lengths can be1 while the global length is infinite. Here S is not closed and does not monoid-generate G. A finite control also shows why omitted/noncofinal projections are insufficient: in C8 with{0,1}, -1 has length7 while its C2 and C4 projected lengths have maximum3.

## Compact Baire word balls: independent product proof

In the exact candidate theorem, G is compact Hausdorff, S algebraically monoid-generates G, and every B_n=(S union {1})^n has the Baire property. Compact Hausdorff spaces and their open subsets are Baire. The increasing B_n exhaust G, so some B_n is nonmeagre and comeagre on a nonempty open U.

Fix x in UU. Choose x=uv with u,v in U. Then W=U intersect xU^-1 is nonempty open, since u belongs to W. On W, B_n is comeagre by restriction from U, and xB_n^-1 is comeagre by restriction from xU^-1 (translation/inversion are homeomorphisms). Since W is nonempty Baire, their intersection is nonempty. Pick a there; x=a b for b=a^-1x in B_n. Hence:

    UU subset B_n B_n subset B_(2n).

This is a product assertion. It does not require B_n to be symmetric, and UU need not contain1. All left translates of the nonempty open V=UU cover G. Compactness extracts g_1V,...,g_tV. Algebraic monoid generation makes every length_S(g_j) finite, so k=max_j length_S(g_j) is finite. Then G is contained in B_(k+2n). All implications are justified; no inverse cost is silently controlled. A rational-grid control distinguishes U+U near2/3 of a circle from U-U near0, documenting why an identity-neighborhood/difference-set substitution would change the argument.

If compactness is removed, increasing closed balls [-n,n] in R, or finite intervals in discrete Z, exhaust the group but no ball-product covers it. If algebraic generation is removed, the Z_2 example has closed regular balls but no coverage of the group. These controls validate the claimed boundary rather than suggesting either missing hypothesis is expendable.

The source [Rosendal manuscript](https://www.math.uic.edu/~rosendal/PapersWebsite/Property%28OB%2910.pdf) states its stronger topologically2-Bergman result for compact Polish groups. Its analytic/Baire input is explicitly stated on page4. The candidate's compact-Hausdorff version is supported by its own complete elementary proof, rather than claiming that wider scope as the printed source theorem.

## Analytic and sigma-compact scope; a stronger missing-hypothesis counterexample

For sigma-compact S in a compact Hausdorff group, a finite product of S union{1} is a countable union of continuous images of finite products of compact sets. These images are compact and hence closed, so every B_n is F_sigma and has the Baire property. For analytic S in compact Polish G, finite Cartesian products of S are analytic and continuous multiplication gives analytic word balls; adding1 and finite unions preserves analyticity. Analytic sets have the Baire property. These applications require genuine algebraic monoid generation; they produce finite positive diameter independently of CB. The candidate correctly limits the analytic assertion to a Polish realization and credits prior theory.

The candidate warns that Baire property of S alone cannot be substituted. An independent explicit counterexample confirms more than a lack of a general closure rule:

Let G=(F2)^N with its compact Polish product topology. Let E be the closed subgroup supported on even coordinates and O the closed subgroup supported on odd coordinates. Each is nowhere dense: any basic cylinder leaves an unspecified coordinate in the complementary infinite parity class, whose value can violate the support constraint. G=E direct-sum O as vector spaces (only two components). Choose algebraic F2 bases H_E and H_O extending the coordinate-unit sets in their components. Then H=H_E union H_O is a basis of all G.

Set S=H union{0}. Since S is contained in the meagre closed E union O, S is meagre and has the Baire property. Every g is a finite sum of basis elements, so S genuinely monoid-generates G. The sum of n distinct coordinate units has unique basis support n and exact positive length n. Therefore S has unbounded positive diameter. It is also symmetric, so this G fails CB and this is not a21.16 separating example.

At least one positive ball must fail the Baire property. Indeed if a B_n had the Baire property and were nonmeagre, B_n+B_n would contain a nonempty open set. A cylinder inside that open set could be modified by adding4n+1 distinct unused coordinate units; the difference of two vectors each of basis support at most2n has support at most4n, so both resulting cylinder vectors cannot lie in B_(2n). Thus B_n cannot both have the Baire property and be nonmeagre. Since the balls exhaust the Baire group, not all can be meagre. This confirms a failure of regularity in a finite product-image of the meagre Baire set S. It is an adversarial omitted-hypothesis control, with no novelty claim.

Consequently the sentence in Turn5 saying a separating witness in a compact Polish realization must be nonanalytic, and some ball must fail the Baire property, is correct. No property(OB) conclusion certifies unrestricted abstract CB or eliminates arbitrary nonanalytic generators.

## Checker audit and reproduction

`verify_turn5.py` and `finite_groups.py` were copied into this audit's `private_replay` and run with bytecode writes disabled. The copies exactly match their frozen source hashes. The JSON agrees structurally with TURN_5_CHECKS.json:74,990 assertions, including49 abelian rectangles,1,195 elementwise Cartesian length comparisons, cyclic-successor lengths, quotient comparisons, and C2 support controls. This is finite evidence and not an algorithm deciding an infinite-group width property.

The independent `independent_controls.py` imports no candidate file. It passes132,421 assertions, chiefly129,600 elementwise nonabelian Cartesian checks and2,700 generation checks, plus precise dropped-hypothesis counterexamples. `INDEPENDENT_CONTROLS.json` records the full counts and diagonal windows. The category/Baire and infinite inverse-limit conclusions are accepted from written proofs, not from assertion counts. No test claims to simulate analyticity or category.

## Required fixes and exact remaining gaps

1. **No mandatory mathematical fix in audited Turn5.** Retain its identity padding, full Cartesian set, closed S, compatible cofinal projections, compact Hausdorff topology, genuine algebraic generation, and all-word-balls Baire hypotheses.
2. **Source certification gap:** retrieve and inspect the exact Maltcev PDF (claimed SHA256 `04250e01cf9acb47208ae37518b91ee8e24809fbecaaeccfcec3bd74e676b9ee`), or explicitly qualify any final assertion that all seven PDFs or all thesis historical attributions were independently verified in this renewed audit. A failed fetch does not justify altering the mathematics or declaring the source statement false.
3. **Disposition gap:** no21.16 solution and no novelty certification. The appropriate research status remains unsolved5/5. Finite controls, analytic compact exclusions, and historical source listings must not be promoted to an unrestricted theorem or successful separating construction. The root's final disposition and PR387 ordering remain separate from this scoped report.

For the wider result, the other algebra family's verification is still required; this report certifies only the stated source/topology scope. No outreach was prepared or attempted.
