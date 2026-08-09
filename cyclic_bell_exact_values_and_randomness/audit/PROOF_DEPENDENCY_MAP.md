# Proof dependency map

Audit date: 2026-08-08

This map separates analytic dependencies from regression artifacts.  A script can catch a normalization, phase, or indexing error; it does not establish an all-dimensional or commuting-operator theorem.

## A. Exact value and first augmentation

```text
CBR-004 scalar extremum and exact scalar equality set
                    |
                    v
continuous functional calculus for U=A0^* A1
                    |
                    +----------------------+
                    |                      |
                    v                      v
CBR-003 polar identity             F_d(U) <= M_d I
  (canonical partial isometry;            |
   kernels retained)                      |
                    \                      /
                     v                    v
                CBR-005 operator inequality I_d <= M_d I
                                      |
                     CBR-008 finite order-d attaining strategy
                                      |
                                      v
                        beta_q = beta_qa = beta_qc = M_d
                                      |
                  Re(A0 B_d) <= I + aligned attainment
                                      |
                                      v
                         CBR-007 augmented value M_d+1
```

The \(q_c\) conclusion is analytic: CBR-003 works in commuting von Neumann algebras on an arbitrary Hilbert space, and continuous functional calculus is applied inside \(W^*(A_0,A_1)\).  Finite direct sums of tensor-product blocks are only regression cases and do not approximate or enumerate all commuting representations.

The equality layers must not be conflated:

1. CBR-004 exactly classifies the **scalar** equality set \(z^d=(-1)^{d-1}\).
2. At the operator level, spectral calculus yields \(F_d(U)=M_dI\iff U^d=(-1)^{d-1}I\).
3. On a single maximizing vector, the global certificate yields only \(P_y\psi=0\), \(G\psi=0\), and \(GA_0^\dagger\psi=0\).
4. None of these statements classifies the full maximizing face of behaviors or all supported representations.

## B. Conditional phase permutations and first-family bias

```text
CBR-003 polar identity
       + maximizing scalar labels z_j
       + product_j z_j = 1
       + exact polar phases s_{rj}
       + product_j s_{rj} = 1
       + weighted-cycle identity
                         |
                         v
        CBR-009 conditional phase-permutation theorem
                         |
      cyclic root/product identities (CBR-010)
                         |
                         +----------------------+
                         |                      |
                         v                      v
          exact score and first harmonics     weighted-shift diagonalization
                                                |
                                                v
                                       CBR-011 target-table formula
                                                |
                        final-two-swap lag-two autocorrelation R_2 != 0
                                                |
                                                v
                                      CBR-012 nonuniform maximizer
                                                |
                                                v
                                      CBR-016 guessing lower bound
```

CBR-009 is sufficient, not necessary.  The product conditions are load-bearing because they enforce the order-\(d\) relations.  A random permutation is admissible only after the underlying labeled data satisfy those conditions.  The theorem constructs a permutation orbit inside a maximizing face; it does not describe all maximizers.

## C. Second augmented family

```text
Fourier orthogonality of Bob observables
 + exact coefficient norm sum_l |lambda_l|^2=1
 + cross-party commutation
                         |
                         v
              CBR-014 complete SOS upper bound
                         |
exact geometric sum S_l=d lambda_l r_l
 + weighted-cycle order-d parity
 + A_l=conjugate(D_l)
                         |
                         v
              CBR-015 annihilation of every SOS factor
                         |
                         v
           exact values d and d+1 in q, qa, and qc
                         |
  A_1 has the same weighted cycle as in CBR-011/012
                         |
                         v
       same nonuniform target table and guessing gap
```

Global optimality comes from the complete SOS identity CBR-014.  Merely observing that a candidate kills selected residuals would not prove an upper bound.  The \(d=4\) exact expansion checks coefficients, conjugations, Fourier orientation, and the factor \(1/(2d)\); the all-dimensional proof is the displayed symbolic derivation.

## D. Randomness interpretation

```text
CBR-011 nonuniform target behavior
 + exact maximization CBR-012 / CBR-015
 + trivial Eve: G >= max_{a,b} p(a,b)
                         |
                         v
              CBR-016 value-conditioned lower bound
                         |
zero-deficit strategy is feasible whenever deficit <= epsilon
                         |
                         v
              CBR-017 endpoint-robustness obstruction
```

The path uses only the scalar score constraint.  A full-behavior program fixes higher Fourier correlators and can exclude the permuted behavior; therefore CBR-018 is a logical boundary, not a caveat that can be dropped.

## E. Setting-complexity results

```text
nonsignalling + one Alice input
 -> explicit local conditional-product model
 -> coherent finite flag purification and grouped PVMs
 -> CBR-019 perfect guessing

specific Fourier-phase ideal tables
 -> exact geometric overlap
 -> CBR-020 and CBR-021 (specific-strategy obstructions)

two circulant operator-system decomposition
 -> computational eigenvector equations
 -> corner block [0 0 T; 0 0 0; T* 0 0]
 -> paired +/- singular-value spectrum
 -> CBR-022 (coefficientwise spectral route only)
```

CBR-019 is universal.  CBR-020--022 are intentionally scoped and do not combine into a general \((2,3,d,d)\) no-go theorem.

## F. Analytic proof versus computational evidence

| Claim group | What proves it | What tests contribute |
|---|---|---|
| CBR-003--008 | Polar algebra, scalar trigonometry, functional calculus, explicit Weyl strategy | Detect adjoint, phase, kernel, and normalization mistakes in finite matrices |
| CBR-009--012 | Product identities, weighted cycles, trace identity, Fourier analysis | Exercise canonical, reversed, random, prime, composite, and deliberately inadmissible cases |
| CBR-013--015 | Exact cyclotomic arithmetic plus complete SOS/geometric-sum proof | Independent \(d=4\) coefficient and projector replay |
| CBR-019 | Explicit hidden-variable and purification construction | Exact-rational hostile enumeration in small dimensions/settings |
| CBR-020--022 | Exact overlap and linear-algebra arguments | Formula and nullspace regressions through finite \(d\) |

No finite test is cited as establishing \(q_c\), an all-dimensional identity, the exact scalar equality set, or a complete maximizing-face classification.
