#!/usr/bin/env python3
"""Exact finite algebra only. This is not a proof of shy-coupling rigidity."""
import argparse
import itertools
import json
import pathlib
import sys

def need(condition, message):
    if not condition:
        raise ValueError(message)

def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        need(key not in obj, 'duplicate JSON key')
        obj[key] = value
    return obj

def integer(value, low=-1000, high=1000):
    need(type(value) is int and low <= value <= high, 'bounded exact integer required')
    return value

def matrix(value, size):
    need(type(value) is list and len(value) == size, 'wrong matrix height')
    for row in value:
        need(type(row) is list and len(row) == size, 'wrong matrix width')
        for item in row:
            integer(item)
    return value

def multiply(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def transpose(a):
    return [list(row) for row in zip(*a)]

def identity(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]

def verify(path):
    raw = path.read_bytes()
    need(len(raw) <= 16384, 'certificate too large')
    data = json.loads(raw, object_pairs_hook=unique_object,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    keys = {'schema','weights','marginal_generator','states','joint_generator',
            'automorphisms','product_map','perverse_J','difference_covariance'}
    need(type(data) is dict and set(data) == keys, 'certificate schema')
    need(type(data['schema']) is int and data['schema'] == 1, 'schema version')
    w = data['weights']
    need(type(w) is list and len(w) == 3, 'three edge weights required')
    for x in w:
        integer(x, 1, 100)
    need(len(set(w)) == 3, 'distinct edge weights required')
    q = [[0,w[0],w[1]],[w[0],0,w[2]],[w[1],w[2],0]]
    for i in range(3):
        q[i][i] = -sum(q[i])
    need(matrix(data['marginal_generator'],3) == q, 'marginal generator mismatch')
    states = [[i,j] for i in range(3) for j in range(3) if i != j]
    need(data['states'] == states, 'ordered off-diagonal state inventory')
    # Reject bools even though Python equality treats True as 1.
    for pair in data['states']:
        need(type(pair) is list and len(pair) == 2, 'pair schema')
        for item in pair:
            integer(item,0,2)
    L = [[0]*6 for _ in range(6)]
    for row,(i,j) in enumerate(states):
        k = next(k for k in range(3) if k not in (i,j))
        for target,rate in [([j,i],q[i][j]),([k,j],q[i][k]),([i,k],q[j][k])]:
            L[row][states.index(target)] += rate
        L[row][row] = -sum(L[row])
    need(matrix(data['joint_generator'],6) == L, 'joint generator mismatch')
    for r,pair in enumerate(states):
        need(sum(L[r]) == 0, 'joint row sum')
        for c in range(6):
            need(r == c or L[r][c] >= 0, 'negative jump rate')
        for coordinate in (0,1):
            for target in range(3):
                actual = sum(L[r][c] for c,s in enumerate(states) if s[coordinate] == target)
                need(actual == q[pair[coordinate]][target], 'marginal-generator failure')
    need(all(sum(L[r][c] for r in range(6)) == 0 for c in range(6)), 'uniform stationarity failure')
    automorphisms = [list(p) for p in itertools.permutations(range(3))
                     if all(q[p[i]][p[j]] == q[i][j] for i in range(3) for j in range(3))]
    need(automorphisms == [[0,1,2]], 'nontrivial symmetry')
    need(type(data['automorphisms']) is list, 'automorphism list')
    for p in data['automorphisms']:
        need(type(p) is list and len(p) == 3, 'permutation schema')
        for item in p:
            integer(item,0,2)
    need(data['automorphisms'] == automorphisms, 'reported automorphisms mismatch')
    R = matrix(data['product_map'],3)
    need(R == [[-1,0,0],[0,-1,0],[0,0,1]], 'product-map mismatch')
    need(multiply(R,transpose(R)) == identity(3), 'product-map orthogonality')
    J = matrix(data['perverse_J'],2)
    need(J == [[1,0],[0,-1]], 'perverse matrix mismatch')
    need(multiply(J,transpose(J)) == identity(2), 'perverse orthogonality')
    sigma = [[2*int(i==j)-J[i][j]-J[j][i] for j in range(2)] for i in range(2)]
    need(matrix(data['difference_covariance'],2) == sigma, 'covariance mismatch')
    need(sigma[0][0] == 0 and sum(sigma[i][i] for i in range(2)) == 4,
         'radial-zero positive-trace control')
    return {'verified':True,'state_count':6,'marginal_checks':36,
            'permutations_checked':6,'identity_only':True,
            'product_map_is_rigid':True,'radial_variance':0,'covariance_trace':4,
            'scope':'exact finite algebra; not the Euclidean conjecture'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('certificate',type=pathlib.Path)
    args = parser.parse_args()
    try:
        result = verify(args.certificate)
    except (ValueError,TypeError,KeyError,IndexError,OSError,UnicodeError) as exc:
        print(json.dumps({'verified':False,'error':str(exc)},sort_keys=True))
        return 2
    print(json.dumps(result,sort_keys=True))
    return 0

if __name__ == '__main__':
    sys.exit(main())
