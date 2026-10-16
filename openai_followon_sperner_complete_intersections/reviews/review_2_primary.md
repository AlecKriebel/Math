# Fresh review 2: primary theorem, scope, priority and attribution

Reviewer: independent primary-source child of fresh complete-package reviewer 2.
Review completed: 2026-10-07 05:39 UTC (2026-10-06, America/Los_Angeles).
Scoped audit completion estimate: 100%. This is not an estimate or certification of the central upstream proof's correctness or of the full publication package.

## Independence and exact reviewed candidate

I read `/Users/alec/Documents/Math/AGENTS.md`, this project's `PROJECT_BRIEF.txt`, the complete `manuscript/main.tex`, `publication/README.md`, and `zenodo-deposit.json`. I did not read existing project reviews, research notes, dependency audits, verdicts or priority conclusions. I made no source, payload, publication, tracker or Git changes. Downloads and scratch are confined to `reviews/review_2_scratch/primary_child/`; this report is the requested review output.

SHA-256 of candidate files:

| File | SHA-256 |
|---|---|
| manuscript/main.tex | `86a9fadc467764915dfb418a3898d01021b801af67b6c710291f2cdb48db865d` |
| publication/README.md | `a39dfcc8eb2e8f78df83dd0e136ddbbc329a2633cef96eac6d1f8e0d42cfd4fd` |
| zenodo-deposit.json | `497c2a0a2e8a0468ebb4b400867768dac144dedbc255ff0ff6a757355a4b37cf` |

## Original HWW result and exact needed hypothesis

