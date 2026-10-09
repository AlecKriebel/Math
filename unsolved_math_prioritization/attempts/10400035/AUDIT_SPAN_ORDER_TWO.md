# Independent audit: the degree-two Milnor/free-exterior obstruction

**Theoretical-edition note.** This is the complete authored mathematical audit, with only the provenance/privacy and unavailable-artifact edits documented in PROVENANCE.md. Its computational passages describe historical supplementary checks. The scripts, fixtures, outputs, and logs are not included, and preparation of this edition did not rerun them. This is an AI mathematical audit, not human peer review or formal proof-assistant verification. Original authored-artifact hashes below identify the pre-edition documents, not any edited public copies.

**Disposition: ACCEPTED, with the exact scope below.**

The proof establishes that, for ordinary unframed smooth ordered two-string links with fixed matching endpoints and rational finite-type invariants of order at most two,

\[
M_2=\operatorname{span}_{\mathbb Q}\{1,\ell,\ell^2\},\qquad
a_1\notin M_2+N_2.
\]

Here `a_1` is the Conway `z²` coefficient of the first individual component closure, `M_2` is the intersection of the **entire unital repeated-index Milnor algebra** with the ordinary order-two space, and `N_2` consists of invariants vanishing on **every actual three-dimensional free-group exterior**. Thus the proposed spanning equality fails at `(k,n)=(2,2)`. The report does not determine whether `N_2` is nonzero, classify `N_n`, prove failures at larger orders, or claim novelty.

This is a mathematical audit using identified published inputs, with independent finite arithmetic checks. It is not a machine proof of a tangle embedding, a Wirtinger simplification, or any source theorem.

## 1. Audited version and source identity

The accepted main artifact is `PROOF_SPAN_ORDER_TWO.md` (before the documented edition-only redactions), 16,133 bytes, SHA256:

`1ffa1273c4d09427d7ff85164a214ddd2c20090ae36ad71a7a9f876c5a8e0d4a`.

The initial audit intake was the earlier version with SHA256 `ec388f36c4724e0459c8fe0c0da2cbd3be1cd54afad7a165654e3e079a93ea0b`. Before acceptance, the final report was read in full. Its changes clarify notation and rational coefficients, add conventional slice-knot and Conway references, explicitly separate the auxiliary slice tests from free-exterior tests, and correct the Coimbra preprint title. These do not change the mathematical argument.

Supporting authored inputs were also read in full:

- `GEOMETRIC_EXISTENCE.md`, 11,855 bytes, SHA256 `fb1c21c0e59e49a274ddfa2adff3db2be4ce50eac8dc02399fe88357ca2643cf`.
- `FILTERED_MILNOR_ORDER_TWO_LEMMA.md`, 9,665 bytes, SHA256 `68189680279f3dd95a03874442431a98aa78d0467358820c67bd8f8691018073`.

All 24 records of the original supporting packet were independently compared to actual byte counts and hashes, with no mismatch. Its private artifact inventory is not reproduced. Hash matching establishes version identity, not mathematical correctness.

