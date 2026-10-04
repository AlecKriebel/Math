# Independent adversarial audit: 2887 / KP-4.11

Audit date: 2026-10-04 UTC. Frozen author package: `submission/`.

## Verdict and binding scope

**The corrected, explicitly scoped package passes as an UNSOLVED five-turn partial attempt. The frozen text does not receive an unqualified mathematical PASS.** Two imported theorem invocations omit compactness as written. The four exact editorial replacements in `CORRECTIONS.json` repair that issue and make clear that the original problem has not been narrowed. `CORRECTED_FULL_PROOF.md` is the checked replacement; `CORRECTIONS.patch` is the equivalent unified diff. Neither a new construction nor a sixth proof attempt is included.

The recommended result remains `unsolved`, `5/5`, no complete candidate, no novelty claim, and no verified resolution of either part. Publication of the mathematical narrative requires these corrections or their exact equivalent, alongside the audit. This verdict does not authorize remote publication, repository changes, or source redistribution.

The binding hashes are:

- Frozen `SHA256SUMS.json`: `52c4ae34c6121c939de807a6de494299c3e80f727566cda09341304591c45104`.
- Frozen `FULL_PROOF.md`: `ab2f3befa08c9974374640315456f615dd9e43defc9bc76c5e06bcb8e3e7cf8f`.
- Corrected replacement: `0279d4c723364dfd32ff5500f01fcc01dcd5752166e65c53a049edd5c0a6f4c1`.

## 1. Exact target and domain

The primary K3 page 199 was checked in text and pixels. Part (a) asks for an orientable smooth ambient manifold whose single Gluck twist gives a homeomorphic, non-diffeomorphic manifold. Part (b) asks for homotopic smooth spheres in an orientable ambient manifold whose two twisted results form such a pair. The second part does not require either result to be homeomorphic to the untwisted ambient manifold. The requirements of orientability, smooth embeddings, trivial normal bundles, and homotopy in part (b) are essential.

The statement imposes neither closedness nor compactness. The general introduction, Chapter 4 introduction (pp.189–190), and Section 4.1 conventions (p.191) were also inspected; no blanket compactness assumption was found. This does not prove the editors' unexpressed intentions about open manifolds. It does mean that the audit must not silently replace the stated problem by its compact or closed subcase. The corrected text preserves the broad target, and explicitly identifies which deductions are only verified for compact or closed manifolds. No noncompact classification, homeomorphism, or smooth-triviality theorem is established by the imported compact statements.

The pinned ID 2887 and its statement match the locally available corpus. The AIM workshop report is not the full K3 problem text. Direct catalogue availability and current catalogue status are not certified by this audit.

