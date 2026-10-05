# Independent audit packet

Decision: PASS, with no required mathematical corrections. The prior resolution remains explicitly attributed to an unrefereed, AI-assisted preprint. See `AUDIT.md` for the complete proof, adversarial hypothesis audit, source-access limitations and publication qualifications.

- `AUDIT_RESULT.json`: concise outcome and exact test counts.
- `SOURCE_AUDIT.json`: public provenance, retrieval and inspection metadata.
- `independent_verify.py`: self-contained, standard-library-only independent verifier.
- `independent_results.json`: deterministic expanded regression output.
- `replayed_check_results.json`: byte-identical replay of the frozen author's results.
- `verify_audit.py`, `AUDIT_MANIFEST.json`: portable payload integrity and original-input binding.

Run `python3 independent_verify.py > regenerated.json` and compare it with `independent_results.json`. Run `python3 verify_audit.py` for the portable audit's integrity. When the frozen author folder/archive are available, add `--author ../author --archive ../rank652-30005479-authored-packet.tar.gz` to verify their binding and all original payloads too.

Expanded tests: 225 instances, comprising every labeled loopless matroid on 1-5 elements and four named non-complex-realizable examples; 15,954 partitions; 29,268 objective evaluations over 1,084 rational subspaces on each of 27 four-element matroids; 11,664 two-matroid coordinate-projection checks; 20,220 constructed forest edges; and 100 additional random rational-subspace checks. These finite checks do not replace the universal mathematical proof.

No downloaded PDF, source full text, rendered source page, corpus content or private coordination file is part of this portable packet.
