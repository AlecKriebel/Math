# Content candidate — conditional on mathematical clearance

This is scope-grounded draft copy, not a publication recommendation or a mathematical verification result. The current paper is version 2.0.0, published 2 August 2026 as a named Zenodo release, DOI [10.5281/zenodo.21753997](https://doi.org/10.5281/zenodo.21753997). Its earlier edition belongs to the same work.

## Suggested title and search description

Title: Reversible reaction networks with a curve of equilibria and no common factor

Suggested slug: `reversible-reaction-equilibrium-continuum`

Description: A four-parameter mass-action family preserves a positive equilibrium ellipse without a common polynomial factor, with exact rate and stability results.

Status: Independent research preprint. Substantial generative-AI assistance is disclosed in the manuscript. Public release and exact-code availability do not constitute peer review. Any later internal-review status must come from completed mathematical reviews, not this scope report.

## Full technical abstract candidate

We study a deterministic mass-action system on a fixed reversible reaction graph with three species, ten complexes, ten reversible pairs and one linkage class. We describe the complete four-dimensional rational rate space for which a prescribed compact positive algebraic ellipse is a steady-state set. The conic-preservation map is a 21-by-20 rational matrix of rank 16. Writing the four free rates as `(a,b,c,d)`, strict positivity of all twenty directed rates is equivalent to `a,b,c,d>0`, `b<c` and `192a+221c<154d`. Every positive member has full stoichiometric rank, so the ellipse lies within the single positive compatibility class. A nonempty Zariski-open subset of this constrained family has geometrically coprime coordinate polynomials; consequently, the equilibrium curve is an actual height-two component rather than the zero set of a scalar factor shared by the whole vector field.

A primitive positive integer specialization at `(a,b,c,d)=(653,1,70,915)` has largest rate 10,296 and total rate sum 52,464. Bounded exact enumeration establishes simultaneous optimality of these two quantities among positive integral vectors on this fixed support preserving this conic. Its steady ideal is radical: over the rationals it is the intersection of the conic prime with a disjoint degree-15 maximal ideal, which contributes fifteen reduced isolated points over an algebraic closure. The original, larger integer specialization is retained as a separate family member and has the same type of decomposition.

For that original specialization, exact characteristic-polynomial identities and Sturm counts classify transverse stability along the entire ellipse. A normally attracting arc and a saddle-type arc meet at two isolated transition points where normal hyperbolicity is lost. Structural arguments show that three species are necessary for the target phenomenon, that one linkage class forces full stoichiometric rank in three species, and that a weakly reversible three-species example requires at least five complexes. The paper supplies exact symbolic verification artifacts for its algebraic, integer-optimality and stability claims. The four-dimensional family has codimension sixteen in ambient rate space; no persistence under arbitrary rate perturbations or global minimality of the ten-complex support is asserted.

## Plain-language explanation candidate

A reaction network can settle at more than one balance of concentrations. Earlier examples even allowed a whole continuous curve of equilibria, but their equations shared a polynomial factor: wherever that factor vanished, every rate of change vanished with it.

This construction claims a different mechanism. Three species and ten reversible reaction pairs preserve an entire ellipse of positive equilibrium concentrations even though the three equations have no common polynomial factor. The paper also identifies four parameters that can vary while keeping that same ellipse. For typical choices within this specially constrained family, the absence of a common factor remains true.

The distinction matters: a continuum of equilibria need not come from one shared scalar multiplier. The family is nonetheless special, and the paper does not claim that the ellipse survives arbitrary changes to all reaction rates. These are mathematical mass-action models, not experimentally validated chemical reactions.

The smaller integer example and the stability calculation concern different rate choices. The smaller example minimizes two integer-size measures within this fixed construction. The stability result applies to the original example, where part of the ellipse attracts nearby transverse motion and another part has saddle behavior. The paper does not prove that the whole ellipse attracts trajectories.

## Provenance and publication constraints

- Canonical record and citation: [Zenodo 21753997](https://zenodo.org/records/21753997), version-specific DOI 10.5281/zenodo.21753997. Do not use the mixed-repository concept DOI 21753404 as an all-versions paper link.
- The main PDF is **embedded in the sole published ZIP**. The exact member is `AlecKriebel-Math-26f7e00/weakly_reversible_continuum_no_common_factor/releases/v2.0/output/pdf/manuscript-v2.0.0.pdf`; SHA256 `fe429cf073b30cacfe1ba75624236cda2545c44076f711d4319dcb22ff79512b`, 14 pages, 108,423 bytes.
- The containing public archive is `AlecKriebel/Math-wr-continuum-v2.0.0.zip`; SHA256 `d92c83fd79fc1a723bcaa3fd0674f9fcf04dec18bb6a220c583f6bef4cbdc9fd`. Link the 180 MB archive externally; do not host it as a website asset.
- No top-level Zenodo PDF URL exists in the record. Any later embedded-reader copy must retain the authenticated archive-member provenance. The duplicate manuscript draft has identical PDF bytes and is not a separate edition.
- Keep the historical eight-page v1 reader and one-page companion separate from the current 14-page main paper. Consolidate all editions into this one research entry.
- The fifteen algebraic isolated points are not asserted to be positive concentration equilibria. The paper's genericity is internal to a constrained family. Graph reversibility is not detailed balance. Integer-rate optimality is not global network minimality.
- Boros–Craciun–Yu already supplied continuum examples and a same-curve parameter family with a common factor. Describe the no-common-factor mechanism and exact constrained structure as the contribution; avoid an unsupported universal priority claim.

## Follow-up recommendation

None proposed. Existing minimum-complexity questions remain interesting, but this scope review has not established enough novelty, precision or a plausible new route to meet the required bar for a paper-worthy follow-up.
