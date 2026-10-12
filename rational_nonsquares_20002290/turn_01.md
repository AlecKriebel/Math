# Attempt 1: assemble nonsquares from square classes and local obstructions

## Target and starting point

The remaining target is N=Q\P₂, in M=(Q;0,1,+,P₂). The prior positive-cone construction already handles negative rationals and inequalities. This attempt tries to build the positive part of N from simpler positively definable arithmetic pieces, first fixed square classes and then finitely many local obstructions. No claim of full resolution is made.

## Fixed rational scalars are available, variable multiplication is not

For each fixed rational c=m/n, n>0, the graph z=cy is expressible by the additive equation nz=my, moving any negative coefficient to the other side. Rational numerals likewise have unique additive definitions. Thus, for fixed nonzero c, the square class

C_c={c q²:q in Q, q≠0}

has a positive-existential definition: there exists s such that P₂(s), s≠0 and x=cs. Here s≠0 is expanded using the prior formula, and x=cs is an abbreviation for a fixed-coefficient additive equation. If c is a nonsquare, every element of C_c is a nonsquare, since c q²=r² would give c=(r/q)².

Every nonzero rational has exactly one class in Q×/Q×². Consequently N is the union of the negative rationals and of the positive nonsquare classes C_c. This offers correct individual positive definitions, but apparently requires infinitely many disjuncts.

## Finite square-class obstruction

**Proposition.** For any fixed finite set c₁,...,c_r in Q×, there is a positive rational nonsquare outside the union of their square classes.

**Proof.** Let S contain all primes appearing in a numerator or denominator of some c_i in lowest terms. Choose a prime p outside S. If p=c_i q², then taking the p-adic valuation gives 1=0+2v_p(q), impossible. The positive rational p is nonsquare for the same valuation reason. This proves the claim. The argument works whether or not the c_i themselves are nonsquares. □

This obstruction is exact and does not depend on a witness-height bound. No finite list of named nonsquare coefficients can cover the missing target. Replacing the list by an existentially quantified coefficient c does not solve it: requiring c nonsquare is circular, and x=cs introduces variable multiplication, absent from M.

## Finite local tests also miss positive nonsquares

A different approach might use the local fact that a positive rational is a square in Q if and only if all its prime valuations are even. Could finitely many completions suffice for a formula assembled from local tests? The answer is negative even if definability of all those local tests is granted.

**Proposition.** For every finite set S of primes there is a positive rational x that is a square in Q_p for every p in S, but is not a square in Q.

**Proof.** Set m=4 times the product of primes in S (empty product 1), and x=m²+1. As an integer, x lies strictly between m² and (m+1)². A rational square that is an integer is an integer square: if a²/b² is an integer and gcd(a,b)=1, then b=1. Hence x is not a rational square.

For odd p in S, x is congruent to 1 modulo p. The polynomial f(T)=T²-x satisfies f(1) divisible by p and f'(1)=2 a p-adic unit, so the usual Hensel lift gives a Q_p-root. At p=2, m is divisible by 4 and x≡1 mod16. The standard criterion that a 2-adic unit congruent to 1 modulo 8 is a square applies. Finally x>0, so the real place supplies no obstruction. □

Thus even all local nonsquare predicates from a predetermined finite set of places, together with negativity, cannot characterize N. This does not prove that arbitrary positive-existential formulas are local finite-place tests. Quantified variables could encode unbounded prime information. Such an encoding is precisely what is missing here.

## Attempt outcome

The construction obtains individually definable nonsquare square classes and a rigorous obstruction to two natural finite assembly strategies. It does not produce a formula for all positive nonsquares and does not prove impossibility for the full language. The next attempt must use genuinely coupled square predicates rather than a finite menu of preselected arithmetic classes or places.

Fresh substantive attempt count: 1/5. Prior positivity and nonzero definitions are credited background, not part of this count.
