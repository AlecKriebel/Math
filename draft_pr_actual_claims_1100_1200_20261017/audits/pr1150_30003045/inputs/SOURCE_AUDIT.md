# Source and scope audit

## Exact question

Ahmed Laghribi's contribution, *Differential and Quadratic Forms in Characteristic Two*, joint with Roberto Aravire and Manuel O'Ryan, appears on printed pages 248–251 of Oberwolfach Report 5/2016, *Algebraic Cobordism and Projective Homogeneous Varieties*. The relevant item is Question 2 on printed page 251 (PDF page 37). The function-field convention is stated on printed page 248 (PDF page 34).

The field has characteristic two; the inseparable extension is arbitrary finite, not restricted to exponent one. The form is bilinear Pfister and must remain anisotropic over the inseparable extension. Its function field comes from the projective quasilinear quadratic form `B(v,v)`. The adjacent nonsingular quadratic-Pfister question is Question 1 and is a different problem.

Full source: https://ems.press/content/serial-article-files/46609

The complete PDF and its text extraction were available for inspection. The exact Question 2 and the convention on printed page 248 were additionally checked visually. The report's full contribution and its preceding exponent-one theorem were read in extracted text.

## Exponent-one predecessor

Aravire–Laghribi–O'Ryan, *Graded Witt kernels of the compositum of multiquadratic extensions with the function fields of Pfister forms*, Journal of Algebra 449 (2016), 635–659.

Author manuscript: https://laghribi.perso.math.cnrs.fr/Witt-kernels%28new-version%29-2.pdf

Theorems 1.1–1.2 use purely inseparable multiquadratic extensions, hence exponent one. Their hypotheses and formula were visually checked on manuscript page 3. The definitions on manuscript page 4 use an affine quadric convention. For an integral homogeneous quadric, its affine-cone function field is a one-variable purely transcendental extension of its projective function field; injectivity of Kato cohomology under pure transcendental extension makes the relevant kernels equal. This translation does not enlarge the exponent-one theorem to exponent two.

The counterexample uses a simple purely inseparable extension of degree four and exponent two. It therefore does not contradict that predecessor.

## Higher-exponent mixed extensions

Aravire–Laghribi–O'Ryan, *Cohomological kernels of mixed extensions in characteristic 2*, author manuscript dated 15 August 2019; Journal of Algebra **542** (2020), 249–276; DOI https://doi.org/10.1016/j.jalgebra.2019.09.012

Author manuscript: https://laghribi.perso.math.cnrs.fr/cohom-kernels.pdf

The manuscript's introduction, Definition 1.3, Theorem 1.4, the relevant membership argument in Lemma 3.1, and the final examples were inspected in text. Definition 1.3 and Theorem 1.4 were additionally checked visually on pages 3–4. Its abstract and introduction describe the failure of two-field mixed kernel splitting at higher inseparability exponent. Section 6's displayed explicit example is about purely inseparable composita; it should not be silently substituted for the mixed three-summand question.

For correspondence with Theorem 1.4, use its inseparability parameter `n=1`, differential degree `m=1`, and Artin–Schreier representative `a=s⁻⁴∈F⁴` (so its parameter `l=2>1`). This gives the same separable quadratic extension as `s⁻¹`. In Definition 1.3 take `f₀=1`, `f₁=z`; the displayed differential generator becomes

`bz²/(1+bz²) dlog z`.

Thus the candidate class is a concrete member of the paper's additional mixed-generator term. The self-contained membership calculation in the proof checks this correspondence directly. The norm-residue argument then proves its nonmembership even after the extra, independent bilinear-Pfister summand is included.

The manuscript defines its kernel-splitting property for `m≥1`. Its formal definition does not settle the original `n=0` case; the candidate proof supplies that case separately.

The publisher landing page could not be fetched with the web retrieval tool (403), so no byte-level comparison against the published typeset PDF is claimed. The author publication list and publisher-deposited Crossref record independently confirm **volume 542**, not 537:

- https://laghribi.perso.math.cnrs.fr/research.html
- https://api.crossref.org/works/10.1016/j.jalgebra.2019.09.012

## Independent standard-fact references

The differential-symbol identification `H₂²(E) ≅ Br(E)[2]`, with `a dlog b` corresponding to the cyclic quaternion class `[a,b)`, was independently checked in Adam Chapman and Anne Quéguiner-Mathieu, *Minimal quadratic forms for the function field of a conic in characteristic 2*, arXiv:2111.15251, PDF page 3: https://arxiv.org/pdf/2111.15251. This was a targeted check of the preliminary identification, not an inspection of every argument in that paper.

The characteristic-two splitting/norm criterion was independently checked in John Voight, *Quaternion Algebras*, Chapter 6, Theorem 6.4.11, especially equivalence of the split-algebra and norm conditions: https://link.springer.com/chapter/10.1007/978-3-030-56694-4_6. The publisher HTML supplies the theorem; no claim of a full-book audit is made.

The cyclic relative-kernel description is recalled in the inspected mixed-kernel manuscript and explained via cyclic two-cocycles in the authored proof. None of these standard facts is attributed to a new calculation here.

## Source identity metadata

The PDF bytes inspected have the following SHA-256 identities:

- OWR 5/2016: 514,462 bytes; `75a01e6e34988e672e0b6b48a56a3467ef7de59ee7fecc850a71e29110bf748c`
- 2016 graded Witt kernels author manuscript: 380,905 bytes; `f6fd774bef7afe291a24ea87d253ef3548cdfb070c29793b1482ed1932df5507`
- 15 August 2019 mixed-kernels author manuscript: 406,587 bytes; `6bee75060598e61159fb78dd1f3167c5dfc3de24611d8af280a791bb1f8a5b03`

These are source-identification metadata, not proof of their mathematical claims. The authored counterexample does not rely on an unverified blanket assertion that every two-field obstruction survives every choice of bilinear Pfister form. In fact, choosing the slot `z` would absorb the displayed class; the proof explicitly uses the independent slot `t`.

## Status and limits

The deliverable is an authored counterexample argument with exact algebra diagnostics, accepted by the independent internal AI mathematical audit in AUDIT_REPORT.md. This acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. It makes no priority claim and no exhaustive claim about later literature. The original universal equality is addressed by a counterexample at its allowed index `n=1`; there is no claim that every index or every field fails. No copied third-party source text or PDF is part of the authored proof.
