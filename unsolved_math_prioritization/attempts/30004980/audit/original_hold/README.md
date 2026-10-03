# Maximum twin width independent audit packet

Verdict for frozen commit ab502620095141f19e983d835c5ca3ac885ed21c: HOLD pending the endpoint-exclusion correction described in PUBLIC_AUDIT_REPORT.md. The exact maximum problem remains unresolved after five attempts.

This packet is separate from the 17-file author package and does not modify it. Python 3.10+ and its standard library suffice. Run the following with the path to the original frozen author package:

```text
python verify_readme.py /path/to/frozen/package
python independent_verify.py /path/to/frozen/package --full
python independent_conference.py
```

The first runner executes all four README commands in a temporary copy. The second independently checks every labeled graph through six and rechecks all sampled certificates. The third independently checks conference controls including Paley(9). Run without Python optimization flags. Results are written alongside the audit scripts. SHA256 manifest entries cover all supplied packet files except the manifest itself.

No source PDFs, extracted source text, private coordination, or publication credentials are included.
