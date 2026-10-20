from fractions import Fraction
values = [(Fraction(k,q), k,q) for k in range(2,21) for q in range(1,k//2+1)]
strictly_below = [(r,k,q) for r,k,q in values if r < Fraction(20,7)]
maximum = max(r for r,k,q in strictly_below)
if maximum != Fraction(17,6):
    raise ValueError('Unexpected rational gap')
print('PASS: maximum k/q < 20/7 with 2 <= k <= 20 and 1 <= q <= k/2 is', maximum)
