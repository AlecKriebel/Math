# Second-round closure: algebra and source-fidelity supplement

Final checkpoint: 2026-09-26T05:06:11+00:00. Assigned closure-review completion estimate: **100%**. Verdict: **A1 closed; no new actionable finding in this scope.** The reproduction reviewer may freeze the reviewed supplement files. Any subsequent content change should be checked against the hashes below.

## Exact review scope and bytes

| Reviewed file | SHA-256 |
|---|---|
| `manuscript/main.tex` | `d79e9fcddad89606de769b672205d09f0e846e135d27a5419ba7b362095a1716` |
| `supplement/verify_exact.py` | `e7ba307b181897e2c4c250e662d52f421b5fc87c3760b01d4df3ee4b9b37ba4f` |
| `supplement/README.md` | `bd7b75d08920bf8f65929150fa3246ca9e71b19e1cb9754d768470fa99d3e2df` |
| `supplement/COVERAGE_AND_TRUST.md` | `651f29b2d3ef368c81d7d502ed8467fcd074684a6e6b9dd83cd3cdc16fdb7ff2` |
| `supplement/test_failure_modes.py` | `752106a62eeebc3db357ba7b3d12beb2ca8d00f9e4ac887155fd8038cc34cbeb` |

This review addresses round-1 A1 and consistency of the revised source-fidelity narrative and implementation. It includes the full `test_failure_modes.py` test harness, both supplement explanatory documents, the source-comparison portions of `verify_exact.py`, and manuscript sections 7–8 plus a check for stale comparison wording elsewhere. It does not replace the independent localization/topology/source reviews or the reproduction reviewer's full-suite execution.

## Why A1 is closed

1. Manuscript section 7 now states only the intrinsic assertions `||Y_1(K)||_F²=24` and `Y_2(K)=0`, which my independent first-round algebra verified exactly. The earlier numerical comparison to the GHR literal matrix and the same-spectrum/unitary-similarity assertion have been removed. Its remaining GHR citation describes the existence of the (3,1) localization theorem; it does not reproduce or normalize the disputed matrix. Section 8 no longer refers to a removed residual table or a supposedly literal old GHR representative.
2. `verify_exact.py` lines 464–546 independently DEFINE the common-prefactor operator. Comments, fingerprint messages, spectrum messages, residual output at lines 696–712, and far-commutativity label at lines 715–720 consistently describe that explicit definition. Its block entries, scalar and separate Pauli encoding agree with my fresh dense calculation from round 1.
3. Lines 547–575 construct the accessible preprint's distinct mixed-prefactor operator, using `+1/sqrt(2)` on the second block. They check the correct exact trace `1+i sqrt(3)`, Hecke residual squared Frobenius norm 18, and shifted generalized residual norms (30,60). These are the values in my independent `evidence/algebra_ghr_source.py`; the code does not silently identify this matrix with the common-prefactor one.
4. README and COVERAGE_AND_TRUST identify the accessible source precisely as **arXiv:1105.5048v1, p.26, Eq.(5.2)**. This is the version/page I inspected visually in round 1. They explicitly decline to adjudicate original intent or later journal typography. There is no unverified claim of a journal typo or intended author correction.
5. The trust document separates finite matrix checks from all-n mathematical and cited-source arguments and accurately limits the claimed implementation independence. Calling the Pauli formula an independent encoding is justified: it is a distinct explicit formula checked against the block construction, although both use the same arithmetic and matrix engine.

## Code and negative-test inspection

The two block arrays match the first-round independent transcription. The revised literal trace constant `CQ23(Q23(1), Q23(0,0,1))` is exactly `1+i sqrt(3)` in the declared basis. Shifted residuals use the intended qubit shifts; their squared Frobenius norm is the unnormalized sum of squared absolute entries. Common-prefactor scalar conversion and the Pauli formula

`-conjugate(q)/2 (III + i IXI - i ZZZ + ZJZ)`

are exact. No change to the mathematical R, K_H, q, S, or intrinsic quaternionic definitions was introduced by this repair. The section-4 table caption now explicitly says the expansion precedes imposing the circle, which is supported by my generic polynomial check.

`test_failure_modes.py` has 26 unittest methods. Its mutation helper requires one unique textual anchor, a nonzero process status, and an explicit `AssertionError:` in stderr; syntax/import errors alone cannot satisfy these tests. The common-block tests now name what they actually mutate. The optimization and no-assert-statement tests remain consistent with the documented policy. The suite does not claim to infer that every mathematically altered witness is not a YBO.

The reproduction reviewer reported all five curated routes and all 26 focused tests passing. I did not repeat the full suite. I added two separate review-only adversarial checks specifically for the newly introduced safeguards, captured in `evidence/algebra_closure.py` and `evidence/algebra_closure.txt`:

- Replace the literal preprint's second-block scalar by the common prefactor: rejected with `AssertionError: literal mixed-prefactor preprint trace is not 1+i sqrt(3)`.
- Reverse the ZZZ coefficient in the independently encoded common-prefactor Pauli formula: rejected by the matrix-equality check, with a nonzero exact (0,0) discrepancy `(sqrt(3)+i)/2`.

Both tests used temporary copies and left the five reviewed files untouched. They bind the verifier to SHA-256 `e7ba307b181897e2c4c250e662d52f421b5fc87c3760b01d4df3ee4b9b37ba4f`.

## Strongest verified conclusion and remaining boundary

The revised manuscript and supplement no longer attribute common-prefactor identities to the accessible preprint's literal mixed-prefactor display. The auxiliary formulas are separately defined, their different consequences are correctly checked, and the central manuscript argument no longer depends on the disputed display. **A1 is fully closed.**

The original authors' intent and typography of any later journal rendering remain unadjudicated by this algebra review. The revised files do not rely on either, so this is now a declared source boundary rather than an unresolved correctness gap. No outreach occurred, no manuscript/supplement files were edited by this reviewer, and no commit or push was made.
