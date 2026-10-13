# Portable evidence index and stage boundaries

All links below are relative to this file. Authored records are preserved,
including historical holds and absolute paths; those describe their stage,
not the final accepted result. The paper and supplement define current scope.
Third-party source PDFs, extracted bodies and rendered images are deliberately
absent. Primary URLs and retrieved-byte hashes identify the sources inspected.

## Submitted stage, immutable

[PR #1024](https://github.com/AlecKriebel/Math/pull/1024), head
37b4b2fa44368f49e534e4982bd11f5667e0bf36, problem 30001113 / OWR-2492-004.
The [27-file pins](SUBMITTED_PINS.json) map every `relative` to `submitted/relative`.

- [Original proof](submitted/current/COUNTEREXAMPLE.md),
  [original audit](submitted/current/INDEPENDENT_AUDIT.md),
  [stage status](submitted/STATUS.json),
  [stage acceptance](submitted/ACCEPTANCE.md).
- [Historical bootstrap](submitted/BOOTSTRAP.py),
  [historical permission/mutation harness](submitted/MUTATION_TESTS.py),
  [historical finite runner](submitted/run_finite_checks.py),
  [original contract](submitted/FINITE_CONTRACT.json).

Do not run the historical sealed harness as a portable entry point. Its UID,
permission, prior acceptance and publication gates are not simulated or
overwritten. Original manifest paths are relative to `submitted/`; `current/`
and `historical/` retain their original relationships. Current executable
mathematical copies live in `../checks/` and are distinct from historical
environmental seals.

## New mathematical and source review

- [Formal-series derivation](formal_series_review_01/FORMAL_SERIES_REVIEW.md)
  and [family verdict](formal_series_review_01/VERDICT.json).
- [Actual-functor derivation](functor_review_01/INDEPENDENT_FUNCTOR_REVIEW.md),
  [independent arithmetic source](functor_review_01/verify_functor_identities.py),
  [pinned arithmetic output](functor_review_01/CHECKS.json),
  [source manifest](functor_review_01/SOURCE_MANIFEST.json).
- [Root 30-case reproduction](root_reproduction/FINITE_REPRODUCTION.json),
  [byte-for-byte contract comparison](root_reproduction/CONTRACT_COMPARISON.json).
  Adjacent `.stdout`/`.stderr` files are complete original raw receipts; remaining
  check outputs are also carried in the reproduction JSON.
- [Root source retrieval](ROOT_SOURCE_RETRIEVAL.json): public source links,
  hashes and old local raw paths. Local paths are provenance, not archive links.

The formal-series and actual-functor families began independently and did not
read each other's conclusions or the historical acceptance. These AI reports
cover mathematical mechanisms; they are not human peer review.

## Priority and attribution

- [Bounded priority audit](priority_review_01/PRIORITY_AUDIT.md),
  [verdict and mandatory credit](priority_review_01/VERDICT.json),
  [65-query ledger](priority_review_01/QUERY_LEDGER.json),
  [11-source/version inspection](priority_review_01/SOURCE_INSPECTION_MANIFEST.json),
  [artifact validation](priority_review_01/ARTIFACT_VALIDATION.json).

OWR p.3039, thesis Question 6.4.4 and arXiv v1 Question 4.4 express the
unrestricted question. Byszewski–Cornelissen published Propositions 4.1 and 6.1
are essential credited antecedents. These reports preserve source-version
hashes without distributing source bodies. Where paths point to another
historical stage or catalogue, the original paths are provenance; use the
public primary URLs to retrieve the source. The bounded audit is not an
exhaustive absence proof.

## Portable checks and current publication gate

- [Runner](../run_checks.py), [guard adaptation record](GUARD_ADAPTATION.json),
  [39-case complete receipt](PACKAGE_REPRODUCTION.json).
- [Original fixed contract](../expected/FINITE_CONTRACT.json),
  [independent baseline](../expected/verify_functor_identities.json),
  [intended independent fault reasons](../expected/INDEPENDENT_CONTROLS.json).
- [First new whole-package review](package_review_01/WHOLE_PACKAGE_REVIEW.md),
  [verdict](package_review_01/VERDICT.json),
  [unchanged copied records](PACKAGE_REVIEW_01_COPY.json). Render PNGs of our own
  PDF and third-party raw bodies are omitted; QA receipts and source URL/hash
  metadata are retained. These are stage-specific evidence, not portable-runner entry points.
- [Current review state](CURRENT_REVIEW_STATE.json): first fresh review passed
  with zero actionable issues; a NEW second review is pending. No immutable
  publication acceptance is claimed yet.
- [Paper](../research_note.pdf), [TeX](../research_note.tex),
  [scope and credit](../SUPPLEMENT.md), [metadata](../metadata.json),
  [inventory](../PACKAGE_MANIFEST.json).

The guard adaptation records all eleven original predicate ASTs. Current
arithmetic expressions are identical; explicit guards survive optimization.
Four actual-source fault families (two per reporting adapter) and six runtime
fault families each run in normal/-O/-OO modes. Syntax errors, missing files,
unrelated exceptions or wrong rejection messages do not count as accepted
negative controls. The complete output contract is compared without trimming
or omitting mathematical fields. None of these finite checks substitutes for
the complete formal-series or all-natural-transformation arguments.
