# Source and literature audit

Checked 2026-09-30. Full PDFs were retrieved for the following primary sources. The relevant model definitions and theorem/conjecture statements were read; no claim is made to have independently recertified all their proofs.

- [Mörters, Emergence of condensation in a self-organised growth model, OWR35/2015, printed1997–1999](https://ems.press/content/serial-article-files/46582). SHA-256 `3115fa983b9e8bd40feae87a9a143daa2bfeb183c50dc4f01de924cc392c2ef9`.
- [Dereich–Mailler–Mörters, Non-extensive condensation in reinforced branching processes, model Example1, RV, Theorem2.2/Corollary2.3 and Section8](https://arxiv.org/pdf/1601.08128). SHA-256 `0998010f1c1df575838f5dc44995b3784cfaacad661b25239cacfd95df82fe63`.
- [Dereich–Mörters, Emergence of condensation in Kingman’s model, deterministic generation recurrence and Theorem1](https://arxiv.org/pdf/1207.6203). SHA-256 `c3f99c31cab8fec8f66fc6f5386e1b07a0b8120bd46fa92f1a97380b321e6607`.
- [Mailler–Mörters–Senkevich, Competing growth processes, model and largest-family limit statements](https://arxiv.org/pdf/1909.07690). SHA-256 `a18ee7445810418c63fbefffa01267cdc14ab054a92d3402dc7fe8fd72871043`.

## Clock and observable distinctions

The original report uses births at physical rate f and mutation probability beta. Clonal births have rate (1−beta)f. Its normalized empirical measure is explicit on printed1997; its family-sum display on1998 lacks the required 1/N factor, which cannot replace that definition. The profile conjecture is printed on1999. The report does not specify a convergence mode on that display; this work rules out convergence in probability to it, and hence stronger deterministic-limit modes.

DMM's Example1 identifies the same house-of-cards model using its gamma parameter equal to1−beta. Its regular-variation hypothesis uses tail exponent alpha, while Conjecture8.1 prints Gamma shape alpha+1, differing from OWR's alpha. Both physical-time expressions must be distinguished from a rescaled clone clock. The DMM largest-family Gamma limit and its non-extensive-condensation theorem do not establish the collective-profile conjecture.

The Kingman model is a deterministic recursion indexed by generation. Its Theorem1, including its assumptions on the mutant tail and initial distribution, cannot be transferred to this stochastic birth process by merely renaming generation as physical time. The 2021 competing-growth paper concerns extremal families and associated point-process limits, again a different observable. Current author publication lists and targeted searches were checked; they do not establish exhaustive novelty or the absence of every later corrected-profile result.

## Remaining claim boundary

The stochastic clock lemma is proved directly in the artifact and does not rely on an unproved growth correction. The conclusion is only a necessary rate constraint and the resulting counterexample to the displayed physical-time formula. A corrected Gamma profile is not proved, and neither the disputed shape parameter nor full universality is resolved.
