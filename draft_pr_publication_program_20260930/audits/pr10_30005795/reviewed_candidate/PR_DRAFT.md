# Draft PR description

Title: Audit 30005795: known Nemuro bound and source corrections

Base: main  
Head: dot/math-30005795  
Draft: true (original delivery; acceptance review below)

## Summary
- Recover the original OWR p. 839 question and its missing Du Val context
- Correct the printed valuation-domain typo: prime divisors over S, not X
- Identify the existing componentwise lct bound in the 2023 Nemuro Lemma, published Lemma 27 / preprint Lemma 26
- Supply a self-contained bound, local/global distinction, finite-support justification and optional optimal-lct characterization
- Flag upstream 30005796 as the same target

## Status
Known-method/source-status correction; no novel solution claim. The PR updates the central QUEUE row to already_solved with the known-method/source-status correction. State, catalogue and historic review files are preserved. One substantive reconstruction turn recorded, below the five-turn cap. Model was gpt-6-astra at xhigh, not ultra.

## Checks
- Full pinned source record read; matching prior report absent (unique problem code)
- Dataset SHA256 verified against manifest
- Original OWR PDF p. 839 visually inspected
- Published Appendix B and author preprint checked, including differing lemma numbering
- PR and branch searches found no prior matching work before branch attempt

## Publication history
The initial connector request to GitHub create_branch for AlecKriebel/Math, dot/math-30005795, base_ref=main returned 403 Resource not accessible by integration. No branch, push or PR was created by that request. On 2026-09-30, the separately authorized GitHub CLI login was verified with repository push permission; duplicate branch/PR checks were repeated and were empty. The source-status files were checkpointed through that route. The single draft PR is [#10](https://github.com/AlecKriebel/Math/pull/10), with initial commit `13a35e9b94183a8ae761407ee25e14210a888bbb`.

## Acceptance review
Independent LCT, Mori finiteness and primary-source families checked the result. Corrections specify log discrepancies, endpoint Q-linear effectivity and the bibliography on p.844; the original frozen snapshot remains available in the program audit folder. A fresh adversary will review the complete corrected candidate before acceptance. No novel paper or DOI is planned for this partial outcome.
