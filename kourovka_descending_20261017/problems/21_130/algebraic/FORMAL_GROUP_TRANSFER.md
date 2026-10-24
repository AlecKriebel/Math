# Formal-group transfer of finite polynomial certificates

2026-10-24. This is a **partial-family theorem**, not a full solution of Kourovka 21.130. Its all-cardinality use is conditional on an unproved coefficient statement. No novelty claim is made.

## The finite polynomial input

For `n>2` and cyclic indices, put `s_i=x_i+x_(i+1)` and

`Q_n(x) = [prod_(i<j)(x_j−x_i)] [prod_(i<j, {i,i+1}∩{j,j+1}=empty)(s_j−s_i)]`.

There are `n(n−3)/2` factors in the second product. Thus `Q_n` is homogeneous of degree `d=n(n−2)`. Let `bar Q_n` denote its image modulo `(x_1^n,...,x_n^n)`, with integer coefficients.

**Input condition at a prime p:** `bar Q_n` has a coefficient not divisible by `p`.

The exact computations and independently checked coefficient witnesses in `polynomial/SLACK_RESULTS.md` establish this input for every odd prime and `3≤n≤9`. This is a finite certificate, not a conjecture about all `n`.

## Integral analytic transfer lemma

Let `K` be a complete discretely valued field of characteristic zero, with valuation ring `O`, maximal ideal `m`, and residue field of characteristic `p`. Let `F(X,Y)∈O[[X,Y]]` be a convergent integral one-dimensional formal group law whose linear part is `X+Y`. Let `B⊂m` be a set of `n` distinct points. If the input condition holds, there is a cyclic enumeration `(b_1,...,b_n)` of `B` for which the `n` values `F(b_i,b_(i+1))` are pairwise distinct.

**Proof.** Form the formal power series

`P_F(x) = [prod_(i<j)(x_j−x_i)] [prod_(disjoint cycle edges i,j)(F(x_j,x_(j+1))−F(x_i,x_(i+1)))]`.

It has no terms of total degree below `d`; its homogeneous degree-`d` part is `Q_n`.

Set `g(T)=prod_(b∈B)(T−b)`, a monic polynomial of degree `n`. All its lower coefficients lie in `m`, so `g(T)≡T^n mod m`. Let `E` be the free `O`-module of polynomials in `n` variables with individual degrees below `n`. On `E`, let `T_i` be multiplication by `x_i` followed by monic reduction modulo `g(x_i)`. These operators commute. Their reductions modulo `m` are the usual nilpotent shifts, so `T_i^n E⊂mE`. Consequently substitution of the `T_i` in any integral formal power series converges in the `m`-adic topology, and gives a well-defined remainder map `rho:O[[x_1,...,x_n]]→E`.

Reduction of `rho` modulo `m` is ordinary reduction modulo `(x_1^n,...,x_n^n)`. In particular, the total-degree-`d` component of `rho(P_F) mod m` is precisely `bar Q_n mod p`. Terms of higher total degree either retain that degree or vanish under this monomial truncation. The input condition therefore implies `rho(P_F)≠0`.

For each tuple in `B^n`, evaluation of the remainder equals evaluation of the convergent original series. One way to check this equality without a formal-division assumption is to approximate by finite-degree polynomials: ordinary monic remainders preserve grid values, and both the series evaluations and the operator remainders converge. A polynomial of individual degrees below `n` which vanishes on `B^n` is zero, by repeated one-variable interpolation over `K`. Hence `P_F` has a nonzero value at some tuple in `B^n`.

Its Vandermonde factor forces all tuple coordinates to be distinct, so they enumerate `B`. Its other factors prevent collisions between values on disjoint cycle edges. Collisions on two adjacent edges are impossible by cancellation in the formal group: `F(u,v)=F(v,w)` implies `u=w`. Thus all neighboring formal sums are distinct. QED.

Boundary checks: convergence uses the finite extension containing the torsion points, hence a complete DVR; all grid points lie strictly inside its maximal ideal; no interpolation denominator is asserted to be an integral unit. Interpolation occurs over the field after the integral remainder is known to be nonzero.

## Transfer to every finite abelian p-group

**Theorem.** Fix `n>2` and a prime `p`. If `bar Q_n` has a coefficient not divisible by `p`, then every `n`-element subset of every finite abelian `p`-group has a cyclic ordering with pairwise distinct neighboring sums.

**Imported primary result.** Lubin and Tate, *Formal Complex Multiplication in Local Fields*, Annals of Mathematics 81 (1965), 380–387, construct an integral one-dimensional formal group law for a local field `K` and uniformizer `pi`. Their Theorem 2(b), pp. 383–384, identifies its `pi^k`-torsion, all represented by elements of positive valuation, with `O_K/pi^k O_K` as an `O_K`-module. [Original paper](https://math.bu.edu/people/jsweinst/AWS/Files/LubinTateFormalCMinLocalFields.pdf), [DOI](https://doi.org/10.2307/1970622). The local cache is `LubinTate1965.pdf`; the cited statement was checked in the original.

**Proof.** Write the given finite abelian `p`-group as a subgroup of `(Z/p^k Z)^h`. Choose the unramified extension `K/Q_p` of degree `h`. Its ring of integers is free of rank `h` over `Z_p`, and `p` is a uniformizer, so the additive group `O_K/p^k O_K` is `(Z/p^k Z)^h`. The imported theorem realizes this group as the `p^k`-torsion of an integral one-dimensional Lubin–Tate formal group.

All its finitely many torsion points lie in the maximal ideal of a common finite extension `L/K`. View the original group as the corresponding subgroup of the formal group, and its subset as a set `B⊂m_L`. Apply the analytic transfer lemma over `L`. Because the embedding is a group embedding, distinct neighboring formal sums give distinct neighboring original sums. QED.

**Verified consequence of the existing finite certificates:** the claim of Kourovka 21.130 holds for `3≤n≤9` in every finite abelian group of prime-power order, for every odd prime and every exponent/rank.

## Exact remaining gaps

1. No proof is known here that `bar Q_n` is nonzero modulo every odd prime for all `n`. A statement about a central coefficient of the unreduced full Vandermonde polynomial does not establish this input.
2. The theorem concerns `p`-groups. An arbitrary finite abelian group of odd order can have several distinct prime divisors. The one-dimensional formal-group embedding above does not embed such a group into its maximal ideal: multiplication by an integer prime to the residue characteristic is invertible there. No reduction from mixed-prime subsets to primary subsets has been supplied.
3. The computations at bounded `n`, even after transfer, are partial. They do not prove the unrestricted target.
