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

Searches for reduced-Ostrovsky nonlinear instability, Lipschitz characteristic evolution, gradient instability, and the exact peaked profile did not locate the precise strong-norm theorem in this package. This is a bounded negative search, not a priority certificate. No outreach was undertaken.

## Precisely scoped contribution and unresolved part

The candidate supplies a local characteristic solution class containing the peak and proves nonlinear orbital departure in $W^{1,\infty}$. It explicitly proves uniform local existence for its perturbation family, one-sided slope evolution, and continuation while slopes remain bounded. The argument controls the moving corner value rather than freezing it at the traveling-wave speed.

The result does **not** imply a fixed $L^2$ or $H^1$ orbital departure. Narrow derivative perturbations can have a fixed slope discrepancy on a small region without a fixed weak-norm discrepancy. It also does not choose or prove uniqueness of an entropy or other weak continuation after a possible gradient breakdown. These are the precise boundaries that prevent promoting the original source problem to a full solved status.

## Previous project work

Before starting, all-state PR and remote branch searches for 30004186 were empty. The cloned queue row was rank 46, queued, 0/5. There was no prior attempt directory, matching state entry, or related-target-group hit. No previous attempt, including an invalidated one, was reset. The only proof work is recorded as substantive response 1/5; the original target outcome remains partial, with a complete candidate for the separately stated strong-norm theorem.
