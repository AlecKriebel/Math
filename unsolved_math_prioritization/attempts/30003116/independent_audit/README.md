# Audit of rational multiplicative orbit entropy

Problem 30003116, rank 993. Verdict: **accept restricted results and reductions; intended asymptotic problem remains unresolved after five approaches**. A one-line mathematical clarification makes the collision lemma explicitly assume U is nonempty; every orbit application already does. No headline bound changes.

Read `FULL_AUDIT.md` for proof-by-proof reasoning, constants, source checks and limits; `ACCEPTANCE.json` is the structured decision. This is an independent AI-assisted review, not formal verification or human peer review.

The original manifest remains pinned to `f0e11096444ac0a676a9e4a8cd267e51bb4600512574eebf961ce5789a03c115`. Original mathematical claims and bytes were not modified. This separate audit package contains authored analysis and code, public citations, hashes and verification metadata only. It excludes copied scholarly source documents, source extracts, dataset contents and private coordination material.

## Reproduce the audit

Run:

    python -B verify_audit.py --expected-manifest AUDIT_MANIFEST_SHA256
    python -B -O verify_audit.py --expected-manifest AUDIT_MANIFEST_SHA256
    python -B -OO verify_audit.py --expected-manifest AUDIT_MANIFEST_SHA256

The external audit manifest pin accompanies this package. These commands verify its flat inventory and repeat 38,715 independent mathematical controls per run. The controls do not import the original mathematical checker.

To repeat the original/candidate packet robustness comparisons, using a separate copy of the original packet:

    python -B independent_packet_controls.py --packet ORIGINAL_PUBLIC_DIRECTORY --expected-manifest f0e11096444ac0a676a9e4a8cd267e51bb4600512574eebf961ce5789a03c115 --hardened verify_public_hardened.py

This runs 174 cases covering both verifier variants and three interpreter modes. All mutations occur in temporary copies. Read-only cases intentionally update manifest file modes to 0444 and use new external pins; the original remains unchanged. The suite includes an intentionally false, re-pinned theorem sentence that both verifiers accept, demonstrating that integrity and finite tests are not mathematical proof verification.

## Required domain clarification

`MATHEMATICAL_CLARIFICATION.patch` adds nonemptiness to the abstract collision lemma. The average-energy identity also holds for an empty set, but its subsequent covering quotient T^2/E_r would be 0/0. This patch does not alter any orbit result. Apply it only to a separately identified revision with a new manifest and external pin.

## Optional hardening

`OPTIONAL_VALIDATOR_HARDENING.patch` and its exact resulting `verify_public_hardened.py` candidate are supplied. The patch validates manifest/schema target fields and cleanly rejects malformed top-level JSON and invalid Python syntax. The original already fails closed on malformed inputs; these are diagnostic/schema improvements.

Do not replace the frozen original silently. If adopting the patch, apply it to a distinct revision, rename the candidate to `verify_public.py`, recompute that file's manifest hash/size, and publish a new external manifest pin. For the otherwise unchanged original with only that validator replacement, the tested new manifest pin is `780dc0f057777d176ed7151a5d7c02b30f2d3e91fed9b92f86558c900ffaf8ec` using sorted, two-space-indented JSON and a final newline. This is a candidate identity, not a claim that the original was changed or published.
