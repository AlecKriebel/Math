# Independent audit of problem 30005356

Verdict: PASS for the negative answer to the literal unrestricted-characteristic assertion. In positive characteristic, inverse Frobenius is definable and lies outside Z[theta]. No mathematical correction was required. The catalogue review-hash omission is supplied as an audit addendum. The author freeze was not changed.

Files:

- AUDIT.md: adversarial checks, scope, correction, and limits
- INDEPENDENT_PROOF.md: self-contained reconstruction, including existence and polynomial faithfulness
- independent_controls.py and INDEPENDENT_RESULTS.json: independent exact finite controls
- verify_public_evidence.py and PUBLIC_EVIDENCE_RESULTS.json: full-corpus/source/freeze fingerprints and review-hash reconstruction
- SOURCE_AUDIT.json: source locations, fresh retrieval metadata, search scope and limitations
- verify_manifest.py and MANIFEST.json: integrity verification

From this directory run:

    python3 verify_manifest.py
    python3 independent_controls.py --check INDEPENDENT_RESULTS.json

The public-evidence program accepts local copies of the separately available public inputs; see its --help output for required paths. Source inputs are intentionally excluded from this packet. The evidence verifier does not output their text or raw records.

The finite controls are sanity checks, not proof of an infinite model-theoretic theorem. This is an AI audit and contains no novelty, human-peer-review, or editorial-acceptance claim. Neither the characteristic-zero classification nor the classification using Z[1/p][theta] is resolved here.
