# Editorial and executable provenance

RESEARCH.md differs only by a local source-gate link and removal of an operational no-publication sentence. SOURCE_STATUS_GATE.md omits nonmathematical source-handling details; its mathematical content and public citations are preserved. The independent mathematical audit and recorded exact output are preserved. The original authored verifier is included for reproducible comparison, not used as the acceptance runner because Python optimization removes assertions.

verify_exact.py is the complete AST-preserving assertion-to-explicit-guard conversion documented in CONVERSION_PROVENANCE.json. The original verifier hash identifies only the included authored code. Additional finite regression checks exercise assumptions, inverse identities, degree-drop/Mahler distinctions, and relative-norm inequalities. They are not substitutes for the all-n proofs and do not establish global unit optimality.

The field norm is N_{L/Q}(alpha)=-1, not its absolute value. Saturation concerns only the rank-one subgroup modulo torsion; no full saturated system is computed.

The per-command replay files were mechanically consolidated into REPLAY_RESULTS.json without dropping commands, output characters, exit codes, or modes. Traceback paths use a documented PACKAGE prefix rather than a machine-specific directory. verify_replay.py validates the complete outputs, not only a success marker. Mathematical scripts and proof claims are unchanged by this consolidation.
