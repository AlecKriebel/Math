# Sticky Cantor classification independent audit

The frozen report is accepted as a complete prior-literature resolution: sticky Cantor sets exist in R^n exactly for n>=4. The historical Sher theorem remains explicitly imported through inspected Frolkina. This is not a new discovery; the substantive approach count remains 0/5.

ACCEPTANCE_AUDIT.md contains the mathematical and source audit. INDEPENDENT_INTEGRITY.json records byte-level source, corpus, archive and correction-patch checks, with no source bodies. INDEPENDENT_RUNS.json and INDEPENDENT_RUNS_DRIVER_OO.json retain full checker outputs from the independent harness under ordinary and optimized execution. ACCEPTANCE.json is the machine-readable decision. AUDIT_MANIFEST.json pins every other audit payload file.

To reproduce the executable checks, supply the original frozen packet and a new, external output directory:

    python3 -B check_independent.py /path/to/frozen_packet /path/to/new_output

Run as UID 1000 with packet directory mode 0555 and files 0444. The harness never changes the input packet. It creates independent mutation fixtures in the external output directory; do not publish those fixtures. Only the authored audit, software and JSON receipts in this package are intended for publication. The original frozen packet is a separately pinned dependency and is not duplicated here.

The same harness supports -O and -OO. Its semantic mutations deliberately update checker pins before execution, ensuring mathematical rejection rather than hash-only rejection. Matrix tests provide independent finite checks of all 626 binary tree shapes through eight leaves. These computations do not prove the imported geometric topology theorems.
