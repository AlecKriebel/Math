# Independent priority and attribution audit

Audit checkpoint: 2026-10-06, America/Los_Angeles (remote receipts retrieved on 2026-10-07 UTC). This audit concerns the exact geometric target and its provenance. It does **not** certify the central unreviewed family 004 proof. No external individual was contacted. The upstream checkout was read only; no Git mutation was performed.

Completion estimates for this bounded audit: 90% of priority/attribution work; 0% certification of the upstream arithmetic breakthrough by this auditor. Overall mathematical and publication percentages must be supplied by the lead researcher after reconciling all dependency audits.

## Executive finding

The passage from rational Hilbert's tenth problem to rational-point existence on arbitrary smooth projective geometrically integral varieties is established machinery. Over Q, even that decision-equivalence predates Poonen's general number-field treatment: his Remark 1.2(c) attributes an earlier route to **R. Robinson**, as presented in Smorynski, *Logical Number Theory I* (1991), §II.7. A follow-on note can explain a newly available consequence **only after** family 004 is validated. It must not advertise a new geometric reduction or an independent solution of rational H10.

I found no exact smooth-projective undecidability theorem in the relevant source manuscripts or a current primary publication of the proposed follow-on theorem. That negative search is not proof of novelty. All substantial mathematics in the proposed core consists of a claimed new arithmetic input and a published transfer. The elementary height consequence adds a precise computability formulation, not a new arithmetic-geometric mechanism.

An unconditional publication is not cleared by this audit. Source validation is an independent necessary gate. If that validation fails, preserve a conditional consequence and the exact obstruction; do not announce removal of the hypothesis.

## Positive primary evidence and chronology

