The exact reviewed helper is UNFIT_FOR_EXECUTION because its opaque Git output
path violates the literal-stream retention contract. This is a source-level
implementation finding, not a defect in any scientific paper or staged page.

At release_three.py:483, subprocess.run captures literal stdout/stderr. At
line 484, stdout_base64 is set to null whenever opaque=True; only its SHA256 is
retained. At line 486, a nonzero result raises before returning the stdout buffer
to its caller. Thus an opaque failed command with nonempty stdout leaves no
recoverable literal stdout in TRACE, the journal or exception records. Likewise,
an opaque command that succeeds but is followed by a parser/validation failure
can lose the exact observed raw stream. Opaque callers include routing at lines
492–496, recursive tree listing at line 722 and TREE cat-file batch at line 834.
The final failure handlers retain the already-reduced event, not the omitted
buffer. PLAN.json's failure_contract requires retaining literal streams.

This deduction follows directly from the saved source; no failing command was
constructed or executed. The required correction is to durably retain the whole
actual stdout for EVERY opaque Git call, including successful calls, before any
later parsing or validation can fail. Retaining stdout only for a nonzero command
exit is insufficient. Root explicitly directed the new source author to retain
all such streams without size optimization. A newly authored source packet and
review are needed before execution can be considered. This audit neither changes
the original packet nor authorizes a fix to run.
