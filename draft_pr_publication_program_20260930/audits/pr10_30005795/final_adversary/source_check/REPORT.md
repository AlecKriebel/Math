# Independent primary-source certificate for PR 10

Checked: 2026-10-01T04:52:31Z. Completion: 100% of assigned source audit.

## Verdict

**PASS: no unresolved primary-source issue and no source acceptance blocker.** The current `reviewed_candidate/BOUND.md` accurately distinguishes the printed question, its repaired valuation domain and inherited surface hypothesis, the stated scope of the published lemma, and the extension inferred from its proof. The classification as a known method/source-status correction is supported. It would be inaccurate to advertise a newly proved 2024 open theorem.

This certificate checks source interpretation and source attribution. It does not replace the independent geometric or log-resolution proof certificates. The upstream duplicate record identifier is a dataset fact rather than a statement appearing in these mathematical primary sources; its independent verification is outside this primary-source certificate. The candidate's local `source_record.json` directly confirms that the cleaned statement omits the Du Val hypothesis and retains the ambient valuation-domain error.

## Independence and evidence discipline

I read `reviewed_candidate/BOUND.md`, then reconstructed the official OWR and CFKO sources directly, without reading existing source/family reports. All conclusions below were obtained from those primary documents. I downloaded PDFs only into ignored `tmp/final/source_check`, rendered the relevant pages, and examined the full page images. No original snapshot or candidate file was edited; no Git mutation, external contact, or publication occurred. `ARTIFACT_HASHES.json` records the PDFs and candidate/snapshot hashes inspected.

## Official OWR question

Primary URL: https://ems.press/content/serial-article-files/48650

DOI: https://doi.org/10.4171/OWR/2024/14

The contribution is *Calabi problem for smooth Fano threefolds* by Ivan Cheltsov and Elena Denisova, beginning on printed p. 836 (PDF page 10) and ending with its references on p. 844 (PDF page 18). Its opening identifies the contribution as the abstract for four lectures explaining how to prove K-stability of smooth Fano threefolds. This matters: the isolated interrogative sentence is part of an exposition of an established technique.

- **Printed p. 836, PDF page 10:** Section 1 begins with smooth Fano threefold X. The chosen surface S contains P and has Du Val singularities. It then defines tau and the positive/negative Zariski parts P(u), N(u).
- **Printed p. 837, PDF page 11:** The surface delta invariant ranges over prime divisors F over S whose centers contain P. Its displayed S-invariant includes exactly the weighted negative-part integral at issue.
- **Printed p. 839, PDF page 13:** Section 3 explicitly reuses Section 1's assumptions and notation. It sets D(u)=P(u)|S and says this restriction is nef by construction. It bounds the volume term using a lower estimate q(u) for the surface delta invariant, then raises the negative-part question.
- **Bottom of printed p. 839:** The question requests K>0 with
  
  `3/(-K_X)^3 * integral_0^tau (P(u)^2.S) ord_F(N(u)|S) du <= K A_S(F)`.
  
  The final sentence really prints F over **X**. This is visible in the rendered PDF; it is not a parser error. The same page's preceding formula ranges over F over S, as does the next example. Since A_S(F) and ord_F of a divisor on S require a divisor over S, replacing X by S is the mathematically compelled interpretation of this typo.
- **Printed p. 840, PDF page 14:** Example 1 immediately treats N(u)=0 up to a, and N(u)=(u-a)E afterwards, with E a prime divisor different from S. If (S,E|S) is log canonical, the report supplies exactly the corresponding discrepancy bound for every prime divisor F over S. It additionally notes the smooth-surface/smooth-restriction example.
- **Printed p. 844, PDF page 18:** Reference [3] is the CFKO paper in Nagoya Mathematical Journal 251 (2023), 686–714. Section 3 already identifies its method as following this reference.

### Does the source ask for a stronger target?

The displayed question imposes no explicit numerical upper limit on K, no requirement that K be independent of X and S, and no optimality requirement. Its surrounding application seeks useful estimates for K-stability, so an arbitrary finite bound need not suffice for a specific application. That practical issue does not convert the stated existence question into an unstated sharp-constant conjecture. The candidate explicitly preserves this limitation. No stronger unresolved target is identifiable in the printed question or following example.

The report's phrase covering all F over S is stronger than the local centers required by the delta-invariant application. The candidate properly handles these separately: global thresholds give the all-center bound; local thresholds apply only when P belongs to the center.

## Published CFKO versus author preprint

Published primary article:

https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/kstable-divisors-in-mathbb-p1times-mathbb-p1times-mathbb-p2-of-degree-112/999FB6032A21485AD71CF230CC802E6C

DOI: https://doi.org/10.1017/nmj.2023.5

Author-hosted primary preprint:

https://www.maths.ed.ac.uk/cheltsov/pdf/220608539.pdf

The Cambridge page's `citation_pdf_url` supplied the published PDF. It is 29 PDF pages, corresponding to journal pp. 686–714. The author-hosted preprint has 24 pages.

### Exact stated setup

Published **Appendix B, pp. 712–713 (PDF pages 27–28), Lemma 27**; preprint **Appendix B, p. 23 (PDF page 23), Lemma 26**:

