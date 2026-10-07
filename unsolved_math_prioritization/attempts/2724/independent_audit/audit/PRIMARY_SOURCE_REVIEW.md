# Independent primary-source review: KP-1.65

Review date: 6 October 2026.

## Verdict

The source audit supports the stated limited outcome: this investigation supplies neither a solution nor a counterexample to the exact, no-index-2 version of KP-1.65. The important distinctions between smooth realization, stabilization, regularity, decomposability, and Lagrangian isotopy are mathematically sound. Two precision edits are warranted: retain Etnyre–Leverson's nonempty-end hypotheses, and clarify that a literal Legendrian-isotopy trace requires adjustment before it is a Lagrangian concordance. The September 2026 construction can be excluded more explicitly because its stated movie includes a cap.

This review covers the cited statements and the arguments that determine their scope. It is not a dependency-by-dependency validation of the research papers, an exhaustive literature search, or independent verification of the catalog and repository-history claims.

## 1. K3 target and elementary pieces

Printed page 63 is also PDF page 63. Both the rendered page and its extracted text were inspected. The target concerns exact Lagrangian cobordisms lacking height-critical points of index 2 and asks for a Lagrangian isotopy to a decomposable representative. It does not merely ask whether the same endpoints admit some decomposable cobordism. The audit preserves these distinctions correctly. The page's discussion also expressly separates the earlier non-decomposable concordance examples because they require index-2 points.

The elementary pieces stated in the audit agree with the standard description in Etnyre–Leverson and Breen: the Lagrangian concordances associated with Legendrian isotopies, isolated maximal-Thurston–Bennequin unknot births, and the permitted Legendrian surgeries. Arbitrary smooth bands are not thereby allowed pieces.

For a source-text-free publication, replace the direct question quotation in the mathematical audit with an authored paraphrase. Do not reproduce the book page.

Source: [K3 preliminary book, p. 63](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf).

## 2. Etnyre–Leverson: exact correction

Theorem 1.2, p. 2, requires a ribbon cobordism in the three-sphere product with nonempty negative end, together with prescribed Legendrian representatives. Its conclusion permits endpoint stabilizations and a smooth isotopy of the original smooth cobordism. Question 1.8, p. 3, asks about stabilizing an already Lagrangian ribbon cobordism whose two ends are nonempty. Neither statement identifies a prescribed unstabilized Lagrangian embedding up to Lagrangian isotopy.

Add the nonempty negative-end condition to both theorem summaries, and the two nonempty-end conditions to the Question 1.8 summaries. These hypotheses matter especially when contrasting the theorem with filling questions.

Section 4, p. 7, footnote 1 also explains that the raw trace of a Legendrian isotopy needs perturbation. Replace the shorthand “Legendrian-isotopy traces” by “the standard Lagrangian concordances associated with Legendrian isotopies.” This avoids suggesting that an arbitrary literal trace is already Lagrangian.

