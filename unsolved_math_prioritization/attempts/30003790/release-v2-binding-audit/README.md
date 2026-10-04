# Corrected release binding audit

Read ACCEPTANCE.md for the supplemental PASS and its exact scope. This directory is separate from the frozen release and does not modify it. MANIFEST.json binds these supplemental files and identifies the accepted release manifest.

To replay the portable read-only assembly check:

    python3 verification/verify_binding.py /path/to/rank618-30003790-release-v2

The output should match verification/result.json under the same Python environment. Python's standard library is sufficient. A relocated copy was also tested successfully.

This closes the corrected assembly's pending binding review only. It does not authorize publication or expand any mathematical conclusion.
