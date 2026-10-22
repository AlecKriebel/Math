# Fresh adversarial whole-package review: PR1118, round 2

Verdict: **PASS — no unresolved actionable finding.** This verdict covers the frozen package identified below, the full negative answer to both literal printed questions, reproducibility, and the bounded priority framing actually stated. It is neither external human peer review nor a worldwide novelty certificate. The inaccessible final body of the closest 2024 article remains an explicit literature-coverage limitation, already disclosed consistently in the paper, README, metadata and audits.

Reviewer: fresh independent adversarial AI reviewer `/root/pr1118_package_round2`. Review began 2026-10-17 18:46:29 UTC. All publication and original PR inputs were read-only. Only this review directory was written. No prior fresh whole-package review report was read. I read the operative paper, independently reconstructed its mathematics and inspected the primary target/current related source before consulting the packaged earlier mathematical/priority conclusions. No PR, Git reference, release, Zenodo record, tracker row, external correspondence, account or paid access was changed.

## Frozen object

Problem 30004231 / OWR-17135-028. Original PR head `8592fb7297d3c4973f2778c47cfa8972cba896a6`; original PROOF.md SHA256 `b6e32c893f45447951cf920777adaaf012b1eb5a9e5a8072a8822fc8fcf2ff28`.

| File | Bytes | SHA256 |
|---|---:|---|
| main.tex | 12609 | 3768c84cf676fb5a13665b7bec564583cbe5e00aa5a6a1ad4f94c2313173a1e3 |
| totally-mixed-face-posets.pdf | 66369 | 6d278166edb67e3244429d20573c93c95d426e43ba9c23d2b6be7b8abc616b0e |
| source-and-verification ZIP | 157431 | 8fa686dc2484647f2cb5523919ea3eaf7f23590991052a6f93cb48d8b21a582e |
| zenodo-upload-kit.zip | 225014 | 5ddeb426bd69f46e70c2b29bfc56fc27e8237174101ee9c7e1d34b77bc60fc39 |
| zenodo-metadata.json | 3153 | 61e52a95d7dfdfaa68952993d1783099d5d6f7e41ab94fd73f1b893eedeeafe2 |
| zenodo-deposit.json | 3476 | e7b4ce789564e2e254f6dadf1c0d457967615bb042da9d21bc238fa9fa254cec |

These identities were independently checked on intake and again at completion. The final receipt records all review evidence hashes separately from the frozen distribution; there is no self-referential archive.

## Exact target and scope

