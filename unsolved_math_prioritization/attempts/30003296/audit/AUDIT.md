# Independent audit: complete surfaces in genus-four moduli

Problem 30003296 / OWR-15177-013. Rank 630. Audit date: 4 October 2026.

## Decision

**PASS AS AN UNSOLVED, LIMITED-SCOPE RESEARCH RECORD.** No fatal mathematical error or required mathematical repair was found in the frozen packet. This is not acceptance of an existence theorem, a nonexistence theorem, or a novel solution. The target remains unsolved; five approach families have been used.

The accepted conclusions are necessary conditions on a hypothetical surface and obstructions to the particular constructions described. Neither a complete surface in abelian moduli nor a nodal surface in compact-type curve moduli resolves the target. No new search route is being charged by this audit.

The audit is bound to these exact author bytes:

- `SHA256SUMS.json`: `77864bb9f2bd0493b64b8bdd73c004e03a9e0125374929ff37a05d165c3bf70f`
- `PARTIAL.md`: `f5d33306717ca687719748155444b7f41ade41c87cee49e2a5ec79fcd089801d`
- Twelve regular files, including the manifest; eleven payload hashes in the manifest.

Every author file was read. Both author verifiers were replayed successfully. The independent control program passed 88 assertions, including checks that do not merely repeat the author program. The original files were not changed. No remote writes were made.

## 1. Source identity and scope

The primary question is Dawei Chen's Question 8 on printed page 3188 of the 2016 Oberwolfach report *Surface Bundles*. The printed page was visually inspected. It asks about a complete complex two-dimensional subvariety of M4. The adjacent Question 9 concerns A4, so exchanging those targets would be a substantive error. The official report metadata gives volume 13 (2016), pages 3149–3195. The packet's treatment of the catalogue's 2017 label is reasonable. [Official record](https://publications.mfo.de/handle/mfo/3560)

The target is the coarse moduli space of smooth, connected, unmarked genus-four curves over C. Its dimension is 9. A complete subvariety is projective because the ambient space is quasi-projective. No smoothness condition on the sought surface is in the question. It is sufficient to consider integral surfaces: any reducible example of dimension two would have an integral two-dimensional component. A compact analytic subvariety becomes a closed analytic subset of a projective compactification and is algebraic by Chow's theorem.

The finite-level-and-resolution reduction is valid. A finite full-level cover supplies a universal smooth curve. An irreducible component over a hypothetical surface is projective; resolving it gives a smooth projective base with two-dimensional image. Pullback preserves smoothness of the curve family. Exceptional curves of the resolution may be contracted by the classifying map, so generically finite, rather than an embedding, is the correct condition. Conversely, a family over a projective surface with two-dimensional classifying image has a proper image of the requested type.

The current arXiv landing page still identifies GMST v3, dated 21 November 2025, as the latest version. Its Section 9.1 and Table 5 were checked against the saved text and live primary HTML. They support compact dimension 2 for the indecomposable abelian locus in genus four and retain the lower/upper bounds 1 and 2 for smooth-curve moduli. They do not resolve Chen's question. This is a dated source check, not an exhaustive literature certificate. [Versioned GMST text](https://arxiv.org/html/2404.06009v3)

The selected catalogue record's canonical JSON digest was independently recomputed and agrees with the source manifest. The four saved primary PDFs also agree with their recorded SHA-256 digests. This audit did not independently rehash the complete imported catalogues or repeat the historical repository duplicate search; it checked the selected records and the supplied repository-gate receipt. No stronger provenance claim is made.

## 2. Route 1: affine strata and positivity

