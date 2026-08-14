# Reproducibility guide

## Environment

The release uses Python 3 with `sympy`, `numpy`, and `scipy`, together with `pdflatex`, `bibtex8`, `pdfinfo`, and `sha256sum`. All central symbolic checks use exact rational or symbolic arithmetic. Numerical optimization and floating-point eigenvalues are used only to search for counterexamples and never to establish a retained theorem.

## Complete replay

From the Phase III root:

```bash
bash release/one_command_replay.sh 2>&1 | tee release/replay.log
```

The script performs the following gates in order:

1. verifies that the frozen STOP and T-ALG archives retain the inherited SHA-256 values;
2. compiles the independent Python sources and checks dependencies;
3. runs the independent unit and certificate-mutation suite;
4. reruns the complete bounded fixed-J census and 5,000 random rational matrices using two disjoint seeds;
5. reruns the conservation, Boolean-selector, row-realization, PARTITION-reduction, fixed-species, and designated-mobile falsifiers;
6. checks the compact external-audit YES and NO reduction examples;
7. rebuilds the journal manuscript, supplement, two-page theorem summary, and five-page proof skeleton;
8. checks PDF page counts and unresolved LaTeX references;
9. audits the mandatory Phase III tree;
10. writes `release/sha256_manifest.txt`.

## Independent implementation boundary

Code under `independent_verifier/` does not import the inherited T-ALG implementation. It reconstructs reaction matrices, direct mass-action differentiation, the open-cube and row-splitting reduction, fixed-species circuit projection, and certificate checks from definitions. The frozen inherited replay is retained only as a separate regression record in `release/inherited_replay.log`.

## Exact versus numerical evidence

Exact gates include determinant identities, Routh-Hurwitz determinants, circuit enumeration, rational cone decomposition, mass-action flux-image equality, symbolic characteristic-polynomial comparison, and certificate mutation. The numerical global searches in the reduction falsifier are adversarial only; the proof of the NO direction is the exact determinant-continuity and cube-gap argument.

## What the release does not implement

The abstract decision theorem invokes fixed-variable real-algebraic decision and Real Nullstellensatz completeness. The release does not vendor a complete general cylindrical algebraic decomposition engine or a practical arbitrary-instance Nullstellensatz certificate generator. A raw network without a supplied exact certificate may therefore remain unresolved in software without weakening the theoretical decidability theorem.

## Frozen-input integrity

Expected archive hashes:

```text
ea8c640f199549710ac1e8de0b896300adfa9be0bdde64753d06b7ada94a5f10  qbio_mass_action_turing_topology_TALG.zip
dd9be02c8e530b0f603d92029b15cc3fdb2443aa188fa1b41ff8e0d31c60a828  qbio_mass_action_turing_topology.zip
```
