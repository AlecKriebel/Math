# Kourovka 21.146

Disposition 2026-10-17T20:48:54.389451+00:00: **already_solved** for this program’s eligibility screening. Selection/priority audit complete (100%); no original solution is claimed here.

## Authoritative problem

Official 21st edition, 6 October 2026 update, printed p. 198: for every n>=3, does every group of type F_(n-1) embed in a group of type F_n, or even F_infinity? A group is F_k if it has a classifying CW space with finite k-skeleton. Contributor: M. C. B. Zaremsky; question attributed as well known.

## Prior complete resolution and exact implication

OpenAI, *A universal group of type F_infinity*, manuscript dated 23 September 2026, Theorem 1.1, gives one F_infinity group containing every finitely presented group. Earliest public repository copy observed in this audit: 6 October 2026 at 21:58:50 UTC, commit adc7f1241b42e322a6451854ab7e4b4c146bf78a. The current 12 October copy is byte-identical. Source: https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/A-universal-group-of-type-F-infinity-September-23-2026/paper.pdf .

Since n-1>=2, all input groups in the Notebook question are finitely presented. The prior theorem therefore supplies an F_infinity target, hence an F_n target, for every input and every n. No word-problem assumption is imposed. This covers all original quantifiers.

The Notebook’s unmarked open entry predates the earliest observed public release. Zaremsky’s newer primary list dated 8 October 2026 crosses out this exact question under its stated convention for AI-solved problems: https://zaremsky.github.io/open_problems.pdf . Root visually confirmed that page; no human referee report is inferred from the crossout alone.

## Independent verification performed here

The disposition is not based solely on a catalogue or an AI preprint assertion. Two independent adversaries reconstructed the controlled integral-chain induction, product-module argument, ascending-HNN conventions and homotopical finite-skeleta passage. Root independently checked the finite idempotent additivity lemma, the faithful nested group-algebra envelope and universal finitely presented group input. Their coverage together checks the informal proof, with no unresolved mathematical objection found. Root reproduced the separate exact checker’s 4,998 integral-chain identities; those finite checks supplement the argument. External standard inputs include Higman embedding and the stated Hurewicz/cellular approximation/Whitehead theorems.

A separate source-level Lean scope/dependency audit found matching top-level universal quantifiers and geometric F_infinity definitions. It did not run a full kernel/comparator build because the local Mathlib project dependency was absent. The prior informal proof audit does not depend on claiming such a rebuild. See the dated reports in reviews/ and priority_20261017.md for precise evidence and limitations.

## Outcome

Skip as a prior complete solution, not an original discovery by this program. No new paper or Zenodo record, and no new publication-tracker row, will be created for it. The preliminary homological observations and blocked rope-trick route remain recorded as limited observations, not a second solution. Next candidate in descending order: 21.145.
