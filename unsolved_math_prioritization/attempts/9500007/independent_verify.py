#!/usr/bin/env python3
"""Independent exact audit of the authored finite certificate; no analytic proof."""
import itertools
import json
import pathlib
import sys
from fractions import Fraction

def require(ok, label):
    if not ok:
        raise ValueError(label)

def unique(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, 'duplicate JSON key')
        result[k] = v
    return result

def integer_tree(x):
    if isinstance(x, list):
        for y in x:
            integer_tree(y)
    else:
        require(type(x) is int, 'only exact integers allowed in arrays')

def square(x, n):
    require(type(x) is list and len(x) == n, 'matrix rows')
    require(all(type(row) is list and len(row) == n for row in x), 'matrix columns')
    integer_tree(x)

def verify(path):
    raw = path.read_bytes()
    require(len(raw) <= 16384, 'oversized certificate')
    data = json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite')))
    keys = {'schema','weights','marginal_generator','states','joint_generator',
            'automorphisms','product_map','perverse_J','difference_covariance'}
    require(type(data) is dict and set(data) == keys, 'schema keys')
    require(type(data['schema']) is int and data['schema'] == 1, 'schema version')
    for key in keys - {'schema'}:
        integer_tree(data[key])
    w = data['weights']
    require(type(w) is list and len(w) == 3 and len(set(w)) == 3, 'three distinct weights')
    require(all(1 <= z <= 100 for z in w), 'weight range')
    q = data['marginal_generator']; square(q, 3)
    require([q[0][1],q[0][2],q[1][2]] == w, 'weight assignment')
    for i in range(3):
        require(sum(q[i]) == 0 and q[i][i] < 0, 'marginal conservation')
        for j in range(3):
            require(q[i][j] == q[j][i], 'marginal reversibility')
            require(i == j or q[i][j] > 0, 'marginal irreducibility')
    states = data['states']
    require(states == [list(s) for s in itertools.permutations(range(3),2)], 'state inventory')
    l = data['joint_generator']; square(l, 6)
    # Check the supplied operator on a basis of functions of each coordinate.
    for row,(i,j) in enumerate(states):
        require(sum(l[row]) == 0, 'joint conservation')
        for col,(u,v) in enumerate(states):
            require(l[row][col] == l[col][row], 'joint symmetry')
            require(row == col or l[row][col] >= 0, 'joint jump positivity')
            if row != col and l[row][col] > 0 and u != i and v != j:
                require((u,v) == (j,i), 'only exchange may move both coordinates')
                require(l[row][col] == q[i][j], 'exchange rate')
        for coordinate in (0,1):
            start = (i,j)[coordinate]
            for target in range(3):
                observed = sum(l[row][col] * int(state[coordinate] == target)
                               for col,state in enumerate(states))
                require(observed == q[start][target], 'generator lumpability')
    # Exact invariant weights and their two pushforwards.
    weights = [Fraction(1,6)]*6
    invariant = [sum(weights[i]*l[i][j] for i in range(6)) for j in range(6)]
    require(invariant == [0]*6, 'joint invariant weights')
    for coord in (0,1):
        require([sum(weights[i] for i,s in enumerate(states) if s[coord] == j)
                 for j in range(3)] == [Fraction(1,3)]*3, 'invariant marginal')
    # All 3^3 functions, not just the permutations: impose uniform pushforward
    # first and then the semigroup-generator condition for that bijection.
    preserving = []; compatible = []
    for f in itertools.product(range(3), repeat=3):
        if [f.count(j) for j in range(3)] != [1,1,1]:
            continue
        preserving.append(f)
        if all(q[i][j] == q[f[i]][f[j]] for i in range(3) for j in range(3)):
            compatible.append(list(f))
    require(compatible == [[0,1,2]] == data['automorphisms'], 'function rigidity')
    r = data['product_map']; square(r,3)
    require(r == [[-1,0,0],[0,-1,0],[0,0,1]], 'printed product map')
    require(all(sum(r[i][k]*r[j][k] for k in range(3)) == int(i==j)
                for i in range(3) for j in range(3)), 'orthogonal product map')
    j = data['perverse_J']; square(j,2)
    require(j == [[1,0],[0,-1]], 'noise example')
    a = [[int(i==k)-j[i][k] for k in range(2)] for i in range(2)]
    sigma = [[sum(a[i][k]*a[h][k] for k in range(2)) for h in range(2)] for i in range(2)]
    square(data['difference_covariance'],2)
    require(sigma == [[0,0],[0,4]] == data['difference_covariance'], 'difference covariance')
    require(sum(sigma[i][i] for i in range(2)) == 4 and sigma[0][0] == 0, 'radial versus full covariance')
    # The six equations force the connection coefficients in the C2 proof to
    # vanish. Verify the purely algebraic permutation/sign chain symbolically.
    chain = [((0,1,2),1),((1,0,2),1),((1,2,0),-1),
             ((2,1,0),-1),((2,0,1),1),((0,2,1),1),((0,1,2),-1)]
    for pos in range(6):
        (a,sa),(b,sb) = chain[pos],chain[pos+1]
        if pos % 2 == 0:
            require(b == (a[1],a[0],a[2]) and sa == sb, 'mixed-partial symmetry chain')
        else:
            require(b == (a[0],a[2],a[1]) and sa == -sb, 'metric-derivative antisymmetry chain')
    return {'verified':True,'joint_states':6,'marginal_basis_checks':36,
            'all_functions_checked':27,'uniform_preserving_functions':len(preserving),
            'compatible_functions':compatible,'invariant_weights':'1/6 each',
            'zero_radial_variance':True,'positive_covariance_trace':4,
            'scope':'Finite exact algebra only; analytic proofs are separately audited.'}

if __name__ == '__main__':
    try:
        result = verify(pathlib.Path(sys.argv[1]))
    except (ValueError,TypeError,KeyError,IndexError,OSError,UnicodeError) as exc:
        print(json.dumps({'verified':False,'error':str(exc)}, sort_keys=True))
        sys.exit(2)
    print(json.dumps(result, sort_keys=True))
