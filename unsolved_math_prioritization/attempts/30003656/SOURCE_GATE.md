# Source, scope, and prior-work gate

Checked 2026-10-03. Problem **30003656 / OWR-15958-003**.

## Retrieval and identity

The required starting URL was [UnsolvedMath 30003656](https://www.unsolvedmath.com/problems/30003656). A direct request returned HTTP 403; the web tool could not access it. A pinned catalogue record was therefore used only to recover the source identity. Its dated open-status assessment is not treated as proof. No matching prior report was found under the problem code in the pinned research-results index.

The independently retrieved original source is Ulrik Buchholtz's contribution, *Syntactic Forcing Models for Coherent Logic*, in [Oberwolfach Report 53/2017](https://doi.org/10.4171/owr/2017/53), internal pp. 14–16. The final paragraph asks whether restricting to algebraic theories restores a positive answer. The definitions and surrounding discussion explicitly concern absence of new geometric consequences, not redundancy of equational axioms or term operations.

The primary preprint [Bezem–Buchholtz–Coquand, arXiv:1712.07743](https://arxiv.org/abs/1712.07743) was read in full for the relevant sections: abstract/introduction, forcing and signature conventions, Theorem 5.11 and its following observation, Examples 6.1–6.2, and Section 7. The paper defines algebraic as purely equational in its final question. It presents definitions for one sort and says that many-sorted details are omitted. Our one-sorted, one-constant theory is therefore within the explicitly described algebraic class.

## Source dependencies

1. **Buchholtz, OWR 53/2017**, internal pp. 14–16. [Institutional report copy](https://oa.tib.eu/renate/server/api/core/bitstreams/f754efe0-f461-4dc6-8e01-be4de222b790/content). Supplies the exact target and its context.
2. **Bezem–Buchholtz–Coquand (2018)**, *Syntactic forcing models for coherent logic*, Indagationes Mathematicae 29, 1441–1464, [DOI](https://doi.org/10.1016/j.indag.2018.06.004), [primary preprint](https://arxiv.org/abs/1712.07743). Supplies the explicit definition of redundancy, Kripke–Joyal conventions, and Theorem 5.11. The current proof includes a self-contained geometric-completeness argument and is not merely an appeal to the theorem.
3. **Ingo Blechschmidt**, *A general Nullstellensatz for generalized spaces*, author-hosted rough draft, Introduction following Wraith's question. [Author source](https://github.com/iblech/internal-methods/blob/master/paper-qcoh.tex); [author-hosted PDF](https://rawgit.quasicoherent.io/iblech/internal-methods/master/paper-qcoh.pdf). Explicitly observes that the bare question has excluded-middle counterexamples and mentions care needed to rule them out. The draft does not specify a strengthened redundancy condition in that paragraph.
4. **Bezem–Coquand (2019)**, *Skolem's Theorem in Coherent Logic*, Fundamenta Informaticae 170(1–3), 1–14, [DOI](https://doi.org/10.3233/FI-2019-1853). The publisher abstract was checked and advertises another negative answer to Wraith's question. The full text was not obtained in this investigation, so its precise relation to the algebraic refinement and the present formula is **not verified**. Some publisher search metadata mixes the special-issue editors into the author list; the named authors are Marc Bezem and Thierry Coquand.

Local source copies are retained only as private research evidence. This public package contains authored analysis, short bibliographic references, and exact-check code; no source PDF, full source text, corpus, or unrelated private material is included.

## Bounded current-literature and duplicate check

Searches included the exact problem title/code, the exact 2018 and 2019 paper titles, and combinations of Wraith, algebraic, redundant, generic model, equality, and excluded middle. Primary evidence located the OWR question, the 2018 paper's algebraic open question, Blechschmidt's scope warning, and the 2019 follow-up abstract. No searched primary source explicitly asserted a later resolution of the algebraic restriction. This negative search result is not proof that none exists.

On repository `AlecKriebel/Math`, live `main` showed rank 506 as queued at 0/5. Exact checks found no Wraith-related issue, no issue matching pointed/redundant, no `attempts/30003656` directory in the live attempts tree, and no related-target-group entry for this problem. The root directory listing had no named Wraith/pointed/coherent effort. The pinned catalogue contained only this target with the Wraith/redundant-sentence description. Nearby completed local public packages did not contain such a target. The repository-wide recursive-tree endpoint failed, so successful narrower listings were used; this is a bounded duplicate screen, not a claim of exhaustive semantic identity search through every historical file.

## Exact theorem and publication caveat

The candidate theorem uses the exact explicit definition:

    For every geometric sequent σ, T+α ⊢ σ implies T ⊢ σ.

Here T is the purely equational theory of pointed objects and α=¬∀x¬¬(x=c). The generic model forces ¬α. In particular the result does not hinge on a classically valid α: the singleton pointed model refutes α in Set.

The displayed source statement imposes no restriction that excludes α and no extra stable/base-change version of redundancy. Nevertheless, the surprising simplicity and the source's open-question wording require an independent scope audit. A stronger, precisely stated intended question would be a separate target. This package neither invents such a condition nor claims to have settled every possible refinement.

**Permissible author-stage label:** candidate negative resolution of the literal displayed definition; independent mathematical/scope audit pending; historical priority unresolved.

**Impermissible labels at this stage:** verified solved, first resolution, new theorem of established novelty, or resolution of an unstated strengthened problem.
