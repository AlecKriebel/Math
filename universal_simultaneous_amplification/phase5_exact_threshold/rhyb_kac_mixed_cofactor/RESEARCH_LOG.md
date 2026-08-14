# Research log: Kac mixed-cofactor feedback

All times are America/Los_Angeles.  No graph enumeration, ansatz search,
literature search, or external communication was used.

## 2026-08-13 18:06 PDT -- exact Poisson gauge and master feedback obstruction

- Proved the determinant-one rank-one Poisson identity
  `det(L+g e_i^T)=det(L+psi_i e_i e_i^T)=T_Q(g)`.  Unlike a positive-part
  replacement, the right column gauge retains the full signed reward
  exactly.
- Built one bordered matrix whose determinant is precisely
  `tau_B(i)tau_D(i)-r^3 T_B(g)T_D(g)`.
- Applied the two Poisson gauges inside the bordered matrix.  On the active
  branch a block signature produces a `Z`-matrix whose only unresolved
  diagonal block is
  `[[1,-r^3 psi_Bi],[-psi_Di,1]]`.
- Proved that the bordered `Z`-matrix is an `M`-matrix if and only if the
  desired one-root Kac inequality already holds.  Thus generic
  Hadamard--Fischer or `M`-matrix principal-minor positivity is circular;
  the conjecture is literally the final two-by-two principal minor.
- Audited the classical mixed-discriminant route: before gauge, the
  directed Laplacian is generally nonsymmetric and the density mark is
  indefinite, outside the Alexandrov--Fenchel cone.  The right Poisson
  gauge is not a positive congruence.
- Proved on a two-state Laplacian with the actual order-three
  singleton/doubleton density marks that the Poisson gauge preserves the
  linear determinant coefficient but changes the quadratic coefficient.
  Hence it cannot be inserted into a stable-polynomial coefficient proof.
- Scope: this closes only the canonical AF/Hadamard--Fischer/generic
  `M`-matrix/stable-polynomial architecture.  It does not refute a new
  cross-rule paired-forest identity or a physical supersolution for the
  feedback matrix.  The diagonal Kac inequality and universal minimal
  product remain open.
