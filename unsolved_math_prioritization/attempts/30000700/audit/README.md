# Portable independent audit

Verdict: PASS for the literal printed universal IM statement, with the zero-value scope qualification. No mathematical correction is required. Novelty and a strengthened nonzero-a problem are not certified.

Read AUDIT.md for the full independent reasoning, source inspection, adversarial controls, and limitations. CORRECTIONS.json gives machine-readable guardrails. BINDING.json binds the exact original author archive and all its members. AUDIT_MANIFEST.json binds the files of this audit (excluding itself).

Run with Python 3, standard library only:

    python3 independent_verify.py
    python3 verify_audit.py
    python3 verify_audit.py --author-packet /path/to/author-packet.zip

The author script's exact rerun output is AUTHOR_CONTROL_RERUN.json. Independent controls are INDEPENDENT_CONTROLS.json. Source material and private coordination are not included. Archive originals were preserved. No remote mutation was performed.
