# Closed-leaf genus-minimality formulation audit

Read REPORT.md first, then PROOF.md. The central scope limitation is essential: the Hopf-product counterexample satisfies the weaker differential condition printed in K3 but fails the globally closed-positive-form condition in Kronheimer's original question.

Run the standard-library checker:

    python check.py
    python -O check.py
    python check.py --self-test
    python -O check.py --self-test

To verify authorized local copies of the three input datasets as well, supply all three explicit paths:

    python check.py --catalog PATH --problems PATH --reports PATH

The dataset option emits hashes and match results, never source records or dataset contents. Missing, changed, duplicated, mismatched, or partially specified inputs are errors. Review PROOF.md separately: exact algebra checks do not mechanize its topology.

The safe archive contains authored analysis, verification code, and public verification metadata only. Source PDFs, source text extractions, dataset records, private working material, and correspondence are excluded.
