# Source scope and prior-work audit

Checked 2026-09-30. The exact task remains the nonlinear behavior of the peaked periodic wave of the **reduced Ostrovsky equation**, not a nearby peakon equation.

## Original source

The requested problem-site URL was attempted first but was inaccessible to the web reader. The complete pinned record was read. No matching code entry was present in the pinned `research_results.json` corpus; the record's dated literature triage was therefore checked against the actual cited papers.

Anna Geyer's contribution, joint work with Dmitry Pelinovsky, occupies printed pp. 1940–1942 of [OWR 32/2019](https://ems.press/content/serial-article-files/46811). Its equation is $u_t+uu_x=\partial_x^{-1}u$ for mean-zero periodic functions, and its profile is $(3z^2-\pi^2)/18$. The report describes linear and spectral instability, then explicitly states that nonlinear instability is still open. It points out that smooth Sobolev well-posedness excludes the peak and that the linearized domain permits jumps which $H^1$ does not.

The workshop occurred in July 2019; the [EMS publication record](https://ems.press/journals/owr/articles/17128) dates publication to 10 September 2020. The record's mixed 2019/2020 metadata is explained by that distinction.

## Established results and nonmatching results

- [Geyer–Pelinovsky, SIAM J. Math. Anal. 51 (2019), 1188–1208](https://pelinovsky.mcmaster.ca/PaperBank/PeakedWaveOstrov.pdf), Theorem 1 and the discussion on pp. 1206–1207: uniqueness and linear instability. The perturbation domain is $X^1_{\rm per}=\{v\in\dot L^2:(c_*-U_*)v\in H^1\}$. The authors explicitly do not infer nonlinear instability from this result.
- [Geyer–Pelinovsky, Proc. AMS 148 (2020), 5109–5125](https://pelinovsky.mcmaster.ca/PaperBank/PeakedSpectralUnstable.pdf): the linearized spectrum covers a vertical strip. A spectral strip is not by itself a nonlinear theorem in a different solution space.
- [Natali–Pelinovsky–Wang, arXiv:2503.15071](https://arxiv.org/abs/2503.15071), [published article](https://www.cambridge.org/core/journals/journal-of-nonlinear-waves/article/instability-of-the-peaked-travelling-wave-in-a-local-model-for-shallow-water-waves/DE8AD3FB7366FEB52BC613CDB1611EC8): nonlinear gradient instability for a Hunter–Saxton-related local model. Its displayed equation has an extra squared-gradient term and different normalization. Its theorem does not directly resolve the reduced Ostrovsky question. It is relevant methodological prior work and is credited as such.

## Superseded nonlinear claim: version history

The separate reviewer identified an important earlier version, which was then checked directly. [arXiv:1804.03788v1](https://arxiv.org/abs/1804.03788v1), submitted 11 April 2018, was titled *Linear and nonlinear instability of the peaked periodic wave in the reduced Ostrovsky equation*. Its Section 4, Definition 4 and Lemma 10, asserted $H^1$ orbital instability using an $L^2$ departure. The [2 January 2019 revision](https://arxiv.org/abs/1804.03788), and the published 2019 paper, remove that nonlinear theorem and explicitly leave nonlinear instability open.

This is a superseded claim, **not an official arXiv withdrawal**. It must be credited and retained in the source history, but it is not a valid current theorem to invoke. In the old argument, smooth Sobolev well-posedness is imported for perturbations of the nonsmooth peak without establishing an appropriate evolution theorem, and the asserted long lifetime is not justified in that setting. Its contradiction also uses a bound proportional to the initial perturbation size, stronger than the qualitative orbital-stability definition supplies. These observations are reasons not to reuse that argument, not a claim about the authors' reasons for revising it.

The present scoped candidate uses neither step: its corner-compatible evolution is constructed directly, continuation is conditional only on a fixed slope bound, and departure crosses a fixed positive slope threshold. It does not restore or claim the earlier $L^2/H^1$ conclusion. The old semigroup-based route and the related later characteristic methods are relevant prior work; no first-priority assertion is made.

Searches for reduced-Ostrovsky nonlinear instability, Lipschitz characteristic evolution, gradient instability, and the exact peaked profile did not locate the precise strong-norm theorem in this package. This is a bounded negative search, not a priority certificate. No outreach was undertaken.

## Precisely scoped contribution and unresolved part

The candidate supplies a local characteristic solution class containing the peak and proves nonlinear orbital departure in $W^{1,\infty}$. It explicitly proves uniform local existence for its perturbation family, one-sided slope evolution, and continuation while slopes remain bounded. The argument controls the moving corner value rather than freezing it at the traveling-wave speed.

The result does **not** imply a fixed $L^2$ or $H^1$ orbital departure. Narrow derivative perturbations can have a fixed slope discrepancy on a small region without a fixed weak-norm discrepancy. It also does not choose or prove uniqueness of an entropy or other weak continuation after a possible gradient breakdown. These are the precise boundaries that prevent promoting the original source problem to a full solved status.

## Previous project work

Before starting, all-state PR and remote branch searches for 30004186 were empty. The cloned queue row was rank 46, queued, 0/5. There was no prior attempt directory, matching state entry, or related-target-group hit. No previous attempt, including an invalidated one, was reset. The only proof work is recorded as substantive response 1/5; the original target outcome remains partial, with a complete candidate for the separately stated strong-norm theorem.


# Current source, historical scope and readiness qualifications

2026-10-02T00:00:35.622836+00:00 — Current source-bound audit correction; original dated records remain exact archives.

OWR32/2019 contributionpp1940–1942 concerns the mean-zero quadratic reduced Ostrovsky equation and periodic parabolic peak. Its closing nonlinear question names no mandatory instability norm. Retain the conservative unsolved/partial disposition for this explicit W1infinity local-characteristic theorem; L2/H1/global weak continuation are limitations, not a uniquely prescribed OWR target. Workshop2019 and report publication10September2020 are distinct. The2019/2020 linear/spectral papers supply background, not a nonlinear proof.

The complete actual2018v1 nonlinear proof was checked. Its fixed peak plus smooth perturbation class fails generic jump evolution, its smooth lifespan import does not include a nonsmooth peak, and its proportional Bdelta stability bound does not follow from qualitative stability. These are present audit deductions; v2 removes the claim, but no official withdrawal or author motive is inferred. The2025 published Hunter–Saxton-related theorem is a different equation with a squared-gradient source and different mean constraint; credit the method without importing its theorem or an H1 escape claim.

The original final17-path diff includes16 attempt files and QUEUE.md. Original body noqueue/confinedfolder assertions and provenance.shared_queue_modified:false are historical stage attestations contradicted as timeless final-head scope. Current metadata/body now explicitly includes the selected shared row. Original RESEARCH_LOG stage statements remain untouched; current correction governs acceptance. Model/effort/query/search/execution claims remain attestations, not authenticated telemetry, global prior absence or novelty certificates.

The pinned prior corpus has noOWR-17128-002 key. Actual readiness context is [source,{}], hash759ed8f6518e7a61a2356296cdc080f951f41bc93ca448182f1ce2143cda5a7b; read-only SQLite stores TEXT{} rather thanNULL. Original readiness lacks review_hash and is not a legacy-ready authentication. The current hash identifies source/prior context, not a mathematical-review artifact. Canonical main stillqueued0/5 and no target state/history at this checkpoint; original headunsolved1/5. Present acceptance reconciliation is pending after the new complete gate and exact remote merge.

All original science/source/oldreviews/code/receipts/ledger/log and ORIGINAL administration/body bytes remain exact. Original candidate pre-review header is explicitly superseded; sections1onward are unchanged. Three early-independent distinct families and root reconstruction/replays support the scoped result. Root synthesis follows family exposure and is not a fourth blind family. New finite/float controls supplement the written universal proofs. The NEW complete current gate is pending. Extensive AI use; unrefereed, no humanpeer-review/proof-assistant certification. No paper, DOI/deposit, release, trackerrow or external outreach.
