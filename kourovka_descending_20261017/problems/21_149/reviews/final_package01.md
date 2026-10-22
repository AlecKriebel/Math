# Independent full-package adversarial review 01

Review checkpoint: **2026-10-17 20:35:02 UTC / 13:35:02 America/Los_Angeles**. This timestamp was obtained from the clock tool. Assigned review pass: **100% complete**. This is a review of a frozen publication candidate, not a human peer review, a formal proof certificate, or an exhaustive priority certificate.

## Frozen artifacts

The package was extracted into `reviews/package01_reproduction/kourovka-21-149/`. I did not author or modify its proof or publication files.

| Artifact | SHA-256 |
|---|---|
| `publication/paper.pdf` | `40fe2bfe2caba65d049cb5e8c567ce15f6a2dcaa998630223cf60878488e31e9` |
| `preprint/main.tex` | `fdb2a51267d802852bc32519924c77b0197f0fdc396c3802c6b57a19229246d6` |
| `publication/source-and-verification.zip` | `2d89ba5dd460a1889ac96de5d631c6131be2334e9387a05bdbf2ff0229a916a0` |

The PDF and TeX inside the ZIP are byte-identical to the corresponding publication PDF and preprint source. All 13 entries of `MANIFEST.json` have the stated byte lengths and SHA-256 hashes. The manifest intentionally does not hash itself. Both authoritative Notebook PDFs cached in the repository match their entries in `source_manifest.json`.

## Verdict

**No outstanding substantive objection found to this frozen package.** I independently checked the complete displayed proof, tried to falsify its critical deductions and scope, reran its exact verifier, rebuilt its PDF, and inspected all six rendered pages.

The explicit theorem for the two master ambient groups is supported by the argument. The standard real Dlab-family application is supported by the specific primary indexed text discussed below, with the access limitation recorded accurately. The paper gives proper prominent credit to the September 2026 rank-one six-family theorem and does not claim that its one-tail mechanism is new. Its novelty assessment is bounded rather than a claim of certified first priority.

This verdict is evidence from an independent AI review pass. It must not be represented as independent human peer review, Lean verification, or proof that no unpublished or unindexed competing result exists. Publication and DOI verification are outside this review.

## Mathematical adversarial checks

### Definitions and source simplicity

The source is the full compact-support locally right `2^Z`-affine group, with unrestricted real breakpoints. It is not silently replaced by a finitely piecewise-linear subgroup or by a dyadic-breakpoint group. The original Dlab paper, Section 2 and Theorems 4.1 and 4.3, matches the definition and supplies the simplicity and two-order assertions used here. Its interval definitions allow arbitrary positive-real slope subgroups. I read the cached original text and opened the primary Cambridge PDF.

The argument from simplicity to perfectness is valid: a nontrivial abelian simple group would be cyclic of prime order, whereas an increasing interval homeomorphism has no nontrivial finite order. A finite two-slope bump supplies nontriviality. Affine rescaling from `[0,1]` to `[a,b]` and identity extension gives precisely `G(L)` for the manuscript's relatively compact open **intervals** `L=(a,b)`. Slopes are unchanged under that rescaling. No simplicity assertion for a disconnected set is used.

Both master ambient classes are groups. An increasing homeomorphism takes a sufficiently small right neighborhood to a right neighborhood, so composition and inversion preserve the pointwise right-affine condition. The eventual affine condition on an initial real ray is likewise preserved. The interval condition explicitly includes zero and excludes the right endpoint.

### Well-ordering and perfect germs

I tested arbitrary subfamilies of support components, not only the whole support. If their finite left endpoints have finite infimum but no minimum, a strictly decreasing sequence of fixed endpoints tends to that infimum. Continuity makes the limit fixed, and the affine right germ containing these fixed points has slope one. It is the identity on a right neighborhood, contradicting component endpoints there. This proves the required well-ordering for interval targets.

For real targets an eventual nonidentity affine formula moves every point sufficiently far left. Thus there is exactly one initial support component, with left endpoint minus infinity; all other components have endpoints bounded below. The same finite-infimum argument handles every subfamily omitting that component. An eventual identity instead bounds all individual support below. These arguments include arbitrary infinite left accumulations of affine pieces and an unbounded final support component.

The right slope at a fixed finite endpoint is an abelian-valued homomorphism. The eventual affine germ on the real line is a homomorphism to the metabelian positive affine group. The image of a perfect group in a solvable group is trivial. Therefore each element of a perfect subgroup fixes some initial interval or ray, and every one of its support components has finite left endpoint. The proof correctly does **not** infer a common initial neighborhood for the entire subgroup.

### Perfect centralizers and disjoint local action supports

