# Strict priority and attribution audit

Checkpoint: 2026-10-06 22:19 PDT (America/Los_Angeles). Independent audit by the priority research agent; primary-source historical review completed independently by a separate agent. Estimated priority-audit completion: 100% for the needed duplication/attribution decision (95% for an exhaustive historical audit, which was neither achieved nor needed); mathematical-resolution and publication-package completion are separate matters controlled by the project's source audits and final package reviews.

## Decision

**The specified consequence and its proof mechanism have already been publicly disclosed in the user's repository. Apply the user's duplication rule. Do not issue a new-discovery preprint or Zenodo deposit of these same core targets solely on the strength of this immediate algebraic consequence.** A fully substantiated research note can document and correct the earlier public triage, but the triage cannot be relabeled an unpublished independent solution. A genuinely substantive repair of the source theorem or another justified in-scope contribution would require its own fresh mathematical and priority assessment.

This is an affirmative duplication finding based on exact public files, not on failed searches. It is distinct from the mathematical question whether the unreviewed October 4 construction is valid. In particular, the prior triage explicitly described itself as conditional on the upstream theorem and said that upstream validation had not been undertaken. Prior public disclosure does not certify that theorem.

## Exact prior public disclosure

The unauthenticated GitHub API returned the following files from current public remote main of `AlecKriebel/Math`:

