# Attempt 5: bounded exact extension search

## Search target and limits

The final approach searches the local extension data for a contradiction and verifies the induced-model calculation independently by exact character arithmetic. A failure of indicator integrality, the twisted-real criterion, or the model formula would expose an error in the proposed mechanisms. Success cannot prove the conjecture for arbitrary blocks, because all tested ambient model groups are solvable and already lie in the known theorem.

The base group is Q8, written as i^a j^b with 0<=a<4 and 0<=b<2, satisfying j^2=i^2 and ji=i^(-1)j. A marked index-two extension is determined by

    alpha in Aut(Q8), z in Q8,
    alpha^2=Ad(z), alpha(z)=z,

with t d t^(-1)=alpha(d) and t^2=z. Every extension of the marked Q8 has such a presentation after choosing t. Different choices can describe isomorphic groups or the same extension; no claim about a list of distinct isomorphism classes is made.

The script enumerates all 24 automorphisms through the possible images of i,j, tests the two compatibility equations, and obtains 32 compatible (alpha,z) presentations. It constructs the multiplication table of each extension and checks all associativity triples and two-sided inverses.

## Exact verification

For each presentation the script computes the five Gow indicators from the square list in the outside coset. It checks:

1. each indicator is -1,0,+1;
2. its nonvanishing agrees with the twisted-real character condition;
3. the degree-weighted sum equals the number of outside involutions;
4. the entire pointwise Fourier identity (2) holds on Q8.

It then constructs G=C3 semidirect E and all five characters psi_lambda from Attempt 1. Values are stored in Z[zeta_3] as pairs of integers, using zeta_3^2+zeta_3+1=0; there is no floating-point approximation. It verifies all 25 inner products per presentation and directly sums psi_lambda(g^2) over all 48 group elements to obtain the Frobenius–Schur indicator.

All checks passed:

- 32 compatible marked presentations;
- 160 model-character indicator comparisons;
- 800 model-character inner-product comparisons;
- exact verification of the two distinct height-sign distributions in Attempt 3.

The eight ordered Gow-indicator vectors each occur four times. Up to permutation of the three nontrivial linear characters, their four forms are

    (1,1,0,0,+1), (1,1,0,0,-1),
    (1,1,1,1,+1), (1,1,1,1,-1).

The last coordinate is the unique degree-two character. Corresponding outside-involution counts are 4,0,6,2. These are local calculations and computations in known model blocks, not 160 new cases outside the published solvable theorem.

## A useful sign diagnostic

For alpha=identity and z=1, E=Q8 times C2 and the degree-two indicator is -1. For alpha=identity and z=-1, the extension is the central product of Q8 and C4 identifying their central involutions, and that indicator is +1. In both cases every irreducible character is twisted-real, all four linear indicators are positive, and the outside-square support is {1,-1}. The multiplicities differ: (2,6) versus (6,2). Therefore knowing the real-character permutation and square support alone still fails to determine the nonlinear sign. The square-corrected flip or the full square multiplicities carry indispensable information.

## Reproduction and final boundary

Run `python3 check_indicators.py` from this folder. The standard-library program writes `exact_results.json`. Every assertion is exact; the finite scope is explicitly recorded in its output. The group and character proofs in Attempts 1–2, rather than finite enumeration, justify their general statements.

No counterexample to the original conjecture was found. No proof for arbitrary real nilpotent blocks was obtained. The five approaches end with the missing duality/form-preserving transfer theorem or the unproved local projective-indicator identities of Attempt 4.

**Final status: unsolved after five substantive approaches.**
