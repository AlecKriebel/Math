# Fresh independent adversarial preprint review 02

**Verdict: PASS for the exact pinned manuscript and publication kit.** The mathematics passes within its explicitly named established-theorem dependencies. The package passes exact inventory, immutable-original comparison, full clean normal and outer `-O` replay, metadata, source compilation, and all-page visual checks. R1 and R2 from review01 are correctly repaired throughout the current presentation. No credible counterexample, unsupported central implication, circularity, or actionable submission defect remains identified in this review.

This is an internal AI-assisted review, not external human peer review, a formal proof certificate, or certification of first historical priority. It performs no publication, merge, Git mutation, or external communication. PASS binds the six exact inputs below; it does not clear future altered bytes automatically.

## Independence, exact target, and evidence

I read the governing source and assessed every proof step before reading previous review reports. The timestamped independent initial assessment was saved at **2026-10-13T04:07:35.616196+00:00** in `evidence/independent_initial_assessment.json`. It records no central mathematical gap, with citation reconciliation and kit checks still pending. Only afterwards did I read review01 and the current root priority notes. The initial assessment does not derive from those verdicts.

The exact hypothesis under adversarial test is: a **smooth integral projective** variety over an **algebraically closed field of any characteristic**, dimension **n ≥ 1**, with positive **relative Fulger–Murayama tangent-bundle Seshadri constant at one arbitrary closed point**. The conclusion is an isomorphism over that same field to projective n-space. No Fano, global tangent nefness, separability, general-point, uncountability, or characteristic-zero assumption may enter before it has been proved or is part of a precisely matched established import. The definition uses quotient projectivization, excludes vertical curves, and counts the entire generic degree in the pushed-forward cycle.

