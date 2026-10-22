# Bounded exact verification

Command executed successfully on 2026-10-05:

    python3 verify.py --sp4 --output verification_results.json

All arithmetic deciding membership is exact integer or rational arithmetic. The only parameter values used for matrix enumeration are prime fields 3,5,7. The coefficient/valuation controls can use prime powers without constructing those fields, because their proven torus-order formulas depend only on q.

## Exhaustive matrix checks

- GL_2(3): 48 matrices, 12 qualifying, proportion 1/4; SL_2(3) has 24 matrices and none qualifying.
- GL_2(5): 480 matrices, 150 qualifying, proportion 5/16; SL_2(5) has 120 matrices and none qualifying.
- GL_2(7): 2016 matrices, 504 qualifying, proportion 1/4; SL_2(7) has 336 matrices and none qualifying.
- GL_3(3): 11,232 matrices, 5,265 qualifying, proportion 15/32; SL_3(3) has 5,616 matrices and 3,159 qualifying.
- Sp_4(3): 51,840 matrices, 17,010 qualifying, proportion 21/64.

The GL enumerator visits every q^(N^2) candidate matrix, tests its determinant, and verifies that the invertible total equals product_(i=0)^(N-1)(q^N-q^i). Each element order is computed by exact repeated powering and prime stripping from that known group order. The powered involution's fixed-space dimension is N-rank(t-I), with exact Gaussian elimination modulo q. The strict upper interval endpoint is tested as 3k<2N.

The Sp_4 enumerator lists each symplectic basis exactly once in column order (v1,v2,w1,w2), for the standard alternating form <v,w>=v1*w3+v2*w4-v3*w1-v4*w2. There are (q^4-1) choices of v1, q^3 of w1 with pairing 1, q^2-1 nonzero vectors v2 in their two-dimensional perpendicular complement, and q choices of w2 in that complement with pairing 1. Hence there are exactly q^4(q^2-1)(q^4-1) bases, matching the group order. Distinct ordered bases give distinct matrices. Each counted matrix is tested by the same order and fixed-space routines. The signed torus coefficient model is a separate computation and agrees exactly.

The order routine additionally verifies A^|G|=I for every enumerated matrix. Source code retains all algorithms. Outputs retain counts and stream hashes, not a list of group elements.

## Further exact controls

- 198 GL/U/Sp coefficient cases: q in {3,5,7,9,13,17}, model size 2 through 12.
- 3,136 valuation cases: each odd q from 3 to 99 and each d from 1 to 64, checking both q^d-1 and q^d+1 against the case formulas.
- 294 fractional-avoidance coefficient/product identities: L in {2,4,8}, rho in {1/2,1/4}, and degree 0 through 48.
- Endpoint negative control: diag(1,-1,-1) in GL_3(3) qualifies and its negative does not. Replacing the upper strict inequality by a weak inequality changes this result.
- Field-valuation negative control: GL_2(3) and GL_2(5) have different proportions, so replacing full two-adic order by parity loses information.
- Special/general negative control: all enumerated SL_2 groups have zero qualifying elements while GL_2 does not.

Finite controls neither establish the asymptotic bounds nor cover larger finite groups. The infinite proof is in PROOF.md and depends on the explicitly credited published torus-counting theorem. The controls check the event definition, finite counting models, and their implementation.
