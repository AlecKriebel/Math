# Execution chronology and repeat-count clarification

This addendum is separate from the sealed independent findings and does not change their mathematical or computational conclusions.

The primary retained suite inventories contain 4 baseline runs, 30 supplied-script mutation runs, and 26 runs of the expanded exact-control suite: 60 distinct retained command/configuration outcomes. The exact-control mechanism was first executed on 9 models in two modes (18 runs); four additional boundary/positive-control models were then added, and all 13 models were rerun in two modes (26 runs). Thus there were 78 actual scientific process executions including the 18 repetitions, not merely 60 process executions. The sealed report's 26 exact-control executions describes the final expanded suite.

The first exact-control aggregate JSON was overwritten by the expanded suite; the repeated input models, checker, commands, stdout, and stderr are unchanged and preserved. The initial tool transcript preserves all 18 initial outcomes. execution_evidence/initial_exact_suite_reconstruction.json transparently reconstructs that phase from these facts and labels the missing original aggregate timestamp; it is not represented as an original contemporaneous receipt. initial_exact_harness_reconstructed.py preserves the first harness code by reversing the sole additive patch. No failed case or pilot was concealed. Every intentional rejection from that phase remains in the final suite with its exact failing reason.

This chronology detail was noticed during preservation handoff after the final independent seal. Future reruns should use fresh copied folders, as the README already states, to keep every phase receipt separately.
