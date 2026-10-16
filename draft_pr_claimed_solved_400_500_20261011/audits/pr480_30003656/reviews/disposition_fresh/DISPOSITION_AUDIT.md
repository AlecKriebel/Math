# Fresh complete-disposition adversarial audit: PR480 / problem 30003656

Checkpoint: 2026-10-11 20:57 America/Los_Angeles (2026-10-12 03:57 UTC).
Frozen candidate: `cd9025795f40bd9ebc2b32de50917d73ca0f2bfa`.
Reviewer scope: adjudicate the exact mathematical, source, priority, and
publication claims; no new proof search or substitute problem. No Git, index,
QUEUE, PR, DOI, tracker, or frozen-source mutation was performed.

## Recommended disposition

**Accept mathematical validity; fail the requested new-open-problem publication
framing. A qualified correction of the selected problem's status to
`already_solved`, followed immediately by skipping the PR under the user's
exact-status filter, is justified under the user's stated definition of that
status. Do not prepare a resolution paper, upload to Zenodo, append a publication
row, merge, close, or comment on that PR after the correction.**

The classification is a prior-result/priority issue for the literal target,
not evidence that someone previously printed this exact one-constant sentence
or explicitly announced this algebraic specialization as the answer. The
finding must make that distinction visible. Suggested Findings language:

> The literal algebraic redundancy question has a credited routine
> prior-method negative resolution: published generic-model calculations and
> geometric classical-conservativity already supply an algebraic
> excluded-middle counterexample. The PR's exact one-constant alpha is valid
> and is also a routine specialization of BBC Theorem 5.11 and Example 6.2.
> Earlier explicit printing of that alpha, or explicit prior recognition of
> the algebraic specialization as a resolution, was not established. No new
> discovery or first-priority claim is accepted.

This is a recommendation, not a mutation authorization to this reviewer. The
root must check the exact current selected row before any scope/status update.

## 1. What was independently checked

I read the frozen `PROOF.md`, `SOURCE_GATE.md`, and `README.md`; the root
`EXACT_CLAIM.md` and mathematical reconstruction; the completed categorical,
syntactic, and reproduction verdicts; and the reproduction hardening addendum.
I read the historical-priority report and independently inspected its relevant
primary-source passages: BBC v1 Theorem 5.11, constructor axioms, Example 6.2,
and Section 7; OWR 53/2017's final algebraic question; Wraith's geometric
conservativity statement; the dated Blechschmidt introduction; and the full
2019 published paper's Section 6.1. The second final priority report was not
yet present at the initial checkpoint; its primary full text was independently
available and read. A final addendum will record reading that completed report.

This audit does not blindly repeat a verdict of mathematical failure. None was
found. The original alpha is the exact original-language sentence

    beta = forall x notnot(x=c),       alpha = not beta,

for the theory of a pointed object with one constant and no nonlogical axioms.
The source's displayed algebraic question is universal over purely equational
theories. A single such theory is enough to refute it; the source has no stated
exclusion of classical tautologies or stable/base-change requirement.

## 2. Mathematical result passes, but that is only one acceptance gate

The all-pointed-map category supplies a collapse to the singleton at every
stage, giving double-negated equality to c for every successor element. Its
generic pointed object therefore validates beta and not alpha. The injection
category always permits a fresh nonpoint whose inequality persists, so every
stage and every successor fails beta; its canonical pointed object validates
alpha. In particular the singleton stage validates alpha by its future stages,
without having a current witness for exists x not(x=c).

Restriction keeps all stage sets and all geometric interpretations, including
equality, images, and arbitrary small joins. It conservatively reflects sequent
validity. The finite-equality quotient argument independently supplies the
same completeness result. I found no attack defeating any of these mechanisms;
the categorical and syntactic reviews check precisely the relevant boundaries.

The finite code findings are also appropriately limited. Normal reproduction
and independent finite controls pass. The removable-assertion false-PASS issue
has a repaired derived checker with successful normal/optimized output equality
and actual rejected equality/forcing mutations. This is a sound finite support
package, not a machine proof of the unbounded theorem. The repair is not a
novelty repair and cannot answer the priority gate.

Thus a closure explanation asserting invalid mathematics, inconsistency,
failure of geometric redundancy, or failure to match the literal signature
would be false. The strongest accepted mathematical outcome remains a valid
counterexample to the displayed universal assertion.

## 3. Checkable overlap with prior results

