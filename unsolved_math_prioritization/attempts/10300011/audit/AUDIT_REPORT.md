# Independent mathematical and executable audit

## Decision

**ACCEPTED AS A SCOPED UNSOLVED REPORT, 5/5.** Problem 10300011 / AMR-102-0011, rank 1004, Calegari Question 6.1. This acceptance applies exactly to the immutable `author_v1` bytes listed in `REVIEWED_SUBJECT.json`. It accepts the restricted mathematical results and the stated failure of the five approaches to solve the full question. It does **not** certify a general characterization, a decision algorithm, novelty, exhaustive worldwide current openness, a formal proof, or human peer review.

The complete authored proof was read, its logical dependencies checked, and the relevant primary-source statements and proof passages inspected. Mathematical review, rather than successful execution of diagnostics, is the basis of the restricted mathematical acceptance. No mathematical or executable acceptance blocker remains for this frozen version.

The subject's independently received and rechecked external pins are:

- `MANIFEST.json`: `93febcc968a3b244c9cdee7af00fb1ce24519ef03582039cd6b68c2733aab3ae`
- `bootstrap.py`: `7ad7d12073e58e60d33966770689af7dbe7193adfcb5cde38b63f41bc30133c5`
- `author/PROOF.md`: `72186bfc50394149ac96404dda56da480a0f6791f236688c5417f4f7f8bb85d1`

## Target, definitions, and review correction

The problem statement and its location were checked against printed page 11 of Calegari's primary PDF. Definitions 1.3–1.4 on printed page 2 match the essential/genuine distinction used in the proof. The surrounding remarks concern geometric, topological, and algorithmic criteria. The question is about the specified lamination, not merely whether its ambient manifold admits some genuine lamination. [Primary problem list](https://arxiv.org/abs/math/0209081).

The report explicitly restricts its theorems to closed connected oriented 3-manifolds, uses nonempty closed unions of complete leaves, allows equality as a sublamination, and keeps separate boundary sides in abstract complementary completions. The interval-bundle boundary pattern is essential to all arguments and is preserved throughout.

One convention ambiguity was identified during pre-freeze review: an unqualified use of “incompressible surface” can admit spherical edge cases under a solely fundamental-group-based definition. The author corrected both the introductory example and Corollary 1.1 to require positive genus, before creating `author_v1`. The accepted version contains that clarification. The audit does not silently alter any frozen author file. No post-freeze correction patch or replacement author manifest is required; the entire frozen subject was preserved and its byte inventory rechecked after execution.

## 1. Finite compact leaves: accepted

Every complementary completion of the finite compact-leaf lamination is compact. Under nongenuineness it is an interval bundle, and all boundary is horizontal. Thus the base is closed. Orientability of the total space forces the bundle orientation character to equal the base orientation character: an orientable base yields the product with two boundary components; a nonorientable base yields the orientable twisted bundle with one boundary component. A spherical horizontal boundary is already excluded by essentiality.

The dual graph is finite and connected. Each two-sided retained leaf contributes an edge, with loops counted twice. Every vertex has degree one or two, so the graph is a path or cycle, including the one-loop and two-parallel-edge cases. The set of removed edges cannot contain a complete cycle because at least one edge is retained. A removed-edge component in a path cannot join both twisted endpoints for the same reason. Consequently each newly merged piece is a finite product chain, with at most one twisted endpoint piece.

Arbitrary attaching homeomorphisms cause no obstruction: one successively changes a product trivialization along a chain. There is no closed gluing cycle left on which a monodromy issue would arise. Adding finitely many product collars to the horizontal boundary of a twisted interval bundle leaves its bundle type unchanged. This proves the needed nongenuine-to-nongenuine implication for this restricted class.

