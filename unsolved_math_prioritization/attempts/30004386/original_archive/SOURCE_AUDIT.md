# Source audit for record 30004386

Checked 30 September 2026. Recommended status: **already_solved**, by prior published work. This status concerns the precise one-dimensional random-probability-measure question, not every large-deviation problem for high-dimensional projections.

## Original question

The problem-page lookup was unavailable. The complete pinned source record is preserved in `source_record.json`, from the verified ulamai/UnsolvedMath cache at revision `37e53eabe540fb458758e198be61634bd02ee008`, with attribution under CC BY 4.0. The research-results entry is null. Its August 2026 open triage had checked only the original report and missed the later paper.

The [complete report](https://publications.mfo.de/bitstream/handle/mfo/3713/OWR_2020_06.pdf?isAllowed=y&sequence=4) is Oberwolfach Report 6/2020, DOI 10.4171/OWR/2020/6, workshop 2–8 February 2020. The group-work report is on pp.411–413, by David Alonso-Gutiérrez, Nina Gantert, Samuel Johnston, Zakhar Kabluchko, Eliza O'Reilly, Joscha Prochno and Kavita Ramanan. Conjecture 1 and the intermediate Lemma 1 are on p.413, which was visually inspected. The definitions of the cube law, directions, Gaussian normalization and κ appear in the preceding pages. The dataset's report title mentions 2021, but the underlying workshop and report number are 2020.

The notation omitted from the standalone dataset question was recovered from this surrounding text. The uniforms are independent with support [-1,1]; κ contains a Gaussian term of variance (1−||α||²)/3. Both the full LDP and the whole closed-unit-ball limit set are part of the target.

## Resolution and version cross-check

- The [publisher page](https://www.impan.pl/en/publishing-house/journals-and-series/studia-mathematica/online/114493/projections-of-the-uniform-distribution-on-the-cube-a-large-deviation-perspective) verifies all three authors, the exact title, DOI 10.4064/sm210413-16-9, Studia Mathematica 264 (2022), 103–119, and online publication on 17 December 2021. Its abstract states the exact random-measure rate formula and normalization.
- The complete openly available [arXiv v2 manuscript](https://arxiv.org/abs/2103.16430v2), revised 19 September 2021, was downloaded and read, including Theorem A, Proposition 3.1 with Lemmas 3.2–3.3, and the sequence-space LDP in Proposition 3.4. The full text is an author manuscript; it is not being mislabeled as a downloaded typeset journal PDF.
- Theorem A and its continuation were checked directly against the original conjecture. The probability space, topology, speed, open-ball finite-rate domain, infinite boundary rate and variance agree.
- The weak compactness and homeomorphism proposition supplies the necessary closedness for the intermediate question. `SOURCE_STATUS.md` adds the elementary unit-norm coefficient approximation needed to make the converse attainability explicit for a sequence indexed by every sufficiently large N.
- An isolated variance-one sentence in the manuscript is inconsistent with its own displayed formula. The independent variance computation gives 1/3 and agrees with the theorem and publisher abstract. This is recorded rather than silently importing the typo.

The full author manuscript and publisher metadata suffice for this source-status identification; a new proof of the published theorem is not claimed. The large-deviation theorem's proof is based on a compact parameter space and sphere-coordinate estimates, and then transport through a homeomorphism. Its compactness is not compactness of the entire space of all real probability measures, and its coefficient topology is not the norm topology of ℓ2.

## Current literature and nearby results

The later primary paper by Kabluchko and Prochno, [*Large deviations for random matrices in the orthogonal group and Stiefel manifold with applications to random projections of product distributions*](https://arxiv.org/abs/2110.12977), explicitly identifies the Johnston–Kabluchko–Prochno result as a case generalized by that work. It is corroborating context, not needed as a substitute theorem. No correction or withdrawal of the exact cube theorem was found in the bounded title/author/DOI search.

Earlier and later quenched/annealed scalar-projection theorems, including work for general product measures, are different statements. The present resolution does not depend on their extra integrability assumptions. The only source distribution required here is the given bounded uniform cube law; no strengthening of the question has been inserted.

## Prior-attempt checks and workflow

The main queue row was queued with 0/5 attempts. Numeric-ID, problem-code, descriptive, history/reset, all-ref attempt-path, repository-path, exact remote-branch and all-state PR checks found no prior project attempt. A broader pinned-dataset search found no second record of this exact cube random-measure conjecture. Unrelated projection and κ-notation problems were not treated as duplicates.

The isolated branch is `dot/math-30004386`. Shared queue/state files were not edited or regenerated. No new substantive proof attempt was used: the exact published solution was identified during source readiness, and the subsequent work checks the source match and its direct intermediate implication. The actual model was gpt-6-astra with xhigh reasoning. Separate adversarial review is pending before a single source-status draft PR.
