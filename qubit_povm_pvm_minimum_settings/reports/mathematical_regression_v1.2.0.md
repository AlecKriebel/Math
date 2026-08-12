# Mathematical regression check — version 1.2.0

**Compared against:** Git tag
`qubit-povm-pvm-minimum-settings-v1.1.0` at
`773356a1de85290c3e85a361e0019f5f82b8e6d9`

**Checked:** 11 August 2026

## Result

**PASS — no pre-existing theorem, proof, formula, or exact artifact changed.**

A new contextual remark notes that the independent Zhu--Chen--Wang witness
could also supply the existence half of the minimum-setting corollary. It does
not alter the corollary, any dependency, or any mathematical bound.

- All 21 `maintheorem`, `theorem`, `lemma`, `proposition`, and `corollary`
  environments in `paper/main.tex` are byte-identical after extraction.
- Extracted theorem-block SHA-256 in both versions:
  `4c4e66da9a8e699bc4e48b02e7804e32bde010a614e33fbc4627c3465939758d`.
- `paper/appendices.tex` is byte-identical to version 1.1.0.
- Every file under `artifacts/` is byte-identical to version 1.1.0.
- The Bell functional, simple and strengthened strategies, values `L0` and
  `L1`, global PVM upper bound `U`, and both exact gaps were rechecked by the
  unchanged exact verifier.
- The manuscript changes outside numbered results are title-page metadata,
  abstract and contribution order, literature comparison, an explicitly
  non-load-bearing contemporaneous-work remark, discussion, availability,
  and disclosure text.

The inserted remark says that the independent ZCW separator can replace the
present separator only for the existence half of the minimum-setting
corollary. It does not enter or modify the proof of universal two-input
equality.
