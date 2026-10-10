# Independent audit companion: 30005902

Verdict: **ACCEPT with scope restrictions; no mathematical correction required.** The 27-dimensional F₃ example has a nonzero bracket on two Ext¹ classes. Finite-dimensional characteristic-zero and input-degrees-at-least-two variants remain unsettled by this work. No novelty, human peer-review or editorial-acceptance claim is made.

Start with `AUDIT_REPORT.md` and `AUDIT_RESULT.json`. The original author ZIP is preserved separately; its authenticated hashes are recorded here.

Standard-library replay:

    python3 -B independent_check.py
    python3 -B verify_audit.py --manifest-sha256 DIGEST --negative-controls --author-zip /path/to/HOPF_LIE_30005902_AUTHOR_SAFE_FREEZE.zip

Use the manifest digest from the separately supplied audit receipt. Omitting the author ZIP skips only the original freeze replay. Omitting the external manifest digest provides internal consistency, not authentication of this audit freeze.

The audit's 29,708 assertions include comparison-map checks independent of the author's 26,584 assertions. The full-corpus rehash is reproducible with `check_identity.py`; see `--help` for the externally supplied inputs. Corpora, repository responses and source PDFs are deliberately absent. Stored identity/source/repository results attest to the audit-time observations; the portable verifier does not pretend to refetch them.

A new audit does not overwrite the historical pending-review wording of the author's original files.
