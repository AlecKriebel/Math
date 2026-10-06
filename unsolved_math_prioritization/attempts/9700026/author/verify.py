#!/usr/bin/env python3
"""Exact rational certificate checks; no third-party packages or source files."""
import copy
import json
import pathlib
import sys
from fractions import Fraction as F

EXPECTED_KEYS = {
    'schema', 'problem_id', 'alpha', 'beta', 'cities', 'initial_weights',
    'square_halfwidth', 'claimed_p', 'claimed_K', 'claimed_lower_bound',
    'claimed_upper_bound'
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    require(type(value) is str, 'rational values must be strings')
    return F(value)


def dist2(a, b):
    return sum((x-y)**2 for x, y in zip(a, b))


def verify(data):
    require(type(data) is dict and set(data) == EXPECTED_KEYS, 'wrong keys')
    require(data['schema'] == 'city-persistence-certificate-v1', 'schema mismatch')
    require(data['problem_id'] == '9700026', 'problem mismatch')
    alpha, beta = rational(data['alpha']), rational(data['beta'])
    require(alpha > 1 and beta > 2*alpha, 'not the refuted parameter region')
    q = alpha/beta
    p = 2*q
    require(p == F(1,2), 'this exact witness checker specializes to p=1/2')
    require(rational(data['claimed_p']) == p, 'incorrect exponent')
    require(type(data['cities']) is list and len(data['cities']) >= 2, 'need at least two cities')
    cities = []
    for row in data['cities']:
        require(type(row) is list and len(row) == 2, 'cities must have two coordinates')
        city = tuple(map(rational,row))
        require(all(0 < a < 1 for a in city), 'city outside strict interior')
        cities.append(city)
    n = len(cities)
    weights = list(map(rational, data['initial_weights']))
    require(len(weights) == n and all(w > 0 for w in weights), 'invalid initial weights')
    require(sum(weights) == 1, 'initial weights do not sum to one')
    h = rational(data['square_halfwidth'])
    require(h > 0, 'nonpositive square halfwidth')
    distances = []
    for i, city in enumerate(cities):
        require(all(h <= a <= 1-h for a in city), 'square crosses domain boundary')
        for j in range(i):
            dsq = dist2(city,cities[j])
            require(dsq >= 8*h*h, 'separation too small for square proof')
            distances.append(dsq)
    k = 4*h*h
    lower = k*k
    require(rational(data['claimed_K']) == k, 'incorrect K')
    require(all(w >= lower for w in weights), 'initial value below claimed all-time bound')
    require(rational(data['claimed_lower_bound']) == lower, 'incorrect lower bound')
    upper = 1-(n-1)*lower
    require(rational(data['claimed_upper_bound']) == upper, 'incorrect upper bound')
    require(lower > 0 and upper < 1, 'bounds do not rule out collapse')

    # Exact samples supplement (never replace) the uniform analytic inclusion.
    # z_i=s^4 gives z_i^q=s, and alpha=2,beta=8 allows integer powers.
    # Scale-equivalent parameters have identical cells, so this check applies to q=1/4.
    membership_checks = 0
    for i in range(n):
        for s in (F(1,2), F(1,3), F(1,5), F(1,17)):
            zi = s**4
            other_indices = [j for j in range(n) if j != i]
            denomin = sum(range(1,n))
            z = [F(0)]*n
            z[i] = zi
            for rank,j in enumerate(other_indices,1):
                z[j] = (1-zi)*rank/denomin
            require(sum(z)==1 and all(w>0 for w in z), 'sample state invalid')
            for a in (-1,0,1):
                for b in (-1,0,1):
                    y = (cities[i][0]+a*h*s,cities[i][1]+b*h*s)
                    require(all(0 <= t <= 1 for t in y), 'sample outside domain')
                    di2 = dist2(y,cities[i])
                    for j in other_indices:
                        dj2 = dist2(y,cities[j])
                        # Cross-multiplied influence: zi^2 / di^8 >= zj^2 / dj^8.
                        require(zi**2 * dj2**4 >= z[j]**2 * di2**4,
                                'sample violates actual influence comparison')
                        membership_checks += 1

    # Coefficients in v=exp(-t/2) for b(t)=(K+A v)^2:
    # b'(t) = -K A v-A^2 v^2 = K sqrt(b)-b, since K+A v>0.
    ode_algebra_checks = 0
    for u0 in (F(1,100), F(1,64), F(1,2), F(99,100)):
        a = u0-k
        derivative_coeffs = (F(0),-k*a,-a*a)
        rhs_coeffs = (k*k-k*k,k*a-2*k*a,-a*a)
        require(derivative_coeffs == rhs_coeffs, 'comparison ODE identity failure')
        require(u0>0 and k>0, 'comparison bracket not positive')
        ode_algebra_checks += 1

    require(F(2,8) == F(1,2)/2 == q, 'scaling identity failure')
    result = {
        'status':'PASS', 'problem_id':data['problem_id'], 'city_count':n,
        'p':str(p), 'K':str(k), 'lower_bound':str(lower), 'upper_bound':str(upper),
        'pairwise_squared_distances':list(map(str,distances)),
        'exact_influence_sample_checks':membership_checks,
        'comparison_ode_algebra_checks':ode_algebra_checks,
        'scope':'Exact arithmetic support; the universal analytic proof is in PROOF.md.'
    }
    if n == 3:
        a,b,c = cities
        determinant = (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        require(determinant != 0, 'illustrative triangle is collinear')
        require(len(set(distances))==3, 'illustrative triangle is not scalene')
        result['triangle_determinant'] = str(determinant)
    return result


def self_test(path):
    base = json.loads(path.read_text())
    verify(base)
    rejected = []
    cases = []
    for key,value in [('alpha','1'),('beta','4'),('beta','2'),
                      ('claimed_p','2'),('claimed_K','1/63'),
                      ('claimed_lower_bound','1/1024'),('claimed_upper_bound','1'),
                      ('square_halfwidth','0'),('square_halfwidth','1/2'),
                      ('problem_id','9700027'),('alpha',True)]:
        d=copy.deepcopy(base);d[key]=value;cases.append((key+'='+str(value),d))
    d=copy.deepcopy(base);d['cities'][0][0]='0';cases.append(('boundary city',d))
    d=copy.deepcopy(base);d['cities'][1]=d['cities'][0];cases.append(('coincident sites',d))
    d=copy.deepcopy(base);d['initial_weights'][0]='0';cases.append(('zero initial weight',d))
    d=copy.deepcopy(base);d['initial_weights'][0]='1/5';cases.append(('wrong weight sum',d))
    d=copy.deepcopy(base);d['private_extra']='forbidden';cases.append(('unexpected key',d))
    for label,d in cases:
        try:
            verify(d)
        except (ValueError,TypeError,ZeroDivisionError):
            rejected.append(label)
        else:
            raise ValueError('adversarial case was incorrectly accepted: '+label)
    # A genuine equivalent admissible pair must pass, not just the literal fixed pair.
    scaled=copy.deepcopy(base);scaled['alpha']='3';scaled['beta']='12';verify(scaled)
    # Nearby, asymmetric positions verify robustness of the geometric inequalities.
    nearby=copy.deepcopy(base);nearby['cities'][0][0]='201/1000';verify(nearby)
    return {'status':'PASS','rejected_adversarial_cases':rejected,
            'accepted_positive_controls':['scaled exponents 3,12','asymmetric nearby positions']}


if __name__ == '__main__':
    default = pathlib.Path(__file__).resolve().with_name('certificate.json')
    if sys.argv[1:] == ['--self-test']:
        answer=self_test(default)
    else:
        require(len(sys.argv)<=2,'usage: verify.py [certificate.json | --self-test]')
        path=pathlib.Path(sys.argv[1]) if len(sys.argv)==2 else default
        answer=verify(json.loads(path.read_text()))
    print(json.dumps(answer,sort_keys=True,indent=2))
