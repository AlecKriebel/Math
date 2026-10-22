# Independent audit of ID 30001223

Read mathematical_audit.md for the accepted mathematical verdict, direct convention bridge and scope limits. The author freeze was not modified.

Run the independent support:

    python -B audit_gate.py
    python -O -B audit_gate.py

Run python -B test_gate.py to replay the audit package's own 28 normal/optimized/mutation controls on temporary copies.

The gate checks this directory's complete regular-file inventory and hashes before executing the independent checker. A __pycache__ directory or other added entry is rejected. External archive hashes authenticate the frozen package; the internal manifest alone does not.

To rerun all 34 independent acceptance/mutation tests on the supplied author freeze:

    python -B replay_author.py /path/to/YOUNG_TOPS_30001223_AUTHOR_SAFE_FREEZE.zip

Only authored mathematical analysis, code, results and public verification metadata are included. No copied source PDF, extract, dataset contents, private coordination file, or third-party private data is included.