Source: [Lagrangian Realizations of Ribbon Cobordisms, v1](https://arxiv.org/abs/2410.06305v1).

## 3. Breen: correct stable scope

Theorem 1.4, p. 4, begins with regular sliceness, equivalently the indicated regular concordance from the maximal-tb unknot, and produces a decomposable concordance after one stabilization of each end with the same chosen sign. It does not assert a filling of the stabilized knot. Problems 1.5–1.6 remain the corresponding unstabilized questions in that manuscript. The audit's summary is correct: it does not establish regularity for every no-index-2 cobordism or identify the original embedding with an unstabilized decomposable representative.

Source: [Regularly slice implies once-stably decomposably slice, v1](https://arxiv.org/abs/2410.21031v1).

## 4. Golovko–Komarek: correct exclusion, version update available

The retained v2 PDF, Section 3.3, p. 6, forces an index-2 point when the connected-sum multiplicity exceeds twice the chosen genus. Thus its examples are non-ribbon and do not satisfy the hypothesis under review.

The current arXiv record now identifies v3, submitted 3 July 2026. Its Section 3.3 was independently inspected in HTML and retains the same positive-index-2 conclusion. Its theorem statement makes the multiplicity condition explicit. The v2 summary is accurate as labeled; a current supplement should record v3 separately rather than relabel v2's byte count or digest.

Cambridge's publisher page confirms online publication on 10 August 2026 and the stated DOI. The DOI resolver failed in this review's web reader, but the publisher page was accessible.

Sources: [v3 full text](https://arxiv.org/html/2511.08731v3), [publisher record](https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/abs/nondecomposable-lagrangian-cobordisms-between-legendrian-knots/FF529570F928F8CCAC3E525A2C73B73D), [DOI](https://doi.org/10.1017/S0305004126102217).

## 5. Dimitroglou Rizell–Golovko: the stronger inference is valid

Sections 5–6, pp. 7–9 of v2, support the audit's inference that the reverse concordance is not strongly homotopy-ribbon. The forward concordance is regular and hence strongly homotopy-ribbon; the endpoint smooth knot types are distinct; antisymmetry of the strongly homotopy-ribbon relation rules out that property for a reverse concordance. The same argument is applied after the fillable satellite construction. Because ribbon concordances are strongly homotopy-ribbon, the reverse examples are not no-index-2 examples.

This is a valid reading of the proof's stronger obstruction. It is not the invalid converse assertion that every non-regular concordance must be non-ribbon. The audit correctly makes that distinction.

Source: [Non-regular Lagrangian concordances between Lagrangian fillable Legendrian knots, v2](https://arxiv.org/abs/2509.13594v2).

## 6. Golovko endoconcordances: correct ribbon obstruction

Proposition 2.1 and its proof, p. 3, assume ribbonness of the constructed endoconcordance and deduce injectivity of its Khovanov map. Functoriality and the difference between the endpoint Khovanov groups contradict that injectivity. The proof therefore obstructs ribbonness itself, not only decomposability. Section 3 uses the same kind of rank obstruction for its families. The audit's exclusion from the no-index-2 class is correct. The manuscript's distinctions involving Hamiltonian non-isotopy do not change the stronger ribbon obstruction used here.

Source: [Non-decomposable Lagrangian endoconcordances and Khovanov homology, v1](https://arxiv.org/abs/2608.27316v1).

## 7. Guadagni: strengthen the exclusion

Theorem 1.1 and Proposition 3.1 generally produce weak cobordisms, which may fail exactness. Definition 3 makes that distinction explicit. Corollary 1 recovers exactness for the concordance case using its topology, so the main example in Theorem 1.2 is correctly described as exact.

The current audit's caution is valid but unnecessarily weak. Section 2.2, p. 5, describes the move U1 as including a cap H3. Proposition 6.2 and the proof of Theorem 1.2, pp. 17–18, use one splitting 1-handle followed by one cap. Consequently, the exhibited movie includes an index-2 critical point. Its diagrammatic presentation is not a no-index-2 construction.

Suggested added sentence: “The explicit construction in Proposition 6.2 and the proof of Theorem 1.2 uses a splitting 1-handle and a cap, so the displayed movie contains an index-2 critical point.”

Source: [Non-decomposable cobordisms via Lagrangian moves, v1](https://arxiv.org/html/2609.35048v1).

## 8. September contextual source

Breen–Zupan, Section 1.1, explicitly keeps the reverse implications among decomposable, regular, and general Lagrangian disk fillings open under several levels of specification. The source audit correctly treats this as related context rather than a logically equivalent reformulation or a proof that KP-1.65 has no solution elsewhere.

Source: [Derivative links in contact topology, v1](https://arxiv.org/html/2609.30182v1).

## Verification metadata and boundaries

All seven retained source PDFs were independently rehashed and their byte counts recomputed. Every result matches its corresponding entry in PUBLIC_VERIFICATION_METADATA.json. The audited PDFs correspond to the stated versions: K3, Etnyre–Leverson v1, Breen v1, Golovko–Komarek v2, Dimitroglou Rizell–Golovko v2, Golovko endoconcordances v1, and Guadagni v1. The v3 Golovko–Komarek check and Breen–Zupan check were HTML inspections, not additional PDF integrity checks.

No mathematical scope reversal was found. Apply the two precision edits above, optionally strengthen the Guadagni paragraph and add the independently checked v3 record, and retain the unresolved-in-this-investigation status. None of these changes supplies the missing global normalization theorem or a counterexample satisfying the target hypotheses.

This authored report contains no source excerpts, source-document copies, dataset contents, or private coordination material.
