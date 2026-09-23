# Prepublication adversarial artifact review

Timestamp: 2026-09-23 03:35:50 UTC. Completion estimate: **100% of this mathematical and reproducibility review**. Verdict: **PASS; no substantive mathematical or executable-verification issue found.** Historical priority remains bounded by the explicit limitations in `priority_independent.md`.

Reviewed `paper/paper.tex`, both verification scripts and their saved outputs, `verification/README.md`, and `audit/priority_independent.md`. The original Knudson source was checked in the preceding independent audit; the BLW comparison was independently checked again against the primary preprint.

## Fresh execution and consistency

Both `verify.py` and `independent_check.py` ran successfully under the local Python interpreter, in normal mode and with `-O`. All four executions produced outputs byte-for-byte identical to their respective saved output files, with no stderr. `verify.py` is byte-for-byte identical to the supplied input script.

The source statement, paper, and computations agree on the filtration, all three finite pairs, the incident matching, the entire directed incidence graph, the zero-path witness, and the changed matching after the earlier cancellation. All vertex rows and edge columns use the same filtration order. The paper does not infer a path from an algebraic elimination and does not conflate the initial field with the modified field.

The inspected source hashes are:

```text
b70401cbcdabf96e4b0a4f9a35b40ef5414619399f21ee984312fc4e85baf7f5  paper/paper.tex
aed912e2ba41f1ce6ed400a65d9c0cc6dc7cdd6361b7e87eb924d303607f1df6  verification/verify.py
d3b5d2fc62636a7ed3d0e8ffa1b759348c715a9bf97016666454e712ce087359  verification/independent_check.py
0e514fb93709499f15e272cb166e4ab99c02439c76c9cd0ce2e8be3f4f3ed8c5  audit/priority_independent.md
```

## Rank invariant and indexing

Stage `s` in the independent program means the subcomplex after the first `s` cells, so stage 0 is empty. For `0 <= i <= j <= 7`, each component of stage `i` maps to its containing component at stage `j`. Their image is spanned by exactly the later components meeting an earlier vertex. Distinct later components are independent in ordinary H0 over any field. Thus `rank(i,j)` computes the inclusion-map rank correctly.

For an interval `[B,D)`, its contribution to that rank is

`r(i,j) = 1_{B <= i} 1_{j < D}`.

Consequently

`r(b,d-1) - r(b-1,d-1) - r(b,d) + r(b-1,d)`

equals 1 exactly when `B=b` and `D=d`, and is zero otherwise. This proves the mixed-difference formula used by `barcode_pairs()`. The loops have `1 <= b < d <= 7`; every requested rank has a valid inclusion direction, birth 1 correctly uses the empty stage, and death 7 is included. Infinite intervals contribute zero to the difference.

A fresh supplementary check compared all 36 valid inclusion-map ranks, including both endpoint stages, with the barcode `[1,infinity), [4,5), [3,6), [2,7)`. Every entry agreed. A separate indicator-function check of the four-term formula for every possible interval birth/death on these stages also passed. Hence the output `[(4,5),(3,6),(2,7)]` has the intended one-based birth/death meaning, with no off-by-one error.

## Arbitrary fields and BLW scope

The paper's signed boundaries are correctly oriented. Reductions give `d-c`, `c-b`, and `b-a`; their latest nonzero coefficients are all 1. These integral identities remain valid in every field, including characteristic two, with the same pivots. This is a proof of the arbitrary-field claim. The executable rational and five-prime checks are additional finite checks, not its logical justification.

Independently read Section 3.3, Lemma 9 and Theorem 13 of the [Bauer–Lange–Wardetzky preprint](https://arxiv.org/pdf/1001.1269). Lemma 9 concerns an intermediate field in a cancellation sequence on a combinatorial surface, after descendants of the relevant pair have been cancelled. The paper merely compares the role of ordered cancellations and expressly avoids claiming to contradict those results. That scope is accurate. The interval example is proved directly and is not presented as an application of the surface theorem.

## Remaining issues and limits

- **No blocking mathematical issue.** No correction to the theorem, proof, arbitrary-field extension, verifiers, or recorded outputs is required.
- **Optional wording precision:** the verification README says the independent script calculates ranks of *all* H0 inclusion maps. The script evaluates the ranks needed for the mixed differences, rather than explicitly evaluating the complete table (for example, `rank(7,7)` is unnecessary). The complete-table check was performed in this review. Changing that phrase to “calculates H0 inclusion-map ranks” would exactly describe the shipped script.
- **Priority uncertainty remains substantive but disclosed:** the unpublished/preparation item and inaccessible book/thesis prevent an absolute novelty certification. The paper correctly calls its literature search bounded and makes no claim of guaranteed first discovery or catalogue status.
- This review covers mathematical/source/code consistency; it is not PDF layout QA, a formal proof-assistant certificate, or a second exhaustive literature search. No paper edits, commits, publication, or external communications were performed by this reviewer.
