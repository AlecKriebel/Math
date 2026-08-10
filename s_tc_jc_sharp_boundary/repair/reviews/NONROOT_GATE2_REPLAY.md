# Gate 2 independent nonroot full-closure audit

Status: **UNRESOLVED**

## Verdict

UNRESOLVED — independent execution did not close every gate.

This is an independent implementation of the standard nonroot local gate. It does not import or execute any submitted Gate 2 engine.

## Exact finite theta atlas


## Cycle/theta directions

- Theta to cycle necessary survivors: True.
- Cycle-to-cycle nonisomorphic equal survivors: True.
- Cycle-to-theta completed strong survivors: 0.
- Promotion tensor types / checked pullbacks / strict / uncertified: unknown / unknown / unknown / unknown.

Every uncertified pullback is retained and promoted; none is treated as nonzero.

## Arbitrary subdivisions

Status: **UNRESOLVED**.

Rigid support plus one locates each directed segment; support plus two fixes pair order on a shared segment. The exact long-word tests include empty and symmetric segments, path sinks, reversed orders, and twelve blocks on one segment. Effective JC path products map `(0,1)^k` surjectively onto `(0,1)`, so every selected weak tensor is realized in Theta0.

## Local theorem

Under the audited hypotheses, `B preceq_JC B'` and `B bowtie_JC B'` occur exactly for labelled standard semi-directed isomorphism or ordinary triangle redirection `T`. T sufficiency and regularity use the inherited exact Theta0 port-tensor correspondence; all strict alternatives are excluded by identities whose target pullbacks have exact fixed sign on the complete open cube.

## Parameter domain and logical limits

All sign certificates use independent effective JC multipliers and inheritance parameters strictly in `(0,1)`; no endpoint 0 or 1 is used. Effective path products are surjective within this domain. No new numeric generic-rank claim is made: strict directions are excluded on the entire open cube, while isomorphism/T regularity is an inherited exact result. Saturated complex boundary ideals are not computed here and are not needed for the open-Theta0 containment conclusion.

The auxiliary old counts-only/tensor-smoke baseline was terminated after roughly 18 minutes at 100% CPU without producing a certificate. It is recorded only as a timeout and supplies no evidence for this verdict.

## Deterministic replay

```bash
PYTHONDONTWRITEBYTECODE=1 AUDIT/CLEAN_ENV/bin/python AUDIT/INDEPENDENT_IMPLEMENTATION/audit_gate2_nonroot_full_closure.py --output AUDIT/INDEPENDENT_IMPLEMENTATION/gate2_nonroot_full_closure_audit.json --markdown AUDIT/GATE2_NONROOT_FULL_CLOSURE_AUDIT.md
```

The JSON companion records all exact factor hashes, class checks, finite counts, promotion levels, input hashes, and implementation limits.
