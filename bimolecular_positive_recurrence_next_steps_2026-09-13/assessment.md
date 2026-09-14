# Publication assessment: single-linkage bimolecular positive recurrence

Assessment date: 13 September 2026, America/Los_Angeles. Reviewed version: 1.2.4. Author: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.

**Recommendation: conditional impact 7.8/10; seek focused specialist comments now, then aim to submit to Applied Probability during 5–12 October 2026. Do not make full Lean formalization, an arXiv endorsement, or an informal endorsement a prerequisite.** The timing is a recommendation, not a journal requirement or an automated commitment.

This assessment concerns this paper alone. It is based on the complete canonical mathematical source, the supplement's probability interfaces, a fresh standalone verification run, independent AI proof and literature audits, and current primary-source publication policies. No person was contacted, no outreach was drafted, and no journal submission was made. These reviews do not constitute independent human peer review or a machine-checked proof.

## Impact and what is actually new

The supplied scoring rubric asks how important a correct, genuinely novel, published theorem would be within its actual subfield. The **7.8** assessment is a judgment of mathematical significance under those conditions, not an acceptance probability, correctness confidence, citation forecast, or average of previous assessments. A plausible subjective range is roughly 7.5–8.1. The independent literature reviewer separately chose 7.7.

The theorem covers every finite weakly reversible stochastic mass-action network with one linkage class and complexes of molecularity at most two, for every fixed positive rate vector and every initial population. Each reachable class is closed; nonabsorbing classes are nonexplosive and positive recurrent; absorbing singletons have their point-mass laws. The main advance removes the pure unary-or-double-complex requirement for every species from Anderson–Cappelletti–Kim's 2020 theorem. It allows arbitrarily many species and addresses the difficult boundary-availability obstruction rather than merely extending a finite computation. [ACK2020](https://doi.org/10.1017/jpr.2020.28).

The marked-target method is the interesting potential source of further impact. It records the last reaction's target, subtracts it from the population, and makes a target-following reaction have exactly zero potential increment. That construction can preserve a useful delayed drift even where ordinary one-step entropy drift is positive. Its application beyond this theorem has not yet been established.

I would revise the earlier 8.4 downward because the present result is best described as a strong specialist advance, near the lower boundary of a major subfield advance. It does not settle all bimolecular networks, multiple linkage classes, or the full weak-reversibility conjecture, and it does not give quantitative tails or convergence rates. This is a scope judgment; the author's amateur status, AI use, and Zenodo hosting do not reduce the conditional score.