Commuting maps permute the support components increasingly. An increasing bijection of a well-ordered set fixes every component, including limit-index components. At a finite left endpoint, perfectness kills the slope character of the centralizer subgroup. For an individual centralizing map this gives an identity right germ. A fixed-point-free increasing map on the component has either forward or backward iterates tending to that left endpoint. Commutation propagates the identity throughout the component.

This propagation works for both displacement signs and for an infinite right endpoint. It needs no rank condition on slopes. Applying it separately to each element of one perfect local image and then taking the union really does give disjoint **action supports** of the two commuting local groups; it is stronger than a statement about any two selected supports. I found no hidden use of a target group order here.

### Least components and arbitrary embeddings

Every action component of an image of a simple group carries a faithful restriction: its restriction kernel is normal and the component has nontrivial action. A fixed nonidentity group element must therefore move a point on every action component. Its support components are well ordered and cannot cross common fixed endpoints. Its least support component consequently lies in the least action component of the group.

The same reasoning inside `J_0` yields `K(L)` for every local simple group. These are actual global local-action components because the boundary of `J_0` is fixed by the full image. This argument remains valid even if the entire group's action support is unbounded below or the elements have no common initial identity ray. It does not assume a standard geometric form for the embedding.

The equivariance identity `K(gL)=e(g)K(L)` has the correct conjugation direction with ordinary function composition. Every image element preserves `J_0`; it carries least components to least components. Disjoint source intervals give disjoint nonempty `K`-intervals.

The finite-tuple interpolation formula is correct for all positive real segment ratios, including boundary ratios equal to either chosen power-of-two slope. The two segment lengths are nonnegative, sum to the source length, and produce the exact target length. Zero-length pieces can be omitted. The assembled finite map fixes common outer endpoints and belongs to `G`. Four-point transitivity therefore makes the relative order of `K(L)` and `K(M)` uniform over all separated pairs. A reversed orientation is allowed; it is not ruled out by an unstated order-preserving-embedding assumption.

### Two tails, order preservation and contradiction

The bump formulas join at the stated breakpoint and are strictly above the identity in the bump interval. The `C_m` descend toward zero and the `D_m` ascend toward one, with positive intervening gaps. Their shrinking lengths give continuity at the closed endpoints. Both `h` and its inverse have the required affine germs at every interior point.

Conjugation by `h` normalizes the full source group, including source elements with infinitely many breakpoints: the argument uses composition of right germs at each interior point and identity near the two boundary points. It does not need an arbitrary source element to have finitely many pieces on its compact support. First support points are transported increasingly, and the first right slope is unchanged by cancellation of the conjugator's positive slope. The displayed positive-cone argument is correct and its identification with Dlab's two orders has the cited external basis.

Each bump interval is invariant, and a sufficiently small compact bump whose support is disjoint from its transported support proves that the restriction of the automorphism to each corresponding local group is nonidentity.

An implementing `u` normalizes the global group and each relevant local image, so it preserves `J_0` and the corresponding least `K(L)`. If its restriction to such a `K(L)` were the identity, faithfulness there would force the nontrivial local automorphism to be the identity. Thus one can choose a genuine support component of `u` inside each `K(L)`. In the positive orientation the `C_m` supply a descending target sequence; in the reversed orientation the `D_m` supply it. The chosen support components are distinct because the local intervals are disjoint. This contradicts the support well-ordering for **every** ambient element `u`, without requiring `u` to belong to a perfect subgroup.

### Exact countermodel for the larger real class

The twisted-diagonal construction in Proposition 7 is valid for arbitrary automorphisms `beta`, with all integer powers allowed. It is continuous at zero because each cell is invariant; each finite cell endpoint has a right identity neighborhood; at zero the map is the identity on the right. The cell of index zero proves injectivity. The shift map `v(x)=x/2` on negative reals sends cell `n` to cell `n+1`, giving exactly `v^-1 E(f) v = E(beta(f))` in the displayed direction.

This does not contradict the theorem: the diagonal image generally has nonidentity support on infinitely many cells tending to minus infinity and fails the eventual left-affine condition. The paper correctly separates this larger finite-point-local class from standard real Dlab groups. In particular, I did not assume that every finite-point locally right-affine map with bounded-above support is an eligible Dlab element.

## Original statement and real-family source scope

The [official current edition](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt-1.pdf), printed p. 199/PDF index 198, asks the corrected ambient-conjugation question and attributes it as the paper states. The cached [official updates](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21upd-1.pdf) explicitly labels the entry a more precise statement and gives the same stronger question. Its entry carries no complete-solution notice. The edition front matter says Novosibirsk 2026. The exact original statement has no ambient-rank restriction.

