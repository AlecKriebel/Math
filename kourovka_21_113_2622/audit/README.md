# Reproducing the independent audit controls

Run from this directory:

    python independent_controls.py
    python extra_controls.py

The independent controls require SymPy. They were rerun with Python 3.12.14 and SymPy 1.14.0; requirements.txt pins that version. These scripts import neither author checker. The extra controls import independent_controls.py, which reruns the first suite before the additional checks. Each script writes its corresponding JSON output beside itself. Compare the outputs to the committed JSON files.

The full mathematical audit is in AUDIT_REPORT.md. Only its local checkpoint/receipt bookkeeping sentence and directory-location wording were sanitized for publication. No mathematical verdict, criticism, condition, verification result, or limitation was removed. Original report SHA-256: 740c98e64ef9889a0935e5d666bfa9b71c03ea730d3012e483ad029f860da276.
