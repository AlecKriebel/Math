# Research log: root-killing cross-rule determinant

## 2026-08-13 -- exact common phase block and Hermitian obstruction

- Expressed every stationary root moment as the first derivative at zero of
  `det(-Q+sW)`.
- Lifted the target-locked dB event Laplacian and the adjoint `L` Laplacian
  to two phase blocks with exactly the same off-diagonal marked-arrow
  coupling `(-mathcal C/2,-J)`.
- Proved the exact determinant identities

  ```text
  det B_D(s;W)=det(A)*det(I-K_D+sW),
  det B_L(s;W)=det(-Q_L+sW)/(2^|Y| det K).
  ```

- Recast `PAPT_n` as the coefficient of `s^2` in the difference of two
  block-diagonal determinant pencils.  This is equivalent to the true
  product target, not a sufficient strengthening.
- Exactified the first canonical PSD route as false.  The common top-block
  difference `(I-S)/2` has a negative `2 by 2` symmetric minor in every
  positive diagonal metric.  On `K_4` the Euclidean determinant is
  `-1/144`.
- The lower adjoint potential is also unordered: `V` ranges from `-2` to
  `2` on the weighted three-path and from `-10115/255783` to its negative on
  the frozen four-vertex orientation witness.
- The exact common-coupling blocks are not `Z`-matrices and cannot be made
  so by a diagonal signature.  For every marked `y=(A,v)`, the shared
  top-right entry at `A` is positive while the reverse `-J` entry is
  negative.  Thus ordinary nonsymmetric `M`-matrix Hadamard--Fischer cannot
  be applied directly either; it would require a larger master block.
- Built the canonical four-sector principal-minor master by duplicating the
  endpoint of the shared selective arrow into locked-return and
  target-forgetting copies.  Its two relevant principal blocks reduce
  exactly to the untransformed dB and `L/C` phase matrices.  However, on
  unweighted `K_3` at bottom block `B=I`, its determinant is `-27/2048`.
  Hence it is not an `M`-matrix and ordinary Hadamard--Fischer still cannot
  start; the union block overcounts the duplicated selective mass.
- **PROVED:** the exact root-killing and common phase-block identities.
- **REFUTED:** a direct Hermitian Loewner/Schur/Hadamard--Fischer proof and
  the direct common-block or duplicated-phase-master `M`-matrix shortcuts.
- **OPEN:** a genuinely nonsymmetric `M`-matrix/forest proof of the exact
  block coefficient, equivalently `PAPT_n`.