1. X is a smooth Fano threefold.
2. A morphism pi:X→P^1 is a fibration into del Pezzo surfaces.
3. S is a fiber, irreducible, reduced, normal, del Pezzo, with at worst Du Val singularities.
4. P is a point in S.
5. N(u)=sum_{j=1}^l f_j(u)E_j for fixed irreducible reduced surfaces E_j on X, different from S, and nonnegative coefficient functions on [0,tau].
6. c_j=lct_P(S;E_j|S).
7. F is a prime divisor over S with P in C_S(F).

Thus the stated lemma itself is **not** a theorem for an arbitrary finite-family klt surface setup. The candidate explicitly says so, which is essential to its accurate attribution.

### Isolated first proof step

The published proof begins on p. 713. Log canonicity of (S,c_jE_j|S) at P gives

`ord_F(E_j|S) <= A_S(F)/c_j`.

Summing after weighting gives the first inequality of the lemma, retaining the volume term unchanged. This is exactly the componentwise local estimate reconstructed by the candidate. This step uses the threshold/discrepancy definition and the local-center condition; it does not use the del Pezzo fibration geometry.

The later step uses P(u)|S=-K_S-N(u)|S and comparison with -K_S to control the volume contribution. This is the geometry-dependent part. Consequently the candidate's general finite-family extension is justified as an inference from the proof mechanism, not a quotation of the full lemma's stated scope. The global version is likewise an elementary extension using global thresholds rather than an assertion about what CFKO explicitly states.

The numbering distinction is genuine and visually checked. The published proof and the preprint proof agree on the isolated mechanism.

### Additional printed defect that does not affect acceptance

The first inequality in both the published lemma and author preprint has the summation upper index tau instead of l. This too is visible in the PDF images. The setup, second inequality, and proof clearly use the l fixed divisors. The candidate reconstructs the correct finite sum and does not reproduce this typo. Its source attribution remains valid, but future literal transcription should flag this additional source defect.

## Supplementary primary citations for Section 3

### BCHM

Primary publisher page: https://www.ams.org/jams/2010-23-02/S0894-0347-09-00649-3/viewer/

Published PDF URL: https://www.ams.org/journals/jams/2010-23-02/S0894-0347-09-00649-3/S0894-0347-09-00649-3.pdf

Primary author preprint: https://arxiv.org/abs/math/0610203 ; PDF https://arxiv.org/pdf/math/0610203

The publisher text labels the Fano-type Mori-dream-space result **Corollary 1.3.2**. Its assumptions are a projective morphism to an affine base, X Q-factorial, (X,Delta) divisorially log terminal, and -(K_X+Delta) ample over the base. A smooth complex projective Fano variety satisfies this with Delta=0 and base a point. Thus the candidate's published reference is correct.

Direct retrieval of the AMS PDF returned HTTP 403. To avoid relying only on parsed publisher mathematics, I separately downloaded and visually checked the authors' arXiv v2 preprint, p. 9, where the corresponding result is **Corollary 1.3.1**. The preprint numbering must not be silently substituted for the published numbering. This retrieval limitation leaves no substantive source issue because the publisher text establishes the published number and the primary preprint supplies the fully rendered mathematical assumptions.

### Okawa

Primary URL: https://arxiv.org/abs/1104.1326 ; PDF https://arxiv.org/pdf/1104.1326

The downloaded primary preprint was independently rendered at pp. 6–7.

- **Proposition 2.8, p. 6:** finite contracting birational maps give an effective-cone decomposition into closed rational polyhedral Mori chambers, with each chamber the join of a pulled-back nef cone and an exceptional cone.
- **Remark 2.12, p. 7:** on a Mori dream space the negative part is uniquely characterized as 1/m times the fixed part of |mD| for sufficiently divisible m.
- **Proposition 2.13 and proof, p. 7:** P and N are Q-linear on each chamber after passing to a suitable small Q-factorial modification, and N(D) is an effective exceptional divisor.

These locations directly support the candidate's chamberwise/divisorial interpretation. The citation to Proposition 2.8 and Section 2.3 is correct; citing Proposition 2.13 explicitly as well would be helpful but is not an acceptance requirement. The source does not support claiming all positive parts are nef on the original model without additional reasoning. The candidate avoids that claim and explicitly distinguishes the source's nef restriction from the general chamberwise formulation.

## Short exact fragments safe for final user reuse

The following quoted fragments total fewer than 25 words per source:

- OWR, p. 839: “Let us use all assumptions and notations of Section 1.” and “for every prime divisor F over X. How to do this?” (21 words combined).
- Published CFKO, pp. 712–713: “Let F be any prime divisor over S” and “Thus, we get the first inequality” (16 words combined).
- Author preprint CFKO, p. 23: “Lemma 26.” (2 words).
- BCHM author preprint, p. 9: “Then X is a Mori dream space.” (7 words).
- Okawa, p. 7: “On Mori dream spaces, Zariski decomposition is unique.” (8 words).

No final response needs a quotation; concise paraphrase with direct primary links is preferable. PDF page images and downloads remain scratch evidence in ignored `tmp/final/source_check`; the durable certificate is this report plus the log, manifest, and verdict.
