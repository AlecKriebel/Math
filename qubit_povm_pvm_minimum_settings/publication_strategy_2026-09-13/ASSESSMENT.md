# Minimum Bell-setting paper: publication assessment

13 September 2026 Pacific. Scope: this paper alone, its current source and verification package, its public July version, and recent related literature. This is an internal assessment with independent agent audits, not external human peer review.

## Recommendation and conditional impact

**7.8/10 under the author's supplied rubric**: a strong specialist result at the upper end of that category, worth selective circulation and journal submission. The rubric assumes the theorem is correct, genuinely novel, and published. This score therefore measures prospective scientific importance, not confidence in correctness, the author's affiliation, citation counts, proof-assistant adoption, or probability of acceptance. A reasonable judgment range is 7.5–8.1; it is not a statistical interval. The previous 8.1 is defensible at the optimistic end, but I would not treat this as a 9-level resolution of a famous central problem.

The value comes principally from the universal two-input theorem. For every finite, input-dependent output architecture, bipartite qubit POVM behaviors lie in the shared-randomness convex hull of qubit PVM behaviors. The same shared variable chooses the complete state-and-measurement strategy, and the state may change between branches. Together with the known possibility of separation at three-by-two settings, this gives a sharp minimum architecture. It rules out every two-input linear Bell witness of indispensable generalized qubit measurements under these conventions. An isolated new three-by-two inequality would warrant a lower assessment.

The result is restricted to qubits, two parties, and convexified behaviors. It does not classify the raw nonconvex sets, solve arbitrary-dimensional or multipartite measurement separation, or give a general practical simulation algorithm. These are scientific scope limits relevant to impact. Mathematical difficulty alone does not move a specialist theorem into a field-changing category.

## What the mathematical review supports

The current manuscript and all appendices were read. The independent mathematical audit formed its assessment before consulting earlier reviews. The exact separation and closure verification suite passed afresh. No clear fatal gap was identified in the bounded review.

The main equality argument has three substantial steps. First, cone circuits simulate the case with a binary party using complete projective strategies. Second, extremality and common-span filtering reduce a hypothetical separator to binary–ternary measurements on each side. Third, an exact physical Lorentz-incidence model excludes all ranks of the metric differential: positive second variation at rank at least two, a multiplier obstruction at rank one, and an explicit local decomposition at rank zero. The physical reconstruction and multiplier identification are especially valuable targets for specialist scrutiny.

The September correction is substantive but already incorporated in the working source: scalar positive-pairing inequalities do not imply Lorentz signature. Signature (1,3) is now an explicit separate condition. The Lean physical-frame assumptions already supplied the necessary signature. Do not present the historical scalar-domain counterexample as a remaining refutation of the main equality.

Detailed evidence and limits: [mathematical audit](math_audit.md) and [Lean audit](lean_audit.md). The strongest checkable endpoint is the physical convex-hull equality, with attained separation, not merely the existence of certificates for selected numerical examples.

## Lean: substantial value already obtained

The package already contains formal proofs of the principal physical claims. Historical full-run evidence records 58 mathematical modules, 675 public declaration dependency reports and 25 expanded statement contracts. This review rehashed all 88 protected inputs and 123 command logs with no mismatch, and freshly ran the independently expanded complex-matrix equality contract and scalar-domain counterexample. Both passed. The dependency audit uses only standard Lean axioms. This review did not rerun the whole full-build suite.

The model starts from actual positive semidefinite complex matrices, normalized states and measurements, and Born probabilities. Its final equality is unconditional within that physical model. This is much more valuable than formalizing a theorem whose central physical conclusion is included as an assumption.

**Do not begin a second broad formalization project.** The useful remaining work is documentation, precise correspondence, and independent reproduction of the existing package. Lean does not determine novelty, importance, or whether a referee can follow the written argument. It does substantially reduce proof-error concerns when the formal statement matches the claimed physical result, which matters particularly for a long proof developed with substantial AI assistance.

The current certificate does not claim to formalize every auxiliary manuscript lemma. Some geometric, duality and optimization arguments are specialized or replaced. It also proves a stronger projective bound, 289/10, through an alternative exact sum-of-squares argument; the manuscript's original analytic bound is weaker. Both suffice for strict separation and neither is an exact-optimum claim. Optional small future tasks are explicit generic smaller-dimension embedding and stochastic-channel bridge theorems, if a reviewer asks. They are not reasons to postpone submission.

