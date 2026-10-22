"""Negative controls ensure the independent verifier rejects broken certificates."""
import copy
import glob
import json
import os
from verify_certificate import verify

base = os.path.dirname(os.path.abspath(__file__))
paths = sorted(glob.glob(os.path.join(base, '*_20_7.json')))
assert len(paths) == 7
for path in paths:
    with open(path) as f:
        data = json.load(f)
    verify(data)
    u, v = data['edges'][0]
    mutations = []
    invalid = copy.deepcopy(data)
    invalid['colors'][str(v)] = invalid['colors'][str(u)]
    mutations.append(invalid)
    invalid = copy.deepcopy(data)
    del invalid['colors'][str(u)]
    mutations.append(invalid)
    invalid = copy.deepcopy(data)
    invalid['colors'][str(u)] = data['p']
    mutations.append(invalid)
    invalid = copy.deepcopy(data)
    invalid['edges'].append([u, u])
    mutations.append(invalid)
    invalid = copy.deepcopy(data)
    invalid['edges'].append([v, u])
    mutations.append(invalid)
    for invalid in mutations:
        try:
            verify(invalid)
        except AssertionError:
            pass
        else:
            raise AssertionError('Accepted invalid certificate: ' + path)
print('PASS: seven valid certificates accepted; 35 corruptions rejected.')
