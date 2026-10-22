#!/usr/bin/env python3
"""Independent exact, source-level audit; standard library only, no imported author code.

Symbolic coefficients are dictionaries in Z[a,b]. Noncommutative expressions
are dictionaries from tuples of generator indices to coefficient dictionaries.
The finite-field computations supplement, and do not prove, the universal result.
"""
import itertools
import json
from pathlib import Path


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def cadd(*items):
    answer = {}
    for item in items:
        for exponent, value in item.items():
            answer[exponent] = answer.get(exponent, 0) + value
    return {k: v for k, v in answer.items() if v}


def cmul(left, right):
    answer = {}
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            key = (a+c, b+d)
            answer[key] = answer.get(key, 0) + x*y
    return {k: v for k, v in answer.items() if v}


def cneg(item):
    return {k: -v for k, v in item.items()}


ONE = {(0, 0): 1}
NEG = {(0, 0): -1}
ALPHA = {(1, 0): 1}
BETA = {(0, 1): 1}


def nadd(*items):
    answer = {}
    for item in items:
        for word, coefficient in item.items():
            answer[word] = cadd(answer.get(word, {}), coefficient)
    return {w: c for w, c in answer.items() if c}


def nmul(left, right):
    answer = {}
    for w, c in left.items():
        for v, d in right.items():
            word = w+v
            answer[word] = cadd(answer.get(word, {}), cmul(c, d))
    return {w: c for w, c in answer.items() if c}


def nscale(coefficient, expression):
    return {w: cmul(coefficient, c) for w, c in expression.items() if cmul(coefficient, c)}


def nsubstitute(expression, images):
    result = {}
    for word, coefficient in expression.items():
        image = {(): coefficient}
        for letter in word:
            image = nmul(image, images[letter])
        result = nadd(result, image)
    return result


def commutativize(expression):
    result = {}
    for word, coefficient in expression.items():
        word = tuple(sorted(word))
        result[word] = cadd(result.get(word, {}), coefficient)
    return {w: c for w, c in result.items() if c}


def public_source_relations():
    # Independently keyed transcription from the two rendered primary displays.
    return [
        {(1,1): ALPHA, (1,3): NEG, (3,1): ONE, (3,3): cneg(ALPHA)},
        {(1,2): ALPHA, (1,4): NEG, (3,2): ONE, (3,4): cneg(ALPHA)},
        {(2,1): ALPHA, (2,3): NEG, (4,1): ONE, (4,3): cneg(ALPHA)},
        {(2,2): ALPHA, (2,4): NEG, (4,2): ONE, (4,4): cneg(ALPHA)},
        {(1,1): BETA,  (1,2): NEG, (4,1): ONE, (4,2): cneg(BETA)},
        {(1,3): BETA,  (1,4): NEG, (4,3): ONE, (4,4): cneg(BETA)},
    ]


def symbolic_checks():
    source = public_source_relations()
    certificate = json.loads((Path(__file__).resolve().parent/'author'/'certificate.json').read_text())
    decoded = []
    for relation in certificate['relations']:
        row = {}
        for value, a, b, word in relation['terms']:
            row[tuple(word)] = cadd(row.get(tuple(word), {}), {(a,b): value})
        decoded.append(row)
    demand(decoded == source, 'Independent primary-source transcription mismatch')
    X, Y = {(0,): ONE}, {(1,): ONE}
    aliases = {1:X, 2:Y, 3:X, 4:Y}
    Q = {(0,0): BETA, (0,1): NEG, (1,0): ONE, (1,1): cneg(BETA)}
    images = [nsubstitute(relation, aliases) for relation in source]
    demand(images == [{}, {}, {}, {}, Q, Q], 'Six relation images fail')
    theta = {0:nadd(X, nscale(BETA,Y)), 1:nadd(nscale(BETA,X),Y)}
    twistQ = {}
    for (i,j), coefficient in Q.items():
        twistQ = nadd(twistQ, nscale(coefficient, nmul({(i,):ONE},theta[j])))
    demand(commutativize(twistQ) == {}, 'Twisted relation is nonzero')
    det = cadd(ONE, cneg(cmul(BETA,BETA)))
    demand(det == {(0,0):1, (0,2):-1}, 'Wrong determinant')
    # X=U+V and Y=V; generator codes now mean U,V.
    reduced = nsubstitute(Q, {0:nadd(X,Y), 1:Y})
    expected = {(0,0):BETA, (0,1):cadd(BETA,NEG), (1,0):cadd(BETA,ONE)}
    demand(reduced == expected, 'Characteristic-free normal form fails')
    demand(nmul(X,Y) != nmul(Y,X), 'Word order has been lost')
    demand(commutativize(Q) != {}, 'Untwisted polynomial target incorrectly works generically')
    # Inverse-lift control: replace beta by -beta in theta, while leaving Q fixed.
    inverse = {0:nadd(X,nscale(cneg(BETA),Y)), 1:nadd(nscale(cneg(BETA),X),Y)}
    wrong = {}
    for (i,j), coefficient in Q.items():
        wrong = nadd(wrong, nscale(coefficient,nmul({(i,):ONE},inverse[j])))
    demand(commutativize(wrong) != {}, 'Inverse coordinate action not detected')
    # The excluded beta=1 and beta=-1 relations genuinely factor in the free algebra.
    for beta, factor in [(1,nmul(nadd(X,Y),nadd(X,nscale(NEG,Y)))),
                         (-1,nscale(NEG,nmul(nadd(X,nscale(NEG,Y)),nadd(X,Y))))]:
        specialized = {w:{(0,0):sum(c*beta**b for (a,b),c in coefficient.items())}
                       for w,coefficient in Q.items()}
        demand(specialized == factor, 'Singular boundary factorization failed')
    # Scalar quotient, independently of the projective-line proof.
    demand(all(not nsubstitute(r,{i:X for i in range(1,5)}) for r in source), 'Scalar quotient failed')
    return {'source_relation_images':[0,0,0,0,'Q','Q'],
            'twisted_Q':0, 'determinant':'1-beta^2',
            'normal_relation':'beta*UU+(beta-1)*UV+(beta+1)*VU',
            'integer_polynomial_identities':True,
            'negative_controls':['noncommutative_word_order','untwisted_target','inverse_lift'],
            'singular_boundary_factorizations':True}


