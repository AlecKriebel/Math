# Approach 1: modular injectivity and the finite-denominator boundary

**Result:** exact fine-scale cardinality; a literal finite-denominator counterexample. Neither settles the intended large-denominator question.

Throughout, a,b are fixed multiplicatively independent integers greater than 1, s is a positive integer, gcd(s,ab)=gcd(s,r)=1, and
A_L(r,s)={a^n b^k r/s mod 1: 0<=n,k<=L}.
The covering number C(E,delta) uses closed intervals of length delta in [0,1]; using circle arcs changes it by at most a factor of 2.

## 1. Fixed points
If L>=1, A_L(r,s) is a singleton if and only if s divides both a-1 and b-1. Necessity follows by comparing r/s with ar/s and br/s and cancelling the unit r modulo s. Conversely these two congruences fix r/s under every product.

Take a=4,b=7,s=3,r=1. The bases are multiplicatively independent: an equality 4^u 7^v=1 for integers u,v forces u=v=0 by the 2- and 7-adic valuations. All coprimality hypotheses hold. Every orbit point is 1/3, hence log C(A,delta)=0 for every positive delta. The exponential series gives e<3, so log log 3>0. No positive c can make 0>=c log log 3. If the cutoff L is less than 1 the same singleton conclusion holds anyway. Thus the unqualified all-denominators formulation is false for these bases. The asymptotic formulation with s>=s0(a,b) is unaffected. This is not presented as a resolution of its intended quantitative content.

The cases s=1 and nonpositive s also need exclusion for the logarithms to be meaningful. Constants must be positive; otherwise K=0 trivializes the database's version. Natural-number exponents are understood. Starting exponents at 1 instead of 0 amounts to replacing the unit numerator r by abr and shifting the cutoff by 1.

## 2. Fine-scale injectivity
Let L be any nonnegative integer satisfying (ab)^L<s. The (L+1)^2 positive integers a^n b^k with 0<=n,k<=L are distinct, by multiplicative independence, and belong to [1,s). Their residues modulo s are therefore distinct. Multiplication by r preserves distinctness because r is a unit. Consequently |A_L|=(L+1)^2 and its distinct points have circle distance at least 1/s.

In particular, L=floor(log(s-1)/log(ab)) gives |A_L| comparable to (log s)^2 for sufficiently large s, and C(A_L,delta)=|A_L| when delta<1/s.

At a general scale delta, each covering interval contains at most floor(s delta)+1 points of the s-grid. Therefore
C(A_L,delta)>=(L+1)^2/(floor(s delta)+1).
For delta=(log s)^(-N), the right side tends to zero for every fixed N. This method establishes many distinct rational points but supplies no useful control of their clustering at the requested scale.

## Remaining gap
A nonconcentration estimate must connect the exact s-grid separation with the much coarser polylogarithmic scale. Increasing the count of points alone does not establish that estimate.
