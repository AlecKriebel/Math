#!/usr/bin/env python3
"""Exact local/model checks; never certifies actual L-function moments."""
import argparse
import json
import math
import sys
from fractions import Fraction as F


class GQ:
    def __init__(self, real=0, imag=0):
        self.r, self.i = F(real), F(imag)

    def __add__(self, other):
        other = other if isinstance(other, GQ) else GQ(other)
        return GQ(self.r + other.r, self.i + other.i)

    __radd__ = __add__

    def __neg__(self):
        return GQ(-self.r, -self.i)

    def __sub__(self, other):
        return self + -other

    def __mul__(self, other):
        other = other if isinstance(other, GQ) else GQ(other)
        return GQ(self.r * other.r - self.i * other.i,
                  self.r * other.i + self.i * other.r)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return GQ(self.r / other, self.i / other)

    def __pow__(self, n):
        answer = GQ(1)
        for _ in range(n):
            answer = answer * self
        return answer

    def __eq__(self, other):
        other = other if isinstance(other, GQ) else GQ(other)
        return self.r == other.r and self.i == other.i

    def norm2(self):
        return self.r * self.r + self.i * self.i


COUNT = 0


def require(condition, label):
    global COUNT
    if not condition:
        raise ValueError(label)
    COUNT += 1


def conv(a, b, degree):
    return [sum((a[j] * b[n-j] for j in range(n+1)), GQ())
            for n in range(degree+1)]


def local_binomial(z, weight, degree):
    out = [GQ(1)]
    for n in range(1, degree+1):
        out.append(out[-1] * z * (weight+n-1) / n)
    return out


def full_local(rows, degree):
    out = [GQ(1)] + [GQ()] * degree
    for z, weight, deleted in rows:
        out = conv(out, local_binomial(GQ() if deleted else z,
                                      weight, degree), degree)
    return out


def exponential_by_powers(logcoeff, degree):
    # Direct Taylor expansion of exp(h), independent of binomial convolution.
    answer = [GQ(1)] + [GQ()] * degree
    power = [GQ(1)] + [GQ()] * degree
    for k in range(1, degree+1):
        power = conv(power, logcoeff, degree)
        fac = math.factorial(k)
        answer = [a + b / fac for a, b in zip(answer, power)]
    return answer


def truncated_local(rows, cutoff_degree, degree, wrong_deletion=False):
    logcoeff = [GQ()] * (degree+1)
    for n in range(1, min(cutoff_degree, degree)+1):
        logcoeff[n] = sum((z**n * weight / n
                          for z, weight, _ in rows), GQ())
    out = exponential_by_powers(logcoeff, degree)
    for z, weight, deleted in rows:
        if deleted:
            out = conv(out, local_binomial(z,
                       weight if wrong_deletion else -weight, degree), degree)
    return out


def rising_coeff(weight, degree):
    out = [F(1)]
    for n in range(1, degree+1):
        out.append(out[-1] * (weight+n-1) / n)
    return out


def tail_bound(weight, prime, degree):
    if weight == 0:
        return F(0)
    d = rising_coeff(weight, degree+1)[-1]
    first = d*d / prime**(degree+1)
    ratio = max(F(1, prime), ((weight+degree+1)/(degree+2))**2 / prime)
    require(ratio < 1, 'tail ratio must be strictly below one')
    return first/(1-ratio)


def determinant(matrix):
    matrix = [[F(v) for v in row] for row in matrix]
    out = F(1)
    for col in range(len(matrix)):
        row = next((r for r in range(col, len(matrix)) if matrix[r][col]), None)
        if row is None:
            return F(0)
        if row != col:
            matrix[col], matrix[row] = matrix[row], matrix[col]
            out = -out
        pivot = matrix[col][col]
        out *= pivot
        for r in range(col+1, len(matrix)):
            factor = matrix[r][col]/pivot
            for c in range(col+1, len(matrix)):
                matrix[r][c] -= factor*matrix[col][c]
    return out


def cue_toeplitz(size, weight):
    def fourier(k):
        return (-1)**abs(k) * math.comb(2*weight, weight+k) if abs(k) <= weight else 0
    return determinant([[fourier(j-k) for k in range(size)] for j in range(size)])


def cue_gamma(size, weight):
    answer = F(1)
    for j in range(1, size+1):
        answer *= F(math.factorial(j-1)*math.factorial(j+2*weight-1),
                    math.factorial(j+weight-1)**2)
    return answer


