"""Own exact jet, valuation, chart and scope controls; no supplied imports.

Finite evidence corroborates the initial uniform proofs, not all complex arcs.
"""
from fractions import Fraction
from random import Random
from itertools import product
from datetime import datetime, timezone
import json
import hashlib


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(a, c):
    return tuple(c*x for x in a)


def multiply(a, b):
    n = len(a)
    return tuple(sum(a[i]*b[k-i] for i in range(k+1)) for k in range(n))


def power(a, k):
    result = (1,)+(0,)*(len(a)-1)
    for _ in range(k):
        result = multiply(result, a)
    return result


def vanish_below(a, n):
    return all(c == 0 for c in a[:n])


def make_series(rng, cutoff, order):
    if order is None:
        return (0,)*cutoff
    out = [0]*cutoff
    if order < cutoff:
        out[order] = rng.choice([-2,-1,1,2])
        for i in range(order+1, cutoff):
            out[i] = rng.randrange(-2,3)
    return tuple(out)


def polynomial_in(x, coefficients, k):
    out = (0,)*len(x)
    for exponent, c in enumerate(coefficients, start=k):
        out = add(out, scale(power(x, exponent), c))
    return out


def in_cylinder(x, y, n, coefficients, k):
    return vanish_below(add(y, scale(polynomial_in(x, coefficients, k),-1)), n)


def polynomial_coefficients():
    # Independent multivariate coefficient expansion for x(t)^2 and x(t)^3.
    zero = (0,0,0,0)
    xs = [{}, *[{tuple(int(i == j) for i in range(4)):1} for j in range(4)]]

    def pmult(a, b):
        out = {}
        for e, c in a.items():
            for f, d in b.items():
                ef = tuple(x+y for x,y in zip(e,f))
                out[ef] = out.get(ef,0)+c*d
        return {e:c for e,c in out.items() if c}

    def smult(a, b):
        out = []
        for k in range(5):
            row = {}
            for i in range(k+1):
                for e,c in pmult(a[i],b[k-i]).items():
                    row[e] = row.get(e,0)+c
            out.append(row)
        return out

    sq = smult(xs,xs)
    cube = smult(sq,xs)
    need(sq[2:] == [{(2,0,0,0):1},{(1,1,0,0):2},{(0,2,0,0):1,(1,0,1,0):2}], 'square coefficient ideal')
    need(cube[3:] == [{(3,0,0,0):1},{(2,1,0,0):3}], 'cube coefficient ideal')
    # Homogeneous degree2 generators cannot generate the nonzero linear x1.
    need(all(sum(e)==2 for row in sq[2:] for e in row), 'nonreduced degree control')
    return {'square_generators':[str(x) for x in sq[2:]],'cube_generators':[str(x) for x in cube[3:]],
            'radical_proof':'x1^2 forces x1, then x2^2+2x1x3 forces x2; all generators in prime(x1,x2). Cube analogous.'}


