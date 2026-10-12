"""Exact rational checks of constants used in the pinned fourfold companion.

This checks arithmetic, not the geometric hypotheses or the full theorem.
Run with Python 3; standard library only.
"""

from fractions import Fraction as F


def verify(label, actual, expected):
    assert actual == expected, (label, actual, expected)
    print(f"{label}: {actual}")


modes = [(F(1), F(1, 2)), (F(9, 16), F(3, 2)), (F(1, 16), F(5, 2))]
moments = [sum(F(1, 2) * a * x ** (2 * j) for a, x in modes) for j in range(4)]
for j, expected in enumerate([F(13, 16), F(61, 64), F(685, 256), F(11101, 1024)]):
    verify(f"M_{2*j}", moments[j], expected)

l = F(35, 12)
_, m2, m4, m6 = moments
verify("positive coefficient of c", l*l*m2-m4, F(50065, 9216))
verify("fourfold integral at c=-1", l*l*(m4-m2)-m6+m4, F(26581, 4096))
verify("fourfold contradiction margin", F(432,625)*(l*l*(m4-m2)-m6+m4)-F(625,144), F(209183,1440000))

d = F(5, 6)
verify("dimension-three margin", (d*d-F(1,3))*(d*d-F(1,4))+d*d/3-F(1,3), F(19,324))
D, beta = F(5,3), F(2,3)
verify("dimension-two constant", (D-beta)*beta**3+(3*D*beta-6*beta*beta)/3-F(1,3), F(5,27))
verify("dimension-two coefficient of c", (D-beta)*beta*beta+(D-3*beta)/3, F(1,3))
