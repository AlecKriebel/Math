# Approach 4: averaged collision energy over prime denominators

**Result:** the target scale and a stronger covering exponent for almost all numerators when the denominator is prime. The exceptional numerators remain uncontrolled.

## Exact finite lemma
Let p be an odd prime, U a set of T distinct residues modulo p, and 0<delta<1/2. For 1<=r<=p-1 define
E_r = #{(u,v) in U^2 : ||r(u-v)/p|| <= delta}.
Then
(1/(p-1)) sum_r E_r = T + [2 floor(p delta)/(p-1)] T(T-1).                 (1)

Proof. The T diagonal pairs contribute for every r. For u!=v the residue u-v is nonzero and multiplication by it permutes the nonzero residues modulo p. Exactly 2 floor(p delta) of those residues have circle distance at most delta from zero. Summing separately over all ordered off-diagonal pairs proves (1). The restriction delta<1/2 ensures these two end ranges do not overlap. QED.

Write U_r={ru/p mod 1:u in U}. Any cover of U_r by K intervals of length delta assigns each of its T points to one covering interval. If the assignment sizes are m_1,...,m_K, then all sum_i m_i^2 ordered pairs assigned to the same interval are counted by E_r. Cauchy–Schwarz gives E_r>=T^2/K. Consequently
C(U_r,delta)>=T^2/E_r.                                                (2)
The same implication holds for circle-arc covers.

For each 0<eta<1, Markov's inequality applied to the nonnegative E_r now shows that all but at most eta(p-1) numerators satisfy
C(U_r,delta) >= eta T / [1+2 floor(p delta)(T-1)/(p-1)].                 (3)
The statement means an upper bound on the integer number of exceptional r; no rounding assumption is needed.

## Application to the multiplicative orbit
Fix the admissible bases a,b. Let p be a sufficiently large prime not dividing ab and set
L=floor(log(p-1)/(2 log(ab))),   U={a^n b^k:0<=n,k<=L}.
By multiplicative independence, U consists of T=(L+1)^2 distinct integers below p. Thus T is bounded above and below by positive constants times (log p)^2.

Take delta=(log p)^(-6) and eta=(log p)^(-1/2). Since
2 floor(p delta)(T-1)/(p-1) <= 2p delta T/(p-1) = O((log p)^(-4)),
(3) gives
C(A_L(r,p),(log p)^(-6)) >= c (log p)^(3/2)
for all but at most (p-1)/(sqrt(log p)) numerators. Here c>0 and the sufficiently-large threshold depend only on a,b. Taking logarithms yields
log C >= (3/2)log log p + O(1).
This is stronger than the requested entropy for this density-one subset of numerators, with an explicit relative exception bound.

## Remaining gap
The original question is uniform in every unit numerator and every admissible denominator. An average over r does not control the worst r, including potentially structured exceptional residues. The permutation count (1) also uses primality: for composite s a nonzero u-v need not be invertible. Neither issue is removed here. Finite computations validate (1)–(3), but cannot turn the density-one theorem into a uniform result.
