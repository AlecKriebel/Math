# Kourovka 21.16: finite group width versus monoid width

**Proposed current disposition: unsolved, 5/5. The historical scoped audit passed; the additive extension clarification requires the fresh revised-head descending audit before acceptance.**

The original asks whether a group can have finite width for every group-generating set but unbounded positive word length for some set genuinely generating all elements as a monoid. Each finite bound may depend on its generating set. No separating example or universal equivalence proof was obtained.

- [Complete result and remaining gap](RESULT.md)
- [Exact source normalization](SOURCE_NORMALIZATION.md)
- [Full independent review](final_review/REVIEW.md)
- [Mandatory turn2 extension-route clarification](TURN_2_EXTENSION_CLARIFICATION.md)
- [Additive turn3 control-description clarification](TURN_3_CONTROL_CLARIFICATION.md)
- [Original maintained Kourovka Notebook](https://kourovkanotebookorg.wordpress.com/)

## Scoped results

The five turns establish an inverse-cost criterion and canonical exhaustion obstruction; directed finite-index and strong-normal-kernel reductions; exact finite-action criteria; exclusions for conjugacy-controlled witnesses; and Cartesian, inverse-limit and compact Baire barriers. Every hypothesis is retained in the linked proofs. `TURN_2_EXTENSION_CLARIFICATION.md` states the established conditional implication omitted from the historical turn2 research-status sentence: any failure of MB extension closure for an MB kernel and MB quotient would already furnish a separating group, because Bergman proves CB extension closure. No such failure is constructed.

A bounded diameter for one symmetric set does not establish the all-generating-set group property. A dense semigroup or a proper invariant semigroup does not meet the algebraic monoid-generation requirement. Topological regularity restrictions apply only where stated; the original allows arbitrary abstract generating sets.

Bergman's uncountable-cofinality implication and Rosendal's stronger topological result are credited. Khelif's announcement is not treated as a reconstructed construction. No novelty certification is made. All 41 frozen author files and all five manifest-bound review files remain unchanged, including historical pending-review wording. The current wrapper and publication manifest bind the mandatory clarification; the fresh whole-package review in `draft_pr_descending_audit_20261002/audits/pr386_2525` governs acceptance of the revised head. Earlier pass/pending wording is historical and cannot substitute for that review. The audit is AI-assisted, not external peer review.

## Reproduction

Python3.10+ standard library only:

    python REPLAY_ALL.py
    python verify_review.py

The author replay reproduces311,547 exact controls and156 manifest bindings. The portable review wrapper additionally verifies every current publication-manifest binding (including the mandatory clarification), verifies the frozen manifests, reruns the author packet and adds6,833 independent controls without author imports. These finite calculations do not establish the infinite-group target or replace the written Baire and inverse-limit arguments.

Raw PDFs and imported records are excluded. Add `--sources PATH` to verify the seven primary PDF hashes when independently supplied. Source-free replay reports zero PDF checks. The additive control clarification distinguishes exact integer dihedral tests from the separate finite scans; the infinite proof is unchanged.