I fetched the [original EMS report](https://ems.press/content/serial-article-files/46818) directly and visually read physical page 70, printed 2464, Problem 3. It requires positive dimensions of both summands and equality of the sum dimension with their dimension sum. It states no genericity assumption. The posed objects are the inclusion poset and its realization. The paper explicitly uses the usual order complex without artificial extrema. Both conditions, the ambient dimension and both requested conclusions match the printed target.

The example has full-dimensional lattice summands in R5. Deliberate nongenericity is stated prominently. No assertion is made about a repaired/intended general-position formulation or the different stable-intersection shellability program. Even if the printed sphere dimension were corrected from n−2 to n−3, the disconnectedness and first homology obstruction would remain. This avoids relying solely on the conspicuous dimensional issue in the printed homology question.

## Independent analytic falsification attempt

The canonical-summand ambiguity is resolved correctly. If G1+G2 is an exposed face of P1+P2, every point in either Gi must attain the corresponding support maximum: otherwise adding a point of the other nonempty summand produces a strict support deficit. Thus Gi lies in the canonical exposed summand. Their support functions, evaluated at any other functional, have nonnegative deficits from those canonical summands whose sum is zero. All deficits vanish; compact convex bodies are determined by support functions. This establishes uniqueness even for the existential reading of the printed decomposition.

For D4−D4 a nonzero functional assigns unequal extrema on the five affinely independent vertices. Its maximum and minimum sets A,B are disjoint nonempty sets; every such pattern is realized by assigning extremal values and subtracting the value on vertex zero. The sum of their two direction spaces is direct: a nonzero intersection would give an affine dependence supported on disjoint subsets of an affinely independent set. The resulting dimension is |A|+|B|−2. These arguments also rule out hidden degeneracy or an omitted max/min pattern.

Inclusion is exactly componentwise inclusion of A,B. Evaluation against an exposing functional of a containing face forces every maximizing difference to have its first index maximal and its second minimal. Hence there are no extra incidences. The positive-summand filter leaves sizes (2,2), (2,3), (3,2): 30 minima, 20 maxima, 60 strict comparisons and no three-chain. Every minimal vertex has degree two; every maximal vertex degree three, so this is a pure graph rather than a graph with isolated zero-dimensional facets.

The connectivity proof is valid. Suppressing the degree-two vertices gives the signed disjointness graph on two-subsets of a five-set. Distinct intersecting subsets of one sign have the complement of their three-element union as a common neighbor. Disjoint subsets are connected through an intermediate pair meeting each. Every vertex also has an opposite-sign neighbor. The whole graph is connected. Suppression does not create or remove a component. A spanning-tree contraction gives precisely eleven circles.

All product-face cases are exhausted. Nonzero interval functionals expose the two endpoints and retain exactly the base qualifiers. A zero interval functional adds one dimension to each summand and one to the sum; its additivity deficit is at least one, independently of the base dimensions. Horizontal whole-base faces have dimensions (4;4,4), and the whole sum has (5;5,5), so neither qualifies. Empty faces fail positivity. Endpoint copies cannot compare across different heights. The final order complex is exactly K disjoint union K.

The shellability obstruction is decisive under both standard conventions: in any ordering of the 120 edge facets, the first facet in the other connected component has only the empty face in common with earlier facets. That intersection has dimension −1 rather than the required zero. It is not a nonpure-shellability loophole, because the complex is already pure one-dimensional. I directly checked [Björner–Wachs Definition 2.1](https://www.math.miami.edu/~wachs/papers/nonpure1.pdf), printed 1302. The six-point lower-dimensional control is correctly described as shellable and is not used to prove nonshellability.

Rational homology (2,22,0,...) follows without numerical evidence. In fact integral H0 is Z² and integral H1 is Z²²: a spanning forest yields unit incidence minors; the graph has no C2 and its cycle subgroup is free. Thus no torsion or coefficient-field artifact is hidden. A wedge of three-spheres is connected with vanishing H1, so both printed assertions are refuted by this example.

## Independent exact computations and controls

I authored `independent_check.py` without importing either distributed verifier or earlier review code. It exposes the actual integer vertex coordinates using the complete normal grid [-2,2]^d, plus all three interval signs, deduplicates actual finite sum-point supports, calculates exact affine dimensions, and derives all strict coordinate-support inclusions. Coverage is exhaustive: every extremal/intermediate labeling is realized by ternary heights, and subtracting the zeroth height puts its normal in that grid. This route does not assume the claimed A,B census.

Ordinary and optimized runs each execute **2,061 explicit exception-based checks** and agree except their timestamps. Results include:

| Case | Nonempty faces | Selected vertices/edges | Components | Boundary rank over Q | Integral H0/H1 ranks |
|---|---:|---|---:|---:|---|
| R4 base | 181 | 50 / 60 | 1 | 49 | 1 / 11 |
| R5 product | 543 | 100 / 120 | 2 | 98 | 2 / 22 |
| R3 control | 51 | 6 / 0 | 6 | 0 | 6 / 0 |

The product face vector is (40,140,200,130,32,1). All 181 vertical faces fail additivity. Boundary ranks also agree over F2,F3,F5,F7,F101. Eight positive/adverse controls test disjoint edges under every ordering, a connected cycle shelling, a late bridge, dropping additivity, coincident versus independent segment directions, an incorrect unsigned boundary, and an artificial cross-component connection. Integral conclusions rely on the forest argument, not inference from finitely many fields.

I extracted the source archive into an independent folder and ran both supplied programs with ordinary Python and -O. Every output equals the distributed expected JSON exactly in both modes. The programs use standard-library integer/Fraction arithmetic, explicit exceptions and no removable assertions, random tests, network services or mutable external data. I inspected both complete program bodies. The geometry program reconstructs supporting facets from integer coordinates, then the facet-intersection lattice, canonical summands, all 8,649 summand-face pairs and all 294,849 nonempty product-face inclusion pairs. Product facets are supplied via a proved elementary product rule, not falsely advertised as a fresh arbitrary 5D hull computation. The independent topology program reconstructs all chains and signed rational boundary matrices, with augmentation and nonvacuous boundary-sign/cone controls. Their advertised scope is accurate.

Evidence: `evidence/REPRODUCTION_RESULTS.json`, both own-check outputs, both pairs of supplied-program outputs, and the independently authored checking source.

## Source versions, priority and attempted transfer

I independently opened the current arXiv version histories of ten relevant records. They agree with the operative ledger; there is no further current-version omission among those records. The 109 fresh query strings in the packaged ledger are distinct, and its 20 source/version entries are present. This validates those accounting claims without turning search count into novelty evidence. My additional six targeted searches found no contrary exact-poset result; irrelevant search hits were not treated as mathematical evidence.

[Fukuda–Weibel v4](https://arxiv.org/pdf/math/0510470v4), Lemma 4, states canonical face decomposition uniqueness; the inspected older simplex/polar geometry is appropriately credited as classical. Its journal reference and arXiv version date match. The note does not claim a new simplex face-lattice theorem.

[Sturmfels–Tevelev](https://arxiv.org/html/0704.3471), Examples 1.3 and 4.10, supplies the scaled opposite-tetrahedron/six-ray antecedent and the indicated sum face numbers. The operative note correctly credits this six-point homology control. It does not mistakenly cite their different projected-fan Example 5.2 for the six-ray example. This older homology antecedent alone does not settle exact-poset nonshellability.

I freshly retrieved the [AB published article HTML](https://oup.silverchair-cdn.com/article-minimal/4085561) from the official publisher CDN (SHA256 ebdfa2ff566c10135eb75a90bb02d393916035370b1e29df8142dd5ce1379d89) and the original arXiv v1. The published body confirms summand facets, Lemma 3.8, and D=sum d_i−s; v1 has Lemma 3.7 and its different ambient formula. The article's online 2017 and issue 2019 dates and six authors match the bibliography. Its counting theorem is neither needed nor silently invoked in the new proof.

[Adiprasito's accessible July 2020 manuscript](https://webusers.imj-prg.fr/~karim.adiprasito/cint.pdf) uses the subset-dimension lower bound on p2. The proper vertical witness in the new note has dimensions (3;2,2), satisfies that criterion and fails exact additivity. It connects endpoint faces in the larger selection, so the new disconnected exact poset is not a counterexample to that stated stable-intersection result. The 2024 published title, volume, pages, DOI and publication date are independently supported by official publisher JSON-LD and the institutional record. An ordinary unauthenticated request to the PDF URL advertised by the official article page returned HTTP 403. I did not inspect that final body, bypass access controls, purchase access or assume it has unchanged definitions/no additional remarks. The package's qualification is accurate.

[HSWW current v2](https://arxiv.org/html/2606.10817v2) is dated 24 July 2026, with an improved schön construction in (C*)8. I read the relevant current introduction and Section 8 rather than relying on the historical June construction. The current PDF (410,046 bytes, SHA256 eef59d8ec20601addb6c243b64b23b84ef64726b7e78acc444e045c9068c6d53) and HTML hashes match the repaired provenance. My separate exact reconstruction of its stated twice-subdivided simplex-skeleton link gives face vectors (12,51,124) before identification and (11,51,124) afterward, with Betti numbers (1,1,84) afterward. This checks its relevant combinatorial conclusion conditional on the source's geometric identification, without purporting to reprove its entire schön embedding.

An earlier arbitrary nonshellable tropical link would settle this exact priority question only after a proved transfer to canonical positive/additive faces of two polytopes, or some other applicable exact-target theorem. I tested the proposed shortcuts. The normal fan of a Minkowski sum alone cannot determine the filter: Q=D4−D4 and 2Q have the same complete normal fan, but (D4,−D4) yields 50 qualifiers while (Q,Q) yields none, since positive-dimensional canonical summands coincide. My support census checks all 181 Q faces in this control. The [Frick–Sanyal universality construction](https://arxiv.org/html/1607.07814v2), Proposition 2, instead records subsets of arbitrarily many summand labels whose partial sums avoid a point. It does not give the required two-summand exact-face representation. Grouping labels or embedding a fan does not establish that missing equality of objects. These are checks of the proposed implications, not impossibility theorems about all other realizations.

No prior result inspected here establishes exact-poset nonshellability. Any such earlier result would suffice, together with the classical homology antecedent, even if its construction differed completely. The operative paper uses precisely this bounded statement and makes no worldwide-first, exhaustive-literature, generic-shellability, or novel-schön-link claim. The remaining 2024 body access gap is material but transparently represented, rather than erased by negative search results.

## Distribution, metadata and provenance

All six frozen file fingerprints match. Both ZIPs pass CRC; paths are relative, without parent traversal, backslashes, symlinks or duplicate names. Source distribution has exactly 29 members, including its manifest; all 28 other members match their manifest and the outer receipt byte-for-byte. No extra source bodies, third-party PDFs, cached HTML, secret, account token or machine environment is distributed. The only PDF member is the authored note.

The kit has exactly five advertised members. Its portable deposit manifest names the two present PDF/source-ZIP basenames. Its embedded PDF/source archive match the outer frozen files exactly. Metadata objects agree between the local upload manifest, standalone metadata, source archive and portable kit. Title, version 1.0.0, 2026-10-17 publication date, preprint type, language, CC BY 4.0 license, independent-researcher author and supplied ORCID are consistent. Related identifiers point to the actual problem, relevant primary works and PR. No DOI or external review/acceptance claim has been invented before publication.

The new note, README, metadata and PROVENANCE identify the operative new edition and distinguish the original proof-only inputs. All eight pinned original-input size/SHA256 pairs match local frozen inputs; original head and proof hash agree. AI usage is prominent, and the note explicitly says unrefereed and distinguishes AI review from human peer review/formal certification. Authored material licensing does not claim to relicense third-party sources.

## PDF rebuild and visual QA

I rebuilt the extracted TeX from the source ZIP using a separate APFS clone of the Tectonic cache, cached-only mode, and untrusted compilation. No shared cache or input was modified. It compiles cleanly to four pages, without overfull boxes or undefined references. All four pages have exactly identical extracted text, uncompressed drawing streams and 110-dpi RGB pixels to the frozen PDF; the independent PDF byte hash is recorded, allowing compiler timestamp metadata to differ.

I visually inspected every page. The title, abstract, theorem and author/ORCID footnote are clear on page 1; all face classifications and product cases fit legibly on page 2; scope, current-source credit, limitations and disclosures are complete on page 3; all seven references and their links fit cleanly on page 4. No missing glyph, clipped equation, overlap, orphan reference heading or confusing page fragment was found. Evidence is `evidence/PDF_COMPARISON.json`; rendered images are temporary verification artifacts.

## Final disposition

**PASS. No required repair to the frozen package.** Its self-contained argument fully refutes both literal unrestricted assertions. The computation and distribution claims are reproducible; related definitions and current versions are accurately distinguished; finite priority coverage and the uninspected 2024 final body are explicitly qualified. No new unresolved actionable defect was identified. This report authorizes no publication or repository mutation; the parent controls the user-authorized workflow and any further fresh-review requirement.