Source: [K3 primary preliminary version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

## 2. Integrity, provenance, and control replay

All 12 author-manifest file records were independently hashed and matched. The manifest's own SHA-256 matches the assigned freeze. The six private PDFs used for K3, KPR, AY, Gabai, AKMR, and Torres match the source manifest in both length and SHA-256. No source copy was inserted into the audit or corrected artifact.

The two pinned corpus files were independently hashed: their 68,931,837-byte and 80,334,822-byte identities match the author's source gate. The exact problem statement matches the selected record; the 6,701-entry report mapping has no `KP-4.11` or `2887` key. This audit does not certify that every differently named report is absent. The repository duplicate checks and queue observations remain the author's time-stamped observations, not a newly repeated live repository survey.

Both author programs were read before execution. `verify_manifest.py` passes, and `verify.py` reproduces `CONTROL_RESULTS.json` byte-for-byte. Independent polynomial-coefficient algebra checks the bundle shear for all symbolic variables rather than a bounded sample; a separately implemented pairing calculation checks the odd-stabilization basis and determinant; the expected-dimension change is zero exactly. These controls provide no smooth-topological or gauge-theoretic oracle. In particular they cannot certify a homeomorphism, a Kirby-diagram move, an exotic sphere, or an invariant evaluation.

## 3. Mathematical deduction audit

### 3.1 Fundamental group, Euler characteristic, and signature

The meridian quotient is correct. The chosen pole gives a based meridian fixed by the twisting map, and both fillings kill precisely its normal closure. The exterior is connected; codimension-two removal does not disconnect the connected ambient manifold. Compactness is stated where finite Euler characteristic is invoked. Oriented compact signature additivity applies along the closed separating gluing 3-manifold, also when the original manifold has other boundary components. These facts alone do not identify an integral intersection form. No failure was found in Proposition 1.1.

### 3.2 Closed simply connected null-homologous case

Proposition 1.2 passes. For the pair consisting of the manifold and the exterior, the relevant relative groups are H3=0 and H2=Z. The map into the latter is intersection with the sphere class, hence zero. Exactness therefore identifies the two absolute second homology groups and identifies the exterior's first homology with Z generated by the meridian. The boundary sphere is zero in the exterior's second homology because its image is zero and the inclusion is injective.

In the twisted Mayer–Vietoris sequence, the degree-two map has the integral unit component into the tubular neighborhood, while the degree-one boundary map is an isomorphism. This proves integral, not merely rational, homology identification. Closed cycles can be pushed into the common exterior's interior, preserving signed intersection counts. The form is therefore the same on both closed simply connected smooth manifolds. Both Kirby–Siebenmann invariants vanish. The invoked topological classification gives an orientation-preserving homeomorphism; its full proof is an external input.

The closedness and simple connectivity cannot be dropped by this argument. There is no compact-with-boundary classification assertion hiding in it. Since the integral forms agree here, parity and the spin/nonspin type agree as well. This preservation is not asserted for arbitrary Gluck twists.

### 3.3 Essential fibre negative control

Proposition 1.3 passes. The clutching loop changes the trivial oriented sphere bundle over S2 to the nontrivial one. A pole section's vertical normal plane has odd Euler number, producing the stated odd form. The product bundle has an even form. Changing the sign of the section convention does not repair the parity mismatch, and reversing orientation does not turn an odd lattice into an even one. Thus the twist changes the homeomorphism type: the product's spin type becomes nonspin. Equal fundamental group, Euler characteristic, and signature do not make this a qualifying exotic pair.

### 3.4 Local knots and the homotopy-sphere reduction

Proposition 2.1 passes. The outer ball boundary and collar are untouched, so capping the modified ball and regluing the punctured manifold give the connected-sum identity. The knot exterior's Alexander-duality homology, unit meridian maps, and the meridian quotient give a simply connected integral homology 4-sphere. Hurewicz and Whitehead yield the homotopy-sphere statement, followed by the external topological 4-dimensional Poincare theorem.

The unknot's boundary rotation extends across its exterior. The relative-ball conclusion uses the standard adjustment of an orientation-preserving diffeomorphism to fix a chosen ball, as in KPR Proposition 1.5; it does not assume the smooth Schoenflies conjecture. In S4 both knots represent the zero class in pi2, so a nonstandard Gluck sphere really would supply both requested examples. No such sphere has been established, and the deduction is not equivalent to every possible exotic homotopy sphere arising by a Gluck twist.

### 3.5 Odd spherical classes and projective-plane stabilization

AY Theorem 1.1 assumes a **compact connected smooth** ambient 4-manifold. Its odd class lies in the sphere-surgered manifold and is spherical. The frozen invocation and Proposition 3.1 omit compactness. Their supplied proof merely applies AY and does not supply a noncompact extension. This is a source-hypothesis gap, not a counterexample to the stronger assertion.

After the explicit scope correction, the disjoint odd sphere supplies the needed class. Corollary 3.2 already assumes compact connected oriented M and therefore passes unchanged: a projective line in a connected-sum summand gives the disjoint square +1 or -1 sphere, and disjointly supported twisting commutes with that connected sum. No cancellation is justified. An arbitrary odd homology class of the original ambient manifold is not a substitute for the source hypothesis.

Source: [Akbulut–Yasui, Theorem 1.1](https://arxiv.org/abs/1205.6038).

### 3.6 Homotopy, concordance, isotopy, and dual spheres

KPR Theorems 1.1–1.2 assume compact M; this must be stated in the frozen section-4 summary. Concordance and the resulting s-cobordism belong to the chosen smooth or locally flat category. A good fundamental group supplies a topological product conclusion, not a smooth one. The closed orientable cyclic-fundamental-group corollary is correctly identified. Homotopy alone is not made into an unrestricted homeomorphism theorem.

Proposition 4.1 passes: transporting the tubular parametrization by the ambient isotopy makes the two gluings commute. Oriented normal trivializations differ by a null-homotopic map from S2 into SO(2). Gabai's published theorem is invoked with orientability, absence of order-two elements, and one common embedded transverse square-zero sphere. An algebraic dual, separate duals, or an unframed sphere does not supply those hypotheses. The S2 x S2 example satisfies them. Nonisotopic spheres still need not yield non-diffeomorphic unmarked twisted manifolds.

Sources: [KPR author manuscript](https://www.maths.gla.ac.uk/~mpowell/gluck-paper.pdf), [Gabai published offprint, Theorem 1.2](https://web.math.princeton.edu/facultypapers/Gabai/Light.Bulb.pdf).

### 3.7 Ordinary Seiberg–Witten obstruction

Proposition 5.1 passes with its stated closed, oriented, simply connected, b2+>1, null-homologous hypotheses. AKMR Lemma 2.3 and its diagram were checked in text and pixels. The common blown-up manifold has two blowdown descriptions, with the proper transform representing the exceptional class up to sign. The common exterior maps to the same orthogonal complement. The usual +/- exceptional lifts have matching ordinary blowup coefficients and unchanged expected dimension. Compatible homology orientations are necessary and explicitly chosen. Simple connectivity removes torsion ambiguity in identifying spin-c structures by first Chern classes. No simple-type assumption is needed for the matching +/-1 exceptional lifts in the ordinary blowup formula.

No chamber-free b2+=1 result, boundary theory, or extension to relative/family invariants is certified. The Kirby move and gauge-theoretic blowup theorem remain external inputs, not consequences of finite matrix checks. The author's manuscript classification is appropriately cautious: Melvin's current research page independently labels the 2018 work unpublished.

Sources: [AKMR manuscript](https://pmelvin.blogs.brynmawr.edu/files/2022/05/2018June14ExoticEmbeddings.pdf), [Melvin's research list](https://pmelvin.blogs.brynmawr.edu/research/).

## 4. False-positive literature and orientability checks

KPR Proposition 1.6 has the required homotopic smooth spheres and exotic output pair, but its ambient manifold contains the RP4 summand and is nonorientable. Proposition 1.4 is orientable but its outputs are not homeomorphic, and it is formulated for locally flat embeddings. Neither meets the requested target. Source: [KPR](https://www.maths.gla.ac.uk/~mpowell/gluck-paper.pdf).

Torres Theorem A concerns closed nonorientable manifolds, and explicitly identifies their orientation double covers diffeomorphically; the covers admit spin structures. The current Cambridge record confirms online publication on 26 March 2026 and the stated volume/pages. Those total cover endpoints do not give an orientable exotic pair. A lifted surgery involves the two lifts of the sphere neighborhood; equality of the final covers is not a theorem that every individual lifted twist or every other covering construction is trivial. The frozen report makes no such stronger claim. Source: [Torres publisher record](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/exotic-nonorientable-fourmanifolds-with-prescribed-fundamental-group/7F23726D4C8144677E17B1482E74C9F9).

The bounded search did not reveal a verified exact solution. This is not an exhaustive still-open certificate. Institutional publication records confirm the KPR 2023 volume and 2024 online publication dates. The AKMR argument has not been silently attributed to the different later embeddings paper.

## 5. Correction and publication gate

The four replacements are the complete required correction set:

1. Section 0: preserve the full domain, explicitly noting the lack of compactness in the target and limiting only the imported deductions.
2. Section 3 AY invocation: add compact connected smooth M.
3. Proposition 3.1: add compact and connected M.
4. Section 4 KPR summary: add compact connected M, keep the normal-bundle condition, distinguish concordance categories, and disclaim an asserted noncompact extension.

The corrected prose is accepted only as a partial attempt. It neither resolves a compact case nor excludes possible noncompact examples. The already compact stabilization corollary, closed null-homologous homeomorphism proposition, and restricted SW proposition need no theorem-level correction.

The original files remain unchanged. `verify_audit.py` checks the frozen input, the four exact substitutions, the corrected hash, and both sets of algebraic controls. `AUDIT_SHA256SUMS.json` binds the separate audit artifacts. All source PDFs, source text, images, selected/full corpora, raw API records, and private coordination remain excluded from publication. No remote writes were made. No helper was spawned. External theorems were checked for applicability; their complete foundational proofs were not rederived or formally verified.

**Final status: UNSOLVED 5/5. PASS applies only to the corrected scoped partial bundle.**
