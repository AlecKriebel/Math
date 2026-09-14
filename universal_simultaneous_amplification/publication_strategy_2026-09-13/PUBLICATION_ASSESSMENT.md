# Publication assessment: simultaneous amplification beyond fitness 3/2

Assessed September 13, 2026 (Pacific time). Scope: **SimAmpB, Papers row 13 only**. The other papers in the supplied workbook were context and have not received new scores or publication assessments.

**Recommendation: score 7.3/10, make two focused proof clarifications, invite selective specialist feedback, and target journal submission in October 2026. Do not make full Lean formalization a prerequisite.** The existing primary and secondary journal choices can remain unchanged.

## What the paper establishes

The main theorem constructs one sequence of finite connected, loopless, undirected weighted graphs that is chosen independently of fitness. For each fixed fitness 1<r<R_hyb, all sufficiently large members beat the complete graph of the same order under both Birth–death and death–Birth updating. Here R_hyb=1.5028569127905696…, the specified isolated root of a sextic. The population threshold may depend on r. This is an existence theorem with carefully ordered quantifiers, not a practical finite-population performance guarantee.

The mechanism combines a clique of size C=t^4, q=t heavy pairs, and roughly 0.7508t hub pendants. Pairs and pendants have complementary effects under the two update rules. An exact finite-state Schur complement identifies the separated migration process. Establishment, cleanup and reciprocal-invasion estimates must control errors below q/C=t^-3, because the amplification advantage itself vanishes at that scale. The exact macro chain accounts for adverse center reversals. Two rational response functions then determine the available fitness interval. A compact-uniform dyadic choice of positive coupling closes the fitness-independent quantifier.

The architecture optimum is restricted to fixed positive parameters in the displayed first-order dilute pair–pendant model. It does not determine the unrestricted simultaneous-amplification threshold, rule out other constructions, or provide a finite universal upper bound. An entirely rational-weight specialization already crosses 3/2, with endpoint approximately 1.50176815.

The relevant published comparator is [Svoboda, Joshi, Tkadlec and Chatterjee (2024)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012008), whose simultaneous-amplifier theorem covers 1<r<1.2. That paper already uses fitness-independent modular constructions, so fitness independence itself should not be presented as originating here. Its theorem is also stated with a different uniformity in fitness/population size; the comparison should show quantifiers explicitly. The 3/2 predecessor is your own earlier unrefereed release. Crossing it is meaningful progress, but should not be described as resolving a famous established 3/2 conjecture.

## Impact score

The workbook's rubric asks for importance within the actual subfield **assuming correctness, genuine novelty, and publication**. My score is **7.3/10**, with a reasonable judgment range of 7.0–7.6. This replaces the previous ChatGPT score of 7.6; the Claude score of 7.0 stays untouched. Their existing average formula consequently evaluates to 7.15 (Excel display may round according to its existing format).

The result earns the “strong specialist result” category through a substantially larger interval than the verified published comparator, an exact optimization within a concrete architecture, a rational witness, and an analytic method that takes the small gain scale seriously. It is clearly worth selective circulation and journal submission.

I would not put it in the 8+ “major subfield advance” band on current evidence. Simultaneous amplification was already known; the unrestricted threshold stays open; amplification vanishes asymptotically; the weak coupling can be extremely small; and no useful finite-size or fixation-time guarantee is supplied. These are limitations of scientific reach, separate from proof confidence. The small numerical increment past your earlier 3/2 result alone is not the principal publication case.

## Review findings and immediate next step

I read the full manuscript and used two independent analytic/computational review routes. They found no decisive counterexample or algebraic error. Four supplied certificate programs passed in a matching Python/SymPy environment, and a separate exact computation checked rational positivity through r=1.5017 and macro-chain identities with reversals. These are strong checks of the finite algebra; they do not machine-verify the population asymptotics. See the two reports in `independent_checks/` for exact scope and evidence.

Before seeking a substantial reading or submitting, make a small, versioned revision addressing:

