# Independent adversarial review — Zenodo 23328912

**Conclusion: PASS at the exact stated scope.** The explicit finite quotient has the asserted simple flag link, and reversible nonabelian presentation changes identify its fundamental group with the marked AIM example. I found no substantive gap in the explicit construction or the separate qualitative deduction from prior tools. This is AI review, not external human peer review, formal proof certification, or a novelty/minimality certificate.

## Reviewed object and independence

The reviewed work is **A two-cube cubulation of the AIM free-by-cyclic example**, Alec Kriebel, v1.0, 12 October 2026, [DOI 10.5281/zenodo.23328912](https://doi.org/10.5281/zenodo.23328912). I read all six actual PDF pages and the complete current `preprint.tex`, then inspected the three mathematical verification programs after completing the fresh controls. Source bindings are:

| Public file | Bytes | SHA256 |
|---|---:|---|
| aim_5_2_two_cube_cubulation.pdf | 77,863 | `3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841` |
| aim_5_2_source.zip | 11,430 | `a244ddbbbb0f7ca6d9ca073d21589bef1e9c0a98a404daaca195ee9fc87f6935` |
| aim_5_2_verification.zip | 56,309 | `8ff6e88f6d4a539680667b22931e080365dfd905dd64f795f408e23cc7bb8f01` |

The fresh acquisition receipt SHA256 is `f2a9045f30b1bd6d152cc7fe5370254a5085df279c17af3d8996e1701922d9dc`. `evidence/source-binding.json` pins that receipt, metadata, PDF, both ZIPs and the TeX source. All 28 extracted members were checked against archive bytes, both ZIP CRC checks passed, and all source assets remain unchanged. There is one distinct reader PDF.

No sibling findings, code or reports were consulted. Dedicated historical assessment bodies, source gates, bundle reports and previous result JSONs were not read or adopted. The manuscript’s own bounded-prior-audit assertion was necessarily encountered and is not a priority certificate. After the independent reconstruction, I read the distributed mathematical helpers, including two stored under `packet/audit/`; their introductory comments refer to a historical written audit, which I did not open. One unchanged helper hashes `ATTEMPT_1.md` as opaque bytes; that does not constitute reading or accepting its body. The earlier sealed Nijenhuis, WARM and Nevo reviews were not changed.

## Exact target and scope

Let F = F(a,b,c), φ(a)=a, φ(b)=ab, φ(c)=bcb, and

G = ⟨a,b,c,t | tat⁻¹=a, tbt⁻¹=ab, tct⁻¹=bcb⟩.

The final b is positive. The explicit inverse φ⁻¹(a)=a, φ⁻¹(b)=a⁻¹b, φ⁻¹(c)=b⁻¹acb⁻¹a composes with φ to the identity in both orders by free reduction. Thus the target is genuinely the indicated free-by-cyclic group, not merely a presentation whose monodromy has been assumed invertible.

The theorem constructs a finite locally CAT(0) unit **cube complex allowing isometric identifications of boundary faces**, with cell counts (1,7,8,2). Its characteristic cubes in the quotient need not be embedded. Its CAT(0) universal cover admits the free, proper, cocompact deck action of the full group G. The counts precede subdivision. No minimal dimension, minimal cell count, virtual specialness, general family, or historical firstness is asserted.

I read the actual archived [AIM Problem 5.2 body](https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/), attributed to Rylee Lyman. Its formula and requested geometric CAT(0) cube action match exactly. The live source timed out in fresh acquisition, and the web tool could not open the archive; the freshly acquired raw archived HTML was independently hash-checked and read. This establishes the historical question’s wording, not its current open status. The three-page [AIM workshop report](https://aimath.org/pastworkshops/freebycyclicrep.pdf), read in full, instead discusses b↦aba and c↦bcb on p.2 and a three-dimensional candidate. The manuscript properly distinguishes those formulas; neither this review nor the manuscript claims that the marked examples are interchangeable or proves their groups nonisomorphic.

## 1. Attack on the finite geometry and repeated incidences

### The base and involution

The one-vertex base K has edges x,y,b and squares xyXY, bxBY, with capitals indicating inverse orientations. Computing every characteristic-square corner gives exactly eight link edges: all four x-sign/y-sign pairs, b⁻ joined to x⁺ and x⁻, and b⁺ joined to y⁺ and y⁻. The link is a simple bipartite graph with no triangles. These are incidence counts, not a set obtained by silently discarding repeated edges.

The map λ sends x↦y, y↦x, b↦b⁻¹. The two square boundaries become yxYX and BybX. Each is a dihedral reparametrization of the same corresponding base square. The oriented boundary data determine the square isometries, agree along identified faces, and square to the identity on characteristic squares as well as edges. This verifies a cubical isometric involution, stronger than checking only its induced group homomorphism. Fresh controls record the dihedral matches and order-two property. See source lines 72–100.

### Q and the two A-corners

The six specified oriented edges of Q have boundaries p:B→A, q:A→C, r:D→C, s:B→D, d:A→B and e:C→A, with j-labels x,y,x,y,b,b. The square words pqr⁻¹s⁻¹ and dpe⁻¹q⁻¹ close, with characteristic vertex cycles (B,A,C,D) and (A,B,A,C). In particular, the second square has **two distinct A-corner incidences**, not one corner counted twice accidentally.

Fresh corner enumeration from those words, without importing the printed link table, gives:

* A: e⁻—p⁻—q⁺—d⁺;
* B: d⁻—p⁺—s⁺;
* C: r⁻—q⁻—e⁺;
* D: r⁺—s⁻.

Each is a simple path. Under j and λj each vertex-link map is injective and its edge image is precisely the induced base-link subgraph. At A, the second square contributes {d⁺,q⁺} and {p⁻,e⁻}; the first contributes {p⁻,q⁺}. The first two are distinct and both needed. There are no omitted higher simplices because the base has dimension two and its link has no triangles. Thus both endpoint maps are local isometries under the injective/full-link characterization, and Q is locally CAT(0).

The edges p,q,s are a genuine spanning tree. Collapsing them sends the square relations to r⁻¹ and de⁻¹. Therefore π₁(Q,A) is infinite cyclic, with generator dp, and its endpoint images are bx and By. The homomorphism H=π₁K→Z sending b to 1 and x,y to zero proves bx has infinite order. This fixes the generator and not a finite-index power. These facts are also available independently through local-isometry injectivity. See lines 102–170.

### The entire quotient link, not only its graph

In Z = K ∪(Q×[0,1]), the four vertical edges z_A,z_B,z_C,z_D remain distinct open cells even though all their endpoints attach to the single base vertex. The edge products give six new squares; the two square products give two three-cubes. The cell count is exactly (1,7,8,2), with Euler characteristic zero. The latter is only a consistency check and is not used to infer asphericity.

I reconstructed link edges from all eight square boundary words and link triangles from **all sixteen individual characteristic three-cube corners**. This checks edge and triangle multiplicities before passing to sets. There are no loops, repeated link edges, collapsed triangles or distinct triangles with the same vertex set. In the second three-cube, the two A-corners at a fixed height share an apex but have different horizontal pairs, so their triangles are genuinely distinct. The saved evidence records cube index, corner index, height, Q vertex and each triangle’s signed germs.

The result is an actual simplicial link with 14 vertices, 32 edges and 16 triangles. Every triangle clique is present and there is no four-clique, hence no larger clique. Omitting either repeated A-corner would remove a required triangle; the independent negative control detects this. The theoretical explanation agrees: the link is the base link together with eight cones over injective full subcomplexes, one per signed vertical germ. No two apices are adjacent. A clique with an apex has its remaining clique in that full base and therefore spans its cone simplex. The proof does not confuse a triangle-count match with the simplicial-complex condition. See lines 172–218.

## 2. Attack on the full marked fundamental group

The two three-cells do not alter π₁. The two base square relators and all six edge-product relators were derived with the stated edge orientations. The fresh program performs literal reversible Tietze eliminations: a removed defining relation contains its removed generator exactly once, so solving and substituting is reversible. It eliminates z_B, z_C and z_D and records

z_B = xzY, z_C = Yzx, z_D = YxzYx, where z=z_A.

The remaining r-relation reduces to the identity using only xy=yx. Rotate the d- and e-relators so that they start in Z=z⁻¹. They become

D = ZbxzYb, E = ZybzbX.

The retained base relation bxB=y supplies yb=bx and bX=Yb, transforming E to D. Therefore discarding E is a certified redundant-relator elimination. The surviving presentation is exactly

⟨x,y,b,z | xyXY, bxBY, ZbxzYb⟩.

This records equality of normal closures through reversible changes; it is not only a forward homomorphism into the desired group.

Now set t=x, a=xY and c=(zx)⁻¹. The inverse substitutions x=t, y=a⁻¹t and z=c⁻¹t⁻¹ compose freely to the identity on all four generators in both directions. Under this free-group basis change, the first two surviving relators are cyclic conjugates of inverses of tat⁻¹a⁻¹ and tbt⁻¹b⁻¹a⁻¹. In the third transformed relator, use the retained second relation ab=tbt⁻¹. The result is cyclically equivalent, up to inversion, to tct⁻¹b⁻¹c⁻¹b⁻¹. Thus the entire presentation is equivalent to the exact target, with positive final b in φ(c)=bcb. These operations and intermediate words are saved in `independent-controls.json`; the handwritten chain in source lines 244–262 agrees.

A distinct exact check evaluates all eight geometric square relators in normal form (w,k) for F(a,b,c)⋊φZ, with multiplication (w,k)(v,l)=(wφᵏ(v),k+l). All are the identity, and both automorphism compositions pass. To ensure the check is not merely abelian, I replaced the proposed c-image by bcb[a,b], which has the **same exponent sums** as bcb. The corresponding target relation has nontrivial freely reduced residue and is rejected. The reversible Tietze certificate proves the isomorphism; the normal-form evaluation and mutant check corroborate its exact marking.

## 3. Global CAT(0), convention and properness interfaces

I directly read the relevant portions of [Leary author-v3](https://arxiv.org/pdf/1009.1540v3), including Appendix C’s convention and complete proofs of Theorem C.4, Theorem C.9 and Corollary C.11, together with their local/subdivision setup. The exact scope matches the manuscript:

* Theorem C.9, p.33, permits the general face-identified cube-complex convention and requires vertex links to be **flag simplicial complexes**. The explicit multiplicity check supplies that stronger hypothesis. Its proof also gives the CAT(0) universal cover.
* Theorem C.4, p.31, shows that a CAT(0) cube complex has embedded characteristic cubes with strict cubical intersections. Thus the universal cover satisfies the stricter convention.
* Corollary C.11, p.33, makes the second cubical subdivision of the locally CAT(0) quotient strict if desired. The original counts need not survive subdivision and are not claimed to do so.

The constructed quotient is finite, connected, three-dimensional and built from unit Euclidean cube shapes. Its cover has finite uniformly bounded local incidence and is locally finite. The resulting length metric is complete and proper; equivalently, in bounded dimension the cubical ℓ¹ and Euclidean path metrics are uniformly comparable, and finite combinatorial balls contain only finitely many compact cubes. There is no inference that a free action on an arbitrary cube complex is automatically proper. Here the deck action is free, properly discontinuous by covering theory, proper on the proper locally finite cover, and cocompact because its quotient is finite. The previous exact group isomorphism identifies this deck group with the whole target G, not a subgroup or finite extension.

## 4. Separate qualitative route through prior tools

Section 5 is not necessary for the explicit two-cube construction, but its claimed deduction was checked independently.

1. In H=⟨Z²,b | bxb⁻¹=y⟩, the HNN normal-form theorem embeds A₀=⟨x,y⟩. In the Bass–Serre tree, the edge from A₀ to bA₀ has stabilizer ⟨y⟩. For g=bx, gA₀=bA₀. Its translated edges concatenate into a bi-infinite path of strictly increasing b-height, so g is loxodromic. The adjacent incoming and outgoing edge stabilizers at A₀ are ⟨x⟩ and ⟨y⟩; their intersection is trivial in the embedded Z². Hence a specific two-edge axis segment has trivial pointwise stabilizer. This does not assume that the whole tree action is acylindrical.
2. The corrected [Minasyan–Osin v6](https://arxiv.org/pdf/1310.6289v6), Corollary 4.3 and its proof on pp.12–13 with Lemma 4.2, gives WPD for that specific loxodromic element from the finite segment stabilizer. No finite-extension result or uncorrected version is used.
3. [Dahmani–Guirardel–Osin v5](https://arxiv.org/pdf/1111.7048v5), Corollary 2.9 and Theorem 6.8, give the virtually cyclic hyperbolically embedded E(g). I read the definitions, elementary-subgroup lemma/proof and the complete Theorem 6.8 proof passage. The collection is a singleton, so pairwise noncommensurability adds no assumption. g has infinite order by b-height. [Sisto v1](https://arxiv.org/pdf/1310.7753v1), Theorem 1, applies because H is finitely generated and g lies in this virtually cyclic subgroup. I checked the Morse definition and the theorem/proof passages through the quasi-convexity deduction. This gives word-metric Morse behavior for g and quasiconvexity of the exact cyclic subgroup ⟨g⟩.
4. K has one vertex, so its universal-cover edge graph is the Cayley graph with the required generators x,y,b. The lifted bx circle contains ⟨g⟩ and has all intermediate vertices within distance one of it. Adding two bounded endpoint paths to a geodesic gives a uniform quasigeodesic between cyclic-subgroup points; the Morse property therefore controls geodesics between the lifted-circle vertices. This uses the combinatorial word metric, not an unjustified conversion from Euclidean CAT(0)-metric quasiconvexity.
5. [Ben-Zvi–Kropholler–Lyman v1](https://arxiv.org/pdf/2011.05374v1), Theorems 1.1 and 5.1, supply a **finite** pointed completion and a local isometry into finite K with fundamental-group image exactly ⟨bx⟩. I read the local-isometry definition, completion construction, relevant quotient/convex-hull passage and full Theorem 5.1 proof. Its maximal-tree generating set is exactly x,y,b here. This application needs existence, exact image and finiteness, not the strongest general uniqueness wording. The original two-edge bx circle is not a local isometry because b⁻,x⁺ span a missing base-link edge; completion, rather than the original circle, is used.
6. Postcomposing the same completed domain with λ retains compatible unit cubical structures at both ends and the exact second generator image By. It avoids separately completing the two cyclic maps with potentially incompatible domains. The same full-cone link argument makes the finite double mapping cylinder locally CAT(0); its dimension is at most three since its domain locally immerses in K. Van Kampen gives the already-checked HNN presentation and therefore G.

The [Hagen–Wise v3](https://arxiv.org/pdf/1605.07879v3) Remark 3.7, p.17, is consistent with this local-isometry gluing argument. Its Corollary 7.2, p.43, gives a free cubical action under its fast-automorphism hypotheses; that statement alone is not used to claim properness or cocompactness. I read both actual passages, including the corollary’s short proof. The abstract tools are prior results; this review does not date the first discovery of their exact application. Exact raw primary hashes, versions, URLs, pages and reading limits are in `evidence/primary-source-checks.json`. This is a check of the imported interfaces and relevant proof passages, not a fresh independent certification of every theorem in the long upstream papers.

## 5. Executed controls and limitations

Fresh `independent_controls.py` was written and run before inspecting the distributed programs. It exhaustively constructs the finite corner data, checks both endpoint link maps, multiplicities and all relevant cliques, records the repeated-A omission control, and produces the reversible presentation certificate and exact nonabelian negative control described above. The global CAT(0) and geometric-action conclusions remain deductions using the checked standard imports, not empirical conclusions.

After that independent work, I read and ran the three unchanged distributed mathematical programs: `packet/verify.py`, `packet/audit/independent_algebra.py` and `packet/audit/independent_audit.py`. All three passed in normal, `-O` and `-OO` modes: **nine successful runs**. The programs use explicit conditional exceptions rather than removable `assert` statements. The two geometric programs each report the same (14,32,16) link and 17 negative controls, while the algebra programs check the exact target relations and generator recovery. Their own stated limitations about forward homomorphisms were retained; the reverse equivalence is supplied by the independent reversible argument above.

Runs used disposable exact copies because two helpers regenerate result files beside themselves. Only those private copies were overwritten, and they were removed afterward. Raw stdout/stderr, newly generated outputs, program hashes, commands and timings are preserved under `evidence/`, with a nine-run summary. All three public assets and all 28 original extracted files were rechecked afterward. No historical result output or historical judgment supplied the current verdict.

## Final disposition

The strongest verified result is the precise explicit three-dimensional unit-cube model with quotient counts (1,7,8,2) under the stated face-identification convention, and a free, proper, cocompact CAT(0) cubical action of the **exact full marked group** a↦a, b↦ab, c↦bcb. The qualitative deduction through prior WPD/Morse/completion tools also has matching hypotheses.

**Substantive findings: none. Central unresolved gaps: none identified.** Historical firstness, minimality, current worldwide open status, virtual specialness, external human review and formal proof certification remain unestablished and are not consequences of these checks. No repair, follow-up conjecture, publication promotion, website/Sheet/Git change or external communication was performed.
