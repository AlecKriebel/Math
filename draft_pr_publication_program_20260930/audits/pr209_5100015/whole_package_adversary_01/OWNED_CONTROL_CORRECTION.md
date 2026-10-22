# Owned control correction

UTC: 2026-10-17T01:33:05.491785+00:00

Initial run exited 1 at line 53, the exact period-four string-value assertion, before numerical diagnostics. Inspection identified ordinary Python integer zeros entering /4 and causing floating-point zeros in a nominally exact SymPy calculation. This can render the exact value as a decimal string. The initial source is retained in owned_controls_initial_failed.py; it is failed audit evidence, not theorem evidence. The repaired source sympifies every input coordinate before exact arithmetic. It will be rerun in full. No source package bytes changed.
