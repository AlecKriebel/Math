# Literal preliminary failures, not scientific-run results

After INITIAL, two raw-primary directory lookups accidentally used Math-relative paths from the owned review working directory (tool878b28). Literal outputs were:

    find: draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_02/phase3: No such file or directory
    find: draft_pr_descending_audit_20261002/audits/pr329_20000450/preprint_review_01/evidence/primary_provenance: No such file or directory

The combined cell later read SOURCE_REFERENCES.json and exited0; individual find statuses were not captured. Corrected absolute-path read-only inventories located the existing raw bodies. No acquisition, source execution or mutation followed from these errors.

The single default Python availability probe in tool5b10b8 was:

    command -v python3
    python3 -c 'import sys, sympy; print(sys.executable); print(sys.version.split()[0]); print(sympy.__version__)'

The path was /opt/homebrew/bin/python3. Its literal error was:

    Traceback (most recent call last):
      File "<string>", line 1, in <module>
        import sys, sympy; print(sys.executable); print(sys.version.split()[0]); print(sympy.__version__)
        ^^^^^^^^^^^^^^^^^
    ModuleNotFoundError: No module named 'sympy'

The combined cell ended with a date command and its overall exit was0; the failed probe's individual exit was not separately captured. This document transcribes the observed tool stream and does not invent a standalone receipt. No native scientific route had run at this point. Root then supplied only the known existing /opt/homebrew/bin/python3.11 path and authorized one bounded availability check. No install, environment mutation or environment-search campaign is authorized.

Verdure's scanned primary PDF text extraction exited0 with empty stderr but produced only18 form-feed characters. It is retained literally as primary/verdure.txt, not treated as body reading. The original title page and printed80-88 were freshly rendered into owned primary images and personally read instead.
