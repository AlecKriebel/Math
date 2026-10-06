# Five substantive routes and exact disposition

Target 30002048 / OWR-11784-007. All-degree status: **unsolved**. The routes below are distinct mechanisms, not five restatements of the same norm condition. No sixth search route was pursued.

## 1. Cyclotomic order and prime-power norm obstruction

Mechanism: classify the order of αʲ for roots of unity and the integer norm of 1−αʲ. The exact formula E₀(ζ_m)=m/Q−1, with Q the largest prime power dividing m, and the inequality m/Q≤φ(m) settle this entire branch. Section 6 of `PROOF.md` supplies an elementary proof.

Outcome: complete subcase, with no hypothesis excluding any order m. Gap: algebraic integers that are not roots of unity are not covered.

## 2. Reduction at finite primes and the limits of a local sieve

For a prime ideal 𝔭 of O_K with α mod 𝔭 nonzero, let t be its multiplicative order in the residue field. Then αᵗ−1 lies in 𝔭, so it is not a unit, and E₀(α)≤t−1≤N(𝔭)−2. If α is a unit, the nonzero condition holds at every 𝔭. If α is not a unit, primes dividing α give no such obstruction. Equivalently, |B_j(f)|=1 holds if and only if f and xʲ−1 are relatively prime after reduction modulo every rational prime; this is also equivalent to |A_m(f)|=1 for every m dividing j.

This is a useful exact local obstruction, but checking finitely many rational primes cannot settle the unbounded-coefficient problem. Here is a constructive reason. Fix a finite nonempty prime set T and k with D=∑_{j=1}^k φ(j)<d. Put H=∏_{j=1}^k Φ_j and take any squarefree M divisible by all primes in T. Then

f=xᵈ+MH

is monic of degree d, has constant term −M, and is Eisenstein at each prime dividing M. It is therefore irreducible. At every p∈T it is congruent to xᵈ, so it passes every coprimality test with xʲ−1 over F_p, even for arbitrarily large j. At the same time, for j≤k, f(ζ_j)=ζ_jᵈ, so |A_j(f)|=1 exactly. Arbitrarily large squarefree M give an unbounded-height family with these properties. This construction is not a counterexample to the conjecture: D<d only gives a much shorter prefix. It shows why the stated finite-prime sieve and a short exact prefix leave a real gap.

Outcome: rigorous obstruction and rigorous limitation. Gap: a uniformly small obstructing prime/finite-field order, or a separate global height bound, is not established.

## 3. Finite quadratic-unit residues and exact CRT classification

The unit groups at Φ₁, Φ₂, Φ₃, Φ₄, Φ₆ have only 2,2,6,4,6 possible residues. Rational CRT followed by integrality reduces every f with E₀≥6 to f=Pq+r with 24 possible r. This yields complete, height-unrestricted computer-assisted proofs e(7)=5, e(8)=7, and e(9)=6. Degree nine uses 24 nonzero quartic equations in one integer coefficient and exhaustive rational-root tests. See `PROOF.md`, `verify.py`, and `results.json`.

Outcome: complete degree-7/8/9 partial result. Gap: for d≥10, q has at least two unrestricted coefficients and the remaining simultaneous norm equations are not solved. Declaring this parametrization to be a proof of the all-degree bound would be circular.

## 4. Archimedean norm growth and the missing near-unit-circle control

Writing the conjugates as α_i gives |N(αⁿ−1)|=∏|α_iⁿ−1|. Growth of the factors with |α_i|>1 suggests eventual failure of the unit condition; its rate is governed by the Mahler measure. The problem is uniform failure at some n≤d. The simple lower estimate |α_iⁿ−1|≥||α_i|ⁿ−1| is ineffective for conjugates near the unit circle and can vanish for conjugates on it. A global product lower bound greater than 1 for at least one n≤d is not obtained.

Stewart's effective general estimate E₀(α)≪d(log(d+1))⁴/(log log(d+2))³ proves finiteness but cannot imply the desired coefficient-one bound: its extra factor is unbounded. Substituting that estimate into the target merely moves the difficulty into an unproved sharpening. The root-of-unity case was handled separately in Route 1, so no claim improperly applies a non-root-of-unity height estimate there.

Outcome: blocked at a specific uniform product-distance estimate. The route supplies neither a new all-degree inequality nor a counterexample.

## 5. Degree amplification by polynomial substitution

For B_n(f)=Res(xⁿ−1,f), let g=gcd(n,k). The map ζ↦ζᵏ sends the n-th roots of unity onto the (n/g)-th roots, each g times. Therefore, exactly,

B_n(f(xᵏ))=B_{n/g}(f)^g.

This tests a plausible way to amplify the exceptional small-degree equality cases into higher-degree counterexamples. If r is the first failed index for f and gcd(r,k)=1, the same index already fails for f(xᵏ). If gcd(r,k)>1 it can move later, but later failures of the original sequence can intervene. The coarse bound from n=kr is E₀(f(xᵏ))≤kr−1, insufficient in general to imply a strict degree bound.

For f=x⁵+x⁴+x³−x−1, exact controls k=1,…,8 give polynomial prefix lengths 5,8,7,8,5,10,5,8 at degrees 5,10,15,20,25,30,35,40. Here “polynomial prefix” refers to resultant conditions and does not assert that each substituted polynomial is irreducible. The identity is independently checked by direct determinant resultants through each first failure in these controls. This entire simple family produces no counterexample. No inference from these eight controls to all k or all polynomials is made.

Outcome: exact transformation law and reproducible failed counterexample family. Gap: the identity does not classify all primitive minimal polynomials or all possible failure-index patterns.