The target matches [FM's final-numbering Conjecture 4.9](https://par.nsf.gov/servlets/purl/10198624) and [Fulger's OWR contribution, p.3289](https://publications.mfo.de/bitstream/handle/mfo/3816/OWR_2019_53.pdf?isAllowed=y&sequence=1). PR718/problem30004324/OWR-17296-007 are consistently identified in the packet and saved PR metadata. Finite controls are explicitly supplementary; the success criterion for the geometry is a checkable noncircular written proof with matching theorem hypotheses.

All authored work is confined to this review folder. Source retrievals were read-only requests to primary repositories, author pages, publishers, or the Stacks Project. Temporary primary PDFs, extracted source bodies, clean extraction trees, compiled copies, and rendered pages were removed after checking. Final evidence retains URLs, retrieval hashes, bibliographic locations, authored analysis, executable integrity checks, and reproduction receipts.

## Mathematical falsification audit

### 1. Direct quotient lifts, including singular rational images

For a normalization `f: P¹ → C → X` of an integral rational curve through x, split `f*T_X = ⊕ O(a_i)`. A quotient summand defines the required map to the quotient projective bundle. Its image Γ has function field between the equal fields of C and P¹. Consequently both relevant generic degrees are one: the tautological degree is exactly a_i and the pushforward is [C]. Positivity of the displayed Seshadri infimum gives `a_i ≥ mult_x(C) ε(T_X;x) > 0`, hence integer `a_i ≥ 1`.

There is no hidden cover-degree division, normalization separability assumption, or substitution of ordinary slopes for Frobenius-normalized slopes on general curves. Several branches over x and a singular image affect multiplicity but do not invalidate the quotient argument. This is stronger than merely finding one very free curve: every rational normalization through x has ample tangent pullback.

### 2. Same-point existence and an absolute minimum

The inspected proof of FM Corollary 4.6 produces a rational curve through **the same x**, rather than merely proving generic uniruledness. It therefore makes the minimum of positive integer A-degrees over rational images through x nonempty and attained. This is an explicit established import, independent of the subsequent conjecture.

The minimum survives every algebraically closed extension K/k. A smaller rational image over K supplies a normalization with a chosen preimage of x_K moved to 0. A degree-c pointed Hom scheme is finite type over k; a K-point makes it nonempty, hence it has a closed k-point. The descended map remains nonconstant because c > 0. Its image is rational by Lüroth, including inseparable intermediate subfields, and has degree at most c. This contradicts the original absolute minimum. The argument does not assume that rationality or birationality is an open condition in an arbitrary curve family, or choose a very general point of a countable field.

### 3. Stable-map boundary, ghosts, and inseparable covers

A connected geometric genus-zero nodal domain has a tree of projective-line components. From the marked component, traverse components constant at x until the first nonconstant one. Its image contains x, hence has degree at least d after the extension argument. Additivity of total map degree yields

`d = Σ e_w (A·C_w) ≥ e_v (A·C_v) ≥ A·C_v ≥ d`.

All nonconstant summands are positive integers. Equality forces exactly one nonconstant component and full generic degree one. Inseparable multiple covers contribute their full degree and cannot escape this equality.

Every contracted subtree attaches along only one edge: two attachments to the sole nonconstant component would create a cycle. For t vertices it has at most one marking and at most `2(t−1)+1+1 = 2t` special-point incidences, while stability requires at least 3t. Thus no ghost survives, including a ghost initially carrying the mark. Self-nodes, positive-genus components, and cycles already contradict arithmetic genus zero. The argument applies to all geometric objects, not only to a generic member or to a chosen curve class.

The contrast with two markings is substantive: a ghost carrying two marks and one node can be stable. The proof correctly uses one marking. A Frobenius cover has zero differential and may have infinitesimal automorphisms, but its greater full degree excludes it before the inertia argument.

### 4. Actual evaluation fiber and finite inertia in wild characteristic

[Abramovich–Oort Theorem 2.8 and §2.5](https://arxiv.org/pdf/math/9808074) provide precisely the proper finite-presentation Artin stack, finite stabilizers, and projective coarse scheme for a projective finite-presentation target, with fixed degree and without a tameness restriction. The actual evaluation fiber at x is proper and nonempty.

A birational normalization is an isomorphism onto its image on a dense smooth open locus. A geometric automorphism preserving the map is therefore identity there and everywhere. On that open locus the differential into smooth X is injective; over an algebraically closed, hence perfect, base, this remains true in positive characteristic. A regular vector field killed by the differential is zero. Isolated vanishing of a differential at a singular preimage does not produce a nonzero vector field supported at that point.

Each finite geometric stabilizer has one point and zero tangent space; Nakayama makes it the identity scheme. This geometric statement also removes nilpotent-only inertia over arbitrary bases. On an atlas, the identity augmentation splits the finite inertia algebra as `O ⊕ J`. The splitting makes the geometric fibers of J zero; Nakayama for the finite module J forces J = 0, without assuming it flat.

[Stacks 04SZ](https://stacks.math.columbia.edu/tag/04SZ) then makes the actual fiber an algebraic space. Its map to the full projective coarse Q is proper by the graph argument, since it is proper over k and Q is separated. Coarse geometric points classify marked-map isomorphism classes, so each geometric fiber has at most one point. Finite type gives quasi-finiteness, including nonreduced zero-dimensional fibers. [03XX](https://stacks.math.columbia.edu/tag/03XX) makes it a scheme, and [02LS](https://stacks.math.columbia.edu/tag/02LS) makes the map finite. Finite over projective is projective. No coarse-moduli commutation with a closed evaluation fiber is used in wild characteristic.

### 5. Genuine universal projective-line bundle over nonreduced bases

The inertia-free scheme represents actual stable maps, so its universal curve, marking, and evaluation descend as actual morphisms. Flatness, finite presentation, and smooth geometric P¹ fibers make the curve morphism smooth. The mark lies in the relative smooth locus and is a relative effective Cartier divisor. Its line bundle has fiber degree one, with `h⁰ = 2`, `h¹ = 0`; proper flat base change supplies a rank-two pushforward and the evaluation quotient.

The induced map to that rank-two quotient projective bundle is fiberwise an isomorphism. It is proper and quasi-finite, hence finite. The algebra-map cokernel has zero fibers and vanishes by Nakayama, making a closed immersion. Flatness of the source over the base lets the defining ideal tensor injectively into the target fiber; that ideal has zero fibers and vanishes. This validates the construction even before reducing the base. The section removes the Brauer obstruction to a general P¹ fibration. Its contraction `eσ = x` is an identity of morphisms, not just a geometric-point statement.

### 6. Pointed Hom torsor, smooth descent, and evaluation surjectivity

A projective-line bundle with section is locally a pointed trivial bundle: a local frame adapted to its line quotient suffices. Its parametrizations form the torsor under `Aut(P¹,0)`, a smooth two-dimensional group in every characteristic. The degree-d pointed Hom scheme parametrizes the same stable maps; every geometric degree-d map is birational by the absolute minimum argument.

At the chosen degree-d normalization, all a_i ≥ 1. Therefore both `H¹(f*T_X(−0))` and `H¹(f*T_X(−0−∞))` vanish, including the borderline a_i = 1 because `H¹(O(−1)) = 0`. Fixed-source infinitesimal deformation theory makes pointed Hom smooth and its evaluation at ∞ smooth at f. The manuscript explains the two-value lifting/gluing obstruction directly; [Gounelas Proposition 4.7](https://ems.press/content/serial-article-files/26314?nt=1) supports this characteristic-free two-point mechanism. It is not an invocation of characteristic-zero generic smoothness.

Smoothness descends along the smooth parametrization torsor. The image point has a unique reduced irreducible component H locally, and after shrinking a neighborhood of f factors through that component. Smooth second evaluation is open there. Thus the actual evaluation from U_H contains a nonempty open subset of X. Projectivity gives closed image, and integrality of X then gives surjectivity. Smoothness over reduced H gives reduced U; flat geometrically integral fibers over integral H give irreducibility. Properness and the marking are retained on the entire component, including its singular or nonnormal boundary points.

### 7. Line-bundle descent and all numerical test curves

Connected integral H makes every fiber degree of e*D constant; birationality identifies it with degree on the image C. For `L = O_X(dD) ⊗ A^(−b)`, its pullback has degree zero on every geometric P¹ fiber and hence is trivial there, with `h⁰ = 1`, `h¹ = 0`. Proper flat perfect base change gives a line bundle B and an isomorphism `π*B ≅ e*L`. The adjunction is checked on all fibers, rather than inferring total triviality from fiber degree alone.

[Stacks 0B91](https://stacks.math.columbia.edu/tag/0B91) applies. The optional [0EX7](https://stacks.math.columbia.edu/tag/0EX7) route requires a reduced base and is used only on H; [0GKA](https://stacks.math.columbia.edu/tag/0GKA) supplies universal structure-sheaf pushforward. The genuine contracted section gives `B ≅ L|_x ⊗ O_H ≅ O_H`, after choosing a basis of the one-dimensional fiber. Hence e*L is trivial.

For **any** integral curve Γ in X, including positive-genus, singular, or x-avoiding curves, the nonempty generic fiber U_η has a closed point with finite residue extension K/k(Γ). Its reduced closure has dimension one, is proper, and dominates Γ with full degree q > 0. It factors through the closed reduced curve Γ because its generic image lies there. The projection formula gives `0 = q deg(L|Γ)` as an equality of integers. [Stacks 0AYQ](https://stacks.math.columbia.edu/tag/0AYQ) corroborates this degree formula without separability. Even when the characteristic divides q, positive integer multiplication is injective on the integers. This is not division inside k.

Thus L is numerically trivial and every Cartier divisor satisfies `d[D] = b[A]` in N¹(X)_R. Since A has degree d > 0 on a fiber image, its class is nonzero and the Picard number is exactly one. The proof does not assert the stronger, unneeded statement that Pic(X) itself is cyclic or that L is already trivial downstairs.

### 8. Nakai positivity and the exact Fano import

The chosen minimal normalization has positive anticanonical degree `b = Σ a_i > 0`. Consequently `−K_X ≡ (b/d)A` with positive rational coefficient. For every r-dimensional integral subvariety Z, expand the difference of powers. The remaining product with [Z] is a real one-cycle, which a numerically trivial divisor annihilates. Hence all top intersections equal the corresponding positive ample intersections.

Smoothness makes −K_X Cartier. [Fujino–Miyamoto Theorem 1.3](https://www.math.kyoto-u.ac.jp/~fujino/Nakai-Moishezon3.pdf) is valid over algebraically closed fields without a characteristic restriction and yields actual ampleness. The proof does not stop at strict nefness.

The directly inspected FM Proposition 4.8(1) assumes precisely smooth projective **Fano**, arbitrary algebraically closed k, and positive tangent constant at some point. Its proof cites Kollár V.3.2; Conjecture 4.9 is subsequently posed and is not an input. Its alternative general-point/characteristic-zero clause is never invoked here. The new argument has proved Fano before applying clause (1), so there is no circular transfer of the central conjecture to an equivalent unsupported claim. Full Kollár and CMSB text were not independently obtained; the established FM proposition is an explicit, inspected import, and that access limit is disclosed.

### Boundary cases and strongest verified conclusion

Dimension one is consistent: the tangent line bundle has degree 2−2g, and positivity forces genus zero; H may simply be a point. The argument covers characteristic two, countable algebraically closed fields, arbitrary algebraically closed extensions, nonreduced initial moduli bases, reduced nonnormal H, singular rational images, marked ghosts, and inseparable lifted test curves. Smoothness, one marking, positivity rather than mere nonnegativity, and the absolute image-degree minimum are genuinely used.

The strongest verified result is that the written proof establishes the full stated theorem given its credited established imports. No remaining central mathematical gap was identified. Finite replay is not being promoted to a proof of the universal geometric assertions.

## References, priority, and disclosures

The exact primary imports and bibliographic checks are recorded in `evidence/source_checks.json`, with source hashes and retrieval status in `evidence/source_retrieval_receipts.json`. FM's final numbering is correctly distinguished from earlier arXiv numbering. OWR authorship, report DOI, contribution pages 3287–3289, and target page 3289 match. Chang's v2 and publisher citation identify the smooth toric case and singular counterexample correctly. Abramovich–Oort, Gounelas, all six cited Stacks tags, and Fujino–Miyamoto have the asserted relevant statements. Kollár's bibliographic identity is supported by the [publisher record](https://link.springer.com/book/10.1007/978-3-662-03276-3); full monograph access is not claimed.

The earlier R1 is repaired to **K. Miyamoto**, confirmed against Keisuke Miyamoto's author manuscript. R2 is repaired to **523–544**, confirmed against the [Andreatta–Occhetta publisher PDF](https://archive.intlpress.com/site/pub/files/_fulltext/journals/ajm/2005/0009/0004/AJM-2005-0009-0004-a005.pdf) and [publisher-deposited DOI metadata](https://api.crossref.org/works/10.4310/AJM.2005.v9.n4.a5). The governing source, support source, rendered PDF, and current/copied root priority notes agree. A comparison to the immutable review01 snapshot proves that these two bibliography edits are the only manuscript changes. The old six snapshot hashes still match review01's verdict. No historical frozen candidate was edited.

[Andreatta–Occhetta Proposition 2.20(b)](https://archive.intlpress.com/site/pub/files/_fulltext/journals/ajm/2005/0009/0004/AJM-2005-0009-0004-a005.pdf) is a genuine standard numerical-generation precursor. Its complex-variety scope is contextual attribution; the present manuscript writes its own required characteristic-free argument. The author does not claim the general numerical principle as new.

The packaged ledger contains exactly **64 distinct queries**, as claimed. I conducted **16 fresh searches** plus primary follow-ups, recorded in `evidence/fresh_priority_ledger.json`. Only primary sources support conclusions. Secondary aggregators incidentally surfaced by discovery searches were not used as proof or as evidence of literature absence. The extension inspected the nearby Mori-type formulations of Achinger–Witaszek–Zdanowicz and Occhetta–Wiśniewski, Kebekus's global anticanonical characterization, newer Fulger–Ray positivity work, Murayama's March 2026 moving-divisor Seshadri paper, and Jovinelly–Lehmann–Riedl's January 2026 free-curve/fundamental-group paper. Their inspected statements have additional Fano, general-point, characteristic-zero, Picard-rank, or global-slope assumptions, or different conclusions. They do not directly supply the fixed-point Fano reduction. The in-preparation vector-bundle moving-Seshadri reference remains without inspected public contents.

No earlier full resolution or explicitly matching immediate consequence was identified in this bounded extension. That finding does not establish first historical priority, exclude unpublished work, or replace a comprehensive human literature review. The manuscript and metadata accurately qualify the priority audit and credit established ingredients and special cases. Extensive AI use, author responsibility, unrefereed status, lack of external human peer review, and lack of a formal machine proof are disclosed. Independent external expert reading could add assurance, but no outreach was prepared or initiated.

## Exact publication kit and immutable history

| Input | Bytes | SHA-256 |
|---|---:|---|
| paper.tex | 17,546 | fe385adc3db169e6eeacce965c337aaf5f7a185491944ca096c0709bbcb785b6 |
| output/pdf/paper.pdf | 91,056 | f3e5619c7e1560c45f7793b0f7e4dabfbbf66d08f568f3478b5bb8f35779ea17 |
| source-and-verification.zip | 281,820 | 22bcb3d40fd734a6ee6e416319f329739395dcc66417da5f27e82d32a85694cf |
| zenodo-deposit.json | 3,468 | 4158f1d7b94528ca7e203859b5cdb41d54038300ca1f468b411570d95cb2f264 |
| zenodo-metadata.json | 3,272 | 4e21becd2c6534e3cf8053428b16690e40df52f77e1f3d3017e29e0b9f5d1cae |
| zenodo-upload-kit.zip | 362,965 | ebe24c6dc38bf339433477070ed4cc7f264f5a525490e04eb0ab8d9d3b45d97c |

All match the supplied pins and current `PACKAGE_INVENTORY.json`. The source archive has exactly **78 files**, its **77 listed entries plus its manifest**. It preserves the exact inventory and bytes of **49 original files**. The author/v2 historical freezes contain 13 and 27 files respectively. Eight current, nested, or explicitly reconstructed manifests are independently checked as closed hash inventories. Historical audit supplements are correctly reconstructed through `AUDIT_LAYOUTS.json`, rather than incorrectly treating partial stored layouts as their original complete trees.

Both main ZIPs and their nested historical ZIPs pass CRC, path uniqueness, traversal/absolute-path, regular-file, and encryption checks. The recursive support scan reaches **116 non-ZIP leaves**, without primary PDF bodies, extracted source downloads, private-source filenames, or common credential/private-key candidates. The included reports are authored assessments and public provenance metadata; source downloads are excluded. Mechanical screening is bounded, not a claim to detect every possible secret.

The outer convenience kit has exactly five members: PDF, source ZIP, flat deposit JSON, metadata JSON, and README. Its PDF and nested source ZIP are identical to the separate published objects. All **five metadata objects** are equal, and top versus flat deposit file paths correctly reflect their locations. Title, version 1.0, author, Independent researcher affiliation, ORCID, date, preprint type, open access, language, license, and related identifiers agree. The ORCID checksum is valid. October 13 UTC build times are October 12 PDT, matching the publication date. Metadata vocabulary matches [Zenodo's documented deposit format](https://developers.zenodo.org/); no live authenticated deposit was attempted.

The CC BY 4.0 declaration identifies the authored deposit license and preserves third-party rights. Frozen historical candidate-only/pending strings and the historical adverse integrity result are transparently preserved as history. The current README distinguishes the governing paper and later reviews from those historical stages. Review01 and this fresh review correctly remain outside the fixed source archive; changing the archive to include its own later clearance would change the reviewed bytes.

## Reproduction, adversarial integrity, and visual QA

From a clean extraction, the **complete** verifier ran normally and with the **entire outer invocation under `-O`**, using Python **3.14.6**, confined temporary paths, and disabled bytecode writes. Both return exit 0, empty stderr, identical PASS JSON, and an unchanged closed extraction. Receipts are `evidence/complete_normal.json`, `evidence/complete_optimized.json`, and `evidence/reproduction_receipt.json`.

The complete replays reproduce 909,136 author finite controls, 85,247 independent finite controls, 14 historical strict mutation rejections, two reconstructed audits, both interpreter modes, relocated and zero-fuzz patched byte-exact reconstructions, and the preserved historical nested-manifest bypass regression. Independent pointed controls reproduce 50,068 rooted marked-tree configurations, the two-mark ghost contrast, borderline cohomology, and derivative controls in characteristics 2, 3, 5, 7, and 11.

My separate `evidence/audit_package.py`, itself run normally and optimized, adds **14 outer-verifier mutation checks**: same-size content corruption, an extra nested manifest, missing payload, duplicate manifest path, manifest self-entry, traversal path, and a symlink, each with and without outer optimization. All are rejected. Its authoritative checks use explicit conditions rather than removable assertions. The executed packaged paths were inspected: process calls use argument arrays for Python and patch; no shell-evaluated process, network client, Git command, or external communication is invoked. Auxiliary finite assertions are exercised in the normal replay and checked against expected output; they do not constitute the geometric proof.

The source recompiles successfully with **Tectonic 0.16.9**, with no warning diagnostics, undefined references, or overfull boxes. All five corresponding pages have identical extracted text and **byte-identical rendered PNGs** at 110 dpi to the distributed PDF. The compiled PDF differs in timestamp-dependent bytes, as the README anticipates; the distributed PDF is separately pinned. All five distributed pages were individually visually inspected: equations, glyphs, theorem numbering, references, margins, page numbers, and both repaired citations are intact. There is no clipping, overlap, missing reference, or unreadable glyph box. The disclosure continuation at the top of page 5 remains readable. PDF information identifies an unencrypted, five-page A4 document, without JavaScript or forms. Optional embedded title/author metadata is absent, but visible attribution and deposit identity are correct.

## Submission readiness and remaining limits

The exact repaired kit is ready for the next separately authorized submission step. This review requires no further correction. Its proof conclusion is supported under the identified established imports; no credible theorem-level counterexample or unresolved unsupported claim was found. The remaining limits are explicitly bounded priority coverage, ordinary reliance on published theorems, unrefereed AI-assisted internal checking, and lack of formal verification. They are disclosed limits, not hidden release defects.

All supporting authored files are listed in `REVIEW_MANIFEST.json`; large temporary extraction/render trees and copyrighted source bodies are excluded and removed. Repository branch remains main. No original, prior snapshot, governing manuscript, publication kit, PR, or remote state was modified by this review.
