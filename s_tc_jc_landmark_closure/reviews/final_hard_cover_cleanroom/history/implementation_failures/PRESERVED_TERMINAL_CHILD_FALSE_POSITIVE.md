# Preserved terminal-child reviewer false positive

Status: **REVIEW IMPLEMENTATION FAILURE; CORRECTED BEFORE USE**

The first schema-3 path replay reported 822 child-set mismatches because the
clean-room reviewer regenerated restoration children for every state with an
unused target dummy.  That is wrong after a path has already terminated with
an exact polynomial separator: terminal states correctly have no children,
even when an unneeded dummy remains.

The failed certificate is preserved as
`schema3_n4_theta2_path_audit_before_terminal_fix.json`.  The correction makes
independent child regeneration conditional on
`terminal_classification == "refined_by_next_restoration"`.  No conclusion
about the primary stream is drawn from the failed reviewer run.

