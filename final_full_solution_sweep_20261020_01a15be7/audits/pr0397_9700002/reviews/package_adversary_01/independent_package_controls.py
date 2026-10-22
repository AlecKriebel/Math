#!/usr/bin/env python3
"""Independent exact optimal-face and malformed-input attacks; no service writes."""
import ast
import copy
import datetime as dt
from fractions import Fraction as Q
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random
import subprocess
import tempfile
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'extracted/congestion-fragmentation-verification'
CHECKS = []

def record(name, detail):
    CHECKS.append({'name': name, 'passed': True, 'detail': detail})

def solve(a, b):
    matrix = [[Q(x) for x in row] + [Q(v)] for row, v in zip(a, b)]
    n = len(b)
    for c in range(n):
        pivot = next((r for r in range(c, n) if matrix[r][c]), None)
        if pivot is None:
            return None
        matrix[c], matrix[pivot] = matrix[pivot], matrix[c]
        z = matrix[c][c]
        matrix[c] = [v/z for v in matrix[c]]
        for r in range(n):
            if r != c:
                z = matrix[r][c]
                matrix[r] = [u-z*v for u, v in zip(matrix[r], matrix[c])]
    return tuple(row[-1] for row in matrix)

def vertices(d):
    a, b = [], []
    for i in range(4):
        unit = [int(j == i) for j in range(4)]
        a.extend([unit, [-x for x in unit]])
        b.extend([d[i], Q(0)])
    a.extend([[1,1,0,0], [0,0,1,1], [1,0,1,0], [0,1,0,1]])
    b.extend([Q(4)]*4)
    result = set()
    for active in itertools.combinations(range(12), 4):
        v = solve([a[i] for i in active], [b[i] for i in active])
        if v is not None and all(sum(x*y for x, y in zip(row, v)) <= z for row, z in zip(a, b)):
            result.add(v)
    return result

def cut_value(x, t):
    values = []
    for mask in range(16):
        left = [i for i in range(2) if mask & (1 << i)]
        right = [j for j in range(2) if mask & (1 << (2+j))]
        rectangle = [2*i+j for i in left for j in range(2) if j not in right]
        values.append(4*(2-len(left)+len(right)) + sum(1+(t-1)*x[q] for q in rectangle))
    return min(values)

rng = random.Random(2026102139701)
models = [tuple([Q(1,5)]*4), tuple([Q(1)]*4), tuple([Q(5)]*4), (Q(5),Q(5),Q(1,5),Q(1,5))]
models += [tuple(Q(rng.randrange(1,36), 7) for _ in range(4)) for _ in range(12)]
face_cases = optimum_vertices = degenerate_faces = 0
for x in models:
    for t in [Q(1), Q(3,2), Q(2), Q(3), Q(7)]:
        d = tuple(1+(t-1)*v for v in x)
        vs = vertices(d)
        optimum = max(map(sum, vs))
        face = [v for v in vs if sum(v) == optimum]
        assert optimum == cut_value(x, t)
        strict = max(d[0]+d[1],d[2]+d[3],d[0]+d[2],d[1]+d[3]) < 4
        if strict:
            assert face == [d]
        if optimum == 8:
            assert all(v[0]+v[1] == v[2]+v[3] == v[0]+v[2] == v[1]+v[3] == 4 for v in face)
        face_cases += 1
        optimum_vertices += len(face)
        degenerate_faces += len(face) > 1
record('exact all-optimal-vertex enumeration', {'instances': face_cases, 'optimal_vertices': optimum_vertices, 'nontrivial_optimal_faces':degenerate_faces, 'method':'Enumerate all 4-active-constraint vertices; solve with Fraction Gaussian elimination; no flow or LP imports.'})

spec = importlib.util.spec_from_file_location('reviewed_replay', PACKAGE/'replay.py')
replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(replay)
binding, policy = replay.load_controls(PACKAGE)
runtime = replay.runtime_versions()
expected = {name:(PACKAGE/'candidate'/file).read_bytes() for name,script,file,produced in replay.COMPONENTS}
base = {name:replay.strict_json(data) for name,data in expected.items()}
base['portable'].update(runtime)
base['portable']['checks'][0] = copy.deepcopy(policy['portable_metadata']['public_projection'])
rejects = []
def rejected(name, fn):
    try:
        fn()
    except Exception as error:
        rejects.append({'name':name, 'error_type':type(error).__name__, 'reason':str(error)})
    else:
        raise AssertionError('False acceptance: ' + name)

# Mutate every leaf outside approved fields, not just a fixed list of flags.
def leaves(v, path=()):
    if type(v) is dict:
        for k,w in v.items():
            yield from leaves(w, path+(k,))
    elif type(v) is list:
        for i,w in enumerate(v):
            yield from leaves(w,path+(i,))
    else:
        yield path,v