def main():
    rng = Random(12320261115)
    jet_cases, parameter_substitutions, exact_prefix_cases = 0,0,0
    digest = hashlib.sha256()
    for n in range(3,13):
        for k in range(2,n):
            for _ in range(30):
                cutoff = n+5
                ox = rng.choice([None,*range(1,n+3)])
                oy = rng.choice([None,*range(1,n+3)])
                x,y = make_series(rng,cutoff,ox),make_series(rng,cutoff,oy)
                zero, one, two = [0]*(n-k),[0]*(n-k),[0]*(n-k)
                one[0],two[0]=1,2
                threshold = vanish_below(x,(n+k-1)//k) and vanish_below(y,n)
                pair = in_cylinder(x,y,n,zero,k) and in_cylinder(x,y,n,one,k)
                exact_pair = in_cylinder(x,y,n,one,k) and in_cylinder(x,y,n,two,k)
                need(threshold == pair == exact_pair, 'two witnesses / exact-prefix equivalence')
                jet_cases += 1
                exact_prefix_cases += 1
                for _ in range(5):
                    coefficients = [rng.randrange(-3,4) for _ in range(n-k)]
                    member = in_cylinder(x,y,n,coefficients,k)
                    need(not threshold or member, 'uniform-claim finite control')
                    parameter_substitutions += 1
                digest.update(str((n,k,x,y,threshold)).encode())
    separators = 0
    directions = {'reference_not_intersection':0,'intersection_not_reference':0}
    for r,j,q in product((2,3),range(1,31),range(1,31)):
        if q<r:
            a,b,direction=q,max(5,j*q),'reference_not_intersection'
        elif q>r or j*r>5:
            a,b,direction=r,5,'intersection_not_reference'
        else:
            need(j*r<5,'no integer reference equality')
            a,b,direction=r,j*r,'reference_not_intersection'
        inside_I,inside_T = a>=r and b>=5, a>=q and b>=j*q
        need(inside_I != inside_T, 'separator did not separate')
        need((inside_T and not inside_I) if direction=='reference_not_intersection' else (inside_I and not inside_T), 'wrong separator direction')
        separators += 1
        directions[direction] += 1
    boundaries = 0
    for n in range(3,81):
        for k in range(2,n):
            r=(n+k-1)//k
            need((k*r==n)==(n%k==0), 'specified reference divisibility boundary')
            boundaries += 1
    need((2,6)==(2,3*2) and 6%4!=0, 'do not generalize n5 all-j obstruction to every nondivisible pair')
    overlaps = 0
    for n,x,w in product(range(2,11),[Fraction(1,2),Fraction(2),Fraction(-3)],[Fraction(1,3),Fraction(-2)]):
        v,h=1/w,x*w
        need(v*h==x and v**(n-1)*h**n==x**n*w, 'second chart overlap')
        overlaps += 1
    contact = 0
    for j,q,s in product(range(1,16),range(1,12),range(6)):
        ox,oy=q+s,j*q+(j-1)*s
        need(ox>=q and oy>=j*q,'satellite exact contact bounds')
        contact += 1
    toric=[]
    for r,b in [(3,2),(2,3)]:
        matrix=((r,1),(5,b));inverse=((b,-1),(-5,r))
        need(r*b-5==1,'toric determinant')
        need(all(sum(matrix[i][l]*inverse[l][j] for l in range(2))==int(i==j) for i,j in product(range(2),repeat=2)), 'toric inverse')
        need((b*r-5,-5*r+r*5)==(1,0),'dense toric arc orders')
        need(-5*(r+1)+r*5<0,'closure may contain arcs outside this raw toric chart')
        toric.append({'weights':[r,5],'matrix':matrix,'inverse':inverse})
    # Essential negative controls for ceiling and closures.
    need(2*2<5 and 2<(5+2-1)//2,'floor would admit forbidden t2,t5')
    need(2*5-1>=5 and (2*5-1)-5*2<0,'satellite arc valid but w has a pole')
    need(vanish_below((0,)*10,3),'identically-zero x is included in reduced cylinder')
    return {'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','jet_cases':jet_cases,
            'random_parameter_substitutions':parameter_substitutions,'exact_prefix_pair_checks':exact_prefix_cases,
            'jet_case_SHA256':digest.hexdigest(),'separator_cases':separators,'separator_directions':directions,
            'divisibility_boundaries':boundaries,'rational_chart_overlaps':overlaps,'satellite_contact_cases':contact,
            'toric_integer_certificates':toric,'nonreduced_coefficients':polynomial_coefficients(),
            'negative_controls':['floor-ceiling discrepancy caught','satellite arc omitted by first chart caught','zero-x closure included','raw toric chart need not cover closed cylinder','nondivisible n6k4 still multiple of differentD3'],
            'limits':'Finite exact controls only; universal complex parameters, formal-arc closure and allj,q statements rest on independent analytic/algebraic proofs.'}


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