The original [Stanford Question 2.13 in Ohtsuki's problem collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), printed p.408 / PDF p.36, was read and its page image visually inspected. It asks the separate nontriviality and spanning questions and uses rational invariants. It does not impose a direct-sum requirement or require a specified meridian marking to be a free basis. The adjacent Polyak discussion is not part of this question. The ordinary unframed convention is the stated interpretation, consistent with the surrounding framing-independence discussion and the Meilhan source; the audit does not rebrand the result as a theorem for arbitrary framed conventions.

## 2. Exact theorem inputs

### Ordinary degree-two classification

[Meilhan, arXiv:math/0402036v2](https://arxiv.org/pdf/math/0402036v2), dated 10 November 2004, was checked at Definitions 1.1–1.3, Section 2.1, and Theorem 2.4. Its string links have ordered upward-oriented fixed ends, without a monotonicity condition. The ordinary `1T` relation is explicit. For two strings, its theorem gives precisely the six functions used in the report:

`1, linking, linking², first-component Conway coefficient, second-component Conway coefficient, plat coefficient minus both component coefficients`.

The source's plat convention joins the two bottom ends and the two top ends. Its knot coefficient is zero on the unknot and one on the trefoil. All uses of this theorem have the correct category and finite-type order. The report needs a spanning theorem here; its coefficient-elimination argument does not secretly require uniqueness before proving the relevant exclusions.

### All-length, repeated-index concordance invariance

[Meilhan–Yasuhara, arXiv:0904.1527v1](https://arxiv.org/pdf/0904.1527v1), Section 2.1.4 and Section 5.1 / PDF p.22, was checked. The former explicitly permits repeated labels; the latter defines fixed-endpoint concordance by disjoint embedded rectangles and states Milnor concordance invariance. The proof does not substitute the nonrepeating link-homotopy theory.

For additional direct published support, the introduction and Section 1, pp.419–420, of [Habegger–Lin, *On link concordance and Milnor's μ-invariants*, Bull. London Math. Soc. 30 (1998), 419–428](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0024609398004494/resource/name/S002460939800449Xa.pdf) were independently read. The paper identifies the full longitude data with nilpotent Artin representations and applies Stallings' theorem to a concordance complement to obtain the same representation at every nilpotent stage. This directly supports the all-length input. Its endpoint definition also expressly separates ordinary strings from monotone braids. No new assumption or change to the frozen proof is needed.

Only the direction “Milnor invariant implies concordance invariant” is used. Neither the converse theorem nor a filtered generation assertion from the framed Habegger–Masbaum framework is needed.

### The free tangle

The complete Appendix Section 4, pp.14–15, of [Nogueira's Coimbra preprint 14–09](https://www.mat.uc.pt/preprints/ps/p1409.pdf) was read, including its free-tangle and individual-cap definitions, tunnel construction, handlebody argument, and the subsequent essentiality paragraph. The complete page-15 artwork was independently viewed. Figures 9 and 10 visibly contain the trefoil arc, the indicated tunnel, and the resulting second proper arc; the crossing interruptions are present.

The relevant source statement is an unnumbered appendix construction, not the main theorem about essential surfaces. The required two facts are its handlebody exterior and its trefoil first capped arc. The proof does not rely on the second component's claimed torus-knot type or on essentiality. The tunnel operation is the displayed conversion from the trefoil's tunnel to a proper second strand; the source identifies the resulting exterior with a handlebody. This is an acceptable cited geometric input. The audit does not replace it with an unsupported claim that an arbitrary knotted arc plus an arbitrary second arc has free exterior.

The distinct later [arXiv:1706.03719v1](https://arxiv.org/pdf/1706.03719v1) was checked as a textual cross-reference only. Its missing Figure 13 is not used as visual evidence. The final main report correctly uses the earlier preprint's title, *Knot complements with meridional essential surfaces of arbitrarily high genus*, and distinguishes the later *Prime knot complements…* title. No byte-for-byte equivalence with a publisher PDF is claimed.

## 3. Audit of the full filtered-algebra argument

This is the logically important step: a high-length polynomial in Milnor invariants might have cancellations that lower its finite-type order. A degree count on displayed generators alone would not exclude that possibility. The submitted proof avoids the problem correctly.

Every finite polynomial in all Milnor invariants is concordance invariant, irrespective of the lengths of its displayed generators. If that resulting function belongs to the ordinary order-two space, the Meilhan theorem can be applied to the **function**. The three null-concordant examples then eliminate its component and plat coefficients. No assertion that all high-length polynomial terms vanish separately is made.

### The slice knot and local tests

For a trefoil `T`, the knot `S=T#(-T)` is smoothly slice, with `-T` the reversed mirror. The smooth concordance-group convention was checked in [Cochran–Harvey's author-hosted arXiv:1404.5076v2](https://math.rice.edu/~shelly/publications/arxiv_geometry_knot_conc.pdf), introduction pp.1–2. Passing to the corresponding based long concordance gives the required endpoint-product collars.

The mirror and reversal conventions do not change the even Conway coefficient. Multiplicativity under connected sum is also explicitly recalled in [Conant, arXiv:math/0503648v2](https://arxiv.org/pdf/math/0503648v2), Section 1. Thus the square knot has Conway polynomial `(1+z²)²` and coefficient two. The argument does not mistakenly treat the integer Conway coefficient as a concordance invariant; the slice knot with nonzero coefficient is precisely what is needed.

Inserting `S` in a small ball on either component, disjoint from the other component, permits its null-concordance inside that ball times the concordance interval. Its linking is zero. The plat encounters the local knot once, so the component/plat-difference coordinates are `(2,0,0)` and `(0,2,0)`, including the possible reversal when tracing the second strand.

### Relative framing of the parallel test

An oriented rank-two normal bundle over a concordance rectangle is trivial. Prescribing the separating normal direction only on the top and the two endpoint sides leaves the bottom free. Those prescribed three sides form one proper boundary arc, so their section extends across the rectangle. This avoids the potentially false assertion that an arbitrary prescribed framing on the entire boundary extends.

Use the product structure in boundary collars and a sufficiently small tubular neighborhood. The two push-offs are disjoint embedded concordance rectangles, with fixed endpoints; their top is the identity two-string link. At the bottom, the normal plane is spatial because the original concordance is product-like there. Hence their bottom is a genuine pair of parallel long arcs. Its linking is zero by concordance invariance, which proves the induced zero-linking normalization rather than assuming it.

Each bottom component individually closes to `S`. The narrow strip between the bottom arcs is an **embedded disk**, with its two short boundary arcs equal to the prescribed caps after the endpoint-collar adjustment. Consequently its entire boundary, the chosen plat closure, is an unknot. The strip need not have an unknotted core relative to the ball boundary for this conclusion: any embedded disk in the three-sphere has unknotted boundary. There is no confusion here with a closed annular cable. Thus the third coordinate row is `(2,2,-4)`.

The coefficient equations have matrix

\[
\begin{pmatrix}2&0&0\\0&2&0\\2&2&-4\end{pmatrix},
\qquad \det=-16.
\]

They force all three non-linking coefficients to vanish over the rationals. Constants, linking, and its square do belong to the stated Milnor algebra and have orders at most zero, one, and two. This proves the full intersection result. The auxiliary slice links are never required to have free three-dimensional exteriors. No conclusion over arbitrary coefficient groups is justified by this elimination.

## 4. Audit of the marked geometric witness

The source works in the PL category. The supporting geometric lemma explicitly smooths its finite tame proper arc system in small disjoint neighborhoods and boundary collars. This preserves the exterior homeomorphism type and the individually capped knot type; there is no wild-arc or four-dimensional smoothing issue.

Choose and fix the component labels and one starting endpoint on each arc. An orientation-preserving sphere isotopy can move the four distinct ordered endpoints to any required two bottom and two matching top points. Extending through a collar and straightening the end neighborhoods gives an ordinary smooth string link. This does not require the arcs themselves to be height-monotone.

The exterior remains the source handlebody. Its boundary is the sphere with four endpoint disks removed, completed by two lateral annuli. It is connected with Euler characteristic `-2`, hence genus two, so the actual exterior group is `F₂`. No statement about a particular bottom meridian basis or only the lower-central quotients is substituted for this topological fact.

After forgetting the second component, boundary caps for the first arc are arcs on a sphere with only the two relevant endpoints. Such caps are isotopic relative to their endpoints. The marked component's standard individual closure therefore remains the trefoil. This reasoning would be invalid if it silently retained the other two punctures, but the proof explicitly forgets the other component first. Orientation choices do not affect the Conway coefficient. Thus `a_1(L)=1` for every boundary marking of the stipulated kind.

No explicit numerical linking value or complete marked crossing list is required by the subsequent argument, which is uniform in the unknown linking. The recovered full primary drawing and this category-conversion proof satisfy the actual existential obligation. The submitted universal four-evaluation argument does not assert or assume a match of all Milnor data with one comparison braid. No stacking, gluing, or alteration of the free witness needs a separate freeness theorem.

## 5. Restriction obstruction and its precise limits

The pure braids with linking `0,1,-1` have pair-of-pants-times-interval exteriors, hence genus-two handlebody exteriors. After discarding either component, the remaining single strand is unknotted. Therefore their first-component Conway values are zero.

If `a_1=m+u`, where `m` is in the established Milnor space and `u` vanishes on every free exterior, evaluation on these three braids forces the quadratic linking polynomial `m` to be identically zero. Evaluation on the Nogueira witness then contradicts `a_1(L)=1`. This proves nonmembership in the sum itself, not merely failure of a chosen direct-sum decomposition.

Writing the unknown linking of the witness as `t`, the four-by-four matrix in the report has determinant two identically in `t`. Its first three columns therefore cannot span the fourth for any marking. This is a finite-dimensional restriction argument; it does not assert equality of the full Milnor data of a braid and the tangle.

The optional consequences `M_2∩N_2=0` and `dim_Q N_2≤2` follow from the same tests and the six-dimensional classification. They do not decide whether `N_2` vanishes. The elementary order-zero and order-one statements are consistent with the source conventions. Failure at order two alone must not be propagated to every larger order, since the larger filtered Milnor space may contain additional functions.

## 6. Independent computation and negative controls

The author's exact-arithmetic script was read and rerun. Its output bytes remained unchanged. An independent checker was written using SymPy 1.14.0 exact rational-function elimination and rank, rather than the author's custom polynomial/permutation implementation.

The independent baseline performed **49 checks**, all passing:

- frozen artifact and source byte/hash matches;
- all entries of the source catalogue and geometric source manifest against their actual bytes;
- null-concordant coefficient rank three, empty homogeneous kernel, determinant `-16`;
- pure-braid polynomial rank three, empty homogeneous kernel, determinant `2`;
- rank four and determinant `2` for the free evaluation matrix over `Q(t)`;
- strict rank increase on adjoining the component-invariant column;
- generic determinants `-2s³` for a slice test with nonzero component coefficient `s`, and `2q` for a free witness with coefficient `q`;
- the square-knot Conway multiplication.

The same checker passed with `python -O`. It does not rely on Python `assert` statements or parse a report's claimed PASS status. Four independent mutant runs, also under `python -O`, were rejected with nonzero exit status:

1. Erasing the cable's `-4` term destroys the coefficient-elimination rank.
2. Erasing the trefoil witness coefficient destroys the restriction obstruction.
3. Replacing the negative-linking braid test with a duplicate positive-linking test destroys the quadratic determination.
4. Replacing the expected Coimbra source digest breaks the source identity check.

These controls show sensitivity to the actual arithmetic and pinned evidence. They cannot detect a false topological source theorem or establish that a picture is an embedding; those were addressed through the source and mathematical review above. The distinction is retained in all machine outputs.

## 7. Source fingerprints and publication boundary

Independently matched primary PDFs:

- Ohtsuki/Stanford statement: 4,731,008 bytes; SHA256 `33d9c18c9ab8403a4d88b978b366451383edd12dd24760a77b9e25b666d9a8fd`.
- Meilhan 2004 v2: 315,045 bytes; SHA256 `8b88fa5ea5df29a3b4a16934e5ade6bab37269462ace0d43bd15bff265f9a3b7`.
- Meilhan–Yasuhara 2009 v1: 519,255 bytes; SHA256 `7333539cfbea8d86e0a5c139388d93576ea1ff08c7d333decd614519a545d487`.
- Nogueira Coimbra 14–09: 305,322 bytes; SHA256 `455b0187bbf9b8214022236ac7a949ecdc5e3a13f7e92aec802ed6d9f9f6d98b`.
- Nogueira 2017 v1, text cross-check only: 420,491 bytes; SHA256 `6426f07a35c87d985429361e85d8d8528d05154b2ec10db0d84cdb5584fe848b`.
- Cochran–Harvey 2014 v2: 463,164 bytes; SHA256 `f934310a778bbb61ea54f22a0f24c1b8c67300f21336247f86d1125d1ea1c2a7`.
- Conant 2012 v2: 89,518 bytes; SHA256 `deb93ea70b706f5ec3a734b66303f64e127e2f4655af1e6c8c5f1ebfa46e1d20`.

Coimbra PDF page 15, containing complete Figures 9 and 10, was independently rendered and inspected. The source rendering and its artifact identity are excluded from this edition.

The supplemental Habegger–Lin published PDF was inspected through the web text reader. A separate direct byte retrieval returned HTTP 403, so this audit claims no retained PDF hash for it. The web extraction is not included, and no extracted-text artifact fingerprint is reproduced. The frozen proof already has the sufficient verified Meilhan–Yasuhara input.

This audit contains authored reasoning and bibliographic/verification metadata. Copied PDFs, source text, and rendered source figures are excluded from any publication payload. No queue or remote changes, outreach, or new proof-search approach were performed during the audit.

**Final acceptance:** the submitted first approach is a valid, source-dependent negative answer to the spanning clause in the stated ordinary rational `(2,2)` category. The independent nontriviality clause remains unresolved by this report.
