# Narrow verifier correction

The original freeze is preserved under manifest SHA-256 `9e290bec9d6ba40ec3a61a1c41b9e70381f75c3ab80db6e2a4ef55f83d3aa751`.

The separate candidate has manifest SHA-256 `daaf2d88de9272733ea1d674396ec2236cfe250d4796dc922e841890ff087b69`.

Changes:

1. Replace 23 `assert` statements in `check_math.py` with calls to an explicit `require` function that raises `ValueError` on failure.
2. Replace 6 `assert` statements in `verify_packet.py` the same way.
3. Re-pin the two changed scripts in the candidate manifest and identify the original manifest it supersedes.

The actual unified patch is `OPTIMIZATION_FIX.patch`. Every other original file is byte-identical, including the complete report and its saved exact-check results. The corrected scripts contain no Assert AST node.

This corrects Python optimization behavior only. It does not add mathematical claims, proof searches, source downloads, JSON-schema validation, or security hardening against a malicious replacement manifest. The packet verifier checks consistency against its local manifest. For artifact identity, first compare the manifest to the separate known SHA-256 pin. Anyone able to rewrite both content and that local manifest can otherwise create a new internally consistent packet.

Python dictionary equality identifies JSON true with integer 1. This minimal correction deliberately retains that original equality behavior; the audit demonstrates it and makes no exact-type promise. Standard `json.loads` also allows nonfinite number tokens. The audit's NaN-in-results mutation is rejected because its result differs, not because the parser is strict.

Reproduce the full read-only UID-1000 control suite with:

`python reproduce_audit.py ORIGINAL_PACKET CORRECTED_PACKET OUTPUT_JSON`

Run this outside either input packet. It uses temporary permission-read-only copies, verifies both external manifest pins, records actual runtime identity/optimization, runs the baseline and negative controls, and confirms the input packets are unchanged. No sources or network are required.
