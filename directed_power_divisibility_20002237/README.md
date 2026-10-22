# Addition with directed p-power divisibility

**Problem:** AIM-LOGIC-0013 / UnsolvedMath 20002237 / queue rank 462  
**Research date:** 3 October 2026  
**Result:** partial results; original problem unresolved after five substantive attempts.

For a fixed prime p, define R_p(x,y) iff y=p^s x for an integer s≥0. The original AIM question asks whether the existential theory of (Z,+,R_p,0,1) is decidable. The domain is all integers; the language includes no order or arbitrary multiplication. Using strictly positive exponents instead gives an effectively interdefinable structure and does not change the decision question.

## What was proved

- **Lattice avoidance.** On an affine integer lattice, finitely many negative R_p-literals and additive disequalities have a common solution iff none individually fails everywhere. Nonidentity forbidden sets have density zero. See [Attempt 1](turn_01.md).
- **One positive atom, arbitrary negative atoms.** Existential sentences whose DNF conjunctions have at most one positive R_p-atom are decidable, even with unrestricted negative R_p-literals and additive disequalities. The earlier UnsolvedMath report covered only the positive-only version. See [Attempt 2](turn_02.md).
- **Named power multiplication.** The graph U∈p^N and y=Ux is positive-existentially definable for arbitrary integer x,y. This interprets exponent addition, ordinary divisibility, and order on the set of powers. See [Attempt 3](turn_03.md).
- **One shared exponential parameter.** Integer solvability of A(p^s)z=b(p^s), for arbitrary polynomial matrices, is decidable, also in the presence of finitely many negative R_p constraints with polynomial-affine arguments. See [Attempt 4](turn_04.md).
- **All atomic negations can be removed.** Nonzero and the complement of the directed R_p relation are positive-existentially definable. Hence the full existential decision problem is equivalent to its positive-existential version. See [Attempt 5](turn_05.md).

## What remains unresolved

Arbitrarily many positive atoms introduce independent power parameters. The full problem is equivalent to integer solvability of linear systems with coefficients depending on these independent powers. The one-parameter argument does not extend automatically: gcd(p^a−1,p^b−1)=p^gcd(a,b)−1 is unbounded, and multivariable polynomial gcd 1 does not imply a constant Bézout identity.

No decidability or undecidability conclusion for the complete AIM target is claimed. No global novelty or first-resolution claim is made for the partial lemmas. Pheidas's result over the nonnegative integers, and Rybalov's 2026 result with an explicitly named exponent-input function and order, do not settle the stated integer-domain reduct.

## Verification and status

The five attempt files contain the mathematical arguments. `verify_partial_results.py` is a standard-library-only deterministic exact-integer regression checker. Run:

    python verify_partial_results.py

The recorded output is [verification.json](verification.json). Its bounded tests check formula identities and representative algorithmic reductions; they are not a substitute for the general proofs. In particular no finite search is presented as a decision procedure for the full open problem.

Source scope and access limitations are documented in [SOURCE_GATE.md](SOURCE_GATE.md). This is an AI-assisted, unrefereed research record; independent mathematical review is required before relying on its claims.