The one-leaf corollary correctly separates the connected two-boundary cut manifold from the two one-boundary cut manifolds. These yield a fiber and semifiber, respectively. The first-Betti-number test is only a sufficient nonproduct obstruction; the proof explicitly does not use its converse. The fiber/semifiber phenomenon is classical, as the report acknowledges. [Gabai–Kazez, Remark 0.2(iii)](https://arxiv.org/abs/math/9805152).

## 2. Circle suspensions and the fixed-manifold example: accepted

In the pullback over the universal cover of the base, whole-leaf saturation is precisely the condition of being the product with a subset of the circle. Closedness and descent are exactly closedness and invariance of that subset. This proves the claimed bijection without assuming that every leaf is compact or that the action has finite orbits.

A complementary gap has a stabilizer acting in order-preserving fashion. The base action is free and properly discontinuous, so the associated quotient is locally an interval bundle even when the stabilizer has infinite index and the base is noncompact. The two abstract ends of a gap remain distinct when they map to the same circle point. The stabilizer fixes these two ordered ends separately. An interval bundle with orientation-preserving transition maps is trivial; a positive fiber density and normalized integration give a global coordinate, using a locally finite partition of unity if needed.

There is no suppressed new boundary at infinity in this particular argument. Give the compact surface base a complete metric and lift it to the covering base. The smooth bundle projection is uniformly Lipschitz relative to a metric on the compact total space. An intrinsic Cauchy sequence in a complementary component therefore has a Cauchy base projection and cannot escape a noncompact base end in finite intrinsic distance. Local bundle charts account for its remaining interval endpoints. This justifies the completion model used in the proof. The argument is specific to the suspension geometry; it does not supply a theorem for arbitrary essential laminations in noncompact interval bundles.

A circle fiber is a closed transversal meeting every horizontal leaf, which establishes tautness. Essentiality of its closed leaf unions is exactly a classical source example. The exclusion is also a special case of the primary problem list's R-covered statement and is not presented as new.

For the contrast in `Sigma_g x S^1`, the nonseparating vertical torus is two-sided and fundamental-group injective. The ambient product is irreducible. Cutting the surface factor gives genus `g-1` with two boundary components, so its first Betti number is `2g-1`; taking the circle product gives `2g`. This differs from `2` for `T^2 x I` when `g >= 2`. There are two horizontal boundary components, so the orientable twisted alternative is excluded. The torus is therefore genuine. The product foliation in that same manifold has the opposite answer, proving precisely that ambient-only invariants cannot decide the question for every specified lamination.

## 3. Intrinsic weight data: accepted in the stated scope

The two one-sector torus carriers have no branch equations and the same nonnegative one-dimensional cone. The chosen single leaf has weight one in both embeddings. The first embedding has a product complement; the second has the genuine complement just computed. A nonempty sublamination of either one-leaf lamination is the entire leaf.

Thus the listed intrinsic topology/incidence/weight data have opposite outcomes. This is a valid obstruction to that deliberately incomplete input. It does not disprove criteria retaining the embedded carrier, ambient information, complementary boundary patterns, holonomy, or additional coding. The different-manifold construction is explicitly distinguished from the preceding fixed-manifold construction. The report does not assume arbitrary incidence matrices are topologically realizable.

## 4. Finite regular covers: accepted

The image of the closed witness is closed because the finite cover is proper. Lifting paths in a leaf proves that its image is saturated. Regularity and deck invariance are exactly what imply that the witness is the full inverse image of its projection; without that equality the complement comparison would not follow.

If the projected witness were nongenuine, each complementary completion would be an interval bundle. Using a pulled-back metric and local lamination charts extends the finite covering across its abstract horizontal boundary sides. Every connected covering of an interval bundle is itself an interval bundle: classify the cover through the deformation retraction to the base, or pull back the corresponding base cover. This remains valid for noncompact bases. It contradicts upstairs genuineness. Essentiality of the projected sublamination follows by inheritance from the specified essential lamination.

For the finite compact-leaf corollary, deck translates are leaves of the same lifted lamination and therefore coincide or are disjoint. Their finite union is closed, remains two-sided with compact leaves, and is deck invariant. Essentiality of the lifted lamination and its closed leaf unions is preserved by the finite-cover/local essentiality conditions. Applying the finite compact-leaf theorem to this union gives the required genuineness. The proof does not replace regularity by an unjustified normal-closure argument or invert the interval-bundle covering implication.

### Direction of the hereditary statements

Three different implications must not be confused:

1. The report proves that a **nongenuine finite compact-leaf** lamination has only nongenuine nonempty sublaminations.
2. General nongenuine foliations can contain genuine sublaminations, so (1) is not asserted generally.
3. A statement that sublaminations of a **genuine** lamination remain genuine would have the opposite logical direction from the property needed to certify arbitrary finite deck-orbit unions.

The published minimal-set discussion in Gabai–Kazez Lemma 1.6 is classical; its conclusion includes a nowhere-dense/no-isolated-leaf representative and its proof may employ a cover or Cantor thickening. These operations cannot simply be read as literal containment of the final representative in the original one. No absence or novelty of minimal extraction is claimed here. A stronger hereditary theorem is neither used nor certified by this audit.

In particular, Brittenham's compact-base interval-bundle theorems include boundary-leaf hypotheses and genus distinctions. His noncompact local argument in Proposition 6 of the Seifert-fibered-space paper assumes a horizontal sublamination and no compact leaves and uses behavior at the ends. Those hypotheses cannot be discarded just by saying “local interval-bundle argument.” This audit checked those passages to avoid importing an unproved generalization. The current report does not make that mistake. [Interval-bundle paper](https://markbrittenham.github.io/UNL_webpages/papers/pdf/surfxi5m.pdf), [Seifert-fibered-space paper](https://markbrittenham.github.io/UNL_webpages/papers/pdf/sflam.pdf).

## 5. Recognition and containment: accepted as an unsuccessful route

Brittenham's cited proposition does require both full carrying support and an essential branched surface. It identifies nongenuineness using the exterior interval-bundle structure with its horizontal/vertical boundary pattern. The inspected proof deals with essential annuli and the relevant possibly noncompact interval bundles. The report retains those hypotheses. [Author preprint, Section 1](https://markbrittenham.github.io/UNL_webpages/papers/pdf/sm2br5.pdf).

Agol–Li Theorems 4.6 and 5.2 concern ambient existence of essential laminations and Reebless foliations. They are not stated as algorithms for containing a genuine closed saturated subset of a prescribed lamination. The report correctly preserves “Reebless” and avoids replacing it with “taut.” [Agol–Li](https://arxiv.org/abs/math/0201310).

Calegari's later minimal-foliation reduction is not an exclusive classification of the original fixed foliation: one alternative changes the foliation. It supplies no missing fixed-lamination algorithm. [Promoting Essential Laminations, Lemma 3.4.2](https://arxiv.org/abs/math/0210148).

The report's enumeration statement is expressly conditional on a specified effectively checked finite certificate language. Enumerating that language semidecides its own certificates, not automatically the topological target. The parallel-slice example correctly refutes only literal representative containment from common carrying; because the slices are isotopic, it is not a counterexample to a richer isotopy/realization theorem. The remaining soundness, completeness, and negative-termination requirements are explicit. This is a failed approach, not a proved algorithm or undecidability theorem.

## Source, corpus, and current-status verification

All six source PDF hashes and sizes in the frozen packet were independently recomputed against the retained primary documents. The exact source question, definitions, cited theorem statements, and relevant proof passages were inspected. The source-free audit metadata also records the additional Seifert-fibered-space paper consulted for the noncompact-end caveat. No claim of a line-by-line audit of every page of every cited paper is made.

Both complete corpus files were rehashed and counted. The unique problem record and inherited research record were independently serialized and compared with the declared record hashes. The inherited material is literature triage, not a preexisting mathematical solution. No corpus contents or scholarly source documents are included in this audit packet. The duplicate search metadata is a bounded prior-search record; this review does not transform it into an exhaustive absence theorem.

The disposition is “unsolved by this work.” The limited literature search and primary-source checks do not establish worldwide openness as of the review date. No such stronger claim is accepted or needed.

## Independent executable checks and their limits

The independent script authenticates the complete frozen subject against an independently built inventory before importing or running its verifier. Its graph oracle uses adjacency traversal and boundary-side subtraction rather than the author's disjoint-set implementation. Stub pairings exhaust all labelled connected degree-one/two multigraphs on one through five vertices: **94 graphs, 1,422 retained subsets**. Additional tests reject **19 malformed graphs** and check the exact surface arithmetic for **99 genera**.

For every normal, `-O`, and `-OO` invocation, the independent input tests run all three inner modes: **9 positive subprocesses** with source/corpus checking and **60 rejected malformed subprocesses**. Original subject, source, and corpus bytes are checked unchanged. The author's own controls were also independently replayed and agree across optimization modes.

The independent authentication-boundary script accepts **3 exact relocated copies** and rejects **45 mutated copies**, including changed proof bytes, coordinated claim/manifest forgery, duplicate or truncated manifests, unsafe manifest paths, boolean byte sizes, missing or added inventory, symbolic links, a FIFO, and a changed bootstrap. A replaced verifier containing an execution marker is rejected without running it. All tests operate on disposable copies; the original frozen bytes remain unchanged.

`REPLAY_RECEIPT.json` records real subprocess results, not expected or fabricated outputs. Every suite was also run under all three outer optimization modes, with identical result objects. No correctness test uses Python `assert`. The scripts assume a trusted interpreter/standard library/operating system and a quiescent filesystem; this is not a hostile concurrent-filesystem security proof. Authentication requires external pins before executing code. Checksums establish identity and bounded programs test bookkeeping, schemas, and rejection behavior. They do not formalize topology, prove universal graph statements from finite enumeration, or solve the original question.

## Publication scope

This packet contains only an authored audit, source metadata, byte identities, executable controls, and their receipts. It includes no copied scholarly PDF, screenshot, extracted paper text, raw dataset record, private coordination material, or remote write. The separate acceptance decision does not rewrite the author's historical “review pending” fields inside the frozen artifact.
