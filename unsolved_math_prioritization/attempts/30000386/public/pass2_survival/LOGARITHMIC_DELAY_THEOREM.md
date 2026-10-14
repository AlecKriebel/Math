Scope: an authored mathematical partial result for the exact two-dimensional king-move Time-Bomb game. The unrestricted conjecture is not resolved. No novelty claim is made. Original contract SHA-256: 1be42b4f13460a91a71948fc532c135b7453f56811566ed5c3f918f8976c5c4c.

Dependency: HIDDEN_BLOCK_CRITERION.md, Theorem 1.

### 2.2 An explicit lead of order sqrt(n) log n

Let

b(j)=1+floor(log₂j),
L_j=j b(j)²,
S_1=1,
S_(j+1)=S_j+L_j.

The lengths are nondecreasing. Therefore

Q < (1/4) sum_(j≥1) 1/L_j.

For j in the dyadic group 2^k≤j<2^(k+1), b(j)=k+1, and

sum_(j=2^k)^(2^(k+1)−1) 1/[j b(j)²] ≤ 1/(k+1)².

Summing and again using sum_(m≥1)1/m²≤2 gives Q<1/2. The randomized survival probability is greater than 1/2.

Define the explicit integer lead function

g(n)=S_(j+2)−n whenever S_j≤n<S_(j+1).

Theorem 1 proves a deterministic win whenever every effective announcement satisfies t_n−n≥g(n). These times may otherwise be mixed arbitrarily and chosen adaptively.

Here is an explicit conversion, including small n:

g(n)≤21 sqrt(n) [1+log₂n] for every integer n≥1.

For j≥2, take the floor(j/2) terms with ceil(j/2)≤i<j in the sum defining S_j. Each satisfies i≥ceil(j/2) and b(i)≥b(j)−1≥b(j)/2. Also floor(j/2) ceil(j/2)≥j²/5 for j≥2. Consequently

n≥S_j≥j² b(j)²/20.

Furthermore j+1≤3j/2 and b(j+1)≤b(j)+1≤3b(j)/2, so L_(j+1)≤27L_j/8. Therefore

g(n)≤L_j+L_(j+1)≤35L_j/8≤(9/2)j b(j)²

≤(9/2)sqrt(20n) b(j)<21 sqrt(n) [1+log₂n],

where b(j)≤1+log₂j≤1+log₂n because S_j≥j. The only block-j=1 time is n=1; then S_2=2, S_3=10, and g(1)=9≤21. This proves the displayed bound for every n.

Thus t_n−n≥ceil(21 sqrt(n)[1+log₂n]) is a simple sufficient delay, and the exact block rule g is usually smaller. In particular the required lead is O(sqrt(n) log(n+1)). The theorem asserts these explicit lead rules, not that every unspecified constant in such an O-bound suffices.
