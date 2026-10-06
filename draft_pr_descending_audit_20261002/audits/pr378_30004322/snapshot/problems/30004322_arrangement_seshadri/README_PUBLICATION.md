# Seshadri line-arrangement question: reviewed partial results

**Original unresolved, five substantive turns completed.** The source asks for the reciprocal maximum collinearity formula for the singular points of every reduced complex line arrangement. The maximum is over all projective lines. The packet proves restricted classes and an effective-range algorithm, not the unrestricted conjecture.

Read FINAL_RESULT.md, then TURN_1.md through TURN_5.md and review/ADVERSARIAL_REVIEW.md. The fifth turn gives an infinite 9q-line family with 13q²+3 singular points, exact Seshadri constant 1/(4q+1), and component-only fractional-cover optimum 4q. The final dual certificate is not asserted optimal over arbitrary auxiliary lines. The first-turn algorithm requires effective coordinates and r<k²; it is not an unrestricted algorithm for unspecified transcendental data. The Hesse value, full Fermat values and classical tools are credited. No historical novelty or human peer-review certification.

The source's report/workshop year is 2019, while the EMS publication date is 19 November 2020. This bibliographic qualification is additive; all36 frozen author files and eight independent-review files are unchanged.

## Reproduction

Python3 and SymPy are required. From this directory run:

    python REPLAY_ALL.py
    python review/verify_review.py --author-dir .

The first command reproduces214070 exact author assertions and62 manifest entries; the second additionally reproduces93918 independent assertions. In a normal public checkout, source_files_checked is0 because raw source PDFs and the screenshot are not included. This explicitly omits source hash verification. Populate sources/ with the exact six files bound by SOURCE_MANIFEST.json and SOURCE_ADDITION_FINAL.json to repeat those checks; primary URLs appear in the source gate and review/SOURCE_REVIEW.json. A partially populated sources/ directory fails rather than silently passing.

Finite controls support the written all-degree and infinite-family proofs; they do not substitute for them. There is no sixth author turn. The PR is a draft research record, with no merge or release.
