# Lalonde exact algebraic verifier

The separate graph and classical-coloring checker runs with

```sh
python3 verification/verify_graph.py
```

It verifies the graph6 checksum, edge counts, exhaustive triangle list,
absence of a $K_4$, Lalonde Section 4.2's published four-coloring, and exact
non-three-colorability by transparent exhaustive backtracking.  The search
fixes the colors on triangle `1,2,3` only up to color-name symmetry and then
tries every locally feasible branch.

Run the commands without Python's `-O` optimization flag. The graph checker
and short paper-form verifier reject optimized mode explicitly because their
exact checks use executable assertions; they never print `PASS` after those
checks have been stripped.

From the project root, run

```sh
python3 verification/verify_lalonde_uniform_obstruction.py \
  certificate/lalonde_uniform_obstruction.json
```

The certificate argument may be omitted; that project-relative certificate is
the verifier's default.

A shorter, independent replay of the four-factor SOS presented verbatim in
the paper is also available:

```sh
python3 verification/verify_obstruction_certificate.py
```

It reads `certificate/obstruction_certificate.json` and checks the rational
free-algebra expansion, graph-neighbor signs, six formal tail compressions,
complex-structure intertwining products, and terminal dimension
coefficients. The longer verifier below uses a distinct
trace-SOS formulation and additionally decodes graph6, checks the clique ideal
witness, and row-reduces the cross-color kernel.

The checker uses only the Python standard library.  Every coefficient is a
`fractions.Fraction`; the free block labels are never assigned numerical
matrices.

## What is independently replayed

1. The graph6 string is decoded without NetworkX and compared to the JSON
   edge list.  The checker enumerates all triangles and verifies that the four
   declared base triangles are exhaustive.
2. The 24-fold color symmetrization arithmetic is checked: dimension `24d`,
   common rank `6d`, and fixed-color corner dimension `3r`.  The clique-column
   identities follow from four mutually orthogonal rank-`r` projections in
   dimension `4r`.
3. In the exact commutative polynomial ring `Q[n,f,d]`, where the formal
   symbol `f` denotes `(n-1)!`, the recurrence `n!=n*f` is replayed to prove
   symbolically (not by sampling values of `n`)

       r=(n-1)!d,  D=n!d=nr,
       D-(n-3)r=3r,  and  3nr<=2nr.

   The last inequality has positive gap `nr` for `n>=3`, `r>0`.
4. In the free noncommutative algebra on self-adjoint projection symbols
   `u1,...,u13`, the checker constructs

       F_j = S_j - (3/2)(1_Q-u_j),  j=10,11,12,13.

   Projection, edge-annihilation, cyclic-trace, uniform-rank, and triangle
   partition relations are applied exactly.  It obtains

       Tr sum_j F_j^* F_j = 2 Tr(T)-6r.

   A noncommutative ideal witness supplied by the certificate replaces the
   three binary factors in `T` by `1_Q-u3`, `1_Q-u2`, `1_Q-u1`.  Base-triangle
   orthogonality then gives `Tr(T)=3r`, so the SOS has trace zero.
5. The four Walsh sign rows `(---),(-++),(+-+),(++-)`, their rank-three left
   inverse, and every free-polynomial expansion leading to
   `A={B,C}`, `B={A,C}`, `C={A,B}` are checked.
6. From the scalar core sign vectors at vertices 1--9, rational row reduction
   proves that same-vertex cross-color orthogonality has exactly the kernel

       [[0,X,Y],[-X,0,Z],[-Y,-Z,0]].

   In particular, there are no adjoints in the lower triangular entries.
7. For the six tail embedding matrices, direct multiplication over the free
   block algebra checks

       Omega_Y, Omega_Z, -Omega_X,
       Omega_(Y+Z), Omega_(Y-X), Omega_(Z-X).

   It also checks the exact inverse coefficient transform, `J^2=-I`, and
   `J Omega_K=Omega_K J=diag(-K,-K)`.
8. The terminal coefficient contradiction is checked as `12r <= 8r` for
   `r>0`.

## Transparent semantic bridges

This is an exact algebraic replay tool, not a foundational proof assistant.
It invokes three elementary finite-dimensional facts explicitly used in the
paper:

- orthogonal projections whose ranks sum to the ambient dimension sum to the
  identity;
- matrix trace is faithful on positive semidefinite matrices, so trace zero of
  a sum of Hermitian squares makes every square factor zero;
- pairwise orthogonal subspaces have total dimension at most the ambient
  dimension.

The tail-plane classification and the implication from the checked
compressions to the stated subspace inclusions remain human-readable linear
algebra in the proof.  The potentially error-prone coefficients, signs,
orientations, and noncommutative expansions are what this verifier targets.

## Expected successful output

The final line is

```text
ALL EXACT CERTIFICATE CHECKS PASSED
```

The verifier prints the certificate's SHA-256 digest at runtime so a run can
be tied to the exact machine-readable input.
