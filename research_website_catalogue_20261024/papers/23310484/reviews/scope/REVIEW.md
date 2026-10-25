# Publication-scope review: missing faces and sphere skeleta

Checkpoint: 2026-10-24T23:51:21Z. Scope-review completion estimate: 100%. Overall catalogue work remains in progress.

## Verdict and independence

PASS for publication scope and faithful website wording, conditional on the root agent's separate mathematical review gate. I read the complete deposited eight-page manuscript and its source independently before seeing any current analytic/adversarial review reports. I have not read those reports. I found no substantive scope mismatch requiring deferral. This verdict does not certify the mathematics on another reviewer's behalf and is not human peer review.

The strongest supported public presentation is the manuscript's stated theorem, with the exact topological-sphere and missing-face assumptions, attribution to the named predecessors, and an unrefereed label. There is no basis for advertising a newly invented general method or first historical priority.

## Bound source and date

- Zenodo record: https://zenodo.org/records/23310484
- Title: Missing faces and topological embeddings of sphere skeleta.
- Author: Alec Kriebel; ORCID https://orcid.org/0009-0001-9320-500X.
- Declared publication date: 2026-10-12. Version: 1.0. DOI: 10.5281/zenodo.23310484.
- PDF: missing_faces_and_sphere_skeleta.pdf, SHA-256 055a6ff8f3451bedc7b75a106329bf2ffd1f02805a568f7f063c13a9b0eb9e59.
- Supplement: missing_faces_verification_v1.zip, SHA-256 3d87ba2ae2a4c9e7dc1cc99a08d75345df0b1f854c6a37ec6d4900a2c48118fa.
- The complete abstract in content.json preserves the deposited abstract, with mathematical notation normalized for readable text. AI-assisted development and lack of independent human peer review remain explicit.

## Exact claim and credit boundary

For a finite simplicial complex S whose realization is homeomorphic to the topological sphere S^(2d), and a missing d-face T on S's actual vertex set, the realization of S^(d) union {T} has no topological embedding into S^(2d). A missing face is absent while all its proper faces are present. The d = 0 case is vacuous under the actual-vertex convention; d = 1 is the familiar planar maximality case. The manuscript also obtains a nonzero mod-2 van Kampen obstruction when d = 2.

The important extension concerns the SOURCE triangulation. Nevo–Wagner's PL-source theorem already rules out topological embeddings; this paper is not merely upgrading a PL nonembedding statement to a topological one. Nor should a triangulated topological sphere be replaced silently by an arbitrary homology sphere. In dimension four the argument works within the PL class of the given triangulation and does not assume it is the standard PL 4-sphere or that a complementary contractible manifold is a standard PL ball.

The algebraic part follows established ambient Lefschetz quotient ideas. The paper's concrete work is the graded Koszul dimension calculation and assembly with established embedding results, plus the dimension-four transfer argument. Its own abstract expressly disclaims first priority and a new general method.

## Primary-source checks

- Nevo and Wagner, On the embeddability of skeleta of spheres (2009), DOI https://doi.org/10.1007/s11856-009-0119-5. Author PDF read at https://pi.math.cornell.edu/~eranevo/homepage/NevoWagner-EmbeddabilitySkeletaSpheres-Rev2.pdf. Theorem 1.2 treats PL source spheres; Conjecture 1.3 asks for the topological-sphere source. Theorem 5.3 is formulated for the general finite-complex transfer with explicit conditions, not exclusively for the standard PL sphere. Problem 1.6 is an existing separate subdivision question.
- Adiprasito, Combinatorial Lefschetz theorems beyond positivity, 2019 v4: https://arxiv.org/html/1812.10454v4. Observation 4.3 and Corollary 4.8 confirm the ambient Lefschetz quotient/dimension mechanism. The manuscript's credit is appropriate.
- Adiprasito and Patáková, A higher-dimensional version of Fáry's theorem, https://arxiv.org/html/2404.12265v3 and https://doi.org/10.1112/blms.70036. Theorem 2 retains the original abstract complex inside an ambient triangulation; it need not retain the original embedding map. The authors describe this fact as folklore.
- Karu and Xiao, On the anisotropy theorem of Papadakis and Petrotou: https://www.numdam.org/item/10.5802/alco.298.pdf and https://doi.org/10.5802/alco.298. Its generic anisotropy/Lefschetz results supply the cited input; do not advertise an unrestricted theorem for arbitrary pseudomanifolds.
- Weber, Plongements de polyèdres dans le domaine métastable (1967), https://doi.org/10.1007/BF02564408; original journal scan available at https://www.e-periodica.ch/cntmng?pid=com-001%3A1967%3A42%3A%3A6. The relevant use is existence of a PL embedding from deleted-product data in the metastable range, not an isotopy statement.

A bounded search for the named conjecture and subsequent resolutions did not identify a verified earlier result of exactly this scope. That is not an exhaustive priority audit and does not justify first-solver or currently-open claims. No publication-priority conclusion is needed for the website.

## Argument and limitations to preserve

The face-ring calculation measures one extra graded class after adjoining the missing face. An ambient Lefschetz surjection would contradict those dimensions. For d >= 3, the metastable passage transfers hypothetical topological embeddability to PL embeddability. For d = 2, the proof verifies the Nevo–Wagner transfer conditions, distinguishes common from newly missing triangles, and starts a bistellar sequence from a flag subdivision within the given PL class.

Finite supplement controls are useful consistency evidence, not a formal proof of the universal theorem. No numerical experiments can replace the local topology, Koszul calculation, or transfer checks. Public copy therefore keeps this argument brief and does not replay the verification history.

## Follow-up decision

follow_up is null. Adding several missing faces is immediate by containment, so is not a paper-worthy new question. A generic homology-sphere or manifold extension does not clear the bar without a precise supported statement and a credible way around the dimension-four difficulty. The Nevo–Wagner subdivision problem is already published and distinct, not a new conjecture to attach to this result. No speculative follow-up is advertised.

content.json supplies SEO title/description, faithful abstract, plain language, exact result, limitations, primary background, a professional collaboration invitation, and source links/filenames. The invitation is page copy only; no person was contacted.
