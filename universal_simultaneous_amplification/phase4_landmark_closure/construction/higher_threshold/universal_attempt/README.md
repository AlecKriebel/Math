# Dense-entry / protected-state construction attempt

This folder studies whether a vanishing class of protected vertices can
improve the rare-mutant phase under both Bd and dB while a density-one dense
class supplies uniform initialization.

All claims are derived from the update rules.  Discovery computations are
labelled numerical and are not fixation proofs.

Files:

- `DENSE_PROTECTED_STATE_NO_GO.md`: exact collision-free dB cap and the
  universal negative second-order coefficient for every weak bounded gadget
  overlaid on complete support.
- `verify_dense_protected_state.py`: exact reconstruction and differentiation
  of the full `2^k-1` colony systems.
- `search_two_type_branching.py`: exact two-class branching equations and a
  numerical search over every reversible two-class mixing law.
- `search_dense_pair_households.py`: exact pair-colony limiting equations.
- `search_dense_gadget_colonies.py`: full bounded-gadget colony search.
- `check_finite_dense_pairs.py`, `check_complete_hessian.py`: finite numerical
  diagnostics only.
- `RESEARCH_LOG.md`: dated findings and status labels.
