# Bounded priority and theorem-scope review

Problem 30001739. Review completed 9 October 2026 UTC.

## Result

**No exact predecessor, translated/twisted-equivalent predecessor, or contradictory established theorem was verified in this bounded review. Priority remains unestablished.** This is not a novelty guarantee, an exhaustive literature search, or a new proof/audit turn. Mathematical proof acceptance is a separate determination.

The target of comparison is the degree-15 Langlands quotient with five segments

[4,6], [2,5], [3,3], [1,4], [0,2]

on the trivial character line over the unramified quadratic extension of Q_3, with arithmetic Galois invariance, noninducedness, and zero multiplicity for both Hermitian forms. This review did not modify that proof or attempt a new proof route.

## Important unresolved related work: Luo–Zha

Caihua Luo and Junwei Zha's *A Remark on Bernstein–Zelevinsky Classification for General Linear Groups* was published online in *Frontiers of Mathematics* on **5 July 2026**. The official abstract reports a counterexample to a Lapid–Mínguez conjecture about generating the maximal submodule of a standard module from smaller standard submodules. Its references identify *On a determinantal formula of Tadić*. The full article's statements, example and proof were not accessible in this review; the publisher provides a subscription preview. [Official record](https://link.springer.com/article/10.1007/s11464-025-0256-0)

A stronger historical locator was verified: Junwei Zha announced the kernel result at the **13 May 2025** CUHK(SZ)–HKU Representation Theory Workshop II. PDF p.1 supplies the date and talk slot; p.4 contains the full abstract. It supplies no explicit multisegment and no unitary-period multiplicity. The search engine's age label was unreliable; the date above is read from the actual program. [Dated program and abstract](https://hkumath.hku.hk/MathWWW/event/2025/Workshop_Program.pdf)

The author's research page links a legacy Google viewer which did not supply readable full text in the earlier pass. Its publicly embedded Drive folder returned HTTP 401 during this review and was not retried. No login, purchase, author contact, or restricted-content route was used. **Do not call the Luo–Zha paper either an exact predecessor or unrelated:** the necessary full-text comparison remains unresolved. In particular, a kernel-generation counterexample does not by itself prove the present unitary-period vanishing.

## Which conjectures and theorems are actually in scope?

FLO Conjecture 6.12 (published p.246) predicts distinction from Galois invariance and a τ-Witt-index inequality. The index is defined from Langlands data on pp.214–215. For the five individually invariant factors here that definition gives index zero. Thus the asserted vanishing also contradicts this conjecture, once the mathematical counterexample is accepted. This is a direct scope comparison, not a second proof. FLO Theorem 13.11 and Corollary 13.12 (pp.292–294) cover proper ladders and irreducible products of ladders, including the unitarizable case. [FLO published paper](https://doi.org/10.1007/s10240-012-0040-z)

The displayed candidate has strict containments, so it is not a ladder multisegment. Assuming its separately established noninducedness, it cannot be a nontrivial irreducible product of ladders either. Uniform twists do not remove these containments or create a proper induced realization. The unitarizable theorem therefore cannot be invoked merely because the symmetric subgroup is called unitary. Likewise, an unramified field extension or character line is not the spherical-representation hypothesis in FLO Lemma 6.14.

Lapid's OWR 2011 §5.3, p.734 gives the noninduced definition and Conjecture 4, whose k=1 total is two. The same page explicitly distinguishes general noninduced representations from ladders. Its preceding kernel-generation question is relevant context, but the present argument only needs containment of selected rank-one kernels, not generation of the entire kernel. [OWR report](https://doi.org/10.4171/owr/2011/14)

Beuzart-Plessis's Theorem 5.2.2, p.35 of arXiv:2008.05036v2, explicitly assumes generic irreducibility. The 2025 survey repeats this restriction in Theorem 3.22 and Remark 3.23, pp.66–67. Neither computes this nongeneric quotient's multiplicity. The survey's counterexample on p.67 concerns a different SL_2 setting and a general relative-parameter formula; it is not this example. [Generic multiplicity paper](https://arxiv.org/abs/2008.05036v2), [survey v1](https://arxiv.org/abs/2509.18062v1)

Lu–Matringe's §5, pp.25–27 of arXiv:2503.11988v2, explicitly starts from square-integrable inducing data and cites the understood generic/tempered multiplicities. Its completeness statement does not establish the general noninduced-product assertion. The arXiv record remains v2, revised 10 April 2026; the final publisher body was not inspected. [Inspected preprint](https://arxiv.org/abs/2503.11988v2)

Gurevich's *On a local conjecture of Jacquet, ladder representations and standard modules*, arXiv:1411.2420v2, pp.1–3, instead studies GL_n(F) inside GL_n(E), with conjugate-duality. Its introductory counterexample and ladder theorem concern that different subgroup and are not a unitary-period predecessor. [Preprint](https://arxiv.org/abs/1411.2420v2)

## Exact examples checked against the candidate

The accompanying comparison ledger normalizes common endpoint translations and reflected translations, and records segment counts, lengths and total degrees. It compares actual displayed multisegments rather than title or abstract similarities.

- OWR p.734: [1,2], [-1,1], [0,0]. This nonladder, noninduced example has three segments and character-line degree 6, not five and 15. No zero unitary multiplicity is stated there.
- Droschl, arXiv:2508.13817v2, p.18: the Leclerc example [4,5], [2,4], [3,3], [1,2] has four segments and degree 8. Theorem 4.3 and its proof on p.16 concern intertwiner pole orders. Both the older September 2025 author PDF and current v2 were inspected; neither displayed example is a match. [Current v2](https://arxiv.org/abs/2508.13817v2)
- Atobe–Kondo–Yasuda, *Local newforms for the general linear groups over a non-archimedean local field*, §2.5, pp.10–11: [5,6], [3,7], [3,4], [2,5], [3,3], [1,2], [0,0]. This seven-segment degree-17 newform example is another numerical search near-hit, not a match. [Published paper](https://doi.org/10.1017/fmp.2022.17)

Uniform character twists preserve the number and lengths of segments, excluding these displayed examples as twist-equivalent predecessors. This does not exclude different examples elsewhere in those papers or the wider literature by automated means.

## Search boundary and use of this result

Fifty exact web queries covered the candidate's endpoint fragments, the centered shift [-3,-1], [-2,1], [0,0], [-1,2], [1,3], a positive shift, GL_15, five segments, odd cycles/pentagons, nonladder/noninduced terminology, and the named conjectures and recent papers. All query strings are retained in `SEARCH_LEDGER.json`.

Only returned indexed results and the specified primary passages were inspected. Mathematical notation indexes poorly. There was no comprehensive citation-graph crawl, subscription database search, non-English survey, or author inquiry. Selected full statements and relevant proof passages were read; this is not an independent audit of every source proof. Inherited denied Seville, Beuzart-Plessis publisher and Lu–Matringe publisher routes were not retried.

Safe conclusion: **a bounded search found no verified exact prior occurrence, but authorship priority is not established, and the Luo–Zha full-text comparison remains open.** Do not describe the result as the first counterexample on this evidence alone.