I inspected the [arXiv record](https://arxiv.org/abs/1601.06928v1), [primary full text](https://arxiv.org/html/1601.06928), and [v1 PDF](https://arxiv.org/pdf/1601.06928v1), especially Definition 2, Propositions 7–8, Sublemma 9, Conjecture 10 and Theorem 11. HWW's field convention permits arbitrary fields, including finite ones. Definition 2 uses all ideals. Proposition 8 expressly invokes Watanabe's Lemma 2.4 to restrict the maximizing ideal to a graded ideal. Theorem 11 conditions the complete intersection's Sperner property on EGH for that complete intersection. There is no additional field-extension, algebraic-closure, or characteristic-zero premise in that implication.

The required EGH input is full-length homogeneous Hilbert-function matching: every homogeneous polynomial ideal containing the defining regular sequence must have a pure-power-containing counterpart with matching degree dimensions. Equality of ideal Hilbert functions and equality of quotient Hilbert functions are equivalent in the fixed ambient polynomial ring. No equality of minimal-generator counts is assumed. The candidate's lines 63–95 state and attribute this correctly.

Public chronology is January 26, 2016 for arXiv v1, and 2017 for the cited journal article. The downloaded v1 PDF displays an automatically generated September 19, 2018 date; that is not evidence of a later first disclosure. The manuscript's citation uses the arXiv submission year, appropriately. The AMS journal PDF request returned HTTP 403. The original Watanabe DOI resolves to Project Euclid, whose security page prevented reading the original chapter; its exact Lemma 2.4 was therefore checked through HWW's explicit primary citation, not independently from the 1987 full text.

## Family 200 primary scope and supplied attribution

I downloaded the pinned primary PDFs and manuscript-specific READMEs directly from `openai/math` at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`:

- [Commuting Division-Coefficient Forms and the Artinian Eisenbud–Green–Harris Conjecture](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/paper.pdf): pp. 3–4, Theorem 1.1, Corollaries 1.2–1.3, and §9.1 on p. 39 were read closely. SHA-256: `20fba09b5fed0f63cb54b9f4bc750627ac834a2ef73fcd8d41a2ea83cac56069`.
- [The Artinian Lex-Plus-Powers Betti Theorem](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/paper.pdf): pp. 1–3, especially Theorem 1.1 and Corollary 1.2. SHA-256: `81874e1994ff2773543f714989feac78650ddc902f7f36047c6ce8d3288a9c05`.

The EGH construction assumes a full sequence over C, positive variable count, and ordered degrees at least two. Its Hilbert consequence supplies one monomial ideal for the entire Hilbert function, with no bound on extra generators of the original containing ideal. Corollary 1.3 covers arbitrary characteristic-zero fields and arbitrary positive sequence length. The LPP companion states stronger Betti bounds. The note uses only the weaker full-length Hilbert consequence and independently explains coefficient-field descent. Its theorem numbers and scope agree with these primary statements.

The two [manuscript README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/Commuting-Division-Coefficient-Forms-and-the-Artinian-Eisenbud-Green-Harris-Conjecture-September-23-2026/README.md) [citation blocks](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-Artinian-Lex-Plus-Powers-Betti-Theorem-September-23-2026/README.md) supply the author OpenAI, the same titles, 2026, the same manuscript-specific citation labels and public PDF links. The candidate faithfully preserves these. Both manuscript headers and READMEs are dated September 23, 2026.

I also inspected the repository README, the family-200 entries of `CONTENTS.md` and `overview.tex`, the EGH build wrapper, and the formalization catalogue for the exact titles. The catalogue has no matching entry and `lean/docs/200.md` returns 404. This supports the candidate's absence of a formalization claim; it does not prove or disprove the unformalized theorem. I did not independently verify the full division-algebra/geometric proof in this scoped review.

## Scope attacks checked in the candidate

The field paragraph is valid for full-length EGH: a fixed ideal and sequence require only finitely many coefficients; faithful flatness descends regularity to the generated coefficient field, a finitely generated characteristic-zero field embeds into C, and a monomial ideal transfers by its exponent set. Degree dimensions are preserved under both field extensions. An arbitrary characteristic-zero field need not itself embed into C.

Degree-one reduction is also sufficient. The full regular sequence has height n, so its linear members cannot be dependent. Eliminating their independent linear span gives a polynomial ring in n-r variables. The remaining images form a homogeneous system of parameters and hence a regular sequence; their positive homogeneous degrees are preserved. The graded algebra isomorphism preserves every ideal and its generator count. If no variables remain, A=k and the maximum is 1, attained by A. No upstream degree-at-least-two theorem is applied to the empty sequence.

The nonhomogeneous-ideal step has the correct inequality direction. Let J be the lowest-degree initial ideal and G the intersection-associated grading of mI. Products give mJ contained in G, while finite grading preserves dimensions. Thus

`mu(I) = dim J - dim G <= dim J - dim(mJ) = mu(J)`.

The proof does not require equality of G and mJ. The field-extension generator paragraph correctly descends an upper bound for extensions of ideals over k; it does not attempt to descend arbitrary ideals over an extension field. The theorem, abstract, examples, README and deposit description keep characteristic zero, standard grading and Artinian complete intersections explicit. They make no unsupported Lefschetz, nongraded or positive-characteristic inference.

## Current public status and priority positioning

I read the [official collection announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/), dated October 6, 2026, and the [public repository README](https://github.com/openai/math). The September manuscript date and October public announcement are distinct facts. The candidate states that distinction and does not assert that September 23 was public disclosure.

A fresh remote-head query during this review returned `adc7f1241b42e322a6451854ab7e4b4c146bf78a` for `refs/heads/main`; GitHub's repository page showed one commit, and the pinned commit page identifies it as the initial commit. Hence the audited primary version remains the current official main version at this check. The repository warns that unformalized results may have issues and describes revision retention. The candidate accurately calls the input unrefereed and does not portray this review as conventional human refereeing.

Current searches included the exact upstream titles with correction/Sperner terms, and combinations of Sperner property, complete intersections, characteristic zero and 2025/2026. I used only the primary sources above as evidence. These searches did not expose a competing explicitly stated general unconditional Sperner result or an official revision, but failed searches cannot certify novelty or absence of every competing source. Text searches of the two primary PDFs and the official catalogue found no explicit Sperner corollary. That observation concerns explicit presentation, not logical availability.

The exact intellectual contribution remains an explanatory immediate corollary note: OpenAI supplies EGH; HWW supplies the previously known implication and all-ideal scope; the note supplies a self-contained account of established reductions, scope checks and examples. I found no independent new mechanism or genuinely broader theorem that should be credited to this author. The abstract, introduction, README and manifest already use that restrained positioning. They cannot support a claim of first proof, a new independent solution, or invention of the all-ideal reduction; they do not make such claims.

## Verdict

**No substantive primary-scope, attribution, or current-public-status defect found in the exact candidate files hashed above.** Their theorem matches the needed HWW implication, their upstream citation and scope agree with the original family-200 statements, and their date and novelty language is appropriately restrained. This verdict supports publication positioning as a consequence note, conditional on the separate complete-package review establishing the central upstream proof and final payload integrity. It does not certify the full upstream theorem, first priority, or conventional peer review.

No mandatory repair is requested by this scoped audit. The unread original Watanabe chapter and non-exhaustive priority search are explicit audit limits, not silently resolved facts.
