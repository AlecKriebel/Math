# Independent novelty and audience audit

Checkpoint: 2026-09-13, local project date. Completion estimate: 100% of this bounded literature/audience audit; this is not a percentage confidence in the theorem or a completed referee report.

Reviewed the Version 1.2.4 introduction, exact main theorem, references, examples, and scope section independently of previous project audits. The task was to challenge novelty and calibrate significance, not certify the entire proof. No external person was contacted and no outreach was drafted.

## Judgment

**Conditional impact: 7.7/10**, with a reasonable subjective range of 7.3–8.0 under the user's rubric, conditional on correctness, genuine novelty, and eventual publication. This is a strong significant specialist result: it removes a substantive boundary hypothesis from an established recurrence theorem, handles arbitrary species count, and potentially introduces a useful marked-potential method. I would reserve a firm 8+ for demonstrated wider methodological consequences or a substantially larger part of the general conjecture. The remaining single-linkage restriction, absence of quantitative convergence/tail bounds, and lack of a general stationary-law formula limit the present result's breadth. Author credentials, independent status, AI use, and the preprint host do not enter this conditional score.

**Novelty survives the searches conducted.** I found no public proof covering all finite, arbitrary-species, single-linkage bimolecular weakly reversible stochastic mass-action networks with unrestricted positive rates and no pure-species condition. This is a search result, not proof that no relevant unpublished or poorly indexed work exists. The closest active authors are unusually valuable as readers because a public two-species result remains without an accessible complete manuscript located in this search.

## Exact comparisons