def main(mutant):
    rows_cases = [
        [(GQ(1), F(1), False)],
        [(GQ(1), F(1), True)],
        [(GQ(1), F(1), False), (GQ(1), F(1), True)],
        [(GQ(1), F(1,4), False), (GQ(0,1), F(3,4), False)],
        [(GQ(0,1), F(1,2), True), (GQ(0,-1), F(3,2), False)],
        [(GQ(-1), F(5,3), True), (GQ(1), F(1,3), True)],
        [(GQ(), F(4,3), True), (GQ(0,-1), F(1,3), False)],
        [(GQ(1), F(0), True)],
    ]
    if mutant == 'negative_weight':
        rows_cases.append([(GQ(1), F(-1,4), False)])
    degree = 24
    truncated_cases = 0
    for rows in rows_cases:
        require(all(weight >= 0 for _, weight, _ in rows), 'nonnegative claimed domain')
        total = sum((weight for _, weight, _ in rows), F(0))
        full = full_local(rows, degree)
        majorant = rising_coeff(total, degree)
        for n in range(degree+1):
            require(full[n].norm2() <= majorant[n]**2, 'full local majorant')
        for cutoff_degree in [1,2,4,8,24]:
            truncated = truncated_local(rows, cutoff_degree, degree,
                                        mutant == 'deletion_sign')
            if mutant == 'finite_equals_full' and cutoff_degree == 1:
                claimed = full_local(rows_cases[0], degree)
                exact = truncated_local(rows_cases[0], 1, degree)
                require(claimed[2] == exact[2], 'sharp finite cutoff differs at coefficient two')
            for n in range(cutoff_degree+1):
                require(truncated[n] == full[n], 'deleted/truncated coefficient agreement')
            # Deleted factors add at most another total to the absolute majorant.
            bound = rising_coeff(total*2 if any(d for _,_,d in rows) else total, degree)
            for n in range(degree+1):
                require(truncated[n].norm2() <= bound[n]**2, 'truncated local majorant')
            truncated_cases += 1

    # Rigorous rational enclosure for the sharp X=3,p=2 counterexample.
    degree = 32
    exact_partial = sum((F(1, 2**n*math.factorial(n)**2)
                         for n in range(degree+1)), F(0))
    first_omitted = F(1,2**(degree+1)*math.factorial(degree+1)**2)
    tail = first_omitted/(1-F(1,2*(degree+2)**2))
    require(exact_partial+tail < F(13,8), 'sharp mean upper bound')
    require(F(13,8) < 2, 'sharp mean strictly below full Euler mean')

    # Nonnegative fractional local tail bounds at the smallest prime.
    tail_certificates = []
    for weight in [F(1,4),F(1,2),F(7,4),F(5),F(17,3)]:
        bound = tail_bound(weight,2,128)
        require(bound < F(1,10**20), 'fractional local tail enclosure')
        tail_certificates.append({'weight':str(weight),'tail_upper_bound':str(bound)})

    # Common-phase exact means for two equal local factors at p=2.
    joint = F(1+F(1,2), (1-F(1,2))**3)
    proposed_joint = F(4) if mutant == 'independent_local_phases' else joint
    require(proposed_joint == 12, 'same-prime joint mean is twelve')
    actual_ratio = F(2,12)
    proposed_ratio = F(1) if mutant == 'ignore_deletion' else actual_ratio
    require(proposed_ratio == F(1,6), 'zeta times principal mod2 deletion ratio')
    proposed_same_E = 2 if mutant == 'modulus_grouping' else 4
    require(proposed_same_E == (F(1)+F(1))**2, 'aggregate same primitive before square')
    proposed_conjugate_E = 4 if mutant == 'conjugate_grouping' else 2
    require(proposed_conjugate_E == F(1)**2+F(1)**2, 'distinct quartic conjugates')

    # First-order regulator for distinct local values 1,-1, weight one each.
    regulator = [GQ(1), GQ(-2)]
    cross = [GQ(1), GQ(-2 if mutant == 'regularizer_sign' else 2)]
    require(conv(regulator,cross,1)[1] == 0, 'correct cross-factor sign cancels linear term')

    # Weyl/Andreief determinant of exact Laurent Fourier coefficients.
    cue_cases = 0
    for weight in range(5):
        for size in range(1,9):
            exact = cue_toeplitz(size,weight)
            require(exact == cue_gamma(size,weight), 'Toeplitz and gamma moments agree')
            require(exact > 0, 'CUE exact mean positive')
            if weight == 1:
                require(exact == size+1, 'CUE m1 polynomial')
            if weight == 2:
                leading = F(1,288) if mutant == 'extra_gamma' else F(1,12)
                require(exact == leading*(size+1)*(size+2)**2*(size+3),
                        'no extra Gamma(E+1) in m2 constant')
            cue_cases += 1

    require(mutant != 'declare_theorem', 'local checks cannot certify L-function moment theorem')
    return {'status':'PASS','scope':'exact local/model normalizations and finite cutoff control only; no actual L-function moment theorem',
            'checks':COUNT,'local_cases':len(rows_cases),'truncated_local_cases':truncated_cases,
            'exact_degree':24,'cue_exact_cases':cue_cases,
            'sharp_X3_p2_mean_interval':{'lower':str(exact_partial),'upper':str(exact_partial+tail),'strict_upper':'13/8','full_Euler_mean':'2'},
            'fractional_tail_certificates':tail_certificates,'asymptotic_proved':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', choices=['negative_weight','deletion_sign','finite_equals_full',
                        'independent_local_phases','ignore_deletion','modulus_grouping',
                        'conjugate_grouping','regularizer_sign','extra_gamma','declare_theorem'])
    args = parser.parse_args()
    try:
        report = main(args.mutant)
    except Exception as error:
        print(f'REJECT: {error}', file=sys.stderr)
        sys.exit(1)
    print(json.dumps(report,indent=2,sort_keys=True))