class Field:
    def __init__(self, p, extension=False):
        self.p, self.extension = p, extension
        self.name = 'GF(4)' if extension else 'GF(%d)' % p
    def add(self,x,y):
        return x ^ y if self.extension else (x+y)%self.p
    def neg(self,x):
        return x if self.extension else (-x)%self.p
    def mul(self,x,y):
        if not self.extension:
            return x*y%self.p
        out = 0
        while y:
            if y&1: out ^= x
            y >>= 1
            x <<= 1
            if x&4: x ^= 7  # z^2+z+1
        return out
    def inv(self,x):
        demand(x != 0, 'Division by zero')
        return self.mul(x,x) if self.extension else pow(x,self.p-2,self.p)


def rank(rows, field):
    pivots = {}
    for input_row in rows:
        row = {j:x for j,x in enumerate(input_row) if x}
        while row:
            col = min(row)
            if col not in pivots:
                inv = field.inv(row[col])
                pivots[col] = {j:field.mul(x,inv) for j,x in row.items()}
                break
            multiple = row[col]
            for j,x in pivots[col].items():
                value = field.add(row.get(j,0), field.neg(field.mul(multiple,x)))
                if value: row[j] = value
                else: row.pop(j,None)
    return len(pivots)


def multiply_forms(left,right,field):
    out = [0]*(len(left)+len(right)-1)
    for i,x in enumerate(left):
        for j,y in enumerate(right):
            out[i+j] = field.add(out[i+j],field.mul(x,y))
    return out


def finite_check(field,beta,max_degree=8):
    # Ordinary homogeneous forms represented by increasing powers of t.
    demand(field.add(1,field.neg(field.mul(beta,beta))) != 0, 'Singular finite-field example')
    theta_powers = [([1,0],[0,1])]
    for unused in range(max_degree):
        a,b = theta_powers[-1]
        theta_powers.append((
            [field.add(a[j],field.mul(beta,b[j])) for j in (0,1)],
            [field.add(field.mul(beta,a[j]),b[j]) for j in (0,1)]))
    results = []
    for degree in range(max_degree+1):
        words = list(itertools.product((0,1),repeat=degree))
        index = {w:i for i,w in enumerate(words)}
        evaluations = []
        for word in words:
            value = [1]
            for j,letter in enumerate(word):
                value = multiply_forms(value,theta_powers[j][letter],field)
            evaluations.append(value)
        target_rank = rank(evaluations,field)
        consequences = []
        if degree >= 2:
            for split in range(degree-1):
                for prefix in itertools.product((0,1),repeat=split):
                    for suffix in itertools.product((0,1),repeat=degree-2-split):
                        row = [0]*len(words)
                        for pair,c in [((0,0),beta),((0,1),field.neg(1)),
                                       ((1,0),1),((1,1),field.neg(beta))]:
                            row[index[prefix+pair+suffix]]=c
                        consequences.append(row)
        relation_rank = rank(consequences,field)
        quotient_dimension = 2**degree-relation_rank
        demand(target_rank == quotient_dimension == degree+1,
               '%s beta=%d degree=%d rank mismatch' % (field.name,beta,degree))
        # Every generated consequence must vanish after the twisted-word map.
        for row in consequences:
            for column in range(degree+1):
                value = 0
                for coefficient,evaluation in zip(row,evaluations):
                    value = field.add(value,field.mul(coefficient,evaluation[column]))
                demand(value == 0, 'A relation consequence survives in target')
        results.append({'degree':degree,'relation_rank':relation_rank,
                        'quotient_dimension':quotient_dimension,'target_rank':target_rank})
    return {'field':field.name,'beta':beta,'degrees':results}


def main():
    result = {'status':'PASS','symbolic':symbolic_checks(),
              'finite_support_only':True,
              'finite_field_checks':[finite_check(Field(2,True),2),finite_check(Field(2,True),3),
                                     finite_check(Field(5),2),finite_check(Field(7),3)],
              'universal_proof_location':'mathematical_audit.md',
              'author_code_imported':False}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