Two distinctions matter for attribution. Reachability symmetry under weak reversibility is already known and is properly attributed in the manuscript; it should not be counted as a second new theorem. Nonexplosion for a broader bimolecular class is also already known; nonexplosion alone does not give positive recurrence. [Paulevé–Craciun–Koeppl](https://people.math.wisc.edu/~craciun/PAPERS_NEW/Pauleve_Craciun_Koeppl_JMB_2014_FINAL.pdf), [Xu v2](https://arxiv.org/html/2409.05340v2).

The ConStRAINeD page currently describes a complete two-species proof and lists the five-author manuscript as in preparation. That announced result and this theorem have different scopes. Neither should be described as superseding the other without the missing manuscript. No accessible superseding arbitrary-species single-linkage binary theorem was located in the present search; unpublished or unindexed overlap remains possible. [ConStRAINeD results](https://constrained.polito.it/publications/).

## What was checked in the proof

The primary reading and independently assigned adversarial reading found **no specific substantive proof gap** in the current argument. The following chain was reconstructed rather than accepted from the old audit summaries:

1. For an enabled next source s and carried target t, the new residual is x−s, so factorial cancellation gives ΔV = log((x)ₜ/(x)ₛ). This includes zero complexes, boundary populations, repeated particles, and channel labels sharing a displacement.
2. Source probabilities yield δ(x,t) ≤ log pₓ(t)+C₀. The finite path episode includes deviation rewards and obeys Jₖ=δₖ+qₖpₖJₖ₊₁. The scalar supremum of log p+C₀+qpM tends to −∞ as M does, so an arbitrarily rare intermediate continuation does not invalidate the propagated bound.
3. The normalized logarithmic extraction keeps every divergent coordinate in I, including coordinates with zero limiting weight. The bimolecular case split supplies either a higher-weight enabled source or an exact invariant incompatible with divergence in one class. In the signed-invariant branch, the negatively weighted companion coordinates really stay bounded.
4. Properness plus finite terminal choices makes the exceptional set finite. Bounded episode lengths justify integrability in the stopped Foster argument. The finite trace controls original jump counts. Projection gives population returns, repeated anchor visits rule out explosion without assuming it first, and the strictly positive global lower bound on holding rates gives finite mean physical return time. Regenerative occupation then supplies the stationary probability.

The current standalone reproducer passed **57 tests** under CPython 3.12.14. Two independently regenerated report files matched one another and the committed canonical report, SHA-256 `dc14127494eaa6ccf3b36a91f5d714ba6f79e76476f8d199760bd3b5faeed586`. These finite checks support identities and boundary examples; they do not prove the universal theorem. This assessment did not rerun the entire PDF/wheel/archive release pipeline or every historical interpreter matrix.

## Best immediate improvement

The existing introductory cycle `0 → A+B → B → 0` is a good explanation of delayed correction, but it is deficiency zero and already falls under complex-balanced theory. The ACK worked example also lies within ACK's hypotheses. Neither is an error, but a reader would benefit from one additional example clearly showing the added coverage.

An independently checked candidate is

`0 → A+B → B+C → C → B → 0`,

with first rate constant 2 and all other rate constants 1. It has three species, five complexes, one linkage class, stoichiometric rank three, and deficiency one. A appears in neither A nor 2A as a complex. Complex balance would require the five fluxes `(2, ab, bc, c, b)` to agree, forcing b=c=2 and also bc=2, a contradiction. Its communicating class is all nonnegative integer triples: enabled paths create each singleton from zero, these paths can be lifted and concatenated, and weak reversibility provides returns. It therefore illustrates coverage beyond the ACK pure-species assumption, the complex-balanced sufficient condition at these rates, and the announced two-species theorem. This does **not** establish that every earlier analytical criterion or bespoke proof fails for this example.

Adding this example and a short known-versus-new comparison would improve readability more immediately than another large suite of finite checks. It is an optional explanatory improvement, not a discovered proof repair. The current manuscript was not changed in this assessment.

## Who could usefully read it

These are recommendations for the human author's consideration only. A small number of directly relevant readers is enough; their agreement is not a condition for journal submission.

| Priority | Reader | Specific value of outside input |
|---|---|---|
| First choice | [Daniele Cappelletti](https://staff.polito.it/daniele.cappelletti/) | Coauthor of ACK2020 and the announced two-species work; strongest overlap check and direct perspective on the boundary step being removed. |
| Equally natural first choice | [David F. Anderson](https://people.math.wisc.edu/~dfanderson/) | Coauthor of the conjecture and direct predecessor; can assess both significance and the marked-target argument. |
| Next | [Jinsu Kim](https://mathjinsukim.com/research/) | Direct predecessor coauthor; particularly relevant to sampled chains, recurrence, and path methods. |
| Optional later | [Andrea Agazzi](https://andagazzi.github.io/) | Relation to the announced two-species construction and multiscale boundary behavior. |
| Optional later | [Chuang Xu](https://sites.google.com/view/chuang-xu) | Distinction between nonexplosion and recurrence; stochastic class and boundary questions. |

The most valuable unresolved questions are whether the removed hypothesis is still a genuine literature gap, whether the top-complex alternative has a missed case, and whether the path-to-Foster interfaces are accepted by specialists. Focused mathematical input is more valuable here than asking for general approval, prestige, or a citation. The current paper and supplement already exist; another elaborate circulation package is unnecessary. Any communication must be prepared and sent by the human author under the project's independent-research policy.

## Lean: useful assurance, lower immediate priority

A faithful end-to-end Lean proof would materially strengthen assurance that the formal statement follows from its assumptions. It would not establish novelty, importance, biological relevance, or journal acceptance. An independent researcher does not inherently need formalization to submit a rigorous proof.

My recommendation is **defer full CTMC formalization; consider a bounded targeted pilot if resources remain after specialist feedback**. The best core target is the universal finite top-complex availability/invariant lemma, including arbitrary species count, arbitrary nonnegative real weights, and zero-weight divergent coordinates. Pair it with the exact factorial identity and scalar propagation. Formalizing only a handful of factorial instances or the elementary scalar optimizer would add relatively little assurance.

These targets still leave the compactification, stopping-time construction, finite-mean returns, nonexplosion, and stationary-law interface to be justified. Partial work should be described precisely as formalized lemmas, not a formalized positive-recurrence theorem. An honest delivery should pin the toolchain, map each formal statement to the manuscript, audit axioms and placeholders, and avoid taking the central conclusion as an assumption.

Current mathlib has relevant kernel/irreducibility definitions and optional-stopping results. That is useful infrastructure, but this limited inspection did not establish an off-the-shelf complete recurrence/CTMC development matching the paper. Full scope and cost would need a separate dependency audit; no reliable completion-time estimate is offered. [Kernel irreducibility](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Kernel/Irreducible.html), [optional stopping](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Martingale/OptionalStopping.html).

## Journal timing and publication metadata

Keep the existing primary route, Journal of Applied Probability through Applied Probability, and the existing secondary route, Stochastic Processes and their Applications. JAP is especially coherent because it published the theorem being extended. Applied Probability makes the JAP/AAP allocation itself; its current instructions generally place research papers of at most 25 printed pages in JAP. [Author instructions](https://www.cambridge.org/core/journals/journal-of-applied-probability/information/author-instructions).

Recommended sequence:

- **14–20 September:** reconcile the DOI/citation metadata, consider the explanatory example, and have the human author circulate to one or two closest readers if desired.
- **Following 2–3 weeks:** address concrete mathematical or novelty comments. Silence is neither validation nor a reason to keep waiting.
- **5–12 October:** submit to Applied Probability if no concrete unresolved issue has emerged. Submit earlier if useful comments arrive and are resolved. If a specialist identifies a specific gap or genuinely overlapping proof, resolve that issue before submission. If a reader explicitly commits to a near-term detailed review, a short extension can be sensible.

This timetable is intended to prevent indefinite preprint limbo. Public commenting can continue during peer review. Lack of arXiv or bioRxiv access is not an obstacle under Cambridge's preprint policy: sharing a preprint anywhere is not considered prior journal publication. Cambridge encourages citing the preprint's persistent identifier. Keep the substantive AI disclosure accurate in the eventual submission. [Preprint policy](https://www.cambridge.org/core/services/open-research-policies/preprint-policy), [JAP preparation and AI disclosure](https://www.cambridge.org/core/journals/journal-of-applied-probability/information/author-instructions/preparing-your-materials).

The Zenodo API confirms DOI **10.5281/zenodo.22089551**, resource type Preprint, version 1.2.4, and the three public files. Its published file checksums match the local public manuscript, supplement, and ZIP. The repository landing-page source still says “No DOI has been assigned”; update that statement and add the DOI to current citation metadata without rewriting frozen historical releases. The remote annotated v1.2.4 tag exists, and the present replay script enforces the exact annotated tag. The missing-tag concerns in the older pre-release audit are therefore historical, not current findings. [Zenodo record](https://zenodo.org/records/22089551), [record metadata](https://zenodo.org/api/records/22089551).

The updated workbook changes only this paper's assessment cells and directly affected presentation. The historical update text, other assessors' score, review checkboxes, and journal choices are preserved. The workbook remains local because it contains unrelated paper histories; the research assessment and checks are checkpointed in the repository.
