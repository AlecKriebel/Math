# Source and status audit: 10300025

Checked 2026-09-30. This record corrects the literal statement's open-status classification. It claims no new research result.

## Exact source

The complete original 2002 PDF was retrieved from [arXiv:math/0209081v1](https://arxiv.org/pdf/math/0209081v1). Question 8.2 and its two remarks on printed p. 16 were read in extracted text and visually checked on a rendered page. The displayed bound is explicitly allowed to depend on the group element. The first remark separately discusses a constant independent of that element. Thus a group-uniform bound is not the displayed question.

The earlier full published paper [The Geometry of R-covered foliations](https://msp.org/gt/2000/4-1/gt-v4-n1-p17-p.pdf), Geom. Topol. 4 (2000), was also obtained. Question 5.3.19 on printed p. 511 has the same per-element quantifier. Section1.1, p.461, specifies closed orientable manifolds and co-orientable foliations. These hypotheses give a finitely generated orientation-preserving action, to which the credited theorem below applies.

The 2002 remark claiming a toroidal obstruction cannot obstruct the literal reparameterization problem: the elementary proof works for all countable line actions. The stronger geometric restriction, if any, intended by that remark was not determined here. No claim is made about a reconstructed geometric strengthening, a previously fixed leaf-space metric, ambient leaf distances, or a uniform constant over all group elements.

## Credited existing result

Deroin–Kleptsyn–Navas–Parwani, *Symmetric random walks on Homeo+(R)*, Ann. Probab. 41 (2013), 2066–2089, [DOI10.1214/12-AOP784](https://doi.org/10.1214/12-AOP784), Theorem8.5, gives a conjugacy of an irreducible finitely generated orientation-preserving line group to Lipschitz homeomorphisms, each with bounded displacement on the whole line.

- [Current arXiv record](https://arxiv.org/abs/1103.1650) checked: v1 March8,2011; v2 March13,2012; v3 July22,2013. No withdrawal displayed.
- The full [v3 PDF](https://arxiv.org/pdf/1103.1650v3) was retrieved. It is the journal reprint, with a pagination/typographic-difference notice, not an inaccessible abstract. Relevant §8, Proposition8.1, Lemma8.3, Proposition8.4 and Theorem8.5 were read; Theorem8.5 and its proof on reprint p.23 were visually checked.
- Theorem8.5's proof enlarges the group by two rationally independent translations to arrange minimality, then uses the preceding stationary-measure construction. The same enlargement also removes irreducibility as an obstacle when one only needs the conclusion for a given finitely generated subgroup.
- Proposition8.4 explicitly identifies the displacement as (x\mapsto g(x)-x) and bounds it uniformly in (x) for each (g). This is the bound used in the elementary implication to the source question, not a bound uniform in (g).
- The stronger published theorem is credited; the package does not independently recertify all stochastic results and their dependencies in the entire paper. Its two self-contained deterministic proofs independently establish the weaker conclusion actually needed by Question8.2.
- The paper itself points to Deroin–Kleptsyn–Navas, Acta Math.199 (2007), TheoremD, as an earlier route. That earlier route is not independently audited here; no priority claim is based on it.

## Prior-attempt and duplicate gate

Before constructing the artifact, read both repository AGENTS files, the queue README, the complete pinned problem record and its untrusted prior report. The unique numeric ID joins to one AMR-102-0025 code in the pinned dataset revision37e53eabe540fb458758e198be61634bd02ee008. The existing report contains only open-status triage, with no proof or earlier campaign attempt.

The main queue at start records rank75, queued,0/5. No matching attempt directory, historical research commit, branch, all-state PR, or related-target-group entry was found. A full pinned statement search for holonomy/leaf-space coarse-isometry formulations returned only this record. The sibling Question7.1 is a different target. Broader title terms produced unrelated PR15, which concerns semigroup hole bounds and was rejected as a false positive.

## Literature search and interpretation limits

Primary-source searches included the exact source numbering, its 2000 predecessor, coarse1-quasi-isometries of R-covered leaf spaces, and conjugacy of finitely generated line groups to bounded-displacement homeomorphisms. They located the published2013 theorem above. Bounded searches did not find a later primary source explicitly discussing the historical Question8.2 numbering or explaining its toroidal remark. Absence of such a search hit is not proof that no discussion exists.

Recommended classification: **already_solved for the literal statement**, credited to known line-action conjugacy results. The countable/orientation-reversing verification avoids an artificial compactness or co-orientation restriction in the imported wording; it is not promoted as a novel theorem. No separate discovery credit is requested.
