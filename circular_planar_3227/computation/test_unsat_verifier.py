import copy
import json
import os
from verify_unsat_certificate import verify
with open(os.path.join(os.path.dirname(__file__), 'dodecahedron_17_6_unsat.json')) as f:
    data = json.load(f)
verify(data)
mutations = []
bad = copy.deepcopy(data)
bad['tree']['children'].pop()
mutations.append(bad)
bad = copy.deepcopy(data)
bad['tree']['children'].append(copy.deepcopy(bad['tree']['children'][0]))
mutations.append(bad)
bad = copy.deepcopy(data)
bad['tree']['remaining_domain'] = [6]
mutations.append(bad)
bad = copy.deepcopy(data)
bad['tree'] = {'leaf': 'contradiction', 'rejected_vertex': 0, 'rejected_domains': [[]]*20}
mutations.append(bad)
bad = copy.deepcopy(data)
bad['symmetry']['neighbor'] = bad['symmetry']['root']
mutations.append(bad)
bad = copy.deepcopy(data)
bad['p'], bad['q'] = 20,7
mutations.append(bad)
for bad in mutations:
    try:
        verify(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('Accepted corrupt UNSAT certificate')
print('PASS: exhaustive UNSAT certificate accepted; six corruptions rejected.')
