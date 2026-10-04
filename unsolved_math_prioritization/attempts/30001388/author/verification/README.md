# Exact controls

Run with Python 3.10 or newer, standard library only:

    python3 verification/check.py > /tmp/baker-check.json
    cmp /tmp/baker-check.json verification/result.json

The checks use integer polynomials and exact rational numbers. The exponential checks use rational Taylor lower bounds and geometric upper bounds for the tail. No binary floating-point computation is used.

What is checked:

1. The Cayley-conjugacy numerator and denominator, including the cubic parabolic fixed-point identity.
2. Exact real-step contraction for the Boole map and twelve finite outside-radius prefix controls.
3. The imaginary-height squared-increment formula.
4. Seventeen certified exponential sample enclosures supporting the scalar inequalities.
5. Six polynomial residue controls.
6. Elementary rational-coordinate separation checks for the topological model.

The proofs for all real arguments, infinite orbits, all entire approximants, and the topology of full sets appear in RESULT.md. Finite samples alone do not prove those universal statements. Fatou-component membership, boundary membership, harmonic-measure statements and the inner function of the entire example rely on the explicitly cited sources and are not numerically tested here.
