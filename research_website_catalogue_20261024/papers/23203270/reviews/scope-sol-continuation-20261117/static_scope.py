"""Static source/provenance comparison only. Never imports native source code."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re

LANE=Path(__file__).resolve().parent
PACKAGE=LANE.parents[1]/'sources/archives/01-source-and-verification.zip.extracted'
prov=json.loads((PACKAGE/'provenance/lean_source_hashes.json').read_text())
checks=[]
for item in prov['sources']:
    name=item['source']
    if not name.startswith('lean/OAI/'): continue
    path=PACKAGE/name;data=path.read_bytes()
    assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    text=data.decode()
    imports=re.findall(r'^import\s+(\S+)',text,re.M)
    checks.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                   'lines':len(text.splitlines()),'imports':imports})
assert len(checks)==55
actual_modules={i['path'][5:-5].replace('/','.') for i in checks}
assert actual_modules==set(prov['closure_modules'])
for item in checks:
    for module in item['imports']:
        assert module=='Mathlib' or module in actual_modules,module
model=(PACKAGE/'lean/OAI/Algebra/AffineCancellation/Model.lean').read_text()
comparator=(LANE/'primary-pinned/lean/ComparatorChallenges/ComplexCancellation.lean').read_text()
prefix=model.split('\nend ComplexCancellation')[0]
assert comparator.startswith(prefix)
native=[]
for name in ['check_stabilization.py','check_nonpolynomiality_certificates.py']:
    data=(PACKAGE/name).read_bytes()
    tree=ast.parse(data.decode(),filename=name)
    native.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                   'all_own_function_definitions':[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)],
                   'literal_check_calls':sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check' for n in ast.walk(tree)),
                   'entrypoint_and_all_own_called_bodies_personally_read':True,
                   'source_ast_parsed_without_execution':True})
result={'utc':datetime.now(timezone.utc).isoformat(),'scope':'Static integrity and selected semantic-source inspection, not kernel certification',
        'unchanged_lean_closure_modules':checks,'closure_count':55,'closure_total_lines':sum(i['lines'] for i in checks),
        'all_imports_resolve_within_closure_or_Mathlib':True,'model_prefix_equals_actual_pinned_comparator_definitions':True,
        'formal_modules_personally_read_complete':['Model','Main','Dimension','EquivariantLift','PositiveObstruction','Determinant','Bundle','OrbitRigidity','HighestWeight'],
        'all_55_formal_proof_bodies_personally_read':False,'kernel_builds_attempted_in_this_lane':0,
        'native_python_source_inspection':native,'other_native_routes_executed':0}
(LANE/'STATIC_SCOPE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'lean_closure_matches':len(checks),'lines':result['closure_total_lines'],
                  'model_matches_comparator':True,'native_sources_statically_parsed':len(native)}))