**Accepted.** Fontanari–Looijenga Theorem 3.1 and Corollary 3.2 have the hypotheses and content attributed to them. The relevant theorem page was visually inspected, and the proofs on the following pages were read. Their three affine successive strata and rational Chow-ring computation apply over C. [Author manuscript](https://webspace.science.uu.nl/~looij101/affinestrat3.pdf)

The packet's consequence for a possibly singular integral projective surface S is correct:

1. The closed intersection with the hyperelliptic locus H is both proper and affine, so it is finite.
2. If S were contained in the thetanull divisor D, a general very ample curve section of S could avoid that finite set. It would be a complete curve in the affine stratum D minus H, which is impossible.
3. Once S is not contained in D, its intersection with D is proper and has dimension at most one. If it were finite, another very ample curve section could avoid it, contradicting affineness of M4 minus D. Hence a complete curve occurs.
4. Such a curve cannot lie in H or avoid H. Its generic point is therefore nonhyperelliptic and lies on the canonical quadric cone. It meets H in finitely many points. In particular S meets H nontrivially.

These arguments require neither smoothness nor normality of S. General hyperplanes avoiding a prescribed finite set exist over C and still cut a positive-dimensional projective surface in a nonempty curve.

The important negative control is P2 with the filtration P2 containing P1 containing a point. Its three successive pieces are affine, yet P2 is itself a complete surface. Similarly, its Chow ring has a nonzero square of the hyperplane class and zero cube. These countermodels show exactly why three affine strata and a vanishing cube cannot force compact dimension at most one.

The positivity statement is also consistent: on a complete subvariety of smooth-curve moduli, the Torelli map to Satake has finite fibers, and the Hodge class comes from an ample rational line bundle there. Its square on a surface can have positive degree. A zero ambient Chow class does not contradict this. The map from a nonproper ambient space to a point has no general proper degree pushforward; the class of a point on A1 is the elementary counterexample used in the packet.

**Remaining gap:** exclude the actual complete curve configuration in D, or prove that it cannot extend to S. The filtration does neither. The substantial overlap with the related record 20000117 is expressly acknowledged and must not be recast as new progress.

## 3. Route 2: Satake cuts and Schottky sections

**Accepted with the stated component limitation.** The dimensions are correct. The Jacobian closure X has dimension 9. The closure of the elliptic-times-genus-three Jacobian locus has dimension 7 and lies outside the smooth Jacobian locus. Seven sufficiently general hyperplanes therefore leave a surface in X and cut a nonempty zero-cycle on this projective boundary component. Positivity of its projective degree, rather than an informal expected-dimension slogan, supplies nonemptiness. Eight hyperplanes can avoid it but leave only a curve in X.

The independent check enumerates all decomposable partitions of 4: their dimensions are 7 for 1+3, 6 for 2+2, 5 for 1+1+2, and 4 for 1+1+1+1. Satake boundary strata have dimensions at most 6. This validates the maximum bad-locus dimension 7. Eight general hyperplanes in the ten-dimensional ambient A4 Satake space can consequently produce a complete indecomposable surface, without making that surface Jacobian-valued.

The cited GMST argument specifically gives the dimension-at-most-two statement for compact subvarieties avoiding the elliptic-times-threefold product locus. Its contrapositive applies to every complete threefold Z in A4. Every ppav of dimension at most three is a product of smooth Jacobians, so this product locus is contained in the compact-type Jacobian image and hence in the Schottky locus. If the Schottky section of Z is an irreducible surface, the forced product point makes it unsuitable.

For a reducible section, the packet correctly stops. A point in a union lies on at least one component, not necessarily on all components. The independent projective countermodel uses the divisor x0*x1=0 in P3 and the point (0:1:0:0): one plane contains the point and the other does not. This is only a check of the invalid quantifier, not an example in A4.

If Z is already contained in the Schottky divisor, cutting by its equation does not produce a surface at all. The packet's conditional wording avoids claiming otherwise. A noncontained two-dimensional Prym or abelian image normally cuts down to a curve; obtaining an entire surface requires the missing containment condition.

**Remaining gap:** find a complete two-dimensional component entirely in the smooth Jacobian locus, or exclude every possible such component. General linear sections and the threefold theorem do not do this.

## 4. Route 3: coverings and automorphisms

**Accepted.** The proof for configurations on a fixed curve is sound. Projection to the first coordinate has fibers that are complete subvarieties of a quasi-affine configuration space on a punctured curve. A proper quasi-affine variety is zero-dimensional. Thus the projection has zero-dimensional fibers and the complete configuration subvariety has dimension at most one. A finite ordering cover preserves properness and dimension, so unordered branch sets are covered as well.

For a complete family with genus-two targets, the map to the affine M2 is constant. After obtaining a family and a finite base change, the isotrivial target can be fixed because a genus-two curve has a finite automorphism group. For fixed target and branch divisor, the remaining double-cover data are finite. It follows that this construction cannot have two-dimensional moduli image.

The general automorphism argument has the needed finiteness qualifications. A nontrivial finite group contains an element of prime order; there are only finitely many possible prime orders. On a suitable finite level cover, a component of the relative automorphism scheme chooses such an automorphism. Its quotient genus and branch data are locally constant on the resulting connected family. Branch orderings can be chosen by a further finite cover. Fixed quotient and fixed branch data determine only finitely many cyclic covers. These steps preserve a complete two-dimensional source and hence require a complete two-dimensional image in the corresponding pointed quotient moduli.

The Riemann–Hurwitz list is exhaustive without a large numerical cutoff. From 6=p(2h-2)+r(p-1), one has h at most 2. For h=0, p-1 divides 8; for h=1, p-1 divides 6; for h=2, p is at most 3. These give exactly the eight triples recorded in the packet. The sole one-branch triple, (7,1,1), is impossible: the relation in the punctured quotient surface group forces the sum of its local monodromies to be zero in the cyclic group, whereas the only branch monodromy must be nonzero. The unramified (3,2,0) case must not be discarded; its finite covering data over a fixed target still prevent a surface.

For h=0 the ordered pointed quotient space is affine. For h=1, fixing the first marked point leaves a quasi-affine punctured-elliptic configuration space over a constant elliptic modulus. For h=2, the fixed-target configuration bound applies. These arguments agree with Zaal's Lemmas 6.4–6.5 and Theorem 6.6; the relevant statements and proofs were read. [Thesis record](https://dare.uva.nl/id/502659b5-ce0a-492e-8042-b670058cb4fd)

**Remaining gap:** no argument applies to every generically automorphism-free surface, to every non-Galois construction, or to every degeneration of covering data. Meeting the automorphism locus in a proper subset is not excluded.

## 5. Route 4: Prym compression

**Accepted as a conditional diagnostic and an explicitly cited special-case rejection.** A degree-two cover of a genus-four curve with two branch points has genus eight; the Prym dimension is four. In the two-branch-point case the restriction of the Jacobian polarization has type (2,2,2,2), and its standard half is the principal Prym polarization. Thus the packet's map to A4 uses a valid conventional normalization. This normalization is an optional explanatory clarification, not a repair. A modern primary account confirms the principally polarized two-branch-point construction. [Lange–Ortega, Introduction](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/blms.12756)

A nonzero section of an invertible sheaf on an integral surface is locally a non-zero-divisor. Its zero scheme is an effective Cartier divisor or empty, so it cannot have the entire surface as its support. Passing to an appropriate finite level cover and an integral component makes the modular line bundle language literal. Consequently the Schottky section must vanish identically for a two-dimensional image to be wholly Jacobian-valued. Avoidance of decomposables is a separate requirement. Neither properness of the source nor the arithmetic dimension four supplies these requirements.

Zaal's Theorem 7.6 was checked in its actual Section 7.2.2 context, including its proof. Its statement is about the genus-eight families obtained from the specified Chapter 2 tower. The packet cites that statement with the same restriction and explicitly disclaims an independent reconstruction of the trigonal/Prym characterization invoked in the source proof. This is acceptable citation-dependent mathematics; the audit is not certifying that external theorem from first principles. Even omitting that citation leaves the general Schottky containment diagnostic intact.

Choi's primary introduction and characteristic-zero discussion were checked. The improved construction theorem is in positive characteristic, and the marked-curve surface theorem has both a positive-characteristic condition and at least one marking. Neither supplies the required complex unmarked surface. The versioned abstract still labels the submission v1 from 2023; the later date generated in the HTML does not identify a new arXiv version. [Choi, versioned text](https://arxiv.org/html/2304.08568v1)

**Remaining gap:** a different complete family with two-dimensional Prym image, identical Schottky vanishing, and no decomposable fibers. The cited tower obstruction is not a universal theorem against Pryms.

## 6. Route 5: smoothing a boundary surface

**Accepted for the stated fixed parameterized family.** Gluing fixed nonisomorphic genus-two curves at moving points gives stable compact-type curves of genus four. There is exactly one separating node. Nonisomorphism prevents interchanging the two components, and their finite automorphism groups ensure finite clutching fibers. The proper image has dimension two but consists entirely of singular curves. Its polarized Jacobian is the fixed product, so its Torelli image is zero-dimensional.

The normal smoothing line on the family is the tensor product of the two tangent lines at the node. In the local equation xy=t, the smoothing tangent is dual to the product of the two cotangent directions. This gives pr1*T(C1) tensor pr2*T(C2), not its dual. The restriction to either ruling has degree -2. A global section restricts to zero on each ruling and is therefore zero everywhere. The resulting H0 vanishing supplies the asserted first-order obstruction.

The appropriate interpretation is deformation of the given family as a morphism to the stack of stable curves, equivalently the ordered clutching calculation. Coarse-space quotient singularities do not turn this into a statement about every arbitrary coarse map. The packet's explicit reference to the fixed parameterized family and the ordered clutching cover is sufficient. The formal clutching source was checked for its actual normal-bundle and infinitesimal-neighborhood framework. No genus-one-only formal splitting theorem is being silently applied to the genus-two-plus-genus-two case. [Polishchuk, Introduction and Section 4](https://arxiv.org/html/2110.04682v3)

**Remaining gap:** this rejects the advertised simultaneous first-order smoothing mechanism. It is not a classification of all complete surfaces or all possible degenerations. The packet correctly makes no such claim.

## 7. Reproducible checks and limits

Run `python3 independent_checks.py --author-dir PATH_TO_AUTHOR_PACKET` with Python's standard library. With the original layout, omitting the argument selects the sibling `submission` directory. The program only reads files and runs the two read-only author scripts. It does not require the saved sources or the imported catalogues.

The 88 successful assertions cover:

- Exact frozen identity, allowlist, eleven payload hashes, and before/after immutability.
- Both author verifier outputs and their agreement with the recorded controls.
- Unsolved status, the five distinct route entries, and the 1–2 smooth-curve bounds.
- A cutoff-free Riemann–Hurwitz derivation.
- Direct enumeration of zero-sum nonzero local monodromies for all ramified triples. The ordered-vector counts are 1, 1, 1, 22, 2, 52, and 0 in the applicable order. These are not counts of isomorphism classes of covers or automorphism-locus components.
- The nonzero characters for the unramified genus-two triple: 3^4-1=80. This is not a count of unlabelled covers.
- All decomposable partitions and Satake boundary dimensions relevant to A4.
- The seven-versus-eight hyperplane threshold, separating the nine-dimensional Jacobian closure from its ten-dimensional abelian ambient space.
- Elementary affine-filtration, truncated-ring, and reducible-component countermodels.
- Double-cover genus, Prym dimension, normal-degree signs, and publication-safety scans.

These are exact arithmetic and logic controls, not a formalization of moduli theory. A passing program does not prove affineness, the Schottky theorem, GMST, Zaal's Prym characterization, the theory of level structures, or deformation-theoretic descent. The human-readable audit supplies the hypothesis and inference review. No proof-assistant certificate or peer review is claimed.

## 8. Corrections and publication safety

There are **no required corrections**. `CORRECTIONS.md` records two optional clarifications: the Prym polarization normalization and explicit stack language for the first-order deformation statement. Neither changes the accepted claims, target, or verdict. The author packet remains unchanged, including its historical `independent_audit: pending` marker. This audit is the separate later assessment; an edited publication copy must receive a new manifest and a checked binding.

The exact safe author file list and audit file list are in `AUDIT_MANIFEST.json`, with SHA-256 hashes and byte counts. The audit manifest excludes itself from its internal file list; its own digest is supplied separately with delivery. Its author binding is to the original author manifest and canonical note above.

Source PDFs, full-text extractions, source-page images, imported catalogue records, the related prior report, repository-gate responses, and private coordination are excluded. Only original analysis, source links, hashes, and small verification programs belong to the audit publication allowlist. The OWR and thesis access notices were inspected and are compatible with private reading; this review does not authorize redistribution of those source files. No credentials or private local directory paths occur in the written audit documents.

A future publication should retain the unsolved status and exact scope. It must not relabel this packet as a solution, present the affine observation as novel, identify a compact-type or abelian-moduli example with the smooth target, or infer a mathematical resolution from passing controls.

**Final target gap:** no proper two-dimensional subvariety wholly in M4(C) has been constructed, and no argument excludes every such subvariety, including singular ones.