I independently ran the **three-query batch** recorded in `audits/primary_left_germ_evidence.md`. It returned the complete indexed primary p. 542 paragraph from [Zenkov--Medvedev's full-text endpoint](https://www.mathnet.ru/php/getFT.phtml?jrnid=al&option_lang=eng&paperid=2480&what=fullt). This paragraph supplies the globally affine maps, the factorization of **every** full-group element into an affine map and an element of `D_H*`, and the explicit affine formula near minus infinity for an element outside `D_H*`. A right neighborhood of minus infinity is an initial real ray. The germ conclusion follows from this defining affine behavior, not from rank-one order classification.

I also independently reproduced indexed p. 543 using the batch `"О группах Длаба" "289–298" doi`, `"Длаба" "полупрямым" "T" "-1"`, and `"Длаба" "D_{*H}" "543"`. It explicitly places bounded-above-support `D_*H` inside full `bar D_H`. Thus the reflected family in this citation is a subgroup of the same right-affine full group; it must not be replaced by arbitrary reflected maps with only left germs. The full group's left-germ restriction passes to that subgroup.

**Exact source-access boundary:** I did not obtain Zenkov--Medvedev PDF bytes or inspect its page images. An ordinary 20-second HTTP retrieval timed out. I reproduced indexed pp. 542 and 543 as page-sized primary extracts; I did not reproduce the standalone p. 538 definition page in this pass despite trying its documented query and variants. The existing source audit records that page and the initial-ray identity definition of `D_H*`; the independently reproduced decomposition and finite-ray formulas corroborate the claimed master-group application. These are indexed primary-text checks, not a claim of visual PDF authentication. I found no contradictory definition in the primary extracts or the current literature. The manuscript and README already disclose the direct-PDF limitation.

## Priority, bibliography and attribution

The current [Gong--Yang--Zeng arXiv record](https://arxiv.org/abs/2609.18630) displays only v1, submitted 16 September 2026. I read its primary [HTML theorem and restrictions](https://arxiv.org/html/2609.18630v1) as well as the cached full text. Theorem 1.1 covers exactly six rank-one families and order-preserving embeddings; its introduction and Remark 2.4 explicitly withhold the higher-rank and reflected-real conclusions. The present theorem therefore goes beyond its stated quantifiers. Its one-tail automorphism and support obstruction are prior art, as the present paper clearly acknowledges.

I checked the user-linked [Lean file](https://github.com/pitmonticone/Kourovka/blob/main/Kourovka/Problem_21_149.lean). Its endpoint theorem explicitly concerns the **original formulation**, a non-inner automorphism of the source group. It has no universal larger-ambient embedding quantifier. The current paper does not misrepresent that formalization as verification of its new theorem. I did not rebuild Lean.

Independent searches included exact problem number and Dlab combined with automorphism, conjugation, ambient, embedding, higher rank, and two-tail terminology. The results recovered the September theorem, the original-formulation work, the original definition paper, and older order-classification material; I found no primary result with the manuscript's full ambient quantifiers. The source and priority audits in the package accurately keep negative searches and inaccessible material separate from positive mathematical evidence. I found no basis to remove the bounded-priority qualification or assert certified first discovery.

The five bibliography entries have appropriate problem/source attribution, author names, and identifiers. The affine-germ centralizer mechanism is presented as classical and linked to Dlab's centralizer results. AI use, separate AI adversaries, absence of independent human peer review, and absence of formal proof-assistant verification are all stated explicitly.

Access limits include unavailable full subscription MathSciNet/zbMATH reviews, possible indexing lag, and unpublished work. I did not claim to search those subscription databases exhaustively or independently verify inaccessible papers in full.

## Reproduction and presentation

`python3 exact_constructions.py` passes and produces exactly the packaged JSON: 1,562 segment cases, 3 tuple cases, 200 bump intervals, 441 conjugated affine-germ cases, and 36 affine-group cases. I inspected the verifier; it uses exact `Fraction` arithmetic, refuses optimized Python mode, and makes no inference from these finite checks to the universal theorem. The README states this limitation accurately.

A fresh `tectonic -X compile main.tex --outdir build` succeeds without reported warnings. The rebuilt PDF's extracted text exactly matches the frozen PDF's extracted text. I rendered and inspected every one of the six frozen PDF pages with Poppler. No clipped formulas, overlapping text, missing glyphs, unresolved citations, or substantive layout defects were found. The result is a readable six-page research note with complete proof, countermodel, sources and disclosures.

The independent reproduction receipt is in `reviews/package01_reproduction/reproduction_receipt.json`. No publication, external communication, Git operation, or unrelated-agent work was performed by this reviewer.

## Disposition

The frozen candidate passes this independent full-package review with **no outstanding substantive objections** under its expressly stated standard-real-Dlab scope and bounded source/priority assessment. A later change to the proof, target definitions, source interpretation, or claimed originality would require rechecking the affected arguments. The parent should still perform the requested fresh sequential package review and verify the final publication files and metadata before any release.
