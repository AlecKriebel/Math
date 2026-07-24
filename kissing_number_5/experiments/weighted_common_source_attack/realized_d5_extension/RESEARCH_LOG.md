# Research log — realized extensions of the 12-point weighted D5 support

## 2026-07-24

- Started a new isolated branch of the weighted-common-source program.
- Frozen input from the preceding projection-membership checkpoint: a scalar
  profile \(h\in\mathbb R^{12}\) is geometrically realized exactly when
  \[
  h^{\mathsf T}Ph=\frac15,\qquad
  h^{\mathsf T}PSPh=\frac1{25}.
  \]
  For two realized profiles, their corresponding unit vectors have inner
  product \(5h^{\mathsf T}Pk\).
- Specialized to the exact 12-point support in `support.py`.  In the scaled
  coordinate \(z=\sqrt2\,y\), the extension region is
  \[
  \|z\|^2=2,\qquad r_i\cdot z\le1\quad(1\le i\le12),
  \]
  and two extensions are compatible exactly when \(z\cdot w\le1\).
- The two objectives in this checkpoint are deliberately independent:
  derive universal exact aggregate inequalities, and search continuously for
  a 29-point extension code that would refute the hoped-for bound \(m\le28\).
