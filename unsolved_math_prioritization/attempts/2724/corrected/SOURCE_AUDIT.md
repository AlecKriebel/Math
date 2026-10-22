# Source audit for Kirby Problem 1.65

Checked on 6 October 2026. This is a bounded, primary-source review, not evidence of novelty or an exhaustive search. No inspected result provides a general decomposition theorem or a verified counterexample satisfying the exact no-index-2 hypothesis. The conclusion is therefore “unresolved in this investigation,” not a claim to have proved the absence of later results.

## Identity and retrieval

The requested catalog identity is problem 2724, KP-1.65. The corresponding complete record and associated empty report passed the inherited-work gate before research began; the only prior assessment was literature triage. Verification metadata records the supplied dataset, statement, and complete record/report hashes.

The live problem URL https://unsolvedmath.com/problems/2724 and its www variant did not render through the web reader; an ordinary HTTPS fetch of the www URL returned HTTP 403. No live-page match is claimed. The exact question was instead checked against the supplied record and the primary K3 book, visually and in extracted text.

The previously listed AIM URL, https://aimath.org/pastworkshops/kirbylistrep.pdf, is a four-page workshop summary, not the book containing Problem 1.65. The corrected primary source is the AMS-authorized preliminary book hosted at Berkeley, printed page 63 (PDF page 63): https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf. The checked question and the index-2 limitation of the 2024 examples agree with the supplied statement and background. Source PDFs and extracted text are excluded from this artifact.

## Smooth realization does not give the required isotopy

John B. Etnyre and Caitlin Leverson, Lagrangian Realizations of Ribbon Cobordisms, arXiv:2410.06305v1, Theorem 1.2 and Question 1.8, pp. 2-3. Their existence theorem assumes a nonempty negative end and allows stabilizations of the Legendrian ends and a smooth isotopy of a ribbon cobordism. The paper separately poses stabilized decomposability of a given Lagrangian ribbon cobordism with both ends nonempty as a question. These statements do not settle the prescribed-embedding, unstabilized target.

https://arxiv.org/abs/2410.06305

Joseph Breen, Regularly slice implies once-stably decomposably slice, arXiv:2410.21031v1, Theorem 1.4 and Problems 1.5-1.6, pp. 3-4. The affirmative statement assumes regular sliceness and changes the endpoints by one stabilization. It is neither a general regularity theorem for all no-index-2 cobordisms nor an unstabilized Lagrangian-isotopy classification.

https://arxiv.org/abs/2410.21031

## Recent non-decomposable examples must be checked against the hypothesis

Roman Golovko and Daniel Komarek, Non-decomposable Lagrangian cobordisms between Legendrian knots, arXiv:2511.08731v2, Section 3.3, p. 6. Their positive-genus examples satisfy an estimate forcing a positive number of index-2 critical points. Their construction therefore does not refute the no-index-2 question. Cambridge lists the article as published online on 10 August 2026; the mathematical inspection here used the identified arXiv version.

https://arxiv.org/abs/2511.08731
https://doi.org/10.1017/S0305004126102217

Georgios Dimitroglou Rizell and Roman Golovko, Non-regular Lagrangian concordances between Lagrangian fillable Legendrian knots, arXiv:2509.13594v2, Sections 5-6, pp. 7-9. The proof rules out strongly homotopy-ribbonness for the reverse concordance: its forward partner has that property, and the two smooth knot types differ. Since ribbon implies strongly homotopy-ribbon, the examples are not no-index-2 counterexamples. This is an inference from their proof and the implication they state, not a general assertion that non-regularity alone obstructs ribbonness.

https://arxiv.org/abs/2509.13594

Roman Golovko, Non-decomposable Lagrangian endoconcordances and Khovanov homology, arXiv:2608.27316v1, Proposition 2.1 and its proof, p. 3, followed by Section 3. The endoconcordance obstruction is non-injectivity of a Khovanov map that would be injective for a ribbon concordance. Thus the obstruction also excludes ribbonness; it does not produce an example in the no-index-2 class. The paper was inspected as a preprint.

https://arxiv.org/abs/2608.27316

Roberta Guadagni, Non-decomposable cobordisms via Lagrangian moves, arXiv:2609.35048v1, Theorems 1.1-1.2 and Section 2.1. The general move theorem initially supplies weak, potentially non-exact cobordisms. The explicit main example is an exact reverse concordance from a stabilized nontrivial knot to a stabilized unknot. Section 2.2 identifies the unknot move U1 as containing an H3 cap; Proposition 6.2 and the proof of Theorem 1.2 use a splitting 1-handle followed by a cap. Thus this displayed construction contains an index-2 critical point and is not a no-index-2 construction. This observation concerns the exhibited movie and does not by itself prove that all isotopic embeddings must have index-2 points. The existence of a diagram movie is not evidence that it uses only the allowed decomposable pieces. The paper was inspected as a preprint; no claim about the minimum stabilization count is needed here.

https://arxiv.org/abs/2609.35048

Joseph Breen and Alexander Zupan, Derivative links in contact topology, arXiv:2609.30182v1, Section 1.1. The September 2026 manuscript continues to distinguish decomposable, regular, and general Lagrangian disk fillings and explicitly leaves the reverse implications open at multiple levels of specification. This is related context, not a logically equivalent formulation or a proof of the status of KP-1.65. HTML inspection only.

https://arxiv.org/abs/2609.30182

## Bounded repository history

Read-only searches in AlecKriebel/Math checked default-branch code for 2724, all pull requests for 2724, commit messages for KP-1.65, and all pull requests for Lagrangian. The exact-ID searches returned no matches. The broader query located PR 61, which concerns adjacent KP-1.66 (ID 2725), and PR 96, which concerns an unrelated variational-control problem. Neither is an inherited proof attempt for this exact problem. Search absence is not proof of novelty or of exhaustive repository-history coverage.

https://github.com/AlecKriebel/Math/pull/61
https://github.com/AlecKriebel/Math/pull/96

No repository state or queue file was changed during this investigation.