1. **Poonen, original geometric transfer.** *Existence of rational points on smooth projective varieties*, [author PDF](https://math.mit.edu/~poonen/papers/chatelet.pdf), [JEMS publication](https://ems.press/journals/jems/articles/1924), DOI [10.4171/JEMS/159](https://doi.org/10.4171/JEMS/159). I inspected Theorem 1.1(i), Remark 1.2(b),(c),(f), Theorem 1.3, §§9–10 and the bibliography, not just the abstract. For a fixed number field, a decision algorithm on regular projective geometrically integral varieties gives one on arbitrary varieties. His effectivity step takes a finite disjoint union; §10 computes components, checks geometric integrality and rejects other components using Lemma 10.1. Thus the paper supplies an algorithmic/oracle transfer, not a stated dimension-preserving many-one map to one promised input. The [arXiv record 0712.1782](https://arxiv.org/abs/0712.1782) records v1 on 2007-12-11 at 17:50:46 UTC. EMS records submission on 2007-12-18 and publication on 2009-06-30. The author PDF carries the manuscript date 2008-06-04. These are distinct dates. The Q-case predecessor is explicitly credited to R. Robinson through [Smorynski's 1991 book](https://link.springer.com/book/10.1007/978-3-642-75462-3), §II.7; I have not independently inspected that book section and do not assign Robinson an earlier public date.

2. **Independent later recognition of equivalence.** Olivier Wittenberg, *Some aspects of rational points and rational curves*, [author ICM survey PDF](https://www.math.univ-paris13.fr/~wittenberg/icm.pdf), p.15, explicitly records that restricting arbitrary number-field varieties to smooth projective varieties does not change the existence decision problem, citing both Smorynski §II.7 and Poonen Theorem 1.1(i). The neighboring discussion contrasts rationally connected varieties, where the restriction can matter. This confirms that the proposed transfer should be framed as inherited.

3. **Related old integral-point theorem is different.** Poonen, *Automorphisms mapping a point into a subvariety* (appendix by Matthias Aschenbrenner), [author PDF](https://math.mit.edu/~poonen/papers/automorphism-combined.pdf), Corollary 4.3, proves undecidability of **integer** solutions for affine inputs whose projective closure is smooth and geometrically integral. I inspected Lemmas 4.1–4.2 and Corollary 4.3. This is not the requested rational-point existence problem on the entire projective closure; replacing integer solutions with projective rational points would lose the relevant constraint.

4. **Existing height undecidability theorem is different.** Natalia Garcia-Fritz, Hector Pasten and Xavier Vidaux, *Effectivity for existence of rational points is undecidable*, [arXiv 2311.01958](https://arxiv.org/abs/2311.01958), [full text v2](https://arxiv.org/html/2311.01958v2), [JNT publication](https://www.sciencedirect.com/science/article/pii/S0022314X25001180), JNT 276 (2025), 81–97. I inspected the language definition and exact Theorems 1.1–1.2. Their undecidability concerns ring equations **augmented by height-comparison predicates**; comparisons on tuples of length at most three suffice. It neither gives plain H10(Q) undecidability nor directly states the requested no-bound result for arbitrary embedded smooth projective promised inputs. Cite it only as adjacent prior work, not as the needed arithmetic input.

5. **Explicit family construction is inherited too.** Bianca Viray, *A family of varieties with exactly one pointless rational fiber*, [arXiv 0908.4440](https://arxiv.org/abs/0908.4440), J. Théor. Nombres Bordeaux 22 (2010), 741–745, DOI [10.5802/jtnb.743](https://doi.org/10.5802/jtnb.743), makes Poonen's family explicit. arXiv records v1 on 2009-08-31 and v2 on 2009-10-12. This audit used the publication record/abstract to identify the citation chain; I do not claim to have verified that paper's construction. No novel-family claim belongs in the present note.

## Upstream release: exact provenance and scope

Pinned commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; remote: [openai/math](https://github.com/openai/math). Family 004's manuscript-specific [README and BibTeX](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/README.md) assign author **OpenAI** and manuscript date **September 24, 2026**. Its introduction, `thm:main`, concerns finite integer-coefficient polynomial input with the number of variables part of the input and unknowns in Q.

The supplied citation is:

```bibtex
@misc{OAI:Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026,
  author = {{OpenAI}},
  title = {{Hilbert's tenth problem over the rational numbers}},
  howpublished = {OpenAI Math Release preprint
                  \href{https://github.com/openai/math/blob/main/preprints/Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026/main.pdf}{OAI:Hilberts-tenth-problem-over-the-rational-numbers-September-24-2026}},
  year = {2026}
}
```

Preserve the manuscript-specific author/title/key, and add the precise commit/version in a note or separate source ledger. Do not replace its author with the follow-on author. The repository README says verification stages vary and some unformalized outputs may have issues. Family 004 has no `lean/docs/004.md`; the formalization catalogue searches do not show its exact paper. This absence does not itself prove mathematical failure.

The source's §7, `thm:degree-normal-form`, **already claims** Turing degree 0′ and quartic/supplied squared-quadratic-list normal forms. Its proof explicitly does not establish many-one completeness of H10(Q). These are not fresh follow-on contributions. The family 004 companion's exact main theorem is a pointwise 2-converse for rational-two-torsion elliptic curves with full 2-power Selmer corank 0 or 1. Its introduction and roadmap do not state the smooth-projective target. The H10 bibliography key `Poonen2009` is *Characterizing integers among rational numbers with a universal-existential formula*, not the JEMS geometric-transfer paper.

Read-only GitHub REST receipts, including retrieval timestamps and response headers, are in `sources/priority_remote/`. At retrieval:

- Repository `created_at`: `2026-10-06T21:47:02Z`; initial commit author/committer time: `2026-10-06T21:58:50Z`.
- `commits/main` equals the pinned commit; complete returned main history has one commit, titled *Initial commit*.
- Commit histories restricted to the H10 manuscript and the pointwise companion each contain only that commit.
- Issues, releases and tags endpoints return empty lists.

Therefore **no later committed correction was detected at this retrieval**. The manuscript's September date and Git commit timestamp do not prove an earlier public disclosure. Repository creation and reachable history constrain provenance but do not by themselves prove the exact instant when the repository became public. The user's October 6 release description is consistent with the observed initial public repository. No first-to-disclose claim is justified.

## Companion/corpus duplication audit

Read the supplied local triage: `openai_followon_batch2_20261006/REPORT.md`, §9; `agent_notes/arithmetic_logic.md`; `agent_notes/final_selection_audit.md`. The triage already proposed this route and expressly was not a source-proof or full-priority certification. It cannot support a claim that the idea originated in this new effort.

Direct exact-scope reading: family 004 introduction and §7; its companion introduction/roadmap; CONTENTS family 004; family 242's integer at-most-one-solution consequence. Family 242 explicitly disclaims corresponding uniqueness assertions over Z or Q, so it is not this target.

The saved `sources/priority_remote/corpus_search.json` records a search of 8,987 `.tex`, `.bib` and `.md` source files under pinned `preprints/`, exact patterns and all hits. Searches cover Châtelet, geometric-transfer title, smooth/projective plus decidability/algorithm proximity, and computable height-bound wording. Apparent Châtelet hits elsewhere are Weil–Châtelet, a unitary equation label, or an unrelated author's surname. The only `Poonen2009` hits belong to family 004's different definability reference. No exact target statement was found. The machine search only identifies candidate files; it does not inspect every theorem in every manuscript and cannot establish novelty.

Current web searches on 2026-10-06 local time covered the exact geometric phrases, H10(Q)/OpenAI 2026 correction terms and the height-bound formulation. The mathematically relevant primary hits inspected are itemized above. Search-engine relative publication labels were not treated as priority evidence. Historical works and surveys calling H10(Q) open describe their own publication state, not proof that it is still open after today's unreviewed release.

## Safe novelty and publication wording

If the arithmetic input passes scrutiny, a defensible statement is: *We spell out the smooth-projective consequence of OpenAI's negative rational H10 theorem using Poonen's published effective transfer, with explicit promise and height-search conventions.* Explain that the arithmetic theorem removes the hypothesis from an already established conditional implication. Avoid *we prove rational H10*, *new geometric reduction*, *first*, *fixed dimension*, *many-one hardness*, or *full formalization*.

Without an independently justified new in-scope extension, the core is an immediate corollary. All of its mechanisms are already public in the two cited inputs. This does not mean an explicit expository corollary statement was located; it means one must not advertise an independent new method or central breakthrough. A failed exact-keyword search cannot supply the missing novelty.

For the optional height result, specify primitive homogeneous coordinates, multiplicative height `max |a_i|`, the actual presentation/embedding, and a computable input-size parameter. A computable bound would make finite enumeration a decision procedure. This is an elementary consequence of undecidability, and hence inherits every source-validity limitation. A bound on one point when points exist differs from effective Mordell's bound on every point under a finite-point promise. Do not blur those results.

## Exact remaining gaps

Chronology clarification added after independent package review: the EMS landing page lists submission on 18 December 2007, whereas the published article's first page lists receipt on 20 March 2007 and revision on 22 August 2008. These conflicting primary metadata are preserved without silently reconciling them. The arXiv v1 public timestamp remains 11 December 2007; a received date alone does not establish public disclosure.

1. Family 004's pivotal proof/dependencies need independent mathematical validation. This is the decisive unresolved gate; this priority audit supplies none.
2. No independent new mechanism has been identified in the proposed transfer/height package. Publication must accurately identify an immediate consequence, and be withheld as an unconditional solution if the arithmetic input fails.
3. R. Robinson's route is attributed through Poonen; Smorynski §II.7 has not been independently read here. Cite this predecessor conservatively rather than inventing an earliest date or claiming to reproduce it.
4. Refresh the live commit/correction check immediately before any promotion or deposit; the present result is timestamped, not a continuing monitor.