## Public revision is the immediate bottleneck

At the time of checking, the [publication record](https://zenodo.org/records/21699161) was created and last modified on 30 July 2026 and exposed only the version-1.1.0 PDF. The [paper landing page](https://aleckriebel.github.io/Math/papers/minimum-bell-setting-complexity/) also identified July 30/version 1.1.0 and directed readers to the old source tag. The current manuscript's verification section still describes the symbolic scripts without mentioning the completed Lean development. A reader following the public paper therefore does not encounter the current corrected, formally checked package as one consistent release.

The next revision should:

1. Include the already-corrected Lorentz-signature definition and a concise changelog.
2. Add an accurately scoped Lean verification paragraph, theorem map, fixed build evidence and reproduction link to the manuscript. Clearly separate principal endpoints from auxiliary coverage limits.
3. Update the related-work discussion and bibliography for the recent separation paper below.
4. Make the publication PDF, review PDF, source, proof package and website agree on version and scope. Archive the revised paper under the existing Zenodo record's version history and link the exact proof snapshot. Keep the historical July release intact.

No new manuscript, website deployment, Zenodo version or GitHub release was created during this assessment. These are recommended next actions, not completed ones.

## Literature positioning

[Vértesi and Bene (2010)](https://arxiv.org/abs/1007.2578) already established the relevant three-by-two qubit POVM advantage. The paper should continue to lead with the matching lower bound, not a claim to have first answered the broad existence question.

[Zhu et al., August 2026](https://arxiv.org/abs/2608.01317) provide a different analytic separator with Lean verification and an unrestricted quantum optimum. Their discussion leaves the two-setting question open. Add a precise comparison: the universal two-input equality and resulting minimality classification are this paper's distinct contribution. The July 30 deposit predates their August 2 initial submission, but dates alone establish neither influence nor misconduct.

[Cerf and Ollivier](https://arxiv.org/abs/2603.26875) address local perturbative quantum-correlation geometry. [Oszmaniec and collaborators](https://arxiv.org/abs/1609.06139) study operator-level projective simulation. These neighboring questions should remain clearly distinguished from equality of convexified Bell-behavior sets. This search was targeted, not an exhaustive novelty certification.

## Journal and timing

Retain the workbook's Physical Review A first choice and Journal of Physics A fallback. PRA explicitly covers quantum foundations and quantum information and allows detailed research articles. It published the closest early separation paper. The older repository recommendation to begin with Quantum should not override the user's current preference and access constraints. A prestige-first submission campaign is not necessary for this specialist result. [PRA scope and criteria](https://journals.aps.org/pra/about).

Aim for submission after one focused revision and **two to three weeks of targeted comment opportunity**, assuming no substantive unresolved objection. If the revised package is ready and shared by approximately September 18, October 2–9 is a reasonable planning window. These are advisory dates, not a journal rule or a promise of review completion. A reader actively checking a specific delicate lemma justifies an agreed short extension; silence alone does not justify indefinite delay. Public comments can continue while the journal reviews the work.

Lack of arXiv access need not delay PRA submission: its instructions make an arXiv identifier optional and permit direct PDF upload, with source requested at acceptance. [APS submission instructions](https://journals.aps.org/authors/web-submission-guidelines-physical-review). IOP also permits preprint sharing on other platforms. [IOP preprint policy](https://publishingsupport.iopscience.iop.org/preprint-pre-publication-policy/).

Before submission, close concrete correctness objections, confirm the actual submitted PDF matches the cited verification snapshot, update the bibliography and verification description, and retain the existing candid AI-use disclosure. A Zenodo DOI records an accessible version; it does not substitute for expert assessment or require a particular waiting period.

## Scope of the delivered workbook

Only the named paper's score, TODO and Updates cells were revised; its existing average formula is retained and recalculated. The other papers were not individually reviewed or rescored. The supplied correspondence history remains intact in the local workbook. Research-note commits exclude that workbook and correspondence-derived personal recommendations.
