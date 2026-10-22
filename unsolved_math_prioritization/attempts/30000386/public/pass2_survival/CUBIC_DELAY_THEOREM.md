Scope: an authored mathematical partial result for the exact two-dimensional king-move Time-Bomb game. The unrestricted conjecture is not resolved. No novelty claim is made. Original contract SHA-256: 1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c.

Dependency: HIDDEN_BLOCK_CRITERION.md, Theorem 1.

### 2.1 Cubic blocks and a simple power-law bound

Take S_j=j³ for j≥1. Then

L_j=3j²+3j+1,

and L_(j+1)>L_j≥3j². Hence

Q < sum_(j≥1) 1/(4L_j) ≤ (1/12) sum_(j≥1) 1/j² ≤ 1/6.

The last inequality follows from 1+integral_1^infinity x^(−2) dx=2. The randomized survival probability is therefore greater than 5/6.

The exact restriction is:

If j³≤n<(j+1)³, then t_n≥(j+2)³.

A simpler sufficient condition is

t_n−n ≥ 26 n^(2/3).

Indeed, n≥j³, and

(j+2)³−n ≤ (j+2)³−j³ = 6j²+12j+8 ≤ 26j² ≤ 26n^(2/3)

for j≥1. For integer time coordinates, the right side can be rounded up. Thus the Angel wins against arbitrary mixed deadlines whenever every effective bomb is announced at least ceil(26n^(2/3)) rounds before its detonation.