| Result | Verified scope | Relation to this manuscript |
|---|---|---|
| Anderson–Cappelletti–Kim, Journal of Applied Probability 2020 | Binary, weakly reversible, one linkage class, plus a pure positive-multiple complex for each species; under binaryity this means the unary or double complex | The manuscript removes the final condition while keeping the others. This is the main novelty claim. [Author manuscript](https://people.math.wisc.edu/~dfanderson/papers/ACK2019.pdf); [institutional publication record](https://iris.polito.it/handle/11583/2857266) |
| Xu, arXiv:2409.05340v2 | Nonexplosion for bimolecular weakly reversible networks, including multiple linkage classes | Does not imply positive recurrence; §6 explicitly still describes bimolecular positive recurrence as unresolved. Its conclusion is broader in network graph scope but weaker in stochastic stability. [Primary manuscript](https://arxiv.org/html/2409.05340v2) |
| Agazzi–Anderson–Cappelletti–Laurence–Mattingly announced result | Project page says every weakly reversible network with two species is positive recurrent, independently of positive rate constants | Project page calls proof complete, gives a method sketch, and still lists manuscript as in preparation. Do not call the result merely speculation, but do not infer details beyond this public scope. Neither theorem contains the other as described: two-species arbitrary structure versus arbitrary-species single-linkage binary structure. [ConStRAINeD](https://constrained.polito.it/publications/) |
| Wiuf–Xu classification | Positive recurrence for weakly reversible systems with one-dimensional stoichiometric subspace | Does not cover arbitrary stoichiometric rank in the present theorem. “One dimension” must not be casually identified with one species. [Primary preprint](https://arxiv.org/abs/2012.07954) |
| Paulevé–Craciun–Koeppl 2014 | Weak reversibility implies symmetric discrete reachability, Lemmas 4.5–4.6 | The closure/communication lemma is established background, not an independent new recurrence contribution. The manuscript appropriately acknowledges this. Their combinatorial recurrence is weaker than stochastic positive recurrence. [Published author PDF](https://people.math.wisc.edu/~craciun/PAPERS_NEW/Pauleve_Craciun_Koeppl_JMB_2014_FINAL.pdf) |

The Xu page identifies v2 as 9 May 2026, while its rendered document has an August 24, 2026 date. Cite the explicit arXiv version and inspect the PDF metadata when updating the bibliography; the May version label is verified. Its mathematical distinction remains clear. The ConStRAINeD status was checked anew for this audit, rather than relying on the manuscript's August 22 access date. A [2023 public Cappelletti talk](https://staff.polito.it/daniele.cappelletti/past_events/23informs/) also explicitly announces two-dimensional positive recurrence. Exact-title searches found announcements, not a complete public manuscript.

## Presentation improvement with mathematical content

The introductory cycle `0 → A+B → B → 0` is a good delayed-drift example, but it has three complexes, one linkage class, and stoichiometric rank two, hence deficiency zero. Its recurrence is already covered by established complex-balanced theory. The other worked example is explicitly an ACK example and contains A, 2B, and C, so also does not demonstrate coverage beyond ACK's pure-species condition. This does not invalidate either pedagogical example or the theorem. It leaves an avoidable gap in explaining why the theorem covers new networks.

A compact additional illustration is the directed cycle

`0 → A+B → B+C → C → B → 0`.

Give its first arrow rate constant 2 and all others rate constant 1. All complexes have molecularity at most two, the graph is strongly connected, and A has neither A nor 2A as a complex. The complex differences from zero include C, B, and A+B, so their span has rank three. There are five complexes and one linkage class: deficiency = 5 − 1 − 3 = 1. The class of zero is infinite: each `0 → A+B` followed by `B → 0` increases A alone, so all `(n,0,0)` are reachable.

This rate choice is not deterministically complex balanced: in a directed cycle the five complex fluxes must all equal. The zero-source flux is 2, so the C-source and B-source fluxes force c=b=2, but the B+C-source flux then equals bc=4. Thus the example lies outside the deficiency-zero/complex-balanced argument, outside the ACK pure-species condition, and outside the announced two-species scope. This is a direct algebraic check, not a claim that every older specialized sufficient theorem has been excluded. It is suitable as an optional addition, not a required new research program.

## Readers who could resolve the remaining external uncertainty

The user can choose a small number of these researchers. They are ranked by substantive overlap, not prestige. This report only identifies public professional information.

1. **Daniele Cappelletti**: unusually strong first reader because he coauthored ACK2020 and belongs to the announced two-species team. Most valuable issues: whether the pure-species removal matches a known/unpublished result, and whether the marked-target proof really avoids the old boundary obstruction. [Professional page](https://staff.polito.it/daniele.cappelletti/); [institutional profile](https://www.polito.it/personale?p=daniele.cappelletti).
2. **David F. Anderson**: equally natural first choice; coauthor of the conjecture, direct predecessor, and announced two-species work. The current public page lists his stochastic reaction-network work and 2025 path-method paper. [University page](https://people.math.wisc.edu/~dfanderson/).
3. **Jinsu Kim**: direct predecessor coauthor with recurrence and mixing-time expertise; particularly well matched to comparing sampled embedded chains with the present stopping-time construction. [Professional page](https://mathjinsukim.com/); [research account](https://mathjinsukim.com/research/).
4. **Andrea Agazzi**: best additional perspective on overlap with the two-species construction and multiscale behavior near coordinate axes. [University profile](https://www.imsv.unibe.ch/about_us/staff/prof_dr_agazzi_andrea/index_eng.html); [research page](https://andagazzi.github.io/).
5. **Chuang Xu**: separate close perspective on nonexplosion, stochastic class structure, and distinctions between regularity and recurrence. [University profile](https://math.hawaii.edu/wordpress/people/chuangxu/); [professional page](https://sites.google.com/view/chuang-xu).

A bounded period for expert comments is sensible, but public silence would establish neither acceptance nor rejection. Once the paper's independent proof audit is satisfactory and concrete corrections are resolved, waiting indefinitely for informal endorsement or an arXiv posting is not justified by the mathematical issues found here. The absence of a complete public competing manuscript is a reason for precise attribution and timely submission, not exaggerated priority claims.

## Remaining gap and limits

The strongest established result of this audit is an exact comparison with the closest accessible predecessor and current primary descriptions. Unresolved: full proof correctness (assigned separately), existence of unpublished overlapping work, and whether the new mechanism will prove useful beyond the present scope. No numerical citation prediction or acceptance probability is warranted. The initial source-search uncertainty cannot be eliminated by a Lean formalization: Lean can validate a specified theorem, but it cannot determine literature priority or journal fit.