1. **Death–Birth cleanup, current source lines 903–937.** Hitting a bounded core deficit and then waiting for hub activation does not ensure the deficit is still bounded at activation. Explicitly use the event that hub activation occurs before the next ordinary-core change. At bounded deficit its activation intensity is uniformly bounded below and ordinary-change intensity uniformly bounded above, giving a fixed positive success probability. Regeneration then supports the existing repeated-attempt argument. The independent review classifies this as a repairable exposition/checkability gap, not a demonstrated false theorem.
2. **Weak-cut inverse wording, current source lines 439–441.** Specify that the uniformly bounded inverses are the fast-block inverse and the inverse of the scaled interior Schur complement. The full transient inverse can diverge when the coupling vanishes.
3. **Deposit consistency.** The public manuscript still says a new identifier has not been assigned, despite the current [Zenodo DOI](https://doi.org/10.5281/zenodo.22089807). It also links the v2.0.3 source directory while the record describes v2.0.4. Synchronize the manuscript, README, version/tag references and deposited source on the next revision. The tracker abstract additionally mentions an affine endpoint obstruction that the reviewed current manuscript does not separately state/prove; replace that stale abstract with the actual deposited abstract when refreshing metadata. This review does not count that extra assertion as an additional theorem.

For a reader, the most useful addition is a compact proof-dependency map identifying exactly where o(q/C), o(1), and o(1/C) estimates are needed. Position the paper around the improved range and complementary module mechanism, while explicitly contrasting the quantifiers with the 2024 theorem. The rational witness can make the algebra easier to enter without requiring a reader to start with the sextic optimizer. These are bounded presentation improvements; a new construction or larger threshold is not required before submission.

## Who could provide useful input

The tracker records only an August 24 Zenodo upload. It contains no recorded specialist contact for this paper. That is a statement about the supplied record, not proof that no contact occurred.

If you have not already shared it, the highest-value initial readers are **Josef Tkadlec and Jakub Svoboda**: both coauthored the directly preceding simultaneous-amplifier paper. Tkadlec also works on limits of amplification and [evolutionary graph theory](https://sites.google.com/view/pepa-tkadlec/research); Svoboda's [research page](https://pub.ista.ac.at/~jsvoboda/my-webpages/) identifies the relevant evolutionary and probabilistic work. Their most useful input would be whether the range/quantifier comparison is positioned correctly and whether the small-gain stochastic proof closes as written. Start with one or two directly relevant people, rather than broadcasting to the entire author group.

For an additional independent perspective, **Benjamin Allen**, lead author of the [2020 death–Birth transient-amplifier paper](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007529), is particularly relevant to fixation and biological interpretation. These are suggestions based on subject expertise, not statements about availability, endorsement or willingness to review.

Only you should decide whether and how to contact these researchers. No messages or outreach drafts were prepared or sent. A private comment is not permission to quote or attribute it publicly; public feedback and acknowledgments should reflect the contributor's wishes. Do not describe existing AI reviews as external human peer review.

## Lean decision

**Full formalization could materially improve assurance, but it is a poor immediate publication investment for this paper.** Being an independent researcher does not by itself make Lean a requirement. The value would come from checking the specific mathematics, rather than from a credential attached to the author.

The easiest components to formalize are response identities, rational margins, the polynomial/optimization argument and perhaps finite macro-chain identities. These already have independent exact certificates. Formalizing them would be useful but would leave the main acceptance risk—the analytic estimates tying those formulas to actual fixation—largely unchanged.

The high-value end-to-end project would need faithful definitions of the two Moran kernels and initialization, finite absorption and rare-coupling trace theory, adapted comparison and stopping arguments, compact-uniform bounds, and the final asymptotic/diagonal theorem. Mathlib has [matrix Schur-complement results](https://leanprover-community.github.io/mathlib4_docs/Mathlib/LinearAlgebra/Matrix/SchurComplement.html) and [discrete-time optional stopping](https://leanprover-community.github.io/mathlib4_docs/Mathlib/Probability/Martingale/OptionalStopping.html), but those ingredients are not a ready-made verification of this manuscript. The amount of additional work is uncertain; this is a substantial separate project, not an inexpensive conversion of the existing algebra scripts.

If you choose a pilot later, specify one bounded theorem and a resource cap before starting. An algebra-only proof should be labeled exactly that. An end-to-end claim must not assume the response expansions or center proposition it is supposed to validate. Require a statement audit and an axiom audit; Lean's [official documentation](https://lean-lang.org/doc/reference/latest/Axioms/) explains that `sorry` introduces `sorryAx`. No invented theorem assumptions should substitute for missing mathematics. My priority order is manuscript clarification, specialist reading, journal submission, and only then optional formalization.

## Journal and timing

The existing journal entries are appropriate and remain unchanged. The primary journal's [scope](https://link.springer.com/journal/285/aims-and-scope) expressly includes rigorous stochastic processes and graph theory relevant to biological systems; it has published [closely related amplifier work](https://link.springer.com/article/10.1007/s00285-023-01937-1). The backup's [scope](https://shop.elsevier.com/journals/theoretical-population-biology/0040-5809) emphasizes mathematical theory with clear biological significance. The present rigorous existence theorem fits the primary positioning well.

Suggested schedule, as planning advice rather than a journal rule:

- **September 14–20:** incorporate the proof clarifications and reconcile metadata, then freeze the version intended for readers.
- **September 21–October 11:** allow roughly three weeks for a small number of relevant specialists to comment, if you choose to share it. A DOI sitting online does not establish that specialists have reviewed it.
- **October 12–19:** submit if the focused fixes are checked and no substantive unresolved objection has appeared. Earlier submission is reasonable if a useful review arrives sooner. If nobody responds, submission can still proceed after your revision is complete; silence is neither validation nor a reason for an indefinite delay.

A substantive objection should be resolved on its merits before submission. An offer of imminent detailed feedback can justify a short extension. Neither Lean completion, arXiv access, public endorsement, nor a set number of preprint downloads should be a submission gate. Springer Nature [explicitly permits preprints without treating them as prior publication](https://support.springernature.com/en/support/solutions/articles/6000258807-preprints), so the Zenodo posting itself is compatible with the selected primary journal route.

## Version and evidence record

Zenodo record 22089807 reports version 2.0.4 and publication date 2026-08-25. Its source archive's MD5 is `a58dc59ffbc4b3f76e36903855b79e60`, matching the downloaded bytes. The archive manuscript differs from local `main.tex` only in the date and figure-label position. This validates the manuscript identity for the mathematical assessment; it is not authentication of the unavailable local v2.0.4 Git tag. The API response and extracted manuscript are retained with this assessment. The public PDF was not separately subjected to full visual QA in this task.

Primary literature searches were current to this assessment and did not locate a superseding competing theorem. That is bounded search evidence, not an exhaustive novelty certification. Publication and acceptance remain editorial decisions. No manuscript edits, journal submission, new Zenodo deposit, or immutable release were performed as part of this assessment.
