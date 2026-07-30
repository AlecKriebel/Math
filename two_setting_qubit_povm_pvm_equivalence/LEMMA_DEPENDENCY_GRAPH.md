# Lemma dependency graph

## Frozen dependencies

- **D1** — exact rational \(3\times2\) separation.
- **D2** — one-binary-party two-input simulation theorem.
- **D3** — residual architecture reduction to pure entangled \((2,3)\)-by-\((2,3)\), with one binary PVM and one genuine ternary rank-one POVM per party.

## Closure dependencies

```text
Lorentz determinant identity
        │
        ├── Local metric normal form (L4)
        │       ├── strict off-diagonal inequalities
        │       └── metric tangent/null-ray map Φ (L8)
        │
        ├── Pure-state conformal Lorentz relation (L5)
        │       ├── P invertible
        │       └── incidence equations F_j=0 (L6)
        │               ├── local physical completeness (L6.1)
        │               ├── incidence smoothness/dimension 14 (L6.2)
        │               └── Lagrange multiplier system
        │
Finite POVM duality (L7.1)
        ├── nonnegative determinant multipliers
        ├── zero-slack deterministic/PVM tie (L7.2)
        └── strict separator ⇒ λ_j>0 ⇒ Λ>0

Incidence differential + λ>0
        │
        ├── weighted Hessian square completion (L9)
        ├── ambient inertia q=(4,12)
        ├── W-space tangent solvability
        └── rank(D)≥2 ⇒ positive second direction (L10)

Quadratic map Φ
        │
        ├── five-point base locus (L11.1)
        ├── rational generic inverse (L11.2)
        ├── four exceptional-fiber resultants (L11.3)
        └── rank(D)=1 ⇒ no strictly positive λ (L12)

rank(D)=0
        │
        ├── transformed pentad permutes base rays
        ├── partition-preserving equal scaling
        ├── bounded three-node flow (L13.1)
        └── explicit deterministic/PVM mixture (L13)

L10 + L12 + L13
        │
        └── no strict residual separator (L14)
                │
                ├── convex nearest-point criterion (L2)
                ├── residual reduction D3
                └── universal two-setting equality
                        │
                        ├── D1
                        └── minimum setting architecture = 3×2
```

## Logical role of D2

D2 remains part of the architecture reduction inherited as D3. The closure proof itself also contains a smaller direct fact: replacing one local input by a deterministic measurement leaves only one nontrivial input on that party, and every such nonsignaling behavior is local.

## Verification coverage

- Algebraic identities in L4, L5, L8, L9, L11, and L13 are checked by `verify_exact.py`.
- The rank-zero constructive mixture is independently generated and checked by `rank_zero_simulator.py`.
- Convexity, duality, dimension, and inertia steps are finite-dimensional human-readable proofs in the dossier.