for component in base:
    exemptions = set(policy['float_tolerances'].get(component, {}))
    if component == 'portable':
        exemptions |= {'/python','/numpy','/scipy','/checks/0/name','/checks/0/files'}
    for path, value in leaves(base[component]):
        pointer = '/'+'/'.join(map(str,path))
        if pointer in exemptions:
            continue
        changed = copy.deepcopy(base[component]); parent = changed
        for key in path[:-1]:
            parent = parent[key]
        if type(value) is bool:
            replacement = not value
        elif type(value) is int:
            replacement = value+1
        elif type(value) is float:
            replacement = value+1.0
        elif type(value) is str:
            replacement = value+' UNREVIEWED'
        else:
            replacement = 'UNREVIEWED'
        parent[path[-1]] = replacement
        rejected(component+pointer, lambda component=component,changed=changed:replay.compare_component(expected[component],json.dumps(changed,allow_nan=False).encode(),component,policy,runtime))
record('unapproved output leaf mutations', {'rejected':len(rejects), 'method':'Every scalar in all three complete output records outside declared exceptions was independently changed and compared through the production byte/typed comparator.'})

before = len(rejects)
for data in [b'{', b'[]', b'null', b'NaN', b'{"a":{"b":1,"b":2}}',b'{"a":[1e999]}', b'\xff']:
    rejected('malformed or wrong-schema output '+repr(data),lambda data=data:replay.compare_component(expected['turn1'],data,'turn1',policy,runtime))
for flag in [0,1,True,False,1.0,None,'true',[],{}]:
    if flag is True:
        continue
    changed=copy.deepcopy(base['turn1']);changed['all_assertions_passed']=flag
    rejected('pass flag wrong type/value '+repr(flag),lambda changed=changed:replay.compare_records(replay.strict_json(expected['turn1']),changed,'turn1',policy,runtime))
record('additional malformed and type attacks', {'rejected':len(rejects)-before})

# Extract and test the actual account-pagination function without importing its
# credential-reading dependencies or executing the live main function.
gate = HERE.parents[1]/'prepublication_check.py'
tree=ast.parse(gate.read_text())
function=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='account_search')
namespace={'urlencode':urlencode}
exec(compile(ast.Module(body=[function],type_ignores=[]),str(gate),'exec'),namespace)
account_search=namespace['account_search']
class Client:
    base='https://example.invalid'
    def __init__(self, pages): self.pages=iter(pages);self.calls=[]
    def request(self,method,url): self.calls.append((method,url));return next(self.pages)
def page(total,ids,next_url=None):
    return {'hits':{'total':total,'hits':[{'id':str(i)} for i in ids]},'links':({'next':next_url} if next_url else {})}
client=Client([page({'relation':'eq','value':3},[1,2],'https://example.invalid/page2'),page(3,[3])])
assert account_search(client,'')['total']==3 and len(client.calls)==2 and all(x[0]=='GET' for x in client.calls)
before=len(rejects)
for name,pages in [
 ('inexact total',[page({'relation':'gte','value':2},[1,2])]),
 ('changed total',[page(2,[1],'https://example.invalid/2'),page(3,[2])]),
 ('duplicate records',[page(2,[1],'https://example.invalid/2'),page(2,[1])]),
 ('incomplete listing',[page(2,[1])]),
 ('pagination loop',[page(2,[1],'https://example.invalid/2'),page(2,[2],'https://example.invalid/2')]),
 ('missing total',[page(None,[])])]:
    rejected('account '+name,lambda pages=pages:account_search(Client(pages),''))
record('offline complete-account pagination attacks',{'accepted_complete_two_page_listing':True,'required_rejections':len(rejects)-before,'gate_sha256':hashlib.sha256(gate.read_bytes()).hexdigest(),'live_code_main_invoked':False})

# Missing-source and wrong-schema integration paths must retain evidence while
# failing before any historical component can run.
with tempfile.TemporaryDirectory(dir=HERE,prefix='own-fixtures-') as temp:
    import shutil
    temp=Path(temp)
    for label,mutation in [('missing_source',lambda p:(p/'turns/turn_02/CANDIDATE.md').unlink()),('unexpected_empty_dir',lambda p:(p/'review/unreviewed').mkdir()),('changed_checker',lambda p:(p/'turns/turn_02/check_model.py').write_text('print(1)'))]:
        candidate=temp/label;shutil.copytree(PACKAGE/'candidate',candidate);mutation(candidate)
        output=HERE/('own_integration_'+label)
        run=subprocess.run([__import__('sys').executable,'-B',str(PACKAGE/'replay.py'),'--candidate',str(candidate),'--output',str(output)],capture_output=True,text=True)
        receipt=json.loads((output/'receipt.json').read_text())
        assert run.returncode!=0 and receipt['status']=='failed' and not receipt['components']
        record('integration '+label,{'exit_code':run.returncode,'components_started':0,'retained_receipt':str(output.relative_to(HERE))+'/receipt.json'})

result={'timestamp':dt.datetime.now(dt.timezone.utc).isoformat(),'all_assertions_passed':True,'checks':CHECKS,'required_rejections':rejects,'scope':'Independent exact finite optimal-face controls plus production-wrapper and pagination falsification. No theorem, novelty or current live-state conclusion follows from these finite controls.'}
(HERE/'INDEPENDENT_PACKAGE_CONTROLS.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({'all_assertions_passed':True,'checks':CHECKS,'required_rejections':len(rejects)},indent=2))
