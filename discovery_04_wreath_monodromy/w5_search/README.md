# Level-five primitive-branch certificate

This directory certifies the next finite case of the all-iterate
wreath-product problem:
\[
\operatorname{Mon}_{\mathbb C}(F^{\circ5})=W_5.
\]

The calculation is not used by the banked \(W_2,W_3,W_4\) theorems.  It
evaluates
\[
N_4(s)=\operatorname{Norm}\bigl(\Delta(X_4)\bigr)
\]
along the target line \((1,2,s)\), where \(X_4\) is the fourth successive
inverse point.  At \(p=23,s=3\), the deepest norm has a simple zero, while
every lower discriminant, leading coefficient, and reconstruction guard is a
unit.  This gives a single transposition in one of the deepest three-leaf
blocks.  Together with the proved \(243\)-cycle and the \(W_4\) quotient, the
kernel lemma gives \(W_5\).

`finite_field_norm_depth4.py` reuses only the audited cubic-algebra
arithmetic from `../w4_search/finite_field_norm.py`; the tower construction
itself is a new depth-agnostic loop.  It is sequential and bounded-memory.
The largest algebra at depth four has dimension \(81\).

`RESULT.md` gives the certificate and proof.  `test_depth4_evaluator.py` and
`verify_w5_modular.py` give the primary exact replay.  The separate
`audit_w5_hostile/` package reconstructs the rank-\(81\) tower with regular
representation matrices, replays the localization and group steps, and
fault-tests twelve independent assertions.  This work is not peer reviewed,
and a finite number of full-wreath levels does not prove the all-iterate
statement.