- [Batch report, section 4](https://github.com/AlecKriebel/Math/blob/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/REPORT.md).
- [Algebra/groups triage, section 1](https://github.com/AlecKriebel/Math/blob/f27318d83bd7000ef817957a9a4b3087de28d198/openai_followon_batch2_20261006/agent_notes/algebra_groups.md).
- [Public commit](https://github.com/AlecKriebel/Math/commit/f27318d83bd7000ef817957a9a4b3087de28d198), whose GitHub commit metadata records 2026-10-07T04:55:38Z, or **2026-10-06 21:55:38 PDT**, with message “Add second ranked batch of ten OpenAI mathematics follow-on research paths.”

The report states, verbatim:

> **Target.** A torsion-free finitely presented group G whose group algebra `F₂[G]` contains an idempotent other than 0 and 1. Extend the same example to every characteristic-two coefficient field. Also exhibit a nonzero cyclic projective module P with `R ≅ R ⊕ P` and `[P]=0` in `K₀(R)`.

Its next paragraph identifies the precise October 4 manuscript, the identities `ab=1`, `ac=0`, `c≠0`, and the construction `e=1−ba`, `P=eR`. The companion algebra triage goes further, verbatim:

> The direct sum R=baR⊕eR and maps r↦br, x↦ax identify baR with R. This is a precise cancellation failure, not merely an unsupported K-theory inference.

Thus all target conclusions, the same source, the same scalar defect, the same right module, the decomposition, and the isomorphism maps were public before this dedicated effort. The prior files do not contain an unconditional audit of the difficult source construction or an executed numerical witness. They are nevertheless a direct public disclosure of the entire proposed elementary follow-on theorem and proof outline. No new mathematical mechanism has been introduced by expanding those calculations into a self-contained proof.

Exact evidence is retained in `priority_evidence/`: the API content and commit-history responses plus the decoded remote bytes. Report blob SHA-1: `cad7c47503a836495f7379dda12760f8cfdc4f59`; SHA-256: `20746bbc95ea76c2661f51fb1c987e36004cc6a07de7a0fc3cd5184da08c8763`. Algebra-triage blob SHA-1: `ef303080eda2ed8134d2fc84ab3735be5425e735`; SHA-256: `d0ecbc688e8ff706c3c392a8cfcbb9cb6b3a51228c32c22420b7a6c0d7f1de66`.

The local checkout shows these triage paths as untracked and has no local path history. That observation is superseded for public-disclosure purposes by the exact remote files and path histories. An untracked local copy can still duplicate public remote work. Git timestamps are not by themselves proof of the instant at which access became public, so the precise claim is: the cited commit is publicly accessible now, and its recorded commit time precedes this audit. No assertion that this is the first disclosure anywhere is made.

## Attribution and earliest upstream version evidence

The pivotal source is OpenAI, *A Torsion-Free Group Algebra That Is Not Directly Finite*, manuscript date October 4, 2026. Cite the manuscript-specific BibTeX in its README, retaining `author = {{OpenAI}}` and its supplied title and URL. Pin the source citation to [commit adc7f124](https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026), and separately mention the manuscript date.

The source's Theorem 1.1 asserts a finitely presented torsion-free group G, scalar elements a,b,c in F₂[G], `ab=1`, `ac=0`, `c≠0`, and a finite two-dimensional classifying complex. Proposition 2.1 gives the path-sum formulas and parity calculation. The substantial proposed construction, coefficient cancellation, root protection, random counting, planar extraction, asphericity, and torsion-freeness belong to OpenAI's source. The follow-on algebra does not constitute a separate solution of direct finiteness.

The remote GitHub repository API lists only initial commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, recorded at 2026-10-06T21:58:50Z (**October 6, 2026, 14:58:50 PDT**). The path-specific commit endpoint for the October 4 manuscript returns this same commit and no later correction at this audit. The current repository is public; its metadata gives creation at 2026-10-06T21:47:02Z. The public events endpoint did not supply a release event, and no releases or tags were listed. Therefore **October 4 is a manuscript date, not an established public-release date**. The pinned initial commit is the earliest available repository version found; this does not exclude prior disclosure elsewhere. The exact remote API responses and response headers are saved.

## Exact conjecture and classical mechanism

The contradicted positive-characteristic specialization, if the October 4 input is valid, is:

> For every torsion-free group H, every field K of characteristic 2, and every scalar x∈K[H], the identity x²=x implies x=0 or x=1.

An existential counterexample over F₂ refutes that universally quantified statement. The stronger consequence that the same group and same element work over **every** characteristic-two field follows from the injective coefficient inclusion F₂[H]→K[H], because distinct group elements remain basis vectors and 0 and 1 remain distinct. It does not assert counterexamples in all positive characteristics.

Öinert's [arXiv:1904.04847v3](https://arxiv.org/abs/1904.04847v3), first submitted April 9, 2019 and revised July 20, 2023, records the three classical unit/zero-divisor/idempotent problems for arbitrary fields and torsion-free groups. Its Problem 1 explicitly includes positive characteristic. The requested paper does not use the characteristic-zero-only or analytic Kadison–Kaplansky formulation. The independent historical audit in `CLASSICAL_PROVENANCE_AUDIT.md` records exact full-text statements and citation chains.

The implication “only trivial scalar idempotents ⇒ direct finiteness” is long established. A concrete pre-2026 primary exposition is Giles Gardam's [lecture source](https://github.com/gilesgardam/lectures/blob/main/kaplansky.tex), Proposition `proposition:kaplansky_relations`, whose proof observes `(βα)²=βα` when `αβ=1`. The lecture source explicitly places idempotents before direct finiteness in the usual hierarchy. Credit this as a documented classical reduction; do not suggest that Gardam invented the observation or that this effort discovered it. The calculation `e=1−ba` is its complementary-idempotent form.

Similarly, direct finiteness of a unital ring is equivalent to the regular right module not being isomorphic to itself plus a nonzero summand. Ara, Goodearl, O'Meara, and Pardo, *Separative cancellation for projective modules over exchange rings* (1996 report), p. 9, explicitly state the regular-module equivalence and distinguish stable finiteness. The specific cyclic projective summand eR and `[eR]=0` are elementary module and Grothendieck-group calculations, not a newly invented K-theory method. Weibel, *The K-book*, Chapter II, §§1–2, supplies the standard group-completion definition. General cancellation for all finitely generated projectives is a stronger property than direct finiteness; the present target gives a concrete failure of that cancellation by an absorbed summand of R. The statement `[P]=0` does not imply `P=0` and is not a nonzero K₀ class. Augmentation also ensures K₀(F₂[G]) itself contains a split copy of ℤ; its entire group is not claimed to vanish. The exact references and independently checked passages are retained in the companion classical audit.

## Companion audit and scope distinctions

The relevant companion files were copied from the pinned read-only upstream clone into `sources/priority_companions/`; the source/copy SHA-256 manifest is stored there. Exact main statements and relevant proof/disclosure sections were inspected, and the source text was searched for the target and equivalent formulas.

| Source | Precise relevant disclosure | Relation to this target |
| --- | --- | --- |
| October 4 torsion-free direct-finiteness paper | F₂, finitely presented torsion-free G, scalar `ab=1`, `ac=0`, `c≠0`; finite 2-dimensional classifying complex | Pivotal unreviewed input. No idempotent/projective/K₀ corollary is stated in the inspected source. “Projective” and “K_0” search hits concern a projective plane and a path-count parameter, respectively. |
| September 23 characteristic-two direct-finiteness paper | Finite field K of characteristic 2, finitely presented group containing an element of odd prime order; scalar one-sided inverse; terminating prescription unexecuted | Does not provide a torsion-free input or guarantee K=F₂. It already gives the cellular-automaton consequence. |
| September 23 group-ring determinant companion | Starts from that torsion-containing characteristic-two input; coefficient restriction yields `XY=I_d`, `C=I_d−YX≠0`, `C²=C`, `XC=0`, `CY=0` | Explicitly already uses the defect-idempotent mechanism, but over a matrix algebra and a group without a torsion-free assertion. It does not duplicate the exact scalar torsion-free target by itself. |
| September 26 odd-characteristic direct-finiteness paper | One specified odd prime p, field order p⁴, finitely generated group containing torsion, scalar one-sided inverse | Does not justify an odd-characteristic torsion-free idempotent conclusion. |
| September 23 torsion-free zero-divisor paper (family 196) | F₂, finitely presented torsion-free group with finite 2-dimensional classifying space and nonzero αβ=0 | Supplies the graph/cone parity and arrangement mechanism developed by October 4. Zero divisors alone do not imply nontrivial idempotents. |
| September 24 Bass trace/idempotent paper (family 207) | Scalar Kaplansky idempotent conclusion over commutative characteristic-zero domains; complex/integral trace conclusions | Different characteristic. It cannot be used to extend the present scalar example to characteristic zero. |
| October 5 ℓ¹ Bass companion (family 207) | Hattori–Stallings support theorem for idempotent matrices in complex ℓ¹(G) | Different algebra and characteristic; not an F₂ consequence. |
| September 23 Kadison–Kaplansky projection paper | A nontrivial scalar projection in a reduced complex group C*-algebra of a torsion-free group | Analytic projection problem, not the scalar F₂ group algebra problem; its independent claims were not adopted as dependencies here. |

The family 197 Lean scope document lists the September 23 characteristic-two example, determinant example, and specified odd-characteristic example. It expressly describes a detailed characteristic-two group **with odd prime torsion**. Its heading does not formalize the October 4 torsion-free construction. No full formalization of the present follow-on has been established by this priority audit. Source validation and any actual Lean verification must be reported separately.

## What has and has not been established

1. A strict affirmative public-duplication witness has been established for the specified immediate consequence and proof outline in the user's own earlier public triage.
2. The established general algebraic reduction is independently documented in a pre-2026 primary source; OpenAI's own determinant companion also uses its matrix form.
3. The supplied source attribution is OpenAI. The source's manuscript date and available public version history are distinguished.
4. The exact torsion-free scalar target is not stated in the inspected upstream companion files. This bounded observation is **not proof of novelty**, and it does not override the affirmative user-repository disclosure.
5. The difficult upstream construction is not validated by this audit. Its strongest unconditional contribution here remains the self-contained algebraic theorem for any unital ring with `ab=1≠ba`. An unconditional torsion-free group result additionally requires the separate source checks to pass.
6. No numerical finite presentation, coefficients, executed multiplication certificate, characteristic-zero/odd-characteristic conclusion, reduced C*-algebra conclusion, nonzero K₀ class, or “first” priority assertion is licensed by this audit.

The full query/version ledger is in `priority_evidence/SEARCH_LOG.md`. No external individuals were contacted and no upstream files, git refs, commits, or releases were modified.
