# Audit of the prescribed polygon bundle core partial result

Problem 10300012 / AMR-102-0012, Calegari Question 6.2, queue rank 1247.
Audit date: 10 October 2026 UTC.

## Verdict and exact scope

**ACCEPT the corrected note as a partial result in its stated closed orientable hyperbolic setting. The original base-manifold problem remains unresolved.** No fatal mathematical gap was found in the audited dependency chain after the completion-map and ambient-isotopy precision repairs described below.

The accepted conclusions are:

1. The prescribed ordinary core of the specified ideal-polygon-bundle complementary region has an unknotted universal lift (Proposition 2.3).
2. For each requested finite radius, a finite cover contains a homeomorphic lift of that same core which is isotopic to a simple closed geodesic with an embedded tube larger than that radius (Theorem 4.2). The geodesic has a noncoalescable insulator family when the radius exceeds log(3)/2.
3. The explicitly stated length/tube/primitive-class hypotheses imply the base-manifold isotopy and, with the additional radius threshold, the insulator conclusion (Proposition 5.1).

This is an independent AI-assisted mathematical audit. It is not a formal verification or human peer review. The acceptance imports the cited established theorems with the inspection limits recorded here. It does not certify novelty, an exhaustive literature search, or the full original conjecture.

### Distributed proof identity

The report distributed as [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md) has 27,528 bytes and SHA-256:

`07ddd342ba7a9a66a7c19ee86625155384f5ba1cd0857b970199dcc242ef9651`.

The proof-only edition retains the complete mathematical arguments, precise hypotheses, corrections and limitations. The acceptance applies to this mathematical content; editorial preparation adds no proof-search turn.

## Scope and imported product theorem

The note correctly distinguishes fullness from very fullness and restricts every claimed partial theorem to a closed orientable hyperbolic 3-manifold. Its specified core is the ordinary disk-bundle core isotopy class, rather than an arbitrary winding-one knot. A finite permutation of polygon sides is allowed.

The product-pair statement used in Section 2 is explicitly recorded in Calegari, Question 6.3, Remark (2), p. 12, with attribution to Gabai–Kazez. Calegari also explicitly states properness of the planar lamination. The use here is non-equivariant. No equivariant product structure is inferred.