The exact candidate requires no new completeness principle beyond
[BBC v1](https://arxiv.org/pdf/1712.07743v1), Theorem 5.11 and Example 6.2:

1. With only the nullary symbol c, constructor-disjointness has no pair of
   distinct symbols, constructor-injectivity has an empty conclusion, and the
   proper-cycle scheme has no positive-arity symbol. Accordingly T+ adds no
   nontrivial axiom to logical equality in this signature.
2. Terms are variables or c. Term substitutions give all pointed maps; injective
   renamings give all pointed injections; the empty theory has trivial topology.
   These are the candidate's exact sites, after the stated variance reversal.
3. BBC Example 6.2 explicitly exhibits the universal double-negated equality
   mechanism for two constants and its negation in the renaming/substitution
   comparison. Reducing the constants to c is a direct specialization of that
   calculation; the candidate's fresh-element/collapse steps are the same
   mechanism.
4. Theorem 5.11 already says that geometric sentences with equality valid in a
   canonical forcing model are derivable from T+. Here this is T itself. This
   yields exactly the candidate's redundancy conclusion.

This reconstruction is our present deduction from published statements. It is
not a claim that BBC explicitly printed the candidate alpha. The source itself
calls the algebraic refinement open at its conclusion, so attributing an
explicitly recognized 2017 answer to those authors would overstate the record.
Conversely, the final open-question wording cannot make the overlapping
machinery cease to imply the displayed negative instance.

## 4. A stronger reason the literal target is not a fresh open resolution

The distinction between exact-formula priority and target priority matters.
The target asks whether *all* redundant sentences hold for *every* algebraic
theory. It does not additionally require a nonclassically-valid witness.
Consequently an older classical-tautology mechanism is enough for the target,
even though it does not give the PR's exact alpha.

There is a particularly short check using already stated primary-source facts.
Let S be the empty equational theory with two constants 0 and 1, and put

    delta = (0=1) or not(0=1).

S is algebraic. BBC Example 6.2 identifies the genuine generic S-model in the
presheaf topos on finite bipointed sets and explicitly gives notnot(0=1)
there. At the finite stage with distinct distinguished points, 0=1 is false.
Its collapse to a stage identifying the points prevents not(0=1). The trivial
topology evaluates disjunction at the stage itself. Therefore delta fails in
that generic model.

Delta is classically valid. If S+delta proves a geometric sequent sigma
intuitionistically, S proves sigma classically by eliminating the tautology.
Wraith's published geometric conservativity statement then yields an
intuitionistic derivation from S. It includes logical equality and arbitrary
disjunctions in its definition of geometric sentences. Hence delta is
S-redundant in exactly the literal target's consequence fragment.

This argument uses [Wraith, ICM 1978 proceedings, p. 332](https://www.mathunion.org/fileadmin/ICM/Proceedings/ICM1978.1/ICM1978.1.ocr.pdf)
and BBC Example 6.2. Moreover, the
[dated 2019 Blechschmidt introduction](https://github.com/iblech/internal-methods/blob/cc39bd8b06aecbe2ecd08a86344a5bcc1b7ed596/paper-qcoh.tex)
expressly records that any excluded-middle instance in the theory's signature
is redundant and commonly fails in the generic model. It does not limit that
general principle to relational theories. The algebraic specialization above
is a direct application of the stated principle to the generic calculation
already printed by BBC.

The 2019 Bezem-Coquand paper, Section 6.1, independently records classical
provability as a known source of redundancy, propositional excluded middle as
a negative answer, and another negative example using a binary relation. It
does not explicitly give this purely equational alpha. The exact-formula
documentary gap therefore remains, but it does not restore the original
literal yes/no target to a problem needing a new mathematical mechanism.

This is priority comparison within the existing target, not a new problem or a
new proof-search route. It does not impose an invented strengthened restriction
excluding delta.

## 5. Why an accurate credited note does not cure this goal's framing

A mathematically sound short note could say:

* the literal algebraic assertion stated in 2017 is false;
* its negative answer follows from already available results;
* the exact nonclassically-valid witness is an explicit one-constant
  specialization, with a self-contained proof and finite reproducibility checks;
* no first-priority or new-theorem claim is made.

That is a coherent credited observation. Its proof can be fully sound, and an
overlooked simple corollary can sometimes warrant publication. The present
audit does not declare such a note unpublishable in every setting.

But the user's specific process requests a preprint framed around decisively
solving the original *unsolved* open problem, followed by publication of the
accepted result. The user also defines `already_solved` as a problem that was
not actually open, with a priority-audit issue. Here the literal target already
has the direct prior-principle refutation above. Calling the new package a
solution of a still-unsolved problem would conceal this, even if a later
sentence disclaimed first priority. Calling it a credited reconstruction would
correct the concealment but change the kind of contribution being released.

Requiring that alpha not be classically valid would not repair that mismatch.
It adds a property absent from the original assertion, and the exact witness
with that property is itself the prior-Theorem-5.11 specialization. Likewise
unstated stability or metatheory restrictions must not be invented to create a
new target. No new proof search for a replacement result is warranted here.

AI-use disclosure and an explicit unrefereed status are necessary for any
future publication but do not establish originality or continuing openness.
An exact tracker/Zenodo metadata match cannot cure a false contribution claim.

## 6. Adversarial counterarguments to the proposed status correction

**A simple corollary can be a new discovery.** Correct. Merely showing that a
claim follows from old machinery is insufficient to establish an earlier
historical discovery; all theorems ultimately follow from earlier principles.
This is why the findings must not assert earlier printing or recognition of
alpha. Here the target already falls to a specifically documented general
counterexample principle plus published generic-model truth calculations,
not an arbitrary long derivation in a prior theory. Under the user's broader
priority-issue meaning of `already_solved`, that suffices for the conservative
classification. It does not settle whether the explicit observation merits
credit of its own.

**BBC explicitly left the algebraic case open.** Correct. That is strong
documentary evidence of the question as stated in 2017. It is not evidence that
the literal sentence quantified over all algebraic theories survives direct
instantiation of published excluded-middle principles. The report must retain
the apparent discrepancy rather than manufacture an intended stronger question.

**No prior exact algebraic counterexample was located.** Correct. This defeats
an unqualified assertion of explicit historical priority. It does not defeat
the derivation in Section 4 or warrant an assertion that the target remained
mathematically open through the present date.

**The candidate alpha is not classically valid.** Correct and valuable. It
distinguishes the witness from excluded-middle examples. The distinction does
not change the original universal target and does not defeat the independent
exact prior-machinery specialization in Section 3.

**Changing status might silently dodge the required close-or-publish outcome.**
This would be a legitimate concern if the update hid an unresolved mathematical
gap or arbitrarily removed an inconvenient eligible PR. The update proposed
here records a concrete independently checkable priority failure in the user's
own status vocabulary, preserves the valid result and evidence, and then
obeys the explicit instruction to skip all non-`claimed_solved` rows. It is a
scope-preserving correction of the outcome, not a substitute research program.

**Should the PR instead be closed as beyond repair?** A mathematical-invalidity
closure would be wrong, and a claim of definitive earlier recognized priority
would go beyond the evidence. After the qualified status correction the PR is
out of scope and the user expressly forbids closing or commenting on it.
Accordingly closure would be premature and incompatible with that filter.

## 7. Concrete next step and remaining limits

The root should reconcile the two completed independent priority reports,
check that they agree on the prior-principle instantiation, and make only the
exact selected status/findings correction plus audit evidence. Then mark the
audit outcome `mathematically_valid_prior_method_priority_mismatch` and skip
this PR. No manuscript or final-package review loop has yet occurred, so there
is no preprint-ready package to upload or merge.

Do not erase the verified theorem, repaired checker, or audit history. Do not
claim the exact alpha was printed before this project. The remaining scholarly
gap is explicit earlier recognition of that alpha or of the algebraic
specialization, and any precisely stated intended strengthening. That gap could
matter to a separately authorized credited-observation project; it does not
justify automatic publication as the new resolution requested here. External
input might clarify intended scope, but independent-research policy prohibits
contacting anyone or preparing outreach.

## Final report cross-check

2026-10-11 20:59 PDT (2026-10-12 03:59 UTC): the completed second report,
`reviews/priority_2019/PRIORITY_REVIEW.md`, is now available and has been read.
It independently reaches the same critical distinction: no explicit exact
alpha or explicitly announced purely equational resolution found in the checked
full texts; literal algebraic negative answer is a routine prior-principle
corollary; first/new-resolution framing fails. Its independent one-constant
excluded-middle specialization and this report's two-constant specialization
agree on the exact consequence fragment and target class. Its full published
2019 source distinguishes the relational Skolem example from the candidate.
No discrepancy requires a mathematical or historical change to this verdict.

Final disposition-audit completion estimate: **100%**. Estimate toward PR480's
operational disposition: **60%**, because the root's reviewed status correction
and scope-stop still remain. These are work-completion judgments, not
mathematical probabilities.
