# Turn 4: an exact asymmetric obstruction certificate

Original conjecture unresolved. The support filter in Turn 2 does not cover every possible pattern. This turn examines the first residual coefficient system displayed in David Zhang's primary MathOverflow report and gives a short explicit algebraic certificate for it. The example and its previously reported infeasibility are credited; no new bounded-degree record is claimed.

## 1. A residual support pair that passes the unit test

Consider exact supports

U={0,1,3,7}, V={0,1,2,3,5,9,11,13}.

Their uniquely represented sums force unit coefficients precisely at U_1={0,7} and V_1={0,11,13}. Every sum of a pair in U_1×V_1 is uniquely represented. Thus Turn 2's unit-collision criterion cannot reject this pair. This is a combinatorial limitation of that criterion, not an example of a feasible unfair factorization.

After endpoint normalization and the forced unit at degree 11 of the second factor, write

A=1+a x+d x³+x⁷,
B=1+b x+c x²+e x³+f x⁵+g x⁹+x¹¹+x¹³.

All six named coefficients a,b,c,d,e,g are strictly positive for the stated exact supports, as is f. Since any positive product coefficient must be 1, the coefficients at product degrees 1,2,3,9,10,14,16 imply

a+b=1, ab+c=1, ac+d+e=1,
c+g=1, ag+e=1, a+d=1, d+g=1.

Only these seven equations are needed; the other product coefficients and the value of f can be ignored for the contradiction. They form a subset of the residual system displayed in Zhang's report.

## 2. Elimination and a portable polynomial identity

The last two equations give d=1−a and g=a. Then c=1−a and b=1−a. The equation ab+c=1 becomes a²=0. Meanwhile ag+e=1 gives e=1−a². Substituting into ac+d+e=1 gives 2−2a²=1. These two requirements contradict each other, even over the complex numbers.

For an entirely mechanical check, define

F1=a+b−1,
F2=ab+c−1,
F3=ac+d+e−1,
F8=c+g−1,
F9=ag+e−1,
F11=d+a−1,
F12=d+g−1.

The following identity holds in the integer polynomial ring in a,b,c,d,e,g:

1 = 2a F1 − 2 F2 + F3 + (2−a)F8 − F9 + (1−2a)F11 + (2a−2)F12.

It is a finite exact certificate, not a floating-point infeasibility report or a call to an unverified external solver. The checker expands both sides using a small integer sparse-polynomial implementation and checks equality coefficient by coefficient.

## 3. All-scale consequence and precise limits

For any positive integer h, simultaneous substitution x→x^h preserves all the coefficient relations. Translations of either support multiply its generating polynomial by a monomial and do not affect uniformity. Therefore no independent positive distributions on exact supports

s+h{0,1,3,7}, t+h{0,1,2,3,5,9,11,13}

can have a uniform sum. Here s,t are arbitrary integers. This is an infinite affine family of impossible support pairs, proved by the same certificate.

Allowing named coefficients to vanish changes the exact support and can change which product coefficients must equal 1; the seven equations must not then be imposed without justification. The identity proves inconsistency whenever the equations do hold, but not that every support deletion has those equations. Likewise, a certificate for this one asymmetric system does not imply a bounded certificate degree for all patterns, and Zhang's reported computations remain external work not replayed here.

The attempt to extend the simple support criterion to every pattern has therefore reached a concrete boundary. Algebraic relations can be essential after unique-sum forcing stops. We have not found a uniform reason that all residual systems must be inconsistent. The general conjecture remains unresolved after four substantive turns.