The original Gabai–Kazez publisher PDF was unavailable to the author after HTTP 403. This audit did not obtain it through an alternate route and does not claim to have inspected its proof. Acceptance of Section 2 is conditional on the imported theorem as stated by Calegari. The author identifies that evidentiary limit accurately. [Calegari primary source](https://arxiv.org/abs/math/0209081)

## Complement injection and the completed boundary

### Lemma 2.1

The planar Jordan-curve argument is valid. A properly embedded complete line cannot be contained in the bounded disk of a Jordan curve lying in a complementary region, and it cannot leave that disk without crossing the curve. Thus every such bounded disk is free of the lamination. Approximating arbitrary loops by polygonal loops and splitting intersections gives simple connectivity of the planar complementary region. Its product with the line is simply connected.

The restriction of the universal covering to a complementary component is a covering of the original component. Its fundamental group is the kernel of the inclusion-induced map, so simple connectivity gives injectivity. In particular, the core generator is nontrivial. The stabilizer of its lifted embedded curve is precisely the image of its own fundamental group; this says nothing yet about the stabilizer of the hyperbolic axis.

### Lemma 2.2

The ambient orientation forces orientation-preserving polygon monodromy. A power fixes the finite ideal-vertex set. An orientation-preserving disk homeomorphism fixing those vertices is isotopic to the identity relative to them: first remove its boundary action, then use a disk isotopy relative to the boundary. Its mapping torus is therefore the required product for constructing the annulus. This cover belongs only to the completed complementary component.

The first precision repair explicitly introduces the universal cover W of the completed bundle. A boundary collar identifies the fundamental groups of the interior and completion. The completion map lifts from W to hyperbolic space; Lemma 2.1 identifies its interior with the actual chosen complementary component. Thus the annulus is not being transferred from an unrelated abstract cover.

The injectivity argument at a boundary side is sound in the stated cut-open, induced-path-metric completion. In a lamination box, two completion approaches through the same incident gap and same plaque side identify in the path-metric completion. The lifted boundary leaf is a proper plane and separates hyperbolic space. The connected complementary component cannot approach it from both opposite sides. Interior and boundary images are also disjoint. These observations give the needed embeddedness of the lifted annular strip. Surjectivity onto the whole boundary leaf is unnecessary.

A compact annular fundamental domain under the nontrivial deck transformation g^k makes the strip proper by proper discontinuity of the ambient group. This also makes its leaf-side boundary line proper.

The second repair specifies how to retain the original core. Extend the auxiliary core isotopy with compact support in the bundle interior, lift it, extend it by the identity across the lifted lamination, and apply its final inverse to the whole strip. The translated compact support pieces form a locally finite family. Their union is closed and misses the lifted lamination. The extension is therefore a genuine ambient isotopy, fixes the leaf-side boundary, and preserves properness and embeddedness. The wording avoids the incorrect literal assertion that the support itself has no accumulation points.

### Proposition 2.3

The leaf plane is ambiently unknotted by the imported product theorem and planar Schoenflies. A proper line inside it is unknotted by planar Schoenflies again. A proper locally flat strip admits a proper product neighborhood; a transverse compactly supported disk isotopy moves one boundary to the other. This is sufficient to establish unknottedness of the original lifted core. No simultaneous isotopy of all deck translates has been produced or assumed.

## Cyclic separation and compact tube embedding

Published Agol Corollary 1.3 has the required non-elementary, word-hyperbolic, proper cocompact cubulation hypotheses. They hold here; Theorem 9.3 supplies cubulation for a closed hyperbolic 3-manifold group. The published numbering, pages 1046 and 1065, was checked. Every infinite cyclic subgroup is quasiconvex, including a proper finite-index subgroup of a maximal cyclic subgroup. Therefore the separation input genuinely applies to the subgroup generated by g, even when g has a root. [Published Agol paper](https://ems.press/content/serial-article-files/26202?nt=1)

The compact-fundamental-cylinder proof of Lemma 3.2 is correct. Only finitely many ambient deck transformations make that cylinder meet itself. Separate the members outside the chosen cyclic subgroup, then intersect the corresponding finite-index subgroups. If two points of the full tube are identified, translating each into the cylinder reduces that identification to one of the retained finite collision set. The reduced element lies in the cyclic subgroup, which forces the original identification to lie there too. Compactness then upgrades injectivity of the tube quotient to an embedding.

This is actual cyclic subgroup separability. Residual finiteness alone and separation of only the maximal cyclic subgroup would not justify the same proof for a proper power.

### Proper powers and the chosen lift

Once the cyclic tube embeds, its axis stabilizer in the finite-index subgroup is exactly the chosen cyclic subgroup. An additional root would identify distinct points on its core. Thus g becomes primitive in this particular finite cover, despite remaining nonprimitive in the original group.

Since the finite-index subgroup contains the full image of the fundamental group of the specified embedded circle, that circle has a degree-one lift. This establishes the homeomorphic projection claimed in Theorem 4.2. The cover need not be normal. The note correctly refuses to pass to the normal-core cover without changing and tracking the lift degree.

## The winding one Core Lemma

The use of Funar–Gadgil Lemma 4.2 is valid in the stated orientable solid-torus setting. Their surrounding use of “geodesic” means topological geodesic; Theorem 4.3 separately requires a primitive class. The note does not silently remove that requirement. [Funar–Gadgil primary PDF](https://arxiv.org/pdf/math/0106163)

The supporting group and peripheral checks pass. Winding one gives one lifted strand in the lifted cylinder. Adjoining the exterior of that standard cylinder changes neither generators nor relations, since its annular boundary inclusion is a fundamental-group isomorphism. Unknottedness gives cyclic kernel. The extension over the longitude splits and its action preserves an oriented meridian, giving Z squared. The compact exterior is irreducible because the winding-one knot cannot lie inside a ball. The inner and outer meridians each map to a generator of the kernel; either longitude maps to a generator of the quotient. Both peripheral maps are therefore injective. The final two-torus-boundary product characterization is the imported solid-torus conclusion of the cited Core Lemma. These checks do not use base-group primitivity after the tube is embedded.

## Virtual assembly and quantitative criterion

The cyclic lift of the prescribed circle is compact. Hence a finite radius contains it strictly in the cyclic tube. Choosing a larger radius than this bound, the requested radius, and log(3)/2 is legitimate. The embedded image has winding one; its universal lift remains unknotted. The Core Lemma applies inside that very tube. The result is the stated simple geodesic in the finite cover and does not change which core is being lifted.

One traversal of the lifted rectifiable circle gives d(x,gx) at most its length A. The strict proposed inequality therefore forces every point of the lifted circle to lie strictly within the radius-r tube. The primitive-class and embedded-tube hypotheses ensure that its winding in the tube is one. The Core Lemma then gives isotopy, not merely free homotopy. Dropping the nonnegative rotational term yields the correctly stronger rotation-free sufficient condition.

## Insulators and remaining obstructions

Gabai–Meyerhoff–Thurston Example A.3, p. 428, supplies the Dirichlet insulator conclusion for a simple closed geodesic whose tube radius exceeds log(3)/2. That strict inequality is respected. Its application here does not require the geodesic to be shortest. The separate shortest-geodesic theorem does not identify a prescribed lamination core. Definitions A.1–A.2, pp. 427–428, were visually inspected. [Primary Annals PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v157-n2-p01.pdf)

The argument in Section 6.2 is correct: the two convexity circles lie in different components of the separating Jordan curve and hence are disjoint. Their hyperbolic planes, and the axes inside them, are disjoint. An arbitrary topological leaf does not supply this round-circle separation, equivariance, local finiteness, or the no-trilinking condition.

The helical comparison curve in Section 6.1 is embedded, represents a proper power, and has unknotted universal lifts, since each lift is a graph in global cylindrical coordinates. It therefore correctly demonstrates that individually unknotted lifts do not imply primitivity or base-manifold geodesic isotopy. It is expressly not a lamination counterexample.

The Fenley–Pinsky–Shannon preprint and Proposition 7.1 construction were checked as a literature caution only. The cited pages describe the surviving orbit as the boundary of a Möbius band after the hyperbolic construction. This does not establish the genuine polygon-bundle lamination hypothesis, and neither the paper's entire proof nor that extra implication is accepted here. [Preprint record](https://arxiv.org/abs/2607.28139)

The following remain unproved for the prescribed core in the base manifold:

- primitivity of its class;
- embeddedness of its geodesic image;
- simultaneous full-group-equivariant straightening of the lifted curve configuration;
- descent of the finite-cover isotopy;
- extension of the finite-index insulator family to the full group;
- automatic satisfaction of the quantitative tube inequality.

No statement in the accepted note resolves these obligations. Its unresolved first-attempt status is the correct one.

## Reproducibility and inspection record

Four primary PDFs were independently retrieved during this audit from their public sources. Each exactly matches the author's retained bytes and SHA-256: Calegari, Funar–Gadgil, published Agol, and Gabai–Meyerhoff–Thurston. The exact byte counts, hashes, public URLs, retrieval times, and match results are recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json). The additional preprint's retained byte identity and the separately checked public version record are also recorded there.

Visual inspection covered Calegari p. 12; Funar–Gadgil pp. 376–377; published Agol pp. 1046 and 1065; and Gabai–Meyerhoff–Thurston pp. 427–428. Extracted primary text supplied the other stated definitions, theorem hypotheses, and source locations. This does not represent a proof audit of every cited paper.

This edition includes authored mathematical analysis and public source-verification metadata. It excludes copied scholarly sources and supplemental computational material. Recorded scholarly retrieval and inspection are historical observations; editorial preparation makes no new source-retrieval, PDF-rehash, source-inspection or literature-search claim.
