# Independent audit of fixed-zero coefficients at n=11

Checkpoint 2026-10-24T19:47:47Z. Best-guess completion toward the full research problem: **15%**. This verifies another finite cardinality and the parent's formula; it does not prove the general coefficient-content hypothesis.

## Verdict and exact certificates

The parent's fixed-zero formula is correct, including sign and factorial denominator. An independent computation using the original binomial grid weights, and explicitly multiplying the integer vertex Vandermonde at each nonzero point, gives

| n | Exponents t | [x^t]Q_n |
|---:|---|---:|
|11|(0,9,10,10,10,10,10,10,10,10,10)|11098103614834|
|11|(0,10,9,10,10,10,10,10,10,10,10)|189427196282499|

The gcd is 1. Thus for every prime p, at least one coefficient is nonzero modulo p. The finite-field argument covers every 11-element subset of every elementary abelian p-group. The independently audited Lubin–Tate transfer then covers **every 11-element subset of every finite abelian p-group, for every prime p, including p=2**. The transfer uses no oddness assumption; p=2 is valid in its integral formal-group and interpolation arguments.

This also determines the full truncated coefficient content at n=11 to be 1, even without expanding the full polynomial: that content divides the gcd of these two coefficients. It does not determine the full support or its size.

The result at n=11 is compatible with known elementary obstructions at other even-characteristic cardinalities. For example, a full elementary abelian 2-group cannot have a rainbow Hamiltonian cycle because its edge colors are nonzero but there are fewer than n of them. The size-eleven statement does not include such a group of order eleven.

## Independent derivation of the parent's simplified formula

Let q=n(n−3)/2 be the number of nonadjacent template-edge pairs, N=n(n−1)/2, H=∏_(k=1)^(n−1)k!, and

    F(a)=∏_(nonadjacent i<j)(s_j(a)−s_i(a)),
    Q_n(a)=V(a)F(a).

Fix a position j>0 and t_0=0, t_j=n−2, t_i=n−1 for all remaining positions. The coefficient formula on the integer grid ∏{0,...,t_i} is

    [x^t]Q_n = 1/(∏t_i!) ∑_a (-1)^(∑(t_i−a_i)) (∏binom(t_i,a_i)) Q_n(a).

Every nonzero summand has a=(0,a_1,...,a_(n−1)), where its tail is a permutation of 1,...,n−1. Therefore ∑a_i=N and the grid sign is (-1)^(n(n−2)−N)=(-1)^q. Also V(a)=sgn(a)H, and the binomial product satisfies

    ∏binom(t_i,a_i)
      = ((n−1−a_j)/(n−1)) · ((n−1)!)^n / H².

Its denominator factor is

    ∏t_i! = (n−2)! ((n−1)!)^(n−2).

Combining these identities gives exactly

    [x^t]Q_n = (-1)^q (n−1)!/H
                · ∑_(tail permutations) sgn(a) F(a)(n−1−a_j).

The zero weight at a_j=n−1 automatically removes the grid points that exceed t_j. Every division above is in characteristic zero to compute an integer coefficient. Only the final integer is reduced modulo p; no factorial is inverted in characteristic p.

## Reproduction and independence

`fixed_zero_audit.py --n 11 --positions 1 2` performs the original grid formula directly, without importing the parent's `fixed_zero_coefficients.py`, without using its simplification, and without sparse polynomial expansion. It evaluates the actual Vandermonde by its 55 factors for every point with nonzero color factor, computes the binomial weights independently for each witness, divides by the original products of t_i!, and asserts zero remainder.

The run found 72244 nonzero Q evaluations and completed in 5.13 seconds. Output is preserved in `fixed_zero_n11_verification.txt`. Agreement is exact for both coefficients and their gcd.

## Remaining gap

No universal content theorem follows from these finite computations. Cardinality ten, general cardinalities, and mixed-prime finite abelian groups require separate arguments beyond this audit.
