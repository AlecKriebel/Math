# Attempt4 — Complex extremizers and the cubic subfamily

**Outcome: sharp n=2,m=3 subcase; no full resolution.**

A finite numerical search in normalized Hermite coefficients suggested nearly
coalescing cubic zeros. Solving the exact triple-zero coefficient conditions
produced r satisfying 4r³+6r²+6r+3=0 and P=K(z-r)³. This gives a rigorous
lower bound C>=0.903669747226... for any possible universal constant.

The upper bound for the entire cubic subfamily was then proved exactly:
shifted root variables obey w1w2w3+w1+w2+w3+2=0; an explicit imaginary-part
identity forces roots avoiding a sufficiently wide strip into one half-plane;
a self-contained polar-derivative argument then forces a zero of the diagonal
cubic in that same half-plane, contradicting its exact roots. The quadratic
boundary case is handled separately with sharp constant1/2.

See `CUBIC_SUBCASE.md` for the complete proof. Rational brackets and all algebraic
identities are checked in `verify.py`. Finite numerical optimization was a
construction aid, never the proof of either bound.

The degree3 coincidence identity does not cover unbounded n,m. Generalizing it
has not supplied a uniform theorem.

Completion estimate toward the unrestricted target: 20%, heuristic only.
